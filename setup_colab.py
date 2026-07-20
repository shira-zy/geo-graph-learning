"""
setup_colab.py — centralized Colab quirks for the Geospatial Graph Learning course.

Every demo notebook starts with a setup cell like:

    !wget -q https://raw.githubusercontent.com/bgalon/geo-graph-learning/main/setup_colab.py
    from setup_colab import setup_unit
    setup_unit("unit-1")

This file fixes-once and updates-everywhere. When Colab breaks something,
patch the relevant `_unit_N_setup()` here and every notebook recovers.

LAYERS:
    A) requirements file fetch — pulls `requirements/<unit>.txt` from main.
    B) PyG ecosystem (unit-5) — runtime torch+CUDA detection → matching wheels.
    C) NetworkX fallback flag for pandana (unit-4) — set in unit-4 setup.
    D) Geopandas/shapely/pyproj/fiona pinning — pinned together in requirements.

This file is intentionally dependency-free. It must run on a fresh Colab
runtime with nothing installed.
"""

from __future__ import annotations

import os
import subprocess
import sys
import urllib.request
from typing import Optional

REPO_RAW = "https://raw.githubusercontent.com/bgalon/geo-graph-learning"
REPO_REF = os.environ.get("GEO_COURSE_REF", "main")  # override to pin to a tag


def _on_colab() -> bool:
    return "google.colab" in sys.modules


def _pip_install(*args: str) -> None:
    cmd = [sys.executable, "-m", "pip", "install", "-q", *args]
    print(f"  $ {' '.join(cmd[3:])}")
    subprocess.run(cmd, check=True)


# Core scientific packages Colab ships preloaded. If a slim install bumps one of
# these transitively, the in-memory copy goes ABI-inconsistent and the runtime
# must be restarted before the smoke test will pass (numpy '_center' break).
_CORE_PKGS = ("numpy", "pandas", "scipy")


def _installed_versions(pkgs: tuple[str, ...]) -> dict[str, Optional[str]]:
    import importlib.metadata as im

    out: dict[str, Optional[str]] = {}
    for p in pkgs:
        try:
            out[p] = im.version(p)
        except im.PackageNotFoundError:
            out[p] = None
    return out


def _warn_if_core_changed(before: dict[str, Optional[str]]) -> None:
    """If pip bumped a core package this session, the loaded copy is now stale.

    Compare on-disk metadata before vs. after install. A diff means Colab's
    already-imported numpy/pandas/scipy no longer matches what's installed —
    a runtime restart is required before anything imports cleanly.
    """
    after = _installed_versions(_CORE_PKGS)
    changed = [p for p in _CORE_PKGS if before.get(p) != after.get(p)]
    if not changed:
        return
    details = ", ".join(f"{p} {before.get(p)} → {after.get(p)}" for p in changed)
    bar = "=" * 72
    print(
        "\n" + bar + "\n"
        "⚠️  A CORE PACKAGE CHANGED DURING INSTALL — RUNTIME RESTART NEEDED\n"
        f"      {details}\n"
        "    Colab's in-memory copy is now ABI-inconsistent (numpy '_center' break).\n"
        "    ➜  Runtime → Restart session, then re-run from the smoke-test cell.\n"
        "    (See this unit's KNOWN_ISSUES.md if the smoke test still fails.)\n"
        + bar + "\n"
    )


def _fetch_requirements(unit: str) -> list[str]:
    url = f"{REPO_RAW}/{REPO_REF}/requirements/{unit}.txt"
    print(f"  fetching {url}")
    text = urllib.request.urlopen(url).read().decode("utf-8")
    # Strip blank lines + comments
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def setup_unit(unit: str) -> None:
    """Install everything the given unit needs.

    On Colab: pip-install the unit's requirements file + handle PyG/pandana quirks.
    Off Colab: assumes the user has run `uv sync --extra <unit>` already; no-op.
    """
    if not _on_colab():
        print(f"[setup_colab] Not on Colab — assuming local uv env. Skipping install for {unit}.")
        return

    print(f"[setup_colab] Setting up {unit} on Colab…")

    # Layer A — common path: install from the unit's pinned requirements.
    # A missing/unfetchable/empty requirements file is FATAL: without it nothing
    # installs and the smoke-test cell fails later with a confusing
    # ModuleNotFoundError. Fail loudly HERE, at the real cause.
    try:
        reqs = _fetch_requirements(unit)
    except Exception as exc:
        raise RuntimeError(
            f"[setup_colab] Could not fetch requirements/{unit}.txt from "
            f"{REPO_RAW}/{REPO_REF}/requirements/{unit}.txt ({exc}).\n"
            f"The unit's requirements are probably not published on "
            f"'{REPO_REF}' yet. Fix: run scripts/export-requirements.sh and "
            f"push requirements/{unit}.txt, or set GEO_COURSE_REF to a branch/"
            f"tag that has it. See the unit's KNOWN_ISSUES.md."
        ) from exc

    if not reqs:
        raise RuntimeError(
            f"[setup_colab] requirements/{unit}.txt is empty — nothing to "
            f"install. Populate the '{unit}' extra in pyproject.toml and run "
            f"scripts/export-requirements.sh before running this notebook."
        )

    before = _installed_versions(_CORE_PKGS)
    _pip_install(*reqs)
    _warn_if_core_changed(before)

    # Layer B — unit-specific quirks.
    handler = {
        "unit-1": _unit_1_setup,
        "unit-2": _unit_2_setup,
        "unit-3": _unit_3_setup,
        "unit-4": _unit_4_setup,
        "unit-5": _unit_5_setup,
    }.get(unit)

    if handler is not None:
        handler()

    print(f"[setup_colab] {unit} ready.")


# ---------------------------------------------------------------------------
# Per-unit quirk handlers. Patched as we discover Colab breakage.
# ---------------------------------------------------------------------------


def _unit_1_setup() -> None:
    """Topology & Feature Engineering — OSMnx, NetworkX, GeoPandas."""
    # Nothing special yet. If we hit geopandas/shapely version conflicts on
    # Colab, pin the four-tuple here.
    pass


def _unit_2_setup() -> None:
    """Trajectory Mining — MovingPandas / LeuvenMapMatching / Kalman."""
    pass


def _unit_3_setup() -> None:
    """Statistical Baselines — Statsmodels, pmdarima."""
    pass


def _unit_4_setup() -> None:
    """Dynamic Navigation — Pandana (with NetworkX fallback flag).

    If pandana fails to install (no Windows wheels, or new Python version),
    notebooks should branch on this flag and use the NetworkX path.
    """
    try:
        import pandana  # noqa: F401
        os.environ["UNIT4_USE_PANDANA"] = "1"
        print("  pandana available — using accelerated path")
    except ImportError:
        os.environ["UNIT4_USE_PANDANA"] = "0"
        print("  pandana unavailable — notebook will use NetworkX fallback")


# Minimal stand-ins so `from torch_sparse import SparseTensor` (and any
# torch_scatter symbol) succeed at IMPORT time. torch-geometric-temporal's
# package __init__ eagerly imports these (via its EvolveGCN modules), but the
# models this course uses (T-GCN, A3T-GCN) never execute them — they run on PyG's
# native scatter over edge_index. A stub that raises only if actually called is
# safe, and avoids the fragile source build that is the #1 Colab install failure.
_TORCH_SPARSE_STUB = (
    "class SparseTensor:  # dummy — unused by TGCN/A3TGCN (native scatter path)\n"
    "    def __init__(self, *a, **k):\n"
    "        raise NotImplementedError('stub torch_sparse.SparseTensor')\n"
    "    @classmethod\n"
    "    def from_edge_index(cls, *a, **k):\n"
    "        raise NotImplementedError('stub torch_sparse.SparseTensor.from_edge_index')\n"
    "def __getattr__(name):\n"
    "    def _f(*a, **k):\n"
    "        raise NotImplementedError('stub torch_sparse.' + name)\n"
    "    return _f\n"
)
_TORCH_SCATTER_STUB = (
    "def __getattr__(name):\n"
    "    def _f(*a, **k):\n"
    "        raise NotImplementedError('stub torch_scatter.' + name)\n"
    "    return _f\n"
)


def _ensure_scatter_sparse_importable() -> None:
    """If the compiled extensions aren't importable, write lightweight stub
    packages into site-packages so torch-geometric-temporal can be imported."""
    import importlib
    import torch_geometric  # installed just above; gives us the site-packages dir

    site_dir = os.path.dirname(os.path.dirname(torch_geometric.__file__))
    for name, body in (("torch_sparse", _TORCH_SPARSE_STUB),
                       ("torch_scatter", _TORCH_SCATTER_STUB)):
        try:
            importlib.import_module(name)
            continue                       # real (or already-stubbed) — leave it
        except Exception:
            pass                           # absent or broken — stub it
        pkg_dir = os.path.join(site_dir, name)
        os.makedirs(pkg_dir, exist_ok=True)
        with open(os.path.join(pkg_dir, "__init__.py"), "w") as fh:
            fh.write(body)
        print(f"  stubbed {name} (compiled extension absent; native scatter at runtime)")


def _verify_temporal_imports() -> None:
    try:
        import torch_geometric_temporal  # noqa: F401
        from torch_geometric_temporal.nn.recurrent import TGCN, A3TGCN  # noqa: F401
        print("  ✓ torch_geometric_temporal imports (TGCN / A3TGCN available)")
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ torch_geometric_temporal still fails to import: {exc}\n"
              "    See unit-5 KNOWN_ISSUES.md → 'scatter/sparse import' gotcha.")


def _unit_5_setup() -> None:
    """Spatio-Temporal GNNs — PyTorch Geometric (Temporal).

    Match PyG wheels to Colab's torch+CUDA at runtime. Do NOT pin torch.

    torch-geometric-temporal's package __init__ EAGERLY imports torch_sparse /
    torch_scatter (via EvolveGCN) even though T-GCN / A3T-GCN never use them.
    Those compiled extensions are the #1 Colab failure: with no matching wheel,
    pip source-builds them and HANGS for many minutes. So we (a) only ever take
    prebuilt wheels (never compile), and (b) if they still aren't importable, drop
    in lightweight stubs so the import chain succeeds. See unit-5 KNOWN_ISSUES.md.
    """
    try:
        import torch
    except ImportError:
        print("  ERROR: torch is unexpectedly missing from Colab — aborting unit-5 setup")
        return

    torch_v = torch.__version__.split("+")[0]
    cuda_v = (torch.version.cuda or "").replace(".", "")
    cuda_suffix = f"cu{cuda_v}" if cuda_v else "cpu"

    print(f"  detected torch={torch_v} cuda={cuda_v or 'none'} ({cuda_suffix})")
    print("  installing torch_geometric (native scatter path)")
    _pip_install("torch_geometric")

    # Best-effort prebuilt scatter/sparse wheels. --only-binary forbids the sdist
    # source build (the hang); a miss just falls through to the stub below.
    try:
        _pip_install(
            "torch_scatter",
            "torch_sparse",
            "--only-binary=:all:",
            "-f",
            f"https://data.pyg.org/whl/torch-{torch_v}+{cuda_suffix}.html",
        )
    except subprocess.CalledProcessError:
        print("  WARN: no matching torch_scatter/sparse wheels — will stub them")

    # Guarantee the import chain resolves (real wheels OR stubs), then install
    # temporal with --no-deps so pip does NOT re-drag the heavy extensions.
    _ensure_scatter_sparse_importable()
    _pip_install("--no-deps", "torch-geometric-temporal")
    _verify_temporal_imports()


__all__ = ["setup_unit"]
