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

### No solutions, ever

This repo is read-only for students. Solution notebooks live in a private
instructor repo. If you find yourself writing answer keys here, STOP.

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

## Working with this repo

If you're a student:

- Read `SETUP.md` first (install + fork + sync workflow).
- Read `rubric.md` and `decision-log-template.md` before your first supervised hour.
- Your work goes in `student-work/` directories. The rest is read-only.

If you're using Claude Code (or any agent) on this repo:

- This file is your operating context. Re-read the constraints above.
- A starter `.claude/` directory provides agent scaffolding for student work.
  Customize it for your fork; do not push customizations upstream.
