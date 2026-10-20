# Jupyter + Git cheat sheet

## One-time setup per machine

```bash
pip install nbstripout nbdime jupyterlab-git
nbdime config-git --enable --global      # readable notebook diffs/merges everywhere
```

## One-time setup per repository

```bash
cd my-repo
nbstripout --install                     # strip outputs on commit
git add .gitattributes
git commit -m "Strip notebook outputs on commit"
```

Verify: `nbstripout --is-installed && echo yes`.

## Minimal `.gitignore` for a Python/Jupyter project

```
.ipynb_checkpoints/
__pycache__/
*.pyc
.venv/
venv/
.env
data/
*.csv
*.parquet
*.pkl
.DS_Store
.vscode/
.idea/
```

## Diffs and merges

```bash
git diff notebook.ipynb            # cell-based diff once nbdime is enabled
nbdiff notebook.ipynb              # explicit, terminal
nbdiff-web notebook.ipynb          # side-by-side in browser
nbdiff-web <id1> <id2> notebook.ipynb   # between two commits
nbmerge-web notebook.ipynb         # resolve a conflicted notebook visually
```

Take one side of a conflicted notebook without a tool:

```bash
git checkout --ours notebook.ipynb     # or --theirs
git add notebook.ipynb
```

## Rules of thumb

* **Outputs out, code in.** Commit code; regenerate outputs. If the outputs
  are the deliverable, export to HTML/PDF and commit that too.
* **Clear and restart before a "real" commit** if you are not using
  nbstripout: *Kernel → Restart Kernel and Clear All Outputs*.
* **Number notebooks**: `01-load.ipynb`, `02-clean.ipynb`. Order = story.
* **Move reusable functions to `.py` files** and import them. Add
  `%load_ext autoreload` and `%autoreload 2` in the first cell.
* **Data stays out of Git.** Keep `data/README.md` saying where it comes
  from, or a `download_data.py` script. For versioned large files look at
  Git LFS or DVC.
* **Secrets never go in notebooks.** Use `os.environ["API_KEY"]` with a
  `.env` file loaded by `python-dotenv`, and ignore `.env`.
* **Commit the environment**: `requirements.txt` or `environment.yml`.
* **Check before committing**: `git status`, then `git diff --staged --stat`.
  A notebook showing +50,000 lines means outputs slipped in.

## Reviewing notebooks on GitHub

* GitHub renders `.ipynb` files with outputs if present.
* In a PR's *Files changed* tab, click the `<>` / document toggle at the top
  right of a notebook to switch between raw JSON diff and **rich diff**.
* Large or output-heavy notebooks may show "Sorry, something went wrong";
  that is GitHub's renderer giving up, not a problem with your file.
  https://nbviewer.org renders any public notebook URL.

## Jupytext (optional)

Pair each notebook with a plain `.py` version and commit only the `.py`:

```bash
pip install jupytext
jupytext --set-formats ipynb,py:percent notebook.ipynb
```

Add `*.ipynb` to `.gitignore`. Jupyter keeps both files in sync on save; VS
Code opens `# %%` files as notebooks directly.

## Running Git from inside Jupyter

Terminal: *File → New → Terminal* in JupyterLab.

Shell commands in a cell: prefix with `!`, e.g. `!git status`,
`!git log --oneline -5`. Fine for looking; commit from a real terminal so
you see prompts and errors properly.

The `jupyterlab-git` extension adds a Git tab in the left sidebar with
stage/commit/push/pull buttons and a diff viewer.
