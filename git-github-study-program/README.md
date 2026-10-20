# Git & GitHub in Two Days — a study program for Python/Jupyter users

You know how to write Python in a Jupyter notebook. You have never used Git.
This program takes you from "what is a repository?" to confidently saving,
sharing and collaborating on code in **one focused day, or two relaxed ones**.

Everything is hands-on. You will type every command yourself, break things on
purpose, and fix them. By the end you will have your own repository on GitHub
containing a notebook, a Python script, a README and a clean history.

## How to use this program

1. Read the lessons **in order**. Each one is 15–30 minutes of reading plus
   practice. Do not skip the practice: Git is learned through the fingers.
2. Keep a terminal open next to the lesson and type the commands as you go.
3. At the end of each day do the exercise file. It ties the lessons together.
4. Afterwards, keep the `cheatsheets/` folder. That is what you will actually
   open six months from now.

A terminal means: **Terminal** on macOS, **Git Bash** on Windows (installed
with Git), or any shell on Linux. You can also open a terminal from
JupyterLab: *File → New → Terminal*.

## The schedule

### Day 1 — Git on your own computer (about 4–5 hours)

| # | Lesson | Time | You will be able to… |
|---|--------|------|----------------------|
| 1 | [Why version control?](day-1/01-why-version-control.md) | 15 min | explain what Git solves and the three key ideas |
| 2 | [Install and set up](day-1/02-install-and-setup.md) | 20 min | run `git` and have it know who you are |
| 3 | [Your first repo: the core loop](day-1/03-first-repo-the-core-loop.md) | 45 min | `init`, `status`, `add`, `commit`, `log`, `diff` |
| 4 | [Undoing things](day-1/04-undoing-things.md) | 40 min | recover from every common mistake |
| 5 | [Branches](day-1/05-branches.md) | 45 min | work on ideas in parallel and merge them, including conflicts |
| — | [Day 1 exercises](day-1/day-1-exercises.md) | 60 min | build a small project with a clean history |

### Day 2 — GitHub and working with others (about 4–5 hours)

| # | Lesson | Time | You will be able to… |
|---|--------|------|----------------------|
| 6 | [GitHub and remotes](day-2/06-github-and-remotes.md) | 45 min | create a repo on GitHub, `push`, `pull`, `clone` |
| 7 | [Pull requests and collaboration](day-2/07-pull-requests-and-collaboration.md) | 45 min | propose changes with a PR, review, fork, use issues |
| 8 | [Jupyter notebooks and Git](day-2/08-jupyter-notebooks-and-git.md) | 30 min | keep notebooks diff-able and your repo clean |
| 9 | [Good habits](day-2/09-good-habits.md) | 30 min | write good commits, `.gitignore`, README, tags |
| — | [Day 2 exercises](day-2/day-2-exercises.md) | 60 min | publish your project and collaborate with yourself |
| — | [Self-check quiz](self-check-quiz.md) | 20 min | confirm it stuck |

If you only have one day: do lessons 1–3, 5, 6, 7 and the Day 2 exercise. Read
4, 8 and 9 later, they are mostly reference material.

## The cheat sheets (keep these)

| Sheet | Open it when… |
|-------|---------------|
| [Git commands](cheatsheets/git-commands.md) | you forgot a command or a flag |
| [GitHub workflow](cheatsheets/github-workflow.md) | you need the step-by-step for a PR, fork or new repo |
| [Fix it! Recovery](cheatsheets/fix-it-recovery.md) | you made a mistake and need the way out |
| [Jupyter + Git](cheatsheets/jupyter-git.md) | notebooks are causing merge pain or huge diffs |
| [Glossary](cheatsheets/glossary.md) | a word in an error message or tutorial is unfamiliar |

## A mental model to carry through the whole program

Think of Git as **"Save and Checkpoint" in Jupyter, but done properly**:

* Jupyter's checkpoint keeps one previous version of one file.
  Git keeps **every** version of **every** file in your project, forever.
* Jupyter's checkpoint has no message. Every Git checkpoint (a *commit*) has a
  note saying what changed and why.
* Jupyter's checkpoint lives only on your laptop. GitHub lets you put your
  whole history on a server so you can share it, back it up and work on it
  from anywhere.

Git is the tool. GitHub is a website that hosts Git repositories and adds
collaboration features on top. You can use Git without GitHub; you cannot
meaningfully use GitHub without Git.
