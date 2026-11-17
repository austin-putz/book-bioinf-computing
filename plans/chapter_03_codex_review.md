---
title: "Chapter 3 plan — Codex review"
subtitle: "Advisory review · issues, comments, and proposed fixes"
date: 2026-11-17
---

Reviewed [chapter_03.md](chapter_03.md) against the full
[chapter outline](PLAN_CHAPTERS.md), the repository and
[series guidance](../../CLAUDE.md), the [series plan](../../PLAN.md)
(especially topic ownership), the chapter template, the shared style
guide, the written Chapters 1–2, and the existing setup and data records.
Locations below refer to the reviewed plan's section numbers and line
numbers. These are recommendations; the source plan and Austin's notes
have not been changed.

**Overall assessment:** keep the chapter and its practical thread. It
covers the Chapter 3 bullets in `PLAN_CHAPTERS.md`, builds directly on
the first two chapters, and gives the recurring project a useful purpose.
The strongest elements are the distinction between inputs and outputs,
the checksum misconception, explicit input provenance, and the notebook
habit. The main revisions concern executable examples and claims that
are stronger than the examples support. No additional major topic is
needed.

## Corrections before drafting

### 1. Fix the checksum check's working directory

**Priority: high. Locations:** outcome/check, lines 53–67; section 4;
every later reuse of the manifest.

The supplied manifest contains bare filenames, but the outcome runs
`md5sum -c data/raw/checksums.md5` from `~/bioinf-book`. The filenames
are resolved from the terminal's working directory, not the manifest's
directory. The advertised success check therefore fails with “No such
file or directory,” even when the downloaded files are correct.

Keep the manifest beside the raw files and use:

```bash
cd ~/bioinf-book
(cd data/raw && md5sum -c checksums.md5)
```

The parentheses let this one check run inside `data/raw` while leaving
the reader at the project root afterward. Explain that in one sentence;
the shell mechanics can wait for Chapter 8. Alternatively, put
`data/raw/` before each filename in the manifest and consistently check
from the project root. Choose one convention for Chapters 3 and 9.

I reproduced the failure and the directory-based fix with a disposable
fixture and the installed GNU `md5sum`.

### 2. Give the local project a manifest for the files it actually contains

**Priority: high. Locations:** sections 7–8; `fig-sample-sheet`;
exercise 3; examples/data; open question 1.

The full upstream test sheet describes seven runs, while the local
project contains only the two mate files from `SRR6357070`. Even
`WT_REP1` has a second run in the upstream sheet that readers have not
downloaded. Saving that sheet as the project's operational sample sheet
would make its metadata describe a larger collection than its local
inputs.

Keep both teaching opportunities, but give them distinct filenames and
roles:

- `data/meta/samplesheet_upstream.csv`: an unchanged, pinned upstream
  example used to inspect repeated samples and missing mate fields.
- `data/meta/reads.tsv`: a small supplied inventory for the local files,
  with `sample`, `run`, `fastq_1`, and `fastq_2` columns. Its one row maps
  `WT_REP1` and `SRR6357070` to the two paths under `data/raw/`.
- `data/meta/samples.tsv`: biological metadata for the samples actually
  selected for this project. Supply any condition labels from verified
  source metadata; do not ask readers to infer biology from names alone.

This does not require teaching the nf-core schema now. Chapter 26 can
turn the inventory into the pipeline's input sheet. The full upstream
metadata exercise can remain an extension if desired.

There is also a concrete counting error in section 7: **three rows, but
two samples, lack `fastq_2`**. Those samples are
`RAP1_UNINDUCED_REP1` and `RAP1_UNINDUCED_REP2`; the latter has two runs.
The claims of seven runs and five samples are correct. These counts are
visible in the [upstream test sheet](https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/samplesheet/v3.10/samplesheet_test.csv).

Replace “one row per file (or run)” with “this sheet has one row per
sequencing run, with columns for its mate files.” Replace “IDs that
exactly match file names” with “sample IDs agree across metadata tables;
file-path fields identify the correct files.” `WT_REP1` and
`SRR6357070_1.fastq.gz` demonstrate why the sample ID and filename need
not be identical. The [versioned nf-core usage guide](https://nf-co.re/rnaseq/3.22.2/docs/usage#multiple-runs-of-the-same-sample)
also explains that repeated sample identifiers group runs of one sample.

Finally, treat correcting the running-data description in
`PLAN_CHAPTERS.md` and `data/README.md` as a factual prerequisite, rather
than an optional wording choice. State the distinction between this
chapter's one-run subset and the broader test fixture. This is a
pipeline test collection, not evidence of a balanced experiment with
three replicates per condition. Experimental design and biological
interpretation remain in Transcriptomics.

### 3. Make the logging example preserve the evidence the chapter promises

**Priority: high. Locations:** section 8; draft script, lines 342–367;
exercise 4; `fig-provenance-chain`.

The script records useful metadata, but it does not yet produce the
described record of “what each run printed”:

- The date-only log filename is overwritten by a second run that day.
  Exercise 4 therefore replaces the first run's evidence.
- SeqKit's error output stays in the terminal; it is not redirected to
  the log. The executed command and its options are not recorded there.
- Computing fresh MD5 values records what was present; it does not
  verify those inputs against the expected manifest.
- Redirecting directly to `results/read_counts.tsv` can leave an empty
  or partial result after failure, replacing an earlier successful one.
- A saved lockfile alone cannot establish which version of an edited
  script produced an older result.

For this supplied script, use a distinct run identifier in the log name
(timestamp plus a collision safeguard), record the command and script
checksum, check the expected input manifest, capture stderr, and write
the result to a temporary output before publishing it on success. Record
success or failure and the output path; optionally record the output
checksum to associate the fixed result filename with its run. A supplied
script snapshot or checksum is enough here; git commits come later.

Keep these as properties of the supplied example. Readers need only run
it and inspect the result and log; Chapter 8 explains the syntax. Do not
turn Chapter 3 into a lesson in shell error traps or production logging.
If this makes the script much longer, provide it as a downloadable file
and show only its relevant parts. It is already about twenty lines,
rather than the “about ten” stated in section 8.

Also distinguish **project inventory** from **inputs to this result**.
`seqkit stats` uses the FASTQ files; it does not use the reference or
sample sheet. They belong in the project's data record, but should not
appear as causal inputs to this particular count result. Add their
arrows when a later analysis actually uses them.

### 4. Qualify the advice that results need no backup

**Priority: high. Locations:** sections 2 and 6; section 2 key idea;
section 2 self-check; `tbl-project-folders`.

“Can be regenerated” is a useful design goal, but “needs no backup”
does not follow automatically. Recreating a small read-count table is
cheap; recreating a published analysis may require unavailable shared
references, considerable compute time, or a particular historical state
of code and settings. Logs and notebook entries also preserve events
that a rerun cannot reproduce.

Suggested replacement:

> Keep generated outputs separate so you can rebuild them from preserved
> inputs, code, settings, and software records. Practice rebuilding this
> chapter's small result. Back up important final results and retain the
> logs and records that explain them; disposable intermediate files can
> follow a different policy.

Apply this consistently to the folder tree, table, callout, and answer
key. Change “your project is reproducible” to “you have the ingredients
for reproducing the analysis.” The rerun exercise supplies evidence of
reproducibility for this example; folder organization alone does not.

### 5. Keep the symlink warning, but separate tested behavior from portability

**Priority: medium. Locations:** section 5; `fig-symlink`; callouts;
misconceptions; open question 7.

The macOS observation is reproducible: in an isolated fixture, both GNU
coreutils 9.11 `rm` and macOS `/bin/rm` removed the target directory and
its contents for `rm -r link/`, leaving the symlink dangling. That
supports the plan's reported macOS check.

It does **not** establish the Linux/WSL outcome. Keep that validation
open, and remove “either way the data are gone” from open question 7:
it assumes the result of a test not yet performed. The figure and main
callout currently present a particular outcome as universal.

The portable lesson can be stated now:

> A symlink is another route to the same data. Editing a file through
> the link edits the target. Remove only the link with `unlink data/ref`
> or `rm data/ref`, without a trailing slash or recursive option.

Use a harmless toy file to demonstrate edits through the link, and
reserve any recursive-deletion illustration for a disposable fixture or
captured output labelled with the tested platform. Never have readers
test it on the real shared reference. If the stepped figure remains,
make removal and editing alternative examples from the intact-link
state: the present step 2 removes the link, so step 3 cannot follow it
as a literal command sequence without recreating it.

### 6. Correct the promise that moving the project preserves external links

**Priority: medium. Locations:** section 2, lines 121–125; section 5,
lines 187–191; cluster exercise.

An absolute symlink survives moving the project only while the target
remains available at that same absolute path. Moving the project from
a laptop to a cluster does not carry `~/bioinf-shared` with it, and a
link is not an additional backup copy of its target.

Say that relative paths *inside the scripts* make the project easier to
move, then give the short migration contract: preserve the project files,
reinstall the environment from its manifest and lockfile, and recreate
`data/ref` to point to the destination's matching reference. Chapter 2
already distinguishes the laptop and cluster filesystems; reuse that
distinction. Actual transfer commands remain Chapter 9 material.

The shared reference record should include its retrieval source,
version, and checksums, not just the machine-specific link target.
Ensure someone owns preservation of that external target when readers
fill in the backup table.

### 7. Use immutable download sources for a provenance chapter

**Priority: medium. Locations:** sections 4–5 and 7–8; examples/data.

The plan records commits, but describes downloads from the moving
`rnaseq` branch. For the final copy-and-run examples, pin all source URLs
to reviewed full commit hashes or a book release that distributes those
exact files. “Last commit touching this file” and “repository snapshot
used for this exercise” should not be confused.

Keep the original upstream sheet unchanged; record any local adaptation
as a derived file with a short explanation. Supply expected checksums
for the reference and sheet as well as the reads. Preserve the original
download address from Chapter 1 and identify the immutable source used
for the Chapter 3 check.

Do not claim that the `v3.10` directory name proves compatibility with
“current nf-core/rnaseq.” Choose and test the pipeline release in
Chapter 26, then identify that pairing explicitly. Chapter 3 needs a
stable example, not the latest schema.

## Teaching and exercise improvements

### Make the permissions demonstration disposable

**Locations:** section 4; outcome/learning goal 2; `readonly-cant-delete`.

Keep the file-versus-directory distinction; it is exactly the right
practical preview of Chapter 7. Describe `chmod a-w` as reducing
accidental changes, rather than making an immutable archive. The owner
can change permissions again, and changing the parent directory can
still affect the raw directory's name or location.

Demonstrate failed writes and deletion attempts on a toy file in a toy
locked directory before applying the recipe to the actual inputs. If a
reader's permissions differ from those assumed, an unexpected successful
demonstration should not damage their FASTQ files. Keep the unlocking
recipe and explain that adding new files also requires checking and
protecting those new files.

### Give readers a reliable starting state and recovery route

**Locations:** promises; section 4; exercises 1, 2, and 4.

Readers may have only R1: R2 was an exercise in Chapters 1 and 2. Recover
each missing mate independently, rather than only handling the case
where the entire Chapter 1 directory is gone. Begin with `cd
~/bioinf-book`; state what to do if a file is already in `data/raw/`
and that a locked destination must not be overwritten on a repeat visit.

Moving the Chapter 1 files is reasonable and consistent with its
temporary-folder promise. Add a note that readers revisiting old
commands should use the new `data/raw/` path or repeat the old download
steps. The old folder can still contain `fastq_summary.txt`; it is not
necessarily empty after the move.

Put the truncated-copy exercise in a supplied, project-specific practice
directory, rather than the fixed shared pathname `/tmp/broken.fastq.gz`.
Keep the expected failures visible and explain that they are intentional.
For exercise 4, give a save location outside `results/` and demonstrate
how to preserve both run logs. `cmp` is a useful supplied command here;
state that silence means the two files match.

### Tighten two answer keys

- **Checksum failure:** distinguish a digest mismatch from a missing or
  unreadable file. Check the named file, manifest, and working directory
  before assuming transfer damage. A trusted expected checksum is the
  comparison baseline; regenerating it from a damaged copy would hide
  the problem.
- **Metadata join:** a trailing space creates a different identifier,
  but the sample does not always “silently drop out.” The consequence
  depends on the join: it may disappear or remain with missing metadata.
  Say “the records fail to match; Chapter 14 shows how to detect this.”

### Refine backup language without adding a backup-software tutorial

Keep 3-2-1 and the restore test. Add a column for retention/version
history and one for the person or service responsible for recovery.
“Backed up: yes” is not enough if deletions are recoverable for only a
short period.

Change “a git repository backs up code” to “git tracks code history;
an independently stored copy protects it against losing this machine.”
A repository can exist entirely on the same disk as the project, as
shown in the [official Git introduction](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository).
The GitHub mechanics still belong in Chapters 21–22.

The scratch-plus-OneDrive self-check lacks enough information for a
numeric answer. Ask instead whether those locations establish a
recoverable backup, and what the reader needs to verify. The plan already
acknowledges that retained version history can change the answer. Keep
the facility/archive retention condition, and remember that an archive
of original reads may not preserve the exact downloaded test subset.

### Keep the naming lesson practical

Replace “never need quoting” in learning goal 1 with “avoid common path
and sorting problems.” Consistent safe names help; readers should still
learn to quote paths and shell variables in Chapter 5. Use a concrete
allowed character set rather than the vague “no special characters.”

Keep the distinction between author-controlled names and identifiers
received from a facility. Avoid banning meaningful release/version
labels: `reference_R64-1-1` or a versioned exported deliverable is useful.
The problem is unexplained names such as `final_final_v2`, not version
information itself. Leave `11-3-25` explicitly ambiguous until the source
date convention is established; a rename cannot recover unknown meaning.

## Scope and series alignment

The current coverage is appropriate for a core chapter. The following
boundaries should survive revision:

| Topic | Chapter 3 should do | Depth stays elsewhere |
|:------|:--------------------|:----------------------|
| Paths, links, permissions | Run a supplied recipe and understand its immediate effect | Chapters 5 and 7 |
| Scripts and logs | Run and inspect a supplied script | Chapters 6 and 8 |
| Storage and transfers | Identify safe locations and a recovery responsibility | Chapters 9–10 and Appendix A |
| Metadata | Map the actual files to samples and preserve identifiers | Chapter 14; nf-core schema in Chapter 26 |
| FASTQ and references | Recognize the files and record their identities | Chapters 15–17; reads-to-alignments methods in Genomics |
| Provenance | Preserve sources, checksums, command, environment, and run record | Chapters 21–24 and 26 |
| FAIR and sharing | One short practical table | Chapters 20 and 22 |
| RNA-seq interpretation | Identify the non-human fixture and its teaching role | Transcriptomics; normalization and FDR in Statistics for Omics |

Do not add alignment, QC/trimming methods, statistical design, or a full
workflow implementation to fix this plan. Likewise, do not relocate the
whole provenance lesson to Part V: the recurring project needs these
habits now. Later books can adapt the layout to their tools rather than
being required to reproduce it exactly.

The early use of commands taught later is acceptable under the book's
examples-first approach. Supply exact commands, one-sentence effects,
and clear stopping points; do not require independent shell programming.

## Visuals, pacing, and reading

The five proposed figures and five tables are a reasonable ceiling.
Keep the project-layout figure for relationships and the folder table
for practical policy; avoid explaining the same tree three times.
The final project tree is most useful if it names the actual new
metadata files, result, and log.

The sample-sheet figure should distinguish *sample → run → mate files*
and mark which files are actually downloaded. This makes the multiple-run
lesson visible without teaching RNA-seq analysis. For readability,
display basenames in the figure and retain the full URLs in the real
source file. Inspect the CSV as CSV in the editor; `column -s, -t` is
not a general CSV parser, and platform differences in empty-field
handling must not shift the very missing fields the lesson depends on.

The proposed symlink figure has three steps, while the shared style
guide proposes four to seven. A useful four-state version is: intact
link; read through link; edit a disposable target through link; remove
only link. This also resolves the broken command sequence noted above.

Keep backups concise but do not make them the first material cut for
length: identifying recoverable storage is an explicit chapter goal.
Reduce repeated layout descriptions, keep FAIR to its table, and move
the full upstream-sheet metadata exercise to an extension before
shortening the practical backup check.

The FAIR table should say these habits **support** FAIR, rather than
implying that a local README and CSV make the project fully FAIR.
Preserve machine-readable metadata, persistent identifiers, and clear
reuse terms. Accessibility can include authentication; it does not
necessarily mean unrestricted access. The [FAIR principles](https://www.gofair.foundation/fair-principles)
make these distinctions explicit.

Keep Wilson, Noble, Wilkinson, and Shotts as the likely four further
reading picks, with one purpose each. Broman and Woo fits Chapter 14
better. The existing plan's scite checks are recorded claims, not checks
repeated by this review; follow the repository's citation workflow when
adding the bibliography entries.

## Recommendations on the open questions

| Question | Recommendation |
|:---------|:---------------|
| Running-data description | Correct the shared description and distinguish the local one-run subset, upstream fixture, and original study. |
| MD5 or SHA-256 | Keep MD5 as the taught transfer check, matching the main outline. Retain SHA-256 in the book's records; an MD5 column is useful, not a reason to duplicate registries. |
| Simulated shared folder | Keep it: it provides a real local symlink without requiring cluster access. Label it as a simulation and document the external target. |
| Move or copy Chapter 1 inputs | Moving is consistent with the prior promise. Add partial-download, repeat-visit, and old-path recovery notes. |
| Notebook tool | Default to `NOTEBOOK.md`; accept an existing institutional notebook. The assessment is whether decisions and dates are recorded. |
| Site backup facts | Verify them in Appendix A before publishing the chapter's table, date the check, and link to the official policy. Do not infer backup from “project storage.” |
| Outstanding command tests | Keep Linux/WSL symlink behavior open. Test permissions on disposable fixtures, CSV display with empty fields, both successful and failing script runs, and repeated runs on the same day. |

## Suggested acceptance checks for the revised plan

1. A reader with only Chapter 1's R1 file can reach the same final state
   as a reader who completed all earlier exercises.
2. The checksum check works verbatim from the stated project directory;
   a missing file and a changed file produce understandable failures.
3. Every local raw file has an inventory entry, a trusted expected
   checksum, and a source record. Upstream-only examples are labelled.
4. A successful run produces the expected two 50,000-read rows and a
   distinct log; a failed run preserves its error and does not publish
   a misleading successful result. A same-day rerun preserves both logs.
5. Readers can explain what deleting a symlink removes, what must be
   recreated on a second machine, and who preserves the reference.
6. The README gives the rerun command; the notebook records a decision;
   the storage table identifies a recovery route for important files.

**Verification limits:** I tested checksum path resolution and the
reported symlink behavior on this macOS host using disposable fixtures.
I inspected the upstream sample sheet and versioned nf-core documentation.
I did not run the complete Pixi/SeqKit exercise, validate Linux/WSL
behavior, recheck the real-data digests, or audit current site backup
policies. Those remain drafting checks, not verified findings here.
