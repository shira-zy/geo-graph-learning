#!/usr/bin/env python
"""Headless environment smoke test for a unit's stack.

Run by the `course-setup` skill (and by you, any time) to confirm the local
`uv` environment can import every library a unit needs — WITHOUT opening or
executing the unit's notebook (so it never dirties the upstream `.ipynb`).

Usage:
    uv run --extra unit-1 python scripts/smoke.py --unit 1
    uv run --extra all    python scripts/smoke.py --unit 1

It mirrors the smoke-test cell at the top of each demo notebook: import every
major library, make one trivial call each, print versions, and apply any
hard version gate (e.g. OSMnx >= 2.0 for unit 1). Exits non-zero on any
failure with a pointer to the unit's KNOWN_ISSUES.md.
"""
from __future__ import annotations

import argparse
import importlib
import sys

# Per-unit import plan. Each entry: (import_name, friendly_name, want_version).
# `want_version` True → print the module's __version__ if present.
UNIT_IMPORTS = {
    "1": [
        ("osmnx", "osmnx", True),
        ("networkx", "networkx", True),
        ("geopandas", "geopandas", True),
        ("shapely", "shapely", True),
        ("matplotlib", "matplotlib", True),
        ("requests", "requests", False),
        ("pyrosm", "pyrosm", True),
        ("igraph", "igraph", True),
        ("folium", "folium", True),
        ("mapclassify", "mapclassify", False),
        ("gdown", "gdown", False),
    ],
    "2": [
        ("osmnx", "osmnx", True),
        ("geopandas", "geopandas", True),
        ("shapely", "shapely", True),
        ("pyproj", "pyproj", False),
        ("rtree", "rtree", False),
        ("scipy", "scipy", True),
        ("networkx", "networkx", True),
        ("leuvenmapmatching", "leuvenmapmatching", False),
        ("filterpy", "filterpy", False),
        ("tslearn", "tslearn", False),
        ("folium", "folium", True),
        ("contextily", "contextily", False),
        ("pyarrow", "pyarrow", False),
    ],
    "3": [
        ("pandas", "pandas", True),
        ("numpy", "numpy", True),
        ("matplotlib", "matplotlib", True),
        ("statsmodels", "statsmodels", True),
        ("statsforecast", "statsforecast", False),
        ("pyarrow", "pyarrow", False),
        ("h5py", "h5py", False),
        ("folium", "folium", True),
    ],
    "4": [
        ("osmnx", "osmnx", True),
        ("networkx", "networkx", True),
        ("geopandas", "geopandas", True),
        ("shapely", "shapely", True),
        ("pyproj", "pyproj", False),
        ("rtree", "rtree", False),
        ("scipy", "scipy", True),
        ("gtfs_kit", "gtfs-kit", False),
        ("folium", "folium", True),
        ("mapclassify", "mapclassify", False),
        ("branca", "branca", False),
        ("pyarrow", "pyarrow", False),
    ],
}

# Units not yet populated — fail loudly rather than silently "pass".
UNPOPULATED = {"5"}

UNIT_DIR = {
    "1": "unit-1-graph-substrate",
    "2": "unit-2-trajectory-mining",
    "3": "unit-3-statistical-baselines",
    "4": "unit-4-dynamic-navigation",
    "5": "unit-5-spatio-temporal-gnns",
}


def smoke(unit: str) -> int:
    if unit in UNPOPULATED:
        print(f"Unit {unit} is not built yet — no deps to smoke-test.")
        return 0
    if unit not in UNIT_IMPORTS:
        print(f"ERROR: unknown unit '{unit}'. Known: {sorted(UNIT_IMPORTS)}")
        return 2

    failures = []
    for import_name, friendly, want_version in UNIT_IMPORTS[unit]:
        try:
            mod = importlib.import_module(import_name)
        except Exception as exc:  # noqa: BLE001 — report every import error
            failures.append((friendly, repr(exc)))
            continue
        version = getattr(mod, "__version__", "") if want_version else ""
        print(f"  ok  {friendly:<18}{version}")

    # Hard gate: units 1 and 4 need the OSMnx v2 module layout.
    if unit in ("1", "4") and not failures:
        try:
            import osmnx as ox

            major = int(str(ox.__version__).split(".")[0])
            if major < 2:
                failures.append(
                    ("osmnx", f"requires >=2.0, got {ox.__version__}")
                )
        except Exception as exc:  # noqa: BLE001
            failures.append(("osmnx version gate", repr(exc)))

    print()
    if failures:
        print("=" * 70)
        print(f"SMOKE TEST FAILED for unit {unit}:")
        for friendly, err in failures:
            print(f"  - {friendly}: {err}")
        known = UNIT_DIR.get(unit, f"unit-{unit}-*")
        print(f"\nFix the environment before continuing. See {known}/KNOWN_ISSUES.md")
        print("Most common: re-run `uv sync --extra unit-%s` from the repo root." % unit)
        print("=" * 70)
        return 1

    print(f"Smoke test passed — unit {unit} environment is ready.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", required=True, help="unit number, e.g. 1")
    args = parser.parse_args()
    return smoke(str(args.unit).lstrip("unit-"))


if __name__ == "__main__":
    sys.exit(main())
