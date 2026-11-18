---
title: "Chapter 7 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-17
---

Reviewed [chapter_07.md](chapter_07.md) against repository and series
guidance, the [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared style guide, written Chapters 1–4, Chapter 5–6 plans, the
environment manifest, and `misconceptions.yml`. Locations refer to the
2026-11-17 plan. The source plan and Austin's notes are unchanged.

**Overall assessment:** keep the practical diagnostic approach and the
chapter's ownership of permissions, `PATH`, startup files, processes,
disk use, and line endings. There are several definite technical
corrections to make before drafting, particularly directory permissions,
capital `X`, startup-file rules, and claims about terminal closure.
The final exercise is promising but needs a complete supplied script
and an explicit sequence of invocation methods.

## Corrections before drafting

### 1. Correct the directory-permission experiment and the meaning of deletion rights

**Priority: high. Locations:** section 2, lines 155–178; section 2's
key idea; permission figure/table; captured outputs, lines 672–675;
`file-perms-protect-delete`.

The claim that removing owner `x` makes plain `ls d` fail is not
generally correct. With directory mode `644`, the owner still has
directory read permission. Using GNU `ls` 9.11 without aliases on this
Mac, I observed:

| Command | Result with readable directory `d`, no owner search permission |
|:--------|:---------------------------------------------------------------|
| `ls d` | Lists the name `f` successfully |
| `ls -l d` | Cannot access `d/f` metadata; shows question marks and `Permission denied` |
| `cat d/f` | `Permission denied` |
| `cd d` | Fails because search permission is missing |

Use that distinction as the lesson: **read** lists names; **search**
(`x`) allows looking up entries and traversing the directory. A
color-enabled alias can make an `ls` capture additionally attempt
metadata access, so capture with a controlled plain command and do not
generalize the alias's behavior into a permission rule.

Also change “the folder's `w` decides deletion” to “write **and search**
permission on the containing directory normally allow removing an
entry.” Traversal of ancestor directories must also work. File read and
write bits are not the deletion permission. Explain that the owner,
group, and other classes are selected rather than cumulatively added:
an owner denied `x` does not fall back to the group's or others' `x`.

For the beginner rule, state that these examples use ordinary local
permissions. One brief cluster note can acknowledge ACLs and the sticky
bit when the ordinary bits do not explain a denial; no ACL tutorial is
needed. Avoid promising every `Permission denied` is an omitted `x`
bit: an execution-disabled filesystem can also produce that symptom.

Finally, distinguish opening an existing writable file from creating a
new directory entry. I verified that redirecting onto an existing
writable file succeeds inside a directory with no write bits. Chapter
3 protects **both** the files and the folder; the Chapter 6/7 handoff
should not attribute every failed output redirection solely to the
folder's missing `w`.

### 2. Fix capital `X` and separate setgid from the sticky bit

**Priority: high. Locations:** section 2, lines 176–186;
`tbl-chmod-recipes`; groups/setgid open question.

`chmod u+X` does not add execute permission **only to directories**.
It applies when the operand is a directory **or already has an execute
bit set for someone**. I checked a regular file at mode `610`:
`chmod u+X` changed it to `710`. The
[GNU chmod source documentation](https://github.com/coreutils/coreutils/blob/master/man/chmod.x)
states the conditional rule.

Suggested wording:

> Capital `X` adds search permission to directories and execute
> permission to files already marked executable. It leaves ordinary
> nonexecutable data files alone.

Also replace “group-sticky (setgid) bit” with **set-group-ID (setgid)
bit**. These are different mechanisms:

| Mechanism | Main directory effect |
|:----------|:----------------------|
| setgid (`g+s`, shown as `s` in the group execute position) | New entries normally inherit the directory's group |
| sticky (`+t`, shown as `t` in the other execute position) | Restricts who can delete/rename entries in a writable shared directory |

Setgid does not by itself grant group read/write permission; the new
file's mode, umask, and any default ACLs still matter. See the official
[directory setgid explanation](https://www.gnu.org/software/coreutils/manual/html_node/Directory-Setuid-and-Setgid.html)
and [mode structure](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html).
Keep this as overview, as proposed.

### 3. Make the startup-file model consistent with its own exceptions

**Priority: high. Locations:** section 6, lines 281–315;
`fig-startup-files`; startup-file table; self-check 6.

The current simplified rules contradict one another: scripts supposedly
read neither file, but `.bashrc` supposedly runs in every shell,
including job shells. Neither is an adequate general rule.

Teach the common cases with the actual fallback order:

| Bash invocation | User startup behavior |
|:----------------|:----------------------|
| Interactive login, or explicitly `--login` | First readable file among `.bash_profile`, `.bash_login`, `.profile` |
| Interactive non-login | `.bashrc` |
| Ordinary noninteractive script | Does not automatically read either; an exported `BASH_ENV` can specify a startup file |
| Some noninteractive SSH command invocations | Bash can read `.bashrc` under its remote-shell rules |

System startup files also apply; defer their site-specific details.
This is supported by the
[official Bash startup rules](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files).
Keep the important Ubuntu `.profile` warning, and include `.bash_login`
in the fallback rather than implying `.profile` is always second.

Terminal application names are examples, not the definition of login
status. Preserve the proposed `shopt -q login_shell` observation and
also distinguish interactive status. An SSH login differs from
`ssh host command`; a scheduler script differs from both.

Make `.bash_profile` sourcing `.bashrc` an explicit feature of the
book's setup, rather than a universal default. The self-check should
inspect the **file that is actually read**, which might be `.profile`.
Settings inherited by a script do not prove that the script reread the
file that originally exported them.

Retain the practical advice to keep startup files quiet and avoid
automatic environment/module activation on clusters. Phrase the latter
as avoiding unintended changes across terminals and remote commands,
not as a claim that every batch shell automatically reads `.bashrc`.
Output can break shell-based transfer protocols, especially `rsync`
and legacy SCP; avoid asserting that every SFTP transfer necessarily
runs Bash and breaks in the same way.

### 4. Replace the guarantee about closing terminals with a reliability rule

**Priority: high. Locations:** section 7, lines 325–337;
`fig-process-states`; `closing-tab-ends-session` callout.

“Closing the terminal or a dropped SSH connection ends the processes
started from it” is too absolute. Survival depends on hangup signals,
the shell's settings, program behavior, and how the process was started.
`nohup`, `disown`, detached processes, and submitted scheduler jobs are
counterexamples; these need not become new practical lessons here.
The [Bash signal/job-control rules](https://www.gnu.org/software/bash/manual/bash.html#Signals)
describe why behavior varies.

Use this practical statement:

> Do not rely on a command started in an ordinary SSH terminal
> surviving a disconnection. Use the site's supported persistent
> session or submit the work to the scheduler. A submitted job's
> lifetime is managed separately from the SSH window.

This preserves the reason for tmux in Chapter 9 and SLURM in Chapter
10 without teaching a false invariant. Conversely, closing the terminal
is not a reliable way to ensure every child process has stopped.

Correct “every command readers have run was [a process]” too: builtins
such as `cd`, variable assignments, and `export` normally execute in
the existing shell. Chapter 5 explicitly teaches this distinction.
Describe an external running program as a process, and the shell itself
as a process that can perform some commands internally.

The diagram should show a stopped process resuming through `fg` or
`bg`, not only a foreground/background transition. Say Ctrl-C normally
signals the foreground job; programs can handle signals, so “asks” is
better than a universal guarantee of immediate termination.

### 5. Make the final exercise expose the stated faults in a reproducible order

**Priority: high. Locations:** outcome/check, lines 90–117; exercise 1,
lines 611–622; examples/data.

The proposed order is feasible, but only with explicit invocation
changes. If readers start by typing `count_lines.sh`, the first failure
is `command not found`, regardless of the file's permissions or CRLF.
Specify the sequence:

1. Invoke the supplied file by path, such as `./bin/count_lines.sh`,
   before granting execute permission.
2. Add the missing execute bit and invoke the **same path** again;
   the CRLF shebang now causes the interpreter error.
3. Fix the script's line endings and confirm the path invocation works.
4. Try its bare command name from a different directory; only now
   diagnose `PATH` and add the scratch `bin/` for this session.

Supply the actual script before finalizing the promised exact output.
Raw `wc -l "$1"` does not print `samples.csv: 7 lines`; the script
needs deliberate filename/count formatting. Explain that readers adapt
a supplied script and that its arguments/substitutions are Chapter 8
material. The setup should explicitly establish the initial mode:
rewriting an existing executable file with `printf > file` does not
remove its execute bit on a rerun.

The script's **line count does not diagnose the CSV's CRLF**, as the
plan correctly notes. Make CSV correction a separate subcheck, ideally
the already-demonstrated `grep -c ',30$'` result of **2**, together with
no remaining CR characters. Otherwise the CSV has no meaningful part
in “make the tool run.”

Also record the status of the no-CR check:

```bash
grep -c $'\r' ~/bioinf-computing-ch07/samples.csv
echo $?
```

After correction it prints `0` then **`1`**: grep found no matching
lines. I verified this with GNU grep 3.12. That is expected, not a
failed correction. It is a useful bridge to Chapter 8's treatment of
`set -e`.

### 6. State what `SHELL`, command lookup, and inherited settings actually tell you

**Priority: medium. Locations:** sections 4–5; common-variable table;
self-checks 4–5; `which-is-enough`.

Add a few precise qualifications rather than another section:

- `SHELL` normally names the user's configured login shell; it is not
  a reliable detector of the interpreter currently running. Reuse
  Chapter 1's `$BASH_VERSION` check when checking Bash.
- Left-to-right `PATH` search describes **external commands**. Aliases
  and functions can take precedence, and builtins need no executable
  on `PATH`. `type -a` is a good choice precisely because it exposes
  these distinctions. An alias or function named `seqkit` in an
  already-running interactive shell is not neutralized merely by
  changing its `PATH`.
- A second independently launched terminal normally does not inherit
  a variable exported in the first. A child shell launched from the
  first does. State that condition in self-check 5; avoid defining a
  variable's lifetime by windows alone.
- On Linux, `type -a ls` may show an alias and both `/usr/bin/ls` and
  `/bin/ls`, even when those directories resolve to the same place.
  “On Linux one line” is not portable expected output.
- `which` implementations vary. Say it is an external lookup utility
  whose answer may differ from Bash's resolution, rather than claiming
  no implementation can report an alias or several matches.

The fake-SeqKit exercise is a good controlled demonstration. Keep it
session-only, use an explicitly supplied shebang/script, and show the
resolved path as well as a printed version. Do not assume bare SeqKit
is absent on every reader's machine.

## Teaching and presentation improvements

### Keep the CRLF lesson, but distinguish valid files from fragile text commands

The silent `,30$` mismatch is a stronger example than inventing a
filename failure in column 2. The plan's correction that CR sticks to
the **last field** is right for this simple unquoted table. Preserve
the `cat -A` evidence and do not rely on `file` naming the line endings
after identifying CSV.

CRLF is normal in CSV; it does not automatically make a CSV invalid.
The failure here is a Unix text pattern or simplistic parser that
leaves CR in its input. Say that proper CSV readers generally handle
record endings, and leave quoting/multiline fields to Chapter 14.
Likewise, `/mnt/c` does not itself rewrite LF into CRLF: editor and
export settings determine the bytes.

Prefer `sed 's/\r$//' input > output` for the first correction, then
check it. GNU `sed -i` can be the second example on a **Chapter 7
copy**. `tr -d '\r'` removes every CR byte, not just CR from line
endings; give that limitation if retaining it. Never imply CRLF repair
is an appropriate transformation for arbitrary binary data.

### Make the permissions recipe table describe changes rather than fixed results

`chmod u+x` and `g+rX` modify an existing mode; they do not correspond
to one octal mode independent of the starting state. Show an explicit
before mode when supplying an octal comparison. Likewise, “undo” needs
the original mode or a recorded reference, not a universal reverse
command.

Default modes depend on umask and site defaults. Label `555`/`444`
for the Chapter 3 data as the expected result from its demonstrated
starting modes, not a universal consequence of `chmod a-w`.

Reuse the existing `readonly-cant-delete` misconception rather than
adding `file-perms-protect-delete`: the current registry already
includes Chapter 7 for it. Extend the existing probe with the directory
read/search distinction if needed.

### Keep disk usage useful without conflating environment and cache locations

The `df` versus quota distinction and explicit `.pixi` operand are
good. Explain that environment files in `.pixi` and Pixi's package cache
are different storage consumers. Moving `PIXI_CACHE_DIR` changes the
cache location; it does not relocate the project's existing `.pixi`
environment. Hard links and copy-on-write storage can also make
apparent sizes and allocated usage differ; one caveat is enough.

Keep byte quotas and inode quotas separate. `df -i` describes filesystem
inode availability, not a user's file-count quota, just as `df -h`
does not report the user's byte quota. Site commands stay in Chapter
10/Appendix A.

### Keep the system comparisons accurate and short

GNU/BSD option failures are a useful closing of Chapter 1's promise.
Say **the GNU tools used by this book** rather than implying every
Linux utility is GNU: `ps`/`top`, for example, are often procps tools,
and the plan already recognizes BusyBox systems. FreeBSD manuals can
provide context, but the installed macOS man pages are the authority
for macOS behavior; FreeBSD is not an exact versioned specification
of Apple's utilities.

Teach `top` on the actual platform and label CPU percentages with its
display convention. “400% means about four logical CPUs” is useful in
the common Linux mode; it should not imply that the display convention
or column names never vary.

### Reduce optional detail without dropping the promised topics

Keep this as one core chapter, with two natural practice sessions:
permissions/execution/environment, then processes/storage/portability.
The advanced GNU/BSD table, setgid/umask detail, and history tuning can
be compact reference material. Do not hide a prerequisite explanation
inside a collapsed box merely to meet Chapter 4's length.

I support the proposed defaults: `#!/usr/bin/env bash`, no required new
`dos2unix` or `htop` dependency, and no permission calculator in the
first draft. Chapter 3 already uses the `env bash` shebang; describe
this as confirming a convention already demonstrated. The remaining
work is testing that convention under the supported Pixi and cluster
routes, not inventing a new alternative setup.

The “everything happens in scratch” statement needs a named exception
for the explicitly planned `.bashrc` changes and notebook records.
Back up existing startup files without replacing an earlier backup
on repeated practice runs, preserve site-provided lines, and test in
a fresh terminal as proposed. Group/site details still require actual
SCINet/Nova confirmation.

## Verification and remaining limits

Local temporary-file checks used Bash 5.3.15, GNU coreutils 9.11, and
GNU grep 3.12 on macOS. They reproduced directory-name listing without
search permission, failed metadata/content access, `u+X` changing a
regular file from `610` to `710`, successful truncation of a writable
file in a nonwritable directory, and grep's expected status 1 after
CR removal. Official Bash and GNU documentation were checked for
startup, signal, and permission rules.

No real startup files, permissions on the reader's project, processes
belonging to other work, or installed environments were changed. This
review does not supply Ubuntu/WSL, VS Code Remote-SSH, Open OnDemand,
or SCINet/Nova captures. The plan appropriately leaves those platform
observations for drafting; its exercise scripts still need a complete
end-to-end run once supplied.
