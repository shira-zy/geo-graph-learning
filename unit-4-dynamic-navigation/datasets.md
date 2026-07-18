# Unit 4 — Data & how to access it

This unit routes over **two** substrates: a road graph (OpenStreetMap) and a
transit timetable (GTFS). Both are fetched and subset **inline** by the notebooks —
nothing is pre-staged. This page lists the sources, the exact Tel Aviv extents the
demo uses, and how to load everything **locally with `uv`** and **on Colab**. Links,
not raw data.

Everything below runs the same in both environments; the only differences are cache
paths (`/content/...` on Colab vs your working directory locally) and that Colab's
first cell installs the deps via `setup_colab.py`.

---

## 1. Tel Aviv road network — OpenStreetMap (primary road substrate)

- **Source:** OpenStreetMap, via **OSMnx** (`ox.graph_from_bbox`). License **ODbL** —
  attribute "© OpenStreetMap contributors."
- **What the demo pulls:** a Tel Aviv core bounding box wide enough to hold the
  cross-town trip plus detour margin:
  - `BBOX (N, S, E, W) = 32.135, 32.040, 34.835, 34.745`
  - Origin (south TA, Florentin / central bus station): `32.0573, 34.7780`
  - Destination (north TA, TAU / Ramat Aviv): `32.1133, 34.8044`
- **Metric CRS:** `EPSG:2039` (Israeli TM grid, metres) for distances and the A*
  great-circle heuristic.
- **Speeds:** `ox.add_edge_speeds` imputes `speed_kph` from OSM `maxspeed`, then
  `ox.add_edge_travel_times` derives `travel_time`. Israeli `maxspeed` tagging is
  incomplete, so the imputation matters.
- **Fallback (if Overpass/Geofabrik is slow or down):** a pre-built, projected
  (`EPSG:2039`) Tel Aviv backup graph on Google Drive, id
  `1P6SyrzDnTFld3YX2cNorpbS0JfiUhTrR`, fetched with `gdown`. If your O-D needs a
  wider area than this graph covers, rebuild from the live bbox above.

## 2. Israel national GTFS — the transit timetable (primary transit substrate)

- **Source:** Israel Ministry of Transport national feed —
  `ftp://gtfs.mot.gov.il/israel-public-transportation.zip`. Free, open Israeli
  government data (attribute MoT). ~4,200 routes, 30,000+ stops, 36 agencies.
- **Loader:** `gtfs_kit.read_feed(...)`, then **clip to the demo bbox + one
  representative weekday `service_id`** before routing. Clip aggressively — the full
  national feed is large and gtfs-kit does no validation.
- **Rolling-window caveat (state this in your interpretation):** the MoT feed is a
  **~60-day window of *planned* service**; it does not archive the past. So the demo's
  road-side speeds (from the bus archive / TomTom shape) and the transit schedule can
  refer to **different dates** — that is fine pedagogically, but say so.
- **Colab-friendly access:** FTP can be awkward on Colab; the notebooks fall back to a
  Drive-hosted copy of the clipped feed, id `1fb4e7XmQft-f8SG_TFhTP_OGvS8zlJkv`
  (via `gdown`). HTTP mirrors also exist (the MobilityData / Mobility Database catalog
  entry for "Ministry of Transport and Road Safety").
- **Period-matched historical GTFS** (if you want to align exactly with the bus
  archive's dates): the community **hasadna open-bus / Stride** archive —
  https://open-bus-stride-api.hasadna.org.il/docs

## 3. Road `w(t)` time-of-day shape — TomTom + Ayalon (a *shape* anchor, not a feed)

- **Sources:** TomTom Traffic Index (Tel Aviv) — https://www.tomtom.com/traffic-index/ ·
  Ayalon Highway peak-hour speeds (Globes) —
  https://en.globes.co.il/en/article-average-peak-hour-speed-on-ayalon-highway-down-to-14-kmh-1001525275
- **What it provides:** the **timing** of the demo's `peak_multiplier(hour)` — a
  double-peak diurnal curve with a deeper evening peak (~17:30) than morning (~08:00),
  calibrated to published speed ratios (Ayalon ~14–24 km/h at peak).
- **Honesty contract:** the **WHEN** (hourly shape) is real Tel Aviv data; **WHICH**
  roads slow and how deeply (the **WHERE**, the per-class sensitivity `s(e)`) is
  **modeled**, because no open per-segment Tel Aviv speed feed exists (Uber Movement
  never covered TLV and is discontinued; per-segment probe data is commercial). These
  are transcribed *shapes*, not a downloaded file — there is nothing to fetch here.

---

## How to run

**Local (macOS / Windows) with `uv`:**

```bash
uv sync --extra unit-4                       # install the unit-4 stack
uv run python scripts/smoke.py --unit 4      # confirm every library imports
# then open geoai-graph-unit4.ipynb with the geo-graph kernel
```

**Colab:** open the notebook via its badge; the first cell fetches `setup_colab.py`
and installs `requirements/unit-4.txt`. Nothing to pre-install, nothing to pre-stage —
the notebook downloads and clips its own OSM + GTFS in-cell (with the Drive fallbacks
above if a live source is unavailable).

**Stack:** OSMnx, NetworkX, GeoPandas, Shapely, pyproj, rtree, scipy, gtfs-kit, folium,
mapclassify, branca, contextily, pyarrow, gdown. Transit routing uses a **vendored
RAPTOR** (always runs); `pyraptor` is an optional import-guarded cross-check.

**Attribution:** OpenStreetMap contributors (ODbL) for the road graph; Israel Ministry
of Transport for GTFS. Keep these attributions on any figure or derived dataset you
publish.
