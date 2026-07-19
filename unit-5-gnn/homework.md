# Unit 5 — Homework (the course capstone end-game): Predict a Corridor Travel-Time at a Future Departure

> **Builds on the supervised task.** Same data (`bus_corridor_u5.npz`, your
> ~10-segment corridor), same trained T-GCN, a new question. Solo and
> asynchronous. Budget **60–90 minutes**. This is the **capstone deliverable for
> the whole course**: you have walked graph → trajectories → statistical baseline
> → dynamic routing → ST-GNN, and now you use the GNN to answer the operational
> question a rider actually asks — *"If I board at A at 5:30 pm, how long until I
> reach B?"*

## Why this question

In class you forecast **per-segment speed** and asked whether the GNN earned its
complexity. A rider does not care about one segment's speed — they care about
**how long the trip from A to B will take, at a specific future departure time**.
That travel-time is built from the model's **multi-step forecasts** rolled out
along the segments between A and B. This homework closes the loop from a
node-level forecast to a **route-level, time-dependent answer** — and asks you to
be honest about how much you should trust it.

## The task

1. **Pick two segment-nodes A (upstream) and B (downstream)** on your corridor and
   a **future departure time** inside your test window (e.g. a rush-hour bin).
2. **Roll out the T-GCN forecast** for the segments between A and B at that
   departure. For each segment on the path, take the model's forecast speed at the
   bin when the bus is expected to *reach* that segment (a simple time-dependent
   walk: arrive at segment *s*, read its forecast speed at the arrival bin,
   `crossing_time = segment_length / speed`, advance the clock, move to *s+1*).
   State your rule for empty/stopped bins (the `velocity==0` decision returns
   here).
3. **Report the predicted A→B travel-time** and compare it to two references:
   - a **naïve constant-speed** estimate (corridor length ÷ a single mean speed),
     and
   - the **actual** A→B travel-time in that test window (ground truth).
4. **Interrogate the answer.** Which segment's forecast dominates the travel-time
   (the slow junction segment)? Does using the GNN's **future** forecast (rather
   than current speed) change the estimate meaningfully at a **60-min-ahead**
   departure — i.e., did the spatial+temporal model buy you anything a snapshot
   wouldn't? Tie it back to your in-class **breakeven** finding: past the breakeven
   horizon, should the rider trust this number?

Keep it light — a defensible rollout and an honest interpretation beat a fancy
optimiser. You do **not** need to build a full RAPTOR/TDSP router; a
segment-by-segment time-dependent walk over your T-GCN forecasts is the intended
scope.

## Deliverables (push to your fork)

Push to `unit-5-gnn/student-work/` in your fork, then share the **fork URL**.

1. **A filled decision log** (`decision-log-template.md`) — your A/B choice,
   departure time, empty/stopped-bin rule, rollout rule, and the three
   travel-time numbers (GNN / naïve / actual).
2. **A 300–500-word markdown writeup** (`writeup.md`) that **interprets** your
   result in transit terms. It must answer:
   - What was your A, B, departure time, and rollout rule, and why?
   - What was the predicted A→B travel-time, and how did it compare to the naïve
     constant-speed estimate and the ground truth?
   - Which segment **dominated** the travel-time, and does that match your
     in-class worst-segment / breakeven finding?
   - Given your breakeven horizon, **how far ahead should a rider trust this
     number** — and did the GNN's future forecast earn its complexity over a
     current-speed snapshot for this trip?
   - One thing that surprised you and a follow-up question it raises.
3. (Optional) your notebook or a couple of figures (the rollout, the dominant
   segment).

## Grading

Applied against `rubric.md` (DIRECT / INTERPRET / EXTEND) with the unit-specific
notes your instructor keeps. The **writeup carries the INTERPRET weight** — a
travel-time number with a hand-wavy explanation scores below a messier rollout
with a precise, breakeven-grounded argument about how far ahead the forecast is
trustworthy.

> **Hint, not a spec:** the interesting result is usually that the GNN's future
> forecast barely differs from a current-speed snapshot for short trips (the
> daily pattern dominates), but *does* matter when your departure straddles the
> onset of a rush-hour slowdown that the upstream signal saw coming. Whether that
> happens on **your** corridor is exactly the "did the GNN earn it?" question —
> answer it from the numbers.

---

<sub>© Geospatial Graph Learning — rights reserved (not open-CC); see the course
`NOTICE.md`. This homework was drafted with AI assistance and reviewed by the
instructor.</sub>
