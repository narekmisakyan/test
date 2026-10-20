# Git commands cheat sheet

Modern Git (2.23+). Older tutorials use `git checkout` where this sheet uses
`git switch` / `git restore`; both still work.

## Setup (once per machine)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "nano"           # or "code --wait"
git config --global --list                        # show all settings
```

## Start

```bash
git init                          # make current folder a repo
git clone <url>                   # copy a remote repo into a new folder
git clone <url> folder-name       # ... with a chosen folder name
```

## The daily loop

```bash
git status                        # what state is everything in? (safe, run often)
git add <file>                    # stage one file
git add <folder>/                 # stage a folder
git add .                         # stage everything in current folder (check status first!)
git add -p                        # stage interactively, hunk by hunk
git commit -m "Subject"           # commit staged changes
git commit                        # commit; editor opens for a longer message
git commit -am "Subject"          # stage all *tracked* modified files + commit
git commit --amend                # replace last commit (unpushed only)
git commit --amend --no-edit      # ... keeping the message
```

## Looking around

```bash
git diff                          # unstaged changes vs staging area
git diff --staged                 # staged changes vs last commit
git diff main..feature            # difference between two branches
git diff <id1> <id2>              # between two commits
git log                           # full history
git log --oneline                 # one line per commit
git log --oneline --graph --all   # all branches as a graph
git log -p <file>                 # history of one file with diffs
git log --author="Name"           # filter by author
git log --since="2 weeks ago"     # filter by date
git show <id>                     # what one commit changed
git show <id>:<path>              # print a file as it was at that commit
git blame <file>                  # who last changed each line
git grep "pattern"                # search tracked files
```

## Undo

```bash
git restore <file>                # discard unstaged edits (irreversible)
git restore --staged <file>       # unstage, keep edits
git restore --source <id> <file>  # bring back a file from an old commit
git reset --soft HEAD~1           # undo last commit, keep changes staged
git reset HEAD~1                  # undo last commit, keep changes unstaged
git reset --hard HEAD~1           # undo last commit, delete changes (dangerous)
git reset --hard <id>             # move branch to <id>, discard everything after
git revert <id>                   # new commit that undoes <id> (safe for shared history)
git clean -n                      # show untracked files that would be deleted
git clean -fd                     # delete untracked files and folders
git reflog                        # every place HEAD has been; recovery map
```

## Stash

```bash
git stash                         # park modified tracked files
git stash -u                      # ... including untracked files
git stash list
git stash pop                     # restore newest stash and drop it
git stash apply stash@{2}         # restore a specific one, keep it
git stash drop stash@{0}
```

## Branches

```bash
git branch                        # list local branches (* = current)
git branch -a                     # include remote branches
git switch -c <name>              # create and switch
git switch <name>                 # switch
git switch -                      # back to previous branch
git switch -c <name> <id>         # branch starting from an old commit
git merge <name>                  # merge <name> into current branch
git merge --abort                 # cancel a conflicted merge
git branch -d <name>              # delete merged branch
git branch -D <name>              # force-delete
git branch -m <new>               # rename current branch
git rebase main                   # replay current branch on top of main (unshared branches only)
git cherry-pick <id>              # copy one commit onto current branch
```

## Remotes

```bash
git remote -v                     # list remotes
git remote add origin <url>       # link to GitHub
git remote set-url origin <url>   # change the address
git push -u origin main           # first push of a branch (sets upstream)
git push                          # push current branch
git push origin <branch>          # push a specific branch
git push origin --delete <branch> # delete a remote branch
git push --force-with-lease       # overwrite remote branch, safely-ish (own branches only)
git fetch                         # download remote commits, do not merge
git fetch --prune                 # ... and forget deleted remote branches
git pull                          # fetch + merge into current branch
git pull origin main              # merge remote main into current branch
git branch -r                     # list remote branches
git switch <remote-branch-name>   # create local copy tracking it
```

## Tags

```bash
git tag                           # list
git tag -a v1.0 -m "Release 1.0"  # annotated tag on HEAD
git tag -a v0.9 <id> -m "..."     # tag an older commit
git push origin v1.0              # push one tag
git push --tags                   # push all tags
git checkout v1.0                 # look at a tagged version (detached HEAD)
git tag -d v1.0                   # delete locally
```

## Files

```bash
git rm <file>                     # delete and stage the deletion
git rm --cached <file>            # stop tracking, keep on disk (after adding to .gitignore)
git mv <old> <new>                # rename
git ls-files                      # list tracked files
git check-ignore -v <file>        # why is this file ignored?
```

## Referring to commits

| Syntax | Means |
|--------|-------|
| `3f2a9c1` | commit by (abbreviated) hash |
| `HEAD` | current commit |
| `HEAD~1`, `HEAD~3` | 1 or 3 commits before HEAD |
| `main`, `origin/main` | tip of a local / remote branch |
| `v1.0` | a tag |
| `main..feature` | commits in feature not in main |
| `stash@{0}` | newest stash |

## Handy aliases

```bash
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
```
