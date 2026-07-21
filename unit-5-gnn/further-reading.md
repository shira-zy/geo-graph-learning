# Unit 5 — Further reading (AI-friendly sources)

Every source behind this unit's slides, demo, and practice, as an external link
plus a short plain-language summary. It is written so that **you or your agent**
can read it as context before building the practice solution. The machine-readable
citations are in [`references.bib`](./references.bib); where to get the data and
how to load it is in [`datasets.md`](./datasets.md).

Sections: **THEORY** (the algorithms) · **PRACTICE** (the tools you'll run) ·
**DATA** (where the numbers come from) · **RECENT** (the research frontier).

---

## THEORY — message passing, graph convolution, and space + time

### Gilmer et al. 2017 — Neural Message Passing for Quantum Chemistry
- **Link:** https://arxiv.org/abs/1704.01212
- **Type:** THEORY
- **Summary:** Shows that many graph neural networks are the *same* algorithm — a
  **Message Passing Neural Network**: each node gathers a message from its
  neighbours, updates its own state, and (optionally) a readout pools node states.
  This is where the "message passing" vocabulary comes from, and it is the mental
  model for the whole unit: a **k-hop receptive field** is just **k rounds** of
  message passing.

### Kipf & Welling 2017 — Semi-Supervised Classification with Graph Convolutional Networks
- **Link:** https://arxiv.org/abs/1609.02907
- **Type:** THEORY
- **Summary:** Introduces the **GCN** layer — a localized first-order approximation
  of a spectral graph convolution that reduces to mixing each node's features with
  the **degree-normalized average of its neighbours'** features. It is cheap
  (scales linearly in the number of edges) and is the spatial operator inside
  everything this unit trains. Intuition for a road network: "smear each segment's
  speed toward its neighbours' average"; stack two layers to smear across two hops.

### Veličković et al. 2018 — Graph Attention Networks
- **Link:** https://arxiv.org/abs/1710.10903
- **Type:** THEORY
- **Summary:** Replaces the GCN's fixed degree-weights with **learned attention**:
  for each neighbour the model computes how much to listen via masked
  self-attention. Same message-passing skeleton, but the weights are now
  content-dependent *and inspectable* — the prototype for the "interrogable
  attention" idea. Crucially, the authors frame attention as an *implicit* weighting,
  i.e. a hypothesis, not a causal claim.

### Hamilton 2020 — Graph Representation Learning (book)
- **Link:** https://doi.org/10.2200/S01045ED1V01Y202009AIM046  (free PDF: https://www.cs.mcgill.ca/~wlh/grl_book/)
- **Type:** THEORY
- **Summary:** A short, free textbook that derives the neighbourhood-aggregation /
  message-passing framework cleanly and presents GCN and GAT as instances of it.
  This is the recommended first read for the math-curious: start with the GNN
  chapter if you want the equations behind the demo.

### Zhao et al. 2020 — T-GCN: A Temporal Graph Convolutional Network for Traffic Prediction
- **Link:** https://doi.org/10.1109/TITS.2019.2935152  (preprint: https://arxiv.org/abs/1811.05320)
- **Type:** THEORY
- **Summary:** Puts a GCN *inside* a GRU — the GCN captures spatial dependence at
  each time step, the GRU carries state across steps. This is the gentlest honest
  "space + time" model and the demo's **live-trained** target. Its own ablations
  (versus GCN-only and GRU-only) are the "earn your complexity" test in miniature:
  the full model has to beat *both halves* to justify combining them.

### Bai et al. 2021 — A3T-GCN: Attention Temporal Graph Convolutional Network
- **Link:** https://doi.org/10.3390/ijgi10070485  (preprint: https://arxiv.org/abs/2006.11583)
- **Type:** THEORY
- **Summary:** Adds an attention layer on top of T-GCN's GRU outputs to weight the
  importance of different **time points** and assemble global temporal information.
  This is the demo's **loaded pre-trained** model and the anchor for the honesty
  lesson: its attention is over **time steps, not neighbour nodes**, so it tells you
  *which past moments* mattered — pair it with a spatial diagnostic (lagged
  cross-correlation) for the "which upstream node" story, and never read a temporal
  heatmap as spatial causality.

### Yu et al. 2018 — Spatio-Temporal Graph Convolutional Networks (STGCN)
- **Link:** https://doi.org/10.24963/ijcai.2018/505  (preprint: https://arxiv.org/abs/1709.04875)
- **Type:** THEORY
- **Summary:** The "other family" of ST-GNN: instead of an RNN, it models time with
  **gated temporal convolutions** stacked with graph convolutions (fully
  convolutional, no recurrence). Named here as the alternative to the recurrent
  GCN+GRU story the course teaches — faster to train, a different way to reach the
  same space × time receptive field.

---

## PRACTICE — the libraries you'll run

### Rozemberczki et al. 2021 — PyTorch Geometric Temporal
- **Link:** https://doi.org/10.1145/3459637.3482014  (preprint: https://arxiv.org/abs/2104.07788)
- **Type:** PRACTICE
- **Summary:** The library the demo and solution use — spatio-temporal signal
  processing on top of PyTorch Geometric, with ready-made `TGCN` / `A3TGCN` layers
  and dataset loaders (including METR-LA). Actively maintained (v0.56.x, 2025). The
  install is the most fragile in the course: **do not pin torch**, and
  `torch_scatter`/`torch_sparse` are optional (PyG ≥2.4 uses native scatter) — see
  [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md) if imports fail.

### Fey & Lenssen 2019 — Fast Graph Representation Learning with PyTorch Geometric
- **Link:** https://arxiv.org/abs/1903.02428
- **Type:** PRACTICE
- **Summary:** The base library (PyG) that PyG-Temporal builds on: efficient message
  passing, `edge_index` graph representation, and the `GCNConv` / `GATConv` layers.
  On current Colab it installs pip-only with no compiled extension required — the
  safe core path.

---

## DATA — where the speeds come from

### Li et al. 2018 — DCRNN: Diffusion Convolutional Recurrent Neural Network (and METR-LA)
- **Link:** https://arxiv.org/abs/1707.01926
- **Type:** DATA
- **Summary:** The documentation of record for **METR-LA** (207 LA freeway loop
  detectors), the dataset the demo forecasts — bundled in PyG-Temporal and
  auto-downloaded. It also sets the **15/30/60-minute horizon convention** the unit
  reuses, and introduces the idea of modelling traffic as **diffusion on a
  *directed* graph** (capturing the upstream→downstream asymmetry a symmetric GCN
  throws away) — the reference point for the directed-vs-undirected adjacency
  decision in the practice. On METR-LA, `0` means a *missing* reading (mask it).

### Open Bus — Israel public-transport GPS archive (The Public Knowledge Workshop / HaSadna)
- **Link:** https://github.com/hasadna/open-bus
- **Type:** DATA
- **Summary:** The source of the **bus-corridor speeds** used in the practice: the
  Israel Ministry of Transport SIRI real-time feed, archived by the volunteer *Open
  Bus* project. The corridor's per-segment speed series (`bus_corridor_u5.npz`) is
  derived from this feed the same way Unit 3 built it; keep the attribution on any
  figure. Segment **geometry/adjacency** is © OpenStreetMap contributors (ODbL 1.0).
  See [`datasets.md`](./datasets.md) for exact IDs and the local-vs-Colab access.

---

## RECENT — the research frontier

### Jin et al. 2024 — Spatio-Temporal Graph Neural Networks for Predictive Learning in Urban Computing: A Survey
- **Link:** https://doi.org/10.1109/TKDE.2023.3333824  (preprint: https://arxiv.org/abs/2303.14483)
- **Type:** RECENT
- **Summary:** The authoritative recent map of ST-GNNs for urban computing — a
  space-operator × time-operator taxonomy that lets you place every model in this
  unit on one grid (spatial: GCN / GAT / diffusion; temporal: GRU / TCN /
  attention). Use it as your "where does everything fit" reference.

### Liu et al. 2023 — STAEformer: Spatio-Temporal Adaptive Embedding Makes Vanilla Transformer SOTA
- **Link:** https://doi.org/10.1145/3583780.3615160  (preprint: https://arxiv.org/abs/2308.10425)
- **Type:** RECENT
- **Summary:** Argues that years of ever-more-complex graph architectures hit
  **diminishing returns**, and that a plain transformer plus a good adaptive
  embedding beats the elaborate graph operators on METR-LA / PEMS leaderboards —
  and (unlike A3T-GCN) attends across **space** as well as time. It is the field
  admitting this unit's thesis: a GNN must *earn* its complexity. The frontier moves
  fast, so re-scan for a newer SOTA if you go deep.

---

<sub>© Geospatial Graph Learning — rights reserved (not open-CC); see the course
`NOTICE.md`. This page was drafted with AI assistance and reviewed by the
instructor.</sub>
