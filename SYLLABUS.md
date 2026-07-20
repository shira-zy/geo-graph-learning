# Syllabus — Geospatial Graph Learning

A 5-unit chapter of a Geo-AI course (15 hours of class time). We treat the
city — its roads, sensors, trajectories, and transit — as a **learnable graph**,
and bridge classical Network Science with modern Deep Learning.

This course is not about out-typing the AI. It is about becoming the analyst who
can **DIRECT** an AI with precise vocabulary, **CHOOSE** the right analysis for a
real question, and **INTERPRET** the results in domain terms — catching both the
expected patterns and the surprises worth chasing.

---

## How every unit is structured

Each unit is **3 hours**, in three parts:

1. **Theory (45 min)** — a slide deck (PDF + HTML).
2. **Demo (45 min)** — a Jupyter notebook, **Colab-first**, that also runs locally.
3. **Supervised practice (60 min)** — an open-ended task you tackle *with* Claude
   Code, applying the rubric below. The deliverable is your **decision log**, not
   a polished notebook.

Every supervised hour follows the same rhythm: ~5 min restate the task · ~40 min
work the loop · ~10 min debrief · ~5 min synthesis.

### The rubric you apply every supervised hour

**direct → interpret → extend** — five checks, three verbs (see
[`rubric.md`](./rubric.md)):

- **DIRECT** — Did I use this unit's vocabulary? Did I specify inputs precisely
  (which city, which metric, which window)?
- **INTERPRET** — Can I explain the result in my own domain words? Did I notice
  anything that didn't match my expectation?
- **EXTEND** — Did I ask a follow-up grounded in what the result revealed?

You fill [`decision-log-template.md`](./decision-log-template.md) as you go.
Memorize the rubric by Unit 3.

### The "wrong-class" question

Every unit's practice hides **one question this unit's tools should *not* answer**.
Recognizing it — and saying *what would have to change* to make it a good fit — is
half the skill. That is the **CHOOSE** muscle.

---

## The five units

Unit numbers follow **teach order** (which is also unit-number order: 1 → 2 → 3 →
4 → 5). Note: our Unit 3 = Statistical Baselines and Unit 4 = Dynamic Navigation —
the inverse of the original syllabus PDF.

| # | Unit | Motivating question | Capability after this unit | Status |
|---|------|---------------------|----------------------------|--------|
| **1** | **[Graph Substrate](unit-1-graph-substrate/)** | Looking only at a road map, which streets are the *arteries* — and how do you define "artery" rigorously enough that a computer can find them? | Turn a road map into a graph; treat topology metrics (centrality, etc.) as analyzable signal; choose the graph + metric that fits a question. | ✅ **Ready** |
| **2** | **[Trajectory Mining](unit-2-trajectory-mining/)** | One bus's GPS is sparse noise — but hundreds run the line daily. Can you reconstruct the *shape* of a bus line, then a whole bus network, from many noisy traces? | Place trajectories **on and off** the graph (map-matching vs. free movement); reason about the noise model and the direction of inference. | ✅ **Ready** |
| **3** | **[Statistical Baselines](unit-3-statistical-baselines/)** | Forecasting sensor 42 from only its own past: how far ahead before a dumb historical-average baseline ties you — and how much error is because time *alone* can't see upstream sensors? | Build a univariate forecasting baseline; find the **breakeven horizon**; name the **spatial gap** a non-spatial model leaves on the table. | ✅ **Ready** |
| **4** | **[Dynamic Navigation](unit-4-dynamic-navigation/)** | At 8am the car app says 35 min, the bus app says 28. Which is *the* answer — and across every commuter, how much total travel time turns on mode and timing? | Route under time-varying cost **w(t)** (road) and over transit (RAPTOR/CSA); quantify the multimodal **"Cost of Anarchy."** | 🔬 **Preview** |
| **5** | **[Spatio-Temporal GNNs](unit-5-gnn/)** | Here's a congestion shockwave moving between intersections. Can a GNN predict where it'll be in 15 min — and can you *read from the model why*? | Build a spatio-temporal GNN that **earns its complexity** over the baselines; interrogate its attention to explain a prediction. | 🔬 **Preview** |

**Status key.** ✅ **Ready** — finalized: theory, demo, and practice are complete.
🔬 **Preview** — the demo is available so you can look ahead, but the content **may
still change** before we teach the unit. Treat preview material as a draft.

### Two bookend sessions

The five units are wrapped by two short slides-only sessions (no demo, practice,
or homework):

- **[Unit 0 — Course intro](unit-0-course-intro/)** (~15 min, once before Unit 1) —
  how the course works: the North Star, the rubric, and the fork/work/share
  workflow.
- **[Unit 6 — Course closing](unit-6-course-closing/)** (~30 min, once after Unit 5) —
  the arc recap (one slide per unit → the single pipeline), working with AI on
  your own projects, and the before/after mirror of where we started.

### One thread runs through the course

A real-city **bus archive** (sparse GPS pings) is the spine that connects the
back half: **Unit 2** reconstructs routes from the traces, **Units 3–4** turn them
into segment-speed forecasts and routing under uncertainty, and **Unit 5** learns
a predictor over the resulting graph. Watch the **Lagrangian → Eulerian** shift —
from following individual vehicles (U2) to fixed-sensor time series (U3+).

---

## How lessons reach you

The full course is **5 units**. Units **1–3 are final today**; Units **4–5 are
preview** and will be finalized before we teach them.

Lessons publish as **tagged releases** (`v-unit1`, `v-unit2`, …). **Sync your fork**
to pull each unit as it lands — including updates to the preview units. New
material arrives in disjoint `unit-N-*/` folders, so syncing never touches your
work in `student-work/`.

---

## Getting started

Read [`SETUP.md`](./SETUP.md). Briefly:

1. Fork this repo to your GitHub account, then clone your fork.
2. Install Claude Code (CLI) and `uv`.
3. `uv sync --extra unit-1` (or `--extra all` for everything available).
4. Open the Unit 1 demo notebook and run its **smoke-test cell** to confirm your
   environment — locally or via the "Open in Colab" badge.
5. Do your work in `student-work/` — conflict-free space that survives upstream
   syncs.

## Asking for help (async)

Push your work — *including a partial decision log* — to your fork and share the
URL. The instructor can clone it and see your actual code **and your reasoning**,
which is far more useful than a screenshot.

---

## Rights & disclaimer

© 2026 Ben Galon. All rights reserved. Part of the **Geo-AI course (The Arena)**.
Provided to enrolled students for course use; not for redistribution. Materials
are **AI-assisted and instructor-reviewed** — learning references, not
guaranteed-correct keys; verify before you rely on them. See
[`NOTICE.md`](./NOTICE.md) for the full notice.
