# Decision Log — Unit 3

---

## Segmentation design (pre-coding decision)

- **Corridor**: Allenby Street, Tel Aviv — the main commercial spine, chosen
  because it carries heavy multi-line bus traffic and its role in network load
  (Unit 1) is already understood.
- **Segmentation strategy**: Hybrid fixed-length with junction isolation and
  stop micro-chunks.
  - Base chunk: **150 m** fixed-length along the corridor centreline.
  - Near OSM junction nodes (degree ≥ 3): isolate with a short buffer so each
    chunk sits either before or after the intersection — not straddling it.
  - Near bus stops: cut into **~50 m** micro-chunks to resolve the dwell/speed
    discontinuity at stop approaches.
  - Junction locations detected via OSM drive graph (nodes of degree ≥ 3
    snapped to the corridor).
- **Why this cut**: Fixed chunks give uniform data density per segment (unlike
  per-OSM-edge, which can vary wildly). Junction isolation prevents mixing the
  free-flow speed of a mid-block with the deceleration pattern at an
  intersection. Stop micro-chunks separate dwell pings from through-traffic pings,
  making each segment's speed series physically homogeneous.

---

## Cycle 1

- **What I asked**: Segment the Allenby corridor (Rothschild → Ben Yehuda, ~1318 m N-S) into chunks so each chunk's speed series is physically homogeneous. I started with a hybrid design: 150 m base chunks + 50 m zones around OSM junctions + 50 m zones around OSM bus stops.
- **What the agent did**: Fetched junction nodes (degree ≥ 3 in the OSM "all" graph) and bus stop points from the Feb 2023 OSM snapshot, tried to cut the y-axis at each special point ± 25 m, then intersect each slab with the ±30 m ribbon.
- **What I understood from the result**: The first attempt gave 125 segments — far too many. Root cause: OSM tags every lane node, pedestrian crossing, and service entrance as a separate node, so "degree ≥ 3" found 73 nodes inside the ribbon, not 3. Similarly, 24 stop poles → OSM records both poles of each physical stop separately. Clustering nearby nodes (within 80 m) reduced this to 3 junction clusters and 6 stop clusters, giving 15 segments — better, but the map looked noisy and the segment types were not cleanly separated because the junction and stop zones still overlapped in several places.
- **Decision**: Dropped the junction/stop logic entirely and went with **uniform 150 m slabs**. Result: 9 segments, each a clean rectangular strip across the ribbon. The uniformity means each segment has roughly the same exposure to pings, making speed series directly comparable across segments.
- **Why this cut**: For a first forecast baseline, uniform chunks are more defensible than hand-tuned zones — the zone boundaries would need ground-truth validation to justify them, and the data quality doesn't support that yet. If a junction effect appears in the speed series, it will show up as a systematic speed drop inside whichever 150 m chunk contains the crossing.

---

## Cycle 2

- **What I asked**: Build a 30-min time series of mean speed per segment (9 segments, 16 days), then run walk-forward evaluation on the last 4 days comparing three models: HistoricAverage (grand mean), SeasonalNaive (repeat same time yesterday), and SARIMA(0,1,1)(0,1,1)[48] (daily seasonality).
- **What the agent did**: Binned 25,686 valid speed observations into 30-min slots, forward-filled gaps up to 1 hour, then ran cross-validation with horizon H=192 bins (4 days). Computed RMSE per segment per model.
- **What I understood from the result**: HistoricAverage won on every single segment. SeasonalNaive was often the worst — worse than even the flat mean. SARIMA collapsed on segments 4 and 5 (RMSE 9.85 and 14.75 km/h on a street averaging 12–13 km/h). This means the time series does not have a strong enough repeating structure for either model to exploit. Day-to-day variation at any given time slot is large enough that yesterday's value is misleading, and ARIMA fit the noise in training data rather than a real signal.
- **My next question / follow-up**: The breakeven floor is HistoricAverage. For SARIMA to win it would need consistent daily patterns — which would require external features (day of week, school calendar, real-time congestion) not just past speed. The diurnal plot showed that segments 3 and 8 behave oppositely at 14:00 — that opposite behaviour is real, but it's not stable enough across days for a model to learn from.

---

## End-of-session rubric check

- [x] DIRECT — specified corridor (Allenby, Rothschild → Ben Yehuda), segmentation strategy (150m uniform slabs), ribbon width (±30m), ping filter (30–120s, 1–80 km/h), forecast horizon (4 days), season length (48 bins/day)
- [x] INTERPRET — explained why southern segments are slower (Rothschild Blvd cross-traffic), why segs 7–8 have fewer pings (fewer lines reach the northern tip), and why HistoricAverage beats SARIMA (day-to-day variation is too large for repeating patterns to hold)
- [x] EXTEND — identified that segments 3 and 8 behave opposite at 14:00, and that beating HistoricAverage would require external features (day of week, events, congestion) not just past speed

## One thing that surprised me today

HistoricAverage — a flat line — beat SARIMA on every single segment. The most complex model was the worst on segments 4 and 5, with RMSE nearly as large as the mean speed itself. A street that clearly has a daily rhythm is still too noisy for a time-series model to exploit without external context.
