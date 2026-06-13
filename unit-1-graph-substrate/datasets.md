# Unit 1 — Data sources & how to access them

This unit's data is **OpenStreetMap**, fetched at runtime — there are no
pre-staged files to download by hand. The demo and the practice/solution
notebooks each fetch and subset their own data inline, so they run end-to-end on
a fresh Colab with nothing pre-installed. This page lists every source, the
exact bounding boxes, and how access differs locally vs. on Colab.

> **Attribution (required).** All OSM-derived data is © OpenStreetMap
> contributors, licensed ODbL 1.0. Keep this attribution on any map or figure
> you publish.

---

## 1. OSM via Geofabrik + pyrosm — *primary path*

The robust, self-contained path the notebooks use by default. Instead of hitting
a live API, they download a regional extract once and cut it to a city bounding
box in memory.

- **Extract:** `israel-and-palestine-latest.osm.pbf` from Geofabrik —
  https://download.geofabrik.de/asia/israel-and-palestine.html
  (direct: `https://download.geofabrik.de/asia/israel-and-palestine-latest.osm.pbf`).
- **How it's used:** download-once-and-cache, then **cut to a bbox with `pyrosm`
  at read time** (no per-query API call), then OSMnx v2 simplify → project to
  UTM → consolidate intersections → take the largest connected component (LCC).
- **Bounding boxes** (WGS84, `[min_lon, min_lat, max_lon, max_lat]`):
  - **Jerusalem — demo:** `[35.180, 31.740, 35.260, 31.810]`
  - **Tel Aviv — practice / solution default:** `[34.760, 32.055, 34.815, 32.110]`
- **Why pyrosm:** it reads the local `.osm.pbf` (no live Overpass dependency) and
  exports an OSMnx-compatible graph, which is what keeps the notebooks runnable on
  a fresh Colab. See [`further-reading.md`](./further-reading.md) → "Library-stack
  alternatives".

## 2. Live OSMnx / Overpass — *showcase, not on the critical path*

The demo also *shows* the idiomatic live pull so you learn it:

```python
import osmnx as ox
G = ox.graph_from_place("Jerusalem, Israel", network_type="drive")
# bbox / point+distance / polygon variants also exist
```

This teaches the data-pulling idiom, but the notebooks do **not** depend on it —
Overpass rate limits and outages can break a live class pull, which is exactly
why the primary path is the cached Geofabrik extract. Use it to fetch your own
city when you extend the task.

## 3. Google-Drive fallback — *if Geofabrik is down*

If the Geofabrik download fails (e.g. a 504), the notebooks fall back to a hosted
copy on Google Drive, fetched with `gdown`. The file may be a prebuilt GraphML
(loaded straight into OSMnx) or an `.osm.pbf` (cut with pyrosm) — the code
detects which.

- **Jerusalem primal, Drive file id:** `18NSCmT1NwNVPl7uqvabuytKfAe3019yC`
  (`gdown.download(id="18NSCmT1NwNVPl7uqvabuytKfAe3019yC", ...)`).

## 4. Boeing Global Urban Street Networks (Harvard Dataverse) — *comparative benchmark*

Pre-built street graphs + pre-computed indicators for thousands of cities. Use
the **indicators table** to turn your city's number into an interpretable one:
when you report Tel Aviv's meshedness or intersection density, this says whether
that value is high or low among thousands of places.

- **GraphML subset DOI:** https://doi.org/10.7910/DVN/KA5HJ3
- **Collection:** https://dataverse.harvard.edu/dataverse/global-urban-street-networks/
- **License:** open per Dataverse terms (CC0-ish); underlying data is
  OSM-derived, so retain OSM attribution.
- **Caution:** the full world collection is ~80 GB — **do not download it whole.**
  Take a single city/country extract or just the indicators CSV. These are
  snapshots from the paper's extraction date, not live OSM, and the
  projection/simplification state varies by release (check before assuming).

## 5. OSM `highway` tags — *optional comparison labels*

Every OSMnx pull carries a `highway` tag per edge (`motorway` > `trunk` >
`primary` > `secondary` > `tertiary` > `residential` > `service` …). No separate
download. These are the **comparison target** for the "artery" question: after
computing betweenness, ask "do my high-betweenness streets coincide with
OSM-tagged arterials?" Treat tags as *noisy* ground truth — they reflect national
tagging conventions, residential edges vastly outnumber arterials, and some
contributors tag class partly from apparent importance (a mild circularity).
OSM wiki: https://wiki.openstreetmap.org/wiki/Key:highway

---

## Local vs. Colab — what differs

The **same notebook code runs in both places**; only where data is cached
differs.

| | Local (`uv`) | Colab |
|---|---|---|
| Setup | `uv sync --extra unit-1` | first cell runs `setup_colab.py` |
| Working dir / cache | your cwd | `/content` (resets each session) |
| Geofabrik extract | downloaded once, cached on disk | re-downloaded per fresh runtime |
| Drive fallback | `gdown` | `gdown` |

If you move the data cache, tell your agent the new path explicitly — the
notebooks handle the common cases but not arbitrary relocations.

## Gotchas (the ones that bite)

- **Project before metric-weighted centrality.** Lengths in degrees are
  meaningless; betweenness/closeness on an unprojected graph are wrong. Project
  to UTM first.
- **Simplify + consolidate before counting intersections or degree.**
  Un-consolidated roundabouts and divided roads inflate node counts and distort
  degree/betweenness.
- **Compute on the LCC.** Real city pulls have a giant component plus small
  disconnected fragments (data errors, ferries, clipped boundaries); centrality
  on the full multigraph breaks.
- **Pin OSMnx ≥ 2.0.** The v2 API renamed functions; older tutorials will not
  run as written.
