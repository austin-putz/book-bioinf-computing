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

::: {.callout-tip}
## WSL status (2026-11-20): complete
All WSL checks are done (screenshots plus `blockB-WSL.txt`). Optional
only: 1.1 from a Windows Terminal **Ubuntu** tab (you used `wsl ~` in
PowerShell).

The machine is **Ubuntu 26.04.1 LTS**, bash **5.3.9**, WSL kernel
6.18, not the 24.04 the checks assumed, and its core tools are
**uutils coreutils 0.8.0** (a Rust rewrite), not GNU, except `cp`,
`mv`, `rm`, `df`, which Ubuntu keeps GNU. `grep` 3.12 and `sed` 4.9 are
GNU; gzip 1.14, file 5.46, procps 4.0.4.
:::

::: {.callout-tip}
## Nova status (2026-11-20): complete
All of Part 2 is done: Blocks A–C, 2.2 (remote command reads
`~/.bashrc`), 2.3 (setgid group folders), 2.4 (no quota command; a
usage file), 2.5 (Exercise 4). Findings that changed the book: Ctrl-Z
switched off site-wide, `which` is a function, umask `0002`, `top`
counts, NFS `df`, quotas. Left: links (Part 5); Atlas and Apple
silicon optional.
:::

::: {.callout-tip}
## Ceres status (2026-11-20): complete
All of Part 3 done on Ceres (3.1–3.6, Blocks A–C). RHEL 9.6 with
Nova's exact tool versions, so outputs match Nova except: umask
`0027` site-wide, Ctrl-Z works, `my_quotas` exists and `df` on
`/project/<name>` shows the project quota, personal primary group,
`top` cuts `first.last` names, SSH banner on stderr. Atlas optional.
:::


1. Open a new Ubuntu window, from the Start menu or Windows Terminal.
   Run **Block A**.
2. Open VS Code connected to WSL (Chapter 2) and open its terminal
   (Ctrl+\`). Run only the first four lines of Block A.
3. In the Ubuntu window, type `bash`, then run lines 2–4 again. A shell
   started inside a shell should say "not login". Type `exit` after.

**Record:** each of the three outputs, labelled Windows Terminal, VS
Code, and nested `bash`.

::: {.callout-tip}
## WSL result, 2026-11-19: complete
| Where | `login_shell` | `$-` | `ps` shows |
|:--|:--|:--|:--|
| `wsl ~` from PowerShell | **login** | interactive | `-bash` |
| VS Code terminal (WSL) | not login | interactive | `/bin/bash --init-file …` |
| `bash` typed in WSL | not login | interactive | `bash` |

Block A, rest: `type -a ls` → alias `ls --color=auto`, `/usr/bin/ls`,
`/bin/ls` (as the chapter); `which` → `/usr/bin/ls`; `command -v` →
the alias. Files: `.bash_history .bash_logout .bashrc .profile`;
`~/.profile` lines 13–15 read `~/.bashrc`. `locale`: `LANG=C.UTF-8`,
all `LC_*` `C.UTF-8` (not `en_US.UTF-8`). `LESSOPEN=| /usr/bin/lesspipe
%s`; `zless` is `/usr/bin/zless`; `umask` `0022`; `df -h ~` →
`/dev/sdd 1007G 2.0G 954G 1% /`.

**Changed in the book:** Chapter 7 now says a new WSL window is a
**login** shell (text, `tbl-startup-files`, `fig-startup-files`), VS
Code's terminal on Linux/WSL is not, and the captured `not login` is
from desktop Ubuntu. `df` example now shows the real `/dev/sdd` line.
:::


### 1.2 Block B and Block C

Run **Block B**, then **Block C**.

**Record:** `blockB-<name>.txt` and Block C's output.

::: {.callout-warning}
## WSL result, 2026-11-20: complete
Block C: Ctrl-C → `130`. Ctrl-Z → `[1]+ Stopped sleep 600`; `ps -o
pid,stat,rss,command` works (`-bash` `Ss`, `sleep 600` `T`); `exit`
printed **`logout`** then `There are stopped jobs.`; `kill %1` →
`Terminated`. `top -u "$USER"` header matches the chapter's shape
(`top - … up …, 1 user, load average`, `Tasks:`, `%Cpu(s):`, `MiB
Mem`, `MiB Swap`; columns `PID USER PR NI VIRT RES SHR S %CPU %MEM
TIME+ COMMAND`).

**Changed in the book:** Chapter 7 notes that a login shell prints
`logout` before refusing.

**Block B (`blockB-WSL.txt`):**

| Check | WSL output | Same as the chapter? |
|:--|:--|:--|
| `echo .*` | `.old_settings` | yes |
| default `sort` | `sample` **last** (as `LC_ALL=C`) | no: chapter shows `en_US.UTF-8` |
| read-only redirect | `-bash: ro.txt: Permission denied`, status 1 | yes, apart from `-bash:` (login shell) |
| MD5, `head` pipeline | `d19f3c7a…`; `PIPESTATUS 141 0` | yes |
| truncated file | `89515`, `PIPESTATUS 1 0` (gzip 1.14) | yes |
| CRLF + `env` | `env: $'bash\r': No such file or directory` + `use -[v]S` line; 127 | wording differs (uutils `env`) |
| CRLF + `/bin/bash` | `/bin/bash^M: bad interpreter: No such file or directory`; **126** | no: bash 5.2 said `required file not found`, 127 |
| `file` on CRLF sheet | `CSV ASCII text`; 7 `\r` lines; 0 `,30$` | yes |
| folder without `x` | `f`; `-?????????` line **without** `cannot access`; `cd` refused | `ls -l` message missing (uutils) |
| `ps -o …,command` | works | yes |

**Changed in the book:** Chapter 6 says WSL's `C.UTF-8` already sorts
like `C`. Chapter 7: capture note and a new paragraph in §9 on uutils
(with the Ubuntu 26.04 release-notes link); the uutils `env` and bash
5.3 CRLF messages (status 126); the missing `cannot access` line;
`-bash:` in login shells.
:::


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

::: {.callout-tip}
## WSL result, 2026-11-19: complete
Toy files 43, 43, 46, 46, 46, 49, 49 bytes: "under 50" holds.
`find share -size +1k` listed `share`, `share/run1`, `share/run2`,
`share/meta`, `share/Run 3 final`, `share/analysis`, and `counts
FINAL.txt`: **folders included**, as in Docker. `-mtime +30` →
`notes.txt`, `.old_settings`. `echo .*` printed `.*` (no dotfiles there;
bash 5.3 never lists `.` and `..`).

**Changed in the book:** Chapter 5 now uses `find share -type f -size
+1k` and explains that Linux folders take 4 KB.
:::


### 1.4 Does `less` open a `.gz` on WSL?

```bash
less ~/bioinf-computing-checks/SRR6357070_1.fastq.gz
```

Quit with `q`. **Record:** readable reads or binary noise. Chapter 5
says "some Linux systems" can open them. If WSL can, add it beside Nova.

::: {.callout-tip}
## WSL result, 2026-11-19: complete
Readable reads (the `LESSOPEN` helper). **Changed in the book:**
Chapter 5 now says Ubuntu, WSL, and Nova have the helper.
:::


### 1.5 Hard links between pixi's cache and `.pixi` (only if Chapter 2's setup is done)

```bash
du -sh ~/.cache/rattler ~/bioinf-computing/.pixi
du -sh ~/bioinf-computing/.pixi ~/.cache/rattler
```

**Record:** both pairs. In Docker the shared 1.3 GB was counted under
whichever came first. Chapter 7 §8 depends on this.

::: {.callout-tip}
## WSL result, 2026-11-19: complete
`~/.cache/rattler` first: `1.3G`, then `.pixi` `97M`. Reversed:
`.pixi` `1.3G`, then `~/.cache/rattler` `118M`. Identical to the Docker
numbers; Chapter 7 §8 is right as written.
:::


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

::: {.callout-tip}
## WSL result, 2026-11-19: complete
Both files end every line in `^M$` (3 of 3 lines). `utf8.csv` starts
with the BOM: `M-oM-;M-?sample,reads^M$`. `file`: `plain.csv: ASCII
text, with CRLF line terminators`; `utf8.csv: Unicode text, UTF-8
(with BOM) text, with CRLF line terminators`.

**Changed in the book:** Chapter 7 §10 adds the BOM (what `cat -A`
shows, `sed '1s/^\xEF\xBB\xBF//'` to remove it, tested on Ubuntu)
and notes that `file` did report CRLF for this small Excel file but not
for the seven-line sheet.
:::


### 1.7 Exercise 4 on WSL

Do Part 2.5's laptop steps here: backup, add the line, new terminal.
Record which startup files exist, and whether `~/.profile` reads
`~/.bashrc`. Chapter 7 says it usually does on Ubuntu and WSL.

::: {.callout-tip}
## WSL result, 2026-11-19: complete
`cp -n` worked but printed `cp: warning: behavior of -n is
non-portable and may change in future; use --update=none instead`.
`grep -n 'EDITOR='` found nothing; the append ran; after `source
~/.bashrc`, `echo "$EDITOR"` → `nano`. (You also found that `echo
'$EDITOR'` prints the literal text: single quotes stop expansion.)

**Changed in the book:** Chapters 5 and 7 now say to ignore that `cp
-n` warning, and why `--update=none` isn't used (missing on Nova's
coreutils 8.32 and on Apple's `cp`). Chapter 5 also gives 26.04's bash
5.3.
:::


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

::: {.callout-warning}
## Nova result, 2026-11-20: Part 2 complete (Blocks A–C, 2.2–2.5)
SSH login, from home (`/home/aputz`):

| Line | Nova output | Same as the chapter? |
|:--|:--|:--|
| bash | `5.1.8(1)-release` | (known) |
| login / interactive / `ps` | **login**, interactive, `-bash` | yes (SSH login) |
| `type -a ls` | alias `ls --color=auto`, `/usr/bin/ls` (no `/bin/ls`) | yes, one file |
| `which ls` | `alias ls='ls --color=auto'` then `/usr/bin/ls` | **no**: chapter says `which` doesn't know aliases |
| `command -v ls` | the alias | yes |
| startup files | `.bash_history .bash_logout .bash_profile .bashrc` (no `.profile`) | |
| reads `~/.bashrc` | `~/.bash_profile` lines 4–5 | yes |
| `locale` | `en_US.UTF-8` throughout | yes (Chapter 6's order) |
| `LESSOPEN`, `zless` | `\|\|/usr/bin/lesspipe.sh %s`; `/usr/bin/zless` | (known) |
| `umask` | **`0002`** | **no**: chapter shows `0022` |
| `df -h ~` | `172.16.7.238:/stor014/home 14T 7.5T 5.9T 56% /home` | NFS, whole shared home |

**Changed in the book (Chapter 7):** umask paragraph names Nova's
`0002` (new files `664`, folders `775`); `which` sentence notes Nova
shows the alias; the cluster `df` paragraph quotes Nova's line.

**Block B (`blockB-nova-login-1.txt`):** AlmaLinux 9.6; GNU coreutils
8.32, grep 3.6, sed 4.8, gzip 1.12, file 5.39, procps-ng 3.3.17.

| Check | Nova output | Same as the chapter? |
|:--|:--|:--|
| `echo .*` | `. .. .old_settings` | yes (Chapter 5 notes bash 5.1) |
| default `sort` | `sample` between `RAP1_…` and `WT_…`; `LC_ALL=C` puts it last | yes |
| read-only redirect | `-bash: ro.txt: Permission denied`, status 1 | yes (`-bash:`, login shell) |
| MD5, `head` pipeline | `d19f3c7a…`; `141 0` | yes |
| truncated file | `89515`, `1 0` (gzip 1.12) | yes |
| CRLF + `env` | `/usr/bin/env: ‘bash\r’: No such file or directory`, **no second line**; 127 | first line yes |
| CRLF + `/bin/bash` | `/bin/bash^M: bad interpreter: No such file or directory`; **126** | as bash 5.3, not 5.2 |
| `file` on CRLF sheet | `CSV text`; 7 `\r` lines; 0 `,30$` | as the Mac |
| folder without `x` | `f`; `cannot access`; `??????????` line; `cd` refused | yes (10 `?`, GNU 8.32) |
| `ps -o …,command` | works | yes |

**Changed in the book (Chapter 7 §10):** older `env` prints one line;
bash 5.1 and 5.3 both say `bad interpreter` (126), bash 5.2 is the odd
one; Nova's `file` 5.39 says `CSV text`.

**Block C:** Ctrl-C → `130` (yes). `top -u "$USER"`: header shape
matches (`top - … up 93 days, 41 users, load average …`, `Tasks: 1714
total`, `%Cpu(s)`, `MiB Mem 192544.7 total`, `MiB Swap`); same columns.
**Chapter 7 now quotes the 41 users and 1,714 processes** as the reason
for `-u`. **Ctrl-Z does nothing on Nova (by design).** First
attempt: Ctrl-Z did nothing, so Ctrl-C ended `sleep` and `exit` logged
out. Diagnosis: iTerm2 on the Mac sends Ctrl-Z fine (local `sleep 600`
stopped); on Nova `stty -a` shows `susp = <undef>` (`monitor on`), set
by `/etc/profile.d/disable-control-z.sh:1: stty susp undef`.
**Changed in the book (Chapter 7 §7):** a paragraph after the Ctrl-Z
pitfall says some clusters switch the key off, names Nova's file, shows
`susp = <undef>` vs `^Z`, and says to use Ctrl-C. The stopped-job
sequence itself is covered by WSL and the Mac; optional on Nova after
`stty susp '^Z'`.

**`type which` (done):** `which is a function`, piping `alias` and
`declare -f` output into `/usr/bin/which --tty-only --read-alias
--read-functions --show-tilde --show-dot`. **Changed in the book
(Chapter 7 §4):** the `which` sentence now says Nova wraps `which` in
a function and quotes `type which`.
:::

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

::: {.callout-note collapse="false"}
## Nova result, 2026-11-20: complete
Run from the Mac in iTerm2 (Duo code, then password):

| Line | Output | As expected? |
|:-----|:-------|:-------------|
| login? | `not login` | yes |
| interactive? | `not interactive` | yes |
| `EDITOR` | `EDITOR=[]` | yes: not set yet (2.5 not done) |
| `ll` | `no ll alias` | does not settle it |

`no ll alias` does not show that `~/.bashrc` was skipped: on Rocky/Alma
the `ll` alias comes from `/etc/profile.d/colorls.sh`, which skips
shells without a terminal. Whether `~/.bashrc` is read is decided by
the after-2.5 run (`EDITOR=[nano]` → read). **After 2.5:** `ssh
aputz@nova.its.iastate.edu 'echo "EDITOR=[$EDITOR]"'` printed
`EDITOR=[nano]`, so a remote command on Nova reads `~/.bashrc`.
**Changed in the book:** Chapter 7's `tbl-startup-files` row adds
"Nova does".
:::

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

::: {.callout-note}
## Nova result (2026-11-20)

| Item | Nova output |
|:--|:--|
| primary group | `domain users` (gid 101); the lab group `its-hpc-nova-abg` is one of the extra groups |
| `/work/ABG` | `drwxrws--T.`, `root` : `its-hpc-nova-abg`: setgid **on**, sticky with no `x` for other (capital `T`) |
| lab folder | `drwxrwsr-x.`, `aputz` : `its-hpc-nova-abg`: setgid **on** |
| test file | `-rw-rw-r--.`, group **`its-hpc-nova-abg`**: took the folder's group (setgid works) |
| `umask` | `0002`, as in Block A |
| `rm ch07_group_test` | asked `rm: remove regular empty file …?`, so `rm` is `rm -i` in that shell. Confirmed 2026-11-20: Austin's own `~/.bashrc` alias, not a Nova default; no book change |

**Changed in the book:** Chapter 7 §2 (*Groups and shared folders*)
now shows this output with `<group>`, `<lab>`, `you` placeholders.
It explains the capital `T` and the trailing `.` (an SELinux label).
Appendix A's stub has a planned-topics bullet for it. Atlas/Ceres
(`/project/<name>`) are still to do (3.4).
:::

### 2.4 Quota command

Find Nova's command for showing your storage use and limits from ISU's
docs (via Appendix A), run it, and record the **command name** and the
**column headers**. Your numbers aren't needed. Chapter 7's disk table
says "the site's quota command"; this lets it name the real one.

::: {.callout-note}
## Nova result, 2026-11-20: complete
ISU's pages ([file storage](https://research.it.iastate.edu/file-storage),
[FAQs](https://research.it.iastate.edu/faqs),
[reducing home use](https://research.it.iastate.edu/reducing-home-directory-usage-nova))
name **no quota command**. Run on Nova (numbers left out; other users'
names never recorded):

| Command | Result |
|:--|:--|
| `cat /work/ABG/group_storage_usage` | group line `NAME AVAIL USED` (`stor017/abg`), then the fraction used (`0.70…`), then one row per member: `TYPE NAME USED QUOTA OBJUSED OBJQUOTA` (`POSIX User`, `QUOTA none`; `OBJ` = file counts) |
| `df -h /work/ABG` | `novastor017:/stor017/abg 143T 101T 43T 71% /work/ABG`: the group's own filesystem, same numbers as the file |
| `quota -s` | prints nothing |
| `type my_workdir my_primary_group cdw` | first two are `/usr/local/bin` programs; `cdw: not found` (ISU's page is out of date) |
| `my_workdir` | **bug:** tries `mkdir /work/abg/aputz` (lower case), fails, prints `ERROR: could not create workdir`. Worth reporting to ISU |
| `du -sh ~` | `4.9G` of the 10 GB home limit |

**Changed in the book:** Chapter 7 §8: `df` table cell "often the
whole shared system"; quota row "quota command or usage file"; a Nova
paragraph (no quota command, home 10 GB with `du -sh ~`, `df -h
/work/<group>` shows the group share, `group_storage_usage` file);
check-yourself answer reworded. Appendix A: a Nova quota bullet.
:::

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

::: {.callout-note}
## Mac result, 2026-11-20: as the chapter predicts for a login file without the `~/.bashrc` line
Austin's Mac (iTerm2, login shell): a new terminal's `echo "$EDITOR"`
printed nothing. iTerm2 opens a login shell, which reads only
`~/.bash_profile`, and Austin's long-standing `~/.bash_profile` has no
line reading `~/.bashrc` (`grep -n bashrc` finds nothing). A reader who
followed Chapter 1 has that line, so the exercise works for them; the
answer's last paragraph and §6's check-yourself already cover this
case. No book change. **Confirmed:** after adding Chapter 1's
`if [ -f ~/.bashrc ]; then . ~/.bashrc; fi` to `~/.bash_profile`, a
new iTerm2 tab printed `nano`. (Austin then removed `EDITOR=nano`; he
uses vim.)
:::

::: {.callout-note}
## Nova result, 2026-11-20: complete
After the four lines, a new SSH login printed the new `EDITOR`: Nova's
`~/.bash_profile` reads `~/.bashrc`, as Block A showed. No book change.
:::

---

## Part 3: SCINet Ceres (Atlas optional)

Needs: a SCINet login. Atlas and Ceres are separate machines. Austin
started on Ceres (2026-11-20), so Ceres is now the main SCINet machine
for these checks; Atlas is optional (nothing depends on it). About 25 minutes per machine. SCINet has had no
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

::: {.callout-note}
## Ceres result, 2026-11-20: complete
Run on `ceres-login-2`:

| Line | Ceres | Same as Nova? |
|:--|:--|:--|
| `pwd`, `$HOME` | `/home/<user>` (user name has a dot: `first.last`) | yes |
| `type ls` | `ls is aliased to `ls --color=auto'` | yes |
| `ls --version` | GNU coreutils 8.32 | yes |
| `find --version` | GNU findutils 4.8.0 | yes |
| `file --version` | file-5.39 | yes |
| `type zless` | `/usr/bin/zless` | yes |
| `LESSOPEN` | `\|\|/usr/bin/lesspipe.sh %s` | yes (a `less` helper is set up) |
| `complete -p ls` | `complete -F _longopt ls` | yes |
| `less …fastq.gz` | first try: no file yet (Block B downloads it); after Block B: **readable reads** | yes |

**Changed in the book:** Chapter 5 §3 now says the captured output is
from Nova **and** Ceres. After Block B, rerun the `less` line; if it
shows reads, Chapter 5 §9's "(Ubuntu, WSL, and Nova have one)" gets
Ceres added. **Done:** after Block B, `less` showed the reads, so
§9 now says "Ubuntu, WSL, Nova, and Ceres have one".
:::

### 3.2 Block A, Block B, Block C

Same as Nova, Part 2.1.

::: {.callout-note}
## Ceres result, 2026-11-20: Block A done
| Line | Ceres | Compared with Nova / the book |
|:--|:--|:--|
| bash | 5.1.8 | same as Nova |
| login? interactive? `ps` | `login`, `interactive`, `-bash` | same (SSH login) |
| `type -a ls` | alias `ls --color=auto`, then `/usr/bin/ls` | same |
| `which ls` | shows the alias, then `/usr/bin/ls` | same as Nova (probably the same `which` function) |
| startup files | `.bash_history`, `.bash_logout`, `.bash_profile`, `.bashrc` | `~/.bash_profile` lines 4–5 read `~/.bashrc` |
| locale | `en_US.UTF-8` | same as Nova; Chapter 6's sort matches |
| `LESSOPEN`, `zless` | `lesspipe.sh`; `/usr/bin/zless` | same |
| **`umask`** | **`0027`** | **differs:** new files `640`, folders `750`: the group can read but not write, others get nothing. Nova `0002`, the book's laptops `0022` |
| `df -h ~` | `vast-vip1.vast.scinet.usda.gov:/home 91T 14T 78T 16% /home` | network storage, like Nova's |

**Confirmed site-wide:** the `grep` found `umask 027` in `/etc/profile`
(line 79) and `/etc/bashrc` (line 90), and `umask 0027` in
`/etc/profile.d/umask.sh`; nothing in your own files.
**Changed in the book:** Chapter 7 §2's umask paragraph adds Ceres
(`0027`: files `640`, folders `750`, group reads but cannot edit;
`chmod g+w` for a labmate who must edit).
:::

::: {.callout-note}
## Ceres result, 2026-11-20: Block B done
**Red Hat Enterprise Linux 9.6**, with exactly Nova's versions: bash
5.1.8, GNU coreutils 8.32, grep 3.6, sed 4.8, gzip 1.12, file 5.39,
procps-ng 3.3.17. Every Block B section gave Nova's output: `echo .*`
lists `.` and `..`; `sample` sorts in the middle (`en_US.UTF-8`), last
with `LC_ALL=C`; `-bash: ro.txt: Permission denied`, status 1; checksum
`d19f3c7a…`, `PIPESTATUS 141 0`; truncated file `89515`, `1 0`; CRLF
`env` one line, 127, `/bin/bash^M: bad interpreter`, 126; `CSV text`,
`7`, `0`; folder without `x` with the `cannot access` line and
`-?????????`; `ps -o …,command` works. **No book change**: Ceres
behaves as Nova does.
:::

::: {.callout-note}
## Ceres result, 2026-11-20: Block C done
Ctrl-C → `130`. **Ctrl-Z works** (unlike Nova): `[1]+ Stopped sleep
600`; `jobs` lists it; `ps` shows `sleep 600` as `T`; `exit` prints
`logout` then `There are stopped jobs.` (login shell, as the chapter
says); `kill %1` → `Terminated`. `top -u "$USER"`: same header and
columns; `62 users`, `Tasks: 1165`; the USER column shows
`austin.+` (names cut to 8 characters).
**Changed in the book (Chapter 7 §7):** "(SCINet's Ceres leaves it
on)" after "Some clusters switch Ctrl-Z off"; Ceres's 62 users and
1,165 processes beside Nova's; a sentence on `top` cutting long user
names (`first.+`).
:::

### 3.3 `ssh host command` from your laptop

Same as Part 2.2, with your Ceres login host (`ceres.scinet.usda.gov`). SCINet logins may go
through extra authentication; if the one-line command can't get
through, record that. It's useful for Chapter 9.

::: {.callout-note}
## Ceres result, 2026-11-20: complete
From the Mac: no prompts shown in the paste, then SCINet's login
banner (the ASCII "SCINet" logo and the USDA authorized-use notice),
then `not login`, `not interactive`, `EDITOR=[]` (expected: Exercise 4
not done yet), `no ll alias` (does not settle it, as on Nova). The
banner is the SSH server's pre-login banner, on stderr: `ssh
austin.putz@ceres.scinet.usda.gov true 2>/dev/null | wc -c` printed
`0` (confirmed). It is not output from a startup file and does not
break `rsync` or `scp`. For Chapter 9 (other session): readers will
see this banner on every Ceres `ssh`, `scp`, and `rsync`; it is
harmless. **After 3.6:**
`ssh austin.putz@ceres.scinet.usda.gov 'echo "EDITOR=[$EDITOR]"'`
printed the banner, then `EDITOR=[nano]`: a remote command on Ceres
reads `~/.bashrc`. **Changed in the book:** the `tbl-startup-files`
row now says "Nova and Ceres do".
:::

### 3.4 Group and setgid checks

Same as Part 2.3, using your project folder under `/project/<name>`.
If you use `/90daydata/<name>`, run `ls -ld` on it as well, without the
touch test. Record the same items.

::: {.callout-note}
## Ceres result, 2026-11-20: complete
| Item | Ceres output |
|:--|:--|
| primary group | `austin.putz` (a personal group, same name and number as the user); project group `proj-ibdru_bioinformatics` is an extra group |
| `/project/ibdru_bioinformatics` | `drwxrws--T.`, `root` : `proj-ibdru_bioinformatics`: setgid on, sticky, closed to others (same as Nova's `/work/ABG`) |
| `…/Austin` | `drwxr-s---.`, `austin.putz` : `proj-…`: setgid on, but **group cannot write** (made under umask `0027`) |
| test file | `-rw-r-----.`, group **`proj-ibdru_bioinformatics`**: setgid works; group reads only |
| `umask` | `0027` (site-wide) |
| `rm` | no prompt (no `rm -i` alias on Ceres) |

**Changed in the book:** Chapter 7 §2, a paragraph after the Nova
example: Ceres has the same pattern (`/project/<name>`, `root`,
`proj-<name>`), but your primary group is personal and umask `0027`
gives `-rw-r-----` / `drwxr-s---`, so the lab can read but not edit
until `chmod g+w`. Appendix A's shared-folder bullet now has Ceres.
:::

### 3.5 Quota command

Same as Part 2.4, for SCINet's command from its docs via Appendix A.

::: {.callout-note}
## Ceres result, 2026-11-20: complete
Found from SCINet's pages (July 2026 newsletter, project-management
guide): **`my_quotas`**. On Ceres:

| Command | Result (numbers left out) |
|:--|:--|
| `type my_quotas` | `/usr/local/bin/my_quotas` |
| `my_quotas` | "Live Quotas for <user>", a note (home quotas fixed; `/90daydata` no quota, removed 90 days after last access; links to request and project-management pages), then `Path  Usage (GB)  Quota (GB)  Availible (GB)  Consumed (%)  Status` in three sections: Ceres Home Directory, Ceres working project storage, Juno long-term project storage (`/LTS/project/…`). Home quota 29.8 GB |
| `df -h /project/ibdru_bioinformatics` | `vast-vip1.vast.scinet.usda.gov:/project 5.6T 2.5T 3.1T 45% /project`: the **project's** 5 TB quota as the size, though "Mounted on" says `/project` |
| `quota -s` | works for home: `space 4320K, quota 30518M, limit 50545M`, files with no limit |

**Changed in the book:** Chapter 7 §8: the Nova-only paragraph became
a Nova-vs-Ceres table (`tbl-cluster-quotas`: quota command, home
limit, group storage, what `df` shows), a sentence that `df` can
mislead both ways, links to ISU and SCINet pages; the check-yourself
question no longer names `/project` (on Ceres `df` there shows the
project quota). Appendix A: a Ceres quota bullet.
:::

### 3.6 Exercise 4 over SSH

Same as Part 2.5, on Ceres.

::: {.callout-note}
## Ceres result, 2026-11-20: complete
After the four lines, a new SSH login printed `nano`: Ceres's
`~/.bash_profile` reads `~/.bashrc` (as Block A showed). No book change.
:::

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

::: {.callout-note}
## Result, 2026-11-20: partly done (gnu.org went down mid-check)
`curl` from the Mac: first pass returned **200** for the bash manual,
`Bash-Startup-Files`, `Shell-Expansions`, the coreutils manual,
`File-permissions`, findutils, grep, sed, and gawk manuals. `Signals`
and `Bourne-Shell-Builtins` (also linked from Chapter 7) timed out, and
then gnu.org stopped answering altogether; Austin's Edge could not load
the pages either, so it is a gnu.org outage, not bad links. **To do:**
retry those two pages and read the coreutils manual's year later.
:::

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

| Check | WSL (2026-11-19) | Nova | Atlas | Ceres | Chapter it changes |
|:------|:---:|:----:|:-----:|:-----:|:-------------------|
| New terminal: login? interactive? | **login**, interactive | login, interactive (SSH) | | login, interactive (SSH) | 7 §6 table and figure |
| VS Code terminal: login? | not login | — | — | — | 7 §6 |
| `ssh host command` reads `~/.bashrc`? | — | yes (not login, not interactive) | | yes (not login, not interactive) | 7 `tbl-startup-files` |
| Login file reads `~/.bashrc`? | yes (`~/.profile`) | yes (`~/.bash_profile`) | | yes (`~/.bash_profile`) | 7 §6, Exercise 4 |
| `EDITOR` in a new login after Ex. 4 | `nano` (via `source`) | yes | | yes | 7 Exercise 4 answer |
| `type -a ls` (alias first?) | yes | yes; `which` shows alias (a function) | | yes; `which` shows alias | 7 §4 |
| `echo .*` (`.`/`..` listed?) | no (bash 5.3) | yes (bash 5.1) | | yes (bash 5.1) | 5 §7 |
| Default locale; `sample` sorts where | `C.UTF-8`; last | `en_US.UTF-8`; middle | | `en_US.UTF-8`; middle | 6 sort, 7 §5 |
| `PIPESTATUS` after `head` | `141 0` | `141 0` | | `141 0` | 6 §2 |
| Truncated count / `PIPESTATUS` | `89515`, `1 0` | `89515`, `1 0` | | `89515`, `1 0` | 6 §3 |
| `Permission denied` wording | same (`-bash:`) | same (`-bash:`) | | same (`-bash:`) | 6 §3 |
| CRLF + `env` message, status | `env: $'bash\r'…`, 127 | one line, 127 | | one line, 127 | 7 §10 |
| CRLF + `/bin/bash` message, status | `bad interpreter`, 126 | `bad interpreter`, 126 | | `bad interpreter`, 126 | 7 §10 |
| `file` on the CRLF CSV | `CSV ASCII text` | `CSV text` | | `CSV text` | 7 §10 |
| Folder without `x` behaves as in 7 §2 | yes; no `ls` message | yes | | yes | 7 §2 |
| `ps -o …,command` works | yes | yes | | yes | 7 §7 |
| Ctrl-C status | 130 | 130 | | 130 | 7 §7 |
| Ctrl-Z (`stty -a` susp) | `^Z`, stops | `<undef>`: off site-wide | | works, stops | 7 §7 |
| `top` header | matches | matches (41 users) | | matches (62 users; names cut to `austin.+`) | 7 §7 |
| `df -h ~` first column | `/dev/sdd` | NFS `…:/stor014/home`, 14T | | NFS `vast-vip1…:/home`, 91T | 7 §8 |
| Quota command | — | none; `group_storage_usage` file, `df -h /work/<group>`, home `du -sh ~` | | `my_quotas`; `df -h /project/<name>` shows the project quota; `quota -s` for home | 7 §8, App. A |
| Folder group, setgid, umask | — | setgid on (`drwxrws--T` / `drwxrwsr-x`); file gets lab group; `0002` | | setgid on (`drwxrws--T` / `drwxr-s---`); file gets project group; umask **`0027`** → `640` | 7 §2, Appendix A |
| `less` opens `.gz` | yes | done | | yes | 5 §9 |
| Toy FASTQ sizes under 50 B | yes (43–49) | — | — | — | 5 §8 |
| pixi cache / `.pixi` hard links in `du` | confirmed | — | — | — | 7 §8 |
| Excel CSV: CRLF, BOM | both; BOM in CSV UTF-8 | — | — | — | 7 §10 |
