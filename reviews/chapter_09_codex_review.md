# Chapter 9 — Codex review

Reviewed: 2026-11-23  
Chapter: [Working remotely](../chapters/09-working-remotely.qmd)  
Revision reviewed: working tree based on `b7a8818`, including the existing
uncommitted chapter and five new figures. Chapter SHA-256:
`abee9b657ace0fcd2753948f60aa068d7108c6e321e0c99f96032b763eb399f2`.

The chapter renders successfully. Its local rsync demonstrations,
checksum failures, stale-copy exercise, and project-move mechanics work
as described. I found three medium-priority issues and one low-priority
correction. These findings concern the written chapter, rather than its
earlier plan. No chapter, figure, environment file, real SSH setting,
key file, or reader-project file was changed for this review.

The draft follows through on the earlier plan review well: it prepares
the destination before the assessed transfer, copies the external
reference separately, replaces the dangling link explicitly, distinguishes
login-node and DTN connection sharing, and checks the pipeline's exit
status as well as its results. The fake-SSH demonstration and same-size,
same-time stale-copy exercise are particularly effective. Keep these
worked examples; the corrections below can stay small.

## Findings

### 1. Inserting the SCINet aliases directly above `Include` changes its scope

**Priority: medium.** Locations: [chapter source](../chapters/09-working-remotely.qmd),
lines 728–743 and 756–771.

The instructions say to insert the four alias entries above the
`Include` line, but do not show the surrounding `Host *` that must
remain immediately before that inclusion. If readers insert the block
directly above the line shown, `Include` becomes part of the final
`Host ceres-dtn` block. The SmallStep configuration is then skipped for
`atlas`, `atlas-dtn`, and `ceres`, including its user name, host trust,
and proxy command. Adding convenient names can therefore break the
authentication route those names need.

SCINet's own [configuration example](https://scinet.usda.gov/guides/access/ssh-login#creating-a-configuration-file)
shows the generated `Host *` followed by `Include`. OpenSSH explicitly
allows [conditional inclusion inside a `Host` block](https://man.openbsd.org/ssh_config.5#Include).
The problem is the insertion point, not the alias hostnames.

**Reproduction:** I put the chapter's four aliases immediately before
an absolute `Include` in a disposable config. The included file used
`Match exec "true"` in place of the real SmallStep host check, followed
by a test user, known-hosts path, and proxy command. With `ssh -F … -G`,
only `ceres-dtn` received those settings; the other three used the local
user name and had no proxy command. Adding `Host *` before `Include`
made all four receive the included settings. No connection or real
SmallStep command was run.

**Suggested correction:** say “insert your aliases before the generated
`Host *` / `Include` block,” and show the end of the complete layout:

```text
Host ceres-dtn
    HostName ceres-dtn.scinet.usda.gov

# Keep SmallStep's generated block after your aliases.
Host *
    Include "~/.step/ssh/includes"
```

Retain the actual generated path on the reader's machine. Ask readers
to check `user`, `hostname`, `userknownhostsfile`, and `proxycommand`
with `ssh -G` for both their login alias and DTN alias.

### 2. The one-off tmux reconnect command loses the configured cluster username

**Priority: medium.** Location: [chapter source](../chapters/09-working-remotely.qmd),
lines 943–947; relevant config at lines 620–637.

The recovery command is
`ssh -t nova-login-1.its.iastate.edu tmux attach -t ch09`.
However, the chapter puts `User <netid>` under `Host nova nova-dtn`.
Typing the full hostname does not match either alias, so SSH defaults
to the laptop username unless another setting supplies one. Readers
whose two usernames differ can fail to authenticate precisely when
trying to recover their session. The chapter already uses explicit
`<netid>@…` correctly in the preceding captured routing example.

**Reproduction:** using only the chapter's full Nova config in a
disposable file, `ssh -F … -G nova` selected the test cluster username.
`ssh -F … -G nova-login-1.its.iastate.edu` selected the laptop username
and also omitted the alias-specific sharing and keep-alive settings.
Adding `netid_test@` to the full hostname selected the intended user.
These were configuration checks without network connections.

**Suggested correction:** use
`ssh -t <netid>@nova-login-1.its.iastate.edu tmux attach -t ch09`
for the one-off command. When the `nova` alias already points at the
correct node, `ssh -t nova tmux attach -t ch09` also works and retains
all its configured options. No extra config block is necessary.

### 3. Globus cannot transfer laptop files while that laptop sleeps

**Priority: medium.** Locations: [chapter source](../chapters/09-working-remotely.qmd),
lines 971–974 and the Globus row at line 1255; related explanation at
lines 1233–1242.

The tmux section recommends Globus as the answer to a laptop going to
sleep, and the comparison table says it runs while the laptop sleeps.
That is true for the cluster-to-cluster example, but not for a transfer
whose source or destination is the laptop through Globus Connect
Personal. Exercise 6 explicitly uses the latter route. Closing the
browser is fine; sleeping the machine that holds the files makes that
endpoint unavailable.

Globus states that [file bytes move directly between the source and
destination systems](https://www.globus.org/data-transfer), and that it
resumes after an unavailable component comes back online. Its
[transfer FAQ](https://docs.globus.org/faq/transfer-sharing/#what-is-the-effective-transfer-rate-reported-by-globus)
also distinguishes transfer time from idle time when a Personal
collection is disconnected. This is a documentation check; I did not
run a live Globus transfer.

**Suggested correction:** qualify both places: “You can close the
browser. Cluster-to-cluster transfers continue while your laptop sleeps;
if the laptop is one end, keep it awake and online with Globus Connect
Personal running. Globus can resume when it becomes available again.”
Keep the existing explanation that cluster-to-cluster transfers need
no laptop connection.

### 4. `ssh-agent -s` is not automatically tied to the terminal's lifetime

**Priority: low.** Location: [chapter source](../chapters/09-working-remotely.qmd),
lines 432–454, especially line 452.

The Ubuntu instructions start an agent with
`eval "$(ssh-agent -s)"`, then say it lasts until that terminal closes.
This invocation starts a background agent; it does not arrange for the
agent to exit with the shell. The shell's environment supplies the
connection information, which a new independent terminal usually lacks,
but losing that environment is different from stopping the agent.
Repeatedly following the recipe can leave several agents running.

**Reproduction:** I launched an isolated agent from a short-lived Bash
shell using the same `eval` pattern and a temporary socket. After the
launching shell exited, a separate process with its saved socket
information could still query it: `ssh-add -l` returned **1**, “The
agent has no identities,” rather than the status-2 connection error.
I then stopped that test agent. No real key was loaded.

The [OpenSSH agent manual](https://man.openbsd.org/ssh-agent.1)
distinguishes this setup from starting a command under the agent, whose
termination does end it, and documents `-k` for explicit cleanup.

**Suggested correction:** replace the lifetime sentence with “This
terminal now knows how to reach the agent; a new terminal normally does
not. The background agent can remain running after you close this
one.” Before closing the terminal that started this manual agent, show
`eval "$(ssh-agent -k)"` to stop it and clear its environment variables.
Limit that cleanup instruction to the manually started Ubuntu agent;
the macOS-managed agent does not need this step.

## Verification performed

- Rendered with `quarto render chapters/09-working-remotely.qmd`:
  successful, without reported missing-reference or missing-citation
  warnings.
- Extracted all **38 Bash blocks**, including those nested in lists,
  and checked them with `bash -n`:
  no syntax errors. Runtime checks were selective; generic transfer
  templates and account-dependent commands were not replayed as a
  continuous unattended session.
- Replayed the fake-SSH and quiet-SSH transfers under a new temporary
  root: the noisy wrapper returned **2** with the quoted protocol
  mismatch, and the quiet wrapper returned **0** with both files copied.
- Confirmed that the dry run leaves its destination absent; adding
  `c.txt` sends only that file's contents; the source-slash examples
  produce the two displayed directory trees; and missing destination
  parents produce exit **11**. Exercise 1 uses the same demonstrated
  directory structure.
- Reproduced checksum success, a one-byte failure with status **1**,
  and repair by rerunning rsync. Replayed Exercise 2 with an initial
  `AAAA` plus newline: the ordinary rerun kept the stale `AAAA`,
  `--checksum` copied `AAAB`, and the original manifest then failed in
  both folders, as the answer explains.
- Checked the Nova config's user, hostname, identity selection,
  keep-alive, connection-sharing, and **36,000-second** idle timeout
  with `ssh -F … -G`. Reproduced the two configuration findings above
  and checked their suggested repairs in disposable configs.
- Started an isolated tmux server with no user config, created a
  detached `ch09` ticker, and confirmed that it kept printing across
  two ticks after the creating client exited. Listed and captured the
  session, then stopped only that test server. The isolated agent and
  tmux checks needed permission to create local sockets outside the
  sandbox; both test processes were cleaned up.
- Tested project copying and link replacement locally. The exclusions
  omitted `.pixi/`, `results/`, and `logs/`; `.git/` and the project
  files copied; an absolute reference symlink retained its target text;
  replacing a deliberately dangling link made the reference accessible.
- Rebuilt Chapter 8's current two-step pipeline in a disposable source
  project, including its folder guard and added result-row check.
  Reused prior temporary copies of both FASTQs and the GTF only after
  matching their SHA-256 hashes against `data/README.md`. Copied the
  project with this chapter's exclusions, made the old reference path
  unavailable, copied the reference separately, replaced the link, and
  checked the receiving manifests. Both source and destination runs
  exited **0**. The result MD5s matched the chapter exactly:
  **`3b9c2b4c499d85a7e70aaf3faaef3c99`** for the feature table and
  **`e1d81de77934f7ab7b44bf72b7520b32`** for the read-count table.
- Checked that `--no-p --no-g` creates read-only files from a `444`
  source under the tested umasks, and retains an existing destination
  file's mode. This agrees with the rsync manual's
  [new/existing destination permission rules](https://download.samba.org/pub/rsync/rsync.1#opt--perms);
  it does not verify the cluster-specific group inheritance captures.
- Confirmed all **40** distinct referenced section, table, and figure
  identifiers exist, all **three** citation keys are present, and all
  **five** included SVGs parse as XML. Checked the figures' source
  content and step descriptions against the surrounding explanations.

## Limits and release notes

Local checks used macOS **15.7.9** on Intel, Bash **5.3.15**, rsync
**3.5.0**, OpenSSH **9.9p2**, tmux **3.7c**, GNU checksum tools, and the
already installed book-environment SeqKit **2.14.0**. The pipeline checks
used those installed tools directly; I did not reinstall an environment
or rerun the pipeline through Pixi. The local reference manifest covered
the verified GTF; `genome.fa.gz` was not available in the reused test
fixtures and its copy/check was not repeated.

I checked official OpenSSH, rsync, Globus, SCINet SSH/transfer, and ISU
login documentation. I did not log into Nova, Atlas, or Ceres, install
or load real keys, edit real SSH config, reproduce Windows/WSL behavior,
or retest certificate renewal, VPN requirements, prompt counts, remote
permissions, timestamp behavior, or overnight tmux persistence. Those
site-specific observations remain the chapter author's captures.

The chapter was rendered and its SVG sources checked, but browser
layout, dark mode, small screens, stepped controls, and accessibility
were not visually tested. Bibliographic metadata and editorial notices
were not re-audited. The chapter source hash remained unchanged
throughout the review.
