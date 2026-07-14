# Unit 1 Writeup — Haifa Light-Rail Stress Test

## What I did

I built a simplified, ITM-projected (EPSG:2039) primal graph of the Haifa
Carmel area from the Geofabrik OpenStreetMap extract using pyrosm and OSMnx.
The graph covers the corridor from Haifa University to Stella Maris and
contains 4,928 nodes and 9,004 edges in its largest connected component (LCC).

To simulate converting surface streets to a light-rail corridor, I removed
two candidate route sets from the car-routable graph and computed
length-weighted betweenness centrality on the before and after graphs using
igraph (C-backed, faster than NetworkX for this graph size).

**Route 1** — Carmel ridge spine: Abba Hushi → Horev → Moria → HaNassi.
137 edges removed. After removal: 18 weakly connected components, 210 nodes
cut from the LCC.

**Route 2** — Lower Haifa / Hadar: Kheshbon → Hatzionut Ave → Herzliya →
Ha-Nevi'im → Herzl (Haifa only — a geographic filter on ITM northing was
needed to exclude the false match on Herzl Street in Tirat Carmel).
121 edges removed. After removal: 25 components, 36 nodes cut from the LCC.

## What I found

Route 1 is the more disruptive route. The decisive criterion is network
severance: removing the Carmel ridge spine cuts 210 intersections from the
main network entirely — those neighbourhoods lose all car-routable access,
not just a longer detour. By comparison, Route 2 disconnects only 36 nodes.

The betweenness spike from Route 1 (+0.046, concentrated on the Carmel
Tunnels) is smaller than Route 2's spike (+0.069, on Allenby / אלנבי).
But the tunnels are a toll road, so the structural prediction likely
overestimates how many drivers would actually use them — the real disruption
from Route 1 is probably worse than the betweenness number suggests.

## What surprised me

When Route 2 was removed, Allenby absorbed the most load — not a street I
would have predicted. Hatzionut Avenue (שדרות הציונות) was the highest-
betweenness street in the baseline (0.086, far above all others), so I
expected removing it to spread load broadly. Instead it concentrated
everything onto the nearest parallel corridor, Allenby. Removing the top
street does not spread load — it transfers it to the next available route.

## Limitations

Betweenness centrality is a structural prediction of through-traffic under
the assumption that every pair of nodes is equally likely to communicate.
It ignores real origin-destination demand, time of day, and road pricing.
The Carmel Tunnels result is the clearest example: topology says they absorb
the load; the toll says real drivers may not follow. Validating these
findings would require real traffic counts or an OD matrix — tools that
arrive later in the course (Unit 3: real flow and sensors).
