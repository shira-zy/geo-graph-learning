# Unit 2 — Known Issues

"If you see X, do Y." Keep entries short and actionable. The demo notebook's
smoke-test cell is designed to surface the import/version problems below *before*
any teaching content.

---

## Leuven matcher: match dies at ping 1 with small `obs_noise` (sigma)

**Symptom:** `DistanceMatcher.match(...)` returns almost nothing
(`path_pred_onlynodes` empty, `last_idx == 0`) when `obs_noise` is small (e.g.
5 or 15 m), but works fine at `obs_noise=50`.

**Cause:** with a small emission sigma the *normalized* observation probability
(an EMA Leuven tracks) drops below `min_prob_norm` and the whole lattice is
pruned at the first observation. The Leuven docstring even notes "`max_dist` is a
hard cut, `min_prob_norm` should be better" — but for the sigma sweep we WANT the
emission model, not the normalized-probability gate, to do the soft work.

**Fix (used in the notebook):** construct the matcher with **`min_prob_norm=None`**
and a fixed generous **`max_dist=200`** (the hard candidate cut), independent of
sigma. This makes the 5/15/50 m sweep produce full matches. See `make_matcher()`
in step 5.

---

## Leuven matched-path accessor is version-sensitive

**Symptom:** `AttributeError` reaching for the matched node/edge sequence after
`matcher.match(...)`.

**Cause:** Leuven's matched-state API changed across versions (repo issue #15).

**Fix:** the notebook pins **`DistanceMatcher.path_pred_onlynodes`** (the Viterbi
node sequence, projected) and asserts its presence in the smoke-test cell, so a
version mismatch fails fast. If a future Leuven renames it, update the accessor in
the smoke cell and in `match_track()` together. (`matcher.lattice_best` and
`matcher.path_pred` are the related, also-version-sensitive accessors.)

---

## `filterpy` fails to build on very new Python / setuptools

**Symptom:** `pip install filterpy` errors with
`Failed building wheel for filterpy` / `setup.py install is deprecated` /
`Invalid dash-separated options` (SetuptoolsDeprecationWarning escalated to error).

**Cause:** filterpy 1.4.5 ships a legacy `setup.py`/`setup.cfg` with dash-named
options that newer setuptools (Python 3.13+ envs) rejects.

**Where it bites:** **fresh free-tier Colab is currently Python 3.12 with an older
setuptools and installs filterpy fine** — this is a *local*-env hazard (a 3.13
`uv`/conda env). If you hit it locally:
- pin an older setuptools in the build env (`pip install "setuptools<70"` then
  `pip install filterpy`), or
- the Kalman step is a ~15-line 2D constant-velocity filter; a `numpy`-only
  predict/update fallback reproduces it if filterpy is unavailable on your box.

Flag for Windows: filterpy is pure-Python (no wheels needed), so Windows installs
fine once the setuptools issue above is avoided.

---

## `rtree` / `geopandas` / `leuvenmapmatching` on Windows

**Symptom:** `OSError: could not find/load spatialindex_c` (rtree) or a shapely/
GEOS load error on Windows local installs.

**Cause:** `rtree` needs the libspatialindex native lib; historically the pip
wheel didn't bundle it on Windows. leuvenmapmatching uses rtree for candidate
search, and geopandas/shapely need GEOS.

**Fix:** on Windows install the geo stack from wheels that bundle the natives —
`pip install rtree geopandas shapely` from recent PyPI wheels works on Python
3.10-3.12; if it doesn't, use `conda install -c conda-forge rtree geopandas
shapely leuvenmapmatching`. `uv sync --extra unit-2` on Windows should pull
working wheels; if rtree fails, fall back to conda-forge for that one package.

---

## osmnx / Overpass download is flaky

**Symptom:** the graph-build cell raises a timeout / HTTP error from Overpass,
or hangs.

**Cause:** the public Overpass API is rate-limited and occasionally down.

**Fix (three-tier, built into the graph cell):** the notebook tries, in order,
**(1)** the local cache `corridor_2039.graphml` → **(2)** a **live**
`ox.graph_from_bbox(...)` (projected to EPSG:2039 + cached) → **(3)** a hosted
**backup graph** on Drive (`id=1P6SyrzDnTFld3YX2cNorpbS0JfiUhTrR`). For a hard
outage you can also point `ox.settings.overpass_url` at a mirror.

---

## Backup-graph fallback path (gdown + gunzip) — when Overpass is down

**Symptom:** the graph cell prints the banner
`OVERPASS DOWNLOAD FAILED — falling back to the hosted backup graph.`

**What it does (by design, not an error):** when live Overpass fails, the cell
`gdown`s `backup_graph_2039.graphml.gz` (Drive `id=1P6SyrzDnTFld3YX2cNorpbS0JfiUhTrR`,
~4.1 MB gz, md5 `5e00deea…`), **gunzips** it, and `ox.load_graphml`s it. The
backup is **already projected to EPSG:2039** (22,514 nodes / 43,837 edges, the
busiest-day corridor with `PAD=0.004`) — do **not** re-project it. It is saved to
`corridor_2039.graphml` so re-runs are instant. Verified: a forced-failure run
yields a graph identical to the live path's. If the gdown itself fails (Drive
quota), re-run; once the cache exists the network is not touched again.

> Note the live and backup graphs differ slightly in node count (~29.7k vs 22.5k)
> because the live bbox is derived from the day's pings while the backup is the
> pre-cut busiest-day corridor. Both are valid EPSG:2039 corridor graphs.

---

## `skimage.skeletonize` on the inverse map-inference raster (step 9)

**Symptom:** `skeletonize` errors or returns a fuzzy/over-connected skeleton.

**Cause:** `skimage.morphology.skeletonize` expects a **boolean** raster. The
notebook thresholds the KDE density with `dens >= np.quantile(dens[dens>0], 0.80)`
(a bool mask) and calls `skeletonize(mask, method="lee")`. The `lee` method is
the robust one for thick blobs; the default (Zhang) can leave stubs. If the
skeleton frays, **raise the threshold quantile** (fewer, cleaner pixels) or
**raise `KDE_BW`** (smoother density) — both are the inverse-problem analogue of
the emission sigma. The smoke cell pins a `skeletonize(...bool..., method="lee")`
one-liner so a missing/renamed API fails fast.

---

## `sknw` (skeleton → graph) is OPTIONAL and not in the deps

**Symptom:** none — the inverse-pipeline cell prints `[fallback] inferred graph:`
rather than `[sknw] inferred graph:`.

**Cause:** `sknw` turns a skeleton raster into a `networkx` graph in one call, but
it is **not pinned** in `requirements/unit-2.txt` (no reliable wheel everywhere).
The notebook `try`s `import sknw` and otherwise falls back to a transparent
8-neighbour pixel graph + degree-2 chain contraction (pure `networkx`). Both
yield the same inferred-graph overlay. Install `sknw` only if you want the
one-call path; it is not required.

---

## Bearing + velocity-aware matching (step 8) — keep the terms `<= 0`

**Symptom:** `Exception: logprob_obs = <positive> > 0` from inside
`DistanceMatcher.match`.

**Cause:** Leuven asserts the emission **log-prob is ≤ 0**. The direction-aware
matcher adds a heading term to `logprob_obs`; if you *reward* agreement (add a
positive value) you can push the log-prob above 0 and trip this assert.

**Fix (used in the notebook):** write the heading term as `HEAD_W * (agree - 1.0)`
— it is **0 when aligned and negative otherwise**, so it only ever penalizes.
Same idea for the velocity gate in `logprob_trans`: subtract a non-negative
`VEL_W * excess`. The per-observation index is recovered inside the hooks from
the `edge_o.label` (`"O<idx>"`) Leuven assigns during matching; if a future
Leuven changes that label format the term silently no-ops (guarded by `try`),
which is safe but disables the feature — check `edge_o.label` if heading stops
mattering.

---

## folium maps don't show in headless CI / nbconvert

**Symptom:** running the notebook with `nbclient`/`nbconvert` produces no visible
map (the figures appear, the maps look "empty").

**Cause:** folium maps render as an `execute_result` with `text/html` (a Leaflet
iframe). Headless executors capture the HTML but don't *display* it; the maps are
present in the output, they just need a browser/Colab/Jupyter front-end to render.
Tiles themselves are fetched **client-side at view time**, so a headless run with
no network still succeeds (the HTML is produced; tiles load when you open it).

**Fix:** none needed for correctness — verify map *presence* by checking each
folium cell has a `text/html` output. For a static fallback when tiles are
blocked, the smoke cell sets `_HAVE_CTX` (contextily) for slide assets.

---

## gdown "permission denied" / confirm-token on the Drive fetch

**Symptom:** the data cell's `gdown.download(id=...)` returns an HTML page or a
quota error instead of the parquet.

**Cause:** Drive throttling, or the file's sharing reverted to private.

**Fix:** the artifact `id=1SdxoE7FUFE1sKSjLpXE1_rf1kmWJDd6u` is public and small
(0.72 MB) so the confirm-token path rarely triggers. If it fails: re-run (cached
once present); or run the OPTIONAL provenance cell at the notebook bottom
(`REGENERATE=True`) to rebuild the artifact from the raw archive
(`id=1BniXRYr5DrYvY_miHpD-hjChFB8s1ac6`).

---

## Direction arrows (PolyLineTextPath / AntPath) don't show on the map

**Symptom:** in Step 1 (`m1`) or Step 5 (`m5`) the ping markers and polylines
render but the **arrowheads / animated flow are missing**.

**Cause / caveats:**
- Both ship with folium (`folium.plugins`), no extra dependency. The smoke cell
  imports `PolyLineTextPath, AntPath` so a missing/renamed plugin fails fast.
- `PolyLineTextPath` injects a `leaflet-textpath` JS snippet that runs **after**
  the polyline is on the map; on **Colab the cell's iframe is sandboxed and only
  runs JS once you "Trust" / re-run the cell**. If arrows are absent, re-run the
  cell (Runtime trust) — the static `text/html` is correct, it just needs the JS
  to execute in a trusted front-end. Tiles + arrows both load client-side.
- The arrow glyph is the Unicode "➤" (U+27A4); keep it as a real character in the
  string, not an escape, or it renders as literal text.
- `AntPath` is the *animated* layer (best-effort eye candy). If animation is
  janky/absent, the static `PolyLineTextPath` arrowheads still carry the
  direction point — that's why both are drawn. In a headless/papermill run
  neither animates (expected); verify *presence* by grepping the cell's
  `text/html` for `textpath` / `antpath` (as the verification plan does).

**Fix:** none for correctness. For a guaranteed-static teaching fallback, the
direction can also be read from START (green) / END (red) markers, which are plain
`folium.Marker`s and always render.
