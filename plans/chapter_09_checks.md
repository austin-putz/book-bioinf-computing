---
title: "Chapter 9: Hands-on checks for Austin"
subtitle: "What to run on WSL, Nova, and SCINet (Atlas, Ceres), and a little on your Mac"
date: 2026-11-23
---

These are the checks Chapter 9 (`chapter_09.md`) still needs from
machines I can't reach from here. The laptop-only behaviour (rsync,
checksums, `ssh -G`, `ssh-keygen` messages, a startup file that prints)
is already captured on the Mac (see *Done on the Mac*). What is left
needs **WSL/Windows**, the **real clusters**, or **you** (logins,
dropped connections, a browser for Globus).

**How to work.**

- Parts can be done in any order; skip what you can't do yet. Three
  small dependencies, each with a fallback: 3.6 uses the test key from
  3.3 (or make one with the line given there); 3.7 and 4.5 need your
  Chapter 3 project and reference on the laptop (and Chapter 8's
  `src/run_all.sh` for their last step, skipped if it is not there
  yet); 4.1's Block F reuses Block F from 3.2 with SCINet values.
- Cluster parts run in the same throwaway folder as Chapters 5–8,
  `~/bioinf-computing-checks` (on the laptop **and** on each cluster),
  plus one test folder in your cluster work/project space. Cleanup lines
  are at the end of each part.
- **Your real setup is never changed.** Keys are made as throwaway
  `test_ed25519` files inside the checks folder, never in `~/.ssh/`. The
  one exception is Part 3.3, which adds the **test** public key to your
  Nova `~/.ssh/authorized_keys` (backed up first, removed afterwards).
  No startup files, no `~/.ssh/config` edits: every option is given on
  the command line with `-o`. The project move (3.7, 4.5) goes into the
  checks folder, **not** over your existing cluster
  `bioinf-computing`.
- Everything is light enough for a login node: the two 2 MB FASTQ files,
  the small yeast reference, and a few tiny files. The one heavier step
  is `pixi install --locked` in 3.7/4.5 (about a minute with your cache
  already filled; deleted at cleanup).
- **Recording:** Blocks E and F write to files. Interactive bits (tmux,
  dropped Wi-Fi, prompts) are "write down what you saw"; a sentence each
  is enough.

**Priority** if time is short:

1. Part 3.3: Nova key login (is the password still asked? does the DTN
   take the key?), *Open questions* 1 in the plan.
2. Parts 3.5 and 4.2: tmux and login nodes on Nova and SCINet, *Open
   questions* 2.
3. Part 3.2 / 4.1: the real `mkdir -p` + `rsync` + `md5sum -c` check
   (the chapter's check), including SCINet's group and permissions
   (*Open questions* 3).
4. Parts 3.7 / 4.5: the whole project move (reference copy, link
   replacement, `run_all.sh`).
5. Everything else.

---

## Part 1: your Mac (two minutes)

You already have Homebrew rsync 3.5.0 and tmux 3.7c, so the install
box is captured. Only the interactive tmux bits are left.

### 1.1 tmux survives a closed window

```bash
tmux new -s ch09
```

Inside tmux, the ticker the chapter will supply:
`while true; do date +%T; sleep 5; done`. Press {{< kbd Ctrl-B >}}, let go,
then {{< kbd D >}}. Close the **whole Terminal window** (confirm if it
asks). Open a new window:

```bash
tmux ls
tmux attach -t ch09
```

**Record:** the exact `tmux ls` line (expected `ch09: 1 windows
(created …)`), the line tmux prints when you detach (expected
`[detached (from session ch09)]`), and that the ticker kept printing
(no gap in the times). Then {{< kbd Ctrl-C >}} and `exit` inside tmux
(or `tmux kill-session -t ch09`).

### 1.2 Scrolling in tmux

In a tmux session, run `seq 200`, press {{< kbd Ctrl-B >}} then
{{< kbd [ >}}, scroll with the arrow keys or Page Up, leave with `q`.

**Record:** did the mouse wheel scroll without that (tmux 3.7 default
is no)? Yes/no is enough.

---

## Part 2: WSL and Windows

### 2.1 Block W: WSL (Ubuntu terminal); paste this

```bash
mkdir -p ~/bioinf-computing-checks/ch09 && cd ~/bioinf-computing-checks/ch09 && {
h() { printf '\n=== %s\n' "$*"; }
h machine
grep PRETTY_NAME /etc/os-release; uname -r
h "installed by default?"
for p in rsync tmux screen ssh ssh-agent; do printf '%-10s ' "$p"; command -v "$p" || echo "MISSING"; done
rsync --version 2>&1 | head -n 1
tmux -V 2>&1
ssh -V 2>&1
h "agent running in a fresh terminal?"
echo "SSH_AUTH_SOCK=[$SSH_AUTH_SOCK]"
ssh-add -l 2>&1; echo "ssh-add status $?"
h "start an agent by hand"
eval "$(ssh-agent -s)"
ssh-add -l 2>&1; echo "ssh-add status $?"
ssh-agent -k
h "keygen dialogue (throwaway key, empty passphrase here)"
rm -f test_ed25519 test_ed25519.pub
ssh-keygen -t ed25519 -C "laptop-2026" -f ./test_ed25519 -N '' 2>&1 | head -n 4
ls -l test_ed25519 test_ed25519.pub
h "ls ~/.ssh before any ssh (fresh Ubuntu has none)"
ls -ld ~/.ssh 2>&1
} 2>&1 | tee ~/bioinf-computing-checks/blockW-wsl.txt
```

**Record:** keep `blockW-wsl.txt` and paste it into the chat.

What it settles: whether readers need `sudo apt install rsync tmux`
(*Decisions* 2: "to check what WSL's Ubuntu has by default"); whether
WSL starts an agent (expected: no, `SSH_AUTH_SOCK=[]` and `Could not
open a connection to your authentication agent.`); the Linux wording of
the keygen lines.

### 2.2 The passphrase prompts (by hand, WSL)

```bash
cd ~/bioinf-computing-checks/ch09
ssh-keygen -t ed25519 -C "laptop-2026" -f ./test2_ed25519
```

Type a short test passphrase twice.

**Record:** the exact prompt lines (expected `Enter passphrase (empty
for no passphrase):` and `Enter same passphrase again:`), and what it
says if you type two different passphrases.

### 2.3 Windows side (PowerShell, not WSL)

Open **PowerShell** (not as administrator):

```powershell
ssh -V
Get-Command ssh | Select-Object Source
Get-Service ssh-agent | Select-Object Status, StartType
mkdir $HOME\bioinf-computing-checks -Force
ssh-keygen -t ed25519 -C "windows-2026" -f $HOME\bioinf-computing-checks\test_ed25519 -N '""'
dir $HOME\bioinf-computing-checks
```

**Record:** the version, the path to `ssh.exe` (expected
`C:\Windows\System32\OpenSSH\ssh.exe`), the agent service's status and
start type (expected `Stopped` / `Disabled`, which needs an admin to
change), and whether `-N '""'` gave an empty passphrase without
prompting. This decides how §3 tells Windows readers to make their
second key (*Decisions* 3) and whether it can say "use the agent" on
Windows at all. It also matters for SCINet: Windows `step` needs this
service running ("If it is not running, SmallStepCLI will not work").
If the service is `Disabled`, the plan sends Windows SCINet readers to
OnDemand unless you want to test the admin route (optional: an admin
PowerShell, `Set-Service ssh-agent -StartupType Automatic; Start-Service
ssh-agent`, then SCINet's Windows `step` steps; record whether VS Code
Remote-SSH then reaches Atlas).

Then, still in PowerShell, whether Windows' ssh accepts connection
sharing (options on the command line, so your config is untouched; any
reachable host works, e.g. your Nova login):

```powershell
ssh -o ControlMaster=auto -o "ControlPath=$HOME\bioinf-computing-checks\cm-%r@%h-%p" -o ControlPersist=10m <netid>@nova-login-1.its.iastate.edu hostname
```

**Record:** the exact message (expected an error about Unix domain
sockets or `getsockname failed`, or the option being ignored), and
whether the login still worked. Decides the plan's "sharing lines in
the WSL config only" note.

Cleanup: `Remove-Item -Recurse $HOME\bioinf-computing-checks`.

---

## Part 3: Nova

You need the **ISU VPN** for 3.3 (keys need it on or off campus). Fill
in the four values at the top of Block F before pasting it.

### 3.1 Block E: on the Nova login node; paste this

Log in as usual (`ssh <netid>@nova.its.iastate.edu`) and paste:

```bash
mkdir -p ~/bioinf-computing-checks/ch09 && cd ~/bioinf-computing-checks/ch09 && {
h() { printf '\n=== %s\n' "$*"; }
h machine
hostname; grep PRETTY_NAME /etc/os-release
h versions
rsync --version 2>&1 | head -n 1
tmux -V 2>&1 || echo "no tmux"
screen --version 2>&1 | head -n 1 || echo "no screen"
ssh -V 2>&1
h "rsync has --mkpath? (the book does not rely on it)"
rsync --help 2>&1 | grep -c -- '--mkpath'
h "tmux as a module?"
module -t avail tmux 2>&1 | head -n 5
h "addresses behind the names (what DNS says, not a count of nodes)"
getent hosts nova.its.iastate.edu nova-login-1.its.iastate.edu nova-login-2.its.iastate.edu novadtn.its.iastate.edu
h "authorized_keys present? (not printed)"
ls -l ~/.ssh/authorized_keys 2>&1
h "group and setgid on your work folder"
ls -ld /work/<group>/<netid>
} 2>&1 | tee ~/bioinf-computing-checks/blockE-$(hostname -s).txt
```

**Record:** keep `blockE-<machine>.txt` and paste it into the chat.
The startup-file test is not here: a `bash -c` run on the login node
does not start the shell the way an `ssh host command` from the laptop
does, so the meaningful test is in Block F.

### 3.2 Block F: on your laptop (Mac or WSL); fill in, then paste

This is the chapter's check, plus the tests that must start on the
laptop. It uses your Chapter 3 project's `data/raw`.

```bash
U=<netid>                                   # your NetID
LOGIN=nova.its.iastate.edu                  # the round-robin name
DTN=novadtn.its.iastate.edu
DEST=/work/<group>/<netid>/bioinf-computing-checks/ch09   # your work folder
RS=(-av)                                    # SCINet: RS=(-avz --no-p --no-g)

mkdir -p ~/bioinf-computing-checks/ch09 && cd ~/bioinf-computing-checks/ch09 && {
h() { printf '\n=== %s\n' "$*"; }
h "ssh host command: bytes on stdout at startup (should be 0, ssh status 0)"
ssh "$U@$LOGIN" true | wc -c; echo "ssh status ${PIPESTATUS[0]}"
h "quotes decide where \$HOME expands"
ssh "$U@$LOGIN" "echo double: $HOME"
ssh "$U@$LOGIN" 'echo single: $HOME'
h "exit status comes back"
ssh "$U@$LOGIN" 'exit 3'; echo "status $?"
h "rsync to a destination whose parents do not exist (expect code 11)"
rsync "${RS[@]}" ~/bioinf-computing/data/raw/ "$U@$DTN:$DEST/missing/a/b/"; echo "rsync status $?"
h "make the destination on the login node, then rsync to the DTN: dry run, real, second run"
ssh "$U@$LOGIN" "mkdir -p $DEST/raw"
rsync "${RS[@]}" -n ~/bioinf-computing/data/raw/ "$U@$DTN:$DEST/raw/"
rsync "${RS[@]}"    ~/bioinf-computing/data/raw/ "$U@$DTN:$DEST/raw/"
rsync "${RS[@]}"    ~/bioinf-computing/data/raw/ "$U@$DTN:$DEST/raw/"
h "verify on the cluster; group and modes"
ssh "$U@$LOGIN" "cd $DEST/raw && ls -ld .. . && ls -l && md5sum -c checksums.md5"; echo "status $?"
h "a symlink arrives as a link"
mkdir -p linktest/data && ln -sfn /Users/nobody/refs/R64 linktest/data/ref
rsync -a linktest/ "$U@$DTN:$DEST/linktest/"
ssh "$U@$LOGIN" "ls -l $DEST/linktest/data; ls $DEST/linktest/data/ref/ 2>&1"
h "scp one file"
scp ~/bioinf-computing/data/raw/checksums.md5 "$U@$DTN:$DEST/"; echo "scp status $?"
} 2>&1 | tee ~/bioinf-computing-checks/blockF-nova.txt
```

Each `ssh` may ask for your code and password (that is part of what we
are counting). **Record:** keep `blockF-nova.txt`, and write down **how
many times** you were asked for a code and a password in total.

Expected: `0` bytes and `ssh status 0`; `double:` shows your
**laptop** home, `single:` the Nova one; `status 3`; the missing-parent
rsync fails with `mkdir … No such file or directory` and `rsync status
11`; the dry run ends `(DRY RUN)`; the second real run resends no file
contents (it may still list `./`); `SRR6357070_1.fastq.gz: OK`,
`SRR6357070_2.fastq.gz: OK`; the link shows `ref ->
/Users/nobody/refs/R64` and `No such file or directory`.

Permissions are a **record, not a pass/fail**: with plain `-av` on
Nova, `ls -ld .` probably shows `dr-xr-xr-x` (the laptop's read-only
mode carried over) and your laptop group is not kept (you are not in
it); write down the mode and group of `..` and `.` exactly. If the
copied `raw/` came out read-only, cleanup (3.8) needs `chmod -R u+w`
first.

### 3.3 Key login with a test key (priority 1)

On the VPN, from the laptop. This adds the **test** key to Nova and
removes it at the end.

```bash
cd ~/bioinf-computing-checks/ch09
ssh-keygen -t ed25519 -C "book-check-key" -f ./test_ed25519   # set a test passphrase
ssh <netid>@nova-login-1.its.iastate.edu 'B=~/.ssh/authorized_keys.bak-$(date +%F-%H%M); if [ -e ~/.ssh/authorized_keys ]; then cp ~/.ssh/authorized_keys "$B" && ls -l "$B"; else echo "no authorized_keys yet: nothing to back up"; fi'
ssh-copy-id -i ./test_ed25519.pub <netid>@nova-login-1.its.iastate.edu
```

Then try the key, telling ssh to use **only** it:

```bash
ssh -i ./test_ed25519 -o IdentitiesOnly=yes <netid>@nova-login-1.its.iastate.edu hostname
ssh -i ./test_ed25519 -o IdentitiesOnly=yes <netid>@nova-login-2.its.iastate.edu hostname
ssh -i ./test_ed25519 -o IdentitiesOnly=yes <netid>@novadtn.its.iastate.edu hostname
ssh -i ./test_ed25519 -o IdentitiesOnly=yes <netid>@nova.its.iastate.edu hostname
```

**Record, for each of the four lines:** which prompts appeared
(passphrase only? passphrase **and** ISU password? code?), and what it
printed or the error. ISU says keys go to a named login node because
`nova.its.iastate.edu` "is not a single server"; the fourth line shows
what readers see if they ignore that. Also: the exact output of
`ssh-copy-id` (it prints how many keys it added).

Then the agent (on a Mac it may offer the Keychain; say no):

```bash
eval "$(ssh-agent -s)"        # WSL only; the Mac already has one
ssh-add ./test_ed25519
ssh-add -l
ssh -i ./test_ed25519 -o IdentitiesOnly=yes <netid>@nova-login-1.its.iastate.edu hostname
ssh-add -d ./test_ed25519
```

**Record:** `ssh-add -l`'s line, and whether the login now asked
nothing (or only the password).

**Cleanup (do not skip):** remove the test key from Nova:

```bash
ssh <netid>@nova-login-1.its.iastate.edu "sed -i '/book-check-key/d' ~/.ssh/authorized_keys && grep -c book-check-key ~/.ssh/authorized_keys"
```

Expected last output `0`. (The backup line prints the dated backup's
name, or says there was nothing to back up; a fresh name each visit,
so an older backup is never mistaken for today's.)

### 3.4 Connection sharing (ControlMaster)

From the laptop, with options on the command line (no config edits).
Stands alone: it makes its own probe file. The transfer goes to the
DTN, as the chapter teaches.

```bash
cd ~/bioinf-computing-checks/ch09 && date > cm-probe.txt
DEST=/work/<group>/<netid>/bioinf-computing-checks/ch09
CM=(-o ControlMaster=auto -o "ControlPath=$HOME/bioinf-computing-checks/ch09/cm-%r@%h:%p" -o ControlPersist=10m)
ssh "${CM[@]}" <netid>@nova-login-1.its.iastate.edu hostname   # signs in (login master)
ssh "${CM[@]}" <netid>@nova-login-1.its.iastate.edu hostname   # should not ask
ssh "${CM[@]}" -O check <netid>@nova-login-1.its.iastate.edu
ssh "${CM[@]}" <netid>@novadtn.its.iastate.edu hostname        # different host: asks again? (DTN master)
ssh "${CM[@]}" -O check <netid>@novadtn.its.iastate.edu
ssh "${CM[@]}" <netid>@novadtn.its.iastate.edu "mkdir -p $DEST"
rsync -av -e "ssh ${CM[*]}" cm-probe.txt <netid>@novadtn.its.iastate.edu:$DEST/ 2>&1 | tail -n 2   # should not ask
ssh "${CM[@]}" -O exit <netid>@nova-login-1.its.iastate.edu
ssh "${CM[@]}" -O exit <netid>@novadtn.its.iastate.edu
```

**Record:** prompts on each line; both `-O check` lines (expected
`Master running (pid=…)`); whether the first DTN line asked again
(expected yes: one master per host); and whether the rsync to the DTN
then asked nothing (expected: it reuses the DTN master). This confirms
the plan's shared `Host nova nova-dtn` block. `cm-probe.txt` is removed
with the rest of `$DEST` in 3.8.

### 3.5 tmux and the two login nodes (priority 2)

1. `ssh <netid>@nova.its.iastate.edu`, run `hostname`, then
   `tmux new -s ch09` and the ticker inside
   (`while true; do date +%T; sleep 5; done`).
2. Detach ({{< kbd Ctrl-B >}} {{< kbd D >}}), then **turn Wi-Fi off**
   for about a minute (or put the laptop to sleep), then on again. Note
   what the frozen terminal finally prints (expected `client_loop:
   send disconnect: Broken pipe` or similar).
3. Log in again with the round-robin name **three times**, each time
   running `hostname; tmux ls`.
4. Then go straight to the node from step 1:
   `ssh <netid>@nova-login-<N>.its.iastate.edu`, `tmux attach -t ch09`.

**Record:** the hostnames you landed on in step 3 (what you observed,
not proof of how many nodes exist; ISU documents two), what `tmux ls`
said on the **other** node (expected `no server running on
/tmp/tmux-…`), and whether step 4 found the ticker still printing with
no gap. Then `tmux kill-session -t ch09`.

Optional: repeat step 2 **without** tmux (`ping -c 600 localhost`
straight in the SSH session), reconnect to the same node, and check
`ps -u "$USER" | grep ping`. Is it still running? (Chapter 7's "do not
count on it either way".) Optional too: leave a detached session
overnight and record whether it is still there next day.

### 3.6 "Host key changed" message (safe, fake file)

On the laptop. This makes ssh compare Nova's real key with a **fake**
`known_hosts` file, so you see the warning without touching your real
one. `ControlPath=none` stops it reusing an open connection.

```bash
cd ~/bioinf-computing-checks/ch09
printf 'nova-login-1.its.iastate.edu %s\n' "$(cut -d' ' -f1,2 test_ed25519.pub)" > fake_known_hosts
ssh -o UserKnownHostsFile=./fake_known_hosts -o GlobalKnownHostsFile=/dev/null \
    -o ControlPath=none <netid>@nova-login-1.its.iastate.edu true; echo "status $?"
```

**Record:** the whole message (expected `WARNING: REMOTE HOST
IDENTIFICATION HAS CHANGED!` … `Host key verification failed.`, status
255). Uses the test key from 3.3 as the "wrong" key; make one with
`ssh-keygen -t ed25519 -f ./test_ed25519 -N ''` if you skipped 3.3.

### 3.7 Move the whole project (priority 4)

The chapter's §7 move, end to end, into the checks folder (your real
cluster `bioinf-computing` is not touched). From the **laptop**; fill
in the first lines, then paste:

```bash
U=<netid>
LOGIN=nova-login-1.its.iastate.edu
DTN=novadtn.its.iastate.edu
DEST=/work/<group>/<netid>/bioinf-computing-checks/ch09
RS=(-av)                                    # SCINet: RS=(-avz --no-p --no-g)
REF=~/bioinf-shared/references/yeast_R64-1-1_test

cd ~/bioinf-computing-checks/ch09 && {
h() { printf '\n=== %s\n' "$*"; }
h "1. files: make the destination, dry run, copy without .pixi"
ssh "$U@$LOGIN" "mkdir -p $DEST/project $DEST/bioinf-shared/references"
rsync "${RS[@]}" -n --exclude .pixi ~/bioinf-computing/ "$U@$DTN:$DEST/project/" | tail -n 3
rsync "${RS[@]}"    --exclude .pixi ~/bioinf-computing/ "$U@$DTN:$DEST/project/" | tail -n 3
ssh "$U@$LOGIN" "cd $DEST/project/data/raw && md5sum -c checksums.md5"; echo "status $?"
h "the copied link, before the fix"
ssh "$U@$LOGIN" "cd $DEST/project && ls -l data/ref; ls data/ref/ 2>&1"
h "3. reference: copy the folder through the DTN and check it there"
rsync "${RS[@]}" "$REF" "$U@$DTN:$DEST/bioinf-shared/references/" | tail -n 3
ssh "$U@$LOGIN" "cd $DEST/bioinf-shared/references/yeast_R64-1-1_test && md5sum -c checksums.md5"; echo "status $?"
h "replace the link: inspect, unlink (no slash), link, list"
ssh "$U@$LOGIN" "cd $DEST/project && ls -l data/ref && unlink data/ref && ln -s $DEST/bioinf-shared/references/yeast_R64-1-1_test data/ref && ls -l data/ref && ls data/ref/"
h "what a plain ln -s over an existing link does (toy, in the checks folder)"
ssh "$U@$LOGIN" "cd $DEST && ln -s /nonexistent toylink; ln -s $DEST/bioinf-shared/references/yeast_R64-1-1_test toylink; echo \"ln status \$?\"; ls -l toylink; rm -f toylink"
} 2>&1 | tee ~/bioinf-computing-checks/blockG-nova.txt
```

Then **on the login node** (interactive, so pixi's output is visible):

```bash
cd /work/<group>/<netid>/bioinf-computing-checks/ch09/project
time pixi install --locked
ls src/run_all.sh && pixi run bash src/run_all.sh 2>&1 | tee ../run_all-nova.txt
```

On the laptop, for comparison: `cd ~/bioinf-computing && pixi run bash
src/run_all.sh 2>&1 | tee ~/bioinf-computing-checks/run_all-laptop.txt`.

**Record:** `blockG-nova.txt`; the dangling link before the fix; both
`md5sum -c` results (raw: two `OK`; reference: `genome.fa.gz: OK` and
`genes.gtf.gz: OK`, plus whatever else is listed); what the plain `ln
-s` over an existing link did (expected `File exists`, link unchanged);
the `pixi install` time; and whether the two `run_all` outputs agree
(skip if Chapter 8's `src/run_all.sh` does not exist yet).

### 3.8 Cleanup (Nova)

Do this after 3.7 if you ran it. On Nova: `chmod -R u+w
/work/<group>/<netid>/bioinf-computing-checks && rm -r
/work/<group>/<netid>/bioinf-computing-checks` (a copied read-only
`raw/` needs the `chmod` before `rm`; this also removes 3.7's `.pixi`),
and `rm -r ~/bioinf-computing-checks/ch09` when the Block E file is
saved. If the dated `~/.ssh/authorized_keys.bak-…` from 3.3 is no
longer needed and the test key is gone, delete it too.

---

## Part 4: SCINet (Atlas, then Ceres if you have time)

No `ssh-copy-id` test: the chapter follows SCINet's documented `step`
certificate route (*Decisions*, §3).

### 4.1 Block E and Block F

Run **Block E** on each login node as in 3.1 (change the `getent` line
to `getent hosts atlas-login.hpc.msstate.edu
atlas-login-1.hpc.msstate.edu atlas-login-2.hpc.msstate.edu
atlas-dtn.hpc.msstate.edu` or `getent hosts ceres.scinet.usda.gov
ceres-dtn.scinet.usda.gov`, and the folder line to `ls -ld
/project/<name> /project/<name>/<first.last>`).

Run **Block F** from the laptop with SCINet's documented rsync options:

```bash
U=<first.last>
LOGIN=atlas-login.hpc.msstate.edu     # or ceres.scinet.usda.gov
DTN=atlas-dtn.hpc.msstate.edu         # or ceres-dtn.scinet.usda.gov
DEST=/project/<name>/<first.last>/bioinf-computing-checks/ch09
RS=(-avz --no-p --no-g)
```

and save as `blockF-atlas.txt` / `blockF-ceres.txt` (change the `tee`
name). **Record:** the files, and how many browser sign-ins you were
asked for (expected: at most one a day). For *Open questions* 3, the
mode and group of `..` and `.` and the files: expected the project's
group (from the setgid folder), not your laptop group, and modes from
the cluster's defaults rather than the laptop's read-only bits. Then,
in the reader's own folder only, try the protection step:

```bash
ssh "$U@$LOGIN" "cd $DEST/raw && chmod a-w . * && ls -ld . && ls -l && cat checksums.md5 > /dev/null && echo group-readable-by-you"
```

**Record:** whether the group still has `r` (and `x` on the folder)
after `chmod a-w`. Cleanup needs `chmod -R u+w` first.

### 4.2 tmux and login nodes (priority 2)

Same as 3.5. SCINet's SSH page names `atlas-login-1.hpc.msstate.edu`
and `atlas-login-2.hpc.msstate.edu` (in its host-key notes) and only
`ceres.scinet.usda.gov` for Ceres; it says nothing about tmux or
routing. Evidence: Block E's `getent` lines, three logins with
`hostname` each time, and a direct login to each documented name.
**Record:** hostnames seen (observed routing, not a total count),
whether tmux exists (or only screen, or a module), whether
`ssh atlas-login-1.hpc.msstate.edu` / `-2` work directly (and on
Ceres, the name `hostname -f` printed), and whether the detached
session was there when you came back to its node.

### 4.3 What `step` wrote

On the laptop:

```bash
grep -n -A3 -i include ~/.ssh/config
ls -l ~/.step/ssh/ 2>&1
```

**Record:** the `Include` line(s) and the file names (not their
contents if they look like keys). This is what Exercise 3 asks SCINet
readers to look at.

### 4.4 Globus (optional, if you have time and a browser)

Install Globus Connect Personal on the laptop and send the two FASTQ
files to the "SCINet-Atlas" (or "SCINet-Ceres") collection, into
`$DEST/globus/`. Then on the cluster: `cd $DEST/globus && md5sum -c
../raw/checksums.md5`.

**Record:** the wording of the verification option as the web app
shows it today and whether it was on by default (SCINet's page already
documents its advice: "Do NOT verify file integrity after transfer",
for speed; leave it **on** for this tiny transfer); the `md5sum -c`
lines; anything confusing in the steps. One sentence each. Same on Nova
("Nova DTN") only if SCINet was not possible.

### 4.5 Move the whole project (priority 4)

As 3.7, with `LOGIN`, `DTN`, `DEST` from 4.1, `RS=(-avz --no-p
--no-g)`, `U=<first.last>`, and the `tee` name `blockG-atlas.txt` /
`blockG-ceres.txt`. Your existing `/project/…/bioinf-computing` is not
touched. One site is enough.

### 4.6 Cleanup (SCINet)

As 3.8, with `/project/<name>/<first.last>/bioinf-computing-checks`
(after 4.5 if you ran it).

On the laptop when all parts are done: `rm -r
~/bioinf-computing-checks/ch09`.

---

## Done on the Mac while writing this file (no action needed)

macOS 15.7 Intel, 2026-11-19: Homebrew rsync 3.5.0 (protocol 32),
Apple `/usr/bin/rsync` = openrsync ("rsync version 2.6.9 compatible"),
OpenSSH_9.9p2 / LibreSSL 3.3.6, tmux 3.7c, `/usr/bin/screen` present.
All recorded in `chapter_09.md` as *captured*. Highlights:

- **Trailing slash:** `rsync -a src dst1` → `dst1/src/…`; `rsync -a
  src/ dst2` → `dst2/…` (openrsync the same). A slash on the
  **destination** makes no difference: `src2/ e1` and `src2/ e2/` give
  the same tree, and `src2 newdir/` still makes `newdir/src2/…`. So the
  optional OJS figure would have only one toggle that matters.
- **Dry run, second run, `md5sum -c` OK/FAILED/status 1, `ssh -G`:** as
  in the plan.
- **Same-size change is missed:** a file edited to the same size with
  its old time kept (`touch -r`) is **not** resent by `rsync -a`; the
  copy stays stale (`AAAA`) until `rsync -a --checksum` (`AAAB`).
  Appending a byte (size changes) is resent. The plan's exercise 2 now
  says this.
- **A startup file that prints breaks rsync:** with a fake `ssh` that
  prints one line before running the remote command, `rsync -av -e
  ./fakessh …` gives `protocol version mismatch -- is your shell
  clean?`, `(see the rsync manpage for an explanation)`, `rsync error:
  protocol incompatibility (code 2) at compat.c(625) [sender=3.5.0]`,
  exit 2; the same without the print copies fine. This can be a
  no-cluster demo in §2.
- **Symlink:** `rsync -a` copies `data/ref` as a link with the same
  target text (`ref -> /Users/someone/refs/R64`), so on another machine
  it dangles. 3.2 confirms the cluster side.
- **Missing destination parents** (2026-11-22): `rsync -a src/
  dest/x/y/` with no `dest/` → `mkdir … failed: No such file or
  directory (2)`, `rsync error: error in file IO (code 11)`, exit 11.
  3.2 confirms it against a cluster rsync.
- **`ssh-keygen`:** `Generating public/private ed25519 key pair.`, the
  two "saved in" lines, `The key fingerprint is:` `SHA256:… laptop-2026`,
  the randomart box; files `-rw-------` and `-rw-r--r--`; `ssh-keygen
  -lf` → `256 SHA256:… laptop-2026 (ED25519)`; an existing file gives
  `./id_ed25519 already exists.` / `Overwrite (y/n)?`.
- **Unprotected key** (`chmod 644`, then `ssh-keygen -y`): the
  `WARNING: UNPROTECTED PRIVATE KEY FILE!` box, `Permissions 0644 for
  'id_ed25519' are too open.`, `It is required that your private key
  files are NOT accessible by others.`, `This private key will be
  ignored.`, `Load key "id_ed25519": bad permissions`.

---

## Results table

Fill in, or paste outputs into the chat and I'll fill it in.

| Check | Mac | WSL | Windows | Nova | Atlas | Ceres | Chapter 9 section it changes |
|:------|:---:|:---:|:-------:|:----:|:-----:|:-----:|:-----------------------------|
| tmux survives a closed window; detach line | yes: `[detached (from session ch09)]`; `ch09: 1 windows (created Sun Nov 22 15:30:08 2026)`; ticker no gap | — | — | — | — | — | §5 |
| Mouse scroll in tmux by default | no: wheel scrolls shell history (arrow-key history); `Ctrl-B [` + arrows works, counter shown | — | — | same: wheel sends arrow keys (`^[[A^[[B…` typed into the running ticker); use `Ctrl-B [` | — | — | §5 `tbl-tmux-keys` |
| rsync / tmux installed by default | done | yes (Ubuntu 26.04.1): rsync 3.4.1, tmux 3.6, screen, OpenSSH_10.2p1 | — | | | | §1 box, *Decisions* 2 |
| Agent running in a new terminal | done | no: `SSH_AUTH_SOCK=[]`, `Could not open a connection to your authentication agent.`, status 2; `eval "$(ssh-agent -s)"` → `Agent pid …`, `The agent has no identities.` ; starting the agent created `~/.ssh/` (700) and `~/.ssh/agent/` (OpenSSH 10.x socket folder) | | — | — | — | §3 |
| Passphrase prompt wording | | OpenSSH 10.2: `Enter passphrase for "<file>" (empty for no passphrase):`, `Enter same passphrase again:`; mismatch → `Passphrases do not match.  Try again.` and asks again | — | — | — | — | §3 |
| Windows `ssh.exe` path, agent service state | — | — | `OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2`; `C:\WINDOWS\System32\OpenSSH\ssh.exe`; ssh-agent `Stopped` / `Disabled`; `-N '""'` made a key with no prompt; home `C:\Users\<name with a space>` (space) | — | — | — | §3, *Decisions* 3 |
| Windows ssh with `ControlMaster`: error or ignored | — | — | error, no login: `getsockname failed: Not a socket`, `Read from remote host nova-login-1…: Unknown error`; unquoted `ControlPath` under `$HOME` with a space → `command-line line 0: keyword controlpath extra arguments at end of line` | — | — | — | §4 |
| Windows `step` with the agent service (optional) | — | — | | — | | | §3, *Decisions* 3 |
| tmux / screen version (or module) | done | tmux 3.6, screen present | — | tmux 3.2a; no `screen`; no tmux module (nova-login-2, AlmaLinux 9.6) | tmux 3.2a; no `screen`; module `tmux/3.5a` (atlas-login-2, Rocky Linux 9.6) | tmux 3.2a; `screen` present (`/usr/bin/screen`); module `tmux/3.3a` (ceres-login-1, RHEL 9.8) | §5 |
| rsync `--mkpath` available | done | yes (rsync 3.4.1 has it) | — | yes, rsync 3.2.5 (protocol 31) | yes, rsync 3.2.5 (protocol 31); OpenSSH_8.7p1 | yes, rsync 3.2.7 (protocol 31); OpenSSH_9.9p1 | §6 |
| Addresses behind the names (`getent`); documented vs observed nodes | — | — | — | `nova` → one public address; `nova-login-1`/`-2` → private (campus/VPN-only) addresses; `novadtn` → one public address | `atlas-login` → two addresses (DNS round robin; one is login-1); `atlas-dtn` → two addresses; `/project` is NFS4 (`atlas-vast-c1:/atlas/project`); project folder `drwxrws--- root proj-<project>`, own folder `drwxr-s---` | `ceres` → one address, landed on `ceres-login-1`; `ceres-dtn` → one address; `/project` NFS4 (`vast-vip1…:/project`); project folder `drwxrws--T root proj-<project>`, own folder `drwxr-s---` | §5 |
| `ssh host true \| wc -c` = 0, ssh status 0 | — | — | — | 0, ssh status 0 (custom `~/.bashrc` prints nothing to stdout) | 0, ssh status 0 (MSU notice banner goes to stderr, harmless) | 0, ssh status 0 | §2 |
| Double vs single quotes over ssh | — | — | — | double: `/Users/<you>` (laptop); single: `/home/<netid>` | double: laptop home; single: `/home/<user>` | single: `/home/<user>` | §2 self-check |
| Exit status comes back over ssh | — | — | — | `status 3` | `status 3` | `status 3` | §2 |
| Prompts per Block F run | — | — | — | 13 connections (Mac, password + TOTP, no sharing): ~24 `Verification code:` + ~28 `Password:` + 3 `'s password:`; most connections asked code + password twice (just-used code refused? to confirm) | none (step certificate); one ECDSA host-key question for `atlas-dtn` because every DTN connection prints `Certificate invalid: name is not a listed principal` (host cert lacks that name) and falls back to known_hosts | none (step certificate); `ceres-dtn` 6/6 connections OK | §3, §4 |
| Missing destination parents: code 11 | done | — | — | code 11: `mkdir … failed: No such file or directory (2)`, `main.c(780) [Receiver=3.2.5]` | code 11, `main.c(780) [Receiver=3.2.5]` | code 11, `main.c(806) [Receiver=3.2.7]` | §6, the check |
| rsync to DTN: dry run, real, second run resends nothing | — | — | — | yes with plain `-av`: dry run lists 3 files + `(DRY RUN)`; second run lists nothing. With `--no-p --no-g` a second run re-sends all three (`<f..t`), never settling | `-avz --no-p --no-g`: real copy OK, second run sends nothing, when the connection lands on `atlas-dtn-2`. `atlas-dtn-1` accepts the step certificate then closes the connection (`Connection closed by UNKNOWN port 65535`, status/code 255): 3/3 direct failures, 5 of 6 via the shared name. Site issue (reported to SCINet); not a reader step | `-avz --no-p --no-g`: dry run `(DRY RUN)`, copy OK, second run sends 0 files | §6, the check |
| `md5sum -c` on the cluster: two OK | — | — | — | two `OK`, status 0 | two `OK`, status 0 | two `OK`, status 0 | §7, the check |
| Mode and group after rsync (`-av` / SCINet `--no-p --no-g`) | — | — | — | Mac → `novadtn` → NFS4 `/work/<group>`: `-av` keeps times but files get `domain users` and the folder loses setgid; `--no-p --no-g`, `--no-p`, `--no-g`, `-rlt`, `-rlt --fsync` all keep the project group (except `--no-g`) but files get the copy time, so every rerun shows `<f..t` for all files. Same `-rlt` to the login node keeps both. DTN `touch -d` works. Cause unknown (DTN-side); see 3.4 notes | `/project` NFS4 (VAST). `--no-p --no-g`: times kept (14:26), group `proj-<project>`, files `-rw-r-----`, folder `drwxr-s---`. Plain `-av`: times kept, files group = personal group, `-rw-r--r--` | `/project` NFS4 (VAST). `--no-p --no-g`: times kept (14:26), group `proj-<project>`, `-rw-r-----`, folder `drwxr-s---`. Plain `-av`: times kept, group = personal, `-rw-r--r--` (same as Atlas) | §6, *Open questions* 3 |
| `chmod a-w` keeps group read (SCINet) | — | — | — | — | yes: `dr-xr-s---`, files `-r--r-----` group `proj-<project>` |  | §6, *Open questions* 3 |
| Symlink arrives dangling | done | — | — | yes: `ref -> /Users/nobody/refs/R64` (Block F) and the project copy `data/ref -> /Users/…/yeast_R64-1-1_test`; `ls data/ref/`: `No such file or directory` | yes: `ref -> /Users/nobody/refs/R64` (Block F) and project `data/ref -> /Users/…`; `No such file or directory` |  | §7 |
| Reference copied, `md5sum -c` both files OK | — | — | — | yes, through the DTN: `genome.fa.gz: OK`, `genes.gtf.gz: OK`, status 0 (project copy built from a Chapter 3-style layout in the checks folder; Austin's Mac project has `data/ref` as a plain folder) | yes (via `atlas-dtn-2`): `genome.fa.gz: OK`, `genes.gtf.gz: OK`; `ls data/ref/` lists the three files after `unlink` + `ln -s` |  | §7 |
| Plain `ln -s` over a link fails; `unlink` + `ln -s` works | — | — | — | yes: `ln: failed to create symbolic link 'data/ref': File exists`, status 1, link unchanged; `ls -l` → `unlink data/ref` → `ln -s` → `ls data/ref/` lists the three files |  |  | §7 |
| `pixi install --locked` time in the moved project | — | — | — | ~41 min in the rsync'd project (`real 40m59s`, `user 1.2s`, `sys 16m19s`) and 24.6 min in a fresh `mkdir` folder (setgid), both with `PIXI_CACHE_DIR` on NFS `/work` (cache reused; hard-linked; 13,003 files, 820 MB); fresh cache on local `/tmp`: 7.3 s. `/work` itself fast (1,000 files 0.2 s, 1,000 links 0.8 s). First install into the empty cache (2026-11-22) took 10 s. Cause: pixi reusing a cache on NFS (locking?). Also: rsync'd project lost setgid, so `.pixi` got group `domain users` | 17.9 s (`real 0m17.857s`) reusing `PIXI_CACHE_DIR` on `/project` (NFS4, VAST): no slowdown, unlike Nova | 47.9 s reusing `PIXI_CACHE_DIR` on `/project` (NFS4, VAST); first install was 54 s: no slowdown | §7 |
| `run_all.sh` output matches the laptop |  | — | — | yes: both result files have the same MD5 as on the Mac (`e1d81de7…`, `3b9c2b4c…`); 50,000 reads each; GTF md5 `504334f6…` (ran on nova-login-2) | yes after the reference arrived and `results/` was moved aside: `run_all status 0`, both MD5s match the Mac (`e1d81de7…`, `3b9c2b4c…`). First try had failed with `ERROR: missing or empty: data/ref/genes.gtf.gz` while the stale copied `results/` still matched: exclude `results/`, `logs/` from the move and check the exit status |  | §7, exercise 5 |
| Key login: passphrase only, or also password? | — | — | — | passphrase only: no code, no ISU password (`Server accepts key`, `Authenticated … using "publickey"`); `ssh-copy-id`: `Number of key(s) added: 1` after one code + password login. On the ISU VPN from home | — | — | §3, *Open questions* 1 |
| Key works on `nova-login-2`, `novadtn`, round-robin name | — | — | — | yes on all four: `nova-login-1`, `nova-login-2`, `novadtn`, and round-robin `nova` (landed on login-1). With the key in the agent (macOS `AddKeysToAgent yes` loads it at first passphrase) logins and the DTN ask nothing | — | — | §3, §4 |
| ControlMaster: second login silent; DTN asks once, then rsync silent | — | — | — | login master: 1 sign-in, second `ssh` silent, `Master running (pid=…)`; DTN asked again (its own master; code + password twice); rsync and `scp` through the DTN master silent (`scp status 0`). Book `ControlPath` under a long folder failed: `unix_listener: path "…" too long for Unix domain socket` (104 chars incl. 17-char suffix); `~/.ssh/cm-%C` works, socket removed on `-O exit` |  |  | §4 |
| tmux on the other login node: `no server running` | — | — | — | started on `nova-login-1`; round-robin logins landed -2, -2, -1, -2 (observed, random): on -2 `error connecting to /tmp/tmux-<uid>/default (No such file or directory)` (tmux 3.2a wording), on -1 `ch09: 1 windows (created …)`; `ssh -t nova-login-1 tmux attach -t ch09` → ticker had no gap across the drop. tmux status bar shows `"nova-login-1"`. Mouse wheel typed `^[[A`/`^[[B` into the running program | started on `atlas-login-2`; round-robin logins landed -2, -1, -1; only -2 listed `ch09: 1 windows …`; reattach via `ssh -t atlas-login-2… tmux attach -t ch09`: ticker had no gap. Status bar shows `"atlas-login-2.hpc.mss"`. tmux 3.2a wording: `error connecting to /tmp/tmux-<uid>/default (No such file or directory)` where tmux never ran, `no server running on /tmp/tmux-<uid>/default` after a session ended |  | §5, `fig-tmux-detach` |
| Direct login to a named login node (Atlas 1/2) | — | — | — |  | yes: `atlas-login-1` and `atlas-login-2` both work directly, no host-key question or certificate warning (step host cert covers them, unlike `atlas-dtn`) |  | §5 |
| Detached session still there next visit | — | — | — | yes after ~1 min Wi-Fi drop (next-day not tested) | yes after ~1 min Wi-Fi drop (next-day not tested) |  | §5 |
| Process without tmux after Wi-Fi drop | — | — | — | | | | §5, Chapter 7 link |
| Frozen-terminal message after a drop | — | — | — | `Connection to nova.its.iastate.edu closed by remote host.` / `Connection to nova.its.iastate.edu closed.` / `client_loop: send disconnect: Broken pipe` (Wi-Fi off ~1 min, VPN at home) | same as Nova: `Connection to atlas-login.hpc.msstate.edu closed by remote host.` / `… closed.` / `client_loop: send disconnect: Broken pipe` |  | §5 |
| "Host key changed" message, status 255 | — | — | — | yes, status 255: full `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` box, `Offending ED25519 key in ./fake_known_hosts:1`, `Host key verification failed.` Also: `nova-login-1`/`-2` each asked the host-key question on first use; same fingerprint as `nova`, ssh lists the other names | — | — | §2 |
| `step` `Include` line and files | — | — | — | — | Mac: `Include ~/.step/ssh/includes` → `~/.step/ssh/config`: `Match exec "step ssh check-host %h"` with `User <user>`, `UserKnownHostsFile ~/.step/ssh/known_hosts` (`@cert-authority *` line; `atlas-dtn` plain key added after the principal warning), `ProxyCommand step ssh proxycommand --provisioner keycloak %r %h %p` |  | §4, Exercise 3 |
| Globus verify option wording, default | — | — | — | | | | §6, Exercise 6 |
