# Unit 5 — Known Issues (Spatio-Temporal GNNs)

Per-unit install/runtime gotchas for `geoai-graph-unit5.ipynb` and the reference
solution. Format: **if you see X, do Y.** Unit 5 has the course's most fragile
install (PyG + PyG-Temporal), so if the notebook won't import, start here.

## Data shapes (the METR-LA snapshot convention — read before editing plots/models)

### The snapshot `x` is 3-D: `[nodes, features, periods]`
`METRLADatasetLoader.get_dataset(num_timesteps_in=12, ...)` yields snapshots whose
`x` is `[nodes, features=2, in_steps=12]` (feature 0 = speed, 1 = time-of-day) and
`y` is `[nodes, out_steps=12]`. Two consequences:
- **Reconstructing the `[nodes, T]` speed matrix:** use `s.x[:, 0, 0]` (speed,
  first in-step of each window), NOT `s.x[:, 0]` (which is `[nodes, 12]` and
  stacks to a spurious 3-D array — it breaks every plot and produces an
  out-of-range shock index → `IndexError` in the maps). See the cell "Speed matrix +
  ALL sensor coordinates."
- **T-GCN forward:** `TGCN` expects `[nodes, in_channels]` per call, so the
  forecaster must **loop the GRU over the 12 periods** (`x[:, :, step]`, threading
  `H`), not pass the whole 3-D `x` in one shot. `A3TGCN` is different — it *wants*
  the `[nodes, features, periods]` window directly.

### `IndexError` in `add_remaining_self_loops` during T-GCN training
Symptom: `model(x, edge_index, snap.edge_attr)` → deep in GCNConv's `gcn_norm`,
`loop_attr[...] = edge_attr[inv_mask]` → `IndexError: index N out of bounds for
dimension 0 with size 2`. On some PyG-Temporal builds the per-snapshot
`edge_attr` is **malformed** for `gcn_norm` (wrong length). **Do:** pass
`edge_weight=None` to T-GCN/A3T-GCN (the demo does) — the models run on the
**unweighted** graph (symmetric-degree normalization). Edge weights are only a
refinement; dropping them is version-robust and does not change the teaching point.

### Speed units: mph vs. normalized (z-score)
The loader z-scores speeds. The demo prefers raw mph if `loader.X` exposes it,
else de-normalizes via `loader.means`/`loader.stds` if present, else labels the
axis "normalized speed (z-score)" (`SPEED_UNIT`). The shockwave (relative drop) is
visible either way; only the axis label/units change.

### Sensor coordinates fetched at runtime
The network-over-map cells fetch `graph_sensor_locations.csv` from the DCRNN repo.
If that fetch fails, a **synthetic layout** is used (map still renders, but node
positions are not geographic). Colab has internet, so this normally succeeds.

## Setup / dependencies

### If the setup cell prints `WARN/404` for `requirements/unit-5.txt`
The unit-5 deps have not yet been published to this repo's `main`, so nothing
unit-specific installed and the smoke test fails at `import torch_geometric`.
**Do:** if you are on the upstream course repo, wait until the unit-5 dependency
publish lands on `main`; if you are on your own fork, sync from upstream. Until
`requirements/unit-5.txt` exists on `main`, the demo cannot install its stack on
Colab.

### If `import torch_geometric` or `import torch_geometric_temporal` fails after install
Almost always a **torch ↔ PyG ABI / version mismatch**. The setup **never pins
torch** (Colab ships its own; pinning forces a reinstall that desyncs the in-memory
copy). **Do:** (1) restart the runtime (Runtime → Restart) and re-run setup so PyG
installs against Colab's *current* torch; (2) confirm the setup is doing runtime
torch-version detection and **not** pinning torch; (3) if a fresh Colab torch bump
outran the PyG-Temporal release, fall back to PyG alone + a hand-rolled GCN+GRU.

### `ModuleNotFoundError: No module named 'torch_sparse'` on `import torch_geometric_temporal`
This is the **#1 Colab install failure**, and it bites at **import time**, not
just install time. Even though T-GCN / A3T-GCN never use them,
`torch-geometric-temporal`'s package `__init__` **eagerly imports** `torch_sparse` /
`torch_scatter` (via its EvolveGCN modules: `from torch_sparse import SparseTensor`).
So if those compiled extensions aren't present, **every**
`import torch_geometric_temporal` — including the smoke test — dies with:
```
File ".../torch_geometric_temporal/nn/recurrent/evolvegcno.py", line 7
    from torch_sparse import SparseTensor
ModuleNotFoundError: No module named 'torch_sparse'
```
And you can't just "install them": there is often **no prebuilt wheel** for Colab's
exact torch build, so `pip install torch_sparse` falls back to a **source compile
that hangs for many minutes** (the symptom that looks like the setup cell is stuck
on installing `torch-geometric-temporal`).

**The fix is automatic — you should not hit this on a fresh Colab.** The course
models run on PyG's **native scatter** over `edge_index`, so `torch_sparse` /
`torch_scatter` are only needed as *names* on the import path.
`setup_colab.py::_unit_5_setup()` installs **prebuilt wheels only**
(`--only-binary=:all:`, never compiling from source) and, if they are still not
importable, writes **lightweight stubs** so the import chain resolves
(`_ensure_scatter_sparse_importable` + a `--no-deps` temporal install +
`_verify_temporal_imports`). Nothing to do on a fresh Colab.

**If you are on an older `setup_colab.py`** and hit this: restart the runtime
(Runtime → Restart) and re-run the setup cell so the current helper runs. **Do
NOT** `pip install torch_scatter torch_sparse` without `--only-binary=:all:` on
Colab — that is what triggers the multi-minute hang. The few temporal models that
genuinely need the real extensions (EvolveGCN, etc.) are not used in this unit.

### If `import torch_geometric_temporal` fails on **Windows**
PyG-Temporal pulls `torch_geometric`, which has Windows wheels, but the geo/DL
stack is best supported on Linux. **Do:** use Python 3.11/3.12 (not a brand-new
pre-release); if a wheel is missing, run on **Colab** (the supported path) or in
WSL. Live-training on a Windows CPU is slow — set `USE_PRETRAINED = True`.

## Compute / GPU

### If there is no GPU (`device CPU` in the smoke-test banner)
Live-training T-GCN on CPU is slow and may blow the demo's time budget. **Do:**
the notebook runs fine CPU-only, but set `USE_PRETRAINED = True` in the Beat-3
build cell to **load `tgcn_metrla.pt`** instead of training live. A3T-GCN is
*always* loaded (never trained live), so it is unaffected. On Colab: Runtime →
Change runtime type → T4 GPU for the live-train experience.

### If live training runs long / hits an OOM or `RuntimeError`
The Beat-3 train cell **catches `RuntimeError`/`MemoryError` and falls back** to
the pre-trained `tgcn_metrla.pt` checkpoint automatically, printing a loud
`⚠ FALLING BACK` banner. **Do:** nothing — let it fall back; or pre-empt by
setting `USE_PRETRAINED = True`. Do not raise the epoch/hidden budget on a free
runtime.

### If the attention animation is slow to render or freezes Colab
`FuncAnimation().to_jshtml()` is the heaviest cell. It is capped at ~16 frames at
low fps and is marked **(OPTIONAL — trim if short on time)**. **Do:** if it
stalls, skip that cell — the stacked temporal-attention + cross-correlation panels
already make the honesty point. Do not raise the frame count on a free runtime.

## Data

### If `METRLADatasetLoader` fails to download METR-LA (network)
The bundled loader auto-downloads METR-LA on first use; a flaky upstream host can
break it. The Beat-1 load cell prints `⚠ FALLING BACK` and points at a cached
tensor mirror. The download is cached (to `/content` on Colab), so a successful
first run makes re-runs instant. If both the loader and the mirror fail, retry on a
fresh runtime.

### If a checkpoint or bus-graph fetch (`gdown`) fails
`fetch_with_fallback` tries **gdown (course Drive)** first, then an **HTTP mirror**
(release asset), printing exactly which path it took; if **both** fail it raises
one clean message. Files are cached (delete to force a re-download). Note: on the
upstream repo some hosted files may still be pending — see the status note in
[`datasets.md`](./datasets.md); until the real `bus_corridor_u5.npz` is hosted, the
practice/solution run on a self-contained **synthetic** corridor with the same
shape and keys, so your code does not change.

### Zeros mean different things on METR-LA vs the bus graph
On **METR-LA a `0` is a *missing* reading** — `masked_metrics` masks `speed <= 0`
before every MAE/RMSE/MAPE (MAPE explodes near zero). On the **bus corridor a `0`
is a real STOPPED bus** (a red light, a stop dwell) — the very congestion you are
forecasting, so the solution's `bus_metrics` **keeps** zeros. If you reuse the
demo's zero-masking blindly on the bus graph you delete real signal *and* feed a
hole the GNN then propagates to neighbours. Decide your stopped-bin handling
explicitly (it is a graded decision in the practice).

### The bus chain is directed; the T-GCN default is undirected
`edge_index` ships the **directed** upstream→downstream chain, but a
symmetric-normalized GCN wants an **undirected** adjacency. You must *choose* how to
wire it and justify it — building the symmetric version from the shipped chain is a
one-liner (`np.concatenate([e, e[::-1]], axis=1)`). This is a graded design
decision, not a bug.

## Honesty (Face c) — not a bug, a teaching invariant

### A3T-GCN attention is TEMPORAL, not spatial — never present it as causality
`A3TGCN._attention` is a **single global learned weighting over the 12 input time
steps** (`softmax(_attention)`), not per-sample and not over nodes. The notebook
keeps the **temporal** attention bar visually separate from the **spatial**
cross-correlation panel; the shockwave animation shows the shock moving while the
attention bar stays fixed. **Do not** merge them into one picture or label a
temporal heatmap as "which node" — that conflation is the Face-(c) error this unit
teaches against.

---

_Hit something not covered here? Note it in your decision log and, if you're on a
fork, open an issue — the instructor adds recurring problems to this file._
