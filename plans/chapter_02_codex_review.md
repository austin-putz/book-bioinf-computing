---
title: "Chapter 2 plan — Codex review"
subtitle: "Advisory review · original plan unchanged"
date: 2026-11-13
---

Reviewed [chapter_02.md](chapter_02.md) against the repository and series
guidance, [PLAN_CHAPTERS.md](PLAN_CHAPTERS.md), the chapter template,
Chapter 1's current plan, the shared style guide, and current official
software and cluster documentation. Line references refer to the reviewed
`chapter_02.md`. Recommendations below are proposals, not new decisions.

**Overall assessment:** keep the structure and scope. Installing one
supported environment, repeating the same check inside VS Code, and then
showing where remote work happens form a useful progression. The editor
survival exercise and compact alternatives table also fit the audience.
The main problems are in the setup contract: readers do not receive the
lockfile that makes the environment reproducible, the remote route needs
to reflect actual site instructions, and Windows readers need an explicit
handoff between WSL and the SSH client used by VS Code.

## Corrections before drafting

### 1. Distribute a tested manifest and lockfile together

**Locations:** section 2, lines 58–68; `fig-pixi-parts`, line 135; key idea,
line 189; draft manifest and download sequence, lines 244–278.

Downloading only `pixi.toml` and running `pixi install` asks each reader to
resolve dependencies. The draft permits a range of Python and R patch
versions and any SeqKit version. Readers installing at different times
can therefore get different environments, even though each gets a local
`pixi.lock` afterward. Pixi's [lockfile documentation](https://pixi.prefix.dev/latest/workspace/lock_file/)
explains why the lockfile should accompany the project.

Publish `pixi.toml` and `pixi.lock` from the **same tested book release**,
along with any task scripts they reference. Use `pixi install --locked`
for the supported setup: it checks consistency and fails rather than
silently updating a stale lockfile. This is documented in the
[`pixi install` reference](https://pixi.prefix.dev/latest/reference/cli/pixi/install/).
The author can solve and update the environment; the beginner's first
session should install that tested result.

Adjust the stepped figure accordingly: manifest + supplied lockfile →
install packages for this platform → run the tool. Explain fresh
dependency solving briefly afterward, leaving details to Chapter 23.
Replace “anyone rebuild exactly the same one” with something narrower:

> The manifest describes the software the project needs. The lockfile
> records the resolved packages for each supported platform.

Different operating systems use different package builds. Do not promise
identical binaries or results across platforms just because a lockfile is
present. Record the Pixi version used to test the book release as well.

### 2. Choose the site-supported remote route before starting a VS Code server

**Locations:** section 5, lines 90–104; `fig-remote-ssh`, line 137;
`tbl-where-to-edit`, line 155; site-policy question, lines 370–372.

The current sequence first connects Remote-SSH to a login node and only
then explains that the site may restrict it. The connection itself starts
the server. Put the site check **before** that action.

This is already a concrete issue for the named audience:

- **Nova:** the [current VS Code guide](https://research.it.iastate.edu/using-vs-code-cluster)
  directs readers to the VSCode Tunnel app or Open OnDemand, with another
  route for Remote-SSH to compute resources. The
  [May 19, 2026 maintenance notice](https://research.it.iastate.edu/news/2026/nova-maintenance-may-19-2026)
  specifically moves VS Code use away from `nova-login-*` and
  `nova-vscode` to compute nodes.
- **SCINet:** its [VS Code guide](https://scinet.usda.gov/guides/ide/vscode)
  documents Open OnDemand and registered tunnels to Ceres compute nodes.
  It also explains ending the interactive session when finished. This
  guide does not establish a general prohibition on Remote-SSH for every
  SCINet system; avoid claiming one.

Retain Remote-SSH as the general skill, with a captured demonstration for
readers whose site uses another route. Let Appendix A supply the working
SCINet/Nova setup, including any required authentication and allocation.
Readers should reach that branch from this chapter without first having
to complete Chapters 9–10.

Change the practical outcome and exercise 4 to “open a remote folder using
your site's supported method.” Keep the no-account path explicit. The
figure can show a generic remote host and distinguish a login-node
connection from an allocated compute session. If a session reserves
resources, include how to end it; closing the editor window alone should
not be presented as releasing an allocation.

### 3. Resolve the Windows/WSL SSH configuration handoff

**Locations:** sections 3–5, lines 78–92; OS scope, lines 167–168;
exercise 4, lines 231–234.

On Windows, installing Pixi and working on local files inside WSL is a
good supported path. However, Windows VS Code's Remote-SSH connection
must not be assumed to use WSL's `ssh` executable, home directory,
configuration, or credentials. Microsoft's
[SSH troubleshooting guide](https://code.visualstudio.com/docs/remote/troubleshooting)
documents Windows SSH-client selection and `remote.SSH.path`; its
[Remote-SSH guide](https://code.visualstudio.com/docs/remote/ssh)
documents choosing a configuration file and `remote.SSH.configFile`.

Consequently, writing `~/.ssh/config` in Ubuntu and then selecting its
alias from Windows VS Code is not a complete recipe. Choose and test one
Windows route. A straightforward default is to configure the SSH host
through **Remote-SSH: Add New SSH Host**, identify the Windows config file
it selects, and verify the connection using that same Windows client.
If the book instead makes VS Code use WSL SSH, provide the complete tested
configuration. An institutional tunnel/OOD branch may avoid this step.

Show Windows-specific SSH setup only where needed; Linux remains the
working environment for analysis commands. Label precisely which home
directory contains each config. No full keys or jump-host tutorial is
needed here, but prerequisites required by the chosen site cannot be
deferred beyond the point where readers need them.

### 4. Teach activation and command lookup, rather than a folder boundary

**Locations:** learning goal 2, lines 39–40; section 2, lines 67–68;
figure, line 135; self-check, lines 206–209; misconception, lines 292–294.

“The tool is not found outside the project folder” gives the wrong causal
explanation. Being inside the folder alone does not make bare `seqkit`
available. `pixi run` runs a command in the environment; `pixi shell`
starts an activated shell. Pixi also supports selecting a project with
`--manifest-path`, as shown in its
[`pixi run` documentation](https://pixi.prefix.dev/latest/reference/cli/pixi/run/).

Use this simpler explanation:

> Installing the book environment does not add its tools to every
> terminal. Use `pixi run` to run a command with the book's software.

Keep `pixi run` as the default. If `pixi shell` appears, show `exit` and
explain that activation lasts for that shell; changing directories does
not by itself deactivate it. A later chapter can explain `PATH` fully.

Revise the self-check to compare bare `seqkit` and `pixi run seqkit` in a
fresh terminal **in the same book folder**. State that the reader has not
installed another SeqKit. This tests activation without mixing it with
file paths or implying that a tool can never be installed elsewhere.

### 5. Settle the Chapter 1 → 2 → 3 file handoff

**Locations:** exercise 2, lines 226–227; data location, lines 240–243;
copy command, line 275; folder questions, lines 363–369.

The check assumes R1 is beside `pixi.toml`, but the prose offers several
locations. The command copies only R1, while exercise 2 needs R2. Chapter
1 also creates `fastq_summary.txt`, which Chapter 3 is meant to carry into
the recurring project. A reader can follow the main sequence and still
be missing the files needed next.

For the current Chapter 1 plan, keep `~/bioinf-ch01/` as the completed
first-session folder and give one explicit sequence that copies R1, R2,
and the summary into `~/bioinf-book/`. State how readers who skipped the
R2 exercise obtain that file. Use the book folder as the recurring project
root; Chapter 3 can introduce its subdirectories and update paths then.
Keep the check task's relative input path consistent with that choice.

Use `curl -fLO` for setup-file downloads, carrying forward Chapter 1's
failure handling. The [curl manual](https://curl.se/docs/manpage.html#--fail)
documents `--fail`; plain `curl -LO` can save an HTTP error response under
the expected filename. Download the manifest and lockfile from one fixed
release, and tell readers to stop if either download or installation
fails. This does not require teaching Git before Chapter 21.

### 6. Make editor setup concrete enough to verify

**Locations:** section 3, lines 72–82; extension table, line 154;
draft environment, lines 252–255; final command, line 278.

The environment path `.pixi/envs/default` is a directory, not the Python
or R executable. Give the exact interpreter-selection steps and then
verify what was selected. Pixi's
[VS Code integration guide](https://pixi.prefix.dev/latest/integration/editor/vscode/)
describes Python environment detection and the manual fallback through
**Python: Select Interpreter**, selecting
`.pixi/envs/default/bin/python` for the Linux/macOS paths used here.

The [R extension's quickstart](https://github.com/REditorSupport/vscode-R#quickstart)
also requires the R package `languageserver` for its language services;
the draft contains only `r-base`. Either include the required R support
package in the tested environment and show how to point the extension at
its R executable, or defer that extension setup to Chapter 12. Running
`pixi run check` in a terminal does not verify the editor's interpreter.

Two small additions will prevent common setup failures:

- On macOS, include the Command Palette action that adds `code` to
  `PATH`, followed by reopening the terminal, or lead with File → Open
  Folder. This is part of Microsoft's
  [macOS installation instructions](https://code.visualstudio.com/docs/setup/mac).
- On Windows, install the **Windows** VS Code application and its WSL
  extension, then open the Linux book folder from WSL. Microsoft's
  [WSL guide](https://code.visualstudio.com/docs/remote/wsl)
  documents this arrangement. Do not send beginners to install a second
  Linux desktop copy of VS Code inside Ubuntu.

Describe extensions accurately: UI extensions can stay local; language
support often runs in WSL or on the SSH host. Microsoft's
[extension-location guidance](https://code.visualstudio.com/docs/remote/ssh#_managing-extensions)
supports this distinction. Replace the blanket claim that all extensions
live remotely. Also state that a laptop environment and its files are not
automatically copied to the cluster when a remote window opens.

### 7. Separate quitting Vim from aborting a Git operation

**Locations:** editor section, lines 105–110; self-check, lines 217–219.

Keep `Esc`, `:q!`, Enter for discarding unsaved edits to an ordinary file.
For the question “how do you leave without committing?”, use `Esc`,
`:cq`, Enter, or change the question to ask only how to leave Vim without
saving. Vim documents [`:cq`](https://vimhelp.org/editing.txt.html#%3Acq)
as quitting with an error status.

With a fresh, empty commit message, `:q!` normally results in Git rejecting
the empty message. But it does not mean “abort the caller”: when an
existing message is already available, Git can still commit. In a
temporary repository, I reproduced this with `git commit --amend`: `:q!`
allowed the staged change to be committed; `:cq` stopped the operation.
This distinction can remain one sentence; no amend tutorial belongs here.

If the section includes a shell setting, write `export EDITOR=nano` for
the current shell. Bare `EDITOR=nano` does not reliably export a previously
unset variable to child programs. Note that Git-specific settings can
override it; the [Git commit manual](https://git-scm.com/docs/git-commit#_environment_and_configuration_variables)
lists the precedence. Persistent configuration can wait for Chapter 7.

### 8. Apply the required machine labels consistently

**Location:** code conventions, lines 161–172.

The plan says every block identifies its machine but then specifies bare
`filename="Terminal"`. The shared style guide §6 explicitly requires
`Terminal (laptop)`, `Terminal (login node)`, or `Terminal (compute node)`.
Use those labels here, distinguishing the local `ssh` command from the
commands entered after connection. On a laptop running WSL, say so in the
surrounding instruction. Keep config filenames as filenames, while naming
the machine/home directory where the file is edited.

## Scope and remaining planning choices

Keep the present main order. The remote sections should be explicitly
conditional on account access and site policy, while all readers complete
the local environment and editor exercises. The tables and four proposed
figures are sufficient; no interactive graphic, video, or extra editor
tutorial is needed.

| Open choice | Recommendation |
|:------------|:---------------|
| Full environment, incremental packages, or features? | First try one tested environment for the book's small core exercises, consistent with the decided setup. Measure download size, installed size, and platform compatibility before choosing A. A download under 1 GB alone does not establish that the environment is practical. |
| “Later chapters never stop for installs” | Narrow this to reusing the book environment for core local examples. Later container/pipeline runtimes and site software may have their own setup; the current three-package draft cannot substantiate an all-book promise. |
| How to distribute setup files? | A small versioned setup bundle containing manifest, lockfile, and task files avoids mismatched downloads. Two fixed-release URLs are also reasonable. Teach downloading, not cloning, here. |
| Cache location | `PIXI_CACHE_DIR` is the documented variable. Treat cache location and installed-environment location as separate choices. Put site paths in Appendix A. |
| Detached environments | The option exists, but keep it out of the beginner's main path. It changes environment placement and cleanup; use it only in a tested site-specific recipe. |

The last two recommendations are supported by Pixi's
[environment-variable reference](https://pixi.prefix.dev/latest/reference/environment_variables/)
and [detached-environment configuration](https://pixi.prefix.dev/latest/reference/pixi_configuration/#detached-environments).
Changing the cache location alone should not be described as moving
`.pixi/envs/`. Avoid prescribing a single cache path for every cluster.

Smaller refinements while drafting:

- Replace the VS Code section's lockfile self-check with an editor task:
  save a line in `notes.txt`, display it in the integrated terminal, and
  identify the current folder and connection. Keep the lockfile question
  with the environment section.
- Check that `nano` and `vim` are available on the supported laptop/site
  setups, or give the missing-editor fallback. Neither is included in the
  draft Pixi dependencies. An environment setup chapter should not assume
  every fresh Linux image has both.
- Mark `pixi add` in the reference table as changing the project's
  dependencies and lockfile. Readers following the supplied setup do not
  need to run it here.
- Narrow “I need sudo to install software” to the software used in this
  chapter. These tools can use user-owned space; that does not mean every
  system component or container runtime can be installed without admin
  support.
- In the remote schematic, label local files and remote files separately.
  Showing a remote folder in VS Code does not synchronize it with the
  laptop's folder. Reuse the Chapter 1 cluster shapes as planned.
- Keep the existing Further reading candidates pending the prescribed
  scite/DOI checks when citations are added. This review adds no paper
  metadata or bibliography entries.

## Verification and limits

Official documentation was checked on 2026-11-13. The Git/Vim behavior was
reproduced locally in a disposable repository, without running Git
mutations in this book's repository. The expected total of 5,050,000 bases
is consistent with the plan's 50,000 reads × 101 bases.

Pixi is not installed in the review environment. I did **not** resolve or
install the draft manifest, run its check task, measure its footprint, or
test Windows/WSL or an authenticated cluster session. The listed platform
builds, Python/R pins, actual SeqKit output, extension setup, and complete
site recipes therefore still need execution checks before chapter drafting
is considered complete. Do not interpret documentation verification as a
successful end-to-end installation.

**Recommended disposition:** retain the chapter's order and teaching aids.
Resolve the distributed setup files, site-supported remote entry point,
Windows SSH handoff, and recurring-project paths before drafting; apply
the command-lookup, editor-exit, and machine-label corrections throughout.
No original plan, registry, dataset record, or repository guidance file
was edited for this review.
