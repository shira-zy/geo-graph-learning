# Unit 2 — Supervised Practice: Build a Whole-City Map From Buses, Then Grade It

**Time: 1 hour, in class, working WITH an AI agent.**
**You will rehearse the loop: DIRECT → INTERPRET → EXTEND.**

> The demo ran the noise frame **forward**: you had OSM, you had GPS, and you
> recovered a *trajectory* (HMM map matching) for **one bus line**. Now run it
> **backward**, and scale it **up to the whole city**.
>
> You are handed **every bus ping over Tel Aviv** — all 1458 lines, 6612
> vehicles, ~4.7 million pings — and **nothing else**. No OSM, no reference
> map, no street names. From those pings alone, **infer the city's road
> network** (density → centrelines → junctions → a `networkx` graph). Then —
> only at the very end — reveal OSM and **grade your inferred map against it**:
> which roads did you recover, which did you miss, which did you hallucinate?
> And *why*?
>
> Your job is not to produce a pretty inferred map. It is to make a
> **defensible, quantified claim** about how good your inferred map is, in the
> vocabulary of map inference — and to be honest about where the bus data, the
> noise model, or your own parameter choices let you down.

This is **open-ended on purpose.** There is no single correct inferred graph.
Two students who pick different cell sizes, KDE bandwidths, density thresholds,
or tolerances can both produce defensible work. You are graded on the **quality
of your direct → interpret → extend loop** (see `rubric.md`), not on matching a
key or maximizing an F1 score.

---

## What you start from

The demo notebook (`geoai-graph-unit2.ipynb`) already gives you the **stack** and
several reusable helpers — **no new heavy dependencies**:

- The inline `gdown` data fetch and the projection transformers (`_tf` forward,
  `inv` inverse) so every distance is in **metres** (EPSG:2039).
- The three-tier OSM-graph fetch (cache → live Overpass → hosted backup) — you
  will hold this **out** until grading time.
- The **Step 9 inverse mini-pipeline** you watched at the end of the demo:
  density → `skeletonize` → a compact `networkx` graph, with the `sknw`-optional
  / pure-`networkx` fallback.

> **One adaptation up front (read this — it's the #1 thing students trip on).**
> The demo's Step 9 estimates density with `scipy.stats.gaussian_kde` on a
> **single line**, and its bandwidth (`bw_method`, e.g. `0.02`) is a
> *dimensionless* scaling — **not** metres. At city scale a per-point `gaussian_kde`
> is far too slow, so you re-express the *same idea* as a **raster**: bin the pings
> into ~30 m cells and **Gaussian-blur with a bandwidth measured in metres** (tens
> of metres — the inverse-problem analogue of the demo's emission σ, which is also
> in metres). The grading is raster too (dilate two boolean images, count overlap),
> not a shapely buffer-union. The reference solution's `infer_graph` /
> `grade_raster` helpers show this raster form — **that**, not the demo's literal
> KDE call, is your real starting block.

> **Step 9 is your starting block, not your finish line.** In the demo, Step 9
> inferred a graph for a **single line** and stopped at a *qualitative* overlay
> (centrelines coloured by distance to the nearest OSM road). The practice goes
> **city-wide** and **past** that: a **quantified precision/recall grade**, a
> **bandwidth-sensitivity sweep**, and a **per-edge confidence score**. Re-doing
> Step 9 unchanged is not an answer.

You are **not** given the prompts to type. Composing the right request, in this
unit's vocabulary, is half the exercise.

---

## Your data — all of Tel Aviv

Use the whole-city ping pool: `tlv_all.parquet` — **4.7 M pings**, 1458 lines,
6612 vehicles, over the Tel Aviv bbox **lat 32.00–32.15, lon 34.74–34.88**
(~16.6 × 13.2 km, 219 km²). `recorded_at_time` is already tz-aware UTC.

> **Derive the bbox from the data cut, not from OSM.** The TLV bounding box is
> fixed by the artifact — you must not peek at OSM to choose your corridor, that
> would smuggle the answer into the question.

At city scale **you cannot afford a per-grid-point `gaussian_kde`** evaluation,
and you should not buffer-and-union every OSM road in shapely to grade (it is
~minutes per grade — fatal once you sweep bandwidths). The reference solution
shows the **raster** form of both — rasterize the pings, blur, threshold,
skeletonize; and grade by dilating two boolean images and counting overlap.
Raster grading is **~2 seconds**, so the bandwidth sweep below is cheap.

---

## The loop, made concrete

Everyone does the **baseline**. Then pick **at least one** extension (a/b/c/d);
strong students do two. Keep a **decision-log entry per cycle** (copy
`decision-log-template.md` into your working folder).

### Baseline — every student

1. **Estimate ping density over the city.** Project the pings to the metric CRS
   and estimate **density** over the bbox (rasterize → Gaussian blur — the
   raster analogue of KDE). Choose a **cell size** and a **bandwidth** — and
   write down, in your log, *why* those numbers (remember: bandwidth is the
   inverse-problem analogue of the demo's emission sigma). Show the density as
   a figure.
2. **Extract centrelines and assemble a graph.** Threshold the density to a
   boolean raster, **skeletonize** it, and trace the skeleton into a `networkx`
   graph (junctions = branch pixels, edges = the chains between them). Report
   node count, edge count, and total inferred length in km.
3. **Now — and not before — reveal OSM and grade your map.** Fetch the OSM
   drive graph for the *same bbox*. Define a **buffered edge match** on a
   **raster** basis: rasterize OSM onto the same pixel lattice, dilate both the
   inferred skeleton and the OSM raster by a tolerance (e.g. ~20 m), and count
   overlap. Compute:
   - **precision** = fraction of your *inferred* length within tolerance of
     *some* OSM road (how much of what you drew is real);
   - **recall** = fraction of *OSM* length (inside your corridor) within
     tolerance of *some* inferred edge (how much of the real network you
     recovered);
   - **F1** as the summary.
   - *Watch the trap:* clip OSM to your **inferred corridor's footprint** (a
     wider dilation of your skeleton) before computing recall — otherwise you
     "miss" every OSM road in a neighbourhood no bus ever drove, and recall
     collapses for a reason that has nothing to do with your method.
4. **Map the agreement.** On a folium map (OSM tile basemap as ground truth)
   draw your inferred edges coloured by whether they **matched** OSM, and
   separately highlight the **OSM roads you missed**. A distribution plot
   accompanies it (the precision/recall pair, or the off-road distance).
5. **Read it back, in domain terms.** For at least **two** disagreements,
   propose a concrete explanation and say which kind it is:
   - a **bus-only / restricted road** OSM lacks or buses uniquely use;
   - an **OSM road buses simply didn't drive** (coverage gap — the dominant
     kind city-wide);
   - a **noise-model artifact** (bandwidth too large → roads merged; threshold
     too high → a real road dropped; skeleton stub → a phantom spur near a
     depot/terminal loop);
   - a genuine **OSM error or staleness**.
6. **Defend your grade in one paragraph.** Is your inferred map *good*? Quote
   your precision/recall, and say what a planner could and could not trust it
   for.

### DIRECT / INTERPRET / EXTEND inside the baseline

- **DIRECT** — every request to the agent should name the operation in unit
  vocabulary: *density estimation, bandwidth, density threshold, rasterize,
  skeletonization / centreline extraction, junction detection, inferred graph,
  buffered (raster) edge precision / recall, corridor clip, coverage*. If your
  prompt would read the same to a non-specialist ("turn the dots into roads"),
  tighten it.
- **INTERPRET** — when the agent returns a graph, a number, or a map, restate
  it yourself: *what fraction* you recovered, *where* the misses cluster, and
  whether that matches your intuition about bus routes vs. the full street grid.
  A precision or recall number that surprises you is a lead, not a bug to hide.
- **EXTEND** — your baseline grade should raise a new question. Follow it. The
  extensions below are structured leads, but a good question of your own counts.

---

## Extensions (pick at least one)

### (a) Per-edge confidence by distinct-vehicle support — *the surprise*

For each inferred edge, count **how many distinct vehicles** (`vehicle_ref`)
contributed pings near it (within tolerance). Colour the inferred graph by that
count and plot its distribution. **Where is your network reliable, and where is
a whole "road" resting on a single bus?** Then re-grade: does precision improve
if you **drop edges supported by fewer than k vehicles**? At city scale a
sizeable fraction of edges rest on one vehicle — terminal loops, deadhead legs,
one-off detours. Most students get a genuine "wait, *that* edge came from one
bus" moment.

### (b) Bandwidth sensitivity — the inverse σ-sweep (now cheap)

Re-run the whole pipeline across a **ladder of bandwidths** (the analogue of the
demo's 5/15/50 m emission-sigma sweep). Because grading is **raster-fast**, this
costs seconds, not minutes. Plot **precision, recall, and F1 vs. bandwidth**.
Find the bandwidth that **maximizes F1** and explain the trade-off in domain
terms: too small → fragmented, noisy spurs; too large → parallel avenues merge
into a blob and precision falls. Notice what happens to **recall** across the
whole ladder — and explain why.

### (c) Time-of-day reconstruction — *or* DTW corridor clustering

Either:
- **(c1) Peak vs. off-peak.** Derive the windows **in-notebook** by converting
  the UTC timestamps to **Asia/Jerusalem**, then re-run the inference for a
  morning peak (06:00–09:00) and a midday off-peak (12:00–14:00) and compare the
  two inferred networks. Which roads appear only at peak? What does that say
  about the city's time-varying transit footprint (a seed for U3/U4's
  time-varying weights)?
- **(c2) DTW clustering.** Take several runs of one busy line and cluster /
  compare them by **DTW** shape similarity (`tslearn`), contrasted with a plain
  **Euclidean** distance — *which metric separates variable-speed bus runs
  better, and why?* (This preserves the syllabus's original Euclidean-vs-DTW
  question.)

### (d) Wrong-class — when is map inference the wrong tool? *(meta)*

Map inference shines when you have **no reference network** and **many passes**
over each road. Articulate, in domain terms, the conditions under which you
should instead reach for **HMM map matching against an existing OSM graph** —
and the conditions under which *aggregating* traces (which you just did)
**hides** a signal that a single matched trace would have surfaced (a one-off
detour, an incident, a closed lane). This is a meta-extend: you are critiquing
your own method and naming what later units (U3 outliers, U4 time-varying w(t))
supply to fix it.

---

## How the hour runs

| Time | What you do |
|---|---|
| 0:00–0:05 | Instructor restates the task + the rubric; you confirm your cell size + bandwidth + tolerance. |
| 0:05–0:45 | Work the loop WITH the agent. Fill a decision-log entry per cycle. |
| 0:45–0:55 | 2–3 students share a **surprising follow-up** they hit (the single-bus edge, the F1 cliff, the coverage-capped recall). |
| 0:55–1:00 | Instructor synthesis. |

---

## What you hand in

- Your **decision log** (one entry per direct → interpret → extend cycle),
  with the end-of-session rubric check filled in.
- Your **one-paragraph defence** of your inferred map's grade (with the
  precision/recall numbers).
- The extension(s) you chose, captured in the log.

You do **not** need a polished notebook for the in-class hour — the log + the
paragraph + your maps are the deliverable. (The take-home `homework.md` asks
for a short writeup.)

---

## A note on prompting (example *structure*, not a script)

You compose your own prompts. As a shape to imitate — not copy — a good DIRECT
request names the object, the operation, and the inputs precisely:

> "From the **EPSG:2039-projected** pings over the TLV bbox, build a density
> raster at \<cell\> m cells, **Gaussian-blur** it with bandwidth \<value\>,
> **threshold** at the \<value\> quantile, **skeletonize** the mask, and trace it
> into a `networkx` graph. Then, treating the OSM drive graph for the same bbox
> as ground truth, compute **raster buffered precision and recall** at a
> \<value\> m tolerance, **clipping OSM to the inferred corridor first**."

Notice what it does *not* say: it doesn't say "turn the dots into roads and
check if it's good," and it doesn't reach for a per-point KDE or a shapely
buffer-union that won't scale to the city. The precision is the point. If your
prompt is vaguer than this, the agent will pick the parameters (and the grading
method) for you — and you'll spend INTERPRET time reverse-engineering its
choices instead of owning them.
