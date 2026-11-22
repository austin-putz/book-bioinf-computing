---
title: "Chapter 9 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-22
---

Reviewed [chapter_09.md](chapter_09.md) against the repository and series
instructions, [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared theme style guide, relevant written material in Chapters 2–3
and 7, the Chapter 8 plan, and [the hands-on checks](chapter_09_checks.md).
Locations and line numbers refer to the plan as reviewed on 2026-11-22.
The source plan, checks file, and Austin's notes are unchanged.

**Overall assessment:** keep the sequence of remote commands, keys,
config, tmux, transfers, and verification. The local route is valuable,
and the distinction between the login node and DTN belongs here. The
largest practical gaps are preparing the receiving directories, moving
the reference data as well as its link, and making the config and
transfer recipes agree with the actual site and client being used.

## Corrections before drafting

### 1. Prepare the transfer destination before the chapter's check

**Priority: high. Locations:** outcome/check, lines 113–124;
section 6, lines 362–382; section 7, lines 408–418; exercise 5,
lines 568–573.

The check sends to
`/work/<group>/<netid>/bioinf-computing/data/raw/` without first
creating the parent directories. Ordinary `rsync -a` does not create
an arbitrary chain of missing destination parents. I reproduced an
exit-11 `mkdir … No such file or directory` failure locally with the
same nested-destination structure.

Add an explicit, labeled `mkdir -p` step on the cluster before the
dry run. A short SSH command to create the folder on the login node
can prepare the shared path; the subsequent data transfer still goes
through the DTN. This also makes the shared-storage relationship
observable. Do not depend on a newer `--mkpath` option being present on
every remote rsync.

The opening check also omits its own “dry run first” habit. Show the
preparation, `rsync -avn`, actual transfer, and receiving-side checksum
check in that order, or clearly identify the opening block as the final
check after setup rather than a block to paste immediately.

### 2. Move the reference directory, then replace the dangling link

**Priority: high. Locations:** section 7, lines 408–418;
`tbl-move-project`, line 468; exercise 5, lines 568–573.

The Chapter 3 reference lives **outside** the project, at
`~/bioinf-shared/references/yeast_R64-1-1_test/`. Copying
`~/bioinf-computing/` with `rsync -a` transfers the `data/ref` link, but
none of its target files. The plan correctly explains the resulting
broken link, then asks readers to recreate it without providing the
cluster's reference copy.

Complete the three-step move with a separate reference-data action:
use an existing matching site/lab reference **only after checking its
identity**, or copy this tiny reference directory through the DTN into
the reader's cluster reference area. Check its `checksums.md5` there,
including both `genome.fa.gz` and `genes.gtf.gz`. No new internet
download lesson is needed.

Show the replacement itself, rather than just `ln -s`: the copied
`data/ref` already exists, so a plain `ln -s target data/ref` does not
reliably replace it. Inspect it, `unlink data/ref` with **no trailing
slash**, then make the new link and check `ls data/ref/`. This reuses
Chapter 3's established rule.

Finish the move by running Chapter 8's `pixi run bash src/run_all.sh`
from the destination project and comparing both outputs. Raw-read
checksums plus a successful environment install do not prove that
the reference link or the project pipeline works.

For the no-cluster exercise, a link back to the laptop's original
reference will still resolve, hiding this failure. Use a deliberately
nonexistent target in a **toy copy**, or ask readers to identify that
the local simulation cannot reproduce a different filesystem. Keep
the real project link unchanged.

### 3. Make the SCINet recipe respect project permissions and host names

**Priority: high. Locations:** outcome/check, line 124;
section 6, lines 363–366; `tbl-move-project`; checks file, Block F's
expected read-only permissions and SCINet adaptation.

The plan promotes `rsync -a` preserving permissions as a universal
benefit. SCINet's own project-storage examples instead use
`rsync -avz --no-p --no-g`, and explain the significance of project
group/setgid inheritance. Follow that site's documented variant in
its note; do not promise identical permission bits on every destination.
[SCINet local-transfer guide](https://scinet.usda.gov/guides/data/transfer/local).

Keep the simple local `-a` demonstration. For the site-specific recipe,
separate “bytes verified” from “permissions deliberately set for this
destination.” If raw data should be protected against accidental writes,
apply the intended protection after verification in the reader's own
directory, in a way that retains the site's group access. The checks
file's unconditional `dr-xr-xr-x` expectation needs the same qualifier.

Also distinguish aliases from actual DNS names. The documented Atlas
DTN is `atlas-dtn.hpc.msstate.edu`; `atlas-dtn` works as a laptop
argument only after the reader defines that alias. Ceres uses
`ceres-dtn.scinet.usda.gov`. Provide each site's alias/config before
using the short name in the check. The SCINet guide above supports
those full host names.

### 4. Apply connection sharing to the DTN and explain its actual lifetime

**Priority: medium. Locations:** section 4, lines 280–306;
open question 1, lines 777–781; checks file, part 3.4.

The worked block enables connection sharing only for `Host nova`.
Its explanation then says later `rsync` and `scp` commands reuse that
sign-in, although the chapter correctly sends those commands to
`nova-dtn`, a different host with no sharing options. The open question
already identifies the mismatch. Fix the instructional block now;
real prompt counts can remain a capture task.

Add the sharing options to both relevant entries, or use a shared
`Host nova nova-dtn` defaults block placed after the specific entries.
Explain that this creates **one master per destination**, not a single
login-node connection serving the DTN. Confirm with `ssh -G` for each
alias and `ssh -O check` after connecting.

`ControlPersist 10h` is an **idle** timeout after no multiplexed clients
remain, not a guaranteed ten-hour sign-in validity period. Likewise,
`ServerAliveInterval` sends probes; it can help with idle connections
but cannot restore a failed VPN or network. Use those precise
descriptions. [OpenSSH config documentation](https://man.openbsd.org/ssh_config.5).

Change “first match wins” to “for most options, the first value found
wins”: SSH can apply multiple matching blocks. The existing `User`
self-check is good. Keep advanced/additive exceptions out of the main
path.

### 5. Keep the ProxyJump lesson usable before Chapter 10

**Priority: medium. Locations:** section 4, lines 307–319;
learning goal 2, lines 148–150; `fig-proxyjump`, line 445.

`ssh -J nova nova18-69` looks like a command readers can run, but it
requires a node assigned to their own active allocation, knowledge
that Chapter 10 has not taught yet. The resource request appears here
while its release is sent to Appendix A, leaving an incomplete live
workflow.

Make this section recognition-only: explain the two-hop connection,
show the config with a clearly labeled allocated-node placeholder, and
link to the complete acquire/connect/release recipe in Chapter 10 or
Appendix A. Alternatively, put all three actions together in a marked
optional walkthrough. Preserve the main outcome of reaching the login
node, transferring files, and keeping a light shell session alive.

Separate the minimum `ProxyJump` example from optional settings copied
from ISU's IDE recipe. That recipe does include `ForwardAgent yes`
and `StrictHostKeyChecking no`, but neither should be presented as
inherent to a two-hop SSH connection. Retain host verification in the
generic example and explain any site-required exception beside the
site recipe. [ISU remote-IDE recipe](https://research.it.iastate.edu/launching-remote-ides-novas-compute-nodes).

### 6. Complete the client-specific authentication route

**Priority: medium. Locations:** section 3, lines 235–262;
section 4, lines 317–319; decisions 3, lines 758–761;
checks file, Windows/WSL parts and SCINet part 4.3.

The decision to use separate Windows and WSL keys is clear; keep it.
But “install both public keys” applies to the Nova-like
`authorized_keys` route, whereas the SCINet path uses SmallStep.
SCINet's Windows instructions require a running Windows `ssh-agent`
service, and the `step` setup updates the invoking client's SSH
configuration. A WSL setup alone does not configure Windows' SSH for
VS Code. Give each relevant client its own explicit site setup, or
send SCINet/Windows readers through the already-supported OnDemand
route. [SCINet SSH guide](https://scinet.usda.gov/guides/access/ssh-login).

Phrase “no personal keys” as “use SCINet's documented certificate
route; skip manual `ssh-copy-id` here.” Silence about a manual-key
alternative does not establish a blanket prohibition. Also replace
“the certificate **is** SCINet's key”: a certificate certifies a public
key and identity; it does not replace the corresponding private key.
OpenSSH's [`CertificateFile` description](https://man.openbsd.org/ssh_config.5#CertificateFile)
explicitly requires the matching private key. One sentence suffices.

The exact WSL agent startup/cleanup and Windows agent service steps
remain legitimate capture tasks. Until captured, avoid promising “one
passphrase per session” uniformly across both clients.

### 7. Fix the tmux/transfer placement and narrow what persistence means

**Priority: medium. Locations:** section 5, lines 322–348;
`fig-tmux-detach`, line 446; exercise 4, lines 562–567.

The login-node examples of acceptable tmux work include “a long
`rsync`,” contradicting the chapter's rule that laptop transfers run
from the laptop through the DTN. Demonstrate a harmless ticker on the
login node. If discussing a laptop transfer under local tmux, label it
as such and say it does not make transfers continue while the laptop
is asleep or offline; Globus is the relevant managed-transfer option.

The supplied ticker is also better than “a long script from Chapter
8”: those scripts are intentionally small, finish quickly, and may
need a project/environment not installed until section 7. Keep the
Chapter 8 connection as recognition of a script, not a new runtime
dependency before moving the project.

Use “command” or “process” in the tmux figure instead of “job” where
no scheduler job was submitted. State that tmux survives client
disconnects while its server/session survives; reboot, session
termination, or site cleanup can still end it. This supports Chapter
10's distinction between a persistent shell and an allocation.

The claim that SCINet's docs are silent about login-node assignment
is too broad: its SSH guide names `atlas-login-1.hpc.msstate.edu` and
`atlas-login-2.hpc.msstate.edu` in the host-key guidance. Use those as
documented leads, while leaving actual routing, direct access, tmux
availability, and persistence as live checks. Ceres still needs its
own evidence. [SCINet SSH guide](https://scinet.usda.gov/guides/access/ssh-login#notes-and-limitations).

### 8. Distinguish the rsync protocol check from modern scp behavior

**Priority: medium. Locations:** section 2, lines 194–203;
section 6, lines 371–374; callout, line 499; checks file, Block E.

The fake-SSH wrapper is a useful demonstration of corrupting rsync's
remote-shell protocol. The prose and callout then apply its conclusion
to `scp` generally, although section 6 correctly notes that current
OpenSSH `scp` uses SFTP. Keep the Chapter 7 qualification: this shell
stdout problem applies directly to rsync over SSH and legacy SCP;
modern SFTP-based `scp` is a different execution path.
[Official scp manual](https://man.openbsd.org/scp.1).

`ssh host true | wc -c` is a useful diagnostic, but nonzero stdout is
not proof that a user's startup file alone caused it; site wrappers
can contribute. Also inspect the SSH exit status: zero bytes from a
failed SSH connection do not establish a clean successful session.
Keep stdout and stderr distinct when explaining the test.

Block E's `bash -c true | wc -c` on the login node is not equivalent
to a fresh SSH command from the laptop: it need not exercise the same
startup behavior. Block F contains the meaningful remote test. Label
Block E's result narrowly or remove that duplicate test.

## Teaching and presentation improvements

### Use a short core route through the SSH configuration material

Keep the current overall section order. Within it, mark the daily
minimum: connect by the supported route, inspect `hostname`, use a
short alias, start/detach/reattach a ticker, dry-run a DTN copy, verify
it, and move the project. Connection sharing can follow as a useful
extension; ProxyJump and detailed IDE settings should be reference or
optional material until readers know allocations.

Keep the no-cluster route complete without requiring a real Nova
account. Use a separate sample config with `ssh -F … -G` for its
checks, or label an inactive sample block clearly. Readers should not
need to install fictitious account entries into their working config
just to complete the local assessment. The real-site exercise can
still extend their actual config.

### Keep transfer-integrity claims tied to the trusted starting point

The same-size/same-time stale-copy exercise is excellent; retain it.
State that a checksum made from the source immediately before transfer
establishes agreement with **that source**, whereas comparison to the
facility's or repository's original manifest can reveal an earlier
change. A newly computed source manifest cannot identify corruption
that was already present when it was made.

The plan already makes rsync's built-in transfer check and its default
size/time selection distinct. Keep that distinction and make “second
run lists no files” mean no unchanged file contents are resent;
verbose status lines or directory metadata may still appear.

The exact SCINet Globus setting is already documented as “Do NOT
verify file integrity after transfer.” Its guide recommends this for
speed; live testing is still needed for the UI's current default, not
to establish whether the setting is documented. Attribute the site's
advice and keep the tiny teaching transfer's verification choice
explicit. [SCINet Globus guide](https://scinet.usda.gov/guides/data/transfer/globus).

### State the network assumption without turning it into a protocol rule

Change “the cluster cannot reach your laptop” and the crossed-out
cluster-to-laptop arrow to “we initiate laptop transfers from the
laptop; a laptop behind a firewall usually cannot accept inbound SSH.”
That explains the practical choice without claiming a universal
restriction. A pull command on the laptop still moves bytes from the
cluster to the laptop; distinguish connection initiation from data
direction in the figure.

Globus uses collections and managed transfer services, so its browser
workflow should not be forced into the same literal SSH arrow model.
The existing overview is enough; no extra network diagram is needed.

### Tighten the checks file before handing it to Austin

These are companion-file issues, not reasons to expand the chapter:

- The checklist says each part stands alone, but part 3.4 refers to
  the capture produced by 3.2, and part 3.6 uses the key from 3.3.
  Name the dependencies and provide a tiny fallback input where useful.
- Part 3.4 sends a probe file through a login node despite the DTN
  teaching rule. `ssh -O check` already tests reuse there; use the DTN
  for the transfer demonstration.
- A glob of DNS answers and three round-robin logins can establish
  what was observed, not prove the total number of login nodes.
  Distinguish documented nodes from observed routing.
- Check config backup existence and use a new backup name deliberately
  on a later visit. A fixed `cp -n` backup can be absent on first use
  or stale after subsequent config changes.
- For rsync group/permission expectations and the reference-link
  exercise, carry the corrections above into the test instructions.

## Verification and remaining limits

I reproduced the local rsync examples in new `/private/tmp/`
directories on macOS with Homebrew rsync 3.5.0 and Apple's openrsync.
The planned source trailing-slash layouts are correct for the supplied
nonempty tree, including an initially absent destination; no correction
to those captured trees is needed. I also reproduced the failure when
destination parents are missing. Tests of an owned read-only receiving
directory did not establish a general rerun failure, so this review
does not claim one.

I checked current official OpenSSH, rsync, SCINet SSH/transfer/Globus,
and ISU SSH/remote-IDE documentation. These support the distinctions
above; they do not establish actual cluster prompt counts, account
permissions, installed software, or session persistence.

No cluster connections, key installation, SSH-config edits, environment
installation, or live Windows/WSL tests were performed. Keep those
remaining checks clearly marked as such. The complete move should be
accepted only after destination creation, both checksum manifests, the
replacement reference link, the locked environment, and Chapter 8's
pipeline have been checked together.
