---
title: "Chapter 9 — Working remotely"
subtitle: "Chapter plan · core · draft"
date: 2026-11-23
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
draft plan, 2026-11-19. Written while the Chapter 8 plan was being
drafted in a parallel session; the boundary with it is under *What this
chapter builds on*, confirmed from the Chapter 8 plan (see
*Decisions*). Decisions from the first open-questions round are
recorded the same day. Site facts were read from the SCINet and ISU pages on
2026-11-19 (listed under *Official links*). Outputs marked *captured*
were recorded on 2026-11-19 on macOS 15.7 Intel in a scratch folder,
with Homebrew rsync 3.5.0, Apple's `/usr/bin/rsync` (openrsync),
OpenSSH 9.9p2, tmux 3.7c, and GNU coreutils (gnubin first on `PATH`, as
after Chapter 1). Rows marked *to capture* need a Linux (Ubuntu/WSL)
machine or a cluster login (Nova, Ceres, Atlas). Revised 2026-11-22
after the Codex review (`chapter_09_codex_review.md`); what changed is
listed under *Decisions (2026-11-22, Codex review)*. SCINet and ISU
facts quoted in that revision were re-read from the official pages the
same day. Revised again 2026-11-23 after Austin ran
`chapter_09_checks.md` on WSL, Windows, Nova, Atlas, and Ceres: most
*to capture* items are now *captured* or *observed* (quoted in place),
and *Decisions (2026-11-23)* lists what changed.

## From `PLAN_CHAPTERS.md`

- Running one command over SSH (`ssh host command`); the "host key
  changed" warning
- SSH and SSH keys; `~/.ssh/config`; jump hosts (`ProxyJump`)
- Connection sharing (`ControlMaster`) so one sign-in serves many
  connections
- tmux / screen so work survives a dropped connection
- Moving data: `scp`, `rsync`, Globus, through the site's data transfer
  node (DTN), not the login node (Nova `novadtn`; SCINet `ceres-dtn`,
  `atlas-dtn`)
- Checksums to confirm a transfer
- Moving the project to the cluster: copy files, reinstall the
  environment, recreate links (Chapter 3's three steps)

## What this chapter builds on

Earlier chapters made promises this chapter must keep (each one is a
forward link already in the written text):

- **Chapter 1:** `fig-cluster-anatomy` (laptop → `ssh` → login node;
  shared storage reached by both login and compute nodes);
  "`@sec-working-remotely` covers connecting"; "everything before
  `@sec-working-remotely` runs on your laptop", so this is the first
  chapter that **assumes** a cluster account for its main path (readers
  without one still need a full route; see *Where commands run*).
- **Chapter 2 (`sec-book-setup-ssh`, `sec-book-setup-remote`):** a first
  `ssh <netid>@nova.its.iastate.edu`, the host-key question (type
  `yes`), `~/.ssh/known_hosts`, `hostname`, `exit`; `tbl-ssh-sites`
  (login hosts, VPN, sign-in, SCINet's `step`, DTN names); the pitfall
  "copying files through the login node"; a minimal `~/.ssh/config`
  (`Host`, `HostName`, `User`) after `mkdir -p ~/.ssh && chmod 700
  ~/.ssh`; "SSH keys … wait for `@sec-working-remotely`"; Windows: the
  Ubuntu terminal uses WSL's `~/.ssh/config`, VS Code Remote-SSH uses
  `C:\Users\<you>\.ssh\config`; `tbl-where-to-edit` row "Remote-SSH to a
  compute node: SSH keys (`@sec-working-remotely`), a held compute node".
  `fig-ssh-basics` already shows the connection; do not redraw it.
- **Chapter 3:** `md5sum -c` "after every download or transfer"
  ("`@sec-working-remotely` reuses it after copying to a cluster"),
  `FAILED` vs `FAILED open or read`; "Moving the project" in three steps
  (copy files; reinstall from `pixi.toml`/`pixi.lock`; recreate
  `data/ref`), "Transfer commands come in `@sec-working-remotely`";
  misconceptions `checksum-proves-correct`, `cluster-is-backed-up`.
- **Chapter 4:** pitfall "never post passwords, SSH private keys,
  tokens"; `tbl-common-errors` (`Permission denied`, `No such file`).
- **Chapter 5:** "it works over any connection … (`@sec-working-remotely`)";
  the cluster note (`pwd` shows the cluster home, `~` is the home of
  the machine you are on; "moving files between machines is
  `@sec-working-remotely`").
- **Chapter 6:** pipes, `>`, `2>`, `wc -c`, `grep` (used here without
  teaching them).
- **Chapter 7:** `chmod 700 ~/.ssh` explained, `600` for a private key
  (`tbl-chmod-recipes` row "private key (`600`)"); "nothing in
  `~/.bashrc` should print text … output there can break `rsync` and
  older `scp` (`@sec-working-remotely`)"; `tbl-startup-files` row `ssh
  host command`; "for work that must keep running, use the site's
  persistent sessions (`tmux`, `@sec-working-remotely`)"; misconception
  `closed-window-decides` ("Run long work in `tmux` … or as a scheduler
  job"); `ps -u "$USER"` on a login node; `type -a`.
- **Chapter 8 (drafted 2026-11-22):** variables, quoting, loops,
  arguments, `set -euo pipefail`, logging, numbered scripts, and a
  minimal git routine. This chapter writes **no** new scripts and uses
  no loops; commands are typed one at a time. If Chapter 8 ends with a
  numbered script that copies or downloads, this chapter can name it,
  not change it. Two bridges: (1) the tmux demonstration and exercise 4
  run the supplied `ticker.sh`, recognisable as a Chapter 8-style
  script, not one of Chapter 8's own scripts (those finish in seconds
  and need the project environment, which reaches the cluster only in
  §7); Chapter 8's plan agrees that this chapter owns tmux. (2) The
  project move in §7 ends by running Chapter 8's `pixi run bash
  src/run_all.sh` on the cluster, unchanged, as the proof that the
  moved project works.

Boundary with Chapter 10: this chapter keeps a **shell** alive with
tmux; holding resources (`srun`, `salloc`, interactive jobs), storage
tiers, quotas, and purges are Chapter 10. tmux on a login node is still
the login node, so the chapter says "light work only" and links
forward. Boundary with Chapter 20: downloads from the internet (`curl`,
`wget`, SRA/ENA, `fasterq-dump`) are Chapter 20; this chapter moves
files **between your own machines**. Boundary with Chapter 22: the same
kind of key logs in to GitHub; Chapter 22 adds it there (one forward
sentence here). Boundary with Appendix A: per-site recipes (exact
config blocks, VPN, Globus collection names, OnDemand file manager)
live in Appendix A; the chapter shows Nova and SCINet as worked
examples in one compact table and links there.

## Outcome and check

- **Outcome:** readers can log in to a cluster with less typing and
  fewer prompts by the route their site supports (a key with a
  passphrase and `ssh-agent` on Nova-like sites; SCINet's `step`
  certificate); read and extend `~/.ssh/config` (short names,
  `ServerAliveInterval`, connection sharing) and recognise a
  `ProxyJump` entry; keep a shell running through a dropped connection
  with tmux and find it again; copy files and folders to and from the
  cluster's DTN with `rsync` (trailing-slash rule, destination made
  first, dry run first, `--no-p --no-g` for project folders), `scp` for a single file, and Globus for large
  transfers; prove a transfer with `md5sum -c` on the receiving
  machine; and move the whole project, reference data included.
- **Check (cluster path):** copy the book's two raw FASTQ files and
  their checksum list from the laptop to the cluster through the DTN,
  then verify **on the cluster**. Four steps, in this order, all typed
  on the laptop (the aliases `nova` and `nova-dtn` come from §4):

  ```bash
  ssh nova 'mkdir -p /work/<group>/<netid>/bioinf-computing/data/raw'   # 1. make the destination
  rsync -avn --no-p --no-g ~/bioinf-computing/data/raw/ nova-dtn:/work/<group>/<netid>/bioinf-computing/data/raw/   # 2. dry run
  rsync -av  --no-p --no-g ~/bioinf-computing/data/raw/ nova-dtn:/work/<group>/<netid>/bioinf-computing/data/raw/   # 3. copy
  ssh nova 'cd /work/<group>/<netid>/bioinf-computing/data/raw && md5sum -c checksums.md5'   # 4. verify
  ```

  Step 1 makes the folder on the login node; step 3 sends the files to
  the DTN, and both see the same `/work` storage. Without step 1, rsync
  stops with `mkdir … failed: No such file or directory` and `code 11`
  (*captured* on the Mac, Nova, Atlas, and Ceres: rsync creates only the
  last folder of a destination, not a chain of missing parents;
  `--mkpath` exists on all three clusters, rsync 3.2.5–3.2.7, but not
  on older laptops, so the book does not rely on it). `--no-p --no-g`
  is the book's one recipe for project folders (*Decisions* 18; §6).
  Expected after step 4 (exact, *captured* on all three):
  `SRR6357070_1.fastq.gz: OK` and `SRR6357070_2.fastq.gz: OK`. On Atlas
  and Ceres, running step 3 again sends nothing. On Nova it currently
  re-checks all three files every time (`<f..t` in `-i` output),
  because files copied through `novadtn` this way get the copy time
  instead of the laptop's (*observed* 2026-11-22; asked ISU); the copy
  is still correct, and the text says so in one sentence. SCINet: the
  alias `ceres-dtn` or `atlas-dtn` defined in §4 (real names
  `ceres-dtn.scinet.usda.gov`, `atlas-dtn.hpc.msstate.edu`),
  `/project/<name>/<you>/…`, and `-z` added as in SCINet's page
  (`rsync -avz --no-p --no-g`).
- **Check (no-cluster path):** the same habits locally. In
  `~/bioinf-computing-ch09/`: (1) `rsync -a src dst1` and `rsync -a src/
  dst2` give the two trees below (*captured*); (2) `md5sum -c` on the
  copy prints `OK` for each file, and after one byte is appended,
  `FAILED`, the warning line, and status 1 (*captured*); (3) `ssh -F
  sample-config -G nova-dtn` on a supplied sample config in the scratch
  folder prints the `hostname` and `user` it sets, without connecting
  (*captured* with a test config). No-cluster readers never add
  fictitious accounts to their real `~/.ssh/config`.

  ```console
  dst1            dst2
  dst1/src        dst2/a.txt
  dst1/src/a.txt  dst2/sub
  dst1/src/sub    dst2/sub/b.txt
  dst1/src/sub/b.txt
  ```

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Log in to a cluster with an SSH key protected by a passphrase (or
   your site's certificate), and explain what the public and private
   halves are for and which one never leaves your laptop.
2. Write `~/.ssh/config` entries that give hosts short names, keep
   connections alive, and share one sign-in across connections, check
   them with `ssh -G`, and recognise a jump-host (`ProxyJump`) entry.
3. Start, detach from, and reattach to a tmux session, so work survives
   a dropped connection, and find the login node it lives on.
4. Copy files and folders between laptop and cluster through the data
   transfer node with `rsync` and `scp`, keeping files in the
   project's group, and choose Globus for large or many files.
5. Prove that a transfer arrived intact with `md5sum -c` on the
   receiving machine, and move the project (files, environment,
   reference link) so its pipeline runs on the cluster.

## Sections

Same pattern as Chapters 1–8: each section opens with something readers
run, then names the idea. Practice runs in `~/bioinf-computing-ch09` on
the laptop; the cluster steps use the reader's own cluster folder
(`/work/<group>/<netid>` on Nova, `/project/<name>/<you>` on SCINet;
storage areas themselves are Chapter 10). Named exceptions outside
scratch: `~/.ssh/` (keys and config; if `~/.ssh/config` exists, back
it up first under a dated name, `cp ~/.ssh/config
~/.ssh/config.bak-$(date +%F)`, and check with `ls -l ~/.ssh`), the
reference copy into the reader's cluster reference area in §7, and the
copy of `~/bioinf-computing` to the cluster in §7. Each section says
which steps need a cluster; the rest work on the laptop alone. Visual
items in brackets are specified under *Visuals and teaching aids*.

**Core route vs extensions.** The daily minimum, marked in the text:
connect by the site's route, check `hostname`, use a short alias,
start/detach/reattach a ticker in tmux, make the destination, dry-run a
DTN copy, verify it, and move the project. Connection sharing follows
as a useful extension; `ProxyJump` and IDE settings for compute nodes
are recognition only until Chapter 10 teaches allocations.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   Chapter 2 logged in once with a password and a code; daily work
   means many logins, long-running commands, and files moving both ways.
   Three machines matter from now on: the **laptop** (where `ssh`,
   `rsync`, and `scp` are typed), the **login node** (where you log in
   and edit), and the **DTN** (where files go in and out). We start
   every laptop transfer from the laptop, in both directions: a laptop
   behind a home or campus firewall usually cannot accept an incoming
   SSH connection. Who starts the connection is separate from which way
   the data flows (a "pull" typed on the laptop still moves files from
   the cluster to the laptop).
   `fig-three-machines` (extends `fig-cluster-anatomy` with the DTN on
   the same shared storage). Setup: `mkdir -p ~/bioinf-computing-ch09 &&
   cd ~/bioinf-computing-ch09`. macOS box: `brew install rsync tmux`
   (Apple's rsync is the older openrsync; tmux is missing), checked
   with `type -a rsync` and `rsync --version` (*Decisions* 2).
   Ubuntu 26.04 under WSL already has rsync 3.4.1, tmux 3.6, screen,
   and OpenSSH 10.2 (*captured* 2026-11-22), so Linux readers install
   nothing; one sentence says `sudo apt install rsync tmux` only if
   `type -a` finds nothing.
   No-cluster readers: which sections work
   locally (§2 fake-`ssh` demo, §3 key generation, §4 `ssh -G` on
   `sample-config`, §5 tmux, §6–§7 local rsync and checksums, exercise
   5's toy copy) and which are captured sessions.
2. **One command on another machine.** *Start hands-on (cluster):*
   `ssh nova hostname` and `ssh nova 'pwd; ls'` from the laptop: the
   command runs on the login node and its output comes back, with no
   prompt to `exit` (recalls `tbl-startup-files`, `ssh host command`).
   Quoting decides where expansion happens: `ssh nova "echo $HOME"`
   prints the **laptop's** home, `ssh nova 'echo $HOME'` the cluster's
   (*captured*: `/Users/<you>` vs `/home/<netid>`; quoting from Chapter
   5, deeper in Chapter 8). `ssh nova 'exit 3'; echo $?` prints `3`:
   the remote exit status comes back (*captured*). *Then
   name it:* `ssh host command` is the form `rsync` uses behind the
   scenes (and older, legacy `scp`), so text printed on standard output
   when the remote shell starts corrupts rsync's data stream. Current
   OpenSSH `scp` copies over SFTP, a different path; Chapter 7's
   wording ("`rsync` and older `scp`") stays. Test (keeps Chapter 7's
   promise): `ssh nova true | wc -c; echo "ssh status: ${PIPESTATUS[0]}"`
   must print `0` and `ssh status: 0` (zero bytes from a failed
   connection prove nothing). Nonzero bytes mean something prints on
   standard output at startup: the reader's own startup file is the
   usual cause, but a site's login scripts can also print; messages on
   standard error (the terminal, not the pipe) do not count
   (*captured*: `0` and status 0 on Nova, Atlas, and Ceres, even with a
   heavily customised `~/.bashrc` on Nova; Atlas prints a long MSU
   notice on every connection, but on standard error, so it is
   harmless and the text says so). What breaks, shown without a
   cluster or any startup-file edit (*captured*): a supplied fake `ssh` wrapper that
   prints one line before running the command; `rsync -av -e ./fakessh
   …` fails with `protocol version mismatch -- is your shell clean?`,
   `rsync error: protocol incompatibility (code 2)`, exit 2, and the
   same wrapper without the print copies fine. Readers run it
   themselves in `~/bioinf-computing-ch09` (*Decisions* 2026-11-22,
   10): the supplied file is made executable with `chmod u+x fakessh`
   (Chapter 7), and the copy is between two local folders, so no
   network is involved. *Then the host
   key again:* the `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`
   message, shown as captured text only (*captured* from a fake
   `known_hosts`: the full box, `Offending ED25519 key in …:1`, `Host
   key verification failed.`, status 255): the site changed its keys
   (check its announcements or published fingerprints, Nova's page) or
   something is in the way; never "fix" it by deleting `known_hosts`
   blindly; `ssh-keygen -R <host>` removes one entry once the site
   confirms. The **harmless** cousin, shown beside it: the first
   connection to a new name for the same machine (e.g. `nova-login-1`
   after `nova`) asks the ordinary host-key question again, and ssh
   adds `This host key is known by the following other names/addresses:
   … nova.its.iastate.edu` (*captured*; all Nova login names share one
   key). [`fig-three-machines`; pitfall: `.bashrc` that prints;
   self-check]
3. **SSH keys: logging in without retyping a password.** *Start
   hands-on (laptop, no cluster needed):* generate a key pair:

   ```bash
   ssh-keygen -t ed25519 -C "laptop-2026"
   ls -l ~/.ssh
   ```

   Readers accept the default file and **set a passphrase** (OpenSSH
   10.x asks `Enter passphrase for "<file>" (empty for no
   passphrase):` and `Enter same passphrase again:`; a mismatch prints
   `Passphrases do not match.  Try again.`; older versions omit the
   file name; *captured* on WSL); `ls -l`
   shows `id_ed25519` (`-rw-------`, 600) and `id_ed25519.pub`
   (`-rw-r--r--`); `cat ~/.ssh/id_ed25519.pub` shows one line
   (`ssh-ed25519 AAAA… laptop-2026`); `ssh-keygen -lf
   ~/.ssh/id_ed25519.pub` prints its fingerprint (*captured*, `256 SHA256:… laptop-2026
   (ED25519)`; must
   not overwrite an existing key: the text says to stop at "Overwrite
   (y/n)?" and answer `n`). *Then name it* with `fig-ssh-key-login`
   (stepped): the **public key** is a lock you may hand to any machine
   (it goes in `~/.ssh/authorized_keys` there); the **private key**
   stays on the laptop and proves you hold the key without being sent;
   the **passphrase** encrypts the private key on disk, so a stolen
   laptop file is useless alone. Permissions from Chapter 7: `~/.ssh`
   `700`, private key `600`, or ssh refuses it (*captured*: `WARNING: UNPROTECTED PRIVATE KEY
   FILE!` … `This private key will be ignored.`). *Then
   `ssh-agent`:* type the passphrase once per session with `ssh-add`;
   `ssh-add -l` lists loaded keys. macOS: `AddKeysToAgent yes` /
   `UseKeychain yes` in a `Host *` block at the end (Apple's OpenSSH
   only): the first login asks for the passphrase once, loads the key
   into the agent, and Keychain remembers it, so no `ssh-add` is needed
   (*observed*). WSL has no agent in a new terminal (`SSH_AUTH_SOCK=[]`,
   `Could not open a connection to your authentication agent.`);
   `eval "$(ssh-agent -s)"` starts one (`Agent pid …`), then `ssh-add`
   (*captured*); with OpenSSH 10.x, starting the agent itself creates
   `~/.ssh/` (`700`) and `~/.ssh/agent/` for its socket, so the text
   never says "you have no `~/.ssh` yet". *Then install the public
   key, by site* (`tbl-site-login`):
   - **Nova:** ISU documents key login as an alternative to the
     authenticator code: "Public key authentication does not use TOTP
     keys"; the passphrase unlocks the key. Keys need the ISU VPN
     "regardless of whether you are on or off campus". The key is copied
     with one ordinary (code + password) login, `ssh-copy-id -i
     ~/.ssh/id_ed25519.pub <netid>@nova-login-1.its.iastate.edu`, and
     key logins go to a **named** login node (`nova-login-1` or
     `nova-login-2`), because `nova.its.iastate.edu` "is not a single
     server". *Captured* 2026-11-22/23 (on the ISU VPN from home):
     `ssh-copy-id` asks for the code and password once and ends
     `Number of key(s) added: 1`; afterwards a login asks **only the
     key passphrase**, no code and no ISU password (`ssh -v`: `Server
     accepts key`, `Authenticated … using "publickey"`). The key
     worked on `nova-login-1`, `nova-login-2`, `novadtn`, and the
     round-robin name; the book still uses the named node (§5). With
     the key loaded, rsync to `nova-dtn` asks nothing, which also
     removes the problem below. Why keys matter so much on Nova: the
     authenticator code cannot be reused, so two connections within
     the same 30-second window fail on the second and ask again
     (*observed*: about two code-and-password rounds per connection
     when commands ran back to back; `There were 6 failed login
     attempts …` greets the next login, and the text says not to
     worry about it).
   - **SCINet:** use SCINet's documented certificate route (the `step`
     setup from Chapter 2, valid "once for the day (or every 16
     hours)") and skip manual `ssh-copy-id` here; SCINet's SSH page
     does not describe personal keys in `authorized_keys`. One sentence
     on what a certificate is: SCINet signs a public key and your
     identity for the day after the browser sign-in; the matching
     private key still stays on the laptop and is still what proves
     you hold it. Readers read the key section for the idea (and for
     GitHub, Chapter 22).
   - **Other sites:** check the site's page first; many allow keys, some
     forbid them or require MFA as well. Never copy a key's private half
     to the cluster, a USB stick, or a chat.
   Windows: the Ubuntu terminal and Windows' own ssh (used by VS Code
   Remote-SSH) are two separate SSH clients with separate `~/.ssh`
   folders, so each client gets its own site setup (*Decisions* 3):
   - **Nova-like sites (keys):** one key pair on each side
     (`ssh-keygen` in Ubuntu and in PowerShell); install both public
     keys in `authorized_keys`.
   - **SCINet (`step`):** `step` configures the SSH client that runs
     it, so a WSL setup does not configure Windows' ssh for VS Code.
     Windows' `step` needs the Windows `ssh-agent` service running
     ("If it is not running, SmallStepCLI will not work", SCINet's
     page). Main route for Windows SCINet readers: Open OnDemand,
     already supported in Chapter 2. A short note links SCINet's
     Windows `step` setup for readers with admin rights who want VS
     Code Remote-SSH from Windows.
   *Captured* on Windows 11: `OpenSSH_for_Windows_9.5p2`, at
   `C:\WINDOWS\System32\OpenSSH\ssh.exe`; the `ssh-agent` service is
   `Stopped` / `Disabled`, so only an administrator can turn it on.
   That supports OnDemand-first for SCINet and means "one passphrase
   per session" is promised for macOS and WSL only. A Windows home
   folder can contain a space (`C:\Users\<name with a space>`), which breaks
   unquoted paths in ssh options (`keyword controlpath extra arguments
   at end of line`); one tip says to quote such paths.
   [`fig-ssh-key-login`
   (stepped), `tbl-site-login`; key idea; misconception
   `public-key-is-secret`; pitfall: never share the private key;
   self-check]
4. **`~/.ssh/config`: names, keep-alives, one sign-in, jump hosts.**
   *Start hands-on (laptop, no cluster needed):* extend Chapter 2's
   entry, then ask ssh what it would do, without connecting:

   ```bash
   ssh -G nova-dtn | grep -E '^(hostname|user|serveraliveinterval) '
   ```

   (*captured* with a test config: `user netid`, `hostname
   novadtn.its.iastate.edu`, `serveraliveinterval 0` before the
   keep-alive line is added). Readers with a cluster edit their real
   `~/.ssh/config`; no-cluster readers write the same blocks into
   `~/bioinf-computing-ch09/sample-config` and use `ssh -F
   sample-config -G …`. The book's Nova block, built one option at a
   time (each one-line explanation; Appendix A holds the final per-site
   versions). First change from Chapter 2: its `HostName
   nova.its.iastate.edu` becomes the named node `nova-login-1`, because
   key logins (§3) and tmux sessions (§5) need one fixed login node.

   ```default
   Host nova
       HostName nova-login-1.its.iastate.edu

   Host nova-dtn
       HostName novadtn.its.iastate.edu

   Host nova nova-dtn
       User <netid>
       IdentityFile ~/.ssh/id_ed25519
       IdentitiesOnly yes
       ServerAliveInterval 60
       ControlMaster auto
       ControlPath ~/.ssh/cm-%C
       ControlPersist 10h
   ```

   - `IdentitiesOnly yes`: offer only this key. Without it ssh offers
     every key in the agent (GitHub, SCINet certificate, …) first
     (*observed* in `ssh -v`), and servers stop after a few wrong
     keys.
   - `ControlPath ~/.ssh/cm-%C`: `%C` is a fixed-length hash of user,
     host, and port. The longer `cm-%r@%h:%p` form failed on macOS
     when the folder path was long: `unix_listener: path "…" too long
     for Unix domain socket` (*captured*; the limit is about 104
     characters including a 17-character temporary suffix).
     OpenSSH's manual recommends `%C`.
   - The shared defaults block comes **after** the specific entries and
     names both aliases, so the login node and the DTN each get the
     same user, key, keep-alive, and sharing settings.
   - `ServerAliveInterval 60`: sends a small probe every 60 s, which
     can stop an idle connection being dropped by a firewall or VPN
     (ISU FAQ recommends it); it cannot bring back a VPN or network
     that has failed.
   - `ControlMaster`/`ControlPath`/`ControlPersist`: the first
     connection to a host signs in and becomes the **master**; later
     connections to the **same host** (a second terminal; `rsync` or
     `scp` to `nova-dtn` after a first sign-in there) reuse it with no
     code or password. This is one master per destination: the login
     node's master does not serve the DTN. `ControlPersist 10h` keeps
     the master open for up to 10 hours **after the last connection
     using it closes** (an idle timeout, not a guaranteed 10-hour
     sign-in); the site or the network can still end it sooner. ISU's
     FAQ recommends sharing for exactly "having to authenticate so
     often". *Captured* on Nova: the login node took one sign-in, a
     second `ssh` asked nothing, `ssh -O check` printed `Master
     running (pid=…)`; the DTN needed its own sign-in, then `rsync` and
     `scp` through it asked nothing. With a key and the agent, sharing
     matters much less; the text presents it as the route for readers
     who sign in with a code (or a site without keys). Check with
     `ssh -O check nova` and `ssh -O check nova-dtn`; close with `ssh -O exit <alias>`; `ssh -G nova-dtn |
     grep '^control'` confirms the DTN picked up the settings. Caution
     in one line: anyone with your laptop account can use the open
     connection while it lasts. **Windows:** connection sharing works
     in the Ubuntu (WSL) terminal, but Windows' own OpenSSH does not
     support `ControlMaster` (it relies on Unix sockets), so the three
     sharing lines go only in the WSL config, never in
     `C:\Users\<you>\.ssh\config`, where they break the connection:
     `getsockname failed: Not a socket`, `Read from remote host …:
     Unknown error`, no login (*captured*, OpenSSH for Windows 9.5p2).
   - For most options, the first value found wins in `~/.ssh/config`
     (ssh reads every matching block), so specific `Host` blocks go
     above shared and `Host *` blocks (same "first match" idea as
     `PATH`, Chapter 7). Exceptions that add up rather than stop at the
     first value stay out of the main text.
   *Then `ProxyJump` (recognition only, no live run):* some machines can
   be reached only through another (a compute node through the login
   node; a cluster behind a gateway). The text explains the two hops
   and shows the minimal config with a clearly labelled placeholder:

   ```default
   Host <allocated-node>
       ProxyJump nova
   ```

   with the one-off form `ssh -J nova <allocated-node>` beside it. The
   placeholder must be a node in the reader's **own active
   allocation**, which Chapter 10 teaches; the complete
   acquire → connect → release recipe (`salloc … sleep infinity`, the
   `Host` block, `scancel`) is taught in Chapter 10, linked from here;
   Appendix A keeps only the per-site config block (ISU's "Launching
   remote IDEs on Nova's compute nodes") and links to Chapter 10.
   Host-key checking stays on in this generic example. ISU's own
   recipe adds `ForwardAgent yes` and `StrictHostKeyChecking no` (its
   block uses `ProxyJump nova-login`, an alias for
   `nova-login-2.its.iastate.edu`); those are site choices, not part of
   a two-hop connection, and are explained beside that site recipe
   in Chapter 10's §5, only for that compute-node entry, never in
   `Host *`.
   SCINet: `step` writes its own `Include` block; do not edit it.
   What it contains (*captured*, exercise 3 asks readers to look):
   `Match exec "step ssh check-host %h"` (only SCINet hosts), `User
   <scinet.user>`, `UserKnownHostsFile ~/.step/ssh/known_hosts` (an
   `@cert-authority` line: trust host certificates SCINet signs), and
   `ProxyCommand step ssh proxycommand --provisioner keycloak %r %h
   %p`, which fetches a new certificate (the browser sign-in) when the
   old one has expired. This is the chapter's real example of a
   `ProxyCommand`. Two visible side effects: `atlas-dtn` prints
   `Certificate invalid: name is not a listed principal` on every
   connection and asks one ordinary host-key question (its host
   certificate does not list that name; harmless; reported to SCINet),
   while `atlas-login-1`/`-2` and Ceres ask nothing. If
   readers want short names, they add their own aliases above it:
   `ceres-dtn` → `ceres-dtn.scinet.usda.gov`, `atlas-dtn` →
   `atlas-dtn.hpc.msstate.edu` (and login aliases for
   `ceres.scinet.usda.gov` / `atlas-login.hpc.msstate.edu`). The short
   names work only after these entries exist; the chapter defines them
   before using them.
   Windows/VS Code: Remote-SSH reads only the Windows config (Chapter
   2); a jump-host entry must be in that file to work there.
   [`fig-proxyjump`, `tbl-ssh-config-options`; tip: `ssh -G`;
   self-check]
5. **tmux: work that survives a dropped connection.** *Start hands-on
   (laptop first, so it works without a cluster):* `tmux new -s ch09`,
   start the supplied `ticker.sh` (prints the time every 5 s; run with
   `bash ticker.sh`), detach with {{< kbd Ctrl-B >}}
   then {{< kbd D >}}, close the terminal window, open a new one,
   `tmux ls` (`ch09: 1 windows …`), `tmux attach -t ch09`: still
   running (*captured* on the Mac: `[detached (from session ch09)]`,
   `ch09: 1 windows (created …)`, no gap in the times). Then the same
   ticker on the login node, with Wi-Fi turned off for a minute instead
   of closing the window (*captured* on Nova and Atlas: the frozen
   terminal ends with `Connection to <host> closed by remote host.`,
   `Connection to <host> closed.`, `client_loop: send disconnect:
   Broken pipe`; after reattaching, the ticker had no gap). tmux's
   green status bar shows the node's name (`"nova-login-1"`), a free
   reminder of where the session lives. *Then name it* with
   `fig-tmux-detach` (stepped): the tmux
   **server** runs on the machine where you started it and owns the
   shell; your terminal is only a **client** attached to it; a dropped
   connection kills the client, not the server. *Then where it lives:*
   Nova has two login nodes and `ssh nova.its.iastate.edu` lands on
   either at random (ISU FAQ), so a session started on `nova-login-1`
   is invisible from `nova-login-2`. Habit: run `hostname` before
   detaching and put that node in `HostName` (as in §4's block).
   *Observed* routing (what we saw, not a count of nodes): Nova's
   round-robin name is one public address, and logins landed on
   `-1`/`-2` at random; Atlas's `atlas-login` is two DNS addresses
   (`-1`, `-2`), and both named nodes accept direct logins with no
   extra prompt; Ceres's name is one address and landed on
   `ceres-login-1`. On the wrong node, tmux 3.2a says `error
   connecting to /tmp/tmux-<uid>/default (No such file or directory)`
   if tmux never ran there, or `no server running on
   /tmp/tmux-<uid>/default` once a session has ended; newer versions
   word it `no server running on …`. Both mean "no session here".
   Installed (*captured*): Nova tmux 3.2a only (no screen, no module);
   Atlas tmux 3.2a, module `tmux/3.5a`, no screen; Ceres tmux 3.2a,
   module `tmux/3.3a`, and `screen`.
   *Then the limits:* tmux on a login node is still the login node:
   editing, short commands, the ticker; heavy work goes to a job
   (Chapter 10), which survives without tmux. Laptop transfers are not
   login-node work: they run on the laptop to the DTN (§6). tmux on the
   **laptop** keeps a laptop transfer's terminal safe from a closed
   window, but not from the laptop sleeping or going offline; for
   that, Globus (§6) manages the transfer. tmux survives client
   disconnects only while its server lives: a node reboot
   (maintenance), the session being killed, or site cleanup of
   long-idle processes still ends it (this sets up Chapter 10's
   difference between a persistent shell and an allocation; Nova's
   login banner announcing the next maintenance date is a real
   example). Scrolling: the mouse wheel does **not** scroll tmux by
   default; in iTerm2 it sends arrow keys, which step through shell
   history at a prompt and type `^[[A^[[B…` into a running program
   (*captured* on Nova); use `Ctrl-B [`. A
   handful of keys only (`tbl-tmux-keys`):
   new, detach, list, attach, kill, scroll (`Ctrl-B [` then `q`), new
   window and switch, split (one row each). `screen` in one row of the
   table and one sentence ("older, same idea; use whichever your site
   has"). tmux on the laptop: the §1 macOS box (Homebrew); already
   installed on Ubuntu 26.04/WSL (*Decisions* 2). [`fig-tmux-detach`, `tbl-tmux-keys`; key idea;
   misconception `closed-window-decides` revisited (with the mechanism);
   pitfall: wrong login node; self-check]
6. **Moving files: `rsync`, `scp`, and the DTN.** *Start hands-on
   (laptop, no cluster):* in `~/bioinf-computing-ch09/`, build `src/`
   (two small files, one subfolder) with one supplied block, then:
   - `rsync -av --dry-run src/ dst3`: lists what would be sent, ends
     with `(DRY RUN)`, and creates nothing (*captured*).
   - `rsync -av src/ dst3`: copies; add `src/c.txt` and rerun: only
     `c.txt` is sent (*captured*), because rsync compares and sends only
     what changed.
   - The trailing slash: `rsync -a src dst1` makes `dst1/src/…`;
     `rsync -a src/ dst2` puts the **contents** in `dst2/` (*captured*,
     `fig-rsync-slash`). Rule: slash on the source means "what is inside".
   *Then remote:* the same command with `host:path` on one side, always
   typed on the laptop, always to the DTN alias (`nova-dtn:`, or
   `ceres-dtn:` / `atlas-dtn:` once §4's aliases exist), in both
   directions (upload raw data, download results). First make the
   destination folder (`ssh nova 'mkdir -p …'`, as in the check): rsync
   makes only the last folder of a destination path, not missing
   parents (*captured*: exit 11). `-a` keeps times and, on a plain
   destination, permissions (shown locally). **Project folders need
   `--no-p --no-g`** (*Decisions* 18): they are group folders with the
   setgid bit (`drwxrws---` on SCINet, `drwxrwsr-x` on Nova), so new
   files should get the project's group. *Captured* on all three:
   plain `-av` gives the copied files the reader's **personal** group
   (`domain users` on Nova, the user's own group on SCINet), and on
   Nova also clears the folder's setgid bit; `--no-p --no-g` keeps the
   project group and the setgid bit and uses the site's default modes
   (`-rw-r-----` on SCINet). This is SCINet's documented command
   (`rsync -avz --no-p --no-g`), and the book uses it for every site.
   Times: kept on Atlas and Ceres, so a second run sends nothing; not
   kept through Nova's `novadtn` (files get the copy time, so every
   run re-checks all files; correct, just slower; plain `-av` and a
   copy to the login node do keep them; cause unknown, asked ISU, one
   sentence in the text, revisit when ISU replies).
   Two separate steps: *bytes verified* (`md5sum -c`, §7), then
   *permissions set on purpose for this destination* (for example,
   protecting `data/raw/` with `chmod a-w` after verification, in the
   reader's own folder, keeping the group's read access; *captured* on
   Atlas: `dr-xr-s---` and `-r--r-----`, group still `proj-…`). `-v`,
   `--progress` or `-P` (resume a broken large copy with `--partial`,
   part of `-P`); `-n` before any copy you are unsure of. `--delete` is
   mentioned only in a pitfall:
   it makes the destination match the source by deleting extras, and
   with a wrong slash or swapped paths it deletes real data.
   `scp file host:path` for one quick file (newer OpenSSH copies over
   SFTP, so §2's startup-file problem applies to rsync and legacy
   `scp`, not to it; one line; SCINet also advises against `scp -r`
   for folders into `/project`, because the setgid bit is not
   inherited); `sftp`/FileZilla/Cyberduck in the table (SCINet
   does not support FileZilla or WinSCP; Nova: FileZilla with one
   connection, or the code and password are asked again and again).
   *Then two macOS facts:* Apple's `/usr/bin/rsync` is openrsync
   ("rsync version 2.6.9 compatible", *captured* on macOS 15.7), which
   lacks some options; the book uses a current rsync (3.x) from
   Homebrew, installed in §1's macOS box (*Decisions* 2), and checks
   with `rsync --version` and `type -a rsync` (Chapter 7). *Then the DTN rule*
   again, now with the reason seen from the inside: the login node is
   shared, the DTN is built for transfers on the same storage, so the
   files appear in the same `/work` or `/project` folder. One line on
   when a DTN misbehaves: a transfer that fails with `connection
   unexpectedly closed` / code 255 right after signing in is worth one
   retry; if it keeps happening, tell the site (*observed*:
   `atlas-dtn-1` accepted the certificate and then closed every
   connection, 5 of 6 tries via the shared name, while `atlas-dtn-2`
   and `ceres-dtn` worked every time; reported to SCINet). *Then Globus
   (overview; optional exercise 6):* for large or many files, or
   cluster-to-cluster (Ceres ↔ Atlas), use the site's Globus collection
   (SCINet "SCINet-Ceres", "SCINet-Atlas", "SCINet-Juno"; Nova "Nova
   DTN") in a browser; Globus restarts failed transfers itself, and
   Globus Connect Personal makes a laptop an endpoint. Captured
   walk-through only (screens described, not screenshots); recipes in
   Appendix A. Small files on SCINet: Open OnDemand's file manager (under
   1 GB, SCINet's advice). [`fig-rsync-slash`, `tbl-transfer-tools`;
   key idea; pitfall: `--delete` and the slash; self-check]
7. **Proving the copy: checksums after a transfer, and moving the
   project.** *Start hands-on (laptop):* make a checksum list in `src/`
   and check the copy in `dst3/` (`a.txt: OK`, `sub/b.txt: OK`); append
   one byte to the copy and check again: `a.txt: FAILED`, `md5sum:
   WARNING: 1 computed checksum did NOT match`, status 1 (*captured*).
   Recall Chapter 3: compute on the **source**, check on the
   **receiving** machine, never recompute from the copy. *Then on the
   cluster:* `ssh nova 'cd … && md5sum -c checksums.md5'` (the chapter's
   check). *Then what each tool already checks:* rsync verifies each
   file it sends against a whole-file checksum, but chooses **which**
   files to send by size and time (exercise 2's stale-copy trap).
   Globus can verify; SCINet's Globus page recommends "Do NOT verify
   file integrity after transfer", which "approximately doubles the
   effective transfer speed". The chapter attributes that advice to
   SCINet, keeps verification on for the tiny teaching transfer, and
   makes `md5sum -c` the check either way (*to check* only the current
   default in the Globus web app). *What a checksum proves depends on
   where the list came from:* a list made from the source just before
   the copy proves the copy matches **that source**; it cannot reveal
   damage already present when the list was made. A list from the
   sequencing facility, ENA, or the original download (Chapter 3's
   `checksums.md5`) can also reveal an earlier change (Chapter 3,
   `checksum-proves-correct`). `rsync --checksum` (compare by content
   rather than size and time) in one sentence. *Then moving the project*
   (Chapter 3's three steps, now with commands, plus the reference data
   that lives outside the project):
   1. **Files.** `ssh nova 'mkdir -p /work/<group>/<netid>/bioinf-computing'`,
      then `rsync -avn` and `rsync -av --no-p --no-g --exclude .pixi
      --exclude results --exclude logs ~/bioinf-computing/
      nova-dtn:/work/<group>/<netid>/bioinf-computing/` (the
      environment is reinstalled, not copied: it is large,
      platform-specific, and full of small files that count against
      the inode quota of Chapter 10; `results/` and `logs/` are left
      behind so step 4 must make them itself); `md5sum -c` on
      `data/raw` on the cluster. The `.git/` folder from Chapter 8
      comes along, so the cluster copy has the same history; Chapter 22 shows the usual
      route instead (push to GitHub, clone on the cluster), and from
      then on the project moves that way while data still moves with
      rsync.
   2. **Environment.** `pixi install --locked` on the cluster login
      node, in the copied project (pixi itself and `PIXI_CACHE_DIR`
      in the work/project folder were set up in Chapter 2; this is
      light enough for a login node, as Chapter 2 already did).
      *Captured* reinstall times from the existing cache: Atlas 18 s,
      Ceres 48 s, but **Nova 25–41 minutes** (twice; first install
      into the empty cache 10 s; a fresh cache on local `/tmp` 7 s).
      The text keeps the `PIXI_CACHE_DIR` advice and adds one Nova
      note: a reinstall can take half an hour; start it and wait, or
      run it in an interactive job (Chapter 10) (*Decisions* 19; asked
      ISU; revisit when they reply).
   3. **Reference data, then the link.** `rsync -a` copies the
      `data/ref` symlink as a link, not the files it points to: the
      Chapter 3 reference lives outside the project, in
      `~/bioinf-shared/references/yeast_R64-1-1_test/`, so `data/ref`
      arrives pointing at a laptop path that does not exist (`ls -l`
      shows it; *captured* on the laptop, cluster side in
      `chapter_09_checks.md`). The reference needs its own copy:
      either use a matching site or lab reference **after checking its
      identity** (its `checksums.md5` or published checksums match the
      laptop's list), or copy this small folder through the DTN into
      the reader's cluster reference area, which mirrors the laptop's
      name inside their own work/project folder
      (`/work/<group>/<netid>/bioinf-shared/references/` on Nova,
      `/project/<name>/<you>/bioinf-shared/references/` on SCINet;
      not the small cluster home; `mkdir -p` first), and run
      `md5sum -c checksums.md5` there (both `genome.fa.gz` and
      `genes.gtf.gz` must say `OK`). No new download. Then replace the
      link with Chapter 3's rule: `ls -l data/ref` (inspect),
      `unlink data/ref` (no trailing slash), `ln -s <cluster reference
      folder> data/ref`, `ls data/ref/` (the four files). A plain
      `ln -s` over the existing link fails: `ln: failed to create
      symbolic link 'data/ref': File exists`, status 1, link unchanged
      (*captured* on Nova); and if the old link pointed at a folder
      that does exist, plain `ln -s` would quietly put the new link
      *inside* it.
   4. **Prove it runs.** `pixi run bash src/run_all.sh; echo $?`
      (Chapter 8) in the cluster copy: status `0`, then compare its outputs with the
      laptop's (`md5sum results/*.tsv`; *captured*: identical on Nova
      and Atlas). Check the exit status, not only the files: on Atlas
      the reference copy had failed, `02` stopped with `ERROR: missing
      or empty: data/ref/genes.gtf.gz`, yet the **stale `results/`
      copied from the laptop** still matched. That is why step 1 leaves
      `results/` and `logs/` behind. Raw-read checksums and a successful
      install alone do not prove the link or the pipeline work; the
      move is done only when destination, both checksum checks, the
      new link, the locked environment, and the pipeline all pass.
   [`tbl-move-project`; self-check]
8. **Summary and exercises.** Summary bullets; links forward to Chapter
   10 (holding a compute node and connecting to it with `ProxyJump`;
   storage tiers and quotas; jobs survive without tmux), Chapter 20
   (downloads from the internet), Chapter 22 (SSH keys on GitHub;
   moving code by clone), Appendix A (per-site recipes).

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, colours from theme classes only.
Colour roles (§2): the reader's laptop and files `given` (blue); allowed
routes and matching checksums `good` (green); refused routes, the
private key's "never leaves" boundary, and `--delete` `warn`; site
machines neutral (`ink`, `line`, `muted`). Reuse shapes from
`fig-cluster-anatomy` (Chapter 1), `fig-ssh-basics` and
`fig-remote-ssh` (Chapter 2).

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-three-machines` | 1 | static | Laptop, login node, DTN, compute nodes, shared storage. Arrows: laptop → login node "ssh: log in, edit, submit"; laptop → DTN "rsync, scp: connection started here", with a double-headed data arrow beside it ("files go both ways"); login → compute "jobs (Chapter 10)"; login and DTN both on the same storage. A small note at the laptop: "behind a firewall: usually cannot accept incoming SSH", not a crossed-out arrow. Globus is named in a caption line, not drawn as an SSH arrow. |
| `fig-ssh-key-login` | 3 | stepped (5 steps) | (1) `ssh-keygen` makes a pair on the laptop: private key locked by the passphrase, public key; (2) the public key is copied once to `~/.ssh/authorized_keys` on the cluster (a password login); (3) at login the server sends a challenge; (4) the laptop signs it with the private key (the agent holds it unlocked), the server checks with the public key; (5) logged in. The private key never crosses the boundary line. SCINet note on the last frame: "`step` gives you a certificate for the day instead". |
| `fig-proxyjump` | 4 | static | Laptop → login node → compute node labelled `<allocated-node>` ("a node in your own allocation, Chapter 10"); one ssh command at the top (`ssh -J nova <allocated-node>`), the minimal config form underneath; a dashed `warn` line laptop → compute node "not reachable directly". Recognition figure, no live run. |
| `fig-tmux-detach` | 5 | stepped (4 steps) | (1) laptop terminal attached to a tmux session on `nova-login-1`, a command (the ticker) running inside; (2) connection drops: client gone, session and command keep running; (3) reconnect lands on `nova-login-2`: `tmux ls` finds nothing (`warn`; the captured `error connecting to /tmp/tmux-<uid>/default (No such file or directory)`); (4) `ssh nova-login-1`, `tmux attach -t ch09`: back. Caption: survives disconnects, not reboots or session cleanup. "Command"/"process", never "job" (no scheduler job is involved). |
| `fig-rsync-slash` | 6 | static | Two panels from the captured trees: `rsync -a src dst1` → `dst1/src/a.txt …`; `rsync -a src/ dst2` → `dst2/a.txt …`; the slash highlighted. Below, a small strip: second run sends only `c.txt`. |

Not used: Mermaid (the transfer decision is a table); screenshots of
Globus (described in text, with a link to the site's own guide).

### Interactive figure (Observable JS, optional)

- None in the first draft. Candidate if testers stumble on the slash
  rule: two toggles (slash on source, slash on destination) and the
  resulting tree. The destination slash makes no difference for an
  existing folder or a new one, which is itself a lesson (*captured*:
  `src2/ e1` and `src2/ e2/` give the same tree).

### Tables (§5)

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-site-login` | 3 | Site · how you prove who you are · keys? · host for key logins · VPN · Windows/WSL note · prompts per day — rows Nova (code + password per connection, often twice when connections come quickly because a code cannot be reused; or key + passphrase on the VPN: passphrase once, then nothing; `nova-login-1/2`; one key per client), SCINet (`step` certificate, 16 h; documented route is the certificate, skip `ssh-copy-id`; Windows needs the `ssh-agent` service, or use OnDemand), "your site" (check its page) |
| `tbl-ssh-config-options` | 4 | Option · what it does · example value · when you need it — `Host`, `HostName`, `User`, `IdentityFile`, `IdentitiesOnly` (offer only that key), `ServerAliveInterval` (probes; cannot restore a failed network), `ControlMaster`/`ControlPath`/`ControlPersist` (one master per host; `ControlPath ~/.ssh/cm-%C`; idle timeout; not in Windows' own OpenSSH), `ProxyJump` (recognition; Chapter 10), `ForwardAgent` and `StrictHostKeyChecking` (site recipes only, never `Host *`), `Include`, `AddKeysToAgent`/`UseKeychain` (macOS) |
| `tbl-tmux-keys` | 5 | Task · tmux · screen — new named session, detach, list, attach, kill, scroll back (`Ctrl-B [`; the mouse wheel does not scroll by default), new window / next window, split; a last row "on our clusters": Nova tmux only, Atlas tmux (+ module 3.5a), Ceres tmux (+ module 3.3a) and screen |
| `tbl-transfer-tools` | 6 | Tool · best for · resumes? · runs where · site notes — `rsync` (project folders: `-av --no-p --no-g`; SCINet adds `-z`), `scp` (one file; SCINet: not `scp -r` into `/project`), `sftp`/Cyberduck, FileZilla (Nova only; one connection), Globus (managed transfer; retries failures itself), Open OnDemand file manager (small files), Rclone (cloud storage; one row, linked) |
| `tbl-move-project` | 7 | Part of the project · copy it? · how · why — scripts, docs, `pixi.toml`/`pixi.lock` (copy); `data/raw/` (copy + `md5sum -c`); `.pixi/` (no: reinstall with `pixi install --locked`); reference folder outside the project (copy through the DTN, or use a site/lab copy after checking its checksums; `md5sum -c` both files); `data/ref` link (arrives dangling: `unlink`, then `ln -s` to the cluster copy); `.git/` (copied; Chapter 22 replaces this with clone); `results/`, `logs/` (not copied: `--exclude`; regenerate with `pixi run bash src/run_all.sh`, check status 0, compare MD5s); all copies with `--no-p --no-g` |

### Code (§6)

- Where each command runs: `filename="Terminal (laptop)"` for every
  `ssh`, `rsync`, `scp`, `ssh-keygen`, `ssh-copy-id`, `ssh -G`;
  `Terminal (login node)` inside an SSH session or tmux on the cluster;
  `filename="~/.ssh/config (laptop)"` for config blocks.
- Tier 2 (shown, not run at render) throughout. Local rsync, checksum,
  `ssh -G`, and tmux steps are real captures; cluster steps are
  captured sessions with user names, groups, and IP addresses replaced
  (`<netid>`, `<group>`, `<address>`). Key fingerprints and public keys
  in captures are from a throwaway key made for the book, never a real
  one.
- Placeholders in angle brackets, never invented names, as in Chapter 2.
- No `--delete`, `StrictHostKeyChecking no` in `Host *`, or
  `rm ~/.ssh/known_hosts` as something to run.

### Plots

None.

### Animation (manim)

None. The stepped key-login and tmux figures cover the sequences.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Pitfall | Text printed on standard output when the remote shell starts breaks `rsync` (and legacy `scp`); `ssh host true \| wc -c` must print 0, with ssh's own status 0 |
| 3 | Key idea | The public key is a lock you can give to any machine; the private key stays on your laptop, protected by a passphrase |
| 3 | Pitfall | Never copy, email, or paste a private key (`id_ed25519` without `.pub`); if it leaks, delete the pair and remove the public key from every `authorized_keys` |
| 4 | Tip | `ssh -G <host>` shows what ssh will do with your config, without connecting |
| 5 | Key idea | tmux keeps the shell on the remote machine; your connection only views it, so losing the connection loses the view, not the work |
| 5 | Misconception | `closed-window-decides` revisited, now with the fix |
| 5 | Pitfall | A cluster with several login nodes: note `hostname` before detaching, or your session seems to vanish |
| 6 | Key idea | A slash at the end of the source means "the contents of": `rsync src/ dst` |
| 6 | Pitfall | rsync does not make missing parent folders: `mkdir -p` the destination first (exit 11 otherwise) |
| 6 | Pitfall | `--delete` with a wrong path or slash deletes real files; dry-run first (`-n`) |
| 7 | Misconception | `transfer-finished-is-verified` (new) |

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: `ssh nova "echo $USER"` and `ssh nova 'echo $USER'` print
  different names on a machine where your user names differ. Which is
  the cluster's? (*The single-quoted one: double quotes let the laptop
  expand `$USER` before ssh sends the command.*)
- §3: A labmate asks for "your SSH key" to give you access to a server.
  Which file do you send? (*`id_ed25519.pub`, the public key; never the
  file without `.pub`.*)
- §4: Your config has `Host *` with `User guest` at the top and `Host
  nova` with `User <netid>` below. Which user does `ssh nova` use, and
  how do you check? (*`guest`: for most options the first value found
  wins. `ssh -G nova | grep '^user '`. Move `Host *` to the end.*)
- §5: You detached from tmux on Nova yesterday; today `tmux ls` says
  `no server running` (or `error connecting to …`). Two possible reasons? (*You landed on the other
  login node, or the session ended (node reboot, or the site cleaned it
  up). Check `hostname`; try the other node.*)
- §6: You run `rsync -a results nova-dtn:/work/<group>/<netid>/results`.
  Where do the files end up? (*In `…/results/results/`; use `results/`
  on the source.*)
- §7: `rsync` finished without errors. Do you still run `md5sum -c`?
  (*Yes: rsync may have skipped a file it thought unchanged, and a list
  from the facility or the original download also catches a file
  damaged or mixed up before this copy (a list made from the source
  just now cannot); it costs seconds for these files.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
material; each says whether it needs a cluster):

1. **The rsync slash and dry run (laptop).** Build the supplied `src/`
   tree; predict, then run, `rsync -a src dst1`, `rsync -a src/ dst2`,
   and `rsync -av -n src/ dst3`; compare with `find … | sort`. Add a
   file and show that a second run sends only it. Record predictions
   and results in `NOTEBOOK.md`.
2. **Catch a damaged copy (laptop).** Make a checksum list in `src/`,
   copy with rsync, check with `md5sum -c`; damage one copy (append a
   byte) and check again; then repair it with one rsync and recheck
   (`rsync -a` resends it because its size changed). Then the trap
   (*captured*): change one letter (same size) and keep the old time
   with `touch -r`; `rsync -a` sends nothing and the copy stays stale
   (`AAAA`) until `rsync -a --checksum` (`AAAB`). Lesson: rsync's quick
   check looks at size and time; `md5sum -c` looks at the bytes.
3. **A key and a config (laptop; cluster optional).** Make an ed25519
   key with a passphrase (skip if you have one), load it with
   `ssh-add` (macOS: the first login does it), and write config entries for your site's login host and
   DTN with `ServerAliveInterval` (with a cluster: in your real config,
   after the dated backup; without one: in `sample-config`, checked
   with `ssh -F sample-config -G`); prove them with `ssh -G`. With a
   Nova-like cluster: install the public key and record what a login
   asks with the key (passphrase once, then nothing). If you sign in
   with a code instead, record how many prompts two quick logins give
   with and without `ControlMaster`, for the login node and for the
   DTN (`ssh -O check` on each). SCINet: record which entries `step` wrote (`cat` the
   included file) instead.
4. **Survive a disconnect (laptop; cluster preferred).** Start a named
   tmux session, run the supplied `ticker.sh` (prints the time every
   5 s), detach, close the terminal (or drop Wi-Fi when on a cluster),
   reconnect, and reattach; record `hostname` and `tmux ls`. Kill the
   session at the end (`tmux kill-session -t ch09`).
5. **Move the project (cluster; the check).** Make the destination,
   dry-run, then copy `~/bioinf-computing` to your cluster folder
   through the DTN with `--no-p --no-g` and without `.pixi/`,
   `results/`, and `logs/`; verify `data/raw` with `md5sum -c`
   on the cluster; copy (or identify and check) the reference folder
   and verify both reference files; replace `data/ref` (`ls -l`,
   `unlink`, `ln -s`, `ls data/ref/`); run `pixi install --locked`
   (Nova: allow half an hour); run `pixi run bash src/run_all.sh`,
   check that it exits `0`, and compare `md5sum results/*.tsv` with the
   laptop's. No-cluster readers: copy into
   `~/bioinf-computing-ch09/fake-cluster/`, where a link back to the
   laptop's reference would still resolve and hide the problem. So in
   a **toy copy** (never the real project), point the link at a
   deliberately nonexistent path, see `ls data/ref/` fail, then replace
   it; and explain why a local simulation cannot reproduce a different
   filesystem.
6. **Globus (optional; SCINet or Nova account).** Install Globus
   Connect Personal on the laptop, transfer the two FASTQ files to your
   site's collection ("SCINet-Ceres", "SCINet-Atlas", or "Nova DTN"),
   and check them with `md5sum -c` on the cluster. Record whether
   verification was on in the transfer settings (SCINet recommends
   turning it off for speed; for this tiny transfer, leave it on).

## Examples and data

- Toy examples, made by readers in `~/bioinf-computing-ch09` with one
  `mkdir`/`printf` block: `src/a.txt`, `src/sub/b.txt`, later
  `src/c.txt`; `ticker.sh` for tmux; `sample-config` (inactive Nova
  and DTN entries for `ssh -F … -G`).
- Reference folder `~/bioinf-shared/references/yeast_R64-1-1_test/`
  from Chapter 3 (genome, GTF, `checksums.md5`, `README.md`), copied to
  the cluster in §7; already listed in `data/README.md`.
- Running dataset: `~/bioinf-computing/data/raw/SRR6357070_1.fastq.gz`
  and `_2` with their checksum list from Chapter 3, copied to the
  cluster; nothing new downloaded, so no new rows in `data/README.md`.
- Captured outputs (2026-11-19, macOS 15.7 Intel; Homebrew rsync 3.5.0,
  protocol 32; `/usr/bin/rsync` = openrsync, "protocol version 29 /
  rsync version 2.6.9 compatible"; OpenSSH_9.9p2, LibreSSL 3.3.6; tmux
  3.7c; `screen` present at `/usr/bin/screen`):
  - Trailing slash, both rsyncs: `rsync -a src dst1` → `dst1/src/a.txt`,
    `dst1/src/sub/b.txt`; `rsync -a src/ dst2` → `dst2/a.txt`,
    `dst2/sub/b.txt` (openrsync gave the same `dst4/src/…` layout).
  - `rsync -av --dry-run src/ dst3` → `sending incremental file list`,
    `created directory dst3`, `./`, `a.txt`, `sub/`, `sub/b.txt`, a
    `sent … received …` line, `total size is 4  speedup is 0.02 (DRY
    RUN)`, status 0; `dst3` not created.
  - After adding `c.txt`, `rsync -av src/ dst3` lists only `./` and
    `c.txt`.
  - `md5sum -c` → `a.txt: OK`, `sub/b.txt: OK`; after appending one
    byte → `a.txt: FAILED`, `sub/b.txt: OK`, `md5sum: WARNING: 1
    computed checksum did NOT match`, status 1.
  - `ssh -F cfg -G nova-dtn` → `user netid`, `hostname
    novadtn.its.iastate.edu`, `port 22`, `controlmaster false`,
    `serveraliveinterval 0` (no connection made).
  - Destination slash makes no difference: `rsync -a src2/ e1` and
    `rsync -a src2/ e2/` give the same tree; `rsync -a src2 newdir/`
    still makes `newdir/src2/…`.
  - Same-size change with the old time kept: `rsync -a` sends nothing
    (copy stale); `rsync -a --checksum` resends it.
  - Fake `ssh` wrapper that prints one line: `protocol version mismatch
    -- is your shell clean?`, `(see the rsync manpage for an
    explanation)`, `rsync error: protocol incompatibility (code 2) at
    compat.c(625) [sender=3.5.0]`, exit 2.
  - `rsync -a` of a symlink: arrives as a link with the same target
    text (`ref -> /Users/someone/refs/R64`).
  - Missing destination parents (2026-11-22, rsync 3.5.0; also
    reproduced by the Codex review with openrsync): `rsync -a src/
    dest/x/y/` with no `dest/` → `mkdir "…/dest/x/y" failed: No such
    file or directory (2)`, `rsync error: error in file IO (code 11)`,
    exit 11.
  - `ssh-keygen -t ed25519 -C laptop-2026` (throwaway key):
    `Generating public/private ed25519 key pair.`, two "saved in"
    lines, `The key fingerprint is:` `SHA256:… laptop-2026`, randomart;
    modes `-rw-------` / `-rw-r--r--`; `ssh-keygen -lf` → `256 SHA256:…
    laptop-2026 (ED25519)`; existing file → `already exists.` /
    `Overwrite (y/n)?`.
  - Private key at `644`: the `WARNING: UNPROTECTED PRIVATE KEY FILE!`
    box, `Permissions 0644 for 'id_ed25519' are too open.`, `This
    private key will be ignored.`, `Load key "id_ed25519": bad
    permissions`.
- Captured 2026-11-22/23 on WSL, Windows, Nova, Atlas, and Ceres (all
  results in the results table of `chapter_09_checks.md`, quoted in
  the sections above): passphrase prompts; WSL agent lines and
  `~/.ssh/agent/`; Windows ssh version, agent service, and the
  `ControlMaster` error; Nova key login, `ssh-copy-id`, keys on all
  four names; prompt counts with and without sharing; the host-key
  warning (fake `known_hosts`) and the "known by other names" prompt;
  `ssh host true | wc -c` (0 on all three) with status; quotes and
  exit status over ssh; tmux versions, drop messages, `tmux ls`
  wordings, observed routing, direct logins; rsync versions and
  `--mkpath`; `mkdir -p` + dry run + copy + `md5sum -c` on all three;
  group, mode, and time after `-av` vs `--no-p --no-g` on all three;
  `chmod a-w` keeping group read (Atlas); dangling link, `ln -s`
  "File exists", reference copy and replacement, `run_all.sh`
  matching the laptop (Nova, Atlas); `pixi install` reuse times;
  `step`'s config; the `atlas-dtn` principal warning and the
  `atlas-dtn-1` failures.
- Still to capture (small): Globus web app's current verification
  default (exercise 6; skipped for now); Windows `step` with the
  agent service turned on by an administrator (optional); whether a
  detached tmux session survives overnight; whether rsync, tmux, and
  openssh are in conda-forge for all three platforms; ISU's answers
  (novadtn times, pixi cache on `/work`) and SCINet's (`atlas-dtn-1`).
- Where commands run: laptop for every connection and transfer; login
  node inside SSH and tmux; DTN only as a transfer target (no
  interactive work there).

## Misconceptions

New entries for `misconceptions.yml`, added when this plan is agreed.
Existing entries revisited here already list `09-working-remotely`
(`run-on-login-node`, `remote-runs-on-laptop`, `closed-window-decides`);
add `09-working-remotely` to `checksum-proves-correct`.

- `public-key-is-secret`: "My SSH public key is a secret, and the
  private one is what I give to servers." The public key is meant to be
  shared (it goes on every server); the private key never leaves your
  laptop. Probe: which file goes into `authorized_keys` on the cluster?
  (`id_ed25519.pub`.) [key idea + self-check, §3]
- `tmux-on-login-is-a-job`: "Inside tmux on the login node I can run
  heavy analysis, because it keeps running." tmux keeps the shell alive,
  but it is still the shared login node; heavy work goes in a job
  (Chapter 10). Probe: you start a 6-hour alignment in tmux on the login
  node; what is wrong? (Login-node rules; it may be killed, and it slows
  everyone.) [text, §5; Chapter 10]
- `rsync-slash-doesnt-matter`: "`rsync src dst` and `rsync src/ dst` do
  the same thing." Without the slash rsync copies the folder itself
  into `dst`; with it, the folder's contents. Probe: the self-check in
  §6. [key idea + self-check, §6]
- `transfer-finished-is-verified`: "If the copy finished without an
  error, the files are fine." A finished transfer says nothing about a
  file already wrong at the source or damaged before this copy, and some
  tools let you turn verification off; check against the source's or
  facility's checksum list on the receiving machine. A list made from
  the source just before the copy proves agreement with that source
  only. Probe: §7's self-check. [misconception callout, §7]
- `rsync-a-copies-it-right`: "`rsync -a` keeps everything as it was,
  so it is always the safest way to copy." Into a group project folder
  it keeps the wrong things: the laptop's permission bits and your
  personal group, so the files do not get the project's group
  (*captured* on Nova, Atlas, and Ceres). Probe: after `rsync -av` into
  `/project/…`, `ls -l` shows your own group; what option fixes it?
  (`--no-p --no-g`.) [text, §6; Chapter 10 storage]
- `copy-to-login-node`: considered and **not** added: Chapter 2's
  pitfall already covers it as a rule; revisited in text only.

## Links to other chapters and books

- Builds on: Chapters 1–7 (see *What this chapter builds on*); Chapter
  8 (drafted) for scripts recognised but not written here, its
  `src/run_all.sh` (run unchanged after the move), and its `.git/`
  (copied with the project).
- Leads to: Chapter 10 (holding a compute node with `salloc`/`srun`;
  storage tiers, quotas, inode limits and why `.pixi` is not copied;
  jobs survive without tmux; the full acquire → `ProxyJump` → `scancel`
  route to a compute node, taught there, with Appendix A holding only
  per-site config blocks);
  Chapter 20 (downloads with `curl`/`wget`, SRA/ENA, checksums from
  repositories); Chapter 22 (an SSH key on GitHub); Chapter 23
  (reinstalling an environment on another machine); Chapter 26
  (running nf-core inside tmux or as a job; staging inputs to the
  cluster); Chapter 38 (cloud storage, Rclone); Appendix A (per-site
  config blocks, Globus collections, OnDemand file manager).
- Other books: Genomics and Transcriptomics assume readers can move
  data to the cluster and verify it; they link here.

## Official links to include

- OpenSSH manual pages (man.openbsd.org): `ssh(1)`, `ssh_config(5)`,
  `ssh-keygen(1)`, `ssh-agent(1)`, `ssh-add(1)`, `sftp(1)`, `scp(1)`
  (openssh.com for the project)
- rsync: rsync.samba.org and its man page (`rsync(1)`), especially the
  trailing-slash paragraph under *USAGE*
- tmux: github.com/tmux/tmux (wiki *Getting Started*); GNU Screen:
  gnu.org/software/screen
- Globus: docs.globus.org (transfer, Globus Connect Personal)
- GNU coreutils `md5sum` (already linked in Chapter 3)
- ISU: *Login to Nova with SSH client* (research.it.iastate.edu/
  login-nova-ssh-client), *Transferring files*, *Globus*, *FAQs*
  (multiplexing, multiple login nodes), *tmux*, *Launching remote IDEs
  on Nova's compute nodes*, *Nova SSH host key fingerprints*
- SCINet: *SSH login* (scinet.usda.gov/guides/access/ssh-login, updated
  2026-01-14; Windows `ssh-agent` service, Atlas login node names),
  *Data transfer* and its *Local* (scinet.usda.gov/guides/data/transfer/local:
  `rsync -avz --no-p --no-g`, DTN host names, setgid note on `scp -r`)
  and *Globus* (…/transfer/globus: "Do NOT verify file integrity after
  transfer") subpages (updated 2026-01-21; re-read 2026-11-22)
- OpenSSH `ssh_config(5)` anchors used in the text: `ControlPath`
  (the `%C` token), `ControlPersist`, `IdentitiesOnly`,
  `ServerAliveInterval`, `CertificateFile`, `ProxyJump`,
  `ProxyCommand`
- VS Code: *Remote Development using SSH* (jump hosts, keys) for the
  Remote-SSH route
- GitHub Docs: *Connecting to GitHub with SSH*, as the pointer to
  Chapter 22

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Verify each with
scite or the publisher, and fetch BibTeX from the DOI or official page,
before adding.

- Shotts, *The Linux Command Line* (2nd ed., No Starch; free at
  linuxcommand.org): its networking chapter covers `ssh`, `scp`, and
  `sftp` briefly; recurring Part II anchor.
- Software Carpentry / HPC Carpentry, *Introduction to High-Performance
  Computing* (carpentries-incubator; Zenodo DOI if one exists): its
  episodes on connecting and transferring files mirror §3–§6 for a
  generic cluster.
- The OpenSSH `ssh_config(5)` page: the authority for every config
  option (url + urldate).
- tmux wiki *Getting Started*: the official short guide, beyond the
  handful of keys in `tbl-tmux-keys`.
- Candidate journal piece, to search with scite: a *PLoS Comput Biol*
  "Ten simple rules" on data management or transfer that covers
  checksums and verified transfers; otherwise none.

## Austin's notes

-

## Decisions (2026-11-19, open questions round)

Austin's answers to the first round of open questions; the sections
above are updated to match.

1. **Boundary with Chapter 8: settled from its plan.** `chapter_08.md`
   says "Chapter 9 owns `tmux`" and leads to "running a long script
   under tmux"; it does not teach `rsync` or `scp`. So exercise 4 runs
   a script readers wrote in Chapter 8 (or the supplied
   `ticker.sh`, now an ordinary Chapter 8-style script), not a plain
   `ping`.
2. **rsync and tmux on the laptop: Homebrew, in a Chapter 9 box.**
   A short "macOS: install rsync and tmux" box at the start of the
   chapter (`brew install rsync tmux`, then `type -a rsync` shows
   Homebrew's first and `rsync --version` says 3.x). Chapter 1 stays as
   written; not added to `pixi.toml`, since these are laptop tools used
   outside the project folder. Ubuntu/WSL: `sudo apt install rsync
   tmux` if missing (checked 2026-11-22: Ubuntu 26.04 has both).
3. **Windows keys: one pair per side.** A key made in WSL for the
   Ubuntu terminal, and a second made in PowerShell (`ssh-keygen`) for
   Windows' own ssh, which VS Code Remote-SSH uses; both public keys go
   on the cluster. No shared key through `\\wsl$\`.
4. **The check copies to the project/work folder** (`/work/<group>/
   <netid>/bioinf-computing` on Nova, `/project/<name>/<you>/…` on
   SCINet), as Chapter 2's OnDemand Working Directory already does;
   Chapter 10 explains the storage tiers.
5. **Globus: overview plus an optional exercise.** Captured
   walk-through in §6; an optional exercise 6 (Globus Connect Personal,
   laptop → the site's collection) for readers with a SCINet or Nova
   account.
6. **`fig-tmux-detach` is a stepped SVG** (4 steps), per the series
   rule for processes shown step by step.

## Decisions (2026-11-22, Codex review)

From `chapter_09_codex_review.md`, accepted in full; the sections above
are updated. SCINet and ISU facts were re-read from the official pages
on 2026-11-22. Where these change a 2026-11-19 decision, the note says
so.

1. **Destination first.** Every remote copy (the check, §6, §7,
   exercise 5) makes the destination with `ssh <login> 'mkdir -p …'`,
   then `rsync -avn`, then `rsync -av`, then `md5sum -c` on the
   cluster. No reliance on `--mkpath`.
2. **The project move includes the reference data.** The reference
   folder from Chapter 3 lives outside the project and is copied (or a
   site copy identified by checksum) separately; `data/ref` is replaced
   with `ls -l` → `unlink` → `ln -s` → `ls data/ref/`; the move ends
   with `pixi run bash src/run_all.sh` on the cluster. The no-cluster
   exercise uses a toy copy with a deliberately broken link.
3. **Site-specific rsync.** SCINet notes use SCINet's documented
   `rsync -avz --no-p --no-g`; "bytes verified" and "permissions set on
   purpose" are separate steps. DTN short names (`ceres-dtn`,
   `atlas-dtn`) appear only after the reader defines the alias.
4. **Connection sharing on both hosts.** A shared `Host nova nova-dtn`
   defaults block after the specific entries; one master per host;
   `ControlPersist` described as an idle timeout and
   `ServerAliveInterval` as probes; "for most options, the first value
   found wins". This answers the old open question 1's DTN part.
5. **`ProxyJump` is recognition only** until Chapter 10: placeholder
   node, minimal block with host-key checking on; ISU's
   `ForwardAgent`/`StrictHostKeyChecking` explained beside its own
   recipe; acquire/connect/release together in Chapter 10 or Appendix
   A (settled by 11: Chapter 10).
6. **Authentication per client.** Refines 2026-11-19 decision 3: one
   key per side still holds for Nova-like sites; for SCINet each
   client needs its own `step` setup (Windows: the `ssh-agent`
   service), or Windows readers use OnDemand. SCINet wording: "use the
   documented certificate route; skip `ssh-copy-id`", and a
   certificate signs a key rather than replacing the private key.
7. **tmux runs the ticker, not a Chapter 8 script and not a transfer.**
   Changes 2026-11-19 decision 1: `ticker.sh` only (Chapter 8's
   scripts are too short and need the project environment). "Command"
   or "process", not "job"; tmux survives disconnects, not reboots or
   cleanup. SCINet's documented Atlas login nodes are cited as leads.
8. **The stdout problem is rsync's (and legacy scp's).** Modern
   SFTP-based `scp` is a different path; the `wc -c` test also reports
   ssh's exit status and does not blame startup files alone.
9. **Smaller changes:** network wording ("we start transfers from the
   laptop; a laptop behind a firewall usually cannot accept incoming
   SSH") replaces "the cluster cannot reach your laptop", and the
   figure's crossed-out arrow; checksum claims tied to where the list
   came from; SCINet's Globus advice quoted and attributed; "second
   run resends no file contents"; the no-cluster route uses
   `sample-config` with `ssh -F`; config backup gets a dated name; a
   core route is marked through the chapter.

Austin's choices on the remaining open points (2026-11-22, interactive
round):

10. **Fake `ssh` demo: readers run it** (§2), with the supplied wrapper
    in the scratch folder; it is the no-cluster route's hands-on look
    at a broken rsync stream.
11. **ProxyJump recipe in Chapter 10.** Acquire → connect → release is
    taught in Chapter 10; Appendix A keeps only the per-site config
    block and links there. Done: `chapter_10.md` §5 now has the
    four-step block (acquire → find → connect → release), a
    self-check, and check 16. When Appendix A is next revised, its
    "Remote-SSH to a compute node" row should link Chapter 10 §5 as
    well as this chapter.
12. **Windows SCINet readers: OnDemand first.** The Windows `step` +
    `ssh-agent` service setup is a short linked note for readers with
    admin rights.
13. **Cluster reference area mirrors the laptop:**
    `bioinf-shared/references/` inside the reader's own work/project
    folder, not the cluster home.

The companion `chapter_09_checks.md` was updated the same day to match
(dependencies named, DTN probe in 3.4, documented vs observed login
nodes, dated backups, SCINet `--no-p --no-g` and permissions record,
Block E's `bash -c` test removed, new 3.7/4.5 whole-project move).

Final review (2026-11-22), small fixes, no change of direction:

14. §4 says explicitly that Chapter 2's `HostName nova.its.iastate.edu`
    becomes `nova-login-1`; `IdentityFile` moved into the shared block
    so the DTN uses the same key.
15. Windows' own OpenSSH has no `ControlMaster`: the sharing lines go in
    the WSL config only (Windows error captured 2026-11-23: `getsockname
    failed: Not a socket`).
16. The project move notes that Chapter 8's `.git/` is copied and that
    Chapter 22 replaces copying code with clone; `logs/` joins
    `results/` as regenerated; `pixi install` runs on the login node as
    in Chapter 2.
17. §1's no-cluster list now names the §2 demo and exercise 5's toy
    copy; the fake wrapper needs `chmod u+x`; links and summary point
    to Chapter 10's `ProxyJump` route.

## Decisions (2026-11-23, after the hands-on checks)

All checks in `chapter_09_checks.md` were run on 2026-11-22/23 (Mac,
WSL, Windows, Nova, Atlas, Ceres; Globus skipped). The sections above
now quote the results; what they changed:

18. **One rsync recipe for project folders: `rsync -av --no-p --no-g`**
    (Austin). Plain `-av` gave files the personal group on all three
    clusters (and cleared setgid on Nova); `--no-p --no-g` kept the
    project group everywhere and kept times on Atlas and Ceres.
    Through Nova's `novadtn` it loses times, so every re-run re-checks
    all files; one sentence in the text until ISU replies. SCINet's
    form adds `-z`. Plain `-a` stays for the local demonstrations.
19. **Nova `pixi install`: a note, not a new recipe** (Austin). Keep
    `PIXI_CACHE_DIR` in the work/project folder (Chapter 2, Appendix
    A); add that a Nova reinstall from the cache took 25–41 minutes
    (Atlas 18 s, Ceres 48 s), so start it and wait or use an
    interactive job. Revisit when ISU replies.
20. **The move leaves `results/` and `logs/` behind and checks
    `run_all.sh`'s exit status**, after a stale copied result hid a
    failed run on Atlas.
21. **Config details from the checks:** `ControlPath ~/.ssh/cm-%C`
    (the long form failed: socket path too long); `IdentitiesOnly
    yes` in the shared block; sharing lines never in the Windows
    config (captured error); keys presented as the main Nova route
    (they remove the code-reuse double prompts), sharing as the route
    for code users.
22. **Smaller text points:** WSL needs no install; OpenSSH 10.x prompt
    wording and `~/.ssh/agent/`; Windows agent service disabled and a
    space in the home path; harmless banners on stderr; the "known by
    other names" host-key prompt; both tmux "no session" wordings;
    tmux's status bar shows the node; the mouse wheel does not scroll;
    `step`'s config as the `ProxyCommand` example; the `atlas-dtn`
    certificate warning; retry once, then tell the site, for code 255
    right after sign-in.

23. **Final review after the checks (2026-11-23):** Chapter 8 marked
    as drafted; outcome, learning goal 4, `tbl-transfer-tools`,
    `tbl-move-project`, and `tbl-ssh-config-options` now carry
    `--no-p --no-g`, the `results/`/`logs/` exclusion, `IdentitiesOnly`,
    and `%C`; `tbl-site-login` gives the observed prompt behaviour;
    exercise 3 fits key users and code users; WSL needs no `apt`; new
    misconception `rsync-a-copies-it-right` (for `misconceptions.yml`
    when the plan is agreed); `ssh_config(5)` anchors for `ControlPath`,
    `IdentitiesOnly`, `ProxyCommand`.

Reported to the sites (drafts in Austin's private notes, not sent yet):
ISU (novadtn times; pixi cache on `/work`), SCINet (`atlas-dtn-1`
closes connections after authentication; `atlas-dtn` certificate
name). Austin's own Nova key login was set up during the checks.

Also for other chapters: Chapter 8's `run_all.sh` log names come out
literally `…_XXXX.log` (the X's are not at the end of the `mktemp`
template); told the Chapter 8 session via Austin.

## Open questions

The first-round questions are answered by the checks (Nova keys:
passphrase only, works on the DTN and all login names, VPN; SCINet:
tmux present, named Atlas nodes reachable, routing observed, sessions
survive a drop; SCINet permissions: project group and `-rw-r-----`,
`chmod a-w` keeps group read). Left open, waiting on others:

1. **ISU:** why files copied through `novadtn` without `-g` get the
   copy time, and why pixi's cache on `/work` is slow to reuse. If ISU
   gives a fix, update §6, §7, and Appendix A.
2. **SCINet:** `atlas-dtn-1` closing connections after sign-in. If it
   is fixed, drop the "observed" note in §6 (the retry line stays).
