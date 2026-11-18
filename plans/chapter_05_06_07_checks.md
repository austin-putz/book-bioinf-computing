---
title: "Chapters 5–7: Hands-on checks for Austin"
subtitle: "What to run on WSL, Nova, SCINet (Atlas, Ceres), an Apple silicon Mac, and in a browser"
date: 2026-11-18
---

These are the checks Chapters 5, 6, and 7 still need from machines I
can't reach from here. They come from the *Open questions* and *Not
captured* notes in `chapter_05.md`, `chapter_06.md`, and
`chapter_07.md`, plus one claim I now doubt (WSL login shells, below).

**What is already done**, so you don't repeat it:

- **macOS (Intel):** every Mac output in the three chapters was
  captured on this Mac.
- **Ubuntu 24.04:** Chapter 7's Linux outputs were captured in a Docker
  container (bash 5.2.21, coreutils 9.4, file 5.45). A container can't
  show what a real terminal window does at startup, so WSL is still
  needed for that.
- **Nova, Chapter 5 part:** captured by you on 2026-11-17. That covers
  `pwd`, `type ls`, bash 5.1.8, coreutils 8.32, `zless`, `LESSOPEN`,
  and bash-completion. Don't redo those on Nova.

**How to work.**

- Each machine has its own part. Do them in any order and skip what
  you can't do yet.
- Everything runs in a throwaway folder, `~/bioinf-computing-checks`.
  Delete it at the end with `rm -r ~/bioinf-computing-checks`.
- Nothing here edits a startup file. Exercise 4 (Part 2.5) is the one
  place you add a line to `~/.bashrc`, and it makes a backup first.
- On a cluster, all of this is light enough for a login node: a 2 MB
  download and some tiny files. No jobs are needed.
- **Recording:** Block B writes its output to a file. For everything
  you type by hand, copy what the terminal shows into the matching
  file, or paste it into the chat. Replace your user name with `you`
  and group or project names with `<group>` if you prefer.

**Priority** if time is short:

1. WSL Part 1.1, the login-shell check.
2. The cluster group checks, Part 2.3.
3. Exercise 4 over SSH, Part 2.5.
4. Everything else.

---

## The two shared blocks

Most parts run the same two blocks. They are written out once here.

### Block A: type these into the terminal by hand

These lines must run in the shell you are typing into, not in a
script. Aliases and the "interactive" flag only exist there. Paste
them in one go:

```bash
echo "$BASH_VERSION"
shopt -q login_shell && echo login || echo "not login"
[[ $- == *i* ]] && echo interactive || echo "not interactive"
ps -o pid,args -p $$
type -a ls
which ls
command -v ls
ls -a ~ | grep -E '^\.(bash|profile)'
grep -n bashrc ~/.bash_profile ~/.bash_login ~/.profile 2>/dev/null
locale | head -n 6
echo "LESSOPEN=[$LESSOPEN]"
type zless
umask
df -h ~
```

**Record:** the whole output.

What each line checks:

- **Lines 2–4** test Chapter 7 §6's claims about which kind of shell a
  new terminal is. A login shell shows as `-bash`, with a leading dash,
  in the `ps` line.
- **`type -a ls`, `which`, `command -v`** check Chapter 7 §4's alias
  output.
- **The two `grep`/`ls` lines** show which startup files exist and which
  one reads `~/.bashrc`. They are the same as Exercise 4's.
- **`locale`** is for Chapter 6's sort order and Chapter 7 §5.
- **`LESSOPEN` and `zless`** cover Chapter 5 §9.
- **`umask`** is for Chapter 7 §2.
- **`df -h ~`** shows the first column of `df` on this machine. Chapter 7
  §8 shows `/dev/sdc`, which is my guess for WSL.

### Block B: paste this; it saves everything to a file

This is one paste. It makes the throwaway folder, downloads one test
file from the book's pinned commit (2.2 MB), and writes all output to
`~/bioinf-computing-checks/blockB-<machine>.txt`.

```bash
mkdir -p ~/bioinf-computing-checks && cd ~/bioinf-computing-checks && {
h() { printf '\n=== %s\n' "$*"; }
h machine
hostname -s; grep PRETTY_NAME /etc/os-release
h versions
echo "bash $BASH_VERSION"
for t in ls grep sed gzip env sort; do $t --version 2>&1 | head -n 1; done
file --version 2>&1 | head -n 1
ps --version 2>&1 | head -n 1

h "ch05: echo .* (bash 5.2+ shows only .old_settings)"
mkdir -p glob && touch glob/.old_settings glob/a.txt
(cd glob && echo .*)

h "ch06: sort order, default locale then LC_ALL=C"
printf '%s\n' WT_REP1 sample RAP1_UNINDUCED_REP2 RAP1_IAA_30M_REP1 | sort
echo ---
printf '%s\n' WT_REP1 sample RAP1_UNINDUCED_REP2 RAP1_IAA_30M_REP1 | LC_ALL=C sort

h "ch06: redirect into a read-only file"
printf 'x\n' > ro.txt && chmod 444 ro.txt
echo y > ro.txt; echo "status $?"
rm -f ro.txt

h "ch06: test file, then PIPESTATUS after head"
[ -f SRR6357070_1.fastq.gz ] || curl -fsSL -o SRR6357070_1.fastq.gz \
  https://raw.githubusercontent.com/nf-core/test-datasets/9dd6d014f560e182047992834a8d267214fbccd1/testdata/GSE110004/SRR6357070_1.fastq.gz
md5sum SRR6357070_1.fastq.gz
gunzip -c SRR6357070_1.fastq.gz | head -n 8 > /dev/null
echo "PIPESTATUS ${PIPESTATUS[*]}"

h "ch06: truncated file, line count and statuses"
head -c 1000000 SRR6357070_1.fastq.gz > broken.fastq.gz
gunzip -c broken.fastq.gz | wc -l
echo "PIPESTATUS ${PIPESTATUS[*]}"

h "ch07: CRLF script with the env shebang"
printf '%s\r\n' '#!/usr/bin/env bash' 'echo "hello"' > crlf_env.sh
chmod +x crlf_env.sh
./crlf_env.sh; echo "status $?"

h "ch07: CRLF script with #!/bin/bash"
printf '%s\r\n' '#!/bin/bash' 'echo "hello"' > crlf_bin.sh
chmod +x crlf_bin.sh
./crlf_bin.sh; echo "status $?"

h "ch07: file and grep on Chapter 5's CRLF sample sheet"
rows=(sample run_folder condition reads
  sample_C "Run 3 final" treated 12
  sample_A run1 control 9
  sample_B run2 control 30
  sample_E run5 treated 105
  sample_B run2 control 30
  sample_D run4 control 8)
printf '%s,%s,%s,%s\r\n' "${rows[@]}" > samples_from_excel.csv
file samples_from_excel.csv
grep -c $'\r' samples_from_excel.csv
grep -c ',30$' samples_from_excel.csv

h "ch07: folder without x (owner), then with it again"
mkdir -p permtest && touch permtest/f && chmod 644 permtest
ls permtest; ls -l permtest; cd permtest 2>&1
chmod 755 permtest

h "ch07: ps -o with command"
sleep 30 &
ps -o pid,stat,rss,command
kill %1
} 2>&1 | tee ~/bioinf-computing-checks/blockB-$(hostname -s).txt
```

**Record:** keep the file `blockB-<machine>.txt`. Copy it to your laptop
with `scp` (Chapter 9) or paste its contents into the chat.

The expected values are the Mac/Ubuntu ones in the chapters. Expected
MD5 for the test file is `d19f3c7a8b4016fa641458257b99a1a1`. The
truncated count was 89,515 with GNU gzip 1.15 on the Mac. A different
number is fine; it gets noted beside the output.

### Block C: interactive bits (Ctrl-C, Ctrl-Z, top)

These need you to press keys.

```bash
sleep 30
```

Press **Ctrl-C**, then:

```bash
echo $?
```

**Record:** the number. Chapter 7 says `130`.

```bash
sleep 600
```

Press **Ctrl-Z**, then paste:

```bash
jobs
ps -o pid,stat,rss,command
exit
```

The `exit` should be refused with "There are stopped jobs."

**Record:** all of it. Then clean up:

```bash
kill %1
jobs
```

`jobs` should show `Terminated` (Linux) after you press Enter once more.

```bash
top -u "$USER"
```

**Record:** the top five lines (the header) and the column names, or
take a screenshot. Quit with `q`.

---

## Part 1: WSL (Windows PC, Ubuntu 24.04)

Needs: the Windows PC with Ubuntu under WSL, ideally after Chapter 2's
setup, so `~/bioinf-computing` exists. About 20 minutes.

### 1.1 Is a new WSL terminal a login shell? (most important)

Chapter 7 §6 says: "A new terminal window on Ubuntu or WSL is
**interactive** but **not a login** shell." I believe WSL actually
starts bash as a **login** shell (its `ps` line shows `-bash`). If so,
the table row, the figure caption, and the sentence need changing.
Desktop Ubuntu's terminal is non-login; WSL may not be.

1. Open a new Ubuntu window, from the Start menu or Windows Terminal.
   Run **Block A**.
2. Open VS Code connected to WSL (Chapter 2) and open its terminal
   (Ctrl+\`). Run only the first four lines of Block A.
3. In the Ubuntu window, type `bash`, then run lines 2–4 again. A shell
   started inside a shell should say "not login". Type `exit` after.

**Record:** each of the three outputs, labelled Windows Terminal, VS
Code, and nested `bash`.

### 1.2 Block B and Block C

Run **Block B**, then **Block C**.

**Record:** `blockB-<name>.txt` and Block C's output.

What WSL settles:

- **Chapter 6:** the default locale and sort order, and the truncated
  count with Ubuntu's gzip 1.12.
- **Chapter 7:** the `env` and `/bin/bash` CRLF messages; the `file`
  answer on the CSV; the `df` first column; `top`; Ctrl-C's 130.
- **Chapter 5:** `echo .*` under bash 5.2.

### 1.3 Chapter 5 practice folder and toy sizes (GNU gzip on Linux)

Chapter 5's toy-file sizes were measured with Apple's gzip. Paste
Chapter 5's "Build the practice folder" block (§1) if you haven't
already, then:

```bash
cd ~/bioinf-computing-ch05
ls -l share/run1 share/run2 "share/Run 3 final"
find share -size +1k
find share -mtime +30
echo .*
```

**Record:** the output. The chapter says the toy FASTQ files are "under
50 bytes each"; Docker gave 43–49. The chapter shows only `counts
FINAL.txt` for `-size +1k`. In Docker the folders were listed too (see
*Done in Docker*), and WSL's real disk should show the same. The
`-mtime` line should list `notes.txt` and `.old_settings`.

### 1.4 Does `less` open a `.gz` on WSL?

```bash
less ~/bioinf-computing-checks/SRR6357070_1.fastq.gz
```

Quit with `q`. **Record:** readable reads or binary noise. Chapter 5
says "some Linux systems" can open them. If WSL can, add it beside Nova.

### 1.5 Hard links between pixi's cache and `.pixi` (only if Chapter 2's setup is done)

```bash
du -sh ~/.cache/rattler ~/bioinf-computing/.pixi
du -sh ~/bioinf-computing/.pixi ~/.cache/rattler
```

**Record:** both pairs. In Docker the shared 1.3 GB was counted under
whichever came first. Chapter 7 §8 depends on this.

### 1.6 A CSV saved by Excel, read from `/mnt/c` (only if Excel is installed)

1. In Excel, type a small table (`sample,reads`, then two rows).
2. Save it **twice** on the Desktop: once as **CSV (Comma delimited)**,
   named `plain.csv`, and once as **CSV UTF-8**, named `utf8.csv`.
3. In Ubuntu, with `<WindowsUser>` replaced by your Windows user name:

   ```bash
   cd /mnt/c/Users/<WindowsUser>/Desktop
   cat -A plain.csv
   cat -A utf8.csv
   file plain.csv utf8.csv
   grep -c $'\r' plain.csv utf8.csv
   ```

**Record:** the output. Look for `^M$` at line ends. `utf8.csv` may
also start with `M-oM-;M-?`, a byte order mark. If it does, Chapter 7
§10 should mention it in a sentence, since it breaks the first column
name the same quiet way.

### 1.7 Exercise 4 on WSL

Do Part 2.5's laptop steps here: backup, add the line, new terminal.
Record which startup files exist, and whether `~/.profile` reads
`~/.bashrc`. Chapter 7 says it usually does on Ubuntu and WSL.

---

## Part 2: Nova (ISU) login node

Needs: a Nova login. About 20 minutes. Chapter 5's part was done on
2026-11-17; this part is Chapters 6 and 7.

### 2.1 Block A, Block B, Block C

Log in as usual. Run **Block A**, then **Block B**, then **Block C**.

What Nova settles:

- **The CRLF messages under bash 5.1.8 and coreutils 8.32.** These
  differ from the Ubuntu 24.04 text in the chapter. Readers on Nova will
  see whatever this gives, so the chapter may need a second example.
- **`file` 5.39 on the CRLF CSV.** Chapter 7 says Ubuntu's `file` 5.45
  doesn't mention CRLF; the older one may.
- **Nova's default locale and sort order** (Chapter 6).
- **Whether a login is "login" and "interactive"** (Block A), and which
  startup file reads `~/.bashrc`.
- **`ps -o … command`** with Nova's procps.
- **`df -h ~` on a shared home.** This shows the whole filesystem;
  compare with your quota in 2.4.

### 2.2 `ssh host command` from your laptop

Chapter 7's table says a command over SSH "often" reads `~/.bashrc`.
From your **laptop**, not Nova, use the same `ssh` you normally use.
If you have an alias in `~/.ssh/config`, use that name:

```bash
ssh <you>@nova.its.iastate.edu 'shopt -q login_shell && echo login || echo "not login"; [[ $- == *i* ]] && echo interactive || echo "not interactive"; echo "EDITOR=[$EDITOR]"; type -t ll || echo "no ll alias"'
```

**Record:** the four lines. Expect "not login" and "not interactive".
`EDITOR` shows whether `~/.bashrc` was read: it is set only after Part
2.5, so run this both before and after 2.5.

### 2.3 Group and setgid checks (Chapter 7 §2, open question 1)

This only lists things and makes one small file in a shared folder you
already use. Replace the placeholders with your real paths: your
group's folder under `/work/`, and the lab folder you share.

```bash
id
ls -ld /work/<group>
cd /work/<group>/<your lab folder>
ls -ld .
touch ch07_group_test && ls -l ch07_group_test
umask
rm ch07_group_test
```

**Record:**

- The folder's owner, group, and mode string.
- Whether there is an `s` where the group `x` would be (setgid).
- Whether the test file got the folder's group or your own primary
  group (the first group in `id`).
- The test file's mode, and `umask`.

Chapter 7 §2's cluster paragraph and Appendix A are written from this.

### 2.4 Quota command

Find Nova's command for showing your storage use and limits from ISU's
docs (via Appendix A), run it, and record the **command name** and the
**column headers**. Your numbers aren't needed. Chapter 7's disk table
says "the site's quota command"; this lets it name the real one.

### 2.5 Exercise 4 over SSH (Chapter 7, Exercise 4)

**On your laptop first**, run the exercise's answer as written in the
chapter:

```bash
cp -n ~/.bashrc ~/.bashrc.bak-ch07
grep -n 'EDITOR=' ~/.bashrc
grep -qxF 'export EDITOR=nano' ~/.bashrc ||
  echo 'export EDITOR=nano' >> ~/.bashrc
```

Open a **new** terminal and run `echo "$EDITOR"`, which should print
`nano`.

**Then on Nova**, run the same four lines, log out, log back in, and
run `echo "$EDITOR"`.

**Record:** whether the new SSH login printed `nano`. If it printed
nothing, Nova's login file doesn't read `~/.bashrc`; record the output
of Block A's `grep -n bashrc …` line. To undo, run
`cp ~/.bashrc.bak-ch07 ~/.bashrc`. Keeping `EDITOR=nano` is harmless.

---

## Part 3: SCINet Atlas (and Ceres, if you have time)

Needs: a SCINet login. Atlas and Ceres are separate machines; do Atlas
first, as planned. About 25 minutes per machine. SCINet has had no
captures yet, so this part includes Chapter 5's cluster note too.

### 3.1 Chapter 5's cluster note (what Nova already gave)

```bash
pwd
echo "$HOME"
type ls
ls --version | head -n 1
find --version | head -n 1
file --version | head -n 1
type zless
echo "LESSOPEN=[$LESSOPEN]"
complete -p ls 2>&1 | head -n 1
less ~/bioinf-computing-checks/SRR6357070_1.fastq.gz
```

Run the last line after Block B (3.2), since Block B downloads the
file. Quit `less` with `q` and record whether it was readable.

**Record:** everything. Chapter 5 §3 shows only Nova's output; if
SCINet's differs (for example, no `ls` alias), the chapter can say so
in a sentence.

### 3.2 Block A, Block B, Block C

Same as Nova, Part 2.1.

### 3.3 `ssh host command` from your laptop

Same as Part 2.2, with your Atlas login host. SCINet logins may go
through extra authentication; if the one-line command can't get
through, record that. It's useful for Chapter 9.

### 3.4 Group and setgid checks

Same as Part 2.3, using your project folder under `/project/<name>`.
If you use `/90daydata/<name>`, run `ls -ld` on it as well, without the
touch test. Record the same items.

### 3.5 Quota command

Same as Part 2.4, for SCINet's command from its docs via Appendix A.

### 3.6 Exercise 4 over SSH

Same as Part 2.5, on Atlas.

---

## Part 4: Apple silicon Mac (optional, only if you have one)

Chapter 7 §4 shows `type -a ls` from an Intel Mac and says the path is
`/opt/homebrew/…` on Apple silicon. After Chapter 1's setup, in a new
Terminal:

```bash
type -a ls
ls --version | head -n 1
shopt -q login_shell && echo login || echo "not login"
```

**Record:** the output. Expect `/opt/homebrew/opt/coreutils/libexec/gnubin/ls`
first, then `/bin/ls`, then "login".

---

## Part 5: any browser (gnu.org links)

gnu.org didn't respond from here while Chapters 5–7 were written. Open
each link and record "opens" or "broken". If broken, record where it
went:

- <https://www.gnu.org/software/bash/manual/>
- <https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html>
- <https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html>
- <https://www.gnu.org/software/bash/manual/html_node/Signals.html>
- <https://www.gnu.org/software/coreutils/manual/>
- <https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html>
- <https://www.gnu.org/software/findutils/manual/>
- <https://www.gnu.org/software/grep/manual/>
- <https://www.gnu.org/software/sed/manual/>
- <https://www.gnu.org/software/gawk/manual/>

Also note the **year** on the coreutils manual's front page.
`references.bib` has `gnu2025coreutils` with `year = {2025}`, copied
from the findutils entry, not checked.

---

## Done in Docker while writing this file (no action needed)

I ran Block B and Chapter 5's setup block in the Ubuntu 24.04 container
(bash 5.2.21, gzip 1.12, file 5.45) on 2026-11-18. Block B ran without
errors.

- **Chapter 6, truncated file:** `89515` lines and `PIPESTATUS 1 0`,
  the same count as GNU gzip 1.15 on the Mac. `head` pipeline:
  `141 0`. Redirect into a read-only file: `ro.txt: Permission
  denied`, status 1. The chapter is right for Linux.
- **Chapter 7, CRLF:** the same `env` and `/bin/bash` messages as in
  the chapter; `file` says `CSV ASCII text`; 7 lines with `\r`.
- **Chapter 5, toy sizes:** 43, 46, and 49 bytes with gzip 1.12, so
  "under 50 bytes" holds.
- **Chapter 5, `find share -size +1k`: wrong on Linux.** It also lists
  `share`, `share/analysis`, `share/meta`, and the three run folders,
  because Linux folders take 4 KB (the Mac capture showed only the
  counts file). Fix: `find share -type f -size +1k`, plus a sentence
  that folders count too. **Not yet changed in the chapter.** WSL
  Part 1.3 confirms it on a real disk.

---

## Results table

Fill in, or paste outputs into the chat and I'll fill it in.

| Check | WSL | Nova | Atlas | Ceres | Chapter it changes |
|:------|:---:|:----:|:-----:|:-----:|:-------------------|
| New terminal: login? interactive? | | | | | 7 §6 table and figure |
| VS Code terminal: login? | | — | — | — | 7 §6 |
| `ssh host command` reads `~/.bashrc`? | — | | | | 7 `tbl-startup-files` |
| Login file reads `~/.bashrc`? | | | | | 7 §6, Exercise 4 |
| `EDITOR` in a new login after Ex. 4 | | | | | 7 Exercise 4 answer |
| `type -a ls` (alias first?) | | done | | | 7 §4 |
| `echo .*` (`.`/`..` listed?) | | done | | | 5 §7 |
| Default locale; `sample` sorts where | | | | | 6 sort, 7 §5 |
| `PIPESTATUS` after `head` | | | | | 6 §2 |
| Truncated count / `PIPESTATUS` | | | | | 6 §3 |
| `Permission denied` wording | | | | | 6 §3 |
| CRLF + `env` message, status | | | | | 7 §10 |
| CRLF + `/bin/bash` message, status | | | | | 7 §10 |
| `file` on the CRLF CSV | | | | | 7 §10 |
| Folder without `x` behaves as in 7 §2 | | | | | 7 §2 |
| `ps -o …,command` works | | | | | 7 §7 |
| Ctrl-C status | | | | | 7 §7 |
| `top` header | | | | | 7 §7 |
| `df -h ~` first column | | | | | 7 §8 |
| Quota command name | — | | | | 7 §8 table |
| Folder group, setgid, umask | — | | | | 7 §2, Appendix A |
| `less` opens `.gz` | | done | | | 5 §9 |
| Toy FASTQ sizes under 50 B | | — | — | — | 5 §8 |
| pixi cache / `.pixi` hard links in `du` | | — | — | — | 7 §8 |
| Excel CSV: CRLF, BOM | | — | — | — | 7 §10 |
