# Glossary

Alphabetical. Words in *italics* have their own entry.

**add** — Put a file's changes into the *staging area*, selecting them for
the next *commit*. `git add file`.

**amend** — Replace the most recent commit with a corrected one.
`git commit --amend`. Only for commits not yet *pushed*.

**base branch** — In a *pull request*, the branch you want to merge into,
usually `main`.

**blame** — Show who last changed each line of a file and in which commit.
`git blame file`.

**branch** — A named pointer to a commit; a separate line of development.
Creating one is instant and copies nothing.

**checkout** — Older command for switching branches or restoring files. Now
split into `git switch` (branches) and `git restore` (files). Still used to
view an old commit: `git checkout <id>`.

**cherry-pick** — Copy a single commit from one branch onto another.

**CI (continuous integration)** — Automated scripts, such as tests, that
run on every push or PR. On GitHub they are *GitHub Actions*; results show
as a tick or cross next to commits.

**clone** — Copy an entire remote repository, including its history, to
your machine. `git clone <url>`.

**commit** — (noun) A snapshot of all tracked files plus author, date and
message, identified by a *hash*. (verb) To create one. `git commit`.

**conflict** — When a merge finds the same lines changed differently on both
sides and needs you to choose. Marked in files with `<<<<<<<`, `=======`,
`>>>>>>>`.

**default branch** — The branch GitHub shows first and PRs target by
default. Usually `main` (older repos: `master`).

**detached HEAD** — State where *HEAD* points directly at a commit instead
of a branch, typically after `git checkout <id>`. Commits made here are
easily lost unless you create a branch.

**diff** — The line-by-line difference between two versions. `-` lines
removed, `+` lines added.

**fast-forward** — A merge where the target branch simply moves its pointer
forward because it had no new commits of its own. No merge commit.

**fetch** — Download new commits and branches from a *remote* without
merging them. `git fetch`.

**fork** — Your own copy of someone else's repository on GitHub, so you can
push to it and open PRs against the original.

**Git** — The version control program. Runs locally.

**GitHub** — A website hosting Git repositories with pull requests, issues
and more. Alternatives: GitLab, Bitbucket.

**GitHub Actions** — GitHub's built-in *CI* system.

**`.gitignore`** — A file listing patterns of files Git should not track.

**hash / SHA** — The 40-character hexadecimal ID of a commit, e.g.
`3f2a9c1e...`. Usually abbreviated to the first 7 characters.

**HEAD** — The commit you are currently on; normally the tip of the current
branch. `HEAD~1` is its parent.

**index** — Another name for the *staging area*.

**issue** — A GitHub discussion thread for a bug, task or question,
numbered `#N`.

**main** — Conventional name of the primary branch. Formerly `master`.

**merge** — Combine the commits of one branch into another. May create a
*merge commit* with two parents.

**merge request** — GitLab's name for a *pull request*.

**origin** — Conventional name of your primary *remote*, the GitHub copy.

**pull** — `git fetch` followed by `git merge`: get remote commits and
merge them into the current branch. `git pull`.

**pull request (PR)** — A GitHub request to merge a branch, with discussion,
diff and review. Not a Git command.

**push** — Send your commits to a remote. `git push`.

**rebase** — Replay a branch's commits on top of another branch, producing a
straight history without merge commits. Rewrites commits; avoid on shared
branches.

**reflog** — Git's log of everywhere HEAD has pointed. The recovery tool.

**remote** — A named reference to another copy of the repo, e.g. `origin`
on GitHub, `upstream` for the original of a fork.

**repository / repo** — A folder tracked by Git, i.e. one that contains a
`.git` directory with the full history.

**reset** — Move the current branch pointer to another commit, optionally
changing the staging area (`--mixed`, default) and working directory
(`--hard`).

**restore** — Put a file back to a previous state: discard edits
(`git restore f`), unstage (`--staged`), or take an old version
(`--source <id>`).

**revert** — Create a new commit that undoes an earlier one. Safe for shared
history.

**squash** — Combine several commits into one, usually when merging a PR
("Squash and merge").

**staging area** — The set of changes queued for the next commit. Filled by
`git add`, emptied by `git commit`.

**stash** — Temporarily shelve uncommitted changes. `git stash` /
`git stash pop`.

**switch** — Change the current branch. `git switch name`; `-c` creates.

**tag** — A permanent label on a commit, used for version numbers like
`v1.0`.

**tracked / untracked** — A tracked file is one Git has in a commit or the
staging area. An untracked file exists on disk but Git has never been told
about it.

**upstream** — (1) The remote branch a local branch is linked to, set with
`push -u`. (2) Conventional remote name for the original repo when you work
on a fork.

**working directory / working tree** — The actual files on disk that you
edit.
