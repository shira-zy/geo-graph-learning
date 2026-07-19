# Unit 5 — Data sources & how to access them

This unit's **demo** runs on **METR-LA** (the LA freeway loop-detector speeds —
the already-Eulerian, fixed-sensor regime a T-GCN/A3T-GCN forecasts). The
**supervised practice + homework + reference solution** run on
**`bus_corridor_u5.npz`** — the **same ~10-segment Tel-Aviv bus corridor Unit 3
used, re-framed as a graph** (nodes = road segments, edges = segment adjacency,
node features = each segment's speed time series). Every notebook fetches and
subsets its own data **inline**, so it runs end-to-end on a fresh Colab with
nothing pre-staged. This page lists every source, the exact IDs/URLs, and how
access differs locally (`uv`) vs. on Colab.

> **Attribution (required).**
> - **Bus GPS (the segment speeds):** Israel Ministry of Transport SIRI feed,
>   archived by **The Public Knowledge Workshop (HaSadna)** via the *Open Bus*
>   project — see [`further-reading.md`](./further-reading.md) → "Datasets /
>   tooling". Keep this attribution on any figure you publish.
> - **Segment geometry / adjacency:** © **OpenStreetMap** contributors, licensed
>   **ODbL 1.0** — the corridor's road segments come from the OSM drive graph
>   Unit 2/3 already use.
> - **METR-LA (demo only):** Li, Yu, Shahabi & Liu, *DCRNN* (ICLR 2018) — the LA
>   Metro loop-detector speeds. See [`further-reading.md`](./further-reading.md)
>   → "METR-LA / spatio-temporal bridge". Keep this attribution on any figure.

---

## 1. `bus_corridor_u5.npz` — the practice's bus corridor, re-framed as a graph

This is the **Unit-3 corridor turned into a spatio-temporal graph.** In Unit 3
you cut a Tel-Aviv corridor into **~10 road segments** and forecast each one's
speed with SARIMA. Unit 5 takes those same segments and their speed series and
packs them into one small `.npz`, ready to drop into a PyG-Temporal `TGCN`:

| Key | Shape | Meaning |
|---|---|---|
| `edge_index` | `[2, E]` | the **directed** segment chain (segment `i` feeds `i+1` downstream). You build the undirected/symmetric adjacency from this — the **graded adjacency decision** is yours. |
| `speeds` | `[segments, time]` | each segment's **per-15-min-bin speed** (km/h) — the same series U3 forecast, stacked as **node features**. |
| `latlon` | `[segments, 2]` | each segment's representative `(lat, lon)` for the folium corridor map. |

**Contents at a glance:** ~10 segment-nodes, ~17 days of 15-min bins (Feb 2023),
one Tel-Aviv corridor. The graph is **tiny on purpose** — a ~10-node / ~17-day
problem is exactly where "did the GNN earn its complexity vs. ten independent
SARIMAs?" becomes a real, measurable question (practice extension (c)).

| Path | Source | Notes |
|---|---|---|
| **Primary** | `bus_corridor_u5.npz` on the course Google Drive (`gdown` by id) | fetched by `fetch_with_fallback(...)` when a real `gdrive_id` is wired |
| **Fallback** | `bus_corridor_u5.npz` as a **GitHub Release asset** over HTTP | `https://github.com/bgalon/geo-graph-learning/releases/download/u5-data/bus_corridor_u5.npz` — CDN-backed, no per-file rate limit |

The notebooks fetch it **exactly as the demo's Section-8 cell does** — the same
`fetch_with_fallback` idiom (gdown → HTTP mirror, cached) used for the demo's
`a3tgcn_metrla.pt` / `tgcn_metrla.pt` checkpoints:

```python
# Same idiom the demo/solution use (gdown if a real Drive id is set, else HTTP mirror).
BUS = {"gdrive_id": "<GDRIVE_ID_bus_graph>",   # wired after the human upload (see the note below)
       "http": "https://github.com/bgalon/geo-graph-learning/releases/download/u5-data/bus_corridor_u5.npz"}

bus_path = fetch_with_fallback("bus_corridor_u5.npz", BUS["gdrive_id"], BUS["http"],
                               label="bus corridor graph")
import numpy as np
busz   = np.load(bus_path, allow_pickle=True)
edges  = busz["edge_index"]     # [2, E] directed i -> i+1
speeds = busz["speeds"]         # [segments, time], km/h, 15-min bins
latlon = busz["latlon"]         # [segments, 2]
```

> **⚠ Honest status — the hosted file is a pending human step.** As of this
> writing the hosted `bus_corridor_u5.npz` is **not yet uploaded**: the course
> Drive `gdrive_id` is still the placeholder `<GDRIVE_ID_bus_graph>`, and the
> GitHub Release asset has not been published. Until an instructor hosts it (a
> human-only step, tracked in `unit-5-gnn/STATE.md`), the **reference solution
> runs on a self-contained synthetic *Ibn-Gabirol-shaped* corridor fallback** —
> a ~10-node chain with a daily-dominated speed series and a downstream-sweeping
> congestion wave, so the notebook is runnable end-to-end with no hosted asset.
> The synthetic fallback has the **same shape and keys** as the real file, so
> your code does not change when the real corridor is wired in — only the numbers
> (and your breakeven verdict) do. `fetch_with_fallback` returns the real file
> the moment the `gdrive_id` (or the Release asset) is live.

## 2. Provenance — where the segment speeds come from (NOT on the runtime path)

`bus_corridor_u5.npz` is **derived**, not raw. You do **not** need any of the
sources below to run the practice — they are listed so the graph is reproducible,
not hand-staged.

- **Segment speeds** come from **`tlv_all.parquet`** (Drive id
  `1BqGMOa5urESNf-X3FHlMXZiFwIDp4EqQ`, ~48 MB) — the same all-Tel-Aviv bus-GPS
  slice Unit 2 and Unit 3 use (~4.7 M pings, 17 days, Feb 2023). Speed on each
  segment is computed from consecutive same-vehicle ping pairs
  (`speed = distance / Δt`, projected to **EPSG:2039** so distances are metres),
  then aggregated across all lines/vehicles into 15-min bins — the exact U3
  recipe. See Unit 3's
  [`datasets.md`](../unit-3-statistical-baselines/datasets.md)
  for that pipeline.
- **Segment adjacency + geometry** come from the OSM drive graph
  (`tlv_2039_backup.graphml.gz`, Drive id `1Um0jcKMT3h434E9U4cYUAXZmq1uj33zR`,
  EPSG:2039) — segment→segment edges are shared junctions along the corridor.
- **Raw archive (one level deeper):** `tlv_all.parquet` is itself cut from
  `busarchive.bin` (1.22 GB ZIP, Drive id `1BniXRYr5DrYvY_miHpD-hjChFB8s1ac6`;
  the GPS lives in `exports/vehicle_locations.parquet`, Feb 2023).

---

## Local vs. Colab — what differs

The **same notebook code runs in both places**; only where data is cached
differs.

| | Local (`uv`) | Colab |
|---|---|---|
| Setup | `uv sync --extra unit-5` | first cell runs `setup_colab.py` → `setup_unit("unit-5")` |
| Working dir / cache | your cwd (`.`) | `/content` (resets each session) |
| `bus_corridor_u5.npz` | `fetch_with_fallback` once, cached on disk | `fetch_with_fallback` per fresh runtime |
| If not hosted yet | synthetic Ibn-Gabirol fallback (self-contained) | synthetic Ibn-Gabirol fallback (self-contained) |

The `unit-5` extra carries the **fragile PyG stack** (`torch`,
`torch_geometric`, `torch_geometric_temporal`; **no torch pin**, and
`torch_scatter`/`torch_sparse` are intentionally omitted). See
`KNOWN_ISSUES.md` if imports fail. If you move the data cache, tell your agent
the new path explicitly.

## Gotchas (the ones that bite)

- **`velocity == 0` means *stopped*, not missing — the OPPOSITE of METR-LA.** On
  METR-LA a `0` is a *missing* sensor reading (the demo masks it to NaN). On the
  **bus corridor a `0` is a real STOPPED bus** (a red light, a stop dwell) — the
  very congestion you are forecasting. If you reuse the demo's zero-masking
  `masked_metrics` blindly you delete that signal *and* feed a graph that then
  propagates the hole to neighbours. Decide your stopped-bin handling explicitly
  (this is a graded decision) — the solution's `bus_metrics` keeps zeros.
- **The chain is directed; the T-GCN default is undirected.** `edge_index` ships
  the **directed** upstream→downstream chain. A symmetric-normalized GCN wants an
  **undirected** adjacency, so you must *choose* how to wire it and justify it in
  graph vocabulary (the unit's graded direct→interpret rehearsal). Building both
  from the shipped chain is a one-liner (`np.concatenate([e, e[::-1]], axis=1)`).
- **Horizons must match your U3 SARIMA.** The bins are 15-min, so future-step
  indices `0 / 1 / 3` are the **15 / 30 / 60-min** horizons — use the *same*
  three you used in U3 so the breakeven comparison is apples-to-apples.
- **The graph is tiny — that is the point, not a bug.** ~10 nodes over ~17 days
  is small for a GNN. Do not "fix" it by inventing edges; interrogate whether a
  GNN is even the right tool at this scale (practice extension (c)).
- **`bus_corridor_u5.npz` bundles speeds, not U3 forecasts.** It does **not**
  contain your Unit-3 SARIMA per-horizon numbers — those are *your* result to
  bring (or to re-fit / fall back on the historical-average floor; see the
  practice task's fallback note).

---

<sub>© Geospatial Graph Learning — rights reserved (not open-CC); see the course
`NOTICE.md`. This page was drafted with AI assistance and reviewed by the
instructor.</sub>
