# Unit 4 — Homework: When Does the Bus Actually Win?

**Solo and asynchronous. Budget 60–90 minutes.**
**Same data, same stack, a new question.** Builds directly on the supervised
practice task — if you haven't done that, do it first.

> In class you computed a city-wide Cost of Anarchy at **8am** and read off a
> single fraction — "the bus wins X% of trips." The honest follow-up: **that
> fraction is half modeled-peak and half real geometry. Which half is which?**
> A CoA result you can defend is one whose drivers you understand — not one
> whose headline number you happened to report.

You will go one step deeper and less scaffolded than the in-class task. Use the
same stack from the demo (`tdsp_path` / `edge_time_at` / `tdsp_weight`, the
vendored `raptor`, `nearest_stop`, the footpath builder, `base_map`) — **no new
heavy dependencies.** Keep your O-D sample modest (60–100 pairs) and cache the
RAPTOR model so a re-run is cheap.

---

## Your task

Pick **one** of the two tracks below. Both are open-ended; both must run the
direct → interpret → extend loop and produce a filled decision log plus a short
writeup.

### Track 1 — The persistence surface (extends baseline + extension a)

A single 8am fraction hides *when* and *where* the advantage lives. Make the
dependence explicit:

1. **Sweep the clock.** Run your CoA sweep across **all three windows** (8am /
   11am / 5pm). For each window report the bus-wins fraction and the
   wrong-objective CoA distribution. Present it as a small table or a grouped
   bar chart by window.
2. **Decompose the driver.** Re-run the **8am** sweep **once with the modeled
   peak switched off** (i.e. route the car at free-flow / 11am-equivalent
   weights but keep the 8am schedule for transit). Compare bus-wins-with-peak
   vs. bus-wins-without-peak. **How much of the 8am bus advantage is the
   modeled peak, and how much survives at free-flow?** This is the load-bearing
   honesty experiment — name the split in a sentence.
3. **Map the persistent corridors.** Identify the O-D pairs (or origins) where
   the bus wins **at 11am too**, or where the wrong-objective CoA stays high
   off-peak. Map them. Propose a reason grounded in transit density or street
   geometry — *not* the peak (the peak is near-off at 11am).

### Track 2 — Reachability and the wrong-class boundary (extends extensions b + c)

The per-pair table answers "this trip." Reachability answers "this place," and
the wrong-class question answers "is shortest-path even the right tool here?"

1. **Two isochrones, three origins.** For **three** origins (one central, one
   peripheral, one near a transit hub), plot the 30-minute **car** isochrone
   (TDSP + convex hull, as in the demo) and the **transit** 30-minute
   reachability set at 8am. Quantify each by area or stop count.
2. **The competitiveness map.** Across your three origins, where is transit
   competitive (transit reach ≳ car reach) and where is it not? Tie the answer
   to *what each origin is near* (an arterial, a rail/BRT corridor, a low-density
   edge).
3. **Name the wrong-class cases.** From your reachability work, pick **two**
   concrete O-D pairs (or origins) where **shortest path is the wrong question**
   — destination-is-a-polygon, reliability-over-mean, parking-dominated, trip-
   chain, or multi-criteria — and state precisely what data or model class
   (e.g. McRAPTOR / Pareto routing, a reliability distribution, a parking model)
   you would need instead. Connect at least one to a later unit's machinery
   (U5's learned travel-time prediction).

---

## DIRECT / INTERPRET / EXTEND, on your own

You no longer have the instructor in the room, so the loop is entirely yours:

- **DIRECT** — prompts must use Unit-4 vocabulary (TDSP, `w(t)` / time-varying
  weight, peak multiplier (real-timed, modeled-in-space), admissible heuristic, RAPTOR / earliest
  arrival / round, GTFS, access/egress walk, isochrone / reachability polygon,
  Cost of Anarchy). Vague prompts cost you INTERPRET time later.
- **INTERPRET** — the homework is graded partly on whether you *noticed* and
  *chased* a surprise. If your three windows produced a clean monotone story
  with no flip and no persistent corridor, look harder — or argue in writing
  that they didn't, and say why that itself is informative. **The
  modeled-peak caveat must appear in your interpretation, not as a footnote.**
- **EXTEND** — your writeup must end on a question your results raised that you
  did **not** have time to answer. Name it precisely.

---

## Deliverables (push to your fork)

Push to `student-work/unit-4/` on your fork, then share the fork URL.

1. **Filled decision log** — one entry per direct → interpret → extend cycle
   (copy `decision-log-template.md`), with the end-of-session rubric check
   completed.
2. **A 300–500 word markdown writeup** that:
   - states the windows / origins / knobs you swept and *why* (DIRECT + selection);
   - interprets your central result in **routing terms**, not just numbers —
     what your persistence surface or competitiveness map *means* (INTERPRET);
   - **explicitly splits real-geometry advantage from modeled-peak artifact**
     (Track 1) or ties competitiveness to transit/road structure (Track 2);
   - names at least one thing that surprised you, or argues honestly that
     nothing did and what that means;
   - ends on the unanswered follow-up question your results raised (EXTEND).
3. *(Optional but encouraged)* your working notebook or a couple of the folium
   maps / the choropleth, so a reader can see what you saw.

---

## A warning worth heeding

The most common way to lose points here is to report a bus-wins fraction as if
it were a property of **Tel Aviv**, when it is partly a property of **the peak
model** you ran the car on. Read that model the way the deck does: its **hourly
timing is real** Tel Aviv data (Ayalon / TomTom), but **its spatial spread is
modeled** — so it is "synthetic" only as a *per-segment congestion measurement*,
not a measured per-segment field. It is fine — expected, even — to use the
modeled peak; the demo does. It is *not* fine to forget that a real per-segment
off-peak congestion measurement (which the GTFS feed did not contain) would have
given a different number. The one sentence of honesty about that — "the bus wins
35% at 8am, but ~all of that advantage evaporates at 11am because the peak is
**real-timed but modeled-in-space**; the corridors where it *persists* are the
real finding" — is what separates a good writeup from an excellent one.
