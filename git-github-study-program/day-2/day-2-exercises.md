# Day 2 exercises — publish and collaborate

**Time: about 60 minutes.** Uses your `cleankit` repo from Day 1 and your
GitHub account.

## Part A — Publish

1. Add a `.gitignore` for Python/Jupyter (lesson 9) and commit it.
2. Create an empty repository named `cleankit` on GitHub.
3. Add it as `origin` and push `main` with `-u`.
4. On GitHub, confirm all your Day 1 commits are visible, including the merge
   commits. Click on the conflict-resolution commit and read its diff.

## Part B — Work through a pull request

5. Open an **issue**: "Add `dedupe()` to remove duplicate values while
   preserving order."
6. Locally: pull, create branch `add-dedupe`, implement:

   ```python
   def dedupe(values):
       seen = set()
       out = []
       for v in values:
           if v not in seen:
               seen.add(v)
               out.append(v)
       return out
   ```

   Commit with a proper subject and a body that references the issue.
7. Push the branch and open a PR. Description: what, why, `Closes #1`.
8. On the *Files changed* tab, leave yourself a line comment asking for a
   docstring. Locally add the docstring, commit, push. See the PR update.
9. Merge the PR with *Squash and merge*. Delete the branch on GitHub. Confirm
   the issue closed itself.
10. Locally: `git switch main`, `git pull`, `git branch -d add-dedupe`,
    `git fetch --prune`. Look at `git log --oneline`: one squashed commit
    for the whole PR.

## Part C — Simulate a teammate and a conflict

11. Clone your repo a second time into `~/cleankit-teammate`.
12. In **both** clones, edit the first line of `README.md` to something
    different and commit (do not push yet).
13. Push from `cleankit-teammate`. Then try to push from `cleankit`. Read the
    rejection message.
14. In `cleankit`: `git pull`. Resolve the conflict, commit, push. Verify on
    GitHub that the README has your chosen line.
15. In `cleankit-teammate`: `git pull`. Both clones now agree.

## Part D — Notebooks

16. In `cleankit`, install `nbstripout` and run `nbstripout --install`.
    Commit the `.gitattributes` it created.
17. Create `notebooks/01-demo.ipynb` that imports `cleankit` and shows each
    function on a sample list. Run all cells. Commit and push.
18. On GitHub, open the notebook. It renders, but with no outputs: the
    stripping worked. (If outputs are there, run `git status`; the notebook
    was probably added before the install.)

## Part E — Version it

19. Update the README to document all functions (lesson 9 template).
20. Create `requirements.txt` (can be empty or contain `nbstripout`).
21. Commit, tag `v1.0` with an annotated tag, push the tag. On GitHub, create
    a Release from it with a sentence of notes.

## Part F — Contribute to someone else's repo (optional, 15 min)

22. Find a repo you like that has a typo in its README, or use
    https://github.com/firstcontributions/first-contributions which exists
    purely for this. Fork it, clone your fork, branch, fix, push, open a PR
    against the original. Watch what happens.

## Self-assessment

- [ ] I can put a local project on GitHub and get it back on another machine.
- [ ] I know what to do when a push is rejected.
- [ ] I can open, update and merge a pull request, and link it to an issue.
- [ ] I can resolve a conflict that comes from a pull.
- [ ] My notebooks commit without outputs and my data stays out of the repo.
- [ ] I can tag a version and find it again later.

Finish with the [self-check quiz](../self-check-quiz.md), then keep the
[cheat sheets](../cheatsheets/) somewhere you will find them.
