# Chapter 6 — Codex review

Reviewed: 2026-11-18  
Chapter: [Text tools and pipes](../chapters/06-text-tools.qmd)  
Revision reviewed: working tree based on `7c0b8f7`. Chapter SHA-256:
`07461330e5e967d1adb99ebeb77c1afefe2640b1123e1e2915c184c380b3df7b`.

The chapter renders successfully, and its central numerical examples
match the checksum-verified inputs. I found two medium-priority issues
and one low-priority correction. These findings concern the written
chapter, rather than its earlier plan. No chapter, figure, environment,
or project-data files were changed for this review.

The strongest teaching sequence is the progression from ordinary pipes to
separate output streams and then a successful partial count of broken
input. The metadata duplicate, the `@` quality-character trap, and the
reverse-complement exercise also make abstract rules observable. The
draft addresses the earlier plan review well: it checks mate-ID counts
as well as equality, identifies the gzip implementation, limits the
four-line FASTQ shortcuts, and provides both a regex tester and a static
fallback. Keep that structure.

## Findings

### 1. Repeated test labels are incorrectly described as the same biological sample

**Priority: medium.** Locations: [chapter source](../chapters/06-text-tools.qmd),
lines 749–754 and 2045–2047; related wording at lines 1152–1153.

The sample-sheet discussion describes repeated labels as “two runs of
the same sample.” Exercise 5 similarly says that `RAP1_UNINDUCED_REP2`
appears twice because that sample has two single-end runs. These are the
fixture's test groupings, not the original study's biological samples
or sequencing layouts. Chapter 3 explicitly teaches this distinction,
but Chapter 6 reverses it while interpreting the same file.

**Verification:** I downloaded fresh ENA file reports for the four runs
under the two repeated labels:

| Test-sheet label | Runs grouped under it | Original biological samples |
|:-----------------|:----------------------|:----------------------------|
| `WT_REP1` | `SRR6357070`, `SRR6357071` | `GSM2879618`, `GSM2879619`: wild-type biological replicates 1 and 2 |
| `RAP1_UNINDUCED_REP2` | `SRR6357074`, `SRR6357075` | `GSM2879622`, `GSM2879623`: uninduced biological replicates 2 and 3 |

All four ENA records report `PAIRED`. The distinct BioSample accessions
also confirm that the repeated labels do not mean one biological sample
sequenced twice. This agrees with
[Chapter 3's provenance discussion](../chapters/03-organizing-projects.qmd),
lines 806–825 and its Exercise 3. See, for example, the ENA reports for
[SRR6357070](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR6357070&result=read_run&fields=run_accession,sample_accession,sample_alias,sample_title,library_layout&format=tsv)
and
[SRR6357071](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR6357071&result=read_run&fields=run_accession,sample_accession,sample_alias,sample_title,library_layout&format=tsv).

**Suggested correction:** retain all the counts, but say “seven runs
under five test labels; two labels each group two runs to exercise
merging.” Describe the three rows without R2 paths as **used as
single-end inputs in this test sheet**. In Exercise 5, say that the
label appears on two such test rows, and link back to Chapter 3 for
why that grouping differs from the original experiment. This preserves
the text-processing lesson without teaching readers to infer biological
replication from pipeline test labels.

### 2. Exercise 2 empties the input before demonstrating duplicate appends

**Priority: medium.** Locations: [chapter source](../chapters/06-text-tools.qmd),
lines 1880–1898 and 1907–1918.

The exercise provides one copy command followed by a block containing
four faulty commands. The third empties `counts_copy.tsv`; the fourth
then reads that empty file and appends nothing. Running the fourth
command twice at that point cannot reproduce the answer's duplicated
names. Readers following the displayed sequence therefore see a
different problem from the one the fourth case is meant to teach.

The answer's prose does tell readers to re-make the copy after the
destructive command. However, the supplied correction block does not
include that reset. Copying it after the faulty block silently produces
empty per-file counts, an empty sorted table, and an empty filename
list. This is especially misleading in a chapter about successful
commands producing unusable results.

**Reproduction:** I ran the setup, all four faulty lines, and the
correction block in their printed order. `counts.tsv` remained **196
bytes**, while `counts_copy.tsv`, `reads_per_file.tsv`,
`counts_sorted.tsv`, and `files.txt` were all **0 bytes**. Restoring the
copy first made the correction block produce the expected nonempty
outputs. With a restored input, two executions of the append command
produced six lines, demonstrating the intended duplication.

**Suggested correction:** separate the faulty cases or explicitly
restore `counts_copy.tsv` before the fourth case. Include the same
`cp …/counts.tsv …/counts_copy.tsv` reset at the start of the answer's
runnable correction block. Say to repeat the fourth faulty command
twice while its input is nonempty. That makes both the failure and the
repair reproducible by following the page in order.

### 3. `join` and `comm` require a consistent locale, rather than specifically `C`

**Priority: low.** Location: [chapter source](../chapters/06-text-tools.qmd),
lines 782–790, especially the parenthesis at lines 788–789.

The locale explanation correctly says that `LC_ALL=C` applies to one
command only, but then says `join` and `comm` need input sorted “that
way.” They require input sorted according to their own comparison rules;
they can use a non-`C` locale too. Setting `C` only for the preceding
`sort` can actually make input unsuitable for a comparison tool that
still runs under the default locale.

**Reproduction:** with GNU coreutils **9.11**, sorting the two lines
`a 1` and `B 2` under `C` and comparing the result under
`en_US.UTF-8` using `comm --check-order` returned **1** with
`file 1 is not in sorted order`. Sorting and comparing under
`en_US.UTF-8` throughout succeeded, as did `join --check-order` on those
consistently sorted inputs. The
[GNU `comm` manual](https://www.gnu.org/software/coreutils/manual/html_node/comm-invocation.html)
and
[`join` sorting guidance](https://www.gnu.org/software/coreutils/manual/coreutils.html#Sorting-files-for-join)
state the required consistency.

**Suggested correction:** say “Use `LC_ALL=C` when the order must be
reproducible. Tools such as `join` and `comm` also need their inputs
sorted using the same locale and comparison rules they use; if you
choose `C`, apply it to those commands too.” No new exercise is needed.

## Verification performed

- Rendered with `quarto render chapters/06-text-tools.qmd`: successful,
  without reported missing-reference or missing-citation warnings.
- Checked all **67 Bash blocks** with `bash -n`: no syntax errors.
  Replayed all 67 blocks in source order in a disposable project and
  scratch directory, preserving file state between blocks. Runs used
  Bash **5.3.15**, GNU coreutils **9.11**, GNU grep **3.12**, GNU sed
  **4.10**, GNU Awk **5.4.1**, GNU gzip **1.15**, and SeqKit **2.14.0**
  on macOS Intel, with `en_US.UTF-8`.
- Redirected the chapter's absolute home/project path prefixes into
  temporary storage and replaced `pixi run seqkit` with the matching
  available SeqKit binary. The user's home, startup files, and reader
  project were not modified. The temporary raw-data directory and its
  files were made read-only for the intended permission failure.
- Reused local copies of both FASTQ files, the compressed genome and
  annotation, and the upstream sample sheet only after verifying all
  five SHA-256 hashes against `data/README.md`.
- Confirmed **200,000 lines**, **50,000 reads of length 101** per mate,
  **21,662** distinct R1 sequences, and the three most common sequences
  with counts **208**, **186**, and **123**. The first FASTQ records
  and context-search output match the actual input.
- Reproduced the overwrite-to-zero demonstration, scoped `noclobber`
  refusal, raw-directory write failure, `tee` output, and separate and
  combined stream captures. The early-closing `head` probe returned
  `PIPESTATUS` **`141 0`** in this run. GNU gzip emitted **89,515**
  newline characters from the million-byte truncated copy, while the
  pipeline's last command returned success, matching the chapter.
- Confirmed the sample-table MD5
  **`971d8f742cb76a8d181d3bdc3dcbceaa`**, seven lines, duplicate
  `sample_B`, and totals **194** and **164**. Verified sample-sheet
  label counts, strandedness counts, 11 FASTQ paths, four R2 paths,
  and both displayed locale orderings.
- Confirmed the five GTF feature counts **129/124/118/115/114**,
  **599** lines on `I` and one on `not_in_genome`, **64** plus-strand
  and **60** minus-strand transcript lines, the three longest spans,
  **124** distinct gene IDs, and the five gene-biotype counts.
- Confirmed the exact motif counts **1,916** and **1,910**, the
  `GAATTC`/`GA.TTC` line and occurrence counts, all six R1 quality
  character counts, and the `@` toy example's incorrect count of
  three versus the true count of two. Independently checked **35,761**
  R1 sequence lines containing `CTG`.
- Confirmed **280** and **18,842** `N` bases. Checked every base/quality
  position in both files: `N` and quality `#` coincide exactly, as
  claimed. The text-tool and SeqKit FASTQ-to-FASTA outputs agree.
- Verified **50,000** extracted IDs per mate, identical in order;
  changing the third ID produced the quoted difference at **character
  61, line 3**, status **1**. Confirmed the small compressed file's
  **400** lines and successful integrity check, and the sequence-only
  compressed file's exact size of **853,893 bytes** with GNU gzip 1.15.
- Ran the reverse-complement exercise: literal `grep` and SeqKit with
  `-P` each counted **0**; SeqKit without `-P` counted **1**, consistent
  with its [documented strand behavior](https://bioinf.shenwei.me/seqkit/usage/#grep).
- Evaluated the regex tester's actual JavaScript matching code under
  Node and compared all **eight** presets against GNU `grep -E` and
  the static answer table: all agree on which lines match. Invalid
  and empty patterns return the intended feedback.
- Confirmed all **30** referenced section, figure, and table
  identifiers exist and all **five** bibliographic citation keys are
  present. Parsed the five included SVGs as XML and confirmed their
  inclusion, the stepped-figure script, and the Observable code in
  the generated HTML.

## Limits and release notes

Runtime verification used macOS Intel with the matching GNU tools;
I did not repeat the walkthrough on Linux, WSL, or a cluster. SeqKit
and GNU gzip came from existing local installations rather than a fresh
reader setup, and the replay substituted the SeqKit binary for Pixi.
This review therefore checks the commands' behavior, not a new
installation or every platform's diagnostics and locale collation.

The browser tool reported no available browser. The JavaScript checks
establish matching behavior, not that Observable's controls, SVG
highlighting, or CDN loading work in a browser. Visual layout, dark
mode, narrow screens, stepped controls, and browser accessibility
remain untested. The earlier-chapter log workflow and bibliographic
editorial notices were not re-audited.
