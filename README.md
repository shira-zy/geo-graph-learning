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

| # | Topic | Status |
|---|---|---|
| 1 | Graph Substrate — Topology & Feature Engineering | _coming soon_ |
| 2 | Trajectory Mining — Unsupervised Learning & HMM | _coming soon_ |
| 3 | Dynamic Navigation — Search Algorithms | _coming soon_ |
| 4 | Statistical Baselines — Time Series | _coming soon_ |
| 5 | Geometric Deep Learning — Spatio-Temporal GNNs | _coming soon_ |

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

## License

TODO — set before first public release.
