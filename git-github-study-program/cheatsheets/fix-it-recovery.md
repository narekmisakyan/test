# Fix it! — recovery cheat sheet

Find your situation, run the fix. Before anything drastic, run `git status`
and read it. Nothing committed is ever truly lost (see the last section).

## Uncommitted changes

| Situation | Fix |
|-----------|-----|
| I edited a file and want the last committed version back | `git restore <file>` (edits are gone for good) |
| I want to throw away **all** uncommitted edits | `git restore .` then `git clean -fd` for untracked files (check with `git clean -n` first) |
| I staged a file by mistake | `git restore --staged <file>` |
| I staged everything by mistake | `git restore --staged .` |
| I need to switch branches but have half-done work | `git stash`, switch, later `git stash pop` |
| Git refuses to switch branch: "would be overwritten" | commit or `git stash` first |
| I deleted a file by accident (not committed) | `git restore <file>` |
| I deleted a file and committed the deletion | `git restore --source HEAD~1 <file>` then commit |

## Last commit (not yet pushed)

| Situation | Fix |
|-----------|-----|
| Typo in the message | `git commit --amend -m "Fixed message"` |
| Forgot a file | `git add <file>` then `git commit --amend --no-edit` |
| Committed too much; want to split it | `git reset --soft HEAD~1`, then re-add and commit in pieces |
| Committed on the wrong branch | `git branch correct-branch` (saves it), `git reset --hard HEAD~1` (removes from here), `git switch correct-branch` |
| Want the commit gone **and** its changes gone | `git reset --hard HEAD~1` |
| Want the commit gone but keep changes to rework | `git reset HEAD~1` |
| Committed a secret (password, API key) | rotate the secret **now**; then `git reset --soft HEAD~1`, remove it, recommit. If already pushed, rotating is the only real fix. |

## Older or already-pushed commits

| Situation | Fix |
|-----------|-----|
| A pushed commit was wrong | `git revert <id>` then `git push` (makes an "undo" commit) |
| Several pushed commits were wrong | `git revert <oldest>^..<newest>` or revert each |
| I want to see the project as it was at commit X | `git checkout <id>`, look, `git switch main` to return |
| I want one file as it was at commit X | `git restore --source <id> <file>` |
| I amended/reset a commit that was already pushed and now push is rejected | if nobody else has pulled: `git push --force-with-lease`; otherwise `git pull`, accept the mess, and revert instead next time |

## Branches

| Situation | Fix |
|-----------|-----|
| I deleted a branch I still needed | `git reflog` to find its last commit id, then `git switch -c <name> <id>` |
| I am in "detached HEAD" and made commits | `git switch -c save-my-work` (commits now live on a branch) |
| I am in detached HEAD and made no commits | `git switch main` |
| Merge went wrong, want to start over | `git merge --abort` (during) or `git reset --hard HEAD~1` (after, if the merge commit is the last one and unpushed) |
| Rebase went wrong | `git rebase --abort` |
| Branch has drifted far behind main | `git switch my-branch && git merge main` (resolve conflicts) |

## Merge conflicts

1. `git status` lists files under *Unmerged paths*.
2. Open each. Find `<<<<<<< HEAD` … `=======` … `>>>>>>> branch`.
3. Edit to the final content; delete all three marker lines.
4. `git add <file>` for each.
5. `git commit`.

Shortcuts for "take one side entirely":

```bash
git checkout --ours <file>     # keep my version (current branch)
git checkout --theirs <file>   # keep their version (incoming branch)
git add <file>
```

Bail out: `git merge --abort`.

For a conflicted notebook: `nbmerge-web notebook.ipynb` (from `nbdime`), or
take one side with `--ours`/`--theirs` and re-apply the other change by hand.

## Remote problems

| Message | Meaning | Fix |
|---------|---------|-----|
| `! [rejected] ... (fetch first)` / `non-fast-forward` | remote has commits you lack | `git pull`, resolve, `git push` |
| `fatal: not a git repository` | you are not inside a repo folder | `cd` into it, or `git init` |
| `fatal: remote origin already exists` | remote is already set | `git remote set-url origin <url>` to change it |
| `There is no tracking information for the current branch` | branch not linked to remote | `git push -u origin <branch>` (or `git pull origin <branch>`) |
| `Permission denied (publickey)` | SSH key not set up or not added to GitHub | lesson 6, option B; or switch URL to HTTPS |
| `Authentication failed` over HTTPS | password used instead of token, or expired token | `gh auth login` or create a new token |
| `Updates were rejected because the tip of your current branch is behind` | same as fetch first | `git pull` then `git push` |
| `refusing to merge unrelated histories` | local and remote repos were both created with content | `git pull origin main --allow-unrelated-histories`, resolve, push |
| `error: Your local changes would be overwritten by merge` | uncommitted edits in files the pull would change | commit or `git stash`, then pull |
| Large file rejected (>100 MB) | GitHub limit | remove from the commit (`git rm --cached`, amend), add to `.gitignore`; consider Git LFS |

## .gitignore not working

| Situation | Fix |
|-----------|-----|
| File is ignored but still shows as modified | it was committed before being ignored: `git rm --cached <file>` then commit |
| Whole folder still tracked | `git rm -r --cached <folder>` then commit |
| Not sure why a file is/isn't ignored | `git check-ignore -v <file>` |

## "Everything is broken and I do not know what I did"

```bash
git reflog
```

This lists every state HEAD has been in, newest first, with what you did:

```
a1b2c3d HEAD@{0}: reset: moving to HEAD~2
f9e8d7c HEAD@{1}: commit: The commit I wanted to keep
...
```

Pick the entry from **before** the mistake and:

```bash
git reset --hard f9e8d7c          # go back there
# or, less drastic:
git switch -c rescue f9e8d7c      # put it on a new branch and inspect
```

The reflog keeps entries for 90 days. It recovers deleted branches, bad
resets, bad rebases and lost commits. The only things it cannot recover are
changes that were **never committed** and were destroyed by `git restore`,
`git reset --hard` or `git clean`. That is why you commit often.

## Nuclear option: start the clone over

If the local repo is hopeless and everything important is on GitHub:

```bash
cd ..
mv project project-broken        # keep it, just in case
git clone <url> project
```

Then copy any uncommitted files you still need from `project-broken`.
