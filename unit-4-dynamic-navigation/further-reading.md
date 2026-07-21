# Unit 4 — Further reading (AI-friendly sources)

Every source behind this unit's slides, demo, and practice, as an external link
plus a short plain-language summary. It is written so that **you or your agent**
can read it as context before building the practice solution. The machine-readable
citations are in [`references.bib`](./references.bib).

Sections: **THEORY** (the algorithms) · **PRACTICE** (the tools you'll run) ·
**DATA** (where the numbers come from) · **RECENT** (the research frontier).

---

## THEORY — the routing algorithms

### Dijkstra 1959 — A note on two problems in connexion with graphs
- **Link:** https://doi.org/10.1007/BF01386390
- **Type:** THEORY
- **Summary:** The original single-source shortest-path algorithm: repeatedly settle
  the nearest unsettled node and relax its edges, giving optimal paths on any
  non-negative edge weight. In this unit it is the baseline — run it with a
  `travel_time` weight for the fastest path and a `length` weight for the shortest
  one, and the two diverge. That divergence *is* the "choosing the cost is choosing
  the question" lesson.

### Hart, Nilsson & Raphael 1968 — A Formal Basis for the Heuristic Determination of Minimum Cost Paths (A*)
- **Link:** https://doi.org/10.1109/TSSC.1968.300136
- **Type:** THEORY
- **Summary:** Introduces A*: fold a heuristic estimate of remaining cost `h(n)` into
  Dijkstra's search so it expands toward the goal, ranking the frontier by
  `f(n) = g(n) + h(n)`. If `h` is **admissible** (never overestimates), A* still
  returns the optimal path while exploring fewer nodes; with `h ≡ 0` it *is*
  Dijkstra. A natural admissible heuristic on a road graph is great-circle distance
  divided by the maximum edge speed.

### Dean 2004 — Shortest Paths in FIFO Time-Dependent Networks
- **Link:** https://people.csail.mit.edu/bdean/tdsp.pdf
- **Type:** THEORY
- **Summary:** When each edge's travel time depends on *when* you traverse it, the
  shortest path depends on your departure time (time-dependent shortest path, TDSP).
  The key condition is **FIFO / non-overtaking** — leaving later never lets you
  arrive earlier — and under it a label-setting Dijkstra stays correct: you just
  evaluate each edge cost at the clock you reach it. Road traffic is essentially
  always FIFO, which is why the lightweight "Dijkstra with a clock" baseline is not
  a toy but the correct algorithm.

### Delling, Pajor & Werneck 2015 — Round-Based Public Transit Routing (RAPTOR)
- **Link:** https://doi.org/10.1287/trsc.2014.0534
- **Type:** THEORY
- **Summary:** Transit journey planning is *not* a graph-shortest-path problem.
  RAPTOR throws the graph away and processes the timetable in **rounds** — after
  round *k*, it knows the earliest arrival at every stop using at most *k* trips —
  with no priority queue and no preprocessing. The Pareto set trading arrival time
  against number of transfers falls out of the rounds for free, which is exactly the
  two criteria riders care about.

### Dibbelt, Pajor, Strasser & Wagner 2018 — Connection Scan Algorithm (CSA)
- **Link:** https://doi.org/10.1145/3274661
- **Type:** THEORY
- **Summary:** RAPTOR's twin. Sort every elementary connection (a vehicle leaving
  stop A at t1, reaching stop B at t2) by departure time once, then answer an
  earliest-arrival query with a single linear sweep over that array. No graph, no
  priority queue, cache-friendly and strikingly simple — a good tool to *name* when
  you want raw earliest-arrival speed rather than RAPTOR's transfer dimension.

### Roughgarden & Tardos 2002 — How Bad Is Selfish Routing? (Price of Anarchy)
- **Link:** https://doi.org/10.1145/506147.506153
- **Type:** THEORY
- **Summary:** When every driver selfishly minimizes their own travel time, the
  resulting equilibrium can be worse than a centrally coordinated optimum; the ratio
  is the **price of anarchy**, bounded by 4/3 for linear latency functions (so
  selfishness costs at most ~33%). This unit borrows the *name* for its "Cost of
  Anarchy" lab but is careful to flag that the lab compares two single-trip times,
  not a congestion equilibrium — naming that gap honestly is itself the interpretation
  lesson.

### Batz, Delling, Geisberger, Neubauer, Sanders & Vetter 2009/2010 — Time-Dependent Contraction Hierarchies *(deeper, optional)*
- **Link:** https://doi.org/10.1137/1.9781611972894.10
- **Type:** THEORY
- **Summary:** Generalizes Contraction Hierarchies — the dominant static road-network
  speedup — to time-dependent weights, storing a piecewise-linear travel-time profile
  on each shortcut so "leave at time *t*" queries still run in microseconds on
  continental networks. It is the production answer to fast TDSP and the reason
  classical routing wins on correctness and speed at city scale.

### Delling, Goldberg, Pajor & Werneck 2014 — Robust Distance Queries on Massive Networks *(deeper, optional)*
- **Link:** https://doi.org/10.1007/978-3-662-44777-2_27
- **Type:** THEORY
- **Summary:** A synthesis of the route-planning speedup landscape: hub-labelling and
  related preprocessing answer shortest-distance queries on continental road networks
  in microseconds and can be engineered to stay fast across many network types. It is
  the state-of-the-art anchor for "exact routing is already extremely fast" — context
  for why learned heuristics are a continental-scale accelerator, not a city-core need.

---

## PRACTICE — the tools you'll run

### Boeing 2017 — OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks
- **Link:** https://doi.org/10.1016/j.compenvurbsys.2017.05.004
- **Type:** PRACTICE
- **Summary:** OSMnx builds a routable road graph from OpenStreetMap and imputes an
  edge `speed_kph`/`travel_time` from `maxspeed`. `weight="length"` vs
  `weight="travel_time"` on the same shortest-path call is the cleanest demonstration
  of cost-as-a-modeling-choice. Time-varying `w(t)` is implemented by handing NetworkX
  a *callable* weight that reads a per-edge, time-of-day speed at the arrival clock.
  Worked routing notebook: https://github.com/gboeing/osmnx-examples/blob/main/notebooks/02-routing-speed-time.ipynb

### gtfs-kit — Python GTFS parsing and analysis
- **Link:** https://github.com/mrcagney/gtfs_kit
- **Type:** PRACTICE
- **Summary:** A lightweight, pure-Python, database-free toolkit for reading a zipped
  GTFS feed (including from a URL), slicing it to a city and a service date, and
  extracting trips-per-stop, route geometries, and time windows. It is the on-ramp
  for the transit beat — but it does **no** validation, so clip the large national
  feed aggressively to one city and one weekday before routing.

### pyraptor — Python RAPTOR over GTFS
- **Link:** https://github.com/lmeulen/pyraptor
- **Type:** PRACTICE
- **Summary:** A pure-Python implementation of RAPTOR (and Range/McRAPTOR) that reads a
  GTFS feed, builds an in-memory timetable, and answers best-journey queries. It is
  research-grade (few releases, pinned to older Python), so this unit ships a small
  **vendored RAPTOR** as the default backend and uses pyraptor only as an
  import-guarded cross-check — a good model for depending on fragile libraries safely.

### r5py and Pandana — the "fast but fragile" accelerators
- **Link:** https://r5py.readthedocs.io/ · https://udst.github.io/pandana/
- **Type:** PRACTICE
- **Summary:** r5py wraps Conveyal's R5 engine for production-grade multimodal routing
  by natively combining OSM + GTFS, but it needs a JVM (a classic Colab fragility).
  Pandana offers contraction-hierarchy shortest paths but is static-weight only (so it
  doesn't serve `w(t)`) and has compiled-extension install risk. Both are kept as
  optional/advanced alternatives; the demo and practice run on NetworkX alone.

---

## DATA — where the numbers come from

### Israel Ministry of Transport — national GTFS feed
- **Link:** https://gtfs.mot.gov.il/ (feed: `ftp://gtfs.mot.gov.il/israel-public-transportation.zip`)
- **Type:** DATA
- **Summary:** A single national GTFS feed covering effectively all licensed operators
  (~4,200 routes, 30,000+ stops, 36 agencies), free and open. It is a **rolling ~60-day
  window of planned service** — it does not archive the past, so the demo uses today's
  feed clipped to a representative weekday and states that the road-side speeds and
  transit schedule refer to different dates. For period-matched historical GTFS, use
  the community hasadna open-bus / Stride archive (https://open-bus-stride-api.hasadna.org.il/docs).

### Israel bus archive + Tel Aviv OSM road network
- **Link:** https://open-bus-stride-api.hasadna.org.il/docs (equivalent open archive)
- **Type:** DATA
- **Summary:** The course's running bus-position archive (used in Units 2–3) and the
  Unit-1 OSM road graph feed this unit's road substrate. Bus speeds are only a *proxy*
  for car speed — they include dwell time and bus-lane effects and are biased low on
  stop-dense corridors — and coverage is sparse, so free-flow OSM speed is the fallback
  where no bus data exists. Naming that bias is part of the interpretation, and it
  slightly flatters transit in the Cost-of-Anarchy comparison.

### TomTom Traffic Index — Tel Aviv (and Ayalon Highway speeds, Globes)
- **Link:** https://www.tomtom.com/traffic-index/ · https://en.globes.co.il/en/article-average-peak-hour-speed-on-ayalon-highway-down-to-14-kmh-1001525275
- **Type:** DATA
- **Summary:** These ground the **timing** of the demo's road `w(t)`: Tel Aviv shows a
  double-peak diurnal congestion shape with a deeper evening peak (~17:30) than morning,
  and Ayalon peak-hour speeds fall to ~14–24 km/h. They are a *shape* anchor only —
  city-aggregate, not per-segment — so **which** roads slow (the WHERE) stays a modeling
  choice. That "the WHEN is real, the WHERE is modeled" honesty line runs through every
  downstream result.

---

## RECENT — the research frontier

### Pándy, Qiu, Corso, Veličković, Ying, Leskovec & Liò 2022 — Learning Graph Search Heuristics (PHIL)
- **Link:** https://arxiv.org/abs/2212.03978
- **Type:** RECENT
- **Summary:** Replaces A*'s hand-built heuristic with a **learned** one: a GNN trained
  by imitation learning on search trajectories predicts `h(n)`, steering the frontier
  harder toward the goal and exploring far fewer nodes (reported ~58% fewer). The catch
  is no admissibility guarantee — the path may be sub-optimal, so you must verify. A
  learned `h` is just the far-right end of the heuristic spectrum: tightest hint, weakest
  guarantee. (No public checkpoint exists, so the practice extension is build-your-own.)

### Holliday & Dudek 2025 — Learning heuristics for transit network design with deep RL
- **Link:** https://doi.org/10.1080/21680566.2025.2561863
- **Type:** RECENT
- **Summary:** A different learning-meets-routing frontier: instead of speeding up queries
  on a fixed network, a GNN policy trained with reinforcement learning helps **design the
  network itself** (the NP-hard Transit Network Design Problem), used as a heuristic inside
  a classical metaheuristic. The hybrid beats either alone, with new results on the Mumford
  benchmark and a real Laval, Quebec redesign — the recurring pattern of "learning steers,
  classical guarantees."

### Wan, Gu & Sun 2025 — Parallel Contraction Hierarchies Can Be Efficient and Scalable
- **Link:** https://arxiv.org/abs/2412.18008
- **Type:** RECENT
- **Summary:** Shows a Contraction Hierarchies construction that parallelizes efficiently on
  multicore hardware, closing CH's historically slow build against its fast queries.
  Evidence that the *classical* side is still actively advancing in 2025 — routing is not a
  solved field that ML is simply replacing.

### Farhan, Koehler, Wang & Zhou 2025 — Dual-Hierarchy Labelling: Scaling Up Distance Queries on Dynamic Road Networks
- **Link:** https://arxiv.org/abs/2506.18013
- **Type:** RECENT
- **Summary:** Targets exactly this unit's setting — road networks whose edge weights change
  in real time — with two complementary hierarchies, one for fast queries and one for cheap
  label updates, plus a parallel variant. Reports 2–4× faster queries with much faster
  updates and a fraction of prior labelling space: fast *exact* dynamic routing without a
  learned model.

### Min & Gomes 2026 — Graph Neural Networks are Heuristics
- **Link:** https://arxiv.org/abs/2601.13465
- **Type:** RECENT
- **Summary:** The latest framing of "GNNs as heuristics": a GNN can become an *unsupervised*
  heuristic for combinatorial optimization from a single training trajectory, demonstrated on
  TSP by encoding global structural constraints as an inductive bias — no search, no
  supervision. It generalizes the direction-of-travel idea behind learned routing heuristics
  toward broader combinatorial problems.
