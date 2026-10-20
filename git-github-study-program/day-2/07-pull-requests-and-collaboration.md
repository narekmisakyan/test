# Lesson 7 — Pull requests and collaboration

**Time: 45 minutes.**

A **pull request** (PR) is GitHub's way of saying: "I have a branch with
changes; please review them and merge them into `main`." It is the heart of
how teams and open-source projects work. (GitLab calls the same thing a
*merge request*.)

A PR is not a Git concept; you cannot make one from the command line with
plain `git`. It lives on GitHub and wraps a branch.

## 1. The pull request workflow

```
1. git switch -c my-change         create a branch
2. edit, commit, commit            do the work
3. git push -u origin my-change    publish the branch
4. open PR on GitHub               describe what and why
5. review: comments, fixes         push more commits; they join the PR
6. merge on GitHub                 main now has the change
7. delete branch, git pull main    clean up locally
```

## 2. Do it

In `~/cleankit`:

```bash
git switch main
git pull
git switch -c add-usage-example
```

Add a usage example section to `README.md` and commit:

```bash
git commit -am "Add usage example to README"
git push -u origin add-usage-example
```

The push output contains a link:
`remote: Create a pull request for 'add-usage-example' on GitHub by visiting: https://github.com/.../pull/new/add-usage-example`.
Open it (or go to the repo page, where a yellow banner offers *Compare & pull
request*).

Fill in:

* **Title**: a short imperative sentence, like a commit message.
* **Description**: what changed and *why*; what a reviewer should look at;
  how you tested it. Markdown works. Writing `Closes #4` links and auto-closes
  issue number 4 when merged.

Click **Create pull request**.

## 3. Read the PR page

* **Conversation** tab: the description and discussion.
* **Commits** tab: the commits in this branch that `main` lacks.
* **Files changed** tab: the full diff. Hover over a line and click the blue
  `+` to leave a comment on that exact line. This is how code review works.
* The **merge box** at the bottom: says whether it can be merged
  automatically (no conflicts) and offers a green **Merge pull request**
  button.

Leave yourself a review comment on a line, then reply to it. This is what a
teammate's feedback looks like.

## 4. Respond to review

A reviewer asked for a change. You simply commit more on the same branch and
push:

```bash
# edit README.md
git commit -am "Clarify example output"
git push
```

The PR updates automatically. Conversations can be marked *Resolved*.

## 5. Merge

Click **Merge pull request → Confirm merge**. The dropdown offers three
styles; for now the default *Create a merge commit* is fine. (*Squash and
merge* collapses all the PR's commits into one, which many teams prefer for
a tidy `main`. *Rebase and merge* replays them without a merge commit.)

Click **Delete branch** afterwards. Then locally:

```bash
git switch main
git pull                              # main now includes the PR
git branch -d add-usage-example       # local branch no longer needed
git fetch --prune                     # forget remote branches that were deleted
```

## 6. Handling a PR that has conflicts

If `main` changed while your PR was open and GitHub says *This branch has
conflicts that must be resolved*, bring `main` into your branch locally:

```bash
git switch add-usage-example
git pull origin main              # merge the latest main into your branch
# resolve conflicts as in lesson 5, git add, git commit
git push
```

The PR becomes mergeable. For small conflicts GitHub also offers a
*Resolve conflicts* button in the browser.

## 7. Contributing to someone else's project: forks

You cannot push to a repository you do not own. The open-source workflow:

1. On their repo page click **Fork**. GitHub copies the repo under your
   account.
2. `git clone` **your fork**.
3. Add the original as a second remote so you can stay up to date:
   `git remote add upstream https://github.com/THEM/project.git`
4. Branch, commit, push to **your fork** (`origin`).
5. Open a PR; GitHub notices the fork and lets you target the original repo.
6. To refresh your fork later:
   `git switch main && git fetch upstream && git merge upstream/main && git push`.

Before contributing, read the project's `CONTRIBUTING.md` if it has one, and
open an issue to discuss anything bigger than a typo fix.

## 8. Issues

**Issues** are GitHub's bug tracker and to-do list. Each has a number, a
title, a discussion thread, labels (`bug`, `enhancement`), an assignee and
optional milestone. Reference an issue from any commit message or PR with
`#12`; GitHub links them. Write `Fixes #12` in a PR description and the issue
closes when the PR merges.

Create one on your `cleankit` repo now: "Add a function that removes
duplicates". Then make a branch, implement it, open a PR whose description
says `Closes #1`, merge it, and watch the issue close.

## 9. Other GitHub features worth knowing exist

You do not need these today, but you will meet them:

* **README.md** is rendered on the repo front page. Markdown.
* **Releases/tags** mark versions (lesson 9).
* **GitHub Actions**: scripts that run automatically on every push or PR,
  typically tests. A green tick or red cross next to a commit comes from
  here.
* **GitHub Pages**: free static website hosting from a repo.
* **Codespaces**: a full VS Code + terminal in the browser, running on
  GitHub's machines. Handy for trying a repo without installing anything.
* **Gists**: single-file snippets with their own URL, good for sharing one
  notebook or script.
* **Discussions**, **Projects** (kanban boards), **Wiki**.
* **Dependabot** alerts you when a dependency has a security problem.

## 10. Working in the browser

For a one-line fix, you can skip the terminal: click the pencil icon on a
file, edit, and choose *Create a new branch and start a pull request*. GitHub
makes the commit, the branch and the PR for you. Press `.` on any repo page to
open it in a browser VS Code.

## Recap

* PR = "please merge my branch", with review. Branch → push → open PR →
  review → merge → delete branch → pull `main`.
* More commits on the branch update the PR.
* Fork when you lack push rights; `origin` is your fork, `upstream` is the
  original.
* Issues track work; `Closes #N` links and closes them.

Next: [Lesson 8 — Jupyter notebooks and Git](08-jupyter-notebooks-and-git.md)
