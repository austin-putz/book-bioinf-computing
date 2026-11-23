# Chapter 8 — Codex review

Reviewed: 2026-11-22  
Chapter: [Shell scripts](../chapters/08-shell-scripts.qmd)  
Revision reviewed: working tree based on `d7bd1e1`, including the existing
uncommitted chapter and five new figures. Chapter SHA-256:
`ca325d37270ae90bc2f55bff2b5cde9cc802f1260270303525c624e4ca2d8c48`.

The chapter renders successfully. Its main scripts, expected counts,
checksum failures, strict-mode demonstrations, and failed-rerun example
work as described. I found two medium-priority issues and two low-priority
corrections. These findings concern the written chapter, rather than its
earlier plan. No book source, figure, environment file, real git setting,
or reader-project file was changed for this review.

The draft addresses the earlier plan review carefully: it preserves the
loop's aggregate failure flag, explains collapsed empty TSV fields,
distinguishes grep's expected status 1 from an input error, and actually
demonstrates the old result surviving a failed rerun. The explanation of
the staging area and the recovery exercise also agree with git's
behavior. Keep those demonstrations and the two-sitting structure; the
remaining changes can stay small.

## Findings

### 1. The final project pipeline still publishes the known header-only SeqKit result

**Priority: medium.** Locations: [chapter source](../chapters/08-shell-scripts.qmd),
lines 1421–1431, 1658–1659, and 1856–1858.

The strict-mode section correctly demonstrates that SeqKit 2.14.0 can
report a decompression error, return 0, and produce only a header. It
then recommends checking the result. However, the subsequent project
walkthrough adds only a current-directory guard to `01_count_reads.sh`;
it never adds that output check. The final `run_all.sh` therefore retains
the exact failure just demonstrated: it publishes the header-only table,
prints `finished:`, runs `02`, and exits successfully.

This is a missing follow-through in the final script, rather than an
error in the deliberately broken demonstration. Input checksums from a
trusted source prevent that particular damaged input from passing, as
the chapter explains. But the chapter also explicitly demonstrates
checksums made after damage, and recommends output checks as a separate
defense. Readers need one concrete application of that recommendation
in the project they leave this chapter with.

**Reproduction:** in a disposable copy of the project, I first ran the
guarded pipeline successfully. I then truncated R2 to 1,000,000 bytes
and regenerated the copied checksum list, matching the chapter's stated
failure scenario. Both checksum checks passed. SeqKit printed
`unexpected EOF`, but `run_all.sh` returned **0**, ran the GTF summary,
and replaced the previous valid read-count table with a **one-line**
file, MD5 **`db1d8098fba21ca3be9934a6cc0dde37`**.

**Suggested correction:** after the demonstration and before introducing
`run_all.sh`, add a small result check between `seqkit stats` and `mv`.
For this fixed two-file project, checking for a header plus two data rows
already catches the demonstrated failure:

```bash
[[ $(wc -l < results/read_counts.tsv.tmp) -eq 3 ]] || {
  echo "expected two read-count rows" >&2
  exit 1
}
```

Explain that this count belongs to this two-input walkthrough; a general
script should derive the expected number from its input list. Checking
the expected read counts is a useful additional check, but a complete
FASTQ validator is unnecessary here. I tested the small row-count guard:
the damaged run exited **1** before `mv`, and the previous good table
kept MD5 **`e1d81de77934f7ab7b44bf72b7520b32`**. Update the later script
checksum captures if this guard is adopted.

### 2. The table checker silently skips a final row without a newline

**Priority: medium.** Locations: [chapter source](../chapters/08-shell-scripts.qmd),
lines 662–677, 2604–2616, and the completed answer at lines 2640–2652.

The supplied and completed `check_samples.sh` both use a plain
`while … read …; do` condition. Bash assigns the final fields when it
reaches EOF without a terminating newline, but `read` returns nonzero,
so the loop body never checks that row. The script can therefore report
success while the table's final sample points at a missing folder. This
is a separate limitation from the already well-explained empty-field
and CRLF problems.

**Reproduction:** I ran the completed answer against these bytes, with
tabs between the columns and **no newline after `missing_folder`**:

```text
sample	run_folder
last	missing_folder
```

It printed nothing and exited **0**. Adding only the final newline made
it print `last: missing folder missing_folder` and exit **1**. The
chapter's supplied fixture ends in a newline and works correctly.

**Suggested correction:** add one sentence to “Limits of `read`” about
the required final newline. For the table-validation exercise, either
explicitly reject an unterminated table or process the final populated
row. One small repair is to give the unused fields an ordinary variable
name and extend the condition:

```bash
while IFS=$'\t' read -r sample folder rest || [[ -n "$sample$folder$rest" ]]; do
```

The existing body can stay the same. This repaired condition reported
the missing folder and exited **1** in the reproduction. The supplied
loop should still be described as limited to simple, populated fields;
this does not fix its empty-field or CSV limitations.

### 3. The stated git minimum does not cover the default-branch setting

**Priority: low.** Location: [chapter source](../chapters/08-shell-scripts.qmd),
lines 2148–2162.

The chapter says any git version from **2.23** supports the commands
used here, then promises that `init.defaultBranch main` selects `main`
when initializing the repository. `git restore` is available at that
minimum, but the configurable initial branch name arrived in **2.28**.
An older git can store an unfamiliar configuration key without using it,
so this setup does not deliver the promised branch name on 2.23–2.27.
The feature's introduction is recorded in the official
[Git 2.28 release notes](https://raw.githubusercontent.com/git/git/v2.28.0/Documentation/RelNotes/2.28.0.txt),
and its setting appears in that release's
[`init` configuration documentation](https://raw.githubusercontent.com/git/git/v2.28.0/Documentation/config/init.txt).

**Suggested correction:** say “git 2.28 or later for the complete setup
shown here; `git restore` itself requires 2.23.” Alternatively, simply
raise the stated minimum to **2.28**. No additional git lesson is needed.
The local checks used git 2.50.1; the historical version distinction was
checked against the release documentation, not an installed old binary.

### 4. The first script's “from any folder” run instruction needs its path

**Priority: low.** Location: [chapter source](../chapters/08-shell-scripts.qmd),
line 114.

The header says `bash gtf_types.sh (from any folder)`. The input path
inside the script is independent of the current folder, but the
relative script filename in that invocation is not. From a different
folder, Bash fails before running any of the script. This is especially
confusing immediately before the chapter teaches how relative paths
work.

**Reproduction:** from a disposable directory outside the script's
folder, `bash gtf_types.sh` returned **127** with `No such file or
directory`. Giving Bash the script's full path worked and produced all
five expected feature counts.

**Suggested correction:** change the header to
`bash ~/bioinf-computing-ch08/gtf_types.sh (from any folder)`, or say
`bash gtf_types.sh (from ~/bioinf-computing-ch08)`. The script's input
path and the following relative-path explanation can stay.

## Verification performed

- Rendered with `quarto render chapters/08-shell-scripts.qmd`:
  successful, without reported missing-reference or missing-citation
  warnings.
- Extracted all **85 Bash blocks**, including fragments and intentionally
  faulty examples, and checked them with `bash -n`: no syntax errors.
  Runtime checks were selective; this does not mean all blocks were
  replayed as one uninterrupted terminal session.
- Rebuilt Chapter 5's practice tree under a new temporary root. Redirected
  literal reader-project and practice-path prefixes into that root;
  the user's home and existing project were not used as test targets.
- Reused local copies of both real FASTQ inputs and the GTF only after
  verifying their SHA-256 hashes against `data/README.md`. Ran the
  original and guarded `01`, `02`, `run_all.sh`, and Exercise 4's `03`
  using the available book-environment SeqKit **2.14.0**.
- Confirmed **50,000 reads per mate**, all five feature counts, and
  biotype counts **116/4/2/1/1**, totaling **124**. The three output MD5s
  match the chapter: **`e1d81de7…`**, **`3b9c2b4c…`**, and
  **`06f05e65…`**. The original and folder-guarded script checksums also
  match **`76fa8eb6…`** and **`f2867b2a…`**.
- Verified that a checksum mismatch makes the guarded pipeline exit
  **1** before `02`. Repeated `02` after truncating the copied GTF to
  5,000 bytes: exit **1**, no success message, unchanged final result,
  and the same partial `.tmp` counts shown in the chapter.
- Ran ShellCheck **0.11.0** on the extracted project scripts: no
  diagnostics. Confirmed through `pixi run --manifest-path
  setup/pixi.toml --locked …` that the existing environment supplies
  SeqKit 2.14.0 and ShellCheck 0.11.0 and selects Homebrew Bash. No
  environment install or upgrade was needed.
- Checked argument quoting and missing-argument status **2**; the final
  read counter's **4/2/3** toy counts and missing-file status **1**;
  and the logging example's incomplete stdout table with a separate
  stderr error and nonzero status.
- Ran the supplied and completed table checkers. The supplied version
  reports the two missing folders; the completed version also prints
  the four found rows. The CSV adaptation fails every numeric check
  because of CRLF while preserving the folder/R1 results, as described.
  Tested the final-newline failure and proposed repair separately.
- Reproduced grep's no-match failure, the status-sensitive repair
  (`n=0`, exit **0**), and a missing input still exiting **2**. Confirmed
  the conditional-function exception and a real-data `gunzip | head`
  exit of **141** on this machine.
- Ran Exercise 3's completed script on good, missing, truncated, and
  valid empty gzip inputs: only the good file prints `3 reads` and
  `OK`; the three bad cases return **1**. Confirmed Apple's native
  `mktemp` leaves `XXXX` literal before `.log`, as the chapter warns.
- Reproduced the committed header deletion and recovery with
  `git diff HEAD~1`, `git restore --source=HEAD~1`, and a new recovery
  commit in a disposable repository. Identity settings were local to
  that repository; the user's global configuration was not changed.
- Confirmed all **52** distinct referenced section, table, and figure
  identifiers exist, all **five** citation keys are present, and all
  **five** included SVGs parse as XML. Checked their source content
  against the surrounding explanations.

## Limits and release notes

Runtime checks used macOS **15.7.9** on Intel, Bash **5.3.15**, GNU
coreutils **9.11**, Apple gzip/gunzip, and Apple Git **2.50.1**. I did
not repeat the Ubuntu/WSL captures, log into a cluster, install an older
git, reinstall the complete environment, or test VS Code's ShellCheck
extension. Most script checks invoked the installed book tools directly;
the separate Pixi check established tool availability and selection,
rather than replaying every example through Pixi.

The chapter was rendered and its SVG sources checked, but browser
layout, dark mode, small screens, annotation controls, stepped controls,
and accessibility were not visually tested. Bibliographic metadata and
editorial notices were not re-audited. The chapter source hash remained
unchanged throughout the review.
