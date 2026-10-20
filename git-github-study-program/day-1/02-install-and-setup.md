# Lesson 2 — Install and set up

**Time: 20 minutes.**

## 1. Install Git

Open a terminal and type:

```bash
git --version
```

If you see something like `git version 2.4x.x`, skip to step 2.

**macOS:** typing `git --version` offers to install the Xcode command line
tools. Accept. Alternatively `brew install git` if you use Homebrew.

**Windows:** download from https://git-scm.com/download/win and run the
installer. Accept all defaults. This also installs **Git Bash**, a terminal
that understands the same commands as macOS/Linux. Use Git Bash for this
program, not PowerShell or cmd, so the commands match exactly.

**Linux:** `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git`
(Fedora).

If you use Anaconda, `conda install git` also works inside your environment.

## 2. Tell Git who you are

Every commit records an author. Set it once, globally:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the same email you will use for your GitHub account, so GitHub can link
your commits to your profile.

## 3. Three settings that save future pain

```bash
# New repos start on a branch called "main" (GitHub's default), not "master"
git config --global init.defaultBranch main

# Use a simple editor for commit messages (nano) instead of vim
git config --global core.editor "nano"

# When pulling, do not create surprise merge commits (explained in lesson 6)
git config --global pull.rebase false
```

If you have VS Code, you can use it as the editor instead:
`git config --global core.editor "code --wait"`.

## 4. Check your configuration

```bash
git config --global --list
```

You should see your name, email and the settings above. These live in a file
called `~/.gitconfig`; you can open and edit it directly if you prefer.

## 5. Terminal survival kit

You will need a handful of shell commands. Jupyter users often have not used a
terminal much, so here is everything required:

| Command | Does |
|---------|------|
| `pwd` | print which folder you are in |
| `ls` (`ls -a` to include hidden files like `.git`) | list files |
| `cd folder` | go into a folder |
| `cd ..` | go up one level |
| `mkdir name` | make a folder |
| `touch file.py` | create an empty file |
| `cat file.py` | print a file's contents |
| `echo "text" > file.py` | overwrite a file with text |
| `echo "text" >> file.py` | append text to a file |
| `rm file.py` | delete a file (no trash can!) |
| `clear` | clear the screen |
| Tab key | autocomplete file names; press it constantly |
| Up arrow | recall previous commands |
| Ctrl+C | abort the current command |

In the exercises you can create and edit files in Jupyter or any editor
instead of using `echo`; the terminal is only needed for the `git` commands.

## 6. Create a GitHub account (needed on Day 2)

Go to https://github.com and sign up with the same email as above. Pick a
username you are happy to show on a CV; it becomes part of your public URL.
Enable two-factor authentication when prompted; GitHub now requires it for
most accounts.

That is all for now. Authentication (letting your terminal talk to GitHub)
is covered in lesson 6.

## Check yourself

Run `git config user.name` and `git config user.email`. Both print the values
you set.

Next: [Lesson 3 — Your first repo: the core loop](03-first-repo-the-core-loop.md)
