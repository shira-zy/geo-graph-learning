# Unit 4 — Known issues (if you see X, do Y)

## Transit backend / pyraptor

- **`pyraptor` fails to import on Colab** (e.g. `SyntaxError`, version/abi error,
  or `pip` refuses the install). **EXPECTED.** pyraptor is pinned to Python
  <=3.10 and Colab ships 3.11/3.12. The smoke-test cell catches this, sets
  `USE_PYRAPTOR = False`, and prints `transit backend = vendored RAPTOR`. **Do
  nothing** — the vendored ~110-line RAPTOR (Beat 7b) is the default teaching
  artifact and always runs. pyraptor is only an optional cross-check.

## Data acquisition

- **Overpass timeout / `graph_from_bbox` fails** in Beat 1. The cell auto-falls
  back to the hosted **backup graph** (`gdown` Drive id `1P6SyrzD…`, EPSG:2039)
  and prints a banner. If the cross-town O-D snaps **outside** that backup graph's
  bbox (origin/dest node lookup lands far away, or routing fails), produce + host
  a wider **TA-core** graph and update `OSM_BACKUP_DRIVE_ID`.
- **GTFS fetch fails** in Beat 1. Fallback ladder (in `_fetch_raw_gtfs`):
  cached zip → **FTP** MoT national feed
  (`ftp://gtfs.mot.gov.il/israel-public-transportation.zip`, keyless, fetched by
  `urllib`) → **Drive**-hosted copy of that raw zip (`gdown`, if
  `GTFS_RAW_DRIVE_ID` is set) → optional **S3** pre-clipped subset (if
  `S3_BASE_URL` set). If none resolve, a clear `RuntimeError` points here.
  *Note:* the original build shipped a transit.land API URL as "primary"; that
  endpoint needs an API key and returns `HTTPError` — replaced with the keyless
  FTP feed.
- **GTFS Drive host — DONE.** `GTFS_RAW_DRIVE_ID =
  "1fb4e7XmQft-f8SG_TFhTP_OGvS8zlJkv"` (`israel-public-transportation.zip`,
  ~125 MB, shared "anyone with link") is wired as the gdown fallback. The
  optional S3 subset (`ta-gtfs-weekday-subset.zip` + `unit4_wt.parquet` under
  `S3_BASE_URL`) remains an unused third fallback. *Note:* the Drive feed is the
  current rolling window, not period-matched to the March-2023 archive — fine for
  the demo (see the Beat 1 date note).

## w(t) derivation

- **GTFS-derived w(t) coverage is 0% / the shapes→edges join is empty** (Beat 3).
  The `build_wt_table` complexity guard catches this, sets
  `USE_SYNTHETIC_ONLY = True`, prints a banner, and the road beats (TDSP,
  isochrones, CoA-car) run on the **synthetic peak multiplier** instead. The
  transit beats are unaffected (they never use the road w(t) table). Causes:
  feed has no `shapes`, a CRS mismatch, or all shapes fall outside the bbox.

## Windows / local wheels

- **`rtree` / `geopandas` / `gtfs-kit` fail to install on Windows.** Use the
  prebuilt wheels (`uv` pulls them automatically); if a source build is
  attempted, install via conda-forge or pin to a wheel-available version. Same
  guidance as Units 1–2.
- **`pyraptor` will not install locally on Python > 3.10.** Expected; the demo
  does not require it (vendored RAPTOR covers transit).

## Time-expanded graph (Beat 7a)

- **`build_time_expanded` is slow / memory-heavy.** That is the *point* of Beat
  7a (the graph explodes). It is bounded to a 06:00–20:00 service window on the
  *clipped* feed. If it is too slow live, narrow the window or note the node count
  and move to 7b — the size chart is the teaching payload.
