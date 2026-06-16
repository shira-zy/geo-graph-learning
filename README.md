# Geospatial Graph Learning

Student materials for the **Geospatial Graph Learning** chapter of a Geo-AI
course: 15 hours across 5 units, bridging Network Science and modern Deep
Learning by treating the city as a learnable graph.

Each unit has three parts:

1. **Theory (45 min)** — slide deck (PDF + HTML).
2. **Demo (45 min)** — Jupyter notebook, Colab-first, runs locally too.
3. **Supervised practice (1 h)** — open-ended task you tackle with Claude Code
   while applying the **direct → interpret → extend** rubric.

## Units

Unit numbers follow **teach order** (which is also the unit-number
order). This means our Unit 3 = Statistical Baselines and our Unit 4 =
Dynamic Navigation — inverse of the original syllabus PDF. See the
"Numbering note" at the top of the working outline (instructor-side).

| # | Topic | Capability after this unit | Status |
|---|---|---|---|
| 1 | [Graph Substrate](unit-1-graph-substrate/) | Topology metrics as analyzable signal; choosing graph + metric for a question. | _coming soon_ |
| 2 | [Trajectory Mining](unit-2-trajectory-mining/) | Trajectories on AND off the graph; noise model + inference direction. | _coming soon_ |
| 3 | [Statistical Baselines](unit-3-statistical-baselines/) | Univariate forecasting baseline + breakeven horizon + spatial gap. | _coming soon_ |
| 4 | [Dynamic Navigation](unit-4-dynamic-navigation/) | Routing under w(t) + multimodal (road vs. transit) Cost of Anarchy. | _coming soon_ |
| 5 | [Spatio-Temporal GNNs](unit-5-gnn/) | ST-GNN that earns its complexity; attention interrogation. | _coming soon_ |

Lessons are published as tagged releases (`v-unit1`, `v-unit2`, …). Sync your
fork to pull new lessons.

## Getting started

Read [`SETUP.md`](./SETUP.md). Briefly:

1. Fork this repo to your GitHub account.
2. Clone your fork.
3. Install Claude Code (CLI) and `uv`.
4. `uv sync --extra unit-1` (or `--extra all` for everything).
5. Your work goes in `student-work/` directories — they're conflict-free
   space designed to survive upstream syncs.

## The rubric

[`rubric.md`](./rubric.md) — five checks, three verbs (DIRECT / INTERPRET /
EXTEND). You'll apply this every supervised-practice hour. Memorize it by
Unit 3.

## Decision log

[`decision-log-template.md`](./decision-log-template.md) — the artifact you
fill during each supervised hour. Push it to your fork before asking for
async help.

## Asking for help

If you're stuck on something async:

1. Push your work (including a partial decision log) to your fork.
2. Share your fork URL with the instructor.
3. The instructor can clone your fork and see your actual code + your
   reasoning — much more useful than a screenshot.

## Two ways to run

Every unit runs both ways — pick whichever fits you:

- **Local with `uv` (recommended):** `uv sync --extra unit-<N>`, then launch
  Jupyter *from inside that env* so it uses the right kernel automatically —
  identical on macOS and Windows:

  ```bash
  uv run --extra unit-<N> jupyter lab
  ```

  (Launching a system `jupyter` instead is the #1 "imports fail after `uv sync`"
  trap.) Full walkthrough in [`SETUP.md`](./SETUP.md#7-open-a-notebook-locally-with-the-right-kernel).
- **Colab (one click):** open the notebook's "Open in Colab" badge; the first
  cell runs `setup_colab.py`, which installs the unit's published
  `requirements/unit-<N>.txt`. Nothing to pre-install. To keep your edits, open
  the notebook **from your own fork** and `File → Save a copy in GitHub` — see
  [`SETUP.md`](./SETUP.md#running-on-colab-and-connecting-it-to-github).

## What each unit ships

Slides (PDF + HTML), a Colab-first demo notebook, `practice-task.md`,
`homework.md`, a **reference solution notebook** (a strong path, not an answer
key — see `NOTICE.md`), `datasets.md` (data sources + how to load them), and
`further-reading.md` (AI-friendly source summaries).

## Rights & disclaimer

See [`NOTICE.md`](./NOTICE.md) — © 2026 Ben Galon, all rights reserved
(Geo-AI course, The Arena). Materials are AI-assisted and instructor-reviewed;
verify before relying on them. Provided to enrolled students; not for
redistribution.
