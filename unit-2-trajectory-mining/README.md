# Unit 2 — Trajectory Mining

**Capability after this unit:** turn noisy GPS into matched trajectories
(*forward* inference — HMM map matching) **or** infer a road network back from
raw GPS alone (*inverse* — KDE → skeleton → graph). The unifying idea is that
**noise is a modeling decision**: you choose an emission (noise) prior and a
transition (network) prior, then run the same frame in either direction. You
finish able to **choose the noise model and inference direction by the
question**, and to say where classical methods suffice and where the learned
frontier is moving.

This unit runs on the **Tel Aviv bus archive** (a SIRI real-time GPS feed at
~1 fix per vehicle per minute) and OpenStreetMap.

---

## What's here

| File | What it is |
|---|---|
| [`theory.pdf`](./theory.pdf) / [`theory.html`](./theory.html) | The 44-slide theory deck (45 min). Citations are external DOI/arXiv links. |
| [`geoai-graph-unit2.ipynb`](./geoai-graph-unit2.ipynb) | **Demo** — a 9-step HMM map-matching arc on bus line 13429: raw pings → pooled → Kalman (honest failure) → HMM + Viterbi → σ sweep → bearing-aware matching → inverse map inference. Colab-first; smoke-test cell up top. |
| [`practice-task.md`](./practice-task.md) | **Supervised practice** — infer the *whole* Tel Aviv street network from all bus pings, then reveal OSM and grade it (raster precision/recall, bandwidth sweep, per-edge confidence). |
| [`homework.md`](./homework.md) | The take-home extension. |
| [`geoai-graph-unit2-solution.ipynb`](./geoai-graph-unit2-solution.ipynb) | **Reference solution** — *a* complete, runnable path through the practice (not an answer key; the task is open-ended). Carries an AI-assisted disclaimer. |
| [`datasets.md`](./datasets.md) | Every data source + exact IDs/bbox, and how to access them **locally (`uv`)** and **on Colab**. |
| [`further-reading.md`](./further-reading.md) | AI-friendly sources page — every paper + tool as an external link + a short summary, grouped THEORY / RECENT / DATA / TOOLING. |
| [`references.bib`](./references.bib) | The unit's BibTeX (machine-readable citations pairing with `further-reading.md`). |
| [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) | "If you see X, do Y" — the fragile bits (Leuven `min_prob_norm`, `filterpy` build, `rtree` on Windows, Overpass flakiness, folium-in-Colab trust). |

## How to run

- **Local (`uv`):** `uv sync --extra unit-2`, then open the notebook with the
  `geo-graph` kernel. See [`../SETUP.md`](../SETUP.md).
- **Colab:** click the badge at the top of the demo notebook; the first cell
  installs the unit's published dependencies. Nothing to pre-stage — each
  notebook fetches and subsets its own data inline.

See [`datasets.md`](./datasets.md) for data access and
[`further-reading.md`](./further-reading.md) for the concepts (both written so
your agent can use them as context).

## Where this sits in the course

- **Unit 1** built the OSM road graph you match against here.
- **Unit 3** picks up exactly where this leaves off — the **Lagrangian →
  Eulerian** shift: matched trajectories aggregate into per-segment speed time
  series.
- **Units 4–5** reuse the matched trajectories + network as travel-time weights
  and as the GNN substrate.

---

Rights & disclaimer: see [`../NOTICE.md`](../NOTICE.md). Materials are
AI-assisted and instructor-reviewed — verify before you rely on them. Your work
goes in [`student-work/`](./student-work/).
