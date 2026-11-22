---
title: "Chapter 8 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-22
---

Reviewed [chapter_08.md](chapter_08.md) against the repository and series
instructions, [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared theme style guide, relevant written material in Chapters 2–7,
the Chapter 9 plan, and [the hands-on checks](chapter_08_checks.md).
Locations and line numbers refer to the plan as reviewed on 2026-11-22.
The source plan, checks file, and Austin's notes are unchanged.

**Overall assessment:** keep the chapter and its two-sitting structure.
Explaining the script readers have already run is a strong payoff, and
the examples with spaces, an overly broad glob, and a tool reporting
success on bad input make the reliability lessons concrete. The main
changes needed concern the table-check exercise, overly broad claims
about temporary outputs and error handling, and a few dependencies that
the current ordering leaves unresolved.

## Corrections before drafting

### 1. Give the table-check exercise a way to return the right exit status

**Priority: high. Locations:** section 4, lines 286–306; exercise 2,
lines 766–773; end of sitting A, lines 348–349.

The demonstration correctly says that its piped `while` loop runs in a
subshell. Exercise 2 then asks readers to adapt that loop into a script
which exits 1 if **any** row has a problem, without supplying the missing
mechanism. The obvious adaptation loses its flag:

```bash
bad=0
tail -n +2 "$table" | while IFS=$'\t' read -r sample folder cond reads; do
  if [[ ! -d "$folder" ]]; then bad=1; fi
done
exit "$bad"
```

I reproduced a final status of 0 despite a missing folder. Exiting from
inside the loop instead would stop at the first bad row, failing the
requirement to report every row.

Supply a skeleton that reads through input redirection in the current
shell. A compact pattern is:

```bash
bad=0
{
  IFS= read -r header
  while IFS=$'\t' read -r sample folder cond reads; do
    if [[ ! -d "$folder" ]]; then
      printf '%s: missing folder %s\n' "$sample" "$folder" >&2
      bad=1
    fi
    # Supplied scaffold: check for an R1 file when the folder exists.
  done
} < "$table"
exit "$bad"
```

The actual supplied exercise script should include its argument/file
checks, header handling, and the R1 check. Explain the one new detail:
the redirection feeds the group without putting the loop in a pipeline.
No process substitution or `lastpipe` lesson is needed. I checked that
this structure preserves the failure flag.

Also bound the TSV recipe to the supplied table, whose fields are all
present: tab is IFS whitespace, so consecutive tabs do **not** preserve
an empty field. With `sample_C<TAB><TAB>control<TAB>12`, I obtained
`folder=control`, `cond=12`, and an empty `reads`. Mention this limitation
and leave general table parsing to Chapter 14.

Finally, merely changing `IFS` to comma will not make exercise 2 reveal
the CRLF problem if it tests only the folder and R1 names: the retained
carriage return is in the **last** field. Add an explicit inspection or
numeric test of `reads`, or make this a separate prediction using
section 4's existing arithmetic example. Say that the comma example is
this simple fixture, not a general CSV parser.

### 2. Change the temporary-output promise to match failed reruns

**Priority: high. Locations:** section 8, lines 428–430; section 9,
lines 451–478; section 10, lines 502–514; callouts, lines 701–702.

Writing to `name.tmp` and then renaming it protects an existing result
from being overwritten with a partial replacement. It does **not** mean
that a failed run leaves no finished-looking result: a successful
**previous** run's `name` remains. The temporary file can remain too.
I reproduced both with the proposed group/redirection pattern.

Use this narrower rule:

> Publish a new result only after the step succeeds. On failure, an
> older result may still exist; use the run's status and log to decide
> whether it belongs to the current run.

Keep `run_all.sh` stopping before later steps, and add one failure check
after a successful run. Show the old final file remaining unchanged,
the failing run's nonzero status, and the absence of its success log
message. The existing fresh-directory failure test remains useful, but
cannot establish rerun behavior.

The fixed `"$out.tmp"` also assumes only one run writes that output at a
time. Two runs share it; unique log names do not solve that. State the
single-writer assumption for this beginner pipeline. If simultaneous
runs are supported later, use a unique temporary file beside the final
output and a deliberate publication policy. Do not expand this chapter
into a concurrency tutorial.

### 3. Do not turn expected nonzero statuses into blanket error suppression

**Priority: high. Locations:** section 7, lines 368–389;
`tbl-strict-mode`, line 652; related self-check, lines 732–736.

`n=$(grep -c ZZZ file || true)` accepts more than “no matches.” It also
accepts an unreadable or missing input. I checked the missing-file case:
the error prints, `n` becomes empty, and the strict script continues
with status 0. That undermines the lesson immediately above it.

Make the distinction explicit: `grep` status 1 is an expected result;
status 2 is an error. Supply a short reference example that preserves
the distinction:

```bash
if n=$(grep -c ZZZ "$file"); then
  :
else
  status=$?
  [[ "$status" -eq 1 ]] || exit "$status"
fi
```

Explain `:` as a successful no-op if this exact form is used. I tested
zero matches and a missing file: the former continued with `n=0`, the
latter exited 2. A plain `if grep -q …` is enough when the exercise only
needs a yes/no branch, but say whether an input error is being handled
separately.

Apply the same caution to `… | head -n 1 || true`: it suppresses an
actual decompression error as well as the expected broken pipe. The
existing recommendation to keep this preview idiom in the interactive
terminal is sufficient for the main path. Do not make unconditional
`|| true` the script template's repair.

Two wording fixes belong here too:

- Replace “141, **every time**” with “141 in all six captured runs on
  this input and system.” The capture is evidence about those runs,
  not a general scheduling or buffering guarantee.
- Refine “commands tested by `&&`, `||` are exempt.” The final command
  in an AND/OR list can still trigger `-e`: `true && false` stops a
  strict script, whereas `false && echo skipped` does not. Use those
  two tiny examples rather than broadening the exception table.

### 4. Put the exercise prerequisites before the sitting break

**Priority: medium. Locations:** length note, lines 181–184;
section 6, line 348; exercises 1–3, lines 756–786.

Exercise 1 requires adding `set -euo pipefail` and interpreting its
effect, but sitting A ends before that line is taught in section 7.
Exercise 2 also needs the aggregate-status scaffold discussed above.

Keep the agreed two sittings, but label the early work as **exercise 1,
part A**: quote arguments, print TSV, and fix the glob. Finish its
strict-mode and failure checks after section 7. Supply exercise 2's
working scaffold before asking for adaptations, or move its full
version to sitting B. This is a small ordering repair, not a reason to
move error handling ahead of variables and loops.

Exercise 3 currently offers `gzip -t`, `[[ -s … ]]`, or an expected
count as though any one will catch all its bad inputs. A valid gzip
file representing empty content has nonzero compressed size and passes
`gzip -t`; the plan's captured answer already recognizes this. State
the actual task: strict mode catches the missing/truncated streams in
this particular `gunzip | wc` script; add a **positive read-count
check** for the valid empty gzip stream. Distinguish that stream from a
zero-byte file named `.gz`.

Keep the line-count shortcut explicitly restricted to these ordinary
four-line toy FASTQ records. Integer division by four is neither a
FASTQ validator nor a substitute for Chapter 15's format-aware tools.

### 5. Make the git recovery diagram and saved-history check exact

**Priority: medium. Locations:** project check, lines 148–149;
section 12, lines 580–595; `fig-git-routine`, line 628; exercise 5,
lines 792–797.

`git restore file` restores the working file from the **index** by
default, not directly from the last commit. The two coincide in the
planned unstaged-edit demonstration, but the figure explicitly names
the wrong source. I verified this by committing one value, staging a
second, editing a third, then restoring: the staged value came back.
This agrees with the [official restore documentation](https://git-scm.com/docs/git-restore).

Keep the small routine. Label its arrow “from staged copy; normally the
last commit here,” or use an explicit `--source=HEAD` when teaching
recovery from the current commit. Show `git diff` before discarding the
edit. A single sentence about the index is enough; Chapter 21 still
owns the full treatment.

The outcome asks for commits for both scripts, but the first supplied
commit contains both at once. Make that acceptable explicitly, and
ensure there are two commits before `HEAD~1` is used. `git log
--oneline` alone does not show which files a commit contains; use one
small `git show --stat HEAD` check or a path-limited log for the promised
script history. Recovery from an older commit should end with a
verification run and a new commit, as exercise 5 already requires.

Say “a repository on the same disk is not an off-machine backup” rather
than “not a backup until pushed”: pushing is one way to make an
independent copy, not the definition of a backup.

### 6. Close the small mismatches between the pipeline, logging, and setup

**Priority: medium. Locations:** section 10, lines 479–531;
`fig-numbered-pipeline`, line 627; decisions 1 and 4,
lines 1019–1033; [hands-on checks](chapter_08_checks.md), part 1.2.

The proposed `02` writes its log messages only to stderr, while the
section introduction and pipeline figure say each step writes into
`logs/`. Choose one consistent description. The simplest is to keep
the short script and explicitly give a whole-run capture command.
When that command uses `| tee`, explain how the caller observes the
script's failure: an ordinary terminal pipeline otherwise reports
`tee`'s success. Do not accidentally recreate the failure-masking bug
that section 9 has just demonstrated.

Either add the promised start/end, input/version, and output-provenance
lines to `02`, or mark it as a deliberately shorter demonstration and
identify which provenance is recorded elsewhere. At present “same
header and strict mode as `01`” can easily be read as “same reliability
and logging template.”

The `pixi.toml` guard is a useful current-directory check, but says only
that a manifest exists. Describe it as catching the common wrong-folder
mistake, rather than proving that this is the intended project. A
fresh scratch copy of the **guarded** script also needs a manifest or a
clearly stated adaptation before it can reach the intended checksum
failure.

ShellCheck is still absent from the checked-in `setup/pixi.toml`, as
the plan correctly records. Keep adding it with a regenerated lockfile
as a drafting dependency, and include an upgrade instruction for readers
who downloaded the Chapter 2 environment before that change. The Mac
checks should also distinguish the original `01` checksum from the
checksum after adding the guard; the latter cannot match `76fa8eb6…`.

## Teaching and presentation improvements

### Retain the central path and make uncommon syntax reference material

The useful first-pass path is: save a command, quote values, loop over
files, take arguments, check failures, understand `01`, run `02`, save
working scripts. Keep `case`, `${10}`, `$$`, Bash 3.2 feature names,
and the less common strict-mode exceptions as recognition/reference
material. This preserves the outline's beginner audience and its
boundary with optional Chapter 34.

Consider showing the existing `count_lines.sh` briefly at the start of
section 2. It gives a very small complete script before the GTF
pipeline. Keep the GTF example as the bridge to `02`; there is no need
to introduce another dataset.

### Keep simplified rules accurate and their demonstrations bounded

“Quote every expansion” is a good default for command arguments.
Qualify the explanation that unquoted values split and glob: these
steps depend on context, notably ordinary assignments and `[[ … ]]`.
Do not make readers infer that the unquoted `$n` in the planned
`[[ $n < 10 ]]` self-check contradicts the lesson. The default IFS
qualification also belongs beside “spaces, tabs, and newlines.”

Keep the misspelled-path example, but describe it first as constructing
the wrong argument `/`. “Would delete the whole filesystem” overstates
what default GNU `rm` will actually allow and ignores permissions.
The valuable lesson is that quoting preserves an argument; it does not
validate the path. Retain the decision never to run this deletion.

After teaching `nullglob`, show the promised empty-list check explicitly
(for example, a supplied array plus its length). Zero loop iterations
are often preferable to a literal glob, but an empty input set should
not silently become a successful analysis.

### Use the series' color roles for results and reference inputs

In `fig-numbered-pipeline`, ordinary output data should remain `given`,
not become green simply because a script succeeded. The GTF is `ref`.
Use `good` for a check badge or matching checksum. The current figure
specification assigns `good` to results and the general color note
assigns it to anything “correct or fixed”; both are broader than the
shared style guide allows.

## Verification and remaining limits

I ran focused reproductions in new `/private/tmp/` directories using
Bash 5.3.15 and Apple Git 2.50.1 on macOS. These covered loss of a loop's
aggregate flag in a pipeline, the redirected-loop repair, collapsed
empty TSV fields, `grep … || true` masking a missing input, the
status-sensitive `grep` repair, stale final output after a failed
temporary-file write, and `git restore` selecting the staged content.
The git behavior was also checked against its official documentation.

I did not rerun the earlier Linux/SeqKit captures, install ShellCheck,
change the environment, or contact a cluster. Those existing captures
are useful evidence, but the full finished scripts, exercise 2's R1
check, Pixi runs, and site-specific version fallbacks still need the
end-to-end checks already listed in the plan.
