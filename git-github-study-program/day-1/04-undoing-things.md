# Lesson 4 — Undoing things

**Time: 40 minutes.**

The reason to use Git is that mistakes stop being scary. This lesson covers
every common "oops" in order of how often it happens. Practise each one in
your `weather-project` repo.

A rule that keeps you safe: **once something is committed, it is almost
impossible to lose it.** Most undo commands only touch things that are *not*
yet committed, and those are the only things at real risk.

## 1. "I edited a file and want to throw the edits away"

The file is modified but not staged. Discard the changes and get back the
last committed version:

```bash
git restore temps.py
```

**This is destructive.** The uncommitted edits are gone for good. Git warns
you in `git status` with the hint `(use "git restore <file>..." to discard
changes)`.

Try it: add a junk line to `temps.py`, run `git diff`, then `git restore
temps.py` and `git diff` again. Clean.

## 2. "I staged a file but did not mean to"

```bash
git restore --staged temps.py
```

The file goes back to "modified, not staged". Your edits are untouched; only
the box was unpacked.

## 3. "I committed with a typo in the message, or forgot a file"

If it is the **most recent** commit and you have **not pushed it anywhere**:

```bash
# fix the message only
git commit --amend -m "Better message"

# add a forgotten file to the last commit
git add forgotten.py
git commit --amend --no-edit
```

`--amend` replaces the last commit with a new one. Never amend a commit that
you have already pushed to GitHub and others may have; that rewrites history
they already have (lesson 6).

## 4. "I want to undo the last commit but keep my changes"

```bash
git reset --soft HEAD~1
```

`HEAD~1` means "one commit before HEAD". The commit disappears from history;
the changes it contained are back in the staging area, ready to re-commit
differently. Use this when you committed too early or bundled two things
together.

Variants, from gentle to brutal:

| Command | Commit removed? | Changes kept staged? | Changes kept on disk? |
|---------|-----------------|----------------------|------------------------|
| `git reset --soft HEAD~1` | yes | yes | yes |
| `git reset HEAD~1` (mixed, default) | yes | no | yes |
| `git reset --hard HEAD~1` | yes | no | **no, deleted** |

`--hard` is the only truly dangerous one. Before using it, make sure you
really want your working directory to look exactly like that older commit.

## 5. "That commit from last week was wrong, and it is already shared"

Do not reset; that rewrites shared history. Instead make a **new** commit that
does the opposite:

```bash
git revert 3f2a9c1
```

Git creates a commit titled `Revert "..."` that undoes the changes of
`3f2a9c1`. History stays intact, the bad change is cancelled. This is the
safe choice whenever the commit has left your machine.

## 6. "I want to see the project as it was at some older commit"

```bash
git log --oneline            # find the id
git checkout 3f2a9c1         # look around (read-only time travel)
git switch -                 # come back to where you were
```

While "checked out" at an old commit you are in **detached HEAD** state. Git
will print a scary-sounding message about it. It just means you are not on a
branch. Look, run the code, then `git switch main` to return. If you want to
build on that old point, create a branch there (lesson 5):
`git switch -c from-old-point`.

## 7. "I just want one old version of one file back"

```bash
git restore --source 3f2a9c1 temps.py
```

The file in your working directory becomes the version from that commit.
Commit it if you want to keep it.

## 8. "I need to switch tasks but I am in the middle of something"

Uncommitted work and a half-finished state. Shelve it:

```bash
git stash              # saves modified tracked files and cleans the directory
# ... do the other thing, switch branches, whatever ...
git stash pop          # bring the work back
```

`git stash list` shows what is stashed; `git stash -u` includes untracked
files too. Stashes are a temporary pocket, not a long-term archive; commit
properly when you can.

## 9. "I did something and now everything is broken, help"

Git keeps a diary of every place HEAD has pointed in the last ~90 days:

```bash
git reflog
```

```
a1b2c3d HEAD@{0}: reset: moving to HEAD~1
8b1e4d2 HEAD@{1}: commit: Correct last reading and print the maximum
3f2a9c1 HEAD@{2}: commit (initial): Add temperature conversion script
```

Find the entry from just before the disaster and go back to it:

```bash
git reset --hard 8b1e4d2
```

This recovers "lost" commits after a bad reset, a deleted branch, a bad
rebase. The only thing reflog cannot recover is work that was never committed
and was destroyed with `git restore` or `git reset --hard`.

## 10. Practice

Do each of these in `weather-project`:

1. Make an edit, discard it with `git restore`.
2. Stage a file, unstage it.
3. Commit, then amend the message.
4. Commit, then `git reset --soft HEAD~1`, then re-commit with a better
   message.
5. Revert your newest commit, then look at `git log --oneline`.
6. Check out your very first commit, `cat temps.py`, switch back to `main`.
7. Run `git reflog` and read the story it tells.

## Recap

| I want to… | Command |
|------------|---------|
| discard unstaged edits to a file | `git restore <file>` |
| unstage a file | `git restore --staged <file>` |
| fix the last commit (unpushed) | `git commit --amend` |
| undo last commit, keep changes | `git reset --soft HEAD~1` |
| undo last commit, drop changes | `git reset --hard HEAD~1` |
| cancel an old/shared commit safely | `git revert <id>` |
| look at an old commit | `git checkout <id>` then `git switch main` |
| get one old file back | `git restore --source <id> <file>` |
| park work temporarily | `git stash` / `git stash pop` |
| find anything I "lost" | `git reflog` |

Next: [Lesson 5 — Branches](05-branches.md)
