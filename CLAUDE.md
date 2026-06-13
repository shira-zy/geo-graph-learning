# Geospatial Graph Learning — Student Repo

This is the **student-facing** repo for the Geospatial Graph Learning chapter
of a Geo-AI course. It contains presentations, demos, dataset links, and
self-work scaffolding. Fork it to do the exercises.

**Pedagogical thesis** (the rubric you'll apply every supervised hour):

> Each unit equips you with enough graph/geo understanding to:
> 1. **DIRECT** an AI using domain-precise vocabulary
> 2. **CHOOSE** the right analysis for a real question
> 3. **INTERPRET** the AI's results in domain terms

See `rubric.md` and `decision-log-template.md` for the artifacts you'll fill
during practice.

---

## HARD CONSTRAINTS (read every time you touch this repo)

### Colab-first

Every demo notebook MUST run end-to-end on a fresh free-tier Colab runtime.
Local execution (macOS, Windows) is the secondary target. If you change a
notebook, you verify Colab still works before committing.

### Reference solutions are provided — they are not answer keys

Each unit ships a reference solution notebook
(`geoai-graph-unit<N>-solution.ipynb`) so you can see *a* complete, runnable
path and confirm the task is feasible. It carries a disclaimer: it is
AI-assisted, may be only static-checked, and the task is open-ended — there is
no single correct answer. **Use it to check your reasoning, not to copy.** You
are graded on your own direct → interpret → extend loop. Do NOT write new
answer keys into this repo.

### Single source for dependencies

`pyproject.toml` is the ONLY hand-edited dependency file. Files under
`requirements/` are AUTO-GENERATED — never hand-edit them. To regenerate:

```bash
bash scripts/export-requirements.sh
```

### Cross-platform local

Local install must work on macOS (instructor's primary) AND Windows (some
students). If a library is unavailable on Windows, document the workaround
in the lesson's `KNOWN_ISSUES.md`.

### `student-work/` is sacred

Per-unit `student-work/` directories (and the optional root one) exist for
students working in their forks. **NEVER modify these after initial scaffold.**
Doing so causes merge conflicts when students sync upstream.

### Cite via external links only

Slides and notebooks reference papers via DOI / arXiv URLs. There is no
instructor-side BibTeX in this repo — the `promoter` subagent converts
BibTeX keys to inline external links when copying lessons here.

### Per-notebook smoke-test cell

Every demo notebook has a smoke-test cell near the top: bare imports + one
trivial call per major library, with a clear error message pointing to the
unit's `KNOWN_ISSUES.md` on failure. Fail fast, before any teaching content.

### English only

Slides, notebooks, READMEs, code comments.

---

## Tooling & data access (for you and your agent)

Each unit lists its exact stack and data sources in its own
`datasets.md` and `further-reading.md`. General rules:

**Environment.** Dependencies live in `pyproject.toml` (per-unit extras).
- **Local (macOS / Windows), recommended:** install `uv` (see `SETUP.md`), then
  `uv sync --extra unit-<N>`. Run notebooks with that environment's kernel.
- **Colab:** the notebook's first cell calls `setup_colab.py`, which installs
  the unit's published `requirements/unit-<N>.txt`. Nothing to pre-install.
- You may need to **add an environment layer yourself**: paths differ (Colab
  uses `/content`; local uses your cwd), and data caches live in different
  places. The notebooks handle the common cases; if you move data, tell your
  agent the new path explicitly.

**Unit 1 stack:** OSMnx v2, NetworkX, GeoPandas, Shapely, pyrosm, igraph,
folium, mapclassify, requests, gdown.

**Unit 1 data:** OpenStreetMap, fetched at runtime — no pre-staged files.
- Primary: a **Geofabrik** regional extract (`israel-and-palestine-latest.osm.pbf`),
  downloaded once (cached) and cut to a city bounding box **inline with pyrosm**.
- The demo *showcases* the live OSMnx/Overpass pull idiom but does not depend on
  it. A Google-Drive copy is a fallback. See `unit-1-graph-substrate/datasets.md`.

**When directing your agent:** name the tool + operation in unit vocabulary
("simplified, UTM-projected, LCC primal graph; length-weighted betweenness via
igraph"), point it at `datasets.md` for how to load data, and at
`further-reading.md` for the concepts. That is enough for it to build the
practice solution.

## Working with this repo

If you're a student:

- Read `SETUP.md` first (install + fork + sync workflow).
- Read `rubric.md` and `decision-log-template.md` before your first supervised hour.
- Your work goes in `student-work/` directories. The rest is read-only.

If you're using Claude Code (or any agent) on this repo:

- This file is your operating context. Re-read the constraints above.
- A starter `.claude/` directory provides agent scaffolding for student work.
  Customize it for your fork; do not push customizations upstream.
