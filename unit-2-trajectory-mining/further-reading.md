# Unit 2 — Further reading (AI-friendly sources)

Every source behind the Unit 2 theory, demo, and practice — grouped, with a
2–3 sentence summary written so **your agent can use it as context**. Links are
external (DOI / arXiv / project pages). Paywalled items are link-only.

> How to use this with an agent: paste a summary + link into your prompt when
> you want the agent to apply a specific method ("match with the Newson–Krumm
> HMM emission/transition model", "grade inferred edges with buffered
> precision/recall"). The vocabulary here is the vocabulary the rubric rewards.

---

## Map matching — classical (the demo's method)

- **Newson & Krumm (2009), "Hidden Markov Map Matching Through Noise and Sparseness."**
  The HMM formulation the demo implements: road segments are hidden states, GPS
  pings are observations, a **Gaussian emission** scores ping-to-segment distance
  and a **transition** term rewards on-road moves whose route distance ≈
  straight-line distance. Their σ ≈ 4 m on car GPS is the starting point we sweep.
  https://doi.org/10.1145/1653771.1653818

- **Lou et al. (2009), "Map-Matching for Low-Sampling-Rate GPS Trajectories" (ST-Matching).**
  Adds a **spatial + temporal/speed** analysis for sparse GPS (≈ 1 fix/min — our
  bus regime), where the plain geometric HMM weakens. We name ST-Matching as the
  principled upgrade for low-sampling-rate data without implementing it.
  https://doi.org/10.1145/1653771.1653820

- **Quddus, Ochieng & Noland (2007), "Current Map-Matching Algorithms for Transport Applications."**
  The survey that organizes map matching into geometric / topological /
  probabilistic / advanced families. Use it to place any method (including the
  HMM) in the broader landscape. https://doi.org/10.1016/j.trc.2007.05.002

## Map matching — recent / learned (the frontier beat)

- **Jiang, Chen & Chen (2023), "L2MM: Learning to Map Matching … for Low-Quality GPS."**
  Learns trajectory + road embeddings so matching is robust to exactly the
  noise/sparsity we face; reports gains over HMMs on low-quality data. The
  "learned matcher beats classical on sparse GPS" headline. https://doi.org/10.1145/3550486

- **Mohammadi & Smyth (2024/2025), "MMformer: Transformer-Based Trajectory Map-Matching."**
  Casts matching as sequence-to-sequence "translation": read the ping sequence,
  write the road-edge sequence. ~10% accuracy gains at large-network scale.
  arXiv: https://arxiv.org/abs/2404.12460 · IEEE TITS: https://doi.org/10.1109/TITS.2025.3565009

- **Han, Yang & Hu (2026), "DiffMM: … via One-Step Diffusion."**
  Treats matching as **denoising** — start from a noisy route guess and diffuse it
  toward a clean on-road path in one step; targets sparse+noisy GPS and claims
  SOTA accuracy *and* speed. The slide-only headline; the one frontier matcher
  with released code (no pretrained checkpoint, so not class-ready). arXiv:
  https://arxiv.org/abs/2601.08482 · https://doi.org/10.1609/aaai.v40i17.38498

- **Shi et al. (2023), "LHMM: A Learning Enhanced HMM Model."**
  A hybrid — keep the interpretable HMM skeleton, learn its emission/transition
  terms. The bridge between the demo's glass-box HMM and the learned frontier.
  https://doi.org/10.1109/ICDE55515.2023.00207

## Map inference — classical (the practice's method)

- **Cao & Krumm (2009), "From GPS Traces to a Routable Road Map."**
  The seminal inverse-problem paper: turn raw traces into a usable graph by
  clarifying/attracting traces then tracing centrelines. The conceptual root of
  the practice. https://doi.org/10.1145/1653771.1653776

- **Biagioni & Eriksson (2012), "Inferring Road Maps from GPS Traces: Survey and Comparative Evaluation."**
  Organizes inference into KDE/density, trace-merging, and intersection-linking
  families, and standardizes the **precision/recall** evaluation the practice
  uses. It also states the rule that **coverage caps recall**. https://doi.org/10.3141/2291-08

- **Davies, Beresford & Hopper (2006), "Scalable, Distributed, Real-Time Map Generation."**
  An early density→centreline pipeline (KDE of traces → contour → skeleton) — the
  direct ancestor of the demo's Step 9 and the practice's raster recipe.
  https://doi.org/10.1109/MPRV.2006.83

- **Ahmed, Karagiorgou, Pfoser & Wenk (2015), "A Comparison and Evaluation of Map Construction Algorithms."**
  Benchmarks inference algorithms on vehicle-tracking data and defines the
  graph-distance/TOPO-style metrics; the research-grade version of the buffered
  precision/recall we simplify to a raster overlap for class. https://doi.org/10.1007/s10707-014-0222-6

- **He et al. (2018), "RoadRunner: Improving the Precision of Road Network Inference."**
  A precision-first inference method; useful contrast for the practice's
  precision-vs-recall trade-off discussion. https://doi.org/10.1145/3274895.3274974

## Map inference — recent / learned (the frontier beat)

- **Eftelioglu et al. (2022), "RING-Net: Road Inference from GPS Trajectories Using a Deep Segmentation Network."**
  Rasterize traces into an image, then segment roads with a CNN — the learned
  analogue of density→skeleton. The predecessor to DGMap. https://doi.org/10.1145/3557917.3567617

- **Liu, Mao, Wu et al. (2025), "DGMap: A Dual-Decoding Framework with Global Context for Map Inference" (CIKM '25).**
  The cleanest "learned version of what you built": its grid-encode /
  keypoint-detect / relation modules map almost one-to-one onto KDE /
  junction-detection / assembly. https://doi.org/10.1145/3746252.3761537

- **Wu, Mao, Liu et al. (2025), "CDMap: Complementarity and Disparity-Aware Map Inference Quality Enhancement" (ICDE '25).**
  A 2025 quality-enhancement method; evidence the inference field is still moving
  fast. https://doi.org/10.1109/ICDE65448.2025.00316

## Smoothing, similarity & clustering

- **Welch & Bishop (2006), "An Introduction to the Kalman Filter."**
  The standard gentle introduction to the predict/update recursion, process vs.
  measurement noise, and the Kalman gain — background for the demo's "honest
  failure" Kalman beat. https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf

- **Berndt & Clifford (1994), "Using Dynamic Time Warping to Find Patterns in Time Series."**
  The original DTW-for-sequences paper: the DP recurrence and warping path that
  let same-shape/different-speed trajectories align. Underpins the practice's
  DTW-vs-Euclidean extension. https://cdn.aaai.org/Workshops/1994/WS-94-03/WS94-03-031.pdf

- **Toohey & Duckham (2015), "Trajectory Similarity Measures."**
  Compact comparison of Euclidean, DTW, LCSS, Fréchet and Hausdorff — the menu
  for "which distance fits variable-speed trajectories?" https://doi.org/10.1145/2782759.2782767

## Datasets

- **Open Bus / The Public Knowledge Workshop (HaSadna), 2023.**
  The SIRI real-time GPS archive of Israel's public transport — the source of the
  demo + practice bus data. https://github.com/hasadna/open-bus

- **Zheng, Xie & Ma (2010), "GeoLife."**
  17,621 user GPS trajectories (Beijing), many at 1–5 s cadence — a dense-GPS
  contrast for extending the practice.
  https://www.microsoft.com/en-us/research/publication/geolife-a-collaborative-social-networking-service-among-user-location-and-trajectory/

- **Porto Taxi (ECML/PKDD 2015, UCI).** 1.7 M taxi trajectories in one city.
  https://doi.org/10.24432/C55W25

- **Map Construction benchmarks (Ahmed et al., 2015), mapconstruction.org.**
  Trajectory datasets *with* ground-truth road maps + evaluation code — the
  standard map-inference testbed. http://www.mapconstruction.org

## Tooling

- **LeuvenMapMatching (Meert & Verbeke).** Pure-Python HMM map matcher
  (`DistanceMatcher`, `InMemMap`) the demo builds on; exposes custom
  emission/transition + non-emitting states for the σ sweep. https://github.com/wannesm/LeuvenMapMatching

- **FMM — Fast Map Matching (Yang & Gidofalvi, 2018).** Very fast C++ matcher;
  noted as an alternative but its build (C++/SWIG/GDAL) is a Colab risk, which is
  why we teach with the pure-Python Leuven stack. https://doi.org/10.1080/13658816.2017.1400548

- **mappymatch (NREL).** Pure-Python matching package (LCSS-based); an
  alternative mechanism noted for contrast. https://github.com/NREL/mappymatch
