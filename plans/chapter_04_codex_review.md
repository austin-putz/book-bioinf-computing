---
title: "Chapter 4 plan — Codex review"
subtitle: "Advisory review · issues, comments, and proposed fixes"
date: 2026-11-17
---

Reviewed [chapter_04.md](chapter_04.md) against the full
[chapter outline](PLAN_CHAPTERS.md), repository guidance, the
[series guidance](../../CLAUDE.md) and [series plan](../../PLAN.md),
the chapter template and shared style guide, the written Chapters 1–2,
the Chapter 3 plan and its review, and the book's reporting page and
issue form. Locations below refer to the reviewed Chapter 4 plan.
Recommendations are advisory; the source plan and Austin's notes are
unchanged.

**Overall assessment:** keep the structure and scope. The chapter covers
the main outline's topics, teaches a useful diagnostic routine before
the longer command-line part, and makes help-seeking a practical skill.
The methods-reading exercise connects troubleshooting to scientific
provenance particularly well. The main revisions are to make failures
reproducible in the promised order, distinguish observations from
diagnoses, and make the help request contain enough evidence to answer.
There is no need for a new major section or deeper RNA-seq teaching.

## Corrections before drafting

### 1. Finalize and test the broken script before promising its failure sequence

**Priority: high. Locations:** outcome/check; exercise 1; open question 4.

The outcome promises three failures in turn, and exercise 1 lists a
filename typo, an en dash, and an invented flag in that order. No script
is supplied yet. If all three defects are in one SeqKit command,
argument parsing finds `--paired` before attempting to open the files.
The invented flag therefore appears first, regardless of the filename
typo's position.

I tested this with SeqKit 2.14.0 and a small synthetic FASTQ. A command
containing all three defects reports `unknown flag: --paired`; the
individual typo and en-dash cases produce the messages recorded in the
plan.

Two reasonable fixes are:

- Use one command and explicitly let the order be invented flag →
  en-dash/file-path errors → successful result, matching the tested
  argument order.
- Supply three short script versions, each with one defect. Readers
  diagnose each version before seeing the corrected command.

Prefer the first if the intended lesson is that fixing one error can
reveal another. Preserve the exact starting file, each intermediate
version, captured messages, exit statuses, and final command so the
answer key is reproducible. If using several commands in one script,
ensure it stops at the intended failure; otherwise later commands can
run and obscure what happened. Readers should edit supplied material,
without needing to understand shell control flow yet.

Three defects are enough. The wrong-working-directory case already
appears in section 4; a fourth defect adds little.

### 2. Separate environment diagnostics from the failing tool's version

**Priority: high. Locations:** sections 2 and 7; exercise 3;
`tbl-request-checklist`; relationship to the issue form.

`pixi info`, `seqkit version`, and R's `sessionInfo()` answer different
questions. They should not be presented as interchangeable ways to
supply “versions.” With Pixi 0.84.2, I confirmed that `pixi info` reports
workspace/platform/environment information but does not identify the
installed SeqKit version as 2.14.0.

For a SeqKit failure, the supplied request should include:

```bash
cd ~/bioinf-book
pixi info
pixi run seqkit version
```

Use `pixi list` when package versions are needed, and
`pixi run Rscript -e 'sessionInfo()'` for an R problem. Keep `pixi run`
on the SeqKit version command: bare `seqkit version` may fail or refer
to a different installation, precisely the problem Chapters 2 and 4
teach readers to notice.

The current *Something doesn't run* form asks for chapter/section,
machine, OS, cluster, command, error, and `pixi info`. It does **not**
have separate fields for expected behavior, attempted fixes, the tool's
version, or a small example. Those are useful additions to a general
help request, but the plan's claim that the form already asks for
“exactly” everything taught here is inaccurate.

Describe the form as the starting model, then identify the extra
evidence needed for a tool-specific question. When the chapter is
drafted, consider adding a failing-tool/version prompt to the form and
updating `reporting.qmd` with it. Do not require readers to paste their
whole lockfile into every request.

### 3. Correct the methods-to-sample-sheet comparison

**Priority: high. Locations:** section 5's second discovery; exercise 4;
Chapter 3 dependency.

The plan says the paper's reverse-stranded setting agrees with
`reverse` in Chapter 3's sample sheet “for the same samples.” However,
Chapter 3 explicitly selects `samplesheet/v3.10/samplesheet_test.csv`,
whose two `WT_REP1` rows, including `SRR6357070`, say **`auto`**. The
other samples say `reverse`. See the [upstream sheet](https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/samplesheet/v3.10/samplesheet_test.csv).

Replace that discovery with:

> The paper reports a strandedness setting. Our selected test sheet
> asks the pipeline to infer strandedness for WT_REP1. That is a request
> to infer a value, not an independent confirmation of the paper's value.

This is a useful reading exercise without explaining strandedness
mechanics. Let Chapter 26 and Transcriptomics handle the pipeline
behavior and biological interpretation.

The paper's stated tool versions, reference release, typeset dash
problems, and CC BY license are supported by the [article itself](https://pmc.ncbi.nlm.nih.gov/articles/PMC6310685/).
Keep that example. Describe the proposed missing information as “not
reported in this excerpt” unless the full paper, supplements, and
deposited materials have been checked. Readers examining a selected
paragraph cannot establish that an item is absent everywhere.

Also distinguish the original study's analysis from the book's nf-core
test run. Using reads from the study does not make the book's later
pipeline a reconstruction of its historical RSEM/STAR analysis.

### 4. Keep the exit-status example, but make its version boundary explicit

**Priority: high. Locations:** section 3; examples/data; misconception
`no-error-means-correct`; Chapter 8 handoff.

The surprising truncated-file example is real for the pinned version:
I reproduced `[ERRO] ... unexpected EOF` with **exit status 0** using
SeqKit 2.14.0 on a synthetic truncated gzip FASTQ. Keep it as a tested
observation, rather than dropping it because an error should normally
produce a nonzero status.

However, the [current SeqKit documentation](https://bioinf.shenwei.me/seqkit/usage/#input-and-output-files)
describes nonzero status for read/decompression errors unless errors
are explicitly skipped. That difference makes this a particularly good
example of the chapter's version-checking lesson. Label the capture
“SeqKit 2.14.0” and retest it whenever the book lockfile changes. Do not
promise the same status for every release or every form of corruption.

Suggested general explanation:

> An exit status of 0 means the program reported success to the shell.
> It does not prove the output answers your question. Read messages and
> check the result against something you know.

Likewise, replace “an error stops” with “an error reports a failed
operation; whether the surrounding script continues depends on the
program and script.” Warnings call for inspection; they do not always
mean the result is wrong. Converting `n/a` to `NA` may be intended, but
it must agree with the meaning of the column.

Show `echo $?` immediately after the command under discussion. A
subsequent `cat`, `ls`, or help command replaces the status being
examined. Leave pipeline-status mechanics to Chapter 8.

### 5. Replace the unmatched-input case with a failure the supplied tools produce

**Priority: medium. Locations:** section 4's second case; checklist;
chapter check.

The proposed “empty results table because the input pattern matched
nothing” does not specify a command. With ordinary Bash settings, an
unmatched wildcard is passed literally. SeqKit 2.14.0 then complains
that that pathname does not exist and exits 255; I verified the SeqKit
response to the literal pattern. Other shell settings or a different
script can produce other outcomes.

Specify the actual command and capture its behavior. For the existing
setup, a good case is a mistyped directory or `*.fq.gz` when the files
end in `.fastq.gz`: diagnose the literal wildcard in the error and use
`ls` to inspect the directory. If an empty result is the intended case,
supply a script that demonstrably produces one and explain why.

Keep “one cause at a time” visible. `Killed` can suggest a resource
problem, but it does not by itself establish out-of-memory failure;
the later scheduler/accounting evidence supplies that diagnosis.

### 6. Make the minimal example reproduce the same failure

**Priority: medium. Locations:** section 7; exercise 3; examples/data.

Making a file smaller does not automatically make a reproducible
example. The request needs the command, relevant directory layout,
small shareable input or its creation instructions, expected behavior,
and the same observed failure after reduction.

Exercise 3 uses the filename-typo failure. That failure generally needs
no real sequencing data: a synthetic file under the intended name and
the mistyped command can demonstrate it. A 100-read copy of the real
file is optional and may distract from the path error. For a corruption
failure, the first 100 intact reads might remove the corruption and
cease to reproduce the bug. Teach readers to retest the failure after
each reduction.

For a working small-file recipe, use the already-installed format-aware
tool and write only to the exercise folder:

```bash
cd ~/bioinf-book
mkdir -p ~/bioinf-ch04
pixi run seqkit head -n 100 data/raw/SRR6357070_1.fastq.gz \
  -o ~/bioinf-ch04/small_R1.fastq.gz
pixi run seqkit stats -T ~/bioinf-ch04/small_R1.fastq.gz
```

I verified this command form with SeqKit 2.14.0 on synthetic data; it
produced a valid 100-record FASTQ. Check the real-data example while
drafting. The original four-lines-per-read recipe works for this book's
specific FASTQ, but is not a general FASTQ rule, and early termination
of a decompression pipe can generate confusing broken-pipe behavior.
Chapter 15 owns format details; Chapter 8 owns pipeline handling.

Keep the privacy rule. Sanitized paths must preserve diagnostic facts:
relative layout, extension, case, the `l` versus `1` typo, and the exact
en dash. Replace private components consistently, rather than replacing
every path with the same placeholder and losing the failure.

### 7. Repair the handoff to logs and the chapter's starting state

**Priority: medium. Locations:** “What this chapter builds on”;
section 4; code conventions; exercise 2.

The Chapter 3 draft log currently records metadata but does not capture
SeqKit's stderr. Its date-only log filename is also overwritten on
same-day reruns. The [Chapter 3 review](chapter_03_codex_review.md)
already proposes corrections. Until that is resolved, Chapter 4 cannot
assume that finding the project log reveals the failed command's error.

Give this chapter one named, tested failing example and its actual log
path, with the useful message visible. Supply captured text for readers
without that file. Do not imply that every application automatically
logs terminal errors or that a log always contains the cause.

After the deliberate `cd ~` example, explicitly return to
`~/bioinf-book` before the next command. Qualify the expected Pixi
failure with a clean setup: if the reader has another manifest in a
parent directory or an active environment, the message can differ.
State that bare `seqkit` fails only when it is absent from the current
shell's `PATH`; another installation can make it run the wrong version
instead. Controlled examples or captured output are preferable to
changing the reader's real environment to force a failure.

Exercise 2 should say `pixi run seqkit stats -a -T ...`, not bare
`seqkit stats -a -T`. I confirmed that `-j, --threads` is present in
SeqKit 2.14.0 help; that part of open question 7 can be closed.

## Teaching and presentation suggestions

### Teach observable clues before naming a cause

The “who / what / on what” figure is useful. Present it as a reading
strategy, not a promise that every message supplies all three: `Killed`
and many crashes do not. `[ERRO]` is a severity label, not a unique
program identifier; the command and surrounding log establish who
printed it.

Keep the R example where the useful path detail appears after the
headline error. Say “find the earliest relevant failure in this run”
rather than “the first error is usually the cause” as an absolute
workflow. Retried runs and combined logs can contain old or recovered
errors. A short relevant log excerpt with surrounding context can be
more useful than an enormous pasted log; preserve the complete text
locally and follow the destination's upload/posting instructions.

### Make the request artifact part of the chapter check

The final read count verifies one debugging exercise, but not whether
the reader can ask for help. Add a second inspection of
`help_request.md`: can someone reproduce the failure from the supplied
commands and input without access to the reader's home directory?
The annotated model answer can show both the broken request and the
one missing fact that would otherwise force a follow-up question.

Keep “do not submit it.” No account, paid assistant, public post, or
cluster access should be required for the chapter's core outcome.

### Keep the AI section short and test meaning as well as syntax

The fabricated `--paired` example is well chosen and already uses an
installed tool. Correct it with the two explicit mate filenames, then
ask what each output row counts: 50,000 reads per mate file corresponds
to 50,000 pairs for this matched run, not 100,000 pairs. This tests the
request's meaning after the syntax is fixed, without becoming an RNA-seq
lesson.

Keep AI last, after the verification tools have been taught. Label the
answer as a constructed example rather than implying it is a captured
output from a particular assistant. Change `ai-code-is-tested` to say
that code should not be **assumed** to have been tested; even reported
tests may use different inputs or environments. The important skill is
checking the evidence and reproducing the relevant result.

The supplied answer should be the normal exercise path; using an
assistant can be an optional variation. Direct readers to current
institutional guidance without making this chapter depend on a
particular product or policy page.

### Keep support routes specific and manageable

Retain the source table, but route by the problem rather than imposing
a long universal search order: site/account/quota problems → site
support; package usage → its designated support venue; a book command
that fails → the book's reporting page. Searching closed issues is a
good addition. The [Bioconductor posting guide](https://bioconductor.org/help/support/posting-guide/)
supports package tags, session information, complete relevant output,
and a small self-contained example.

An hour without progress is a useful flexible checkpoint, not an
admission requirement for asking. Beginners also cannot always know
whether a filesystem is broken “for everyone.” Encourage reporting the
observed symptom and evidence without requiring that diagnosis first.

Keep text as the required medium for command-line messages. A screenshot
can supplement text for a VS Code layout or dialog problem; it should
not replace the command and message. The issue form's text requirement
can remain unchanged.

### Control visual and terminology load

Four figures and seven tables are already plenty for this short Part I
chapter. The error reference table has eleven entries, including R and
Python messages not taught until Part III. Split it into common cases
readers diagnose now and a compact “recognize later” reference, or move
the latter entries beside their later chapters.

The stepped checklist should allow an exit when the problem is solved
at step 3. Do not carry a solved Pixi case through resource diagnosis
and reduction as if every step were compulsory. The proposed labels
also show eight destinations for seven steps; make “ask” a final
outcome outside the seven-step sequence, or consolidate the steps.

For usage notation, “uppercase words or angle brackets commonly mark a
value you supply” is safer than treating capitalization as a universal
grammar. Emphasize that brackets and angle brackets are not typed
literally in these examples.

The macOS manual mismatch is worth retaining. I reproduced BSD
`man ls`/`man sed` selection on this host and confirmed that prepending
the corresponding Homebrew `libexec/gnuman` directories selects the GNU
pages. If updating Chapter 1, preserve default manual search paths and
test both Intel and Apple silicon prefixes; use package-prefix lookup
rather than hardcoding `/usr/local`. Homebrew's [coreutils formula](https://github.com/Homebrew/homebrew-core/blob/main/Formula/c/coreutils.rb)
documents its manual layout. Keep the version tip even after the setup
fix: executable lookup and manual lookup remain distinct.

## Scope and series alignment

The methods excerpt belongs here as a reading exercise. Do not teach
cutadapt algorithms, RSEM/STAR parameters, DESeq2 design, or sequencing
chemistry to make it understandable. Supply a small glossary and ask
readers to locate evidence, report values, and recognize missing
information.

| Topic | Chapter 4 owns now | Depth remains elsewhere |
|:------|:-------------------|:------------------------|
| Help and usage | Find a flag and the documentation for the installed version | Tool-specific chapters |
| Failures | Identify clues, inspect inputs, and choose a next check | Shell mechanics in Chapters 5–8 |
| Resources | Recognize symptoms and route to the right evidence/help | Chapter 10 and Appendix A |
| Methods reading | Extract tool, version, setting, reference, and source | Analysis methods in Genomics/Transcriptomics; statistics in Statistics for Omics |
| Small examples | Adapt a supplied reproducer and retest it | R/Python practice in Chapters 12–13; debuggers/tests in Chapter 34 |
| Community help | Search and draft a useful request | GitHub mechanics in Chapter 22 |
| Archive metadata | Compare one public record with the paper and local subset | Download/API and checksum details in Chapter 20 |

Exercise 4 should explicitly distinguish the archive's full run from
the book's 50,000-pair subset. Archive FASTQ checksums identify the full
archive files, not the nf-core subset. Provide a dated captured record
as a fallback if the ENA interface changes, and label the units rather
than silently treating every field named “read count” as individual
mate reads. No full archive download is needed here.

## Recommendations on the open questions

| Question | Recommendation |
|:---------|:---------------|
| AI section placement | Keep one short final section that applies the earlier checks. |
| macOS manuals | Fix manual search in Chapter 1 after testing the full setup; keep the Chapter 4 tip. The fix worked for `ls` and `sed` on this Intel Mac. |
| SeqKit citation | Add the requested SeqKit2 citation through the normal verification workflow, and review Chapter 2's citation with it. Keep the older entry where it still supports a relevant claim. |
| Exercise size | Keep three defects; first finalize their actual order and captures. |
| Institutional guidance | Link only current official guidance that applies; a generic instruction to check local policy is sufficient otherwise. |
| Help desks | Name the support role in the chapter and link to Appendix A for maintained site contacts. |
| Outstanding checks | `-j` is confirmed in 2.14.0. The current [samtools 1.25 manual](https://www.htslib.org/doc/samtools-sort.html) does not list `--fast`; using SeqKit for that self-check would avoid requiring a tool absent from the present setup manifest. Retain WSL and rendered-code checks. |

For further reading, keep Dall'Olio, the bug-reporting paper, one AI
paper, and the official minimal-example guide. The author left blank
for the bug-reporting paper is Benjamin C. Haller, confirmed on the
[publisher page](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010540).
SeqKit2 remains a software citation rather than a fifth general reading
assignment. No bibliography entries were added in this review; the
plan's reported scite checks have not been repeated here.

## Suggested acceptance checks

1. The supplied script and each intermediate fix produce the documented
   messages in the documented order under the released environment.
2. The truncated-file capture is labelled with its tested SeqKit
   version, with stderr and exit status captured separately.
3. A reader can follow the wrong-directory example and resume the next
   example from the correct project root.
4. A small reproducer still shows the same failure and writes no files
   into protected raw-data storage.
5. The model help request contains the tool's version, a working input
   or creation recipe, expected/observed behavior, and consistent
   redactions; the issue form and reporting page agree with the text.
6. The methods table distinguishes quoted source text, normalized flag
   spelling, reported values, and information not supplied in the
   excerpt. WT_REP1's `auto` setting is represented correctly.
7. Rendered command blocks preserve U+2013 in the deliberately broken
   command and ASCII hyphens in its correction. Working code and output
   remain separate, with complete captures available.

**Verification limits:** I tested selected SeqKit 2.14.0 failures, its
help flags and small-file command, Pixi 0.84.2 info output, and manual
selection on this macOS Intel host using isolated fixtures or read-only
inspection. I checked the article, upstream sheet, and official
documentation cited above. I did not test Linux/WSL, execute the still
unspecified final exercise script, independently recheck the live ENA
record, or audit institutional AI policies. Those remain drafting
checks rather than verified findings here.
