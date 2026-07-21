# Unit 5 — Supervised Practice: Train a T-GCN on the Bus Corridor, Then Ask If It Earned Its Complexity

**Time: 1 hour, in class, working WITH an AI agent.**
**You will rehearse the loop: DIRECT → INTERPRET → EXTEND.**

> In Unit 3 you cut a Tel-Aviv corridor into ~10 road segments and forecast each
> one's speed with **SARIMA**, finding a **breakeven horizon** per segment — the
> point past which your smart model stops beating a dumb historical-average
> floor. You also found the **spatial gap**: a univariate model is blind to the
> *upstream* segment whose slowdown arrives a few minutes later.
>
> In this unit's demo you watched a **T-GCN** (GCN + GRU) close exactly that gap
> on METR-LA — message passing lets each node borrow its neighbours' recent
> speed — and you saw where **A3T-GCN**'s attention is honest (it weights past
> **time steps**, not neighbour nodes) and where reading it as spatial causality
> would be a lie.
>
> Now you take the **same ~10-segment corridor from your U3 practice**, re-framed
> as a **graph** (nodes = segments, edges = adjacency, node features = the
> per-segment speed series), train a small T-GCN on it, and answer the capstone
> question:
>
> **Did the GNN push the breakeven horizon OUTWARD versus your own U3 SARIMA on
> the same segments — and is the win real, or did you overengineer a ~10-node,
> 17-day problem?** Defend your answer either way.

This is **open-ended on purpose.** There is no single correct answer — an honest
"the GNN barely helps here, and here's why" is a **top-marks result**, not a
failure. Two students who choose different adjacencies, horizons, or floors can
both produce defensible work. You are graded on the **quality of your direct →
interpret → extend loop** (`rubric.md`), not on beating U3 or maximising an R².

---

## Your first graded decision: directed or undirected adjacency?

Nobody hands you this one. The bus corridor is a chain of segments in the
direction of travel. You must choose how to wire the graph the T-GCN passes
messages over, and **justify it in domain terms**:

- **Undirected** (symmetric) — segment *i* and *i+1* exchange messages both
  ways. This is what a plain symmetric-normalized GCN wants, and it is the
  T-GCN default. But it lets a *downstream* slowdown "leak" information
  *upstream*, which is not how congestion physically propagates on a one-way bus
  corridor.
- **Directed** (upstream → downstream only) — encodes the asymmetry U3's lagged
  cross-correlation actually found: the upstream segment *leads* the downstream
  one. This matches the physics (and DCRNN's design), but a symmetric-normalized
  GCN is not built for it, so you must reason about what changes.

Name your choice in your prompt, in graph vocabulary, run it, and **interpret
how it changes the prediction** on at least one segment. This directed-vs-
undirected call is the unit's **direct → interpret** rehearsal — treat it as a
first-class decision, not a config flag.

---

## What you start from — the demo's stack, no new heavy deps

Everything you need is in **this unit's** environment (the fragile PyG install
is already in the `unit-5` extra):

- **From the demo's helper cell:** `fetch_with_fallback` (gdown → HTTP mirror,
  cached), `masked_metrics` (MAE/RMSE/MAPE — **but read the `velocity==0` note
  below before you reuse it blindly**), `plot_error_distributions` (box + hist +
  ECDF), and `plot_loss_curve`.
- **The `TGCNForecaster` model class** from the demo — a `TGCN` encoder + a
  linear head to the horizon. It already handles a 2-D `[nodes, features]` input
  (one period) as well as METR-LA's `[nodes, features, periods]`, so it drops
  straight onto the bus graph.
- **The demo's training loop** (Adam, `lr=1e-3`, MSE, step the GRU across the
  window) — mirror it; do **not** just copy the reference's answer.
- **The bus corridor data** — `bus_corridor_u5.npz` (fetched exactly as the
  demo's Section-8 cell does): `edge_index` (the directed segment chain),
  `speeds` `[segments, time]` (your U3 per-segment speed series, 15-min bins),
  and `latlon` `[segments, 2]` for the folium map. Access details are in this
  unit's [`datasets.md`](./datasets.md).

The reference solution (`geoai-graph-unit5-solution.ipynb`) wraps the plumbing —
the windowing function that yields `(window, target)` tensors, the training loop,
the per-horizon evaluator — into reusable helpers.

> **Sanctioned vs. not.** Reusing the demo's named helpers and the
> `TGCNForecaster` class is **encouraged** — the plumbing is not the graded work.
> What is graded is the **decisions**: your adjacency choice, your input window
> and horizons, your zero-speed handling, and your interpretation of whether the
> GNN earned its complexity. What is **not** OK is copying the reference's
> *conclusions* (its adjacency verdict, its breakeven numbers) and presenting
> them as yours. Reuse the machinery; make the calls yourself; defend each in
> your log.

> **The `velocity == 0` trap (opposite of METR-LA!).** On METR-LA a **0 means
> MISSING** — so the demo's `masked_metrics` drops zeros. On the **bus corridor a
> 0 means STOPPED** (a red light, a stop dwell) — a **real, informative low
> speed**. If you blindly mask zeros you throw away exactly the congestion you
> are trying to forecast, and you feed a graph that then propagates that hole to
> neighbours. Decide explicitly how you treat stopped-vehicle bins and say why.

You are **not** given the prompts to type. Composing the right request, in this
unit's vocabulary, is half the exercise.

---

## The loop, made concrete

Everyone does the **baseline**. Then pick **at least one** extension (a/b/c);
strong students do two, and the honest-overkill extension (c) is worth as much
as a clean win. Keep a **decision-log entry per cycle** (copy
`decision-log-template.md`). In the in-class hour go deep on the **target
segment + its upstream neighbour**; the reference runs the whole corridor so you
can compare.

### Baseline — every student

1. **Load the bus corridor as a graph and CHOOSE its adjacency.** Fetch
   `bus_corridor_u5.npz`. Build the adjacency **directed** or **undirected** (see
   the graded decision above) and **write down why** in your log. Report the
   number of segment-nodes and edges, and draw the corridor on a folium map with
   nodes coloured by a mid-window speed.
2. **Decide your zero-speed / stopped-bin handling** (the `velocity==0` trap) and
   your window geometry: input window (how many past 15-min bins the GRU sees)
   and forecast horizons — **use the same 15/30/60-min horizons as your U3
   SARIMA result** so the comparison is apples-to-apples.
3. **Train a small T-GCN on the corridor.** Mirror the demo's loop (small hidden
   dim, MSE, Adam). The graph is tiny — a handful of epochs converges in seconds;
   watch the loss fall on the loss-curve helper. State the architecture in your
   prompt ("small T-GCN, hidden 16, N-step input window").
4. **Evaluate at 15/30/60 min with the same protocol as U3, against a floor.**
   Compute per-horizon error for the **target segment**, and put it next to
   **(i) a historical-average floor** on the same series and **(ii) your own U3
   SARIMA per-horizon numbers** for that segment. Plot all curves on one
   error-vs-horizon chart and mark the **breakeven horizon** (the last horizon
   where the model still beats the floor).

   > **No U3 SARIMA numbers of your own? (fallback).** If you are doing Unit 5
   > standalone, or didn't keep your U3 results, note that `bus_corridor_u5.npz`
   > bundles the segment **speeds**, not U3 forecasts. Two honest options: **(i)**
   > fit a quick SARIMA on the bundled corridor speeds for this segment as a
   > stand-in comparator, or **(ii)** drop the SARIMA line entirely and read the
   > breakeven against the **historical-average floor alone** — the floor is the
   > baseline that actually decides "did the GNN earn it," so this is still a
   > valid, honest breakeven read. Say which you chose in your log.
5. **Answer the capstone question, honestly.** Did the T-GCN push the breakeven
   **outward** vs your U3 SARIMA on this segment? Is the win **largest at the
   short horizons** where the upstream-neighbour signal arrives, shrinking as the
   horizon grows (the U3 caveat, now for a GNN)? Or did it barely move — because
   the graph is tiny and the series is dominated by its own daily pattern? Both
   are legitimate; defend yours from the numbers, not your gut.

### DIRECT / INTERPRET / EXTEND inside the baseline

- **DIRECT** — name every operation in unit vocabulary: *adjacency matrix
  (directed / undirected / symmetric-normalized), message passing, k-hop
  receptive field, node features, T-GCN = GCN + GRU, input window, forecast
  horizon, per-horizon MAE/RMSE, historical-average floor, breakeven horizon*.
  If your prompt reads the same to a non-specialist ("predict the bus speed with
  a graph network"), tighten it. And **name your adjacency choice explicitly** —
  the agent must not pick it for you.
- **INTERPRET** — when the agent returns a breakeven number or an error curve,
  restate it in transit terms: *how far ahead* the corridor is predictable, *where
  the floor wins*, and whether the GNN's win (or non-win) matches what you know
  about this road and about a ~10-node/17-day graph.
- **EXTEND** — your result should raise a new question. Follow it. The extensions
  below are structured leads, but a good question of your own counts.

---

## Extensions (pick at least one)

### (a) Attention on a real congestion event — *with the honesty guardrail*

Find a rush-hour window in your **test** period where speed drops on the corridor.
Train (or load) an **A3T-GCN** and read its **temporal attention** for the target
segment's forecast in that window: a bar of weight vs **past input step** —
"which past moments did the model lean on."

> **HARD guardrail (the unit's whole point).** A3T-GCN's attention is **temporal**
> — over time steps, **NOT** over neighbour nodes. It **cannot** tell you *which
> upstream segment* mattered. To answer "which upstream node?" you must supply a
> **separate spatial diagnostic on a separate axis**: U3's **lagged upstream →
> downstream cross-correlation** (corr vs lag; a peak at a positive lag is the
> spatial evidence). Show the two plots **side by side, never merged**, and state
> out loud: *a temporal-attention bar is not spatial causality.* Presenting the
> temporal heatmap as a "which node" answer is the exact mistake this unit exists
> to teach against. Frame the attention weight as an **interrogable hypothesis**,
> not a proof.

### (b) Interrogate the WORST-predicted segment — the antidote to attention over-trust

Rank your segments by test error and pick the **worst** one. Ask, in domain
terms: **what is the graph missing here?** Is this a segment with too few passes
(thin data)? A junction approach whose speed is signal-timing noise no neighbour
predicts? A dead-end node with only one graph neighbour, so message passing has
nothing to borrow? Name **what additional data or graph structure would help**
(a cross-street feed? a signal-phase feature? a richer adjacency?). This is the
negative case that guards against "pretty attention → over-trust."

### (c) Wrong-class — when is a GNN OVERENGINEERED here? *(a top answer, not a cop-out)*

You just trained a GNN on a **~10-node graph with ~17 days** of data. Articulate,
in domain terms, the conditions under which that is the **wrong tool**: when the
graph is too small for message passing to add signal; when each segment's series
is so dominated by its own **daily pattern** that a univariate SARIMA (or even the
historical-average floor) already captures it; when the spatial signal is real
but so weak that ten independent SARIMAs are cheaper and just as good. Use your
own breakeven comparison as evidence. Tie it to the field's own admission
(STAEformer: *diminishing returns from architectural complexity*). **An honest
"a GNN is overkill for this corridor, and here's the measured reason" is a
full-marks answer.**

---

## How the hour runs

| Time | What you do |
|---|---|
| 0:00–0:05 | Instructor restates the task + the rubric; you confirm your **adjacency choice**, your zero-speed handling, and your 15/30/60-min horizons. |
| 0:05–0:45 | Work the loop WITH the agent. Fill a decision-log entry per cycle. Go deep on the target segment + its upstream neighbour. |
| 0:45–0:55 | 2–3 students share a **surprising follow-up** (the GNN barely helped; attention leaned on only the last two steps; the directed graph flipped the result; a dead-end node was the worst). |
| 0:55–1:00 | Instructor synthesis. |

---

## What you hand in

- Your **decision log** (one entry per direct → interpret → extend cycle), with
  the end-of-session rubric check filled in. Your **directed-vs-undirected
  adjacency choice + reason** and your **zero-speed handling** are required
  entries.
- Your **breakeven comparison** (an error-vs-horizon plot: T-GCN vs the floor vs
  your U3 SARIMA, breakeven marked) and a **one-paragraph verdict** on whether
  the GNN earned its complexity on this corridor.
- The extension(s) you chose, captured in the log — including, if you did (a),
  the **two side-by-side axes** (temporal attention + spatial cross-correlation)
  with the honesty caveat stated.

You do **not** need a polished notebook for the in-class hour — the log + the
breakeven comparison + your maps are the deliverable. (The take-home
`homework.md` asks for a short writeup.)

---

## A note on prompting (example *structure*, not a script)

You compose your own prompts. As a shape to imitate — not copy — a good DIRECT
request names the object, the operation, and the inputs precisely:

> "Load the bus corridor as a graph from `bus_corridor_u5.npz` (nodes =
> segments, edges = adjacency, node features = per-segment 15-min speed). Build
> the adjacency **\<directed upstream→downstream / undirected symmetric-
> normalized\>** — I chose this because \<reason about one-way bus flow / GCN
> symmetry\>. Treat `velocity==0` bins as **\<stopped-real / dropped\>** because
> \<reason\>. Train a **small T-GCN (GCN + GRU, hidden 16)** with an
> **\<N\>-step input window**, MSE, Adam. Evaluate the **target segment** at
> **15/30/60 min** with masked MAE/RMSE, against a **historical-average floor**
> and my **U3 SARIMA** numbers, and mark the **breakeven horizon**."

Notice what it does *not* say: it doesn't say "predict the bus speed with a graph
net and see if it's good," and it doesn't let the agent pick the adjacency, the
horizons, or the zero-speed rule. The precision is the point. If your prompt is
vaguer than this, the agent will choose your adjacency for you — and you'll spend
INTERPRET time reverse-engineering its choices instead of owning them.

---

<sub>© Geospatial Graph Learning — rights reserved (not open-CC); see the course
`NOTICE.md`. This task was drafted with AI assistance and reviewed by the
instructor.</sub>
