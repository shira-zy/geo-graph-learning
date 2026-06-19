# Unit 2 — Data sources & how to access them

This unit's data is the **SIRI real-time bus-GPS archive** for Israel (the
demo + practice run on Tel Aviv), plus the **OpenStreetMap** road network the
trajectories are matched against / compared to. Every notebook fetches and
subsets its own data **inline**, so it runs end-to-end on a fresh Colab with
nothing pre-staged. This page lists every source, the exact IDs and bounding
box, and how access differs locally vs. on Colab.

> **Attribution (required).**
> - **Bus GPS:** Israel Ministry of Transport SIRI feed, archived by **The
>   Public Knowledge Workshop (HaSadna)** via the *Open Bus* project — see
>   [`further-reading.md`](./further-reading.md) → "Datasets". Keep this
>   attribution on any figure or table you publish.
> - **Road network:** © **OpenStreetMap** contributors, licensed **ODbL 1.0**.

---

## 1. The bus-GPS artifacts — pre-cut, hosted on Google Drive (*primary path*)

The raw archive is **1.22 GB** (and ~675 MB of it is an unrelated SQL dump), so
the notebooks never pull it at runtime. Instead each notebook `gdown`s a small,
pre-cut **zstd parquet** and reads it with pandas/pyarrow. Columns:
`recorded_at_time` (tz-aware UTC), `lat`, `lon`, `bearing`, `velocity`,
`line_ref`, `vehicle_ref`.

| Used by | File | Drive id | Size | Contents |
|---|---|---|---|---|
| **Demo** | `ta_line_13429.parquet` | `1SdxoE7FUFE1sKSjLpXE1_rf1kmWJDd6u` | ~0.72 MB | One Tel Aviv line (13429): 42,190 pings, 166 vehicles, 16 days |
| **Practice / solution** | `tlv_all.parquet` | `1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ` | ~48 MB | **All** Tel Aviv pings: 4,725,997 rows, 1,458 lines, 6,612 vehicles |

```python
import gdown, pandas as pd
gdown.download(id="1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ", output="tlv_all.parquet", quiet=False)
df = pd.read_parquet("tlv_all.parquet")          # 4.7M pings over the TLV bbox
```

- **Tel Aviv bounding box** (WGS84): **lat 32.00–32.15, lon 34.74–34.88**
  (~16.6 × 13.2 km, 219 km²). The cut is filtered to this box.
- **Cadence** ≈ 1 GPS fix per vehicle per minute — the sparse regime the whole
  unit is about.

## 2. The road network — OSM via OSMnx (*fetched live, with a hosted fallback*)

The notebooks build the corridor / city road graph from OSM and reproject to
**EPSG:2039 (Israeli ITM)** so every distance (emission σ, tolerances, edge
lengths) is in **metres**.

```python
import osmnx as ox
G = ox.graph_from_bbox((34.74, 32.00, 34.88, 32.15), network_type="drive")
Gp = ox.project_graph(G, to_crs="EPSG:2039")
```

Overpass can rate-limit or time out, so each notebook uses a **three-tier
fetch**: on-disk cache → live Overpass → `gdown`+gunzip a hosted backup graph.

| Used by | Backup file | Drive id | Size | Graph |
|---|---|---|---|---|
| **Demo** | `corridor_2039_backup.graphml.gz` | `1P6SyrzDnTFld3YX2cNorpbS0JfiUhTrR` | ~4.1 MB | Line-13429 corridor, EPSG:2039 (22,514 / 43,837) |
| **Practice / solution** | `tlv_2039_backup.graphml.gz` | `1Um0jcKMT3h434E9U4cYUAXZmq1uj33zR` | ~3.15 MB | Whole-TLV drive graph, EPSG:2039 (17,459 / 33,719) |

## 3. The raw SIRI archive — *provenance only, NOT on the runtime path*

The canonical source the two cuts are derived from. You do **not** need this to
run anything; it's here so the artifacts are reproducible, not hand-staged.

- **File:** `busarchive.bin` (1.22 GB ZIP), Drive id
  `1BniXRYr5DrYvY_miHpD-hjChFB8s1ac6`. The GPS lives in one member,
  `exports/vehicle_locations.parquet` (20.79 M rows, Feb 2023).
- **Regenerate a cut** (deterministic): download → extract that one member →
  project the 7 columns → filter to the TLV bbox (or a single `line_ref`) →
  write zstd parquet. `gdown` can choke on a file this large; use the
  `https://drive.usercontent.google.com/download?id=…&confirm=t` endpoint. The
  demo's optional "provenance" cell shows the recipe.

## 4. Alternative trajectory datasets — *if you want a different city*

Swap-in sources for extending the practice to your own data (same pipeline):

- **GeoLife** (Microsoft Research, Beijing) — 17,621 GPS trajectories, many at
  1–5 s cadence. Good for a *dense*-GPS contrast to the sparse bus feed.
- **Porto taxi** (ECML/PKDD 2015, UCI) — 1.7 M taxi trajectories, one city.
- **mapconstruction.org** — benchmark trajectory sets *with* ground-truth road
  maps, the standard testbed for map-inference precision/recall.

See [`further-reading.md`](./further-reading.md) → "Datasets" for links.

---

## Local vs. Colab — what differs

The **same notebook code runs in both places**; only where data is cached
differs.

| | Local (`uv`) | Colab |
|---|---|---|
| Setup | `uv sync --extra unit-2` | first cell runs `setup_colab.py` |
| Working dir / cache | your cwd | `/content` (resets each session) |
| Parquet + backup graph | `gdown` once, cached on disk | `gdown` per fresh runtime |
| Live OSM | OSMnx → Overpass | same (backup graph if it fails) |

If you move the data cache, tell your agent the new path explicitly — the
notebooks handle the common cases but not arbitrary relocations.

## Gotchas (the ones that bite)

- **Project to EPSG:2039 before any metres-based step.** Emission σ,
  tolerances, and edge lengths are all in metres; computing them on lat/lon
  degrees is silently wrong.
- **`recorded_at_time` is UTC.** For a local-time window (e.g. a 06:00–09:00
  peak slice) convert to `Asia/Jerusalem` first.
- **Overpass is flaky for a 219 km² query.** Expect to hit the hosted backup
  graph in class; that's by design, not a failure.
- **The whole-city pool is 4.7 M points.** Density/skeleton work on a *raster*
  (bin → blur), which is O(pixels) — don't run a per-point `gaussian_kde` over
  the city, and grade with a raster overlap, not a shapely buffer-union.
