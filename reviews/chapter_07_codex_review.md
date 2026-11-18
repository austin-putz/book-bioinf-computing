# Chapter 7 — Codex review

Reviewed: 2026-11-18  
Chapter: [The Linux system](../chapters/07-linux-system.qmd)  
Revision reviewed: working tree based on `7c0b8f7`, including the existing
uncommitted chapter and six new figures. Chapter SHA-256:
`a0d722c639cf68250db12e02f360ff596907d87a3660926089d3a935eada1f23`.

The chapter renders successfully. Its main permission demonstrations,
script-repair sequence, CRLF examples, and fake-SeqKit exercise work as
described. I found two medium-priority issues and one low-priority
correction. These findings concern the written chapter, rather than its
earlier plan. No chapter, figure, environment, real startup file, or
reader-project file was changed for this review.

The draft handles the earlier plan review well. In particular, it now
distinguishes directory read permission from search permission, explains
why an existing writable file can change inside a nonwritable directory,
correctly describes capital `X`, and avoids promising that closing a
terminal always stops or preserves its processes. The final exercise's
ordered progression through permission, shebang, and command lookup
failures is effective. Keep the two-sitting suggestion: this is a large
chapter, but the split follows the concepts naturally.

## Findings

### 1. Exercise 4 treats any mention of `EDITOR` as a configured setting

**Priority: medium.** Locations: [chapter source](../chapters/07-linux-system.qmd),
lines 1820–1829, especially the `grep -n EDITOR` guard at line 1822.

The answer promises to add `export EDITOR=nano` only when necessary and
then obtain `nano` in a new terminal. Its guard searches for the text
`EDITOR` anywhere in the file. A commented-out setting, explanatory
comment, or another variable containing that word makes `grep` succeed
and suppresses the append. The requested setting can therefore remain
absent even though the recipe finishes successfully.

**Reproduction:** I ran the answer's backup and append commands against
two disposable startup files, containing respectively:

```bash
# export EDITOR=vim
```

and:

```bash
export VISUAL_EDITOR=vim
```

Neither received the `export EDITOR=nano` line. Fresh interactive Bash
shells reading those files through `--rcfile`, with no inherited
`EDITOR`, printed `EDITOR=[]`. A file with no mention of `EDITOR`
received the line and correctly produced `EDITOR=[nano]`.

**Suggested correction:** distinguish an active assignment from a text
mention. For a simple repeatable recipe whose intended setting is
specifically `nano`, use an exact-line check such as
`grep -qxF 'export EDITOR=nano' ~/.bashrc`, then append that line if it
is absent. Explain that an existing active `EDITOR` assignment should
be inspected and edited deliberately, and retain the fresh-terminal
check because later assignments can override earlier ones. Keep the
backup step; it successfully preserves the first backup on repeat runs.

### 2. The process-state command uses a column name macOS does not support

**Priority: medium.** Location: [chapter source](../chapters/07-linux-system.qmd),
lines 1112–1127, the `ps -o pid,stat,rss,cmd` example and its output.

The chapter runs on the reader's laptop, including macOS after the
book's setup. That setup installs GNU core utilities but does not
replace macOS's `ps`. The `cmd` output keyword works with Linux's
procps `ps`; Apple's `ps` rejects it, leaving out the command column
that readers need to associate a stopped process with `sleep 600`.
The later portability section correctly identifies `ps` as separate
from GNU coreutils, but this runnable example needs the distinction too.

**Reproduction:** on macOS **15.7.9**, the supplied command returned
**1** with:

```text
ps: cmd: keyword not found
```

It printed the other three columns without the command name. Using
`command` instead of `cmd`, checked on the test process, returned
**0** and included the `COMMAND` column. Apple's
[`ps` keyword source](https://github.com/apple-oss-distributions/adv_cmds/blob/main/ps/keyword.c)
also lists `command` as an accepted keyword.

**Suggested correction:** use `ps -o pid,stat,rss,command`, and update
the corresponding capture. This retains the same lesson and avoids
another operating-system tabset or dependency.

### 3. Plain assignment does not remove an existing export

**Priority: low.** Locations: [chapter source](../chapters/07-linux-system.qmd),
lines 759–761 and the `NAME=value` row at line 782.

The variable-lifetime table says that `NAME=value` is not seen by
programs the shell starts. That is true when the assignment creates a
previously unexported variable. An already-exported variable keeps its
export attribute when assigned a new value. This distinction is
particularly relevant here because the preceding example has just
exported `x`, and the chapter also demonstrates assigning `PATH`,
which is normally already exported.

**Reproduction:** under Bash **5.3.15**:

```bash
export x=1
x=2
bash -c 'echo "$x"'
```

The child prints **`2`**. After `export -n x`, a new child no longer
receives it. The [Bash `export` documentation](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
describes export as an attribute marking a variable for subsequent
commands, with `-n` removing that attribute.

**Suggested correction:** change the table entry to “no, unless already
exported,” and say “`x=1` creates a shell variable; exporting it makes
its value available to child programs, including after later
assignments.” The worked example itself is correct and can stay.

## Verification performed

- Rendered with `quarto render chapters/07-linux-system.qmd`:
  successful, without reported missing-reference or missing-citation
  warnings.
- Checked all **35 Bash blocks**, including the supplied script and
  startup-file fragments, with `bash -n`: no syntax errors. Runtime
  checks were selective; real login startup files and arbitrary process
  management commands were not replayed as an unattended script.
- Rebuilt Chapter 5's practice tree under a temporary root and replayed
  **13** Chapter 7 filesystem/environment blocks with the practice-path
  prefixes redirected there. Used Bash **5.3.15**, GNU coreutils
  **9.11**, GNU grep **3.12**, and GNU sed **4.10** on macOS Intel.
  Set umask `0022` in the disposable walkthrough to match its starting
  permissions.
- Confirmed that removing owner search permission preserves plain
  directory-name listing but prevents metadata lookup, file access,
  and `cd`. Checked the converse too: search permission without read
  permission allows opening a known filename while directory listing
  fails. An owner denied search permission does not fall back to the
  other permission classes.
- Reproduced overwriting an existing writable file inside a nonwritable
  directory, with creation and deletion still refused. Confirmed the
  demonstrated symbolic and octal permission changes, including the
  conditional `X` rule on a regular file: **610 → 710**.
- Evaluated the permission calculator's actual conversion code under
  Node for all **512** ordinary modes, for both file and folder: **1,024**
  cases. Checked all **512** generated symbolic file-mode recipes
  against actual `chmod` results. The displayed `750`, `644`, and
  `700` examples agree with the calculator.
- Reproduced the four script invocation outcomes: execution through
  Bash, refusal before the execute bit, successful path invocation
  after adding it, and failed bare-name lookup. Ran Exercise 1's full
  repair sequence, including the initial **126**, CRLF interpreter
  failure **127**, successful path invocation, missing bare command
  **127**, and successful invocation after changing `PATH`.
- Confirmed that the CRLF sample sheet initially yields **0** matches
  for `,30$` and **7** lines containing carriage returns. After repair,
  the counts become **2** and **0**. The script prints
  **`samples.csv: 7 lines`** both before and after sheet repair; the
  no-CR `grep` returns the expected status **1**. Verified the
  invisible last-field value `$'9\r'` and its failed comparison with
  `9`.
- Ran Exercise 3's fake executable and an actual Pixi invocation:
  bare `seqkit` selected the fake **0.0.1**, while `pixi run` placed
  its environment first and selected SeqKit **2.14.0**. Used Pixi
  **0.84.2** with `--locked` and an existing temporary environment's
  manifest; no new environment was installed. That older environment's
  lockfile differs from the current book lockfile, so this check
  establishes command lookup behavior, not current dependency
  reproducibility.
- Tested the `.bashrc` backup/append recipe only on disposable files.
  Its positive case adds one setting, a repeat avoids another copy,
  and the first backup remains intact. Tested its two false-positive
  cases and the exported-variable reassignment described above.
- Used interactive Bash sessions with disposable `sleep` jobs to
  check Ctrl-C (**130**), background job listing and termination,
  Ctrl-Z suspension, the stopped-job exit warning after an intervening
  external command, and termination of the suspended job. Test jobs
  were ended; no processes belonging to other work were signalled.
- Reproduced the native macOS diagnostics for `ls --version`,
  `cat -A`, `stat -c`, BSD `sed -i` without a suffix, `grep -P`, and
  `du --apparent-size`; also confirmed native `du -A` succeeds. The
  process-column discrepancy is recorded above.
- Confirmed all **41** referenced section, figure, and table
  identifiers exist and all **three** bibliographic citation keys are
  present. Parsed the six included SVGs as XML and confirmed their
  inclusion, the stepped-figure script, and the Observable code in
  the rendered HTML.

## Limits and release notes

Runtime checks used macOS **15.7.9** on Intel with the available GNU
tools. I did not reproduce the Ubuntu/WSL captures, log into a cluster,
audit site startup files or quotas, or verify ACL and shared-group
behavior on cluster storage. The book's full software installation,
hard-link disk accounting, `top` display, and measured environment
sizes were not rebuilt or remeasured. Startup-file selection rules
were checked against the official Bash documentation; fresh-shell
runtime checks used explicit disposable `--rcfile` files rather than
modifying the user's login files.

The browser tool reported no available browser. The calculator checks
establish its conversion logic, not browser controls or layout.
Dark mode, narrow screens, stepped controls, CDN loading, and browser
accessibility remain untested. Bibliographic editorial notices were
not re-audited.
