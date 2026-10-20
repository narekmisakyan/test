# GitHub workflow cheat sheet

Step-by-step recipes for the things you do on GitHub. Assumes you have
authenticated once (`gh auth login`, an SSH key, or a token).

## Put an existing local project on GitHub

1. GitHub → **+** → *New repository*. Name it. **Do not** add README,
   `.gitignore` or license (keep it empty).
2. ```bash
   cd project
   git remote add origin https://github.com/USER/project.git
   git push -u origin main
   ```
3. Refresh the page.

## Start a new project from GitHub

1. GitHub → **+** → *New repository*. This time tick *Add a README* and pick
   a Python `.gitignore` and a license.
2. `git clone https://github.com/USER/project.git` and `cd project`.

## Get a copy of any public repo

```bash
git clone https://github.com/OWNER/repo.git
```

## Daily sync

```bash
git pull            # start of session
# work, commit
git push            # end of session
```

## Push rejected: "fetch first" / "non-fast-forward"

```bash
git pull            # merge their work; fix conflicts if any; commit
git push
```

## The pull request recipe

```bash
git switch main && git pull                    # start from fresh main
git switch -c short-descriptive-name           # branch
# edit, git add, git commit (several times is fine)
git push -u origin short-descriptive-name      # publish branch
```

Then on GitHub: *Compare & pull request* → title + description (`Closes #N`
to link an issue) → *Create pull request*.

Reviewer asks for changes:

```bash
# edit, git add, git commit
git push                                       # PR updates itself
```

After merge (button on GitHub, then *Delete branch*):

```bash
git switch main
git pull
git branch -d short-descriptive-name
git fetch --prune
```

## PR says "This branch has conflicts"

```bash
git switch my-branch
git pull origin main        # merge latest main into the branch
# resolve conflicts, git add <files>, git commit
git push
```

## Contribute to a project you cannot push to (fork workflow)

1. Click **Fork** on their repo.
2. `git clone https://github.com/YOU/repo.git && cd repo`
3. `git remote add upstream https://github.com/THEM/repo.git`
4. `git switch -c my-fix`, commit, `git push -u origin my-fix`
5. Open PR; base = their repo `main`, compare = your fork `my-fix`.
6. Keep your fork fresh:
   ```bash
   git switch main
   git fetch upstream
   git merge upstream/main
   git push
   ```

## Issues

* **New issue**: title, description, labels. Each gets a number `#N`.
* Reference from commit message or PR: `See #N`. Close via PR: `Closes #N`,
  `Fixes #N`, `Resolves #N` in the PR description.

## Release a version

```bash
git tag -a v1.2.0 -m "Describe the release"
git push origin v1.2.0
```

GitHub → *Releases* → *Draft a new release* → choose the tag → notes →
*Publish*. Users can download a zip of that exact version.

## Authentication

| Method | Setup |
|--------|-------|
| GitHub CLI | install `gh`, run `gh auth login`, follow prompts |
| SSH | `ssh-keygen -t ed25519 -C "email"`, copy `~/.ssh/id_ed25519.pub` to *Settings → SSH and GPG keys*, use `git@github.com:USER/repo.git` URLs |
| Token | *Settings → Developer settings → Personal access tokens*; paste as password when Git asks |

Switch an existing clone between HTTPS and SSH:
`git remote set-url origin git@github.com:USER/repo.git`

## Useful `gh` CLI commands

```bash
gh repo create project --private --source=. --push   # create repo from current folder and push
gh repo clone OWNER/repo
gh pr create --fill                                   # open PR from current branch
gh pr list
gh pr checkout 42                                     # get PR #42 locally
gh pr merge 42 --squash --delete-branch
gh issue create --title "Bug" --body "Details"
gh issue list
gh browse                                             # open repo in browser
```

## Where things are on the GitHub page

| Want | Where |
|------|-------|
| clone URL | green **Code** button |
| history | *commits* link above file list |
| switch branch | branch dropdown, top left |
| edit a file in browser | pencil icon on the file (creates a commit) |
| file history | open file → *History* |
| who changed a line | open file → *Blame* |
| CI results | *Actions* tab; tick/cross next to commits |
| settings, collaborators, delete repo | *Settings* tab |
| browser VS Code | press `.` anywhere in the repo |

## Markdown you will use in READMEs, issues and PRs

````markdown
# Heading 1
## Heading 2
**bold**  *italic*  `inline code`
- bullet
1. numbered
[link text](https://url)
![image alt](path/to/image.png)
> quote
- [ ] task not done
- [x] task done

```python
code block
```
````

Tables: `| a | b |` rows with a `|---|---|` line under the header.
