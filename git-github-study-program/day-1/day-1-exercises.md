# Day 1 exercises — build a small project with a clean history

**Time: about 60 minutes.** Start a fresh repository; do not reuse
`weather-project`.

Work through the steps in order. After each step, run `git status` and
`git log --oneline` and make sure they show what you expect. Hints are at the
bottom; try without them first.

## The project: a tiny data-cleaning toolkit

### Step 1 — Initialise

Create a folder `cleankit`, make it a repository, and confirm you are on
branch `main`.

### Step 2 — First commit

Create `README.md` containing a title and one sentence. Commit it with the
message `Initial commit with README`.

### Step 3 — Add code

Create `cleankit.py`:

```python
def strip_whitespace(values):
    return [v.strip() for v in values]

def to_float(values):
    return [float(v) for v in values]
```

Commit as `Add whitespace and float helpers`.

### Step 4 — Two changes, two commits

Make **both** of these edits before committing anything:

* In `cleankit.py`, add a function `drop_empty(values)` returning only
  non-empty strings.
* In `README.md`, add a line listing the three functions.

Now create **two separate commits**: the first containing only the
`cleankit.py` change, the second containing only the README change. (You will
need `git add` with a specific filename, not `git add .`.)

Verify with `git show HEAD` and `git show HEAD~1` that each commit touches
exactly one file.

### Step 5 — A mistake, undone

Add a line `print("debug")` to `cleankit.py` and commit it with message
`oops`. Now remove that commit from history **without losing any other work**,
using a reset. Check `git log --oneline` no longer shows `oops` and
`cleankit.py` no longer has the debug line.

### Step 6 — A branch for a risky idea

Create a branch `robust-float`. Change `to_float` so it skips values that
cannot be converted:

```python
def to_float(values):
    out = []
    for v in values:
        try:
            out.append(float(v))
        except ValueError:
            pass
    return out
```

Commit on the branch. Switch back to `main` and confirm `cleankit.py` still
has the old version.

### Step 7 — Main moves on

On `main`, add a function `lowercase(values)` to `cleankit.py` (at the end of
the file) and commit. Draw, on paper, what `git log --oneline --graph --all`
will show. Then run it and compare.

### Step 8 — Merge

Merge `robust-float` into `main`. Was there a conflict? (There should not be,
since the two branches edited different parts of the file.) Delete the
branch.

### Step 9 — Create and resolve a conflict

Create branch `rename`. In it, rename `strip_whitespace` to `strip_ws` in
`cleankit.py` and commit. Back on `main`, rename the same function to
`trim` and commit. Merge `rename` into `main`, resolve the conflict by
keeping the name `trim`, and complete the merge.

### Step 10 — Time travel

Check out the commit from Step 3. Print `cleankit.py` and confirm only two
functions exist. Return to `main`.

### Step 11 — Stash

Start editing `README.md` but do not commit. Realise you need to switch to a
new branch `hotfix` to fix something urgent. Stash your edit, create the
branch, add a comment line to `cleankit.py`, commit, switch back to `main`,
merge `hotfix`, then pop your stash and commit the README edit.

### Step 12 — Review

Your final `git log --oneline --graph` should show roughly 10 commits, at
least two merge commits, and no `oops`. Read every message top to bottom: can
a stranger follow the story?

## Self-assessment

You are ready for Day 2 if you can do all of these without looking at notes:

- [ ] Explain the difference between working directory, staging area and
      repository.
- [ ] Make a commit containing only one of several modified files.
- [ ] Undo the last commit, keeping the changes.
- [ ] Create a branch, commit on it, merge it, delete it.
- [ ] Resolve a merge conflict.
- [ ] Use `git reflog` to find a commit you "lost".

## Hints

<details>
<summary>Step 4</summary>

```bash
git add cleankit.py
git commit -m "Add drop_empty helper"
git add README.md
git commit -m "List available functions in README"
```
</details>

<details>
<summary>Step 5</summary>

`git reset --hard HEAD~1` is fine here because the only thing in that commit
is the debug line you want gone. If you had other uncommitted edits you
wanted to keep, you would use `git reset --soft HEAD~1`, then
`git restore --staged cleankit.py`, then fix the file by hand.
</details>

<details>
<summary>Step 9</summary>

After `git merge rename` reports a conflict, open `cleankit.py`, find the
`<<<<<<<` block, keep the `def trim(values):` line, delete the markers and
the other version, then `git add cleankit.py && git commit`.
</details>

<details>
<summary>Step 11</summary>

```bash
git stash
git switch -c hotfix
# edit cleankit.py
git commit -am "Add explanatory comment"
git switch main
git merge hotfix
git branch -d hotfix
git stash pop
git commit -am "Expand README"
```
</details>

Next: [Lesson 6 — GitHub and remotes](../day-2/06-github-and-remotes.md)
