---
title: "Chapter 6 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-17
---

Reviewed [chapter_06.md](chapter_06.md) against repository and series
guidance, the [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared style guide, written Chapters 1–4, Chapter 5 and 7 plans,
`data/README.md`, and the book environment. Locations refer to the
2026-11-17 plan. Recommendations are advisory; the plan and Austin's
notes are unchanged.

**Overall assessment:** the chapter has strong examples, especially
the nonadjacent metadata duplicate, separate stdout/stderr, destructive
redirection, and the deliberately mismatched GTF sequence name. Keep
those. Correct the mate-ID check, replace implementation-specific
partial counts, and reduce the amount of GTF/FASTQ programming required
before readers have met the format chapters.

## Corrections before drafting

### 1. Define mate IDs from the actual headers and check the number of IDs too

**Priority: high. Locations:** outcome/check, lines 97–101; exercise 3,
lines 568–572; captured-output list.

The real first headers are:

```text
@SRR6357070.25017281 25017281/1 kraken:taxid|4932
@SRR6357070.25017281 25017281/2 kraken:taxid|4932
```

The mate marker is in the second whitespace-delimited field, followed
by an additional annotation. It is **not at the end of the header**.
A natural implementation such as `sed 's|/1$||'` on the whole header
therefore fails. The plan's stated first result,
`@SRR6357070.25017281 25017281`, also requires dropping the annotation,
not merely stripping `/1` and `/2` endings.

For this fixture, compare the first field alone. It is already the
same identifier in both mates:

```bash
gunzip -c data/raw/SRR6357070_1.fastq.gz \
  | awk 'NR % 4 == 1 {print $1}' \
  > ~/bioinf-computing-ch06/ids_R1.txt
gunzip -c data/raw/SRR6357070_2.fastq.gz \
  | awk 'NR % 4 == 1 {print $1}' \
  > ~/bioinf-computing-ch06/ids_R2.txt
wc -l ~/bioinf-computing-ch06/ids_R1.txt ~/bioinf-computing-ch06/ids_R2.txt
cmp ~/bioinf-computing-ch06/ids_R1.txt ~/bioinf-computing-ch06/ids_R2.txt
```

Expected: 50,000 lines in each file, 100,000 total, first line
`@SRR6357070.25017281`, and `cmp` status 0 with no output. I verified
that all 50,000 first-field IDs agree in order on the checksum-matched
files. This is a fixture-specific four-line FASTQ example, not a general
FASTQ parser.

The count is necessary: `cmp` also succeeds on **two empty files**,
which I reproduced. A successful comparison establishes equality of
the extracted lists, not that extraction worked or that the input FASTQ
files were valid. Add a small negative example with one altered ID so
readers recognize a real mismatch. Introduce `cmp` and its exit status
where it first appears.

If removing mate suffixes is an essential learning goal, keep it on a
tiny header fixture whose suffix locations are specified, or normalize
the second field explicitly and show the exact result.

### 2. Recapture GNU gzip's partial output, not just its error wording

**Priority: high. Locations:** section 4, lines 199–218; examples/data,
lines 622–624; misconception `pipe-stops-on-error`; open question 1.

The plan correctly labels the current capture as Apple gzip. However,
the planned GNU recapture must update the **count** as well as the
messages and exit statuses.

Using the checksum-matched R1 file truncated to exactly 1,000,000 bytes,
GNU gzip **1.15** on this Mac returned status **1** and emitted
**89,515 newline characters** before reporting unexpected end of file.
The plan's Apple-gzip capture reports **89,253**. Both demonstrate the
same failure, but the incomplete output differs between implementations.

Keep the example, and phrase the lesson as:

> Decompression failed after producing partial text. `wc` successfully
> counted the text it received. That count is incomplete and cannot be
> used as the read count.

Label an exact number with the captured gzip version; do not make
non-divisibility by four the test of corruption. A different truncation
can coincidentally produce a multiple of four and still be wrong.
Likewise, status 141 from an early-closing `head` is a common capture,
not a guaranteed status for every program, input size, and scheduling
order. Chapter 8 can explain pipeline status and `pipefail` fully.

Keep the distinction from the pinned SeqKit 2.14.0 status-0 bug.
`pipefail` detects a nonzero stage status; it cannot repair a tool that
reports success despite an error. This is exactly why the result checks
from Chapter 4 still matter.

### 3. Complete the adapter exercise: the two defaults happen to agree here

**Priority: medium. Locations:** section 6, lines 313–315; exercise 6,
lines 584–590; open question 1.

I tested SeqKit **2.14.0**, including its installed help. Sequence
searches inspect both strands by default; `-P` restricts to the positive
strand. On the actual files, however, both choices give the same counts:

| Input | Literal motif on sequence lines | SeqKit both strands | SeqKit `-P` |
|:------|---------------------------------:|--------------------:|------------:|
| R1 | 1,916 | 1,916 | 1,916 |
| R2 | 1,910 | 1,910 | 1,910 |

Thus the answer to “do they agree?” is **yes for this fixture**. Do not
promise that the default search produces a discrepancy. Use `-s -P`
for the matching comparison, and, if strand behavior is part of the
exercise, add one toy record containing only the reverse complement
`GCTCTTCCGATCT`. This makes the distinction observable without relying
on the real files to contain it. SeqKit's
[official usage documentation](https://bioinf.shenwei.me/seqkit/usage/#grep)
describes these search options; the installed 2.14.0 help is the version
authority for this exercise.

The existing `grep … | seqkit stats` approach is fine. If simplifying
to a direct count, the SeqKit flag is **`-C`**, not GNU grep's `-c`.

Describe 1,916 as reads containing this **exact motif**, not as an
adapter-contamination estimate or proof of why the historical paper
selected its trimming parameters. Partial adapters, mismatches, and
biological interpretation belong in the applied books.

### 4. Keep every written output in scratch and every SeqKit invocation in Pixi

**Priority: high. Locations:** sections 3–4, lines 181 and 199–202;
section 9, lines 391–395; code conventions and decisions.

The chapter's default working directory is `~/bioinf-computing`, and
the explicit decision is that Chapter 6 output goes to
`~/bioinf-computing-ch06/`. Several abbreviated examples instead use
bare `counts.tsv`, `out.tsv`, `err.txt`, and `seqs.txt.gz`, which would
be created in the project. The `tee` example also uses bare `seqkit`,
although readers have not entered `pixi shell`.

Make every runnable block obey the stated convention. For example:

```bash
pixi run seqkit stats -T \
  data/raw/SRR6357070_1.fastq.gz \
  data/raw/SRR6357070_2.fastq.gz \
  | tee ~/bioinf-computing-ch06/counts.tsv \
  | cut -f1,4
```

Keep `-T`: `cut` assumes tab-separated fields, whereas SeqKit's default
display table is intended for people. The separately captured error
example should use full scratch paths for both streams too.

Explain the scope and reset of `set -o noclobber`. If left enabled,
later deliberately repeated output commands can fail for a reason
unrelated to their lesson. Demonstrate it in a disposable subshell or
explicitly restore the previous setting. `noclobber` also does not make
all writing tools safe: `tee file` can still overwrite a file.

Notebook entries are a reasonable exception to the “all output in
scratch” statement, but name that exception explicitly.

### 5. Limit the regex tester's equivalence claim

**Priority: medium. Locations:** section 7; `fig-regex-tester`,
lines 450–456; cross-language tables.

Keeping Austin's decided interactive tester is sensible. Calling
JavaScript regexes “extended-style (like `grep -E`)” is only a useful
surface analogy. It does not guarantee identical matches or highlighted
substrings. For example, on `ab`:

- GNU `grep -Eo 'a|ab'` prints `ab` (verified with GNU grep 3.12).
- JavaScript `/a|ab/.exec('ab')` selects `a`, as illustrated in the
  [ECMAScript specification](https://tc39.es/ecma262/multipage/text-processing.html#sec-disjunction).

Label the tester as using JavaScript and validate a deliberately shared
subset of patterns against the chapter's GNU grep examples. Evaluate
each supplied line independently; explain anchors as line boundaries;
display invalid-pattern feedback rather than breaking the figure.
Avoid examples using JavaScript-only constructs. A short fixed
prediction/result table should preserve the lesson when the interactive
figure does not load.

The proposed R example `grepl("^SRR[0-9]+", x)` is valid: base R defaults
to extended regular expressions. I checked it locally and against the
[R regex documentation](https://www.stat.math.ethz.ch/R-manual/R-devel/library/base/html/regex.html).
Keep it, while distinguishing base R, stringr, Python, and JavaScript
engines rather than presenting one universal regex implementation.

### 6. Keep four-line FASTQ shortcuts explicitly attached to this input

**Priority: medium. Locations:** sections 1–2, 6, 8–10; FASTQ-counting
misconception; exercises 1 and 6.

The plan correctly explains why `grep -c '^@'` is unsafe. But several
replacements are called “safe ways” without repeating the file-specific
assumption: `NR % 4`, `head -n 400`, and the GNU sed FASTQ→FASTA command
all assume exactly four lines per record. They do not validate FASTQ
and are not general solutions for wrapped or malformed input.

Keep the useful line-position examples, labelled “for this four-line
fixture.” Present `seqkit stats`, `seqkit head`, and `seqkit fq2fa` as
the actual processing recipes. Consider moving the clever
`sed -n '1~4s/^@/>/p;2~4p'` into an optional worked contrast: it adds
GNU-specific address syntax to a chapter already introducing both sed
and awk. A simple substitution is enough for core sed practice.

The context example should escape the dot in the exact read accession:
`'^@SRR6357070\.6710070 '`, or use an appropriate fixed-string search.
Otherwise a wildcard dot appears in the chapter that is teaching the
importance of literal dots. Also say that `grep -c` counts matching
**lines**, not occurrences or biological records.

## Teaching and presentation improvements

### Preserve the excellent small table, and use one canonical copy

I reproduced its MD5, seven-line count, and sums **194** and **164**.
The duplicate and `Run 3 final` field make `uniq` and awk's default
whitespace splitting concrete. Keep these before the real sample sheet.
For the main commands, always use the Chapter 6 copy after creating it;
otherwise readers must keep track of two interchangeable paths.

Remove the header **before** arbitrary sorting/filtering when the
subsequent calculation assumes it is the first row. `sort -u` happens
to leave this particular header first in the tested locales, but that
is not a general table-processing rule. Distinguish deduplicating entire
identical rows from identifying duplicate sample IDs: `sort -u` does
not resolve conflicting records with the same sample label.

“Always `sort | uniq -c`” should mean “sort first to count equal values
regardless of their original positions.” Sometimes consecutive runs are
the intended object and sorting would destroy the question. Keep the
beginner habit, but state its purpose.

### Separate a pipe's transport from a program's resource use

Pipes avoid an explicit intermediate file between commands, but they do
not guarantee that the participating programs never write temporary
files or use substantial memory. `sort` may buffer data and spill to
disk; it generally needs all input before producing its final sorted
output. The [GNU sort documentation](https://www.gnu.org/software/coreutils/manual/coreutils.html#sort-invocation)
documents temporary storage and `TMPDIR`.

One sentence beside the pipeline figure is enough. Also do not imply
that `gunzip -c | head` validates the unconsumed remainder: the first
few reads can look intact even when later compressed data is damaged.

### Reduce the required annotation exercise and provide the missing scaffolding

The feature counts and malformed sequence-name discovery are excellent.
I verified the 600 records, feature counts **129/124/118/115/114**, 124
distinct gene IDs, and transcript-biotype counts in the checksum-matched
annotation. The first record is indeed `not_in_genome`.

However, extracting quoted GTF attributes and ranking transcript lengths
introduces attribute parsing and coordinate conventions before Chapter
17. These tasks go beyond “adapt a supplied example” unless the actual
parsing command and a labelled nine-field line are supplied. Make the
feature summary required; make the more involved gene-ID/biotype and
longest-transcript work an annotated extension or later revisit.

For any transcript-length calculation, use `end - start + 1` for the
GTF span, and do not describe that genomic span as spliced transcript
length. Keep the earlier warning that feature rows are not gene counts.
A `bedtools` command is not automatically a drop-in GTF feature filter;
name the concrete operation/package in the comparison table or retain
awk for this simple column test.

### Keep stream conventions as conventions

“Results on stdout, messages on stderr” is a useful tool convention,
not a guarantee the shell enforces. Some programs mix them or provide
their own log files. Redirection routes a file descriptor's bytes; it
does not classify text by meaning. This supports Chapter 4's advice to
inspect the actual result and messages.

The Chapter 6 color plan currently makes all stdout/results `good` and
all stderr `warn`. The series style guide reserves green for checks,
blue for data and its reorganizations, and vermillion for pitfalls.
Keep ordinary result streams blue and routine stderr neutral; reserve
vermillion for the demonstrated decompression error or overwrite.

## Verification and remaining limits

Local checks used Bash 5.3.15, GNU coreutils 9.11, GNU grep 3.12,
GNU Awk 5.4.1, GNU gzip 1.15, and SeqKit 2.14.0 on macOS. The FASTQ
and GTF MD5s matched `data/README.md`. Checks included the real header
layout, all mate-ID comparisons, adapter counts with/without `-P`,
the truncated gzip's emitted line count, toy-table checksum/sums, and
the GTF counts above. These were temporary-file checks, not changes to
the project data or environment.

No Ubuntu/WSL or cluster run was performed. The exact Linux diagnostic
text, site locale defaults, and full reader exercise sequence still
need capture when drafting. Retain version labels and distinguish
supplied output from a result verified on every supported platform.
