---
title: "Chapter 7 — The Linux system"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
draft plan, 2026-11-17, revised the same day after the Codex review
(`chapter_07_codex_review.md`; see *Review responses*). Written while the Chapter 5 and 6 plans were
being drafted in parallel sessions; boundaries with them are under
*What this chapter builds on* and were agreed with the Chapter 5 session
(see *Coordination*). Outputs marked *captured* were recorded on
2026-11-17 on macOS 15 Intel in a scratch folder, with Homebrew bash
5.3.15 and GNU coreutils 9.11 (gnubin first on `PATH`, as after Chapter
1), and, for the BSD rows, the Mac's own `/bin/bash` 3.2 and BSD tools.
Rows marked *to capture* still need a Linux (Ubuntu/WSL) or cluster run.

## From `PLAN_CHAPTERS.md`

- Users, groups, permissions, `chmod`
- Executable files and shebang lines
- `PATH` and environment variables
- `.bashrc` vs `.bash_profile`
- Processes: `ps`, `top`; interrupting (Ctrl-C) and `kill`
- Disk usage: `df`, `du`
- GNU (Linux) vs BSD (macOS) tools
- Line endings (LF vs CRLF)

## What this chapter builds on

Earlier chapters made promises this chapter must keep (each one is a
forward link already in the written text):

- **Chapter 1:** the macOS `~/.bash_profile` block (Homebrew `shellenv`,
  the `gnubin` loop on `PATH`, `MANPATH`, then "read `~/.bashrc` too")
  was copied and run on trust; "`@sec-linux-system` explains the
  differences" between GNU and BSD tools. The WSL pitfall says
  `/mnt/c/...` invites "line-ending and permission problems". `df -h ~`
  was used to read free disk. Ctrl-C "stops the running command".
- **Chapter 2:** the pixi installer "adds `~/.pixi/bin` to your `PATH`
  … in `~/.bashrc`"; "`@sec-linux-system` explains how the shell finds
  commands" (why bare `seqkit` is not found, what `pixi run` and
  `pixi shell` change); `export EDITOR=nano` "lasts only for the current
  terminal; `@sec-linux-system` shows how to make it permanent";
  `chmod 700 ~/.ssh`; `export PIXI_CACHE_DIR=…` on clusters.
- **Chapter 3:** `chmod a-w data/raw/* data/raw`, `ls -ld`, and the
  finding that a read-only file in a writable folder can still be
  deleted with `rm -f` (misconception `readonly-cant-delete`);
  "`@sec-linux-system` explains permissions properly".
- **Chapter 4:** `command not found` (exit 127) "not on this shell's
  `PATH`"; "if another copy is installed, it runs that one instead,
  possibly a different version (`@sec-linux-system`)"; `Permission denied`
  and `No space left on device` rows of `tbl-common-errors`; `echo $?`.
- **Chapter 5 (planned, parallel session):** names the `ls -l` fields
  (type letter `d`/`l`/`-`, owner, group, size, time, name, `->`) and
  leaves the permission column to this chapter; uses `type cd` / `type
  ls` only to tell a builtin from a program; one line on Ctrl-C and
  stopping `tail -f`; `file` to spot gzip/binary files before `cat`;
  forward mention that a folder's size in `ls -l` is not its contents';
  points `.bashrc` history settings here. No `find -perm`, `umask`,
  groups, or the executable bit.
- **Chapter 6 (planned, parallel session; confirmed by it):** pipes;
  `>`, `>>`, `<`, `tee`; stdout/stderr, `2>`, `2>&1`, `&>`,
  `/dev/null`, `noclobber`; `wc`, `cut`, `sort`, `uniq` (with
  `LC_ALL=C` for sort order); `grep` and regular expressions; `sed` and
  `awk` basics, with `sed -i` "never on `data/raw/`"; `zcat`/`gzip`.
  It uses `cat -A` once, to show tabs (`^I`) and colour codes, leaving
  line endings here; mentions Ctrl-C in one line; and notes that a
  redirect into read-only `data/raw/` gives `Permission denied` without
  explaining permissions. This chapter uses pipes, `>>`, `sort`, and `cat -A`
  without teaching them (Chapter 6 teaches `sort -n -k -t -r -u`, not
  `-h`; §8 adds `-h` in one line), and owns the GNU vs BSD `sed -i`
  difference. Exit status in pipelines (`PIPESTATUS`) is Chapter 8.

Boundary with Chapter 8: this chapter makes a one-line script runnable
(shebang, executable bit, `PATH`); variables, quoting, loops, arguments,
and `set -euo pipefail` are Chapter 8. Boundary with Chapter 10: a
process here vs a submitted job there; `module load` is named here as
"something that changes `PATH`" and taught there.

## Outcome and check

- **Outcome:** readers can read and change the permissions on their own
  files and folders and say why a command was refused; make a script
  run as a command; explain why a command is or is not found, and which
  copy runs; set an environment variable for one command, one session,
  or every new terminal (in the right startup file); find, stop, and
  end their own processes; find what fills a disk; recognise a GNU-only
  option failing on BSD tools; and detect and fix Windows line endings
  in a sample sheet or script.
- **Check:** exercise 1's folder `~/bioinf-computing-ch07/` holds a supplied
  script `bin/count_lines.sh` (Windows line endings, mode set to
  `644` by the setup block, so not executable even on a rerun) and
  `samples.csv`, a copy of the Chapter 5 practice tree's
  `meta/samples_from_excel.csv` (CRLF). The supplied script (readers
  adapt it, not write it; `$1`, `$(…)`, and `basename` are Chapter 8):

  ```bash
  #!/usr/bin/env bash
  # count_lines.sh: print a file name and its number of lines
  printf "%s: %s lines\n" "$(basename "$1")" "$(wc -l < "$1")"
  ```

  Readers fix it in a fixed order, always running it **by path** until
  step 4 (*captured* end to end, bash 5.3.15, GNU coreutils/sed/grep,
  macOS 15 Intel):

  1. `./bin/count_lines.sh samples.csv` → `Permission denied`, exit 126.
  2. `chmod u+x bin/count_lines.sh`, same command → `env: bash\r: No
     such file or directory`, exit 127 (macOS `/usr/bin/env`; Linux
     prints `/usr/bin/env: 'bash\r': No such file or directory`, *to
     capture*).
  3. `sed -i 's/\r$//' bin/count_lines.sh`, same command →
     `samples.csv: 7 lines`.
  4. From `~`, by name: `count_lines.sh ~/bioinf-computing-ch07/samples.csv`
     → `count_lines.sh: command not found`, exit 127; then `export
     PATH="$HOME/bioinf-computing-ch07/bin:$PATH"` for this terminal,
     and it prints (exact) `samples.csv: 7 lines`.

  **The CSV is a separate sub-check**, because the line count cannot see
  CRLF (`wc -l` counts newlines: 7 before and after). Before the fix
  `grep -c ',30$' samples.csv` → `0` and `grep -c $'\r' samples.csv`
  → `7`; after `sed -i 's/\r$//' samples.csv` they give **`2`** and
  `0` (*captured*). After the fix `grep -c $'\r'` exits with status
  **1** (`echo $?`): grep found no matching lines, which is the expected
  result, not a failure (a bridge to Chapter 8's `set -e`). Not `file`:
  for this file it says only `CSV text`, before and after, see §10.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Read a permission string such as `-rw-r--r--` or `drwxr-x---`, say
   who may read, change, or enter, and change it with `chmod`.
2. Make a script run as a command with a shebang line and the
   executable bit, and explain `Permission denied` and `command not
   found` when it does not.
3. Explain how the shell finds a command through `PATH`, find which
   copy runs with `type -a`, and set environment variables for one
   command, one session, or every new terminal.
4. Find, stop, and end your own processes with Ctrl-C, `ps`, `top`, and
   `kill`, and find what is filling a disk with `df` and `du`.
5. Recognise when a command depends on GNU (Linux) or BSD (macOS)
   tools, and detect and fix Windows (CRLF) line endings.

## Sections

Same pattern as Chapters 1–4: each section opens with something readers
run or diagnose, then names the idea. Everything runs on the laptop in a
scratch folder, `~/bioinf-computing-ch07`, so nothing in `~/bioinf-computing` can
be damaged; the project is only read (`ls -l` on `data/raw/`, `du`).
Named exceptions outside scratch: the deliberate `~/.bashrc` lines in
§6 and exercise 4 (backed up first, to a dated name such as
`~/.bashrc.bak-ch07` with `cp -n`, so a second practice run never
overwrites the first backup; site-provided lines kept; tested in a
fresh terminal), and notes in `NOTEBOOK.md`. Cluster differences get a
short paragraph where they matter. Visual items in brackets are
specified under *Visuals and teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   Chapters 1–4 asked readers to run several "system" commands on
   trust (the `~/.bash_profile` block, `chmod a-w`, `pixi run`); this
   chapter explains what they did, so that when one goes wrong readers
   know where to look. Setup: `mkdir -p ~/bioinf-computing-ch07 && cd
   ~/bioinf-computing-ch07`. The Chapter 5 practice tree
   (`~/bioinf-computing-ch05/share/`, built by Chapter 5's paste block and
   reused in Chapters 5–8) is used read-only in §8 and §10; a reader
   who skipped it reruns that block (linked).
2. **Who may do what: users, groups, permissions.** *Start hands-on:*
   `whoami`, `id` (user, primary group, all groups), then `ls -ld
   ~/bioinf-computing/data/raw` and `ls -l
   ~/bioinf-computing/data/raw` from Chapter 3: `dr-xr-xr-x` and
   `-r--r--r--`. *Then name the parts* with `fig-permission-string`:
   type letter (Chapter 5) + three triplets for **user** (owner),
   **group**, **other**, each `r`, `w`, `x` or `-`. On a file: read
   contents, change contents, run it. On a **folder** the same letters
   mean something else: `r` list the names, `w` add, remove, or rename
   entries, `x` (search) look up entries, go inside, and pass through
   to things below. *Captured* with plain GNU `ls` (no alias:
   `\ls` or `command ls`, since a colour alias can also read file
   details and change the result) on a folder `d` set to `644` (owner
   `r` and `w`, no `x`):

   | Command | Result |
   |:--------|:-------|
   | `ls d` | lists the name `f`: `r` is enough to read names |
   | `ls -l d` | `ls: cannot access 'd/f': Permission denied`, and `-????????? ? ? ? ? ? f` |
   | `cat d/f` | `cat: d/f: Permission denied`, although `f` is readable |
   | `cd d` | `cd: d: Permission denied` |

   So `r` reads the list of names; `x` is needed for anything about the
   entries themselves. The three classes are **chosen, not added up**:
   if you own the folder, only the owner triplet counts, so an owner
   without `x` is refused even when "other" has `x` (*captured*: `655`
   folder, `cat` fails). This closes Chapter 3's surprise: `rm` changes
   the **folder's** list of entries, so it needs `w` **and** `x` on the
   folder (and `x` on every folder above it), not any permission on the
   file (*captured*: a `600` folder, `w` without `x`, refuses `rm`).
   Misconception `readonly-cant-delete`, now explained (its probe is
   extended, see *Misconceptions*). *Creating vs changing:* writing into
   an **existing** writable file works even in a folder without `w`
   (*captured*: `echo new > r/f` in a `555` folder succeeds, `echo x >
   r/new` fails), because only a new entry changes the folder. That is
   why Chapter 3 protected the files **and** the folder, and why a
   redirect into `data/raw/` is refused: onto an existing raw file by
   the file's missing `w`, as a new file by the folder's. One sentence
   of honesty: these are ordinary local permissions; on clusters, ACLs
   and the sticky bit (below) can also explain a refusal, and a
   filesystem mounted without execute rights can refuse `./script` with
   `Permission denied` whatever its bits say (ask the help desk; no ACL
   tutorial). *Then change them with `chmod`:* symbolic form
   first (`u`/`g`/`o`/`a`, `+`/`-`/`=`, `r`/`w`/`x`), recalling Chapter
   3's `chmod a-w` and Chapter 2's `chmod 700 ~/.ssh`; then the octal
   form as a shortcut readers will meet in documentation (`r=4, w=2,
   x=1`, one digit per triplet; `644`, `755`, `700`, `600`, worked from
   the figure; *captured* with GNU `stat -c '%A %a %n'`: `-rw-r--r-- 644`,
   `-rwxr--r-- 744`). Symbolic changes (`u+x`, `g+rX`) **modify** the
   current mode, so their octal result depends on where you started;
   octal sets the whole mode. Chapter 3's `555`/`444` are the result of
   `a-w` on its starting modes (`755`/`644` with `umask 0022`), not what
   `a-w` always gives. `-R` for a whole tree, with a pitfall: `chmod -R
   a+x` makes every data file "executable". Capital `X` adds search
   permission to folders and execute permission to files **already
   executable for someone**; it leaves ordinary data files alone
   (*captured*: `u+X` turns a `610` file into `710`, a `600` file stays
   `600`; GNU `chmod` documentation). *Then groups and shared folders
   (cluster paragraph):* on a cluster, a project's files are shared by a
   Unix group (e.g. `/project/<name>` on SCINet, `/work/<group>` on
   Nova; details in Appendix A); readers check with `ls -ld` and `id`
   which group owns a folder and whether they are in it. `chgrp`, the
   **set-group-ID (setgid)** bit, and the **sticky** bit are marked
   *overview*, one row each in a small table: setgid (`g+s`, an `s` in
   the group `x` place) makes new entries in the folder take the
   folder's group, but does not by itself make them group-readable (the
   new file's mode, `umask`, and any default ACLs decide that); sticky
   (`+t`, a `t` in the other `x` place, as on `/tmp`) lets only an
   entry's owner delete or rename it in a folder everyone can write.
   Usually set up by the site; when files you create are not readable
   by labmates, check the group and ask the help desk (GNU coreutils
   *Directory Setuid and Setgid* and *Mode Structure*). `umask` in one paragraph (why new files come out `-rw-r--r--`,
   `umask` printed `0022`, *captured*), no exercise. *Administrators and
   `sudo`:* on a cluster you are not an administrator and never need
   `sudo` for this book (Chapter 2's environment and Chapter 23's
   environments install into your own folders); on your laptop `sudo`
   is for system changes only, never for fixing permissions on your own
   files. [`fig-permission-string`, `fig-permission-calculator` (OJS), `tbl-permission-meaning`,
   `tbl-chmod-recipes`; key idea; pitfall: `chmod -R 777`;
   self-check]
3. **Making a script run: the executable bit and the shebang line.**
   *Start hands-on:* a one-line file `hello.sh` (`echo "hello from
   $0"`), made with nano (Chapter 2). Three attempts (*captured*, bash
   5.3):

   | Command | Result | Why |
   |:--------|:-------|:----|
   | `bash hello.sh` | `hello from hello.sh` | bash reads the file; it need not be executable |
   | `./hello.sh` | `bash: ./hello.sh: Permission denied`, exit 126 | no `x` bit |
   | `chmod u+x hello.sh`, then `./hello.sh` | `hello from ./hello.sh` | now executable |
   | `hello.sh` (no `./`) | `bash: hello.sh: command not found`, exit 127 | the current folder is not on `PATH` (§4) |

   Exit codes 126 ("found but cannot run") and 127 ("not found") join
   Chapter 4's `echo $?`. *Then the shebang line:* add `#!/usr/bin/env
   bash` as line 1, and say what it does: when the kernel runs the file,
   it reads the first line and starts that program with the file's
   name. Without a shebang, bash happens to run it as a bash script, but
   another program might not; always add one. Why `/usr/bin/env bash`
   rather than `/bin/bash` (decision for the book, see *Open
   questions*): `env` searches `PATH`, so on a Mac it finds Homebrew's
   bash 5 instead of Apple's `/bin/bash` 3.2 (*captured*: `/bin/bash
   --version` is 3.2.57), and in `pixi shell` it finds the
   environment's programs. Same pattern for R and Python scripts:
   `#!/usr/bin/env Rscript`, `#!/usr/bin/env python3` (one line each;
   Chapters 12–13). The shebang must be the very first line, starting
   at the first character. *Then one paragraph on `./`:* `.` is the
   current folder, so `./hello.sh` is a path, and paths skip the
   `PATH` search. [`fig-run-a-script` (stepped), table above as
   `tbl-run-attempts`; key idea; self-check]
4. **How the shell finds a command: `PATH`.** *Start hands-on:* `echo
   "$PATH" | tr ':' '\n'` (pipes from Chapter 6): one folder per line,
   searched top to bottom, first match wins. Then `type -a ls` on each
   OS: on a Mac after Chapter 1, two lines, GNU first (*captured*: `ls
   is /usr/local/opt/coreutils/libexec/gnubin/ls`, then `ls is
   /bin/ls`; `/opt/homebrew/…` on Apple silicon); on Linux see below.
   `type cd` → `cd is a shell builtin` (recalls Chapter 5). *Then the
   book's environment:* from `~/bioinf-computing`, `type -a seqkit`
   (nothing: `bash: type: seqkit: not found`, *to capture*) vs `pixi run
   bash -c 'type -a seqkit; echo "$PATH" | tr ":" "\n" | head -3'`: pixi
   puts `.pixi/envs/default/bin` first, for that one command (*to
   capture*). `pixi shell` does the same for a whole shell until `exit`.
   This is the explanation Chapter 2 promised, and the reason for
   Chapter 4's `command not found`. *What `PATH` covers:* the
   left-to-right search is for **external commands**. Bash checks
   aliases, functions, and builtins first, and builtins need no file on
   `PATH`; `type -a` shows all of these in order, which is why the book
   uses it. Changing `PATH` does not override an alias or function of
   the same name already defined in the shell. Expected output varies:
   on Ubuntu, `type -a ls` may show an alias (`ls is aliased to 'ls
   --color=auto'`) and both `/usr/bin/ls` and `/bin/ls`, which are the
   same file on current Ubuntu (*to capture*); the plan does not promise
   "one line on Linux". *Then the wrong copy:* if two
   seqkits are on `PATH`, the first wins, maybe an older one (Chapter
   4's forward link). Check with `type -a` and `seqkit version`; inside
   the book, `pixi run` makes the environment's copy win. On a cluster,
   `module load` changes `PATH` the same way (Chapter 10), and a module
   loaded alongside `pixi shell` can put a second copy ahead. `which`
   in one sentence: a separate lookup program, whose versions differ
   and whose answer may not match what bash will actually run; prefer
   bash's own `type -a`.
   *Then changing `PATH`:* prepend your own folder with
   `export PATH="$HOME/bin:$PATH"` (the same shape as Chapter 1's
   `gnubin` line, now explained); never replace it (`PATH=~/bin` breaks
   every command; how to recover: open a new terminal, or `export
   PATH=/usr/bin:/bin`), and never put `.` in `PATH`. Bash remembers
   where it found a command; after moving a program, `hash -r` (one
   line). [`fig-path-search` (stepped), `tbl-finding-commands`; key
   idea; misconception `installed-everywhere` revisited; self-check]
5. **Environment variables.** *Start hands-on:* `echo "$HOME"`,
   `echo "$USER"`, `echo "$SHELL"`, then `env | sort | head` (variables
   every program inherits). Then the export test (*captured*):

   ```bash
   x=1
   bash -c 'echo "child sees x=[$x]"'   # child sees x=[]
   export x
   bash -c 'echo "child sees x=[$x]"'   # child sees x=[1]
   ```

   *Then name it:* a **shell variable** lives in this shell; an
   **environment variable** (exported) is copied into every program it
   starts, including scripts, R, Python, and tools. Copies go one way,
   down to children: a script cannot change its parent's variables
   (which is why `pixi shell` starts a new shell). A second terminal
   opened separately is not a child of the first, so it does not see
   the export; a `bash` started from the first does. `SHELL` names your
   configured login shell, not necessarily the shell running now; to
   check you are in bash, use Chapter 1's `echo "$BASH_VERSION"`. Three lifetimes, in
   `tbl-variable-lifetime`: one command (`EDITOR=nano git commit`,
   `TMPDIR=/scratch/... sort ...`), this terminal (`export`), every new
   terminal (startup file, §6). *Then the variables readers will
   meet:* `HOME`, `USER`, `PATH`, `PWD`, `SHELL`, `EDITOR`, `TMPDIR`
   (where `sort` and many tools write temporary files; Chapter 29's
   `samtools sort`), `LANG`/`LC_ALL` (one line: Chapter 6's `LC_ALL=C sort`
   was one; also changes messages; Chapter 36), tool settings (`PIXI_CACHE_DIR` from Chapter
   2, `APPTAINER_CACHEDIR` in Chapter 24), and `SLURM_*` variables
   inside jobs (Chapter 10). Names are upper case by convention; spaces
   around `=` break the assignment (one example: `x = 1` → `x: command
   not found`; quoting is Chapter 8). [`tbl-variable-lifetime`,
   `tbl-common-variables`; tip; self-check]
6. **Startup files: `.bashrc` and `.bash_profile`.** *Start hands-on:*
   `shopt -q login_shell && echo login || echo "not login"` in each
   place the reader opens a shell: a new laptop terminal, VS Code's
   terminal, an SSH session, `bash` typed inside a terminal (*to
   capture* on Ubuntu, WSL, macOS, and a cluster), plus `[[ $- == *i*
   ]] && echo interactive` for the second question. *Then name it:* two
   questions decide what bash reads, **login or not** and **interactive
   or not**; which terminal app you use is only an example, and
   `shopt`/`$-` are the test. The common cases (`tbl-startup-files`,
   from the Bash manual's *Bash Startup Files*):

   | How bash starts | Reads (user files) |
   |:----------------|:-------------------|
   | Interactive login (SSH login, macOS Terminal, `bash --login`) | the **first** that exists of `~/.bash_profile`, `~/.bash_login`, `~/.profile` |
   | Interactive non-login (new Ubuntu/WSL terminal, `bash` typed in a shell) | `~/.bashrc` |
   | A script (non-interactive) | neither, unless the exported variable `BASH_ENV` names a file |
   | `ssh host command` (no login, non-interactive) | often `~/.bashrc`, under bash's remote-shell rule |

   System files (`/etc/profile` and the like) are read too; their
   details are site-specific (Appendix A). The **book's setup**, not a
   universal default: Chapter 1's macOS block makes `~/.bash_profile`
   read `~/.bashrc`, and Ubuntu's `~/.profile` does the same, so
   settings go in `~/.bashrc` and reach every interactive shell.
   `fig-startup-files` shows these routes.
   Readers now reread Chapter 1's block line by line and Chapter 2's
   pixi line in `~/.bashrc`. Check on Linux/WSL: `ls -a ~` and `grep -n
   bashrc ~/.bash_profile ~/.profile` to see which exists (Ubuntu ships
   `~/.profile`, which bash reads only if there is no `~/.bash_profile`;
   creating an empty `~/.bash_profile` silently stops `~/.profile` from
   being read: pitfall). A script that sees a variable usually
   **inherited** it from the shell that started it; that does not mean
   the script read `~/.bashrc`. *Then make Chapter 2's `EDITOR` permanent:*
   `echo 'export EDITOR=nano' >> ~/.bashrc` (note `>>` appends; `>`
   would erase the file, Chapter 6), then open a **new** terminal and
   `echo "$EDITOR"`, or `source ~/.bashrc` in the current one. *Safe
   editing rules (pitfall callout):* back up first (`cp ~/.bashrc
   ~/.bashrc.bak-ch07`, with `cp -n` so a second run keeps the first
   backup); keep one terminal open while testing in a new one; a
   `.bashrc` that prints text can break `rsync` and legacy `scp`
   (Chapter 9), because `ssh host command` may read it, so guard output
   with `[[ $- == *i* ]]`; on a cluster, keep the site's default lines,
   and do not load modules or activate environments from startup files:
   they would change every terminal and every remote command without
   you asking, and make a job's software depend on your dotfiles
   (Chapter 10 and Appendix A). If a broken startup
   file stops new terminals from working: `bash --noprofile --norc`
   gives a clean shell to fix it from. History settings (`HISTSIZE`,
   `HISTCONTROL`) as the Chapter 5 follow-up: two lines in `.bashrc`.
   Aliases in one sentence (`alias ll='ls -l'`), with the warning that
   aliases do not work in scripts. [`fig-startup-files`,
   `tbl-startup-files`; key idea; pitfall: output in `.bashrc`;
   self-check]
7. **Processes.** *Start hands-on:* `sleep 300` then Ctrl-C (the prompt
   returns; `echo $?` → 130, *to capture*). Then `sleep 300 &` (runs
   in the background; `[1] <PID>`), `jobs`, `ps` (PID, terminal, time,
   command), `kill %1` → `[1]+ Terminated sleep 300` (*captured*). Then
   `top` (or `htop` where installed), taught on each platform as it
   looks there: find the busiest process, read `%CPU` (in Linux `top`'s
   usual mode 100% = one logical CPU, so 400% ≈ four; Chapter 1's cores;
   other modes and macOS label it differently) and `RES` memory; `q`
   quits; sort by memory with `M` (Linux `top`; macOS `top -o mem`).
   *Then name it:* a **process** is a running program, with a **PID**,
   an owner, and a parent. Every external program readers have run was
   one; the shell is a process too, and runs builtins such as `cd` and
   `export` inside itself, without a new process (Chapter 5's `type
   cd`). **Foreground** vs **background**; Ctrl-C sends `SIGINT` to the
   foreground job, which normally stops it, though a program may catch
   it and clean up first; `kill <PID>`
   asks politely (`SIGTERM`, the default); `kill -9 <PID>` forces it
   (`SIGKILL`) as a last resort, since the program cannot clean up
   (half-written output files: check and delete them). Ctrl-Z
   **suspends** a process; it still holds its memory until `fg`, `bg`,
   or `kill` (pitfall; `exit` warns `There are stopped jobs.`). You can
   only signal your own processes. *Then the cluster paragraph:* do not
   rely on a command started in an ordinary SSH terminal surviving a
   disconnection; use the site's supported persistent session (tmux,
   Chapter 9) or submit the work to the scheduler, whose jobs live
   independently of your SSH window (Chapter 10). The reverse is not
   reliable either: closing a terminal does not guarantee that
   everything started from it has stopped (whether a process survives
   depends on hangup signals, shell settings, and how it was started;
   `nohup` and `disown` exist, not taught here; Bash manual *Signals*),
   so on a login node, `ps -u "$USER"`
   or `top -u "$USER"` finds leftovers to end; heavy work belongs in a
   job, and a process is not a job (Chapter 10, `run-on-login-node`
   from Chapter 1). [`fig-process-states`, `tbl-signals`; key idea;
   pitfall: Ctrl-Z; self-check]
8. **Disk usage: `df` and `du`.** *Start hands-on:* `df -h ~` (recalled
   from Chapter 1; *captured* columns `Size Used Avail Use% Mounted on`),
   then `df -h ~ ~/bioinf-computing /tmp` to see that folders can sit on
   different filesystems. Then `du -sh ~/bioinf-computing/*
   ~/bioinf-computing/.pixi | sort -h` (*to capture*); one line on
   `-h`: like Chapter 6's `sort -n`, but it understands sizes such as
   `512K`, `1.2G` (plain `-n` would put `1.2G` before `512K`). The book
   environment in `.pixi` is far larger than the data. Two different
   consumers of space: the installed environment in the project's
   `.pixi/`, and pixi's shared package **cache** (downloads, reused
   between projects). Chapter 2's `PIXI_CACHE_DIR` moves the cache to
   project storage on clusters; it does not move an existing `.pixi/`
   environment. *Then name
   it:* `df` reports a whole filesystem's space; `du` adds up what is
   inside a folder. `ls -l` on a folder shows the folder entry's own
   size (e.g. `4096`), not its contents (closes Chapter 5's forward
   mention). `du` reports space used on disk, which can differ from the
   file sizes `ls -l` adds up (one sentence, `--apparent-size`; small
   files round up to a block, and hard links or copy-on-write storage
   can make the two differ further; one caveat, no more). *Then the cluster paragraph:* `df` on
   a shared filesystem shows the whole system (petabytes), not your
   share; your limit is a **quota**, read with the site's command
   (Chapter 10, Appendix A). Quotas can count files too: `df -i` shows
   the whole filesystem's file slots (inodes), not your file-count
   quota, just as `df -h` is not your byte quota; both quotas come from
   the site's command (Chapter 10). `du` on a huge tree is slow and
   loads a shared filesystem: run it on the folder you suspect, not on
   `/`. `ncdu` mentioned as an interactive alternative where installed.
   [`tbl-disk-commands`; tip; self-check]
9. **GNU (Linux) and BSD (macOS) tools.** *Start with a diagnosis
   round:* commands that work on Linux and fail with the Mac's own
   tools, each with its real BSD output (*captured* with `/bin/bash`
   3.2 and the BSD tools, i.e. a Mac **without** Chapter 1's setup):
   `ls --version` → `ls: unrecognized option '--version'`; `cat -A
   file` → `cat: illegal option -- A`; `stat -c '%a' file` → `stat:
   illegal option -- c`; `sed -i 's/x/y/' file` → `sed: 1:
   "file": unterminated substitute pattern` (BSD `sed -i` wants a
   backup suffix and takes the script as that suffix: an especially
   confusing message). Then the same commands with GNU tools first on
   `PATH` (*captured*: `ls (GNU coreutils) 9.11`, …). *Then name it:*
   The Linux systems readers use ship **GNU** versions of the core tools
   this book uses (`ls`, `cp`, `sed`, `grep`, …; not every Linux tool is
   GNU: `ps` and `top` usually come from procps); macOS
   ships **BSD** versions, with the same names, mostly the same basic
   use, and different options and messages. Chapter 1's `gnubin` lines
   put GNU first so the book's commands work as written; `type -a` and
   `--version` tell which one you have (GNU prints a version; BSD
   tools usually reject `--version`). Where it still bites: scripts
   copied from a colleague's Mac, `#!/bin/bash` on a Mac (bash 3.2:
   `declare -A`, `mapfile` missing; one line, Chapter 8), and minimal
   containers (Alpine/BusyBox, Chapter 24) that have a third set.
   *Overview, inline:* a short table of options readers are most
   likely to meet that differ (`sed -i`, `date -d`, `stat -c`,
   `readlink -f`, `grep -P`, `sort -V`, `head -n -1`, `du
   --apparent-size`, `cat -A`). [`tbl-gnu-bsd`; tip; self-check]
10. **Line endings: LF and CRLF.** *Start hands-on:* in
    `~/bioinf-computing-ch05/share/`, the practice tree's
    `meta/samples.tsv` and `meta/samples_from_excel.csv` hold the same
    table. Ask one question of each: how many rows have 30 reads?
    (*Captured*, GNU grep 3.12, on the final tree's rows:)

    ```bash
    grep -c $'\t30$' meta/samples.tsv          # 2
    grep -c ',30$' meta/samples_from_excel.csv  # 0
    ```

    No error, and the CSV gives the wrong answer. `cat` shows nothing
    odd. `cat -A meta/samples_from_excel.csv` (Chapter 6 used it for
    tabs, `^I`; same tool, new mark) shows the reason (*captured*):

    ```
    sample,run_folder,condition,reads^M$
    sample_C,Run 3 final,treated,12^M$
    sample_A,run1,control,9^M$
    ```

    while `cat -A meta/samples.tsv` ends lines in plain `$`. Every line
    of the CSV ends in an invisible `\r` before the newline, so the
    line ends in `30\r`, not `30`. *Then the shape of the damage:* the
    `\r` sticks to the **last field only**. `cut -d, -f2` (the run
    folder) comes out clean (*captured*: `ls -d` on it works), but
    `cut -d, -f4` gives `9\r` (`printf '%q'` shows `$'9\r'`,
    *captured*), so a comparison is silently false (`[ "$f" = 9 ]` →
    different) and arithmetic fails (`$(( f * 2 ))` → `arithmetic
    syntax error: invalid arithmetic operator`, *captured*, bash 5.3).
    The same happens to a file name when it is the last column of a
    sheet (*captured* on a stand-in: `ls: cannot access
    'SRR6357070_1.fastq.gz'$'\r': No such file or directory`; GNU `ls`
    shows the hidden character as `$'\r'`, many tools print a name that
    looks right). And a script saved with CRLF fails on its first line:
    `./crlf.sh` → `bad interpreter: /bin/bash^M: No such file or
    directory` (exit 126, *captured*; with `#!/usr/bin/env bash` on
    Linux the message is `/usr/bin/env: 'bash\r': No such file or
    directory`, *to capture*).

    *How to detect it, and why not `file`:* `file` reports CRLF for
    plain text (*captured*: a two-line stand-in gave `ASCII text, with
    CRLF line terminators`; a CRLF script likewise), but for this sheet
    macOS `file` 5.41 says only `CSV text`, before **and** after the
    fix (*captured*): once libmagic recognises CSV it stops describing
    line endings (`file -e csv` shows the `CRLF` note, *captured*, but
    that flag is not worth teaching). Ubuntu/WSL's newer `file` is *to
    capture*. So the book's test is `cat -A` to look and `grep -c
    $'\r' file` to count (*captured*: 7 before the fix, 0 after);
    `od -c | head` as a byte-level alternative (Chapter 6 if taught
    there, otherwise one line). `file` stays useful for scripts and
    other text it does not classify.

    *Then name it:* Linux and macOS end lines with **LF** (`\n`);
    Windows uses **CRLF** (`\r\n`); old Mac files used CR alone (one
    sentence). CRLF is **normal and valid in CSV**, and proper CSV
    readers (R, Python; Chapter 14) handle it; what breaks is a Unix
    text command or simple parser that keeps the `\r` as part of the
    last field. Files pick up CRLF from Windows editors, Excel "Save as
    CSV", and email attachments. Under `/mnt/c` in WSL (Chapter 1's
    pitfall, now explained) it is the Windows editor or export setting
    that writes CRLF; the folder itself does not change the bytes.
    *Fix, first into a new file:* `sed 's/\r$//' samples.csv >
    samples_lf.csv`, then check with `grep -c $'\r'`; then GNU `sed -i
    's/\r$//'` in place, on a **Chapter 7 copy** only (*captured*:
    `grep -c $'\r'` then gives 0 and `grep -c ',30$'` gives 2). `tr -d
    '\r' < in > out` removes **every** CR byte, not only those at line
    ends; fine for a sample sheet, but say so. Line-ending fixes are for
    text files only, never for compressed or binary data. `dos2unix`
    where installed (not in the book
    environment; see *Open questions*). In VS Code, the status bar shows
    `LF` or `CRLF`; click to change, and set `"files.eol": "\n"` once
    (Chapter 2's editor). Git can convert line endings for you
    (`core.autocrlf`, Chapter 21). Check sample sheets with `cat -A`
    or `grep -c $'\r'` before a pipeline run (Chapter 26). One sentence on the UTF-8 BOM,
    another invisible start-of-file character from Excel (Chapter 36).
    [`fig-line-endings`, `tbl-line-endings`; pitfall; misconception
    `csv-is-csv`; self-check]
11. **Summary, exercises, further reading.** Summary as five bullets
    that mirror the learning goals; exercises (below); annotated further
    reading.

Length note: this is a long chapter (nine concept sections), taught as
two natural sittings: permissions, running scripts, `PATH`, variables,
startup files (§2–§6), then processes, disk, GNU vs BSD, line endings
(§7–§10). If the draft runs over Chapter 4's length, the compact
reference parts are the first to move into a collapsed *overview* box
rather than be cut: §9's option table, §2's setgid/sticky/`umask`
detail, §6's history settings. Never collapse something a later step
depends on just to save length.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside
a `::: {#fig-…}` div, colours from theme classes only. Colour roles
(§2): the reader's files and folders `given` (blue); allowed/fixed
`good` (green); refused or hidden characters `warn`; system text
neutral (`ink`, `line`, `muted`).

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-permission-string` | 2 | static | `drwxr-x---` and `-rw-r--r--` split into type letter + user/group/other triplets, each letter labelled; beneath, the octal digits (`750`, `644`) built from 4+2+1; a side panel "on a folder: r = list names, w = add/remove/rename (needs x too), x = look up and go inside". |
| `fig-run-a-script` | 3 | stepped (4 steps) | Typing `./hello.sh`: (1) shell sees a path, skips `PATH`; (2) kernel checks the `x` bit (no → `Permission denied`, 126); (3) kernel reads `#!/usr/bin/env bash`; (4) `env` finds `bash` on `PATH`, bash runs the file. A final frame shows the CRLF case failing at step 4 with `bash\r`. |
| `fig-path-search` | 4 | stepped (4 steps) | The `PATH` folders as a vertical list of boxes; the shell checks each for `seqkit`: (1) plain terminal, not found → 127; (2) `pixi run` adds `.pixi/envs/default/bin` on top → found; (3) a second, older seqkit in `~/bin` above it wins; (4) `type -a` lists both. |
| `fig-startup-files` | 6 | static | Four ways bash starts (interactive login; interactive non-login; script; `ssh host command`) with arrows: login → first of `~/.bash_profile` / `~/.bash_login` / `~/.profile`; non-login → `~/.bashrc`; script → none (`BASH_ENV` faint); `ssh host command` → `~/.bashrc` (dashed, "often"). The arrow "`.bash_profile` (or Ubuntu's `.profile`) reads `.bashrc`" labelled as the book's setup. |
| `fig-process-states` | 7 | static | A process's life: start → foreground ⇄ background (`&`, `bg`, `fg`), Ctrl-Z → stopped (still holding memory, `warn`), stopped → foreground (`fg`) or background (`bg`), Ctrl-C / `kill` → ended (labelled "asks"), `kill -9` → ended (forced); the shell as parent. |
| `fig-line-endings` | 10 | static | The last two lines of the practice sheet as bytes: TSV `…control\t30\n`, CSV `…control,30\r\n` with the `\r` highlighted in `warn`; below, what `cat` shows (identical) vs `cat -A` (`^M$`), and the last field a script reads (`30\r`, so `,30$` does not match) while column 2 (`run2`) is clean. |

Not used: Mermaid, screenshots (VS Code's `LF`/`CRLF` status-bar item
described in text; a small schematic only if testers miss it).

### Interactive figure (Observable JS, optional)

- **`fig-permission-calculator` (§2), decided 2026-11-17: build it in
  the first draft.** Nine checkboxes (r/w/x × user/group/other) that
  show the permission string, the octal number, and the `chmod`
  command (`u=rwx,g=rx,o=`), plus a toggle "file / folder" that
  changes the plain-language meaning of each letter (folder: `r` list
  names, `x` reach entries, `w` add/remove with `x`). Placed after
  `fig-permission-string` and the octal paragraph. Lesson in words, so
  it survives without JavaScript: the three forms (`rwxr-x---`, `750`,
  `u=rwx,g=rx,o=`) say the same thing. Follows STYLE-GUIDE §7
  *Interactive figures*: inputs in their own cells, `echo: false`,
  theme colour classes only (`given` for set bits, `muted` for unset),
  no data. Optional extra if it stays small: a "before" mode and a
  symbolic change (`g+rX`) showing the after-mode, which teaches that
  symbolic changes modify the current mode.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-permission-meaning` | 2 | Letter · on a file · on a folder · what fails without it (message) |
| `tbl-chmod-recipes` | 2 | Goal · before (`ls -l`) · symbolic · octal equivalent from that before-mode · after — rows: protect raw data (`a-w`, from `644`/`755`), make a script runnable (`u+x`, from `644`), private folder (`700`, `~/.ssh`), private key (`600`), share read-only with group (`g+rX`). Undo row: there is no general reverse command; note the original mode (`stat -c '%a'`) before changing, and set it back with octal |
| `tbl-run-attempts` | 3 | Command · result · exit status · why (the four attempts above) |
| `tbl-finding-commands` | 4 | Command (`type -a`, `type`, `which`, `command -v`, `echo $PATH`, `hash -r`) · what it tells you · when to use |
| `tbl-variable-lifetime` | 5 | How set · lasts for · seen by child programs? · example |
| `tbl-common-variables` | 5 | Variable · what it holds · who uses it · chapter |
| `tbl-startup-files` | 6 | How bash starts · example · reads (with the login fallback order and `BASH_ENV`) · book's setup (the table in §6) |
| `tbl-signals` | 7 | Key or command · signal · what the program can do · when to use |
| `tbl-disk-commands` | 8 | Question · command · read which column · cluster note |
| `tbl-gnu-bsd` | 9 | Task · GNU (Linux) · BSD (macOS) · error you see on the wrong one |
| `tbl-line-endings` | 10 | System · line ending · bytes · how to see it · how to fix it |

### Code (§6)

- `filename="Terminal (laptop)"` throughout, tier 2 (shown, not run at
  render); everything cheap. Cluster-only commands (`ps -u "$USER"` on a
  login node, the site quota command) labelled `Terminal (login node)`
  and shown, not run.
- Failing commands are shown **with** captured output in `.console`
  blocks and their exit status; for the GNU/BSD round, the cause is in
  a collapsed answer so readers diagnose first (as in Chapter 4 §3).
- Outputs that depend on OS are given for Linux first, macOS in a
  tabset only when they differ (`type -a ls`, `top` keys, `stat`). No
  zsh variants (book decision).
- User names, groups, and PIDs in captures replaced consistently:
  `you`, `yourgroup`, PIDs kept as numbers (they are not private) but
  marked "yours will differ".
- CRLF files (the Chapter 5 tree's `samples_from_excel.csv`, `crlf.sh`,
  exercise 1's script) must keep their CRLF bytes through Quarto and git: serve them
  as downloads from `exercises/ch07/` with a `.gitattributes` rule
  (`exercises/ch07/* -text`), or have readers create them with
  `printf '…\r\n'` (simpler, no download; preferred, see *Open
  questions*). Check the rendered page's code blocks contain no `\r`.
- Never show `chmod -R 777` as something to run; it appears only in
  the pitfall as text.

### Plots

None.

### Animation (manim)

None. The two stepped SVGs cover the sequences (running a script,
searching `PATH`).

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | On a folder, `r` lists names, `x` lets you reach the entries, and `w` together with `x` lets you add, remove, or rename them; a file's own permissions do not protect it from deletion |
| 2 | Pitfall | `chmod -R 777` "fixes" a permission error by letting everyone change or delete your files; find which bit is missing instead |
| 3 | Key idea | A command runs as a program if the shell can find it (a path, or a folder on `PATH`), it has the `x` bit, and its first line names an interpreter that exists |
| 4 | Key idea | The shell searches `PATH` left to right and runs the first match; `type -a` shows every match in order |
| 4 | Misconception | "Once I install a tool, it works in every terminal" (`installed-everywhere`, from Chapter 2): now with the mechanism |
| 5 | Tip | Set a variable for one command by writing it in front: `TMPDIR=/scratch/you sort big.txt` |
| 6 | Pitfall | A `.bashrc` that prints text can break `rsync` and legacy `scp`; back up before editing (without overwriting an older backup) and test in a new terminal |
| 7 | Pitfall | Ctrl-Z does not stop a program for good; it pauses it, still holding memory |
| 7 | Misconception | `closing-tab-ends-session` (from Chapter 2) revisited: do not rely on a command surviving a closed window or dropped SSH connection, nor on closing it to stop everything; use tmux (Chapter 9) or a job (Chapter 10) |
| 9 | Tip | `--version` is a quick test: GNU tools answer, BSD tools usually refuse |
| 10 | Pitfall | Files from Windows or Excel can end lines in CRLF; check with `cat -A` (look for `^M`) before a script reads them |

`readonly-cant-delete`, `which-is-enough`, and `csv-is-csv` are
handled in text and self-checks to stay under three callouts per
screen.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: A folder is `drwxr-xr-x` and owned by you; a file in it is
  `-r--r--r--`. Can you delete the file? (*Yes: deletion changes the
  folder, where you have `w` and `x`. `rm` asks first; `rm -f` does
  not.*)
  Second item: what does `chmod 640 notes.txt` give? (*`-rw-r-----`:
  you read and write, the group reads, others nothing.*)
- §3: `./run.sh` says `Permission denied`; `bash run.sh` works. What is
  missing? (*The `x` bit: `chmod u+x run.sh`.*)
- §4: `type -a samtools` prints two lines, `~/bin/samtools` then
  `/usr/bin/samtools`. Which runs when you type `samtools`? (*The
  first, `~/bin/samtools`.*)
- §5: You run `export THREADS=4` in one terminal, then open a second
  terminal, opened separately, and run `echo "$THREADS"`. What prints?
  (*An empty line: `export` reaches only that shell and programs it
  starts, and the second terminal is not one of them. Put it in
  `~/.bashrc` for every new terminal.*)
- §6: You added `export EDITOR=nano` to `~/.bashrc` but SSH logins to
  the cluster do not see it. What do you check? (*Which login file bash
  actually reads there, the first of `~/.bash_profile`, `~/.bash_login`,
  `~/.profile` that exists (`ls -a ~`), and whether that file reads
  `~/.bashrc` (`grep -n bashrc` on it).*)
- §7: `top` shows your `python` at `400%` CPU. How many cores is it
  using? (*About four logical CPUs, in Linux `top`'s usual display:
  100% is one.*)
- §8: `df -h /project` says 2.1P free, but your job fails with `Disk
  quota exceeded`. Why? (*`df` shows the whole filesystem; your group's
  quota is separate. Check the site's quota command.*)
- §9: A script from a colleague runs `sed -i 's/chr//' genes.bed` and
  fails on a Mac without Chapter 1's setup, with `sed: 1: "genes.bed":
  …`. Why? (*BSD `sed -i` expects a backup suffix and read the script
  as that suffix; use GNU sed, or `sed -i ''` on BSD only.*)
- §10: `cat -A samples.csv` shows `^M$` at every line end. Name one
  way it got that way and one fix. (*Saved from Excel or a Windows
  editor; `sed -i 's/\r$//' samples.csv`.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
material):

1. **Make a broken tool run (the check).** Create the supplied folder
   with one block: `printf '%s\r\n' …` writes
   `~/bioinf-computing-ch07/bin/count_lines.sh` (the script under
   *Outcome and check*, CRLF), then `chmod 644` on it so it starts
   non-executable even on a rerun; copy the practice tree's CSV with
   `cp ~/bioinf-computing-ch05/share/meta/samples_from_excel.csv
   ~/bioinf-computing-ch07/samples.csv` (a copy, so the shared tree
   stays as Chapter 8 expects). Then follow the four steps in the
   check, fixing one fault at a time from the message alone: run by
   path (`Permission denied`) → `chmod u+x`, same path (`bash\r`) →
   fix line endings, same path (works) → by name from `~` (`command
   not found`) → `bin/` on `PATH`. Then the CSV sub-check (`,30$`
   count 0 → 2, `\r` count 7 → 0, and the status 1). Record each
   message and fix in `NOTEBOOK.md`. (*Fixes: `chmod u+x`, `sed -i
   's/\r$//'` on the script and the CSV copy, `export
   PATH="$HOME/bioinf-computing-ch07/bin:$PATH"`; outputs as in the
   check.*)
2. **Read and set permissions.** In `~/bioinf-computing-ch07/perm/`, make
   `notes.txt`, `run.sh`, and a folder `private/`. Using
   `tbl-chmod-recipes`, set them to `-rw-r--r--`, `-rwxr-xr-x`, and
   `drwx------`, once with symbolic and once with octal `chmod`; check
   with `ls -l` (and `stat -c '%A %a %n'`). Then explain, from
   `ls -ld ~/bioinf-computing/data/raw`, why `rm` on a raw file fails.
3. **Which copy runs?** Make `~/bioinf-computing-ch07/fakebin/seqkit`, a
   supplied two-line script (`#!/usr/bin/env bash` and `echo "seqkit
   v0.0.1 (fake)"`); make it executable and put `fakebin` first on
   `PATH` in this terminal. Run `type -a seqkit` (resolved paths),
   `seqkit version`, and, from `~/bioinf-computing`, `pixi run bash -c
   'type -a seqkit; seqkit version'`. Which copy runs in each case,
   and why? Close the terminal to undo. (*Fake copy for bare `seqkit`,
   listed first by `type -a`; any other seqkit a reader already has
   appears below it. Under `pixi run`, pixi's folder comes first.*)
   Exercise 3 must not touch `~/.bashrc`.
4. **Make a setting permanent.** Add `export EDITOR=nano` (and, on a
   cluster, the `PIXI_CACHE_DIR` line from Chapter 2 if not already
   there) to `~/.bashrc` after a backup; prove it works in a new
   terminal and, if you have a cluster account, a new SSH login.
   Record in `NOTEBOOK.md` which startup files exist on each machine.
5. **Find and end a process; find the space.** Start `sleep 600 &`,
   find its PID with `ps` and in `top`, end it with `kill`, and confirm
   with `jobs`. Then list the five largest items in `~/bioinf-computing`
   with `du -sh … | sort -h | tail -5` and say which is the
   environment and why it is large.

## Examples and data

- Toy examples, made by readers in `~/bioinf-computing-ch07` with `printf`,
  `nano`, or `touch`: `hello.sh`, the permission practice folder, a
  fake `seqkit`, a CRLF script, exercise 1's `count_lines.sh`.
- **Chapter 5 practice tree** `~/bioinf-computing-ch05/share/` (decided in the
  Chapter 5 plan: built once by Chapter 5's paste block, reused in
  Chapters 5–8; folder name may change when Chapter 6 settles it).
  Used here read-only: `meta/samples_from_excel.csv` (CRLF, written
  with `printf '…\r\n'`) and `meta/samples.tsv` (LF) in §10 and
  exercise 1 (copied, not edited); `du -sh *` on the tree in §8 as a
  small warm-up before `~/bioinf-computing`. Optional for §2: `ls -l`
  on its `run*/` folders. Never `chmod` or `sed -i` the tree itself.
- Running dataset: read-only use of `~/bioinf-computing/data/raw/`
  (Chapter 3) for `ls -l` and `du`; the CRLF sample sheet reuses
  Chapter 3's `WT_REP1` / `SRR6357070_1.fastq.gz` names. Nothing new to
  download, so no new rows in `data/README.md`.
- Captured outputs (2026-11-17, macOS 15 Intel; GNU = Homebrew bash
  5.3.15 + coreutils 9.11; BSD = `/bin/bash` 3.2.57 + system tools):
  - `./hello.sh` without `x` → `Permission denied`, exit 126; with `x`
    → `hello from ./hello.sh`; by name → `hello.sh: command not found`,
    exit 127.
  - CRLF script with `#!/bin/bash` → `./crlf.sh: /bin/bash^M: bad
    interpreter: No such file or directory`, exit 126.
  - Folder `d` at `644` (owner `r`, `w`, no `x`), plain GNU `ls` 9.11
    without aliases: `ls d` → `f` (exit 0); `ls -l d` → `ls: cannot
    access 'd/f': Permission denied` and `-????????? ? ? ? ? ? f` (exit
    1); `cat d/f` → `cat: d/f: Permission denied`; `cd d` → `cd: d:
    Permission denied`. Folder at `655` (owner no `x`, others `x`):
    `cat` still refused. Folder at `600` (`w` without `x`): `rm` refused.
    Folder at `555`: `echo new > r/f` onto an existing writable file
    succeeds; `echo x > r/new` → `Permission denied`.
  - `chmod u+X`: a `610` file → `710`; a `600` file stays `600`.
  - Exercise 1 end to end (supplied script, final CSV rows): by path
    without `x` → `Permission denied`, 126; with `x` → `env: bash\r: No
    such file or directory`, 127 (macOS `/usr/bin/env`); after `sed -i`
    → `samples.csv: 7 lines`; by name from `~` → `command not found`,
    127; with `bin/` on `PATH` → `samples.csv: 7 lines`. CSV: `,30$`
    0 → 2, `\r` 7 → 0, `grep -c $'\r'` status 1 after the fix.
    Rewriting an executable file with `printf >` keeps its `x` bit (so
    the setup's `chmod 644` is needed).
  - `kill -INT` on a bash process → exit status 130 (Ctrl-C's status;
    the interactive Ctrl-C itself still *to capture*).
  - `umask` → `0022`; GNU `stat -c '%A %a %n'` → `-rwxr--r-- 744`,
    `-rw-r--r-- 644`, `drwxr--r-- 744`.
  - `file`: a two-line comma stand-in → `ASCII text, with CRLF line
    terminators`; the final tree's `samples_from_excel.csv` → `CSV
    text` before and after the fix (macOS `file` 5.41; `file -e csv` →
    `ASCII text, with CRLF line terminators`); `samples.tsv` → `ASCII
    text`.
  - Final tree (rows from `chapter_05.md`): GNU `cat -A` → `…,reads^M$`,
    `sample_C,Run 3 final,treated,12^M$`; `wc -l` → 7; `grep -c ',30$'`
    → 0 (CSV) vs `grep -c $'\t30$'` → 2 (TSV); `cut -d, -f2` clean;
    `cut -d, -f4` of row 3 → `$'9\r'`; `[ "$f" = 9 ]` false; `$(( f *
    2 ))` → `arithmetic syntax error: invalid arithmetic operator`;
    `grep -c $'\r'` → 7, and 0 after `sed -i 's/\r$//'` (then `grep -c
    ',30$'` → 2).
  - Stand-in with the file name in the last column: GNU `ls` →
    `ls: cannot access 'SRR6357070_1.fastq.gz'$'\r': No such file or
    directory`, exit 2; `printf '%q'` → `$'SRR6357070_1.fastq.gz\r'`.
  - BSD: `ls --version` → `ls: unrecognized option '--version'`;
    `cat -A` → `cat: illegal option -- A` + usage; `stat -c` →
    `stat: illegal option -- c` + usage; `sed -i 's/x/y/' samples.csv`
    → `sed: 1: "samples.csv": unterminated substitute pattern`, exit 1.
  - `type -a ls` (Mac, GNU first) → gnubin `ls`, then `/bin/ls`;
    `type cd` → `cd is a shell builtin`.
  - Export test → `child sees x=[]`, then `child sees x=[1]`.
  - `sleep 300 &` then `kill %1` → `[1]+  Terminated: 15  sleep 300` on
    macOS bash (Linux prints `Terminated`; *to capture*).
  - `df -h .` header `Filesystem Size Used Avail Use% Mounted on`.
- To capture on Ubuntu/WSL and a cluster login node: the `env bash\r`
  message; `type -a seqkit` outside and inside `pixi run`; `pixi run`'s
  `PATH` head; `shopt -q login_shell` in each kind of shell, including
  VS Code Remote-SSH and Open OnDemand terminals; Ubuntu's default
  `~/.profile` / `~/.bashrc` lines; `ps` and `top` columns and keys;
  Ctrl-C exit status 130; `du -sh` of `.pixi` and `data/` on each OS;
  `df -h` on a cluster `/project` and the site quota command (Appendix
  A); `file` on the practice tree's CSV with Ubuntu/WSL's newer
  libmagic (macOS 5.41 says only `CSV text`). (GNU grep's `,30$` count
  is now captured with Homebrew's `ggrep` 3.12; the test Mac's plain
  `grep` is ugrep.)
- Where commands run: laptop; cluster paragraphs labelled login node.

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters), to add when this plan is agreed. Existing entries
revisited here get `07-linux-system` added to their `chapters` list:
`readonly-cant-delete` (Chapter 3), `installed-everywhere` (Chapter 2),
`closing-tab-ends-session` (Chapter 2), `need-sudo-to-install`
(Chapter 2), `run-on-login-node` (Chapter 1).

- No new `file-perms-protect-delete` entry: it duplicates
  `readonly-cant-delete`, which already lists `07-linux-system`. Extend
  that entry's reality instead: "Deleting, moving, and adding files
  change the folder, so they need `w` and `x` on the folder; the
  file's own permissions do not matter. Protect the folder as well as
  the files." Add a second probe: a folder you own is `drwxr--r--`
  (no `x`); can you `cat` a readable file inside it? (No: without `x`
  you can list names but not reach the entries.) [text and self-check,
  §2]
- `chmod-777-fixes`: "When I get `Permission denied`, `chmod 777` (or
  `sudo`) is the fix." It removes protection for everyone and hides
  which bit was missing; read the permission string and change only
  that bit. On a cluster, `sudo` is not available. [pitfall, §2]
- `script-needs-bash`: "To run a script I must type `bash script.sh`."
  With a shebang and the `x` bit it runs as a command, and on `PATH`
  it runs by name; `bash script.sh` ignores the shebang (a Python
  script run that way fails). Probe: `bash plot.py` with
  `#!/usr/bin/env python3` on line 1: what happens? (bash tries to run
  Python code as shell and fails.) [text, §3]
- `which-is-enough`: "`which` tells me exactly what will run." `which`
  is a separate program whose versions differ, and its answer may not
  match bash's: aliases, functions, and builtins come before `PATH`.
  bash's `type -a` shows what bash will run, in order. [text, §4]
- `export-is-permanent`: "Once I `export` a variable, it stays set."
  It lasts for this shell and the programs it starts; new terminals
  need it in `~/.bashrc`. [self-check, §5]
- `csv-is-csv`: "A CSV file is a CSV file; where it was saved doesn't
  matter." Line endings (and a BOM) depend on the program and OS that
  saved it, and an invisible `\r` sticks to the last field of every line, so
  matches and comparisons on it fail silently.
  Probe: a sample sheet looks right in `cat`, but the pipeline says a
  listed file does not exist; first check? (`grep -c $'\r' samples.csv` /
  `cat -A`.) [pitfall + self-check, §10; also Chapter 14]

## Links to other chapters and books

- Builds on: Chapters 1–4 (see *What this chapter builds on*), Chapter
  5 (`ls -l` fields, paths, `type cd`, `file`), Chapter 6 (pipes,
  `>`/`>>`, `sort`, `sed`).
- Leads to: Chapter 8 (scripts: shebang and `x` bit assumed, exit
  statuses, `set -euo pipefail`, variables and quoting; bash 3.2 on
  macOS); Chapter 9 (`.bashrc` output breaking `scp`/`rsync`; tmux so
  processes survive; `chmod 600` keys); Chapter 10 (`module load`
  changing `PATH`, `SLURM_*` variables, a process vs a job, quotas and
  inode limits, `TMPDIR` on compute nodes); Chapter 14 (CRLF and BOM in
  tables read by R and Python); Chapter 21 (`core.autocrlf`, the `x`
  bit in git); Chapter 23 (how environments change `PATH`; caches and
  `$HOME`); Chapter 24 (containers' own `PATH` and minimal tools);
  Chapter 26 (checking sample sheets before a run); Chapter 29
  (`TMPDIR` and `samtools sort`); Chapter 35 (`top` and `%CPU` when
  testing thread counts); Chapter 36 (text encodings, BOM, `LANG`);
  Appendix A (site groups, project folders, default dotfiles, quota
  commands).

## Official links to include

- GNU Bash manual: *Bash Startup Files*, *Environment*, *Job Control*
  (gnu.org/software/bash/manual)
- GNU coreutils manual: `chmod`, `ls` (file permissions), `df`, `du`,
  `stat`, *File permissions* chapter (gnu.org/software/coreutils/manual)
- Linux man-pages project (man7.org): `chmod(1)`, `signal(7)`,
  `environ(7)`, `execve(2)` (shebang lines, for the curious), `ps(1)`,
  `top(1)`
- FreeBSD manual pages (man.freebsd.org) for background on BSD `sed`
  and `stat` only. They are not an exact specification of Apple's
  tools: the man pages installed on the Mac (`man sed`) are the
  authority for macOS behaviour, and the book's BSD outputs come from
  captures on a Mac
- VS Code docs: line endings / `files.eol` setting
  (code.visualstudio.com/docs)
- Microsoft WSL docs: *Working across file systems* (already linked in
  Chapter 1)
- Git docs: `gitattributes` / `core.autocrlf` (git-scm.com), as a
  pointer to Chapter 21
- pixi docs: `pixi shell` / `pixi run` and how activation sets `PATH`
  (pixi.sh)
- Site docs via Appendix A: SCINet and ISU Nova pages on groups,
  project storage, and startup files

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Verify each with
scite or the publisher, and fetch BibTeX from the DOI or official page,
before adding.

- Shotts, *The Linux Command Line* (No Starch, 2nd ed.; free online
  edition at linuxcommand.org): chapters on permissions, processes,
  the environment, and startup files map onto §2–§7 one to one. A
  recurring anchor for Part II.
- Software Carpentry, *The Unix Shell* (swcarpentry.github.io; Zenodo
  DOI to fetch for the current release): its episodes stop before
  permissions and `PATH`, so cite it here only for its
  *Shell scripts* episode as the bridge to Chapter 8, or drop.
- GNU Bash manual, *Bash Startup Files* section: short, authoritative
  answer to "which file does my shell read?" (url + urldate).
- Robbins, *Bash Pocket Reference* (O'Reilly) or the GNU coreutils
  manual as a desk reference: pick one; the free manual is preferable
  for this audience.
- Candidate journal piece, to search with scite: a *PLoS Comput Biol*
  "Ten simple rules" on working with HPC or the command line, if one
  covers environments and permissions well; otherwise none.

## Austin's notes

-

## Coordination (2026-11-17)

Chapters 5 and 6 were being planned in parallel. A message to both
sessions listed what this chapter claims. The Chapter 5 session
replied: its plan names the `ls -l` fields but leaves the permission
column here; uses `type cd`/`type ls` only for builtin vs program;
mentions Ctrl-C in one line; uses `file` only to spot binary files;
gives `du` and `.bashrc` history settings forward links only; recalls
`chmod a-w` without explaining it; no `find -perm`, `umask`, groups, or
executable bit. This plan matches that. The Chapter 6 session replied that its plan
claims none of this chapter's items (details under *What this chapter
builds on*); §2 can now explain its `Permission denied` on a redirect
into `data/raw/` (onto an existing raw file the file's missing `w`
refuses it; a new file is refused by the folder's missing `w`;
corrected after the Codex review), and §10 reuses its `cat -A`
with `^M` in place of `^I`. It confirmed that Chapter 6 does not teach `sort -h`, so §8
explains it in one line and links back to Chapter 6 for `sort`.

Later message from the Chapter 5 session: Austin decided the Chapter 5
practice tree (`~/bioinf-computing-ch05/share/`) is reused in Chapters 5–8, and
it includes `meta/samples_from_excel.csv` (CRLF) for this chapter. §10
and exercise 1 now use it instead of a file of their own; captures
made on stand-in files must be redone on the final tree.

Then the Chapter 5 session reported that macOS `file` 5.41 calls the
final CSV only `CSV text`. Rechecked here and confirmed (also after the
fix). Recapturing on the final rows showed a second problem with this
plan: the `\r` sticks only to the **last** field, so `cut -d, -f2`
(run folder) is clean and the planned `ls` failure would not happen.
§10 now opens with a silent wrong count (`grep -c ',30$'` → 0, TSV → 2),
detects CRLF with `cat -A` and `grep -c $'\r'`, and explains why
`file` is not the test; the check and self-check §10 changed to
match.

## Review responses (2026-11-17)

Codex (`chapter_07_codex_review.md`). Every testable point was rechecked
here before changing the plan (bash 5.3.15, GNU coreutils 9.11, GNU sed,
GNU grep 3.12, macOS 15 Intel, plain commands without aliases): the
folder-permission table, class selection (`655`), `w` without `x`
refusing `rm`, writing into an existing file in a `555` folder, `u+X`
on `610` and `600`, `printf >` keeping the `x` bit, grep's status 1
after the CRLF fix, `tr -d '\r'` removing a mid-line CR, and exercise
1's supplied script and four-step sequence end to end. The startup-file
and signal rules were checked against the Bash manual. All six
corrections accepted:

1. **Folder permissions:** §2 now teaches `r` = list names, `x` =
   reach entries, with the captured table (`ls d` works, `ls -l d`,
   `cat`, `cd` fail); deletion needs `w` **and** `x` on the folder;
   classes are chosen, not added up; creating vs changing an existing
   file; one sentence on ACLs, sticky bit, and no-exec mounts.
   `file-perms-protect-delete` dropped in favour of extending
   `readonly-cant-delete`.
2. **Capital `X` and setgid:** `X` wording corrected (folders, and files
   already executable for someone); "group-sticky" replaced by
   set-group-ID, with the sticky bit as a separate row; setgid does not
   by itself grant group access. `tbl-chmod-recipes` now has a
   before-mode column and an honest undo row; Chapter 3's `555`/`444`
   described as the result from its starting modes.
3. **Startup files:** login vs interactive as two questions; the login
   fallback order (`.bash_profile`, `.bash_login`, `.profile`);
   scripts read neither unless `BASH_ENV`; `ssh host command` often
   reads `.bashrc`; `.bash_profile` reading `.bashrc` named as the
   book's setup; self-check §6 inspects the file actually read;
   inherited variables do not prove a script read `.bashrc`; module
   advice and the "prints text" pitfall reworded (`rsync`, legacy
   `scp`).
4. **Processes:** the "closing ends everything" claim replaced with the
   reliability rule (tmux or a job; closing is not a reliable stop
   either); builtins run inside the shell; Ctrl-C sends `SIGINT`,
   which a program can catch; `fig-process-states` shows stopped →
   `fg`/`bg`; the `closing-tab-ends-session` callout reworded.
5. **Exercise 1:** the script is supplied, the setup sets mode `644`,
   the four steps run by path until the last, exact outputs captured;
   the CSV is a separate sub-check (`,30$` 0 → 2, `\r` 7 → 0, status 1
   as the expected "no match").
6. **`PATH` and variables:** `PATH` search is for external commands
   (aliases, functions, builtins first; an alias is not overridden by
   `PATH`); `SHELL` is the login shell, not the running one; a
   separately opened terminal does not inherit an export; `type -a ls`
   on Ubuntu may show an alias and two paths; `which` described as a
   separate program whose answer may differ; the fake-seqkit exercise
   uses a supplied script and shows resolved paths.

Teaching suggestions also adopted: CRLF is valid CSV, the failure is in
text tools; `/mnt/c` does not change bytes; fix into a new file first,
`sed -i` on a Chapter 7 copy, `tr -d '\r'`'s limitation stated; `.pixi`
environment vs pixi cache; `df -i` is not a quota; "the GNU tools this
book uses" (procps for `ps`/`top`); macOS man pages, not FreeBSD's, are
the authority; `top` percentages labelled by display; two sittings and
"never collapse a prerequisite" in the length note; named exceptions to
"scratch only" (`~/.bashrc`, `NOTEBOOK.md`) with non-overwriting
backups.

Not adopted: nothing.

## Decisions (2026-11-17, open questions round)

Austin's choices:

- **Shebang: `#!/usr/bin/env bash`** for every bash script in the book
  (Chapter 8 inherits it). Confirms what Chapter 3's
  `01_count_reads.sh` already does. Still to test while drafting:
  under `pixi run`, inside `pixi shell`, and on the clusters. R and
  Python scripts use `#!/usr/bin/env Rscript` and `#!/usr/bin/env
  python3`.
- **`dos2unix`: teach `sed`, mention `dos2unix`;** not added to the
  book environment.
- **Processes: teach `top`, mention `htop`** where installed; not added
  to the book environment.
- **Permission calculator: build it now** (`fig-permission-calculator`,
  see *Interactive figure*).
- **Length: keep all nine sections here,** including GNU vs BSD (§9),
  taught as two sittings (see the length note under *Sections*).
- **Groups and setgid on clusters: Austin runs the checks later** on
  Nova and Atlas (commands below); §2's cluster paragraph and Appendix
  A are written from those captures.

## Final review before drafting (2026-11-17)

Chapters 5 and 6 are now written (commits `fbc6c9b`, `7c0b8f7`). Their
text makes promises to this chapter that the plan did not yet cover,
so these are added:

- **Change the prompt** (Chapter 5 §2: "@sec-linux-system shows how to
  change it"): §6 gets a short paragraph: the prompt is the variable
  `PS1`; `PS1='\u@\h:\w\$ '` gives `you@laptop:~/bioinf-computing$`
  (`\u` user, `\h` host, `\w` folder); try it in one terminal, then
  put it in `~/.bashrc` if wanted. On a cluster, keep the host name in
  the prompt: it shows login node vs compute node.
- **Aliases** (Chapter 5 §2: "`type ls` may say `ls is aliased to …`.
  Aliases are @sec-linux-system"; Nova does say so, captured by Austin
  for Chapter 5): §4 explains them where `type -a ls` shows one: an
  alias is a shortcut bash expands before searching `PATH`; `alias`
  lists them; `\ls` or `command ls` runs the program without the alias.
  §6 then shows defining one in `~/.bashrc` (`alias ll='ls -l'`) and
  that aliases are not used in scripts.
- **Your locale settings** (Chapter 6 §5: "your settings are
  @sec-linux-system"): §5's `LANG`/`LC_ALL` line grows to a short
  paragraph: `locale` prints the current settings; `LC_ALL=C` for one
  command (Chapter 6) vs `export` vs `~/.bashrc`; the book does not
  change the default.
- **`noclobber` in `~/.bashrc`** (Chapter 6: "You could turn it on for
  good in your `~/.bashrc` (@sec-linux-system), but this book does
  not"): one sentence in §6, consistent with that.
- **Chapter 6's redirect into `data/raw/`**: its example
  `echo test > data/raw/notes.txt` makes a **new** file, so §2 explains
  it with the folder's missing `w`; the `sort … > data/raw/SRR…gz`
  example targets an existing file, refused by the file's missing `w`.
- **Nova facts from Chapter 5's capture** (Austin, 2026-11-17): bash
  5.1.8, GNU coreutils 8.32, `type ls` → `ls is aliased to `ls
  --color=auto'`. Used in §4's alias note and §9.
- **Readers who skipped Chapter 5:** exercise 1 and §10 need only
  `meta/samples_from_excel.csv` and `meta/samples.tsv`; the chapter
  links to Chapter 5's setup block, as Chapter 6 does.
- **Further reading:** add the GNU coreutils manual as a new `@manual`
  entry (`gnu2025coreutils`, URL and access date, no DOI, the same
  pattern as `ramey2025bash`); Software Carpentry dropped (its lessons
  stop before permissions and `PATH`).

## Chapter written (2026-11-17)

`chapters/07-linux-system.qmd` written from this plan. **Linux outputs
were captured on Ubuntu 24.04** in a Docker container (bash 5.2.21, GNU
coreutils 9.4, grep 3.11, sed 4.9, file 5.45, procps), host `laptop`,
user `you`, with a stand-in project built from the real test data
(pinned commit, checksums matching Chapter 3) and the book's
environment installed by `pixi install --locked`, plus Chapter 5's setup
block. macOS/BSD outputs captured on this Mac (macOS 15.7, `/bin/bash`
3.2.57, system tools). Choices and findings while writing:

- **New captures that changed the text:** on Ubuntu, `file` 5.45 calls
  the CRLF CSV `CSV ASCII text` (no CRLF note), so `file` is ruled out
  on Linux too. `env` with a CRLF shebang prints
  `/usr/bin/env: ‘bash\r’: No such file or directory` plus a second,
  misleading line (`use -[v]S to pass options in shebang lines`); with
  `#!/bin/bash`, bash 5.2 says only `cannot execute: required file not
  found`. Both are in §10. The arithmetic example was dropped: bash
  5.2's message prints a raw `\r` that garbles the terminal.
- **Hard links shown for real:** `du -sh ~/.cache/rattler .pixi` counts
  the shared 1.3 GB under whichever comes first (1.3G + 97M, or 1.3G +
  118M reversed); used for the one hard-link caveat in §8.
- **`type -a ls` on Ubuntu:** alias + `/usr/bin/ls` + `/bin/ls`, as the
  review predicted; `which ls` → `/usr/bin/ls`; `command -v ls` → the
  alias.
- **Normalised in captures:** dates set to Nov 17; `$USER` shown as
  `you` (empty in the container, set on a real login); `ps` output
  drops the container's extra `sh` parent line; `top` header shows `1
  user`, `0 zombie`, and only the two test processes; `df`'s first
  column shown as `/dev/sdc` (a WSL-style disk; the container showed
  `overlay`), with a sentence that the first column differs by machine.
- **GNU/BSD table trimmed** after checking macOS 15: `readlink -f`,
  `sort -h`, and `sort -V` now work on the Mac's own tools, so those
  rows were removed; `du -A`, `stat -f '%Lp'`, `cat -et`, `date -j -f`
  checked.
- **Figures:** `permission-string`, `run-a-script` (stepped, 5),
  `path-search` (stepped, 4), `startup-files`, `process-states`,
  `line-endings` in `figures/`; checked in a headless browser. The
  process figure has no direct foreground → background arrow (it goes
  through Ctrl-Z and `bg`). `fig-permission-calculator` (OJS) checked:
  renders, no errors.
- **Misconceptions:** six new entries in `misconceptions.yml`
  (`chmod-777-fixes`, `script-needs-bash`, `which-is-enough`,
  `export-is-permanent`, `closed-window-decides`, `csv-is-csv`);
  `readonly-cant-delete` extended; `07-linux-system` added to
  `need-sudo-to-install` and `run-on-login-node`. The Chapter 2 entry
  `closing-tab-ends-session` (about an Open OnDemand tab) is a different
  claim, so the terminal case got its own id.
- **References:** `gnu2025coreutils` added as an `@manual` (URL and
  access date, as `gnu2025findutils`). gnu.org did not respond from
  here, so its manual links (coreutils, Bash *Startup Files*,
  *Signals*) follow the established URL pattern and need a recheck.
  Software Carpentry dropped from further reading; the Linux man-pages
  project added.
- **Not captured:** a real SSH login and `ssh host command` (startup
  file behaviour taken from the Bash manual); cluster outputs (group
  checks above).

## Open questions

1. **Cluster group checks (Austin, on Nova and Atlas login nodes;
   only lists and makes one small file in your own project folder):**

   ```bash
   id                                   # your user, primary group, all groups
   ls -ld /work/<group> /project/<name> # whichever applies on that cluster
   cd <your project folder>             # the folder you share with the lab
   ls -ld .                             # an 's' in the group x place = setgid
   touch ch07_group_test && ls -l ch07_group_test
   umask
   rm ch07_group_test
   ```

   Record: the project folder's owner, group, and mode; whether the
   test file got the folder's group (setgid working) or your primary
   group; its mode; `umask`. Paste the output (user names can be
   replaced by `you`).
2. **To capture while drafting** (listed under *Examples and data*):
   Ubuntu/WSL and cluster outputs, including `env: 'bash\r'` on Linux,
   `type -a` with Ubuntu's `ls` alias, `shopt -q login_shell` in each
   kind of shell, `top` columns, and Ctrl-C's status 130 typed by hand.

## Codex review of the written chapter (2026-11-18)

`reviews/chapter_07_codex_review.md`. All three findings checked and
accepted:

1. **Exercise 4's `grep -n EDITOR` guard** also matched a commented-out
   or unrelated line, so the append was skipped. Now `grep -n 'EDITOR='`
   to look first, then `grep -qxF 'export EDITOR=nano' || echo … >>`.
   Tested on throwaway rc files (`# export EDITOR=vim`,
   `export VISUAL_EDITOR=vim`, unrelated): one line added after two
   runs, and a fresh `bash --rcfile` shows `EDITOR=[nano]`.
2. **`ps -o …,cmd`** fails on macOS (`ps: cmd: keyword not found`,
   status 1). Switched to `command`, which both macOS and procps accept
   (Ubuntu header `COMMAND`); capture updated, annotation notes `cmd`
   is Linux-only.
3. **`NAME=value` row**: an already-exported variable stays exported
   (`export x=1; x=2; bash -c 'echo $x'` prints `2` on macOS bash and
   Ubuntu). Table now says "no, unless already exported"; the prose
   adds that `PATH` can be changed by plain assignment for this reason.

## WSL checks applied (2026-11-20)

From Austin's WSL screenshots (Ubuntu 26.04.1, bash 5.3.9); details in
`chapter_05_06_07_checks.md`. A new WSL window (`wsl ~`) is a **login**
shell; VS Code's WSL terminal is not, so §6's text, `tbl-startup-files`,
and `fig-startup-files` were corrected. Also: `logout` before the
stopped-jobs refusal in login shells; real `df` line (`/dev/sdd`); the
`cp -n` warning on Ubuntu; Excel's CSV UTF-8 byte order mark in §10.
Block B's output (coreutils flavour, sort order under `C.UTF-8`) still
to come.
Block B arrived (`blockB-WSL.txt`): Ubuntu 26.04's core tools are
**uutils coreutils 0.8.0** (GNU kept for `cp`, `mv`, `rm`, `df`; grep
and sed GNU). Added a uutils paragraph to §9 with the release-notes
link, the uutils `env` and bash 5.3 CRLF messages (`bad interpreter`,
status 126), the missing `cannot access` line from `ls -l` in §2, and
`-bash:` in login shells. Chapter 6 notes WSL's `C.UTF-8` sorts like
`C`. Not done: telling readers to switch to GNU coreutils (needs
`--allow-remove-essential`): Austin decided 2026-11-20 to keep Ubuntu's default (book `CLAUDE.md`).
