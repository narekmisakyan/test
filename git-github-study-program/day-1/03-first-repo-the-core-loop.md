# Lesson 3 — Your first repo: the core loop

**Time: 45 minutes. Type everything.**

By the end of this lesson you will know the five commands that make up 90% of
daily Git use: `status`, `add`, `commit`, `log`, `diff`.

## 1. Create a repository

```bash
cd ~                      # go to your home folder
mkdir weather-project
cd weather-project
git init
```

Output: `Initialized empty Git repository in /Users/you/weather-project/.git/`

Run `ls -a`. You see the hidden `.git` folder. Your folder now has a memory.

## 2. The most important command: `git status`

```bash
git status
```

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`git status` tells you where you are and what Git is waiting for. **When in
doubt, run `git status`.** It never changes anything; it only reports.

## 3. Create a file

Make a file called `temps.py` with this content (use Jupyter, VS Code, or
`nano temps.py`):

```python
temps_c = [21.5, 23.0, 19.8, 25.1]

def to_fahrenheit(c):
    return c * 9 / 5 + 32

print([to_fahrenheit(t) for t in temps_c])
```

Now:

```bash
git status
```

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        temps.py
```

**Untracked** means: Git sees the file but has never been told to remember it.

## 4. The two-step save: `add` then `commit`

This is the part that confuses everyone at first, so read slowly.

Saving in Git is two steps:

1. `git add` — choose **which changes** go into the next snapshot. This puts
   them in the **staging area** (also called the *index*).
2. `git commit` — take the snapshot of everything staged, with a message.

Why two steps? Because you often edit five files but want to make two
separate commits ("fix bug in loader" and "add plot"). Staging lets you pick.

Think of it as packing a box: `add` puts items in the box, `commit` seals it
and writes the label.

```bash
git add temps.py
git status
```

```
Changes to be committed:
        new file:   temps.py
```

The file is staged. Now seal the box:

```bash
git commit -m "Add temperature conversion script"
```

```
[main (root-commit) 3f2a9c1] Add temperature conversion script
 1 file changed, 5 insertions(+)
 create mode 100644 temps.py
```

`3f2a9c1` is the start of the commit's ID (a 40-character hash). You will
usually refer to commits by their first 7 characters.

`git status` now says `nothing to commit, working tree clean`. Everything on
disk matches the latest snapshot.

## 5. The three places a file can be

Every file lives in up to three places at once. This picture is worth
memorising:

```
   Working directory          Staging area              Repository
   (your files on disk)       (the box being packed)    (sealed snapshots)

        edit file  ──git add──▶  staged  ──git commit──▶  committed
                 ◀──git restore──        ◀──git restore --staged──
```

* **Working directory**: what you see in your editor.
* **Staging area**: what will go into the next commit.
* **Repository**: the permanent history in `.git`.

`git status` shows you the difference between all three.

## 6. Make a change and see it: `git diff`

Edit `temps.py`: change `25.1` to `26.4` and add a line at the end:

```python
print(f"Max: {max(temps_c)} C")
```

```bash
git status      # says: modified: temps.py
git diff        # shows exactly what changed, line by line
```

```diff
-temps_c = [21.5, 23.0, 19.8, 25.1]
+temps_c = [21.5, 23.0, 19.8, 26.4]
 ...
+print(f"Max: {max(temps_c)} C")
```

Lines starting with `-` were removed, `+` were added. This answers "what did I
change since my last save?", a question you could never answer with
`analysis_v2_fixed.ipynb`.

`git diff` compares working directory to staging area. After you `git add`,
plain `git diff` shows nothing; use `git diff --staged` to see what is about
to be committed.

## 7. Commit the change

```bash
git add temps.py
git commit -m "Correct last reading and print the maximum"
```

Shortcut: `git commit -am "message"` stages **all modified tracked files**
and commits in one go. It does not pick up new (untracked) files; those still
need `git add`.

## 8. Look at the history: `git log`

```bash
git log
```

```
commit 8b1e4d2... (HEAD -> main)
Author: Your Name <you@example.com>
Date:   ...

    Correct last reading and print the maximum

commit 3f2a9c1...
Author: ...

    Add temperature conversion script
```

The compact version you will actually use every day:

```bash
git log --oneline
```

```
8b1e4d2 (HEAD -> main) Correct last reading and print the maximum
3f2a9c1 Add temperature conversion script
```

`HEAD` means "the commit you are currently standing on". `HEAD -> main` means
HEAD is at the tip of the `main` branch.

To see what a specific commit changed:

```bash
git show 3f2a9c1
```

## 9. Adding several files at once

Create two more files: `README.md` (one line of description) and `notes.txt`.

```bash
git add .            # stage everything new or modified in the current folder
git status
git commit -m "Add README and notes"
```

`git add .` is convenient but dangerous if your folder contains things you do
not want tracked (data files, secrets, `.ipynb_checkpoints`). Lesson 9 shows
`.gitignore`, which fixes this. For now, always run `git status` before
committing to check what is in the box.

## 10. Practice loop

Do this five times with small changes to any file, until it is boring:

```bash
# edit a file
git status
git diff
git add <file>
git commit -m "What and why"
git log --oneline
```

Boring is the goal. This loop is Git.

## Recap

| Command | Meaning |
|---------|---------|
| `git init` | turn this folder into a repository |
| `git status` | what state are my files in? |
| `git add <file>` / `git add .` | stage changes for the next commit |
| `git commit -m "msg"` | snapshot the staged changes |
| `git commit -am "msg"` | stage all modified tracked files and commit |
| `git diff` / `git diff --staged` | what changed, unstaged / staged |
| `git log --oneline` | compact history |
| `git show <id>` | what did that commit change? |

Next: [Lesson 4 — Undoing things](04-undoing-things.md)
