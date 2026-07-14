# Decision Log — Unit 1

Copy this template into your unit's `student-work/decision-log.md`. Add one
entry per direct → interpret → extend cycle during the supervised-practice
hour. Push to your fork before asking for async help — your reasoning matters
as much as your code.

---

## Cycle 1

- **What I asked** (in my own words): Build a simplified, EPSG:2039 (ITM) projected, LCC primal graph of the Haifa Carmel area, covering the Abba Hushi → Horev → Moria → HaNassi corridor from Haifa University to Stella Maris.
- **What the agent did**: Downloaded the Israel-Palestine Geofabrik extract, cut it to the Carmel bounding box with pyrosm, simplified + projected to ITM + took the largest connected component → 4,928 nodes, 9,004 edges. Plotted the primal graph.
- **What I understood from the result**: The Carmel network is corridor-dominated, not a grid. The terrain forces roads into a few east-west spines with steep connecting streets. The candidate route runs roughly through the middle of the network. My hypothesis: when this corridor is removed there are no good parallel alternatives, so load will spread across the entire remaining network rather than concentrating on one street.
- **My next question / follow-up**: Identify the edges belonging to Abba Hushi → Horev → Moria → HaNassi in the primal graph and remove them to build the "after" graph (the car-routable network with the rail route gone).

## Cycle 2

- **What I asked**: Find the edges in the primal graph corresponding to the route (Abba Hushi → Horev → Moria → HaNassi) and remove them to build the "after" graph. Keep the original node set — don't recompute on the new LCC.
- **What the agent did**: Matched edges by Hebrew OSM name (substring match for unique names; exact match for "שדרות הנשיא" to avoid false hit on "רבי יהודה הנשיא"). Removed 137 edges. Reported: 18 weakly connected components after removal, 210 nodes disconnected from the main cluster.
- **What I understood from the result**: The network broke into 18 pieces from just one corridor removal — strong confirmation of the "few dominant corridors" hypothesis. 210 intersections lose all car-routable access. Decision to keep original node set means those 210 nodes will show betweenness = 0 in the after graph; this is meaningful (they're isolated) but will dominate the "biggest drop" ranking — need to flag that when interpreting the comparison.
- **My next question / follow-up**: Compute length-weighted betweenness centrality on both G_before and G_after using igraph, then find which streets rose and fell most in ranking.

## Cycle 3

- **What I asked**: Compute length-weighted betweenness centrality on G_before and G_after using igraph (C-backed, fast). Show which streets gained and lost the most betweenness, and map the difference spatially. Dropped information centrality — O(n³), impractical on 4,928 nodes.
- **What the agent did**: Converted both graphs to igraph (collapsing parallel edges by minimum length), ran directed length-weighted betweenness, normalized, computed Δ = after − before. Mapped results: gold = removed route, blue = gained load, red = lost load.
- **What I understood from the result**: Load did NOT spread across the whole city as I hypothesised — it concentrated heavily on two streets: מנהרות הכרמל (Carmel Tunnels, the biggest gainer by far) and מגורשי ספרד. The tunnels run parallel and underground to the removed surface spine, making them the natural detour when the Carmel ridge corridor is gone. Streets adjacent to the removed route (פרויד, ראול ולנברג) lost betweenness because they fed into a corridor that no longer exists. My original hypothesis was partially wrong: the load concentrated rather than dispersed.
- **My next question / follow-up**: The Carmel Tunnels are a toll road — structurally they absorb the load, but will drivers actually use them? This is where topology-only analysis starts to mislead. What data would fix it?

## Cycle 4 — Extension (a): comparing two candidate rail routes

- **What I asked**: Compare Route 1 (Abba Hushi → Horev → Moria → HaNassi, Carmel ridge) against Route 2 (Kheshbon → Hatzionut Ave → Herzliya → Ha-Nevi'im → Herzl, lower Haifa/Hadar) across four structural criteria: load concentration, accessibility drop, number of high-centrality disruptions, and LCC fragmentation.
- **What the agent did**: Removed Route 2 edges with a geographic filter (ITM northing threshold) to exclude the false match on Herzl Street in Tirat Carmel. Ran igraph betweenness on G_after_2. Compared both routes: Route 1 — 137 edges removed, 18 components, 210 nodes cut from LCC, peak Δ-betweenness +0.046 (Carmel Tunnels). Route 2 — 121 edges removed, 25 components, 36 nodes cut from LCC, peak Δ-betweenness +0.069 (Allenby / אלנבי). Mapped both delta distributions.
- **What I understood from the result**: Route 1 is the more disruptive route. It disconnects 210 intersections from the main network — those neighborhoods lose all car-routable access, not just a longer detour. Route 2 disconnects only 36 nodes. Even though Route 2 removes a higher-betweenness street (Hatzionut Ave, which was the top-betweenness street in the baseline) and causes a larger peak load spike on Allenby (+0.069 vs +0.046), the decisive criterion is network severance: 210 vs 36 nodes cut off. The Carmel ridge spine is load-bearing for access to entire neighbourhoods; the lower-city route has parallel alternatives.
- **My next question / follow-up**: Betweenness is a structural prediction — it ignores demand and the fact that Carmel Tunnels are a toll road. What data (e.g. real traffic counts or OD matrices) would let me verify whether the structural severance actually translates to accessibility loss for real trips?

---

## End-of-session rubric check

- [x] DIRECT — phrased requests using unit vocabulary, specified inputs precisely
- [x] INTERPRET — explained results in own words, noticed surprises
- [x] EXTEND — at least one follow-up grounded in a result

## One thing that surprised me today

Allenby (אלנבי) absorbed the most traffic when Route 2 was removed — even though it was Hatzionut Ave (שדרות הציונות) that was the highest-betweenness street in the baseline. Removing the top street doesn't spread load evenly; it concentrates everything onto the next available parallel corridor, which turned out to be Allenby.
