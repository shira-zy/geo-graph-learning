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
```

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

## 7. Verify everything works

Once Unit 1 is published, you'll be able to:

```bash
# From the repo root, open the demo notebook
cd unit-1-graph-substrate
jupyter notebook demo.ipynb
```

Run the **smoke-test cell** (always near the top of every demo notebook).
If it passes, your local env is good. If it fails, check the unit's
`KNOWN_ISSUES.md` first.

## Workflow during the course

### Where your work goes

Each unit's `student-work/` directory is yours to fill. It's empty in the
upstream repo, so your work won't conflict when you sync new lessons:

```
unit-1-graph-substrate/
├── theory.pdf          ← upstream-owned, READ-ONLY for you
├── demo.ipynb          ← upstream-owned
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

### Colab note

Every demo notebook has an "Open in Colab" badge at the top. Click it to
launch in your browser with zero local setup. Colab pre-installs PyTorch
with CUDA; for Unit 5 (GNNs) you'll want **Runtime → Change runtime type →
T4 GPU**.

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
