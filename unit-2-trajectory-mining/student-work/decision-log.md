# Decision Log — Unit 2

---

## Cycle 1

- **What I asked**: From 4.7M bus GPS pings over Tel Aviv (all lines, all vehicles, 16 days), estimate ping density over the city using a raster approach: project to EPSG:2039, bin into 30 m cells, and Gaussian-blur with a 75 m bandwidth. Show both the raw count and the blurred density on a folium dark basemap.
- **What the agent did**: Projected all pings to ITM (EPSG:2039), built a 30 m raster (~460 × 490 pixels covering ~13 × 14 km), counted pings per cell, then blurred with σ = 2.5 pixels (= 75 m). Displayed both layers as toggleable overlays on a CartoDB dark-matter map.
- **What I understood from the result**: The blurred density map clearly shows Tel Aviv's main bus corridors — multiple bright ridges aligned with major roads (Ayalon, Ibn Gabirol, Derech Begin, etc.). Some sections of Ayalon and Road 1 are missing: those are highway segments where buses don't drive, so there are no pings and no density ridge. The raw count map shows the same pattern but as a noisy spray of dots; the blur turns those dots into continuous ridges that look like roads. The dark basemap confirms that the ridges align with actual streets — the method is working.
- **My next question / follow-up**: The missing highway sections are a structural limit of the method (buses simply didn't drive there), not a parameter problem. When I grade against OSM later, I need to clip OSM to my inferred corridor first — otherwise those undriven highways will count as missed roads and collapse my recall unfairly. Next step: threshold the blurred density, skeletonize the mask into centrelines, and assemble a networkx graph.

---

## Cycle 2

- **What I asked**: Grade the inferred skeleton against OSM using raster-buffered precision/recall at 20 m tolerance. Clip OSM to the inferred corridor before measuring recall, so roads buses never entered (Ayalon, Road 1) don't penalise the score.
- **What the agent did**: Fetched the OSM drive graph for the TLV bbox (17,459 nodes, 33,719 edges), rasterized it onto the same 30 m lattice, dilated both rasters by 20 m (~1 pixel), clipped OSM to a wide dilation of the skeleton (the "corridor"), then computed precision = skeleton ∩ dilated-OSM / skeleton, recall = OSM-in-corridor ∩ dilated-skeleton / OSM-in-corridor.
- **What I understood from the result**:
  - Precision = 0.866: almost everything the skeleton drew is near a real OSM road — the algorithm is not inventing phantom roads.
  - Recall = 0.367: within the bus corridor, only 37% of OSM road pixels were close to the skeleton. The agreement map (red = false negatives) shows the missed roads are side streets, not main corridors.
  - F1 = 0.515.
  - The 80th-percentile threshold is the main driver of low recall: side streets with infrequent bus service produce density ridges too faint to survive the cutoff, so they are never skeletonized. The method effectively infers "roads buses use heavily," not "all roads."
- **My next question / follow-up**: Lowering the threshold (e.g. to 60th percentile) should recover more side streets and improve recall, at the cost of more fragments and possibly lower precision. The corridor coverage statistic (48.3% of OSM) also reflects this — only roads within reach of a bus route were ever candidates for recovery.

---

## Cycle 3

- **What I asked**: Test whether lowering the threshold to the 60th percentile recovers the missed side streets (reduces red FN pixels on the agreement map) at the cost of lower precision.
- **What the agent did**: Re-ran the full pipeline (threshold → skeletonize → grade) at the 60th percentile, reusing the fetched OSM raster. Produced a comparison table and a new agreement map.
- **What I understood from the result**:
  - Recall improved only slightly: 0.367 → 0.393. Red (FN) dots shrank on the agreement map — the lower threshold did recover some side streets.
  - Precision dropped: 0.866 → 0.796. Orange (FP) dots grew — faint density patches from GPS noise or sparse routes were included as phantom roads.
  - F1 improved marginally: 0.515 → 0.526.
  - The biggest change was connectivity: components fell from 99 → 22. The 80th-percentile threshold was cutting mid-road gaps on occasionally-serviced streets; at 60th percentile those gaps are bridged.
  - Total skeleton length nearly doubled (208.8 → 371.1 km) but recall barely moved — because the corridor denominator also grew (48.3% → 65.3% of OSM), and many newly added pixels are FPs rather than true side streets.
  - **Key insight**: the threshold controls connectivity more than coverage. Lowering it is most valuable when a well-connected graph matters more than precision; keeping it high is better when you want a clean, high-confidence network.
- **My next question / follow-up**: The F1 difference is small (0.011). The choice between thresholds depends on downstream use — navigation routing favours the 60th (fewer fragments), map cleaning favours the 80th (fewer phantom roads).

---

## End-of-session rubric check

- [x] DIRECT — phrased requests using unit vocabulary, specified inputs precisely
- [x] INTERPRET — explained results in own words, noticed surprises
- [x] EXTEND — at least one follow-up grounded in a result

## One thing that surprised me today

Road 1 is completely missing from the inferred network — not because of a parameter choice, but because buses never drive on it. The method is blind to any road the fleet didn't use, regardless of how important that road is. No pings → no density ridge → no skeleton, at any threshold.
