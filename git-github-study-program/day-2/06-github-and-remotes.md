# Lesson 6 — GitHub and remotes

**Time: 45 minutes.** You need the GitHub account from lesson 2.

So far everything lived on your laptop. Today you connect it to GitHub.

## 1. What a remote is

A **remote** is a named link to another copy of your repository, usually on
GitHub. By convention the main remote is called `origin`.

Pushing sends your commits to the remote. Pulling fetches commits from the
remote and merges them into your branch. Nothing happens automatically; Git
only talks to the remote when you tell it to.

```
   your laptop                                  github.com
   ┌─────────────┐      git push               ┌─────────────┐
   │  main       │ ──────────────────────────▶ │  main       │
   │  (local)    │ ◀────────────────────────── │  (origin)   │
   └─────────────┘      git pull / fetch       └─────────────┘
```

## 2. Authenticate once

GitHub no longer accepts your account password from the command line. Pick
one of these, once per machine.

### Option A — GitHub CLI (easiest)

Install `gh` from https://cli.github.com (`brew install gh`, `winget install
GitHub.cli`, or your Linux package manager). Then:

```bash
gh auth login
```

Choose *GitHub.com → HTTPS → Login with a web browser*, follow the prompts.
This also configures Git to use the stored credential. Done.

### Option B — SSH keys (what most developers end up using)

```bash
ssh-keygen -t ed25519 -C "you@example.com"      # press Enter for all prompts
cat ~/.ssh/id_ed25519.pub                       # print the PUBLIC key
```

Copy the printed line. On GitHub: *Settings → SSH and GPG keys → New SSH
key*, paste, save. Test:

```bash
ssh -T git@github.com
# Hi username! You've successfully authenticated...
```

With SSH, repository addresses look like `git@github.com:user/repo.git`.
With HTTPS they look like `https://github.com/user/repo.git`. Use whichever
matches how you authenticated.

### Option C — Personal access token over HTTPS

*Settings → Developer settings → Personal access tokens → Fine-grained
tokens*. Create one with *Contents: read and write* on your repos. When Git
asks for a password, paste the token. A credential helper (installed with Git
on Windows and macOS) remembers it.

## 3. Put an existing local repo on GitHub

Use your `cleankit` repo from the Day 1 exercise.

1. On github.com click **+ → New repository**. Name it `cleankit`. Leave it
   **empty**: do not tick "Add a README", do not add `.gitignore` or a license
   (you already have content; a non-empty remote complicates the first push).
   Choose Public or Private. Click *Create repository*.
2. GitHub shows instructions. The relevant part:

```bash
cd ~/cleankit
git remote add origin https://github.com/YOURNAME/cleankit.git   # or the git@ form
git push -u origin main
```

`-u` (upstream) links your local `main` to `origin/main` so that in future
plain `git push` and `git pull` know where to go. You only need `-u` the
first time for each branch.

Refresh the GitHub page. Your files and your whole history are there. Click
*commits* to browse them; click any file and press the *History* button.

```bash
git remote -v          # show configured remotes
```

## 4. Starting from GitHub instead: `git clone`

The other direction. If the repo already exists on GitHub (yours or someone
else's, public), copy it to your machine:

```bash
cd ~
git clone https://github.com/YOURNAME/cleankit.git cleankit-copy
cd cleankit-copy
git log --oneline      # full history came along
git remote -v          # origin is already set up
```

Try cloning something real: `git clone https://github.com/pandas-dev/pandas.git`
gives you the entire source and 15 years of history of pandas. (It is
large; delete it afterwards.)

## 5. The daily rhythm: pull, work, commit, push

```bash
git pull               # get anything new from GitHub first
# ... edit, git add, git commit, repeat ...
git push               # send your commits to GitHub
```

`git pull` is actually two steps: `git fetch` (download new commits to a
hidden `origin/main` reference) followed by `git merge origin/main`. You can
run them separately when you want to look before merging:

```bash
git fetch
git log --oneline main..origin/main    # what is on GitHub that I lack?
git merge origin/main
```

## 6. Simulate a collaborator

You have two clones now: `~/cleankit` and `~/cleankit-copy`. Pretend they are
you and a teammate.

1. In `cleankit-copy`, add a line to `README.md`, commit, `git push`.
2. In `cleankit`, run `git pull`. The line appears.
3. Now in `cleankit`, change `cleankit.py` and commit. In `cleankit-copy`,
   change `README.md` again and commit, then push.
4. In `cleankit`, `git push`:

```
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

This is the single most common Git message in team work. It means: *someone
pushed since you last pulled. Pull first, then push.*

```bash
git pull           # merges origin's new commit with yours (may open editor; save and close)
git push           # now succeeds
```

If both of you edited the same lines, the pull produces a conflict, which you
resolve exactly as in lesson 5, then `git push`.

## 7. Pushing branches

Branches are local until you push them:

```bash
git switch -c add-docs
# ... commit ...
git push -u origin add-docs     # creates the branch on GitHub
```

Later, `git push` alone works on that branch. To see remote branches:
`git branch -r`. To get a branch a teammate pushed:

```bash
git fetch
git switch their-branch          # Git creates a local copy tracking origin/their-branch
```

To delete a branch on GitHub after merging: `git push origin --delete
add-docs`.

## 8. Rules for shared history

Once a commit is pushed, assume someone else has it.

* **Never** `--amend`, `reset`, or `rebase` commits that are already pushed to
  a shared branch. Use `git revert` instead.
* **Never** `git push --force` to `main`. On your own feature branch that
  nobody else has pulled, `git push --force-with-lease` is acceptable after
  an amend; the `--with-lease` part refuses if someone else pushed meanwhile.
* Pull before you start work; push when you stop. Small, frequent pushes
  mean small, easy merges.

## 9. Reading a GitHub repository page

Spend five minutes on your repo's page and find:

* **Code** tab: files, latest commit per file, the README rendered below.
* The **branch dropdown** (top left of the file list).
* **Commits** link: the history, with a diff view per commit.
* **Issues**, **Pull requests**, **Actions**, **Settings** tabs.
* The green **Code** button: the clone address.
* The pencil icon on any file: edit in the browser (this makes a commit!).

## Recap

| Command | Meaning |
|---------|---------|
| `git remote add origin <url>` | link local repo to GitHub |
| `git remote -v` | list remotes |
| `git push -u origin main` | first push of a branch |
| `git push` / `git pull` | sync current branch |
| `git fetch` | download without merging |
| `git clone <url>` | copy a remote repo locally |
| `git push -u origin <branch>` | publish a branch |
| `git push origin --delete <branch>` | delete a remote branch |
| `git branch -r` | list remote branches |

Next: [Lesson 7 — Pull requests and collaboration](07-pull-requests-and-collaboration.md)
