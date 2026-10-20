# Lesson 5 — Branches

**Time: 45 minutes.**

Branches are the feature that turns Git from "a better Save As" into a
collaboration tool. They are also cheap and instant, so use them freely.

## 1. What a branch really is

A branch is just a **name that points at a commit**. `main` points at your
latest commit. When you commit on `main`, the pointer moves forward.

Create a second name pointing at the same commit, commit on it, and the two
names diverge. That is all. No files are copied.

```bash
git branch              # list branches; * marks the current one
```

## 2. Create and switch

```bash
git switch -c add-plot        # create branch "add-plot" and switch to it
git branch                    # * add-plot
```

(`git switch -c` is the modern form. Older tutorials write
`git checkout -b add-plot`. Both work.)

Now add a plotting function to `temps.py`:

```python
def plot(temps):
    import matplotlib.pyplot as plt
    plt.plot(temps)
    plt.ylabel("°C")
    plt.show()
```

```bash
git commit -am "Add plot function"
git log --oneline
```

```
c4d5e6f (HEAD -> add-plot) Add plot function
8b1e4d2 (main) Correct last reading and print the maximum
...
```

`add-plot` is one commit ahead of `main`. Switch back and look:

```bash
git switch main
cat temps.py            # the plot function is gone!
```

Not gone, just not on this branch. Switch again and it is back. Git swaps the
files in your working directory to match the branch. Jupyter will show the
file change too if you have it open (reload the notebook if it asks).

## 3. Merge

When the work on a branch is finished, bring it into `main`:

```bash
git switch main              # go to the branch you want to merge INTO
git merge add-plot           # bring add-plot's commits in
```

```
Updating 8b1e4d2..c4d5e6f
Fast-forward
 temps.py | 6 ++++++
```

**Fast-forward** means `main` had nothing new, so Git simply moved the `main`
pointer forward to where `add-plot` was. No new commit was needed.

Delete the branch; its commits are now part of `main`:

```bash
git branch -d add-plot
```

## 4. Merge when both sides changed (merge commit)

Now simulate real life, where `main` moves on while you work on a branch.

```bash
git switch -c add-stats
```

Add to the end of `temps.py`:

```python
print(f"Mean: {sum(temps_c) / len(temps_c):.1f} C")
```

```bash
git commit -am "Print mean temperature"
git switch main
```

On `main`, edit `README.md` (add a line) and commit:

```bash
git commit -am "Expand README"
git log --oneline --graph --all
```

```
* 9f8e7d6 (HEAD -> main) Expand README
| * 1a2b3c4 (add-stats) Print mean temperature
|/
* c4d5e6f Add plot function
```

The branches have diverged. Merge:

```bash
git merge add-stats
```

Git opens your editor with a prepared message `Merge branch 'add-stats'`.
Save and close (in nano: Ctrl+O, Enter, Ctrl+X). Result: a **merge commit**
with two parents. The graph now shows the lines joining.

```bash
git branch -d add-stats
```

## 5. Merge conflicts (the thing everyone fears)

A conflict happens when both branches changed **the same lines** of the same
file. Git cannot guess which version you want, so it asks you. It is not an
error, it is a question.

Create one on purpose:

```bash
git switch -c celsius-label
```

Change the `plt.ylabel("°C")` line to `plt.ylabel("Temperature (°C)")`.

```bash
git commit -am "Clearer y label"
git switch main
```

On `main`, change the **same line** to `plt.ylabel("degrees C")` and commit:

```bash
git commit -am "Plain-text y label"
git merge celsius-label
```

```
Auto-merging temps.py
CONFLICT (content): Merge conflict in temps.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` says `both modified: temps.py`. Open the file:

```python
<<<<<<< HEAD
    plt.ylabel("degrees C")
=======
    plt.ylabel("Temperature (°C)")
>>>>>>> celsius-label
```

* Between `<<<<<<< HEAD` and `=======` is the version on your current branch.
* Between `=======` and `>>>>>>> celsius-label` is the incoming version.

To resolve: **edit the file so it contains exactly what you want** and delete
the three marker lines. For example keep just:

```python
    plt.ylabel("Temperature (°C)")
```

Then tell Git the conflict is settled:

```bash
git add temps.py
git commit                  # accept the prepared merge message
git branch -d celsius-label
```

Done. Three rules for conflicts:

1. Read `git status`; it lists every conflicted file.
2. In each file, search for `<<<<<<<`, decide, remove markers.
3. `git add` each fixed file, then `git commit`.

If you panic: `git merge --abort` returns everything to the state before you
started the merge.

VS Code, PyCharm and GitHub's web editor all show conflicts with
"Accept current / Accept incoming / Accept both" buttons, which does the same
thing with fewer keystrokes.

## 6. Everyday branch commands

| Command | Meaning |
|---------|---------|
| `git branch` | list local branches |
| `git switch -c name` | create and switch to a branch |
| `git switch name` | switch to an existing branch |
| `git switch -` | switch to the previous branch |
| `git merge name` | merge `name` into the current branch |
| `git branch -d name` | delete a merged branch |
| `git branch -D name` | force-delete an unmerged branch (its commits are abandoned) |
| `git branch -m newname` | rename the current branch |
| `git log --oneline --graph --all` | picture of all branches |
| `git merge --abort` | cancel a conflicted merge |

## 7. How people actually use branches

The near-universal convention, called **feature branching**:

* `main` always works. You never commit experiments directly to it.
* Every new piece of work gets its own short-lived branch:
  `fix-date-parsing`, `try-xgboost`, `add-tests`.
* When finished, merge into `main` (on GitHub, via a pull request, lesson 7)
  and delete the branch.

For a solo data-science project this still pays off: you can start a big
refactor on a branch, switch back to `main` to run yesterday's working
version for a meeting, and switch back to continue.

## 8. Practice

1. Create a branch `add-tests`, add a file `test_temps.py` with a trivial
   assert, commit, merge it into `main` (fast-forward), delete the branch.
2. Create two branches from `main` that each modify a different line of
   `README.md`. Merge both. No conflict expected; look at the graph.
3. Create two branches that modify the **same** line. Merge, resolve the
   conflict, commit.
4. Start a merge that conflicts and abort it with `git merge --abort`.

Next: [Day 1 exercises](day-1-exercises.md)
