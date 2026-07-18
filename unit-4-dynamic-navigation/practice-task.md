# Unit 4 — Supervised Practice: A City-Wide Cost of Anarchy

**Time: 1 hour, in class, working WITH an AI agent.**
**You will rehearse the loop: DIRECT → INTERPRET → EXTEND.**

> The demo routed **one** cross-town O-D pair: car (TDSP on a modeled peak
> `w(t)`) vs. bus (vendored RAPTOR on the clipped GTFS), at three departure
> hours. On that single trip the **car won every hour** — but the modeled
> rush-hour peak eroded most of its advantage. One trip is an anecdote. Now
> scale it to a **city**.
>
> Sample **~100 origin–destination pairs** across Tel Aviv. For each pair and
> for **three departure windows** (8am peak / 11am off-peak / 5pm peak),
> compute the optimal **car** path (TDSP + the modeled peak `w(t)`) and the
> optimal **transit** journey (RAPTOR + GTFS + an access/egress walk). Then read
> the resulting decision space two ways — the **Cost of Anarchy**:
>
> - **(a) Wrong-objective car CoA** *(the syllabus's original lab question)* —
>   for each pair, route once for **distance** and once for **time**, then
>   evaluate **both routes at the same peak hour**. How much extra travel time
>   does a driver pay for optimizing the **wrong objective** (shortest distance)
>   during congestion?
> - **(b) Car-vs-transit CoA** — for what **fraction** of trips is the bus
>   actually faster, and **where in the city** is the bus advantage strongest?
>   Map it.
>
> Your job is not to produce one number. It is to make a **defensible,
> quantified claim** — in this unit's vocabulary — about what your city's
> decision space looks like at 8am, **and to be honest about what is real
> structure versus what is an artifact of the modeled peak model.**

This is **open-ended on purpose.** There is no single correct answer. Two
students who pick a different O-D sample, a different distance band, or a
different "bus wins" threshold can both produce defensible work. You are graded
on the **quality of your direct → interpret → extend loop** (`rubric.md`), not
on matching the reference solution or hitting a target percentage.

---

## Read this first — the honesty contract (it is the whole lesson)

The demo established, and **you must inherit**, two facts that shape every
interpretation you make:

1. **The car's time-of-day congestion is REAL-TIMED but MODELED-IN-SPACE.** The
   GTFS-derived road speeds proved ~flat by hour (planned schedules barely encode
   rush hour), so the car side runs on an explicit, class-sensitive peak `w(t)`
   (`peak_multiplier(hour)` × `road_sensitivity`). Read it the way the deck does:
   its **hourly timing is real Tel Aviv data** (Ayalon Highway diurnal speeds /
   TomTom Traffic Index TLV — a deeper evening peak ~17:30 than morning ~08:00),
   but **which roads slow and how deeply is modeled** (arterials clog hard, local
   streets less), because no open per-segment TLV congestion feed exists. So the
   peak is "synthetic" **only as a per-segment congestion *measurement*** — the
   WHEN is real, the WHERE is modeled; it is not a measured per-segment field.
   When you find "the bus wins more at 8am," the correct reading is *partly* "the
   modeled peak punishes the car" — say so. An interpretation that forgets this
   is below bar.
2. **Transit is the vendored RAPTOR**, not `pyraptor` (which is unavailable on
   Colab's Python). The transit time also flatters reality: the schedule is
   roughly flat by hour and we count scheduled ride time, not wait-time variance.

"Cost of Anarchy" here is a **teaching proxy** — it measures wrong-objective and
car-vs-transit time gaps. It is **not** the game-theoretic *price of anarchy*
(no congestion equilibrium is computed). Naming that gap honestly is itself part
of the INTERPRET grade.

---

## What you start from

The demo notebook (`geoai-graph-unit4.ipynb`) gives you the **stack** and the
**helpers** you will reuse — **no new heavy dependencies**:

- `base_map` / `od_markers` / `add_path` / `path_latlon` — the folium scaffolding.
- The three-tier substrate fetch: OSM road graph (cache → live Overpass →
  Drive backup) and the GTFS fetch (`ftp://gtfs.mot.gov.il…` → Drive
  `GTFS_RAW_DRIVE_ID` → optional S3), clipped in memory by `_restrict_feed` and
  a programmatic weekday `pick_weekday_service`.
- The **car-routing core**: `peak_multiplier` / `road_sensitivity` /
  `edge_time_at` / `tdsp_weight(hour)` / `tdsp_path(hour, src, dst)` /
  `tdsp_total_min`. **Mind the O-D:** the demo's `tdsp_path` was generalized to
  `tdsp_path(hour, src=ORIG, dst=DEST)` — a bare `tdsp_path(hour)` **defaults to
  the demo's single O-D**, so per pair you MUST pass your own `src, dst`. Either
  call `tdsp_path(hour, src, dst)`, or (the efficient pattern the reference
  solution uses) build `w = tdsp_weight(hour)` **once per hour** and call
  `nx.dijkstra_path(G, src, dst, weight=w)` per pair. `tdsp_total_min(path, hour)`
  is already O-D-agnostic (it re-times any node path).
- The **transit core**: `nearest_stop(latlon)`, the footpath builder,
  `build_raptor_model`, the vendored `raptor(origin_stop, dest_stop, dep_s)`, and
  the journey reconstruction. For the ~100×3 sweep the reference solution builds a
  **vectorized, projected `nearest_stop_xy(x, y)`** variant (KD-tree over projected
  stop coords) so it can snap all pairs at once — same idea as `nearest_stop`,
  faster at scale.

> **The one thing you must build that the demo did not: scale.** The demo ran
> each helper **once**. You will run them **~100 × 3 times**. That changes the
> engineering, not the algorithm:
> - **Snap O-D pairs to graph nodes once**, vectorized (`ox.distance.nearest_nodes`
>   accepts arrays); snap to nearest stops once.
> - **Cache the per-hour TDSP weight** — `tdsp_weight(hour)` rebuilds a closure
>   each call; build it once per hour and reuse it across all pairs.
> - **Build the RAPTOR model once** (it is the slow part — tens of seconds).
> - Keep your O-D sample **modest** (60–100 pairs) so the full sweep finishes in
>   a few minutes, not an hour.
>
> A scaffolding cell in the reference solution shows the vectorized snap + the
> cached-weight loop. **That** is your starting block.

You are **not** given the prompts to type. Composing the right request, in this
unit's vocabulary, is half the exercise.

---

## The loop, made concrete

Everyone does the **baseline**. Then pick **at least one** extension (a/b/c/d);
strong students do two. Keep a **decision-log entry per cycle** (copy
`decision-log-template.md` into your working folder).

### Baseline — every student

1. **Sample your O-D pairs.** Decide *how*: a uniform random sample of graph
   nodes, a residential-grid sample, or the instructor's curated list. Impose a
   sane **straight-line distance band** (e.g. 2.5–9 km) so you are not routing
   trivially-short or off-the-graph pairs. Write down your sampling choice and
   *why* — it determines what "your city" means in the result.
2. **Compute the car side.** For each pair, compute the time-optimal path —
   `tdsp_path(8, src, dst)` (pass your own `src, dst`; a bare `tdsp_path(8)`
   silently returns the demo's single O-D), or the cached-weight pattern
   `nx.dijkstra_path(G, src, dst, weight=tdsp_weight(8))` built once — then
   `tdsp_total_min` it. For framing (a) you also need the **distance-optimal** path
   (`nx.shortest_path(..., weight="length")`) evaluated **at 8am** — i.e. how
   long the shortest-distance route actually takes when the peak is on.
3. **Compute the transit side.** For each pair, snap O and D to nearest stops,
   run `raptor(..., 8*3600)`, take the earliest arrival across rounds, and add
   the access + egress **walk** (nearest-stop distance ÷ walk speed). Mind the
   trips RAPTOR returns `None` for — they are **unreachable by bus** in your
   clip; that is data, not a bug, and you must decide how to count them.
4. **Compute the two CoA measures.**
   - **(a)** `coa_a = time(distance-route @ 8am) / time(time-route @ 8am)`
     per pair. Summarize its distribution (median, p90) and the **fraction of
     pairs where the wrong objective costs more than X%**.
   - **(b)** `bus_wins = transit_min < car_min` per pair. Report the **fraction**
     at 8am, and the car/transit ratio distribution.
5. **Map it.** A folium **choropleth or graduated-marker map** of the O-D pairs
   (or their origins) coloured by the CoA measure — so the **geography** of the
   result is visible, not just a histogram. Pair every metric with a
   distribution plot.
6. **Defend your interpretation in one paragraph.** What does this say about Tel
   Aviv at 8am? Where is the bus competitive, and *why might that be* (transit
   density, parallel arterials, the modeled peak)? Be explicit about the
   modeled-peak caveat.

### DIRECT / INTERPRET / EXTEND inside the baseline

- **DIRECT** — every request to the agent should name the operation in Unit-4
  vocabulary: *time-dependent shortest path (TDSP)*, *`w(t)` / time-varying edge
  weight*, *the peak multiplier (real-timed, modeled-in-space)*, *admissible heuristic* (if you reach
  for A*), *RAPTOR / earliest arrival / round*, *GTFS*, *access/egress walk*,
  *Cost of Anarchy*, *isochrone* (extension b). If your prompt would read the
  same to a non-specialist ("find the fastest way across town"), tighten it.
- **INTERPRET** — when the agent returns a fraction, a distribution, or a map,
  restate it yourself in **domain terms**: *what fraction* of trips the bus
  wins, *where* the wins cluster, and crucially *how much of the bus advantage
  is the modeled peak vs. real network geometry*. A result that surprises you
  is a lead, not a bug to hide.
- **EXTEND** — your baseline result should raise a new question. Follow it. The
  extensions below are structured leads, but a good question of your own counts.

---

## Extensions (pick at least one)

### (a) Off-peak persistence — *the surprise*

Repeat the whole sweep at **11am** (off-peak). Does the Cost of Anarchy
**collapse**, or does it **persist in certain corridors**? Map the pairs whose
CoA (either measure) stays high at 11am and propose a reason. **Watch for the
honest twist:** with the modeled peak switched (near-)off at 11am, the
car's time drops sharply while transit is schedule-flat — so the car-vs-transit
result can **flip hard**. Interpreting *why* (modeled peak, not real off-peak
congestion) is the point.

### (b) Isochrone competitiveness

Pick a single origin. Plot the **30-minute reachability isochrone** at 8am for
**car** (`single_source_dijkstra_path_length` with `tdsp_weight(8)` + convex
hull, as in the demo) and a **transit reachability set** (RAPTOR-reachable stops
within 30 min), **side by side**. Note this is **not** a bare helper reuse: the
demo's `raptor()` returns only a single-destination `best_per_round`, so it can't
list *every* stop reachable within the cutoff. You need a small **reachability
variant** of the RAPTOR loop that keeps the full arrival map (the reference
solution provides one as `transit_reach(origin_stop, dep_s, cutoff_s)`). Identify
neighborhoods where transit is competitive and neighborhoods where it is not.
What does the *shape* of each reachability region tell you that the per-pair CoA
did not?

### (c) Wrong-class — when is "shortest path" the wrong question? *(meta)*

For which O-D pairs is **shortest path itself the wrong framing**? Articulate
the conditions explicitly, in domain terms:

- the **destination is a polygon, not a point** (a campus, a mall — which stop /
  which entrance?);
- **delay/reliability** matters more than mean time (the p90, not the median);
- **parking availability** at the destination dominates the real door-to-door cost;
- the trip is a **chain** (school → work → errand), not a single leg;
- the user's preference is **multi-criteria** (fewest transfers, least walking —
  the Pareto front the demo's McRAPTOR sidebar gestured at).

For each, name the data or model class that would be needed to answer it
properly. This is a meta-extend: you are critiquing your own tool.

### (d) Frontier method — a learned A* heuristic *(optional, ambitious)*

The RECENT reading covers **learned graph-search heuristics** (PHIL, Pándy et
al. 2022, arXiv:2212.03978 — a GNN that predicts a node-to-goal estimate, used
as the A* heuristic, reportedly exploring ~58% fewer nodes). **There is no
public PHIL implementation or checkpoint**, and the method needs PyTorch (a U5
dependency). So this extension is genuinely **build-your-own / optional**:

- Either **sketch** the design — what node features, what training signal
  (true distance-to-goal labels from a batch of Dijkstra runs), how you would
  guarantee or check **admissibility** (an inadmissible heuristic breaks the
  optimality guarantee) — without training; **or**
- train a **tiny** regressor (even a non-GNN baseline: predict
  straight-line × a learned scale per road class) as an A* heuristic on your
  graph, measure the **explored-node reduction** vs. plain Dijkstra, and ask:
  **do you trust the result? How would you check it is still optimal?**

The interesting answer is the *verification* question, not the speedup.

---

## How the hour runs

| Time | What you do |
|---|---|
| 0:00–0:05 | Instructor restates the task + the rubric; you confirm your O-D sample, distance band, and the modeled-peak caveat. |
| 0:05–0:45 | Work the loop WITH the agent. Fill a decision-log entry per cycle. |
| 0:45–0:55 | 2–3 students share a **surprising follow-up** (the 11am flip, a corridor where the bus wins, an unreachable cluster). |
| 0:55–1:00 | Instructor synthesis. |

---

## What you hand in

- Your **decision log** (one entry per direct → interpret → extend cycle), with
  the end-of-session rubric check filled in.
- Your **one-paragraph defence** of your city's 8am decision space (with the
  CoA fraction / distribution numbers and the modeled-peak caveat stated).
- The extension(s) you chose, captured in the log.

You do **not** need a polished notebook for the in-class hour — the log + the
paragraph + your maps are the deliverable. (The take-home `homework.md` asks for
a short writeup.)

---

## A note on prompting (example *structure*, not a script)

You compose your own prompts. As a shape to imitate — not copy — a good DIRECT
request names the object, the operation, and the inputs precisely:

> "For each of the \<N\> snapped O-D node pairs, compute the **time-dependent
> shortest path** at an **8am departure** using the **modeled peak `w(t)`**
> (`tdsp_weight(8)`), and separately the **distance-optimal** path; evaluate
> **both** at 8am to get the **wrong-objective Cost of Anarchy** per pair. In
> parallel, snap each O and D to the **nearest GTFS stop**, run **RAPTOR** at an
> 8am departure, add the **access/egress walk**, and flag pairs the bus can beat
> the car on. Return a tidy frame I can choropleth by **origin**."

Notice what it does *not* say: it doesn't say "compare driving and the bus," and
it doesn't ask the agent to invent the peak model or the walk penalty. The
precision is the point. If your prompt is vaguer than this, the agent will pick
the sampling, the distance band, and the unreachable-trip convention for you —
and you'll spend INTERPRET time reverse-engineering its choices instead of
owning them.
