# Unit 5 — Geometric Deep Learning (Spatio-Temporal GNNs)

**Capability after this unit:** train a small **spatio-temporal graph neural
network** (a GCN inside a GRU — **T-GCN**, then attention-augmented **A3T-GCN**)
and use it to close the **spatial gap** Unit 3 measured — the upstream neighbour a
univariate forecaster is blind to. You learn to read message passing as a **k-hop
receptive field over space and time**, to **interrogate attention weights** as an
*observable hypothesis* about network causality (never as proof — and never confuse
attention over *time steps* with attention over *nodes*), and — the capstone
judgement — to **defend whether a GNN actually earns its complexity** over Unit 3's
baseline, or is overkill for a small, thin problem. You finish able to **direct** an
AI in this unit's vocabulary, **choose** whether a GNN is even the right tool, and
**interpret** its forecasts and its attention honestly.

The **demo** forecasts **METR-LA** (207 LA freeway sensors) and races the GNN
against Unit 3's SARIMA + historical-average floor across 15/30/60-min horizons.
The **practice** re-frames Unit 3's ~10-segment Tel-Aviv **bus corridor** as a
graph and asks whether a T-GCN pushes the breakeven horizon outward — or whether ten
independent SARIMAs were enough.

> **Numbering note.** Geometric Deep Learning is **Unit 5** in our teach order (the
> capstone). Every public-side artifact uses the teach-order numbering.

---

## What's here

| File | What it is |
|---|---|
| [`theory.pdf`](./theory.pdf) / [`theory.html`](./theory.html) | The theory deck: the spatial gap → message passing (GCN → GAT) → adding time (T-GCN = GCN+GRU) → attention as interrogable structure (A3T-GCN, temporal ≠ spatial) → when a GNN earns its complexity. Figure-rich; citations are external DOI/arXiv links. |
| [`geoai-graph-unit5.ipynb`](./geoai-graph-unit5.ipynb) | **Demo** — load METR-LA as a spatio-temporal graph, find a real congestion **shockwave**, **live-train a T-GCN**, race it against Unit 3's baseline across horizons, then load a pre-trained **A3T-GCN** and read its attention *honestly* (temporal attention paired with Unit 3's spatial cross-correlation). Colab-first; smoke-test cell up top. |
| [`practice-task.md`](./practice-task.md) | **Supervised practice** — build the bus-corridor graph, choose a directed-vs-undirected adjacency (a **graded design decision**), train a small T-GCN, evaluate 15/30/60-min vs a floor + your U3 SARIMA, mark the breakeven, and deliver an honest "did the GNN earn it?" verdict. |
| [`homework.md`](./homework.md) | The take-home capstone end-game: roll the trained T-GCN forward to an **A→B transit travel-time** at a future departure, and say how far ahead a rider should trust it. |
| [`geoai-graph-unit5-solution.ipynb`](./geoai-graph-unit5-solution.ipynb) | **Reference solution** — *a* complete, runnable path through the practice (not an answer key; the task is open-ended, and an honest "a GNN is overkill here" is a top answer). Reuses the demo's helpers; carries an AI-assisted disclaimer. |
| [`datasets.md`](./datasets.md) | Every data source + exact IDs, and how to access them **locally (`uv`)** and **on Colab** (METR-LA via the bundled loader; the bus corridor `.npz`, with a self-contained synthetic fallback). |
| [`further-reading.md`](./further-reading.md) | AI-friendly sources page — every paper + tool as an external link + a short summary, grouped THEORY / PRACTICE / DATA / RECENT. |
| [`references.bib`](./references.bib) | The unit's BibTeX (machine-readable citations pairing with `further-reading.md`). |
| [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) | "If you see X, do Y" — the fragile bits (the PyG / PyG-Temporal install, torch-version ABI, the optional `torch_scatter`/`torch_sparse`, GPU-vs-CPU training, the checkpoint/data fallbacks, and the temporal-≠-spatial honesty invariant). |

## How to run

- **Local (`uv`):** `uv sync --extra unit-5`, then open the notebook with the
  `geo-graph` kernel. See [`../SETUP.md`](../SETUP.md). The `unit-5` extra installs
  the pip-safe leaves (scikit-learn, matplotlib, folium, gdown, numpy); the fragile
  **PyG stack** (`torch`, `torch_geometric`, `torch-geometric-temporal`) is installed
  separately — on Colab by the setup cell, locally per `KNOWN_ISSUES.md`. **Do not
  pin torch.**
- **Colab (recommended for this unit — GPU):** click the badge at the top of the
  demo notebook; the first cell runs `setup_colab.py`, which detects Colab's torch
  and pulls matching PyG wheels. METR-LA auto-downloads; nothing to pre-stage. Use a
  **T4 GPU** runtime for the live-train experience.

> This is the course's most fragile install. If an import fails, read
> [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) first — most failures are a torch↔PyG
> version mismatch or the optional scatter/sparse wheels, both documented there.

See [`datasets.md`](./datasets.md) for data access and
[`further-reading.md`](./further-reading.md) for the concepts (both written so your
agent can use them as context).

## Where this sits in the course

- **Unit 1** produced the graph / adjacency / CRS mental model the ST-GNN operates on.
- **Unit 3** *measured* the spatial gap — the univariate **breakeven horizon** and
  the upstream cross-correlation — and supplies the SARIMA + historical-average
  baseline this unit must beat. Same corridor, same 15/30/60-min horizons, so the
  comparison is apples-to-apples.
- **Unit 4** contributed the time-varying-edge-weight (`w(t)`) framing; the GNN here
  supplies a **learned** version of that signal and must beat the modeled baseline.
- **This unit** is the **capstone**: it closes the gap with message passing, turns
  the attention map into an interrogable spatial hypothesis, and ends on the honest
  judgement of *when the complexity was worth it*.

---

Rights & disclaimer: see [`../NOTICE.md`](../NOTICE.md). Materials are AI-assisted
and instructor-reviewed — verify before you rely on them. Your work goes in
[`student-work/`](./student-work/).
