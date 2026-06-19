# Unit 2 — Homework: From "Is My Map Good?" to "When Should I Trust It?"

**Solo and asynchronous. Budget 60–90 minutes.**
**Same data, same stack, a new question.** Builds directly on the supervised
practice task — if you haven't done that, do it first.

> In class you inferred a **whole-city** road graph from bus pings and **graded
> it once** against OSM (one cell size, one bandwidth, one threshold, one
> tolerance). The honest follow-up: **how much of your grade was the bus data,
> and how much was your own parameter choices?** An inferred map you can defend
> is one whose grade you understand — not one whose F1 you happened to maximize.

You will go one step deeper and less scaffolded than the in-class task. Use the
same stack from the demo (raster density via `scipy` `gaussian_filter` +
`skimage.skeletonize` + `networkx` + `folium`, plus `tslearn` if you pick
Track 2) — **no new heavy dependencies.** Grade on a **raster** basis (the
shapely buffer-union does not scale to the whole city).

---

## Your task

Pick **one** of the two tracks below. Both are open-ended; both must run the
direct → interpret → extend loop and produce a filled decision log plus a short
writeup.

### Track 1 — Map the sensitivity surface (extends baseline + extensions a/b)

A single F1 number hides how you got it. Make the dependence explicit:

1. **Sweep two knobs, not one.** Re-run the inference across a small **grid** of
   (bandwidth × density threshold) — say 3 bandwidths × 3 thresholds — and
   record precision, recall, and F1 for each. (Raster grading makes this cheap.)
   Present it as a **heatmap** (or a small table with a clear best cell). Where
   is the ridge of good F1, and is it a sharp peak or a broad plateau?
2. **Confidence-filter the best map.** Take your best (bandwidth, threshold)
   cell and apply the **per-edge distinct-vehicle confidence** filter from
   extension (a): drop edges supported by fewer than *k* vehicles, for two or
   three values of *k*. Report how precision, recall, and the inferred length
   move as *k* rises. At what *k* do you start deleting *real* roads (recall
   falls faster than precision rises)?
3. **Defend a single operating point.** Choose one (bandwidth, threshold, *k*)
   you would actually ship, and justify it for a specific use — e.g. "a
   conservative bus-corridor map a planner can trust" vs. "a high-recall draft
   for a human to clean up." The right point depends on the use; say which use
   you optimized for.

### Track 2 — Coverage is the ceiling (extends extensions b/c + the wrong-class question)

The map-inference literature's blunt rule is that **coverage — how many
distinct passes a road gets — caps recall.** You saw recall plateau around ~0.4
in class no matter the bandwidth; now show *why*. Test it on the city:

1. **Recall vs. coverage.** Bin OSM roads inside your corridor by how many
   distinct vehicles passed near them (0, 1, 2–3, 4+). Compute **recall within
   each bin.** Show that under-travelled roads are the ones you miss — and
   quantify it (a bar chart of recall vs. coverage bin).
2. **Aggregation hides things.** Find at least one road or movement that a
   **single matched trace** reveals but the **aggregate inferred map** erases
   (a one-off detour, a turn only one bus made). You may reuse the demo's
   matcher to match a couple of individual runs for contrast. Explain, in
   domain terms, *why* aggregation smoothed it away.
3. **Name the right tool.** Given (1) and (2), state precisely **when map
   inference is the wrong choice** and HMM matching against a reference network
   is right — and which later unit of this course (U3 outlier detection, U4
   time-varying edge weights) gives you the machinery to chase the signals
   aggregation hid.

---

## DIRECT / INTERPRET / EXTEND, on your own

You no longer have the instructor in the room, so the loop is entirely yours:

- **DIRECT** — prompts must use Unit 2 vocabulary (density estimation,
  bandwidth, density threshold, rasterize, skeletonization, junction detection,
  inferred graph, raster buffered precision/recall, corridor clip, coverage,
  distinct-vehicle support; DTW if Track 2's contrast). Vague prompts cost you
  INTERPRET time later.
- **INTERPRET** — the homework is graded partly on whether you *noticed* and
  *chased* a surprise. If your sweep produced a clean monotone story with no
  cliff and no plateau, look harder — or argue in writing that it didn't, and
  say why that itself is informative.
- **EXTEND** — your writeup must end on a question your results raised that you
  did **not** have time to answer. Name it precisely.

---

## Deliverables (push to your fork)

Push to `student-work/unit-2/` on your fork, then share the fork URL.

1. **Filled decision log** — one entry per direct → interpret → extend cycle
   (copy `decision-log-template.md`), with the end-of-session rubric check
   completed.
2. **A 300–500 word markdown writeup** that:
   - states the knobs / bins you swept and *why* (DIRECT + selection);
   - interprets your central result in **map-inference terms**, not just
     numbers — what your sensitivity surface or coverage curve *means*
     (INTERPRET);
   - names at least one thing that surprised you, or argues honestly that
     nothing did and what that means;
   - ends on the unanswered follow-up question your results raised (EXTEND).
3. *(Optional but encouraged)* your working notebook or a couple of the folium
   maps / the heatmap, so a reader can see what you saw.

---

## A warning worth heeding

The most common way to lose points here is to report an F1 as if it were a
property of *the bus data*, when it is really a property of **your parameter
choices on** the bus data. It is fine — expected, even — to pick a bandwidth
and report its F1. It is *not* fine to forget that a different defensible
bandwidth would have given a different number. The one sentence of honesty
about that — "this grade is conditional on bandwidth = X; the plateau around it
is what makes me trust it" — is what separates a good writeup from an excellent
one. And city-wide, the recall ceiling (~0.4) is the *data* talking, not your
pipeline — say so.
