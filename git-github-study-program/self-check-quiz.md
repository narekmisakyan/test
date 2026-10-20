# Self-check quiz

Twenty questions. Answer each in your head or on paper, then expand the
answer. Aim for 16+ before calling the program finished.

### 1. What is the difference between Git and GitHub?
<details><summary>Answer</summary>
Git is the version control program running on your computer. GitHub is a
website that hosts Git repositories and adds collaboration features (pull
requests, issues, reviews). Git works without GitHub.
</details>

### 2. What does `git status` change?
<details><summary>Answer</summary>
Nothing. It only reports the state of the working directory and staging
area. Run it as often as you like.
</details>

### 3. Why are `git add` and `git commit` separate steps?
<details><summary>Answer</summary>
So you can choose which changes go into a commit. The staging area lets you
make several focused commits out of one editing session.
</details>

### 4. You edited `a.py` and `b.py`. How do you commit only `a.py`?
<details><summary>Answer</summary>
`git add a.py` then `git commit -m "..."`. Do not use `git add .` or
`git commit -a`.
</details>

### 5. What does `git commit -am "msg"` not include?
<details><summary>Answer</summary>
New, untracked files. `-a` only stages modifications and deletions of files
Git already tracks.
</details>

### 6. What is `HEAD`?
<details><summary>Answer</summary>
A pointer to the commit you are currently standing on, normally the tip of
the current branch.
</details>

### 7. You want to discard your uncommitted edits to `notes.txt`.
<details><summary>Answer</summary>
`git restore notes.txt`. Irreversible: the edits are gone.
</details>

### 8. You committed too early and want to add more to that commit before pushing.
<details><summary>Answer</summary>
Stage the extra changes, then `git commit --amend --no-edit` (or
`--amend -m "new message"`). Only for unpushed commits.
</details>

### 9. Difference between `git reset --soft HEAD~1` and `git reset --hard HEAD~1`?
<details><summary>Answer</summary>
Both remove the last commit from the branch. `--soft` keeps its changes
staged; `--hard` throws the changes away from disk as well.
</details>

### 10. A bad commit was pushed to `main` two days ago. How do you cancel it?
<details><summary>Answer</summary>
`git revert <id>` creates a new commit that undoes it. Do not reset or
rewrite shared history.
</details>

### 11. What is a branch, physically?
<details><summary>Answer</summary>
A name (a tiny file) pointing to a commit. Committing on a branch moves the
pointer. Creating one copies nothing.
</details>

### 12. What is a fast-forward merge?
<details><summary>Answer</summary>
When the target branch has no new commits of its own, Git just moves its
pointer forward to the merged branch's tip. No merge commit is created.
</details>

### 13. You see `<<<<<<< HEAD` in a file. What happened and what do you do?
<details><summary>Answer</summary>
A merge conflict: both branches changed those lines. Edit the file to the
version you want, remove the marker lines, `git add` the file, `git commit`.
`git merge --abort` cancels instead.
</details>

### 14. `git push` is rejected with "fetch first". Why, and what now?
<details><summary>Answer</summary>
The remote has commits you do not have. `git pull` (resolve any conflicts),
then `git push`.
</details>

### 15. What does `git pull` actually do?
<details><summary>Answer</summary>
`git fetch` (download new commits from the remote) followed by `git merge`
of the remote branch into your current branch.
</details>

### 16. What is `origin`?
<details><summary>Answer</summary>
The conventional name for your default remote, usually the GitHub copy of the
repo you cloned from or pushed to.
</details>

### 17. When should you never use `git push --force`?
<details><summary>Answer</summary>
On a shared branch like `main`, or any branch others may have pulled. It
overwrites their history. On your own unshared feature branch,
`--force-with-lease` after an amend is acceptable.
</details>

### 18. What is a pull request?
<details><summary>Answer</summary>
A GitHub request to merge one branch into another, with a description, a
diff, review comments and a merge button. Not a Git command; it wraps a
pushed branch.
</details>

### 19. Why do notebooks cause merge conflicts, and what is the fix?
<details><summary>Answer</summary>
`.ipynb` files store outputs and execution counts as JSON, which differ on
every run. Strip them before committing (`nbstripout --install`) and move
stable code into `.py` modules.
</details>

### 20. Name four things that should be in a Python project's `.gitignore`.
<details><summary>Answer</summary>
Any four of: `.ipynb_checkpoints/`, `__pycache__/`, `*.pyc`, `.venv/`,
`.env`, `data/`, `*.csv`, `.DS_Store`, `.vscode/`.
</details>

### Bonus. You ran `git reset --hard` and lost a commit. Is it gone?
<details><summary>Answer</summary>
No. `git reflog` lists where HEAD has been; find the commit id and
`git reset --hard <id>` or `git switch -c rescue <id>`. Only uncommitted work
is truly lost.
</details>
