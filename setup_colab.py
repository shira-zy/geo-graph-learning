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


def _unit_5_setup() -> None:
    """Spatio-Temporal GNNs — PyTorch Geometric (Temporal).

    Match PyG wheels to Colab's torch+CUDA at runtime. Do NOT pin torch.
    """
    try:
        import torch
    except ImportError:
        print("  ERROR: torch is unexpectedly missing from Colab — aborting unit-5 setup")
        return

    torch_v = torch.__version__.split("+")[0]
    cuda_v = (torch.version.cuda or "").replace(".", "")
    cuda_suffix = f"cu{cuda_v}" if cuda_v else "cpu"

    print(f"  detected torch={torch_v} cuda={cuda_v or 'none'}")
    print(f"  installing torch_geometric (+ optional scatter/sparse for {cuda_suffix})")

    _pip_install("torch_geometric")

    # Optional accelerator extensions — PyG 2.4+ does not hard-require them.
    # Try to install but don't fail the whole setup if wheels are unavailable.
    try:
        _pip_install(
            "torch_scatter",
            "torch_sparse",
            "-f",
            f"https://data.pyg.org/whl/torch-{torch_v}+{cuda_suffix}.html",
        )
    except subprocess.CalledProcessError:
        print("  WARN: torch_scatter/sparse wheels not available — continuing without")

    _pip_install("torch-geometric-temporal")


__all__ = ["setup_unit"]
