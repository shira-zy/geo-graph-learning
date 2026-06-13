# Unit 1 — Further reading (sources + summaries)

Every source behind this unit, as an external link with a short summary. This
page is written to be read by **you and your agent** — point your agent here for
the concepts, and at [`datasets.md`](./datasets.md) for how to load the data.

**Type key:** `THEORY` (concepts/definitions) · `PRACTICE` (tools/how-to) ·
`DATA` (datasets/empirical) · `RECENT` (current state of the field).
Where an arXiv version exists it is linked (open access); two older sources are
link-only behind a paywall and marked **(link-only)**.

---

## Foundations — what a street network *is*

### Boeing 2017 — OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks
- **Link:** https://arxiv.org/abs/1611.01890
- **Type:** PRACTICE
- **Summary:** Introduces OSMnx, the library this unit is built on, for
  downloading OpenStreetMap data and turning it into an analyzable street graph.
  Explains why a street network is modeled as a non-planar directed multigraph
  and how the toolkit projects, simplifies, and computes basic measures. The
  accessible "what is OSMnx and why" starting point.

### Boeing 2025 — Modeling and Analyzing Urban Networks and Amenities with OSMnx
- **Link:** https://arxiv.org/abs/2505.00736
- **Type:** RECENT
- **Summary:** The current OSMnx reference, matching the v2.x API the demo pins
  against. Cite the 2017 paper for the idea and this one for today's functions.
  Read it if you want the up-to-date picture of what OSMnx can model.

### Boeing 2025 — Topological Graph Simplification Solutions to the Street Intersection Miscount Problem
- **Link:** https://arxiv.org/abs/2407.00258
- **Type:** RECENT
- **Summary:** The definitive treatment of *why raw OSM miscounts intersections*
  (curved streets digitized as many segments; one junction becoming a cluster of
  nodes) and how edge simplification + node consolidation fix it. These choices
  change node counts, degree, and betweenness — so simplification is itself a
  modeling decision, not a cleanup step. The reference for the "operations as
  craft" half of the unit.

### Newman 2003 — The Structure and Function of Complex Networks
- **Link:** https://arxiv.org/abs/cond-mat/0303516
- **Type:** THEORY
- **Summary:** The heavyweight background reference for general network-science
  vocabulary — degree distributions, small-world and scale-free structure,
  clustering, components. Use it to ground the terms the unit borrows when it
  asks "is this city scale-free?" It is broad (not street-specific), so skim the
  sections you need.

---

## There is no neutral graph — primal vs. dual

### Porta, Crucitti & Latora 2006 — The Network Analysis of Urban Streets: A Primal Approach
- **Link:** https://arxiv.org/abs/physics/0506009
- **Type:** THEORY
- **Summary:** Defines the **primal** representation — intersections as nodes,
  streets as length-weighted edges — the geographic, distance-aware graph the
  demo uses. Frames the centrality family as everyday questions ("being near",
  "being between", "being direct"). The plain-language entry point to centrality.

### Crucitti, Porta & Latora 2006 — The Network Analysis of Urban Streets: A Dual Approach
- **Link:** https://arxiv.org/abs/cond-mat/0512535
- **Type:** THEORY
- **Summary:** The companion **dual** representation — streets as nodes,
  intersections as links. Its payoff is the unit's teachable surprise: the *same*
  city looks near-regular in the primal graph but shows broad, scale-free-like
  degree structure in the dual. The cleanest demonstration that the graph you
  build determines the answer you get.

### Crucitti, Latora & Porta 2006 — Centrality Measures in Spatial Networks of Urban Streets
- **Link:** https://arxiv.org/abs/physics/0504163
- **Type:** THEORY
- **Summary:** The rigorous definitions of five centrality measures (degree,
  closeness, betweenness, straightness, information) on metric-weighted primal
  graphs. Its strongest claim is that no single index *is* importance — each
  answers a different question — which is the scholarly form of the "choose the
  right metric" skill. The reference for what each metric actually computes.

---

## Operationalizing "importance" — centrality

### Freeman 1977 — A Set of Measures of Centrality Based on Betweenness  *(link-only)*
- **Link:** https://doi.org/10.2307/3033543
- **Type:** THEORY
- **Summary:** The original definition of betweenness centrality: a point's
  importance "in terms of the degree to which it falls on the shortest path
  between others." This is exactly the definition NetworkX/OSMnx implement and
  the natural "artery" metric — the streets the most shortest paths route
  through. Paywalled (JSTOR); the definition is restated in the centrality
  sources above.

---

## Structural metrics for the whole fabric

### Cardillo, Scellato, Latora & Porta 2006 — Structural Properties of Planar Graphs of Urban Street Patterns
- **Link:** https://arxiv.org/abs/physics/0510162
- **Type:** THEORY
- **Summary:** Applies the **meshedness coefficient** to 20 cities' street
  patterns — one number for "how grid-like / redundant is this fabric?",
  empirically ranging from ~0.014 (tree-like) to ~0.348 (densely meshed New
  York). Also shows street networks have low clustering (right-angle grids make
  squares, not triangles). The source for the single-number structural measures.

### Buhl et al. 2004 — Efficiency and Robustness in Ant Networks of Galleries  *(link-only)*
- **Link:** https://doi.org/10.1140/epjb/e2004-00364-9
- **Type:** THEORY
- **Summary:** The original definition of the meshedness coefficient
  m = (E − N + 1) / (2N − 5) — the ratio of a planar graph's actual independent
  cycles to its planar maximum, bounded in [0, 1]. Introduced for ant gallery
  networks; Cardillo et al. (above) carried it over to city streets. Paywalled
  (Springer); the formula and bounds are restated in the Cardillo paper.

---

## The field at scale + the current map

### Boeing 2020 — A Multi-Scale Analysis of 27,000 Urban Street Networks
- **Link:** https://arxiv.org/abs/1705.02198
- **Type:** DATA
- **Summary:** Computes purely structural indicators (intersection density,
  connectivity, circuity) across every US city, town, and urbanized area, showing
  they vary systematically across places — evidence that topology alone carries
  spatial signal. Pairs with the Harvard Dataverse indicator tables (see
  [`datasets.md`](./datasets.md)) that let you say whether *your* city's number
  is high or low among thousands.

### Barthelemy & Boeing 2024 — A Review of the Structure of Street Networks
- **Link:** https://arxiv.org/abs/2409.08016
- **Type:** RECENT
- **Summary:** A short, current, open-access survey by two leaders of the field —
  the best single map of the whole topic. It also delivers a useful pruning
  result: the classical alpha/beta/gamma transportation indices are largely
  redundant (they mostly track average degree), so this unit can defensibly skip
  them. Start here if you want the big picture quickly.

---

## Web topics (practitioner clusters, not single papers)

### Does betweenness centrality actually predict traffic flow?
- **Links:**
  Kazerani & Winter 2009, *Can Betweenness Centrality Explain Traffic Flow?* —
  https://doi.org/10.13140/2.1.1739.0089 ·
  Gao, Wang, Gao & Liu 2013, *Understanding Urban Traffic-Flow Characteristics:
  A Rethinking of Betweenness Centrality* — https://doi.org/10.1068/b38141
- **Type:** THEORY
- **Summary:** The honest caveat behind the "artery" question: betweenness is a
  *structural proxy*, not a measurement of realized traffic. It ignores demand
  and distance-decay, so it overestimates flow at the most central nodes; adding
  origin/destination heterogeneity and a distance-decay term reproduces observed
  flow far better than topology alone. A high-betweenness map is a hypothesis
  about flow, not a measurement — this is where the INTERPRET skill and the
  practice extension ("when is a topology-only answer misleading?") live.

### Library-stack alternatives if OSMnx/NetworkX prove fragile
- **Links:**
  pyrosm "Working with graphs" — https://pyrosm.readthedocs.io/en/latest/graphs.html ·
  igraph vs NetworkX benchmark — https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages-v2/ ·
  graph-tool performance — https://graph-tool.skewed.de/performance.html ·
  OSMnx issue #153 (NetworkX backend is slow) — https://github.com/gboeing/osmnx/issues/153
- **Type:** PRACTICE
- **Summary:** Practical guidance on speed and loading. NetworkX centrality is
  pure-Python and slow (~8× slower than igraph for betweenness on mid-size
  graphs), so the unit keeps an igraph fallback for the heavy betweenness call.
  pyrosm reads a local `.osm.pbf` extract (no live Overpass) and exports an
  OSMnx-compatible graph — which is how the demo stays self-contained. graph-tool
  is fastest but hard to install on Colab, so it's a pointer only.
