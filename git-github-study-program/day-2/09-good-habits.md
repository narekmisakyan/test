# Lesson 9 — Good habits

**Time: 30 minutes.**

Everything so far was mechanics. This lesson is about using them well, which
is what separates a repo people enjoy working in from one they dread.

## 1. Commit messages

A commit message has a **subject line** and an optional **body**, separated
by a blank line:

```
Fix off-by-one in rolling mean window

The window included the current row twice when `center=True`.
Added a regression test with a 3-row frame.

Closes #17
```

Rules that the whole industry agrees on:

* Subject ≤ 50 characters, capitalised, no trailing period.
* **Imperative mood**: "Add plot", "Fix bug", not "Added" or "Fixes". Test:
  the subject should complete the sentence *"If applied, this commit will
  ___"*.
* Body explains **why**, not what (the diff already shows what). Wrap at 72
  characters.
* One logical change per commit. "Fix typo and rewrite loader" is two commits.

For multi-line messages run `git commit` without `-m`; your editor opens.

Bad: `fix`, `wip`, `changes`, `asdf`, `final version`. You will search this
history one day; make the search worth it.

## 2. `.gitignore`

A file named `.gitignore` in the repo root lists patterns Git should never
track. Commit the `.gitignore` itself.

A solid starting point for a Python/Jupyter project:

```
# Jupyter
.ipynb_checkpoints/

# Python
__pycache__/
*.pyc
*.egg-info/
build/
dist/

# Environments
.venv/
venv/
env/
.conda/

# Secrets and local config
.env
*.key
config.local.*

# Data and outputs
data/
*.csv
*.parquet
*.pkl
*.h5
outputs/
*.log

# Editors and OS
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Patterns: `name/` ignores a folder anywhere, `*.csv` an extension, `/data`
only at the root, `!keep.csv` un-ignores. GitHub offers a full Python
template when you create a repo, and https://gitignore.io generates one for
any combination of tools.

If you already committed something before ignoring it:

```bash
git rm --cached data/big.csv     # stop tracking, keep the file on disk
git commit -m "Stop tracking data file"
```

It stays in old commits; truly purging history needs `git filter-repo`,
which is beyond this program. The lesson: add `.gitignore` as your **second
commit**, right after the README.

## 3. A README that answers the three questions

Every repo front page should tell a stranger:

1. **What** is this? One paragraph.
2. **How** do I run it? Install steps and one example command.
3. **Where** do I go next? Structure, contributing, license, contact.

```markdown
# cleankit

Small helpers for cleaning lists of strings before analysis.

## Install

    pip install -e .

## Usage

    from cleankit import to_float
    to_float(["1.5", " 2 ", "x"])   # [1.5, 2.0]

## Layout

- `cleankit.py` — the library
- `notebooks/` — exploration, numbered in order
- `tests/` — run with `pytest`
```

## 4. Repository layout for a data project

```
project/
├── README.md
├── .gitignore
├── requirements.txt      # or environment.yml / pyproject.toml
├── data/                 # ignored; put a README inside explaining how to get it
├── notebooks/
│   ├── 01-explore.ipynb
│   └── 02-model.ipynb
├── src/ or project_name/ # reusable .py code
└── tests/
```

Commit `requirements.txt` (`pip freeze > requirements.txt`) or
`environment.yml` (`conda env export --from-history > environment.yml`) so
others can rebuild your environment.

## 5. Tags and releases

A **tag** is a permanent name for one commit, used for versions:

```bash
git tag -a v1.0 -m "First working release"
git push origin v1.0            # tags are not pushed by default
git tag                         # list
git checkout v1.0               # look at that version
```

On GitHub, *Releases → Draft a new release* turns a tag into a page with
notes and downloadable archives. Tag the version you used for a paper or a
report so you can always reproduce it.

## 6. Small things experienced people do

* `git status` before every commit, `git diff --staged` before every
  commit of consequence. Read what you are about to commit.
* Commit early, commit often. A commit is free; a lost afternoon is not.
* Pull before starting; push before stopping.
* Branch names: short, lowercase, hyphenated, descriptive. `fix-nan-handling`
  not `stuff` or `branch2`.
* Never commit generated files you can regenerate (outputs, build artefacts,
  caches).
* Never commit credentials. If you did, rotate the credential immediately;
  removing it from history is not enough once pushed.
* Keep `main` working. Experiments go on branches.
* Write the README before you forget how the project works, which is sooner
  than you think.
* Make aliases for what you type most (lives in `~/.gitconfig`):

```bash
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.co switch
```

## 7. Licenses (for public repos)

Without a license file, others technically may not reuse your code even if
it is public. For most personal projects pick **MIT** (do what you want,
keep the notice). GitHub adds one via *Add file → Create new file → name it
`LICENSE`* and offers templates. https://choosealicense.com explains the
options.

Next: [Day 2 exercises](day-2-exercises.md)
