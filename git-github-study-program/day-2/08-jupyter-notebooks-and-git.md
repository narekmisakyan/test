# Lesson 8 — Jupyter notebooks and Git

**Time: 30 minutes.**

Notebooks work with Git, but they have two quirks you must know about or they
will drive you mad.

## 1. What an `.ipynb` file actually is

Open a notebook in a text editor. It is JSON:

```json
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [ { "data": { "image/png": "iVBORw0KGgoAAAANSUhEUgAA..." } } ],
   "source": [ "df.plot()\n" ]
  }
 ]
}
```

Your code is in there, but so are **execution counts**, **outputs** (including
every plot as a giant base64 string) and metadata. Consequences:

* **Diffs are unreadable.** Change one line of code, re-run, and `git diff`
  shows thousands of changed characters of image data.
* **Merges conflict constantly.** Two people re-run the same notebook, the
  execution counts and outputs differ, Git sees conflicting lines everywhere
  even when the code is identical.
* **Repos bloat.** Every committed output of a 2 MB plot stays in history
  forever.

## 2. Fix 1: do not commit outputs (recommended)

Install `nbstripout`, which strips outputs automatically every time Git
stages a notebook. Your notebook on disk keeps its outputs; only the committed
version is clean.

```bash
pip install nbstripout
cd ~/cleankit            # inside each repo, once
nbstripout --install
```

This writes to `.gitattributes` and `.git/config`. From now on
`git add notebook.ipynb` stores a version without outputs or execution
counts. Diffs become plain code diffs. Merges mostly just work.

Alternative without any tool: in Jupyter, *Kernel → Restart & Clear Output*
before every commit. It works but you will forget.

When you *do* want outputs preserved (a report where the plots are the
point), keep a separate exported copy: *File → Save and Export Notebook As →
HTML* and commit the HTML, or keep that notebook out of nbstripout with a
`.gitattributes` exception.

## 3. Fix 2: readable notebook diffs with `nbdime`

```bash
pip install nbdime
nbdime config-git --enable --global
```

Now `git diff` on a notebook shows cell-by-cell changes, and
`nbdiff-web notebook.ipynb` opens a side-by-side viewer in the browser.
`nbdime` also provides a merge tool (`nbmerge-web`) for the conflicts that do
happen.

GitHub itself renders notebooks nicely and, in PRs, shows a *rich diff* for
`.ipynb` files (the toggle at the top right of the file in *Files changed*).

## 4. Fix 3: ignore the junk Jupyter creates

Jupyter writes `.ipynb_checkpoints/` folders next to every notebook. They
must never be committed. Lesson 9 covers `.gitignore` properly; the lines you
need are:

```
.ipynb_checkpoints/
__pycache__/
*.pyc
.venv/
```

## 5. A workflow that keeps notebooks and code sane

The pattern most data teams converge on:

1. **Explore in notebooks.** Name them with a number prefix so they sort:
   `01-load-data.ipynb`, `02-clean.ipynb`, `03-model.ipynb`.
2. **Move stable code out into `.py` modules** as soon as a function is used
   in more than one place. Notebooks then `from cleankit import to_float`.
   Python files diff and merge perfectly; notebooks stay short.
   Add `%load_ext autoreload` / `%autoreload 2` at the top of a notebook so
   edits to the module are picked up without restarting the kernel.
3. **Commit at natural checkpoints**: "loader works", "baseline model
   trained". Not every cell execution.
4. **Do not commit data.** Data is big, changes differently from code and
   may be private. Put it in `data/` and add `data/` to `.gitignore`. Commit
   a small sample or a script that downloads it. (For tracking large files
   with Git, look up *Git LFS* or *DVC* later.)
5. **Do not commit secrets.** API keys go in a `.env` file or environment
   variables, and `.env` goes in `.gitignore`. A key pushed to a public repo
   is compromised within minutes; bots scan for them.

## 6. Jupytext: notebooks as plain text (optional, advanced)

[Jupytext](https://jupytext.readthedocs.io) pairs each `.ipynb` with a `.py`
file containing the same cells as a script with `# %%` markers. You commit the
`.py`, ignore the `.ipynb`, and Jupyter keeps both in sync. VS Code and
PyCharm open `# %%` files as notebooks directly. Worth adopting once you are
comfortable with everything else in this program.

## 7. Git inside JupyterLab

The `jupyterlab-git` extension (`pip install jupyterlab-git`) adds a Git
sidebar to JupyterLab: stage, commit, push, pull, branch, all with buttons,
and a diff viewer. It is a fine way to run the daily loop once you understand
what the buttons do.

## Practice

1. In `cleankit`, create `01-demo.ipynb` with two cells that import and use
   your functions, run it, commit it. Look at `git show --stat HEAD` and the
   diff. Note the noise.
2. Install `nbstripout`, run `nbstripout --install`, re-run the notebook,
   commit again. Look at the diff: only metadata changed, no outputs.
3. Add a `.gitignore` with the four lines above and commit it. Confirm
   `.ipynb_checkpoints/` no longer appears in `git status`.

Next: [Lesson 9 — Good habits](09-good-habits.md)
