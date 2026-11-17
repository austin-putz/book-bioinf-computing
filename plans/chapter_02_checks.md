---
title: "Chapter 2 — Hands-on checks for Austin"
subtitle: "Step-by-step: Windows, SCINet, Nova, Apple Silicon"
date: 2026-11-13
---

These are the checks from `chapter_02.md` (*Open questions*) that need a
real Windows PC or a cluster account. Each part stands alone: do them in
any order, skip what you can't do yet, and write results in the table at
the end. Nothing here changes anything permanent: all test files go in a
folder you delete afterwards.

**Notes for Austin:** Austin is new to Windows and SCINet, so every step
is spelled out. If something on screen doesn't match what's written here
(menus move between versions), write down what you saw. That's useful for
the chapter too, because readers will hit the same thing. Where a step
says "your site's docs", the official page is linked; follow it and
record what it asked you to do.

---

## Part 1 — Windows PC

Needs: a Windows 10 or 11 PC you can install software on (admin rights for
step 1.1). About 45–60 minutes the first time, mostly waiting.

### 1.1 Install WSL and Ubuntu (skip if already done)

1. Click **Start**, type `PowerShell`, right-click **Windows PowerShell**,
   choose **Run as administrator**, and click **Yes**.
2. In the blue window, type this and press Enter:

   ```
   wsl --install
   ```

3. When it finishes, **restart the PC**.
4. After the restart, an **Ubuntu** window opens by itself (if not:
   Start → type `Ubuntu` → open it). It asks for a new **UNIX username**
   and **password**. Pick anything simple; this is only for Ubuntu. When
   you type the password nothing appears on screen; that's normal.
5. You now see a prompt ending in `$`. This is the Linux terminal the book
   calls "Terminal (laptop)" on Windows.

Official steps: <https://learn.microsoft.com/en-us/windows/wsl/install>

### 1.2 Check nano and vim in Ubuntu

In the Ubuntu window, type each line and press Enter:

```bash
which nano vim
nano --version | head -n 1
vim --version | head -n 1
```

**Record:** the three outputs. If `which` prints a path for each (like
`/usr/bin/nano`), both exist. If one prints nothing, it is missing.

::: {.callout-note}
## Result (2026-11-14, ThinkPad E14, fresh `wsl --install` + Ubuntu)

Both present in the default Ubuntu image:

```
$ which nano vim
/usr/bin/nano
/usr/bin/vim
$ nano --version | head -n 1
GNU nano, version 8.7.1
$ vim --version | head -n 1
VIM - Vi IMproved 9.1 (2024 Jan 02, compiled Aug 18 2026 18:55:02)
```

Meaning for the chapter: WSL readers need no install step for nano or
vim; `pixi run nano` is only a fallback there.
:::

### 1.3 Install VS Code on the Windows side

1. In a web browser go to <https://code.visualstudio.com/> and download
   **VS Code for Windows** (the big blue button).
2. Run the installer. On the **Select Additional Tasks** page, make sure
   **Add to PATH** is ticked. Keep everything else as offered.
3. Open VS Code from the Start menu.

Do **not** install VS Code inside Ubuntu; the Windows copy talks to
Ubuntu through an extension.

**Check it's on PATH:** `where.exe code` in a new PowerShell window, and
`which code` in Ubuntu. If either finds nothing: close all terminals,
run `wsl --shutdown` in PowerShell, reopen, and try again; if still
missing, rerun the installer with **Add to PATH** ticked.

::: {.callout-note}
## Result (2026-11-14, ThinkPad E14)

Austin wasn't sure whether **Add to PATH** had been ticked; both checks
show it was (it is ticked by default):

```
PS> where.exe code
C:\Users\Thinkpad E14\AppData\Local\Programs\Microsoft VS Code\bin\code
C:\Users\Thinkpad E14\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd

$ which code
/mnt/c/Users/Thinkpad E14/AppData/Local/Programs/Microsoft VS Code/bin/code
```

Meanings for the chapter: (1) readers who can't remember the install
choices need exactly this check, so it goes into Chapter 2 §3; (2) WSL
inherits the Windows `PATH`, which is why `code` works in Ubuntu; (3)
the Windows user name here contains a space (`Thinkpad E14`), so the
path does too. `code` still works, but any command that names a
`/mnt/c/Users/...` path must quote it: a real example for Chapter 5
(quoting paths) and another reason to keep work in the Linux home (`~`).
:::

### 1.4 Install the two extensions

1. In VS Code, click the **Extensions** icon on the left edge (four small
   squares), or press `Ctrl+Shift+X`.
2. Search `WSL` and install **WSL** (publisher: Microsoft).
3. Search `Remote - SSH` and install **Remote - SSH** (publisher:
   Microsoft).

### 1.5 Check `code .` from Ubuntu

1. Close VS Code. In the **Ubuntu** window type:

   ```bash
   mkdir -p ~/vscode-test && cd ~/vscode-test
   code .
   ```

2. A VS Code window should open. Look at the **bottom-left corner**: it
   should say something like `WSL: Ubuntu`.
3. In VS Code, open a terminal: menu **Terminal → New Terminal**. Type
   `echo "$BASH_VERSION"` and `pwd`.

**Record:** did `code .` work the first time? What did the bottom-left
corner say? What did the two commands print?

::: {.callout-note}
## Result (2026-11-14, ThinkPad E14)

Extensions **WSL** and **Remote - SSH** installed (1.4) without issues.
`code .` from Ubuntu opened VS Code the first time, with `WSL: Ubuntu`
in the bottom-left corner. In VS Code's terminal:

```
$ echo "$BASH_VERSION"
5.3.9(1)-release
$ pwd
/home/austinputz/vscode-test
```

Meanings for the chapter: the VS Code terminal is the Ubuntu bash (5.3,
same major version as Homebrew bash on macOS), and it opens in the Linux
home, not under `/mnt/c`, so the status-bar check and the self-check in
§3 work as written.
:::

### 1.6 The main question: which SSH config does Remote-SSH write?

You don't need a working cluster login for this part; we only want to see
which file VS Code uses.

1. In VS Code (any window), press `Ctrl+Shift+P` to open the **Command
   Palette** (a search box at the top).
2. Type `Remote-SSH: Add New SSH Host` and press Enter.
3. It asks for an SSH command. Type a made-up one:

   ```
   ssh testuser@example.org
   ```

4. It then asks **which SSH configuration file to update**, showing a
   list of paths. **Record every path in that list exactly** (a phone
   photo is fine). Pick the first one.
5. Now press `Ctrl+Shift+P` again, type `Remote-SSH: Open SSH
   Configuration File`, press Enter, and again **record the list of
   paths**. Pick the same one; the file opens, and you should see a
   `Host example.org` entry. Delete those lines and save (`Ctrl+S`).
6. Open **PowerShell** (not as administrator) and type:

   ```
   where.exe ssh
   ssh -V
   ```

   **Record both outputs.** This tells us which SSH program Windows uses
   (expected: `C:\Windows\System32\OpenSSH\ssh.exe`).
7. In the **Ubuntu** window type `ls -la ~/.ssh`, and record whether it
   exists. This shows that Ubuntu has its own, separate SSH folder.

::: {.callout-note}
## Result, steps 1–4 (2026-11-14, ThinkPad E14)

Run from the `WSL: Ubuntu` VS Code window. *Add New SSH Host* offered:

```
C:\Users\Thinkpad E14\.ssh\config
C:\ProgramData\ssh\ssh_config
Settings specify a custom configuration file   (small grey option)
Help about SSH configuration files             (small grey option)
```

Meanings for the chapter: even inside a WSL window, Remote-SSH works on
the **Windows** side and offers only Windows files, never Ubuntu's
`~/.ssh/config`, which confirms the "two config files" explanation.
Readers pick the **first** (their own user file); the second is the
system-wide file for every Windows user and needs admin rights to edit.
:::

::: {.callout-note}
## Result, step 5 (2026-11-14)

*Open SSH Configuration File* listed the same user file first,
`C:\Users\Thinkpad E14\.ssh\config` (selected), plus the system-wide
`C:\ProgramData\ssh\ssh_config` (same list as step 4; confirmed, no dot).
Both commands point at the same user file, so readers can use either to
find it.
:::

::: {.callout-note}
## Result, steps 6–7 (2026-11-14)

```
PS> where.exe ssh
C:\Windows\System32\OpenSSH\ssh.exe
PS> ssh -V
OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2

$ ls -la ~/.ssh
ls: cannot access '/home/austinputz/.ssh': No such file or directory
```

Meanings for the chapter: Windows uses its built-in OpenSSH client
(no Git for Windows or extra install needed). Ubuntu has **no** `~/.ssh`
folder yet. That's normal, not a missed step: a fresh Ubuntu creates it
the first time you use `ssh` (it saves `known_hosts` after the `yes`
prompt) or make a key with `ssh-keygen` (Chapter 9). Meanwhile the
Windows `C:\Users\<you>\.ssh\` folder exists because VS Code just wrote
its `config` there. Two separate folders, confirmed. The chapter can
say so in one sentence so readers aren't alarmed by the error.
:::

What we expect (to confirm): VS Code writes to
`C:\Users\<you>\.ssh\config`, which is **not** the same file as Ubuntu's
`~/.ssh/config`. That's the "two config files" the chapter explains.

### 1.7 (Optional) Try the pixi trial in Ubuntu

If you have time, run Part 4 inside the Ubuntu window. It measures the
book environment on Linux without a cluster.

::: {.callout-note}
## Result (2026-11-14, WSL Ubuntu, ThinkPad E14)

No errors or warnings.

```
real    0m9.779s
user    0m8.978s
sys     0m11.328s

Python 3.12.16
R version 4.4.3 (2025-02-28) -- "Trophy Case"
seqkit v2.14.0
file                   format  type  num_seqs    sum_len  min_len  avg_len  max_len
SRR6357070_1.fastq.gz  FASTQ   DNA     50,000  5,050,000      101      101      101

--- sizes
1.3G    .pixi
132M    /home/austinputz/pixi-trial/cache
files in .pixi:  15524
files in cache:  19858
x86_64
pixi 0.84.2
```

Meanings: same versions and `seqkit stats` as the Mac run. The cache
looks small because on Linux the environment's files appear to be hard
links to the cache's copies, so `du` counts them once; real disk use is
about 1.4 GB in total. On a cluster, keep the cache on the same storage
as the project, or the links become copies and the space doubles. (Details
in `chapter_02.md`, *Trial install*.)
:::

### 1.8 Clean up

In Ubuntu: `rm -rf ~/vscode-test`. Keep WSL and VS Code if you want them.

---

## Part 2 — SCINet (Ceres or Atlas)

Needs: a SCINet account (apply through your PI or USDA contact; approval
can take a while). SCINet requires multi-factor authentication. Read
these official pages first; they change, so follow them over anything
here:

- Getting started / account: <https://scinet.usda.gov/guides/start>
- Accessing SCINet (hub): <https://scinet.usda.gov/guides/access/>
- SSH login: <https://scinet.usda.gov/guides/access/ssh-login>
- Open OnDemand: <https://scinet.usda.gov/guides/use/open-ondemand>
  (the Ceres site itself: <https://ceres-ondemand.scinet.usda.gov/>)
- VS Code on Ceres: <https://scinet.usda.gov/guides/ide/vscode>
- Storage locations: <https://scinet.usda.gov/guides/data/storage>
- Quotas (`my_quotas`):
  <https://scinet.usda.gov/guides/data/project-management>

(Links checked 2026-11-13.) SCINet's own advice is that for most work
you do **not** need SSH: Open OnDemand in a browser is the recommended
way in. So if SSH setup gets stuck, do 2.3 (Open OnDemand) first; its
shell and VS Code apps let you do 2.2 and 2.4 too.

**Notes for Austin:** if any link above has moved, start from
<https://scinet.usda.gov/guides/> and record the new address.

**Austin is using Atlas** (decided 2026-11-14). Atlas is SCINet's other
cluster, at Mississippi State, with the same SCINet account. The
differences from the Ceres steps below, per the SCINet pages (checked
2026-11-14):

| | Ceres | Atlas |
|:--|:--|:--|
| SSH host | `ceres.scinet.usda.gov` | `atlas-login.hpc.msstate.edu` (lands on `atlas-login-1` or `-2`) |
| SSH sign-in | step CLI + eAuthentication | same setup, same daily sign-in |
| Open OnDemand | <https://ceres-ondemand.scinet.usda.gov/> | <https://atlas-ood.hpc.msstate.edu/> |
| VS Code app in OnDemand | yes (SCINet VS Code guide) | **not documented**; check the app list |
| Home quota, `my_quotas` | 30 GB; works | 30 GB; documented to work on Atlas too |
| Interactive job | `salloc -A <project>` (partition `ceres`) | `salloc -A <project>`; Atlas partition names not on SCINet pages (check `sinfo`) |

Atlas docs (MSU): <https://www.hpc.msstate.edu/computing/atlas/> (shown
in the login banner).

### 2.1 First login with SSH

1. Open a terminal on your Mac.
2. Follow the SSH login page. SCINet's SSH sign-in is not a plain
   password: it uses a small program called **step** (SmallStep CLI) that
   opens the USDA eAuthentication page in your browser (LincPass/AltLinc,
   or Login.gov for non-USDA users), about once a day. The page explains
   how to install and set it up; on the Mac it will likely be a Homebrew
   install. **Record each setup step** you had to do; readers will need
   the same list in Appendix A.
3. Then log in with:

   ```bash
   ssh your.username@ceres.scinet.usda.gov
   ```

4. The first time, SSH asks *Are you sure you want to continue
   connecting (yes/no/[fingerprint])?* Type the full word `yes`.
5. Complete the browser sign-in if it asks.

**Record:** the exact prompts you saw, in order (copy them from the
terminal, removing anything secret like codes). This becomes the captured
session in Chapter 2 §4, so it is valuable.

::: {.callout-note}
## Result (2026-11-16, Intel MacBook, first SSH login to Ceres)

Austin had only used Open OnDemand before. Setup, following
<https://scinet.usda.gov/guides/access/ssh-login>:

```
~ $ brew install step
~ $ step version
Smallstep CLI/0.31.0 (darwin/amd64)
Release Date: 2026-09-25T19:43:47Z

~ $ step ca bootstrap --ca-url https://step-ca.scinet.usda.gov --fingerprint adb703fd18f176937743b20228d52af7a705d63a0471cd67428660be5fd006bf
The root certificate has been saved in /Users/<you>/.step/certs/root_ca.crt.
The authority configuration has been saved in /Users/<you>/.step/config/defaults.json.

~ $ step ssh config --set Provisioner=keycloak --set User=austin.putz
✔ /Users/<you>/.ssh/config
✔ /Users/<you>/.step/ssh/includes
✔ /Users/<you>/.step/ssh/config
✔ /Users/<you>/.step/ssh/known_hosts
```

What `step ssh config` wrote. At the end of `~/.ssh/config` (existing
entries untouched):

```
# autogenerated by step @ 2026-11-16T16:51:02Z
Host *
    Include "/Users/<you>/.step/ssh/includes"
# end
```

`~/.step/ssh/includes` only includes `~/.step/ssh/config`, which holds:

```
Match exec "step ssh check-host %h"
    User austin.putz
    UserKnownHostsFile "/Users/<you>/.step/ssh/known_hosts"
    ProxyCommand step ssh proxycommand --provisioner keycloak %r %h %p
```

Login: `ssh austin.putz@ceres.scinet.usda.gov` opened the default
browser (Edge); Austin was already signed in to Login.gov, so it
connected without further pages.

```
[austin.putz@ceres-login-1 ~]$ hostname
ceres-login-1.ceres.scinet.usda.gov
[austin.putz@ceres-login-1 ~]$ exit
logout
Connection to ceres.scinet.usda.gov closed.
```

(SSH lands in home: `pwd` on the login node printed `/home/austin.putz`.)

Meanings for the chapter:

- Three commands, run once (install, bootstrap, ssh config), with the
  fingerprint copied from SCINet's page; then plain `ssh`.
- No `Host ceres…` block: `step` checks each host (`Match exec`) and, for
  SCINet hosts only, sets the user, uses its own `known_hosts`, and gets
  a short-lived certificate (`ProxyCommand`), opening the browser when a
  new one is needed. No SSH keys or passwords.
- Because of that `known_hosts`, the usual host-key `yes` prompt is
  skipped on SCINet (confirmed: no prompt on first login). So
  the captured first-login session with the `yes` prompt should come
  from Nova, and the SCINet text says what to expect instead.
- If the reader is not already signed in, the browser shows the
  eAuthentication → Login.gov pages (as in the welcome email) first.
:::

### 2.2 Look around (on the login node)

```bash
hostname
echo "$SHELL"
which nano vim
nano --version | head -n 1
```

::: {.callout-note}
## Result (2026-11-14, Atlas)

```
[austin.putz@atlas-login-1 ~]$ hostname
atlas-login-1.hpc.msstate.edu
[austin.putz@atlas-login-1 ~]$ echo "$SHELL"
/bin/bash
[austin.putz@atlas-login-1 ~]$ which nano vim
/usr/bin/nano
/usr/bin/vim
[austin.putz@atlas-login-1 ~]$ nano --version | head -n 1
 GNU nano, version 5.6.1
```

Login banner: Atlas runs Rocky Linux 9.x. Meanings: bash is the login
shell, and nano and vim are both there, so §6 works on the cluster
without installing anything. Nano 5.6.1 is older than WSL's 8.7.1, but the
basics the chapter teaches (^O save, ^X exit, the help bar) are the same.
Readers who want the newer one have it from the book environment
(`pixi run nano`). The prompt `[user@host ~]$` differs from Ubuntu's
`user@host:~$`; worth one line in the chapter so readers don't think
something is wrong.
:::

Then check storage. Home directories have a 30 GB quota; your project
directory is under `/project/<project_name>/`. Run:

```bash
my_quotas
```

Record the output for home and project (bytes, and files if shown).

::: {.callout-note}
## Result (2026-11-14, Atlas)

Project names replaced with placeholders (this file is in the public repo).

```
[austin.putz@atlas-login-2 project]$ my_quotas
Live quotas for austin.putz

Loading Quotas...
Note: All home directory quotas are of fixed size and cannot be increased. Temporary space on
      /90daydata does not have quotas, but data are removed 90 days after last access. ...

Path                          Usage (GB)  Quota (GB)  Available (GB)  Consumed (%)  Status

Atlas home directory
          /home/austin.putz          <1          30              29             0  OK

Atlas working project space
      /project/<project_a>           <1        1000             999             0  OK
      /project/<project_b>            0          <1              <1             0  OK
```

Meanings: home is 30 GB and fixed; a project is set per project (1000 GB
here). `/90daydata` has no quota but deletes files 90 days after last
access. **No file-count (inode) column**, so the output can't tell us
whether pixi's ~15,500 files hit a file limit; space-wise, one book
environment (1.3 GB) fits in home but uses about 4% of it, and the
cache-on-same-storage advice puts both in `/project`. A reader may belong
to several projects, some with almost no space (the second row), so
the chapter should say "your project directory" and show how to pick it
from this list.
:::

::: {.callout-note}
## Result (2026-11-14, Ceres)

Project names replaced with placeholders, matching the Atlas result
(`<project_a>` is the same project on both clusters).

```
[austin.putz@ceres-login-1 project]$ my_quotas
Live Quotas for  austin.putz
Note: All home directory quotas are of fixed size and cannot be increased. ...
                                Path  Usage (GB)  Quota (GB)  Availible (GB)  Consumed (%)  Status
 Ceres Home Directory
                   /home/austin.putz         0.0        29.8            29.8           0.0      OK
 Ceres working project storage
                /project/<project_b>      8058.0     10240.0          2182.0          78.7      OK
                /project/<project_a>      2532.8      5120.0          2587.2          49.5      OK
 Juno long-term project storage
            /LTS/project/<project_b>       246.6       500.0           253.4          49.3      OK
            /LTS/project/<project_a>        26.0      1024.0           998.0           2.5      OK
```

Meanings, comparing with Atlas:

- **Each cluster has its own storage.** The same two projects exist on
  both, but on Ceres they hold terabytes and on Atlas almost nothing, and
  the quotas differ (`<project_a>`: 5120 GB on Ceres, 1000 GB on Atlas;
  `<project_b>`: 10240 GB vs under 1 GB). Files and environments made on
  one cluster are not on the other. The chapter should say this plainly:
  install the book environment on the cluster you will use.
- **The output looks different on each cluster** (column spacing,
  decimals vs `<1`, home quota shown as 29.8 vs 30). The book should show
  one captured example and tell readers theirs will look a bit different.
- **Juno long-term storage (`/LTS/project/...`) shows only on Ceres.** It
  is for keeping data, not for running analyses or environments.
- **Still no file-count column** on either cluster.
:::

### 2.3 VS Code through Open OnDemand

Follow the VS Code guide (link above), **Method 1: VS Code Server in Open
OnDemand**:

1. Log in to Open OnDemand in a browser:
   <https://ceres-ondemand.scinet.usda.gov/>.
2. Start the **VS Code** app; choose a small request (e.g., 1–2 cores,
   1–2 hours) and your project account if asked.
3. When it says **Running**, click **Connect**. VS Code opens in the
   browser.
4. Open a terminal inside it (☰ menu → Terminal → New Terminal) and run
   `hostname`. It should be a compute node, not a login node.
5. **End the session:** back in Open OnDemand, go to **My Interactive
   Sessions** and click **Cancel** on the VS Code session.

**Record:** each screen's choices (a few screenshots help), the
`hostname` output, and confirm that Cancel ended it. Also note whether
the guide told you to move `~/.local/share/code-server` to project
storage, and whether you did.

::: {.callout-note}
## Result (2026-11-14, Ceres, Method 1)

VS Code Server started from Ceres Open OnDemand; in its terminal:

```
[austin.putz@ceres20-compute-2 4a88d91a-2c2b-4d99-96d3-650c4475a96b]$ hostname
ceres20-compute-2
```

Meanings: a compute node (`ceres20-compute-2`), not a login node, so the
route works as SCINet describes. The terminal opened in a folder named
by a long ID (the OnDemand session's own folder), not in home: worth a
line in the chapter, with `cd` to the project folder (or File → Open
Folder…) as the first step.

**Start form** (Interactive Apps → Servers → **VS Code**; screenshots
2026-11-14). Fields in order, with what Austin used:

| Field | Used | Notes |
|:------|:-----|:------|
| Account | `<project>` | drop-down of your Slurm accounts (projects); avoid `sandbox` (2-hour limit) |
| Queue | `ceres` | partition |
| QOS | `ceres` | "only required for priority partitions" |
| Number of cores | 2 | |
| Memory required | `8G` | whole number + unit |
| Number of hours | 2 | the session ends at this limit |
| Optional Slurm Arguments | (blank) | e.g. `--job-name` |
| Working Directory | (blank) | "Select your project directory; defaults to $HOME"; has a **Select Path** button |
| Codeserver Version | 4.17 | |
| Email when session starts | unchecked | |

The form's own note: "installed extensions can take up significant
space, so we recommend that you make a symlink for
`~/.local/share/code-server` that goes to a subdirectory of your
`/project` space." The app list also shows **VS Code Tunnel**, RStudio
Server, Jupyter, and Desktop under Servers/Desktops.

**Cancel:** stopped VS Code, but the browser tab stayed open and had to
be closed by hand.

Meanings for the chapter: tell readers to set **Working Directory** to
their project folder on the form; then VS Code should open there and
they never need to open a folder mid-session (which reloads the window
and stops running commands). Not yet tested with it set. The symlink
note matches SCINet's VS Code guide; whether Chapter 2 does it now or
defers it is open.

**Extensions folder, with no extensions installed:**

```
[austin.putz@ceres20-compute-2 ~]$ du -sh ~/.local/share/code-server 2>/dev/null || echo "not there"
976K    /home/austin.putz/.local/share/code-server
```

Under 1 MB after one session, so it is not a quota problem in Chapter 2;
it grows only when extensions are installed (each is often tens to
hundreds of MB).

**Working Directory test (2026-11-16):** second session with Working
Directory set to the project folder (path shortened):

```
[austin.putz@ceres20-compute-10 Austin]$ pwd
/project/<project>/Austin
```

From the screenshot: the Explorer opened on that folder, and the
browser address ends `?folder=/project/...`, so the setting carries
through. The terminal's login message says "To see your quotas, run
/usr/local/bin/my_quotas". The Welcome tab's *Recent* list shows the
earlier sessions' ID folders under `~/ondemand/data/sys/...`: the
ID-named folder is OnDemand's per-session folder in home. The status
bar's left end shows only the remote icon, **no** `SSH: <host>` text,
so in browser VS Code readers check where they are with `hostname`,
not the status bar.
:::

(Optional: Method 2, the registered tunnel, needs a Microsoft account;
try it only if Method 1 is done.)

### 2.4 pixi trial on Ceres

Do Part 4 on a **compute node**, not the login node. Start an interactive
job first (SCINet's docs give the exact command; it looks like
`salloc` or `srun --pty bash` with a time limit), and use your project
directory as the base folder. Type `exit` when done to release the node.


::: {.callout-note}
## Result (2026-11-14, Ceres compute node via OnDemand VS Code)

Run in the OnDemand VS Code terminal (already a compute node, so no
`salloc` needed), base folder in project storage (path shortened).

```
real    8m23.733s
user    0m15.324s
sys     0m6.571s
Pixi task (check): python --version && R --version | head -n 1 && seqkit version
Python 3.12.16
R version 4.4.3 (2025-02-28) -- "Trophy Case"
seqkit v2.14.0
file                   format  type  num_seqs    sum_len  min_len  avg_len  max_len
SRR6357070_1.fastq.gz  FASTQ   DNA     50,000  5,050,000      101      101      101
--- sizes
1.3G    .pixi
114M    /project/<project>/<you>/pixi-trial/cache
files in .pixi:  15524
files in cache:  19858
linked files: 12408
x86_64
pixi 0.84.2
```

Meanings: works, same results as WSL and the Mac. **Ignore the time:**
the project folder was opened in VS Code mid-run, which restarted the
terminal, so the 8.4 minutes includes an interrupted attempt. The chapter
still warns that a first install on a cluster can be slow. 12,408 linked
files confirms the hard-link explanation.

**Lesson for the chapter:** open the project folder in VS Code
*before* starting anything in its terminal; opening a folder reloads
the window and stops what the terminal was running.

**Reinstall from the cache** (same session, nothing downloaded):

```
[austin.putz@ceres20-compute-2 book]$ rm -rf .pixi
[austin.putz@ceres20-compute-2 book]$ time pixi install
The default environment has been installed.

real    0m57.127s
user    0m0.903s
sys     0m1.160s
```

Meanings: about a minute just to write the files to project storage,
with almost no CPU, so shared storage is the slow part (WSL did a full
install, downloads included, in 10 s). The "can be slow" warning is
justified.
:::

---

## Part 3 — Nova (ISU)

Needs: a Nova account and the ISU network (on campus or the ISU VPN).
Official pages:

- VS Code on Nova: <https://research.it.iastate.edu/using-vs-code-cluster>
- Remote IDEs on compute nodes:
  <https://research.it.iastate.edu/launching-remote-ides-novas-compute-nodes>
- Nova main docs: <https://research.it.iastate.edu/> (search "Nova")

**From Austin's experience (2026-11-16, not yet re-tested):** off
campus, connect the ISU VPN first with **Cisco Secure Client** (the
newer name for Cisco AnyConnect). Nova login uses two-factor
authentication with a code from an authenticator app (e.g. Google
Authenticator), set up on first login. A login attempt on 2026-11-16
failed (server possibly down); retry later.

Same steps as Part 2, with Nova's names:

1. **SSH login** (record the prompts, as in 2.1).
2. **Look around** (2.2): `hostname`, `echo "$SHELL"`, `which nano vim`,
   and your `/work/<group>/<user>` space and quota.
3. **VS Code:** use the **VS Code Tunnel** app or **VS Code Server** app
   in Nova's Open OnDemand (first link). Run `hostname` in its terminal;
   record how you close or end it (the tunnel app allows ten
   connections; old ones are closed by right-click).
4. **pixi trial** (Part 4) on a compute node, in `/work/...`.

::: {.callout-note}
## Result: first-login prompts (2026-11-16, Mac → Nova)

Run with `ssh -o UserKnownHostsFile=/dev/null nova` so the first-time
prompt shows again without changing any file. Password and
authenticator-code lines removed by Austin; last-login address removed.

```
$ ssh -o UserKnownHostsFile=/dev/null nova
The authenticity of host 'nova.its.iastate.edu (129.186.90.9)' can't be established.
ED25519 key fingerprint is SHA256:DRxKEui9nnf4BSBeLSN4mZ5Il3eHjsoiN74EvzSlmxE.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'nova.its.iastate.edu' (ED25519) to the list of known hosts.
(aputz@nova.its.iastate.edu) Verification code:
(aputz@nova.its.iastate.edu) Password:
############################################################################
#                                                                          #
# User guides are available at https://research.it.iastate.edu/            #
#                                                                          #
# Tip: Use Search option to find information on the site.                  #
#                                                                          #
############################################################################
#                                                                          #
# Do not rely on /work, /lustre, or /ptmp as your only copy of important   #
# files. Files on /ptmp not accessed for 60 days will be deleted.          #
# Always copy important data to a backed-up system like /lss.              #
#                                                                          #
##########################                                                 #
#                                                                          #
# The next Nova maint is scheduled for January 12, 2027.                   #
#                                                                          #
# Jobs with time limits on Nova that cross the maintenance window will     #
# automatically be held and started once work completes.                   #
#                                                                          #
############################################################################
Last login: Mon Nov 16 17:55:22 2026 from <address>
```

Meanings for the chapter: this is the captured first-login session for
§4: host-key prompt (type `yes`), "Permanently added" (saved in
`~/.ssh/known_hosts`), then password and authenticator code, then the
site banner. The code is asked **before** the password, and
neither shows what you type (prompt wording recorded 2026-11-16). The banner names Nova's storage:
`/work`, `/lustre`, `/ptmp` (deleted after 60 days unused) are not
backed up; `/lss` is. Useful for Chapter 10 and Appendix A.
:::

::: {.callout-note}
## Result: look around (2026-11-16, Nova login node, via `ssh nova`)

```
Mon Nov 16 : ~ $  hostname
nova-login-2
Mon Nov 16 : ~ $  echo "$SHELL"
/bin/bash
Mon Nov 16 : ~ $  which nano vim
/usr/bin/nano
/usr/bin/vim
Mon Nov 16 : ~ $  nano --version | head -n 1
 GNU nano, version 5.6.1
Mon Nov 16 : ~ $  pwd
/home/aputz
```

Meanings: same as Atlas: bash, nano 5.6.1 and vim present, SSH lands
in home. The prompt (`Mon Nov 16 : ~ $`) is Austin's own customised
one, so captured Nova sessions in the book should use a plain
`[user@nova-login-2 ~]$` style prompt instead. The Nova username is
the ISU NetID, not the SCINet-style `first.last`.

**SSH from a Mac with several keys (2026-11-16):** the first Nova and
Atlas attempts failed with "Received disconnect … Too many
authentication failures": `Host *` in `~/.ssh/config` offered every key
(three `IdentityFile` lines plus the agent), and the server hung up
before reaching password + authenticator code. `ssh -o
PubkeyAuthentication=no` worked; the lasting fix was per-host entries
(`Host nova` with `PubkeyAuthentication no`, `IdentitiesOnly yes` for
GitHub) and no keys under `Host *`. A pitfall for Chapter 9.
:::

::: {.callout-note}
## Result: VS Code from Nova Open OnDemand (2026-11-16)

In the VS Code terminal (group name replaced):

```
Mon Nov 16 : /work/<group>/aputz $  hostname
nova18-69
Mon Nov 16 : /work/<group>/aputz $  pwd
/work/<group>/aputz
```

Meanings: a compute node (`nova18-69`, not `nova-login-*`), opened in
the group's `/work` folder, as ISU describes.

**App:** Nova OnDemand (<https://nova-ondemand.its.iastate.edu/>) →
Interactive Apps → Servers → **VS Code Server** (runs in a browser
tab). The list also has VS Code Tunnel, Jupyter, Jupyter - Lightweight,
RStudio Server (+ Classic), and Nova Desktop. Sessions page:
`…/pun/sys/dashboard/batch_connect/sessions` (*My Interactive
Sessions*).

**Start form** (screenshots 2026-11-16), compared with Ceres:

| Field | Used | Notes | vs Ceres |
|:------|:-----|:------|:---------|
| Account | `<group>` | Slurm account | same idea; no `sandbox` |
| Slurm Partition | `nova` (max time 31-00:00:00) | "Priority partitions available only to those users who purchased nodes" | Ceres: Queue `ceres` + QOS |
| Number of hour | 3 | must be under the partition limit | same |
| Number of Tasks Per node | 4 | "Number of CPUs per node" | Ceres: Number of cores |
| Memory Required | `8G` | no decimals; no unit = MB | same |
| Extra Optional Slurm Arguments | (blank) | e.g. `--gres=gpu:a100:1` | same idea |
| Extra Modules to Load on Start | (blank) | space-separated module names | **Nova only** |
| Working Directory | `/work/<group>/<netid>/` (set by Austin) | "defaults to **last used directory** if no directory is specified"; **Select Path** button | Ceres: defaults to `$HOME` |
| Codeserver Version | 4.97 | | Ceres offered **4.17**, much older |

Same extensions note as Ceres, with `/work` in place of `/project`:
symlink `~/.local/share/code-server` to a subdirectory of your `/work`
directory.

**In the window** (screenshot): the address ends `?folder=/work/<group>/<netid>`;
the Explorer shows that folder; the status bar's left end shows the
remote icon and the Git branch, but no host name, as on Ceres, so
`hostname` is the check.

Meanings for the chapter: the two sites' forms differ in names
(Queue/QOS vs Slurm Partition; cores vs tasks per node) and in the
Working Directory default, so the chapter teaches the common idea
(account, time, CPUs, memory, folder) and Appendix A gives each site's
field names. The old code-server on Ceres (4.17) may not run current
extensions; worth noting in Appendix A.

**Ending the session** (screenshots 2026-11-16, a second session on
`nova18-72`): *My Interactive Sessions* shows a card "VS Code Server
(<job id>)" with **1 node | 4 cores | Running**, Host, Created at, Time
Remaining, Session ID, and **Connect to VS Code**, plus a red
**Cancel** button. Cancel → banner "Session was successfully
canceled"; the card turns **Completed** with a **Delete** button (and
edit and relaunch icons) and says "For debugging purposes, this card
will be retained for 7 more days". The VS Code tab stayed open and was
closed by hand, as on Ceres.

**Checked (2026-11-16):** closing the VS Code tab on its own does
**not** end the session; the card stays Running until Cancel.

Meanings for the chapter: on both sites, end a session with **Cancel**
on its card (not by closing the tab), then close the tab; Delete only
removes the finished card. The card's Time Remaining is the reminder
that the session holds a node until cancelled or timed out.
:::

::: {.callout-note}
## Result: pixi trial (2026-11-16, Nova compute node, OnDemand VS Code)

First paste attempt started R's interactive prompt partway (cause not
found; likely the long block broke on paste); quit with `q("no")` and
reran in three smaller pastes (manifest written with one `printf`
line). So the "first install" below found the environment already
installed by the broken attempt (path shortened).

```
=== first install
✔ The default environment has been installed.

real    0m0.218s
user    0m0.054s
sys    0m0.011s
✨ Pixi task (check): python --version && R --version | head -n 1 && seqkit version
Python 3.12.16
R version 4.4.3 (2025-02-28) -- "Trophy Case"
seqkit v2.14.0
file                   format  type  num_seqs    sum_len  min_len  avg_len  max_len
SRR6357070_1.fastq.gz  FASTQ   DNA     50,000  5,050,000      101      101      101
813M    .pixi
105M    /work/<group>/<netid>/pixi-trial/cache
files in .pixi: 15524
files in cache: 19858
linked files: 12408
x86_64
pixi 0.84.2
=== reinstall from cache
✔ The default environment has been installed.

real    0m2.403s
user    0m0.171s
sys    0m0.410s
```

Meanings:

- Same versions and `seqkit stats` as every other run.
- **Reinstall from cache: 2.4 s on Nova `/work`, 57 s on Ceres
  `/project`**, for the same ~15,500 files. Shared storage speed varies a
  lot between sites, so the chapter says "can take minutes on some
  clusters", not a fixed number.
- **`.pixi` shows 813 MB on Nova vs 1.3 GB on Ceres and WSL**, with the
  same file count. Likely `/work` stores files compressed and `du`
  reports the space used on disk (inference, not checked). So sizes in
  the book should say "about 1.3 GB (less on some storage)".
- Same 12,408 hard-linked files: the cache-on-same-storage advice holds.
- First-install time not usable (already installed).
- **Lesson for the book:** long pasted blocks can break in the browser
  VS Code terminal; give readers short blocks, and write files with
  the editor or one-line commands rather than long heredocs.
:::

::: {.callout-note}
## Result: storage (2026-11-16, Nova login node)

Server address and group name replaced with placeholders.

```
$ quota -s
$ df -h ~
Filesystem                  Size  Used Avail Use% Mounted on
<server>:/stor014/home       14T  7.5T  6.1T  56% /home
$ df -h /work/<group>/
Filesystem                Size  Used Avail Use% Mounted on
novastor017:/stor017/<group>  143T   97T   47T  68% /work/<group>
```

Meanings: `quota -s` prints nothing, so Nova reports no per-user quota
that way; there is no `my_quotas` equivalent found yet. `df` shows the
size of the **shared** filesystem (all users' homes: 14 TB; the
group's `/work`: 143 TB), not a personal limit, so it can't answer
"how much may I use". Nova's home and `/work` limits must come from ISU's
docs (to look up for Appendix A). For the book: `df -h` is a useful
command but a common misreading ("I have 6 TB free in home").
:::

---

## Part 4 — pixi trial (any Linux or Mac)

This installs pixi and the draft book environment into **one test
folder** and measures it. It does not edit your `.bashrc`, and it keeps
pixi's cache in the test folder too, so it doesn't use home-directory
quota. Works in WSL Ubuntu, on a cluster compute node, or on an Apple
Silicon Mac.

1. Choose the base folder:
   - WSL or Mac: your home folder, `~`
   - SCINet: your project directory, e.g. `/project/<project_name>/<you>`
   - Nova: your work directory, e.g. `/work/<group>/<you>`
2. Copy this whole block, change the `BASE=` line, and paste it into the
   terminal:

   ```bash
   BASE=~                                   # <- change on a cluster
   T="$BASE/pixi-trial"
   mkdir -p "$T" && cd "$T"
   export PIXI_HOME="$T/pixi-home" PIXI_CACHE_DIR="$T/cache"
   export PIXI_NO_PATH_UPDATE=1 PIXI_NO_TELEMETRY=1
   curl -fsSL https://pixi.sh/install.sh | sh
   export PATH="$PIXI_HOME/bin:$PATH"
   mkdir -p book && cd book
   cat > pixi.toml <<'EOF'
   [workspace]
   name = "bioinf-book"
   channels = ["conda-forge", "bioconda"]
   platforms = ["linux-64", "osx-arm64", "osx-64"]

   [dependencies]
   python = "3.12.*"
   r-base = "4.4.*"
   seqkit = "*"
   nano = "*"

   [tasks]
   check = "python --version && R --version | head -n 1 && seqkit version"
   EOF
   curl -fLO https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
   time pixi install
   pixi run check
   pixi run seqkit stats SRR6357070_1.fastq.gz
   echo "--- sizes"
   du -sh .pixi "$PIXI_CACHE_DIR"
   echo "files in .pixi:  $(find .pixi | wc -l)"
   echo "files in cache:  $(find "$PIXI_CACHE_DIR" | wc -l)"
   uname -m; pixi --version
   ```

3. Copy **everything it printed** from `pixi --version` downwards (and
   the `real` time line) into the results table, or paste it into a text
   file for me.
4. Clean up:

   ```bash
   cd ~ && rm -rf "$T"
   ```

   (On a cluster, also type `exit` to end the interactive job.)

What we expect: the check prints Python 3.12, R 4.4 and seqkit; `seqkit
stats` shows `50,000` reads and `5,050,000` bases. On an Intel Mac the
environment was 1.1 GB with about 14,000 files; the cluster numbers tell
us whether that is a problem for home and project quotas.

---

## Part 5 — Apple Silicon Mac (optional)

If you can borrow an M-series Mac (Apple menu → About This Mac says
"Apple M1/M2/…"), run Part 4 there with `BASE=~`. Record the output and
`uname -m` (should say `arm64`).

---

## Still to do (as of 2026-11-16)

1. ~~SCINet first SSH login (2.1)~~ done 2026-11-16 (no `yes` prompt).
2. ~~Ceres Working Directory test (2.3)~~ done 2026-11-16: works.
3. ~~Nova (Part 3)~~ done 2026-11-16, except Nova's quota limits
   (look up in ISU docs).
4. **Optional:** Atlas OnDemand app list (is there a VS Code app?);
   Apple Silicon run (Part 5).

## Results

Fill in what you can; "not done" is fine. Paste long outputs below the
table or send them as text files.

| Check | Where | Result |
|:------|:------|:-------|
| nano / vim present | WSL Ubuntu | **Done 2026-11-14:** both present (`/usr/bin/nano`, GNU nano 8.7.1; `/usr/bin/vim`, Vim 9.1). See 1.2. |
| `code` on PATH (`where.exe code`, `which code`) | Windows + WSL | **Done 2026-11-14:** yes in both. See 1.3. |
| Extensions WSL + Remote - SSH | Windows VS Code | **Done 2026-11-14:** installed. See 1.4. |
| `code .` opens VS Code, status bar text | WSL | **Done 2026-11-14:** opened first time; `WSL: Ubuntu`; bash 5.3.9; `pwd` in Linux home. See 1.5. |
| Config file list from *Add New SSH Host* | Windows VS Code | **Done 2026-11-14:** `C:\Users\<you>\.ssh\config` (pick this), `C:\ProgramData\ssh\ssh_config` (system-wide); Windows files only, even from a WSL window. See 1.6. |
| `where.exe ssh`, `ssh -V` | Windows PowerShell | **Done 2026-11-14:** `C:\Windows\System32\OpenSSH\ssh.exe`, OpenSSH_for_Windows_9.5p2. Ubuntu `~/.ssh` not yet created (normal). See 1.6. |
| First SSH login prompts (secrets removed) | SCINet | **Done 2026-11-16 (Ceres, from Mac):** `brew install step`, `step ca bootstrap`, `step ssh config`; `ssh` opened Edge, already signed in to Login.gov, connected to `ceres-login-1`. No host-key `yes` prompt (step's `known_hosts`). See 2.1. |
| First SSH login prompts (secrets removed) | Nova | **Done 2026-11-16:** host-key prompt (`yes`), verification code, then password, banner (storage: `/work`, `/lustre`, `/ptmp` not backed up, `/lss` is). See Part 3. |
| nano / vim present, `$SHELL` | SCINet login node | **Done 2026-11-14 (Atlas):** `/bin/bash`; `/usr/bin/nano` (GNU nano 5.6.1), `/usr/bin/vim`; Rocky 9. See 2.2. |
| nano / vim present, `$SHELL` | Nova login node | **Done 2026-11-16:** `nova-login-2`; `/bin/bash`; `/usr/bin/nano` (GNU nano 5.6.1), `/usr/bin/vim`; lands in `/home/<netid>`. See Part 3. |
| Home and project quota (bytes, files) | SCINet | **Done 2026-11-14 (Atlas):** home 30 GB (fixed); project quota per project (1000 GB); `/90daydata` no quota, 90-day purge; `my_quotas` shows no file counts. **Ceres too:** home 29.8 GB; the same projects have separate, different quotas per cluster (5–10 TB on Ceres); Juno LTS listed on Ceres only. See 2.2. |
| Home and work quota (bytes, files) | Nova | **Partly done 2026-11-16:** `quota -s` empty; `df -h` shows shared filesystems (home 14 TB total, group `/work` 143 TB), not personal limits. Limits to look up in ISU docs. See Part 3. |
| VS Code route used, `hostname`, how ended | SCINet | **Done 2026-11-14 (Ceres):** OnDemand VS Code Server; `hostname` = `ceres20-compute-2` (compute node); terminal starts in the session's ID-named folder. Form: account, queue/QOS `ceres`, 2 cores, 8G, 2 h, Working Directory set to the project opens there (tested). Cancel stopped VS Code; tab closed by hand. See 2.3. |
| VS Code route used, `hostname`, how ended | Nova | **Done 2026-11-16:** OnDemand VS Code on compute node `nova18-69`, in `/work/<group>/<netid>`. VS Code Server app; form recorded (partition `nova`, tasks per node, memory, modules, Working Directory defaults to last used; code-server 4.97). Cancel on the card → Completed (Delete clears the card, kept 7 days otherwise); tab closed by hand. See Part 3. |
| pixi trial: time, sizes, file counts | WSL | **Done 2026-11-14:** 9.8 s; `.pixi` 1.3 GB / 15,524 files; cache 132 MB / 19,858 files (hard links); check and stats as expected. See 1.7. |
| pixi trial: time, sizes, file counts | SCINet | **Done 2026-11-14 (Ceres):** first-run time not usable (interrupted); reinstall from cache 57 s (storage-bound); `.pixi` 1.3 GB / 15,524 files; cache 114 MB; 12,408 hard-linked files. See 2.4. |
| pixi trial: time, sizes, file counts | Nova | **Done 2026-11-16:** reinstall from cache 2.4 s (Ceres 57 s); `.pixi` 813 MB (likely compressed storage) / 15,524 files; 12,408 hard links; first-install time not usable. See Part 3. |
| pixi trial | Apple Silicon | |

## Questions or surprises

- (write anything confusing here; it probably belongs in the chapter)
