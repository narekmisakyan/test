# Lesson 1 — Why version control?

**Time: 15 minutes. No typing yet.**

## The problem you already have

Open your project folder. Does it look like this?

```
analysis.ipynb
analysis_v2.ipynb
analysis_v2_fixed.ipynb
analysis_FINAL.ipynb
analysis_FINAL_really.ipynb
analysis_FINAL_really (1).ipynb
```

Every data scientist has lived this. It creates four problems:

1. **Which one is current?** Nobody knows, not even you in a month.
2. **What changed between v2 and v2_fixed?** You would have to open both and
   compare by eye.
3. **Can I go back?** Only if you kept the old copy and remember what was in it.
4. **Can two people work on it?** Email it, then merge changes by hand. Painful.

Version control solves all four. **Git** is by far the most popular version
control system. It was written in 2005 by Linus Torvalds (who also wrote
Linux) and today practically every software project uses it.

## The three ideas that make Git click

### 1. A repository is a folder with a memory

A *repository* (repo) is just a normal folder on your disk with one hidden
sub-folder called `.git` inside it. That hidden folder is the memory: it stores
every version of every file you have ever asked Git to remember.

You never touch `.git` by hand. You talk to it through `git` commands.

Delete `.git` and the folder is a normal folder again. Nothing else changes.

### 2. A commit is a snapshot with a message

When you tell Git "remember this", it takes a *snapshot* of all your files at
that moment, attaches your name, the date and a message you write, and gives
it an ID. That snapshot is a **commit**.

Commits chain together: each one points to the one before it. The chain is
the **history** of your project. You can walk back along it to any point.

```
 first commit        add plot          fix bug          add README
      o ----------------- o ----------------- o ----------------- o   <- now
```

A commit is permanent and cheap. Make many small ones.

### 3. A branch is a parallel line of history

Want to try a risky idea without disturbing your working code? Make a
**branch**. It is a separate line of commits that starts from where you are.
When the idea works, you **merge** the branch back. When it does not, you
delete the branch and nothing happened.

```
                     try-new-model
                 o -------- o -------- o
                /                        \
   o -------- o -------- o -------- o ---- o   main
```

Branches are what make collaboration possible: everyone works on their own
branch and merges when ready.

## Where GitHub fits

Git works entirely on your computer. **GitHub** is a company (owned by
Microsoft) that hosts Git repositories on the internet. When you *push* your
repo to GitHub:

* it is backed up,
* other people (or you, on another machine) can *clone* it,
* you get a web interface to browse history, discuss changes, review code and
  track bugs.

GitLab and Bitbucket are competitors that do the same thing. The Git commands
are identical; only the website differs.

## Vocabulary for today

| Word | Meaning |
|------|---------|
| repository / repo | a folder tracked by Git (has a `.git` inside) |
| commit | a saved snapshot with a message |
| history | the chain of commits |
| branch | an independent line of commits |
| merge | combine the commits of one branch into another |
| working directory | your actual files on disk, the ones you edit |
| remote | a copy of the repo living somewhere else, usually GitHub |

## Check yourself

* What would you lose if you deleted the `.git` folder? *(The entire history.
  Your current files would stay.)*
* What two things does every commit carry besides the file snapshot?
  *(An author/date and a message.)*
* Is GitHub required to use Git? *(No.)*

Next: [Lesson 2 — Install and set up](02-install-and-setup.md)
