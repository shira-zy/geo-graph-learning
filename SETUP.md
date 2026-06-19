# Course Setup

Complete this before week 1 of the course. Allow ~30 minutes.

## Prerequisites

- A GitHub account.
- Comfort with the command line (Terminal on macOS, PowerShell or WSL on Windows).
- Python 3.11+ (we'll install via `uv` if you don't have it).

## Two ways to run (choose consciously)

Every demo + solution notebook runs both ways. Decide which you'll use:

| | Local with `uv` (recommended) | Colab (one click) |
|---|---|---|
| **Setup** | `uv sync --extra unit-<N>` (this guide) | none — first cell runs `setup_colab.py` |
| **Where** | your machine (macOS / Windows) | browser, free GPU/CPU runtime |
| **Best for** | repeat work, your own data, offline | a quick look, no local install |

Local gives you a persistent environment and your own files; Colab is
zero-install but resets each session. The same notebook code runs in both —
only the first setup cell differs. The rest of this guide sets up the **local**
path; for Colab just open the notebook's "Open in Colab" badge.

## 1. Fork this repo

Click **Fork** at the top right of
[github.com/bgalon/geo-graph-learning](https://github.com/bgalon/geo-graph-learning).
This creates `<your-username>/geo-graph-learning`.

### Privacy alternative (optional)

If you'd prefer your work not be publicly visible:

- Create a new **private** repo on your account.
- Clone it locally and add this repo as the upstream remote (see step 3).
- Functionally identical, just not labelled "fork" on GitHub's UI.

If you don't want any remote at all, you can just clone this repo directly —
but then you give up the ability to share your work when asking for async
help.

## 2. Clone your fork

```bash
# Replace <your-username> with your GitHub username
git clone https://github.com/<your-username>/geo-graph-learning.git
cd geo-graph-learning
```

## 3. Add the upstream remote

So you can pull new lessons as they're published.

```bash
git remote add upstream https://github.com/bgalon/geo-graph-learning.git
git remote -v   # confirms 'origin' is your fork, 'upstream' is the source
```

To sync a new lesson later:

```bash
git fetch upstream
git merge upstream/main
git push origin main   # update your fork
```

You can also pin to a specific tagged release:

```bash
git fetch upstream --tags
git checkout v-unit1    # stable snapshot
```

## 4. Install `uv`

`uv` is a fast Python package manager. Pick your platform:

### macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# OR if you use Homebrew:
brew install uv
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify: `uv --version`.

## 5. Install the course dependencies

From the repo root:

```bash
# Install everything for all units (a few hundred MB):
uv sync --extra all

# OR install only what you need for one unit:
uv sync --extra unit-1
uv sync --extra unit-2   # Trajectory Mining
```

> **Available units.** Each published unit lives in its own folder with a
> rendered theory deck (`theory.pdf` / `theory.html`), a Colab-first demo
> notebook, and a reference solution:
> - **Unit 1 — Graph Substrate:** `unit-1-graph-substrate/geoai-graph-unit1.ipynb` (`--extra unit-1`)
> - **Unit 2 — Trajectory Mining:** `unit-2-trajectory-mining/geoai-graph-unit2.ipynb` (`--extra unit-2`)
>
> Install the extra that matches the unit you're opening (the examples below use
> Unit 1; swap `unit-1` → `unit-2` to open the Trajectory Mining notebook).

`uv` creates a `.venv/` automatically. Activate it if you want:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

## 6. Install Claude Code

You'll use Claude Code for the supervised-practice hour each week.

```bash
# Requires Node.js 18+
npm install -g @anthropic-ai/claude-code
```

Then authenticate:

```bash
claude
# Follow the auth prompts
```

If you don't have Node.js, install it from [nodejs.org](https://nodejs.org/) first.

## 7. Open a notebook locally (with the right kernel)

The #1 local gotcha is opening a notebook with the **wrong Python** — a system
Jupyter that can't see the libraries `uv` just installed, so imports fail even
though `uv sync` succeeded. Avoid it entirely by launching Jupyter **from inside
the `uv` environment**. Then the running env *is* the kernel — there's nothing to
select.

```bash
# From the repo root. The --extra must match the unit you're opening.
uv run --extra unit-1 jupyter lab
```

This works **identically on macOS and Windows** (PowerShell): `uv run` resolves
the environment, so you never activate a venv or pick a kernel by hand. Jupyter
Lab opens in your browser; navigate to the notebook (e.g.
`unit-1-graph-substrate/geoai-graph-unit1.ipynb`) and open it. The kernel in the
top-right will be the project's Python — exactly the env you synced.

> Prefer classic Notebook or an editor with its own Jupyter (e.g. VS Code)?
> Register the env as a named kernel once, then pick it from the kernel list:
> ```bash
> uv run --extra unit-1 python -m ipykernel install --user \
>   --name geo-graph --display-name "Geo-Graph (uv)"
> ```
> Re-run with a different `--extra` only matters at install time; one kernel
> serves every unit you've synced into the same `.venv`.

Run the **smoke-test cell** (always near the top of every demo notebook).
If it passes, your local env is good. If it fails:

- Confirm the kernel (top-right in Jupyter) is the project Python, not a global
  one. If you launched with `uv run … jupyter lab`, it already is.
- Check the unit's `KNOWN_ISSUES.md` for platform-specific library notes.

## 8. Let the agent set up and tutor you (recommended)

This repo ships two Claude Code **skills** so you can drive everything by talking.

### One-time setup, done for you

In Claude Code, from the repo root, just say:

> **make full setup**  *(or type `/setup`)*

The agent (the `course-setup` skill) will, with your confirmation: `uv sync` the
unit's deps, register the `geo-graph` kernel, run a headless smoke test, and — if
you want it — install and **test** the live notebook bridge described next. It
asks whether you're local or on Colab and adapts.

### The supervised-practice hour

When it's time to practice, say:

> **let's work on the practice of unit 1**  *(or type `/practice`)*

The agent (the `practice-tutor` skill) states the task and dataset, then coaches
you through the **direct → interpret → extend** loop. Importantly: **the agent
writes and runs the notebook cells; you direct it (in domain vocabulary) and
interpret the results.** That division is the point of the course — you learn to
*command* an analysis and *read* it, not to type it.

### The live agent↔notebook bridge (local only)

So the agent can write and run cells while you watch, this repo uses the
[Jupyter MCP server](https://github.com/datalayer/jupyter-mcp-server). You'll have
**two windows**: the **terminal** (Claude Code — you talk to the agent) and your
**browser** at `localhost:8888` (JupyterLab — cells appear and run live there).

What the bridge needs (the setup skill does all of this for you):

- The `local` dependency extra: `uv sync --extra unit-1 --extra local` — this
  adds JupyterLab + the real-time-collaboration extension that lets you and the
  agent edit the same notebook with **no save conflicts** (changes merge and
  autosave; no "file changed on disk" prompts).
- A token in your environment. `scripts/start_lab.py` generates one, writes it to
  a gitignored `.env.local`, and launches JupyterLab. Load it into the shell that
  runs Claude Code:
  ```bash
  set -a; source .env.local; set +a     # macOS / Linux
  ```
- The committed `.mcp.json` wires Claude Code to the server (the token comes from
  your environment — nothing secret is committed). **After first setup, restart
  Claude Code** so it loads `.mcp.json`, and **approve** the `jupyter` server when
  prompted. The setup skill then runs a test cell to confirm the bridge works.

If a bug bites (e.g. a duplicate cell, a stuck save), see
`unit-1-graph-substrate/KNOWN_ISSUES.md` → "Agent notebook bridge".

### On Colab there's no bridge

Claude Code can't drive Colab. There the practice tutor coaches by chat — it
hands you cells to paste and run, and you tell it what you saw. Same loop, same
rubric.

## Workflow during the course

### Where your work goes

Each unit's `student-work/` directory is yours to fill. It's empty in the
upstream repo, so your work won't conflict when you sync new lessons:

```
unit-1-graph-substrate/
├── theory.pdf              ← upstream-owned, READ-ONLY for you
├── geoai-graph-unit1.ipynb ← upstream-owned
├── homework.md         ← upstream-owned
└── student-work/       ← YOUR space
    ├── README.md
    ├── my-notebook.ipynb
    ├── decision-log.md
    └── ...
```

### Per-week checklist

1. **Sync** the new lesson: `git fetch upstream && git merge upstream/main`.
2. Read the theory deck.
3. Run the demo notebook in Colab (link in the notebook header) or locally.
4. During class, do the supervised-practice task in `student-work/` while
   filling `decision-log.md`.
5. After class, do the homework. Push to your fork.

### Asking for async help

If you get stuck:

1. Push your work to your fork (even broken code is useful context).
2. Share your fork URL with the instructor.
3. Include your decision log — it shows what you were trying to do, which
   helps far more than a code snippet alone.

### Running on Colab (and connecting it to GitHub)

Colab is the zero-install path: open a notebook in your browser, the first cell
runs `setup_colab.py`, and you're going. Two ways in — pick based on whether you
want to **keep your edits**.

**A. Just look / run the upstream notebook (read-only).**
Click the **"Open in Colab"** badge at the top of any demo notebook. This opens
the *course* copy. Edits are **not saved** unless you do `File → Save a copy in
Drive`. Fine for a quick run; not where your graded work should live.

**B. Open a notebook from your own fork (edits go back to GitHub).**
This is the one to set up, so your practice/homework notebooks live in your repo.

1. **Authorize Colab once.** In Colab: `File → Open notebook → GitHub` tab. Click
   the prompt to **authorize** Google Colab to access GitHub. If you took the
   **private-repo** route (SETUP step 1), also tick **"Include private repos"**
   when GitHub asks.
2. **Open your notebook.** In that same `GitHub` tab, type your
   `<your-username>/geo-graph-learning`, choose the branch (`main`), and pick the
   notebook. Or just edit the URL directly:

   ```
   https://colab.research.google.com/github/<your-username>/geo-graph-learning/blob/main/unit-1-graph-substrate/geoai-graph-unit1.ipynb
   ```

3. **Save your changes back to GitHub.** `File → Save a copy in GitHub`. Pick your
   fork + branch, write a commit message, save. The notebook is now committed to
   your repo — `git pull` to bring it down locally, or just keep working in Colab.

> Tip: do your real work in the unit's `student-work/` folder (copy the demo
> there first, or save your own notebook into it) so syncing new upstream lessons
> never conflicts with your edits.

**GPU runtimes.** Colab pre-installs PyTorch with CUDA; for Unit 5 (GNNs) switch
to a GPU with **Runtime → Change runtime type → T4 GPU**.

## Troubleshooting

### `uv sync` fails

Run `uv sync --extra unit-1 --verbose` and check the error. The most common
issues are platform-specific wheels for geospatial libraries — check the
unit's `KNOWN_ISSUES.md` for known workarounds.

### A notebook won't import a library

Check the unit's `KNOWN_ISSUES.md` first. If the notebook works on Colab
but not locally, that's likely a platform-specific library issue — open an
issue on the upstream repo.

### "I haven't pushed anything but want help"

Push first. Even an empty repo with a `decision-log.md` saying
*"I'm stuck on step 2"* gives the instructor something concrete to respond to.
