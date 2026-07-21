# Unit 4 — Dynamic Navigation

**Capability after this unit:** treat "shortest path" as undefined until you fix
three things — the **cost** you optimize, whether the **clock** matters (`w(t)`),
and the **abstraction** you route over (a road graph vs a transit timetable). You
run Dijkstra / A* / TDSP on the road side and **RAPTOR / CSA** on the transit side,
and you interrogate the **decision space** a router really produces — isochrones,
alternatives, and a multimodal **Cost of Anarchy** — rather than a single path. You
finish able to **direct** an AI in this unit's vocabulary, **choose** the right
abstraction for a question, and **interpret** where and when the bus actually beats
the car — while naming what is real vs modeled.

This unit routes over **Tel Aviv**: an OpenStreetMap road graph (with time-varying
edge weights) and the Israel Ministry of Transport national **GTFS** timetable. The
demo takes one cross-town trip (south TA → north TA, across the Ayalon corridor); the
practice scales it to a city-wide Cost of Anarchy over ~100 origin–destination pairs.

> **Numbering note.** Dynamic Navigation is **Unit 4** in our teach order. The
> original syllabus PDF labels it Unit 3. Every public-side artifact uses the
> teach-order numbering.

---

## What's here

| File | What it is |
|---|---|
| [`theory.pdf`](./theory.pdf) / [`theory.html`](./theory.html) | The theory deck (45 min): cost → `w(t)` + FIFO → Dijkstra/A*/TDSP → transit (time-expanded → RAPTOR/CSA) → decision space (isochrones + multimodal CoA) → wrong-class check → learned-steers-classical frontier. Citations are external DOI/arXiv links. |
| [`geoai-graph-unit4.ipynb`](./geoai-graph-unit4.ipynb) | **Demo** — one cross-town Tel Aviv O-D answered many ways: distance vs time → time-varying `w(t)` → A* → TDSP (8am vs 11am) → isochrones → a *naive* time-expanded transit graph (and why it hurts) → **RAPTOR** (the fix) → the multimodal compare. Colab-first; smoke-test cell up top. |
| [`practice-task.md`](./practice-task.md) | **Supervised practice** — scale the single trip to ~100 O-D pairs × 3 time windows into a city-wide **Cost of Anarchy**: (a) wrong-objective car CoA and (b) car-vs-transit, mapped, with a defensible quantified claim and a real-vs-modeled honesty statement. |
| [`homework.md`](./homework.md) | The take-home extensions (off-peak persistence surface; reachability + the wrong-class boundary). |
| [`geoai-graph-unit4-solution.ipynb`](./geoai-graph-unit4-solution.ipynb) | **Reference solution** — *a* complete, runnable path through the practice (not an answer key; the task is open-ended). Reuses the demo's helpers; carries an AI-assisted disclaimer. |
| [`datasets.md`](./datasets.md) | Every data source + exact IDs/bbox/O-D, and how to access them **locally (`uv`)** and **on Colab**. |
| [`further-reading.md`](./further-reading.md) | AI-friendly sources page — every paper + tool as an external link + a short summary, grouped THEORY / PRACTICE / DATA / RECENT. |
| [`references.bib`](./references.bib) | The unit's BibTeX (machine-readable citations pairing with `further-reading.md`). |
| [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) | "If you see X, do Y" — the fragile bits (GTFS FTP-on-Colab, pyraptor Python-version cap, the vendored-RAPTOR default, the Drive fallbacks). |

## How to run

- **Local (`uv`):** `uv sync --extra unit-4`, then `uv run python scripts/smoke.py
  --unit 4` to confirm the stack imports, and open the notebook with the
  `geo-graph` kernel. See [`../SETUP.md`](../SETUP.md). The `unit-4` extra installs
  osmnx, networkx, geopandas, shapely, pyproj, rtree, scipy, gtfs-kit, folium,
  mapclassify, branca, contextily, pyarrow, gdown.
- **Colab:** click the badge at the top of the demo notebook; the first cell
  installs the unit's published dependencies. Nothing to pre-stage — each notebook
  downloads and clips its own OSM + GTFS inline (with Drive fallbacks).

See [`datasets.md`](./datasets.md) for data access and
[`further-reading.md`](./further-reading.md) for the concepts (both written so your
agent can use them as context).

## Where this sits in the course

- **Unit 1** produced the OSM road graph + segment/CRS mental model this unit routes
  over.
- **Units 2–3** produced the per-segment, time-of-day speed framing that motivates
  `w(t)` (the empirical finding that stop-limited bus data is ~flat is *why* the
  road peak's timing is anchored to Ayalon/TomTom instead).
- **This unit** turns the graph into a **routing substrate** and introduces the
  `w(t)` abstraction — cost as a function of the clock — plus schedule-native transit
  routing.
- **Unit 5** inherits both: a spatio-temporal GNN routes over the same graph and its
  job is to supply a **learned / predicted** `w(t)` that must beat this unit's
  **modeled** baseline, segment by segment.

---

Rights & disclaimer: see [`../NOTICE.md`](../NOTICE.md). Materials are AI-assisted
and instructor-reviewed — verify before you rely on them. Your work goes in
[`student-work/`](./student-work/).
