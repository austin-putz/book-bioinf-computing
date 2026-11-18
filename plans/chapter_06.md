---
title: "Chapter 6 — Text tools and pipes"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
draft plan, 2026-11-17. Outputs marked *captured* were recorded on
2026-11-17 on macOS 15 (Intel) in a clean `bash --norc` (bash 5.3.15)
with Chapter 1's GNU tools first on `PATH` (GNU grep 3.12, GNU sed 4.10,
GNU Awk 5.4.1, coreutils 9.11), seqkit 2.14.0, and `LC_ALL=en_US.UTF-8`,
on the book's own files (MD5s match `data/README.md`). **Not GNU:**
`gunzip` on the test Mac was Apple gzip 457.140.3, because Homebrew's
`gzip` was not installed there; messages from `gunzip` are marked
*captured (Apple gzip)*. After the Codex review the truncated-file
case was recaptured with **GNU gzip 1.15** (conda-forge build, same Mac),
marked *captured (GNU gzip 1.15)*; Linux/WSL captures are still to do.
Everything else is to be checked while drafting.

## From `PLAN_CHAPTERS.md`

- Pipes and redirection; standard output vs standard error
- `>` overwrites: destructive redirection
- `grep`, `cut`, `sort`, `uniq`, `wc`
- `sed` and `awk` basics
- Regular expressions (shared across shell, R, Python)
- Working with compressed files (`zcat`, `gzip`)

## What this chapter builds on

- **Chapter 1** used, without explaining: `gunzip -c … | head -n 8`,
  `gunzip -c … | wc -l`, `$(( … / 4 ))`, `>` to write
  `fastq_summary.txt` and `>>` to add R2's line (the chapter text
  already points to `@sec-text-tools` for `>` and `>>`). Also the
  annotated FASTQ record, "four lines per read *in this file*", and the
  decision to use `gunzip -c`, not `zcat` (macOS's built-in `zcat`
  looks for `file.gz.Z`). This chapter explains every piece.
- **Chapter 3:** the project in `~/bioinf-computing`: `data/raw/`
  (read-only), `data/meta/samplesheet_upstream.csv` (nf-core's sheet,
  unchanged), `data/meta/reads.tsv` and `samples.tsv`, `data/ref ->`
  the shared reference folder with `genome.fa.gz` and `genes.gtf.gz`,
  and `src/01_count_reads.sh`, which writes `results/read_counts.tsv.tmp`
  and then `mv`s it into place, and tees messages into `logs/`. Chapter
  3's plan promises Chapter 6 for "`>` vs `>>`, `cut | sort | uniq` on
  the sample sheet".
- **Chapter 4:** stderr vs stdout was named there ("Chapter 6") in the
  truncated-file capture (header on stdout, `[ERRO]` on stderr, exit 0);
  exit status with `echo $?`; the `no-error-means-correct`
  misconception; the adapter `AGATCGGAAGAGC` from Wu et al. 2018's
  cutadapt command; seqkit's `sum_n` (N bases) of 280 (R1) vs 18,842
  (R2) from exercise 2.
- **Chapter 5** (plan being written in parallel): paths, `cd`, `ls`,
  wildcards and brace expansion, quoting, `find`, `cat`/`less`/`head`/
  `tail`, `file`, `zless`. It defers to this chapter: pipes,
  redirection, `grep`, `sort`, `zcat`, "patterns match file names, not
  contents (that is `grep`)", "globs are not regular expressions", and
  the pipe in `find … -type f | wc -l`. Its practice tree
  `~/bioinf-computing-ch05/share/` includes `meta/samples.tsv`, built
  for this chapter's `cut`/`sort`/`uniq`/`grep`; §5 opens with it
  (decided 2026-11-17), with a recreate block for readers who skipped
  Chapter 5.
- **Chapter 7 owns** (confirmed by the Chapter 7 planning session,
  2026-11-17): permissions, shebang, `PATH`/`type`/`which`, environment
  variables, `.bashrc`, processes and Ctrl-C/`kill`, `df`/`du`, GNU vs
  BSD, and line endings (`file`, `cat -A`, `dos2unix`). This chapter
  uses `cat -A` once only to make tabs visible (`^I`) and links to
  Chapter 7 for the rest; `sed -i`'s GNU/BSD difference is a forward
  link, not taught here.

## Outcome and check

- **Outcome:** readers chain small tools with pipes to answer questions
  about text files without opening them: how many reads, how long, how
  many of each kind, which lines match. They send results to files and
  messages to a separate place, never overwrite an input by redirecting
  onto it, read compressed files through a pipe, write a basic regular
  expression, and use `cut`, `sort`, `uniq -c`, `grep`, `sed`, and `awk`
  on the book's FASTQ, GTF, and sample-sheet files. They know when a
  format-aware tool (seqkit; samtools and bedtools in Part IV) is the
  safer choice.
- **Check:** two parts, both with exact expected output (*captured*).
  1. From `~/bioinf-computing`, one pipeline counts the feature types in
     the test annotation:

     ```bash
     gunzip -c data/ref/genes.gtf.gz | cut -f3 | sort | uniq -c | sort -k1,1nr
     ```

     ```
         129 exon
         124 transcript
         118 CDS
         115 start_codon
         114 stop_codon
     ```

     There is **no `gene` line**, which is itself a finding (§5).
  2. The read IDs of the two mate files are in the same order. In this
     file the header is `@SRR6357070.25017281 25017281/1 kraken:taxid|4932`
     (R2: `…/2 …`): the mate marker sits inside the second field, not at
     the end, and the **first field** is already identical in both mates.
     Exercise 3 writes that field for every record:

     ```bash
     gunzip -c data/raw/SRR6357070_1.fastq.gz \
       | awk 'NR % 4 == 1 {print $1}' > ~/bioinf-computing-ch06/ids_R1.txt
     gunzip -c data/raw/SRR6357070_2.fastq.gz \
       | awk 'NR % 4 == 1 {print $1}' > ~/bioinf-computing-ch06/ids_R2.txt
     wc -l ~/bioinf-computing-ch06/ids_R1.txt ~/bioinf-computing-ch06/ids_R2.txt
     cmp ~/bioinf-computing-ch06/ids_R1.txt ~/bioinf-computing-ch06/ids_R2.txt
     echo $?
     ```

     Expected (*captured*): `50000` lines in each file (`100000 total`),
     first line `@SRR6357070.25017281`, `cmp` prints nothing and `$?` is
     `0`. **Both parts are needed:** `cmp` also says "identical" for two
     empty files (*captured*), so the count shows the extraction worked.
     A negative example with one changed ID shows what a mismatch looks
     like (*captured*: `ids_R1.txt ids_R2_bad.txt differ: char 54, line
     3`, exit 1). `cmp` and its exit status are introduced here. This is
     a check for this four-line file, not a FASTQ parser.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Connect commands with pipes, and send output to a file with `>`,
   `>>`, and `tee`, without overwriting an input.
2. Keep results (standard output) and messages (standard error) apart,
   and capture or discard each on purpose.
3. Count, sort, and summarise columns with `cut`, `sort`, `uniq -c`,
   and `wc`, and find lines with `grep`.
4. Write a basic regular expression and use it in `grep` and `sed`, and
   select and compute on fields with `awk`.
5. Read and write gzipped files through a pipe, and say when a
   format-aware tool is safer than a text tool.

## Sections

Same pattern as Chapters 1–5: each section opens with something readers
run on the book's files, then names the idea. Commands run on the
laptop from `~/bioinf-computing`; anything the reader writes goes to the
scratch folder `~/bioinf-computing-ch06/` (`mkdir -p ~/bioinf-computing-ch06` in §1),
**never** into `data/`; every runnable block uses full scratch paths
for what it writes. The one exception: exercises add entries to the
project's `NOTEBOOK.md` (Chapter 3's habit). Every seqkit call is
`pixi run seqkit` (readers have not used `pixi shell`). Visual items in brackets are specified under
*Visuals and teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   most bioinformatics files are plain text with one record per line
   (or per four lines), so a dozen small tools, each doing one job,
   answer most quick questions when joined with `|`. This is the "Unix
   philosophy" in one sentence, no history lesson. Point back to
   Chapter 1's commands: "you ran pipes already; now you will see what
   they do". Make the scratch folder.
2. **Pipes.** *Start hands-on:* rerun Chapter 1's two commands on the
   project's file: `gunzip -c data/raw/SRR6357070_1.fastq.gz | head -n
   8` and `… | wc -l` (`200000`, *captured*). Then take the pipe apart:
   `gunzip -c` alone would print 200,000 lines to the screen (do not;
   show the first two lines and say why), `head` alone waits for input
   (Ctrl-C, one line, Chapter 7 for processes). *Then name it:* every
   program has a standard input and a standard output; `|` connects the
   output of the left program to the input of the right one; no file is
   written in between; both run at the same time. (One sentence: a pipe
   avoids an intermediate *file*, but a program in it may still use
   memory or temporary files: `sort` needs all its input before it can
   print, and spills to `TMPDIR` for big inputs, Chapter 10.) Filters (read
   stdin, write stdout) vs programs that need a file name. Build one
   pipeline step by step on the sequence lines, checking the output
   after each added step (the habit this chapter teaches):

   ```bash
   gunzip -c data/raw/SRR6357070_1.fastq.gz | awk 'NR % 4 == 2' | head -n 3
   gunzip -c data/raw/SRR6357070_1.fastq.gz | awk 'NR % 4 == 2 {print length($0)}' | sort | uniq -c
   ```

   (`  50000 101`, *captured*: every read is 101 bases.) `awk` is only
   used here as "line 2 of every 4", **which works because this file has
   exactly four lines per read** (Chapter 1; Chapter 15 for files that
   do not); it is explained in §8. One sentence: `head` stops reading
   early, so `gunzip` is stopped too; this is normal here (you will often
   see status 141 for the stopped program, e.g. *captured (Apple gzip)*:
   `PIPESTATUS` `141 0`, though it depends on the program and timing;
   Chapter 8's `pipefail`). And `gunzip -c | head` reads only the start:
   it says nothing about whether the rest of the file is intact (that is
   `gzip -t`, Chapter 1).
   [`fig-pipeline` (stepped); key idea; self-check]
3. **Redirection and the `>` trap.** *Start hands-on:* Chapter 1's
   summary line with `>` and the R2 line with `>>`, rewritten into
   `~/bioinf-computing-ch06/fastq_summary.txt`; run the `>` line twice and `cat`
   (one line), then `>>` twice (duplicated line). `<` in one line
   (`wc -l < file` prints the number without the file name, *captured*).
   *Then the trap,* on a toy file:

   ```bash
   printf 'b\na\nc\n' > ~/bioinf-computing-ch06/toy.txt
   sort ~/bioinf-computing-ch06/toy.txt > ~/bioinf-computing-ch06/toy.txt
   wc -c ~/bioinf-computing-ch06/toy.txt        # 0: the file is now empty
   ```

   (*captured*.) Why: the shell opens (and empties) the output file
   **before** `sort` starts, so `sort` reads an empty file. Same for
   `grep`, `cut`, `sed` without `-i`. Fixes: write to a new name, check
   it, then `mv` (exactly what Chapter 3's script does with
   `read_counts.tsv.tmp`: now readers can see why); `set -o noclobber`
   as a safety net, demonstrated in a throwaway subshell so it does not
   stay on and break later steps that overwrite on purpose:
   `( set -o noclobber; echo x > ~/bioinf-computing-ch06/toy.txt )`
   (*captured*: `toy.txt: cannot overwrite existing file`, exit 1; `>|`
   forces). It guards `>` only: `tee file`, `cp`, and `sed -i` still
   overwrite. Making it permanent in `.bashrc` is mentioned, not
   recommended (Chapter 7). `>` on a typo'd name silently makes a
   new file; `>` on the right name silently replaces it. Chapter 3's
   read-only `data/raw/` protects raw data from exactly this (*to
   capture*: `Permission denied` when redirecting into it). `tee`:
   save and see at once (*captured*):

   ```bash
   pixi run seqkit stats -T \
     data/raw/SRR6357070_1.fastq.gz \
     data/raw/SRR6357070_2.fastq.gz \
     | tee ~/bioinf-computing-ch06/counts.tsv \
     | cut -f1,4
   ```

   (`-T` gives tab-separated output, which `cut` needs; seqkit's default
   table is laid out for people.) `tee -a` appends. [`fig-overwrite`, `tbl-redirection`;
   pitfall callout; misconception `redirect-to-same-file`; self-check]
4. **Standard output vs standard error.** *Start hands-on:*

   ```bash
   pixi run seqkit stats -T data/raw/SRR6357070_1.fastq.gz \
     data/raw/SRR6357070_2.fastq.gz > ~/bioinf-computing-ch06/counts.tsv
   ```

   The table goes into the file, but a `processed files: 2 / 2 …
   done` line still appears on the screen (*captured*). Why? It went to
   a second stream. *Then name it:* two output streams, stdout
   (results) and stderr (messages, progress, warnings, errors), both
   shown on the terminal by default, so they look the same until you
   redirect. `2>` sends stderr to a file, `2>&1` sends it where stdout
   goes (order matters: `> file 2>&1`, not `2>&1 > file`), `&>` is
   bash's shorthand, `/dev/null` discards. "Results on stdout, messages
   on stderr" is a **convention** tools follow, not something the shell
   checks: redirection moves bytes from a stream, it does not sort text
   by meaning, and some tools mix the two or write their own log files.
   Return to Chapter 4's
   truncated file (`head -c 1000000 … > ~/bioinf-computing-ch06/broken.fastq.gz`):
   `pixi run seqkit stats -T ~/bioinf-computing-ch06/broken.fastq.gz
   > ~/bioinf-computing-ch06/out.tsv 2> ~/bioinf-computing-ch06/err.txt`
   puts the header in `out.tsv` and the `[ERRO] … unexpected EOF` in
   `err.txt` (*captured*; `err.txt` keeps ANSI
   colour codes, shown with `cat -A` as `^[[31m`: say once that colour
   codes can end up in logs). *Why it matters:* a results file that
   contains error messages breaks the next tool; a log that lost the
   errors is useless (Chapter 3's script keeps both in `logs/`, Chapter
   4's "find the log"). *Then the pipe only carries stdout:*

   ```bash
   gunzip -c ~/bioinf-computing-ch06/broken.fastq.gz | wc -l
   ```

   prints `gzip: …broken.fastq.gz: unexpected end of file` **and**
   `89515` (*captured (GNU gzip 1.15)*: `PIPESTATUS` `1 0`; Apple gzip
   gave two error lines and `89253`: the partial output differs between
   implementations, so the chapter labels the number with its gzip
   version). The lesson, in these words: decompression failed after
   producing partial text; `wc` successfully counted the text it
   received; that count is incomplete and cannot be used as a read
   count. `$?` is `0` because it is `wc`'s status. (Do not teach "not a
   multiple of 4" as the test for damage: another cut could land on a
   multiple of 4 and still be wrong.) Ties to `no-error-means-correct`;
   `set -o pipefail` (Chapter 8) catches a stage that *reports* failure,
   but not a tool that reports success despite an error (Chapter 4's
   seqkit exit 0), which is why Chapter 4's result checks still
   matter.
   Never discard stderr with `2>/dev/null` just to make a screen look
   clean: only for messages you have read and know you do not need
   (seqkit's progress line is the example). [`fig-streams`,
   `tbl-redirection`; key idea; misconceptions `errors-go-to-file`,
   `pipe-stops-on-error`; self-check]
5. **Counting and summarising: `wc`, `cut`, `sort`, `uniq`.** *Start
   hands-on with a warm-up on Chapter 5's practice table*
   (`~/bioinf-computing-ch05/share/meta/samples.tsv`: tab-separated,
   columns `sample`, `run_folder`, `condition`, `reads`, a header and 6
   unsorted rows, one sample listed twice; decided 2026-11-17). A short
   block recreates the file in `~/bioinf-computing-ch06/` for readers
   who skipped Chapter 5 (same `printf` lines as Chapter 5's paste
   block, so both stay byte-identical). Rows final in the Chapter 5
   plan (2026-11-17):

   ```bash
   rows=(sample run_folder condition reads
     sample_C "Run 3 final" treated 12
     sample_A run1 control 9
     sample_B run2 control 30
     sample_E run5 treated 105
     sample_B run2 control 30
     sample_D run4 control 8)
   printf '%s\t%s\t%s\t%s\n' "${rows[@]}" > ~/bioinf-computing-ch06/samples.tsv
   ```

   (MD5 `971d8f742cb76a8d181d3bdc3dcbceaa`, *captured*: readers who
   have Chapter 5's file can compare. The array and `printf` are shown,
   not taught: Chapter 8.) Small enough to check by eye; all *captured*:
   - `cat` it and find the duplicate by eye (`sample_B`, rows 3 and 5);
     `wc -l` → 7.
   - **`uniq` only merges neighbours.** `cut -f1 … | uniq -c` lists
     `sample_B` twice with count 1; `cut -f1 … | sort | uniq -c` shows
     `2 sample_B`. The habit: sort first, so equal values are counted
     wherever they sit in the file (`uniq` alone is right only when you
     want runs of neighbouring lines, which is rare at this stage).
     `uniq -d` lists only `sample_B`.
   - `cut -f3 | sort | uniq -c` → `1 condition`, `4 control`,
     `2 treated`: the header was counted; fix with `tail -n +2`.
   - `grep -w treated` → the `sample_C` and `sample_E` rows.
   - The `reads` column sorts as `105 12 30 30 8 9` as text and
     `8 9 12 30 30 105` with `sort -t$'\t' -k4,4n` (`$'\t'` in one line:
     how to type a tab for `-t`). This is the first meeting with
     `sort-is-numeric`; the GTF start positions below repeat it.
   - The duplicate matters: the `reads` total is 194 with it and 164
     without (header removed with `tail -n +2` **before** `sort -u`, so
     the header can never be sorted into the data), the sum §8 computes
     with awk. Duplicated metadata rows inflate totals silently. `sort -u`
     removes only rows identical in every column; two rows with the same
     sample label and different values are a conflict to resolve, not a
     duplicate to drop (Chapter 14).
   - Two samples, `sample_D` and `sample_E`, have no read files in the
     practice folder (Chapter 5's design): one sentence that a sample
     table and the files on disk can disagree, checked properly in
     Chapter 14.

   *Then the real sample sheet* (Chapter 3's promise):

   ```bash
   cut -d, -f1 data/meta/samplesheet_upstream.csv | sort | uniq -c
   ```

   (*captured*: 5 labels, `WT_REP1` and `RAP1_UNINDUCED_REP2` twice,
   and `sample` once: the header again, fixed with `tail -n +2`.) Here
   the duplicate labels already sit next to each other, so `uniq` alone
   would happen to be right: the warm-up is why readers sort anyway.
   Then strandedness: `tail -n +2 … | cut -d, -f4 | sort | uniq -c` →
   `2 auto`, `5 reverse` (*captured*). One more discovery:
   - **Sort order depends on the locale.** In `en_US.UTF-8`, the header
     `sample` sorts between `RAP1_…` and `WT_…`; with `LC_ALL=C sort`,
     after all upper-case names (*captured*). Counts are the same, the
     order is not. Use `LC_ALL=C` when the order must be reproducible
     or another tool needs it (`join`, `comm`; one sentence). Check on
     WSL and a cluster what the default locale is.

   *Then the annotation* (`data/ref/genes.gtf.gz`, through the link):
   `cut -f3 | sort | uniq -c | sort -k1,1nr` (the chapter check). No
   `gene` lines: this test GTF has transcripts, exons, CDS, start and
   stop codons only, 600 lines, no comment lines (*captured*). Then
   `cut -f1 | sort | uniq -c` → `599 I` and `1 not_in_genome`
   (*captured*): one CDS line sits on a sequence name that is not in
   the genome (`genome.fa.gz` has only `>I`, *captured*). Two minutes of
   counting found something a reader would otherwise meet as a pipeline
   error. nf-core put it there on purpose, to test that the pipeline
   copes with it (commit `1b17b24`, 2019-08-30, "Add gtf line using
   chromosome not in genome"; *checked* 2026-11-17): real annotations
   and genomes do not always match either (Chapter 15). *Then name the tools* in a table: `wc` (`-l`, `-c`),
   `cut` (`-f`, `-d`, tab is the default delimiter: why TSV is easy and
   CSV with quoted commas is not, Chapter 14), `sort` (`-n`, `-k`, `-t`,
   `-r`, `-u`), `uniq` (`-c`, `-d`). Numeric vs text sort on twelve
   transcript start positions: `sort` puts `10091` before `1807` and
   `335` near the end; `sort -n` gives `335 538 1807 …` (*captured*).
   `sort -k1,1nr` explained piece by piece. Duplicated reads as a
   counting example: 21,662 distinct sequences among 50,000 reads; the
   most common appears 208 times (*captured*); what that means is QC
   (Genomics/Transcriptomics books), not this chapter.
   [`tbl-text-tools`; tip: `LC_ALL=C`; misconceptions
   `uniq-finds-all-duplicates`, `sort-is-numeric`; self-check]
6. **Finding lines: `grep`.** *Start hands-on:* count read headers in
   both mates: `gunzip -c … | grep -c '^@SRR'` → `50000` and `50000`
   (*captured*). Then the adapter from Chapter 4's methods excerpt:
   `grep -c AGATCGGAAGAGC` on the sequence lines → 1,916 (R1) and
   1,910 (R2) reads contain this **exact motif** (*captured*): the
   sequence the paper gave cutadapt. Not an estimate of adapter
   contamination (partial adapters and mismatches are missed) and not
   proof of why the authors trimmed; that belongs to the applied books.
   `grep -c` counts matching **lines**, not occurrences and not
   records. Then a gene in the annotation: `grep -w 'gene_name "CDC19"'`
   shows its five lines (*captured*: transcript and exon 71786–73288 on
   `+`). *Then the trap:* would `grep -c '^@'` also count reads? Here,
   yes (50,000, *captured*), but only because this file's quality
   characters are `# / 7 < B F` (binned qualities, *captured*). `@` is
   a valid quality character (Phred 31, Chapter 15), so in other files a
   quality line can start with `@`: shown on a supplied 2-read toy
   FASTQ where `grep -c '^@'` says 3. Better for **this four-line
   file**: `awk 'NR % 4 == 1'` (position, not content); but that also
   assumes four lines per record and validates nothing. The general
   recipe is a format-aware tool (`pixi run seqkit stats`). Same lesson
   as Chapter 1: true for this file is not true for FASTQ.
   *Then the flags* (table): `-c`, `-v`, `-i`, `-w`, `-n`, `-o`, `-A`/
   `-B`/`-C` (show a read's full record: `grep -A 3 '^@SRR6357070\.6710070 '`,
   with the dot escaped, since this chapter teaches that `.` matches
   anything, *captured*), `-F` (fixed string), `-E`, `-f file` (one line;
   used for ID lists later), `-r` (one line). Exit status: `1` when
   nothing matches (*captured*: `grep -c ZZZZ` prints `0`, exit 1),
   which matters inside scripts (Chapter 8). `zgrep` reads `.gz`
   directly (one line). [`tbl-grep-flags`; pitfall callout;
   misconception `grep-at-counts-reads`; self-check]
7. **Regular expressions.** *Start hands-on:* `grep -c GAATTC` (an
   EcoRI site) → 2,818 lines; `grep -c 'GA.TTC'` → 11,404 (*captured*):
   the `.` matched any letter. Then the sample sheet: `grep -o
   'SRR[0-9]*_1' … | sed 's/_1$//'` lists the 7 run IDs, and `grep -Eo
   'SRR[0-9]+_[12]\.fastq\.gz' … | wc -l` → 11 file names (4 paired ×
   2 + 3 single-end = 11, *captured*). *Then name the parts* with the
   regex-anatomy figure: literal characters, `.`, `[ ]` and `[^ ]`,
   `*`, `+` and `?` (`-E`), `{n,m}`, `^` and `$`, `\` to make `.` a
   literal, `( )` and `|` with `-E`. Basic (`grep`, `sed`) vs extended
   (`grep -E`, `sed -E`, `awk`) syntax in two rows; `-P` (Perl) exists
   in GNU grep, one line. Always single-quote a regex so bash does not
   expand it. *Then globs vs regexes* (Chapter 5's promise): `*.fastq.gz`
   in `ls` means "any name ending in .fastq.gz"; in `grep` the same
   characters mean something else (`*` = "zero or more of the previous
   character"). Table side by side. *Then the cross-language point:*
   simple regexes like this one work the same in R (`grepl("^SRR[0-9]+",
   x)`; base R uses extended syntax by default) and Python
   (`re.search(r"^SRR[0-9]+", s)`). They are separate engines, not one
   universal regex: base R, stringr (ICU), Python's `re`, JavaScript
   (the tester below) and GNU grep differ in details (escaping
   backslashes in R strings, raw strings in Python, which alternative
   wins in `a|ab`); Chapters 12–13 use them. One warning: regexes for structured
   formats get fragile fast (quoted CSV, nested GTF attributes). [`fig-regex-anatomy`,
   `fig-regex-tester` (Observable JS),
   `tbl-glob-vs-regex`, `tbl-regex-basics`; misconception
   `glob-is-regex`; self-check]
8. **Editing streams with `sed`, computing with `awk`.**
   *`sed` first, hands-on:* `sed 's/^chr//'` on a 2-line toy BED
   (`chr1` → `1`, *captured*), the chromosome-naming fix Chapter 15
   discusses; the file itself is unchanged (`cat`, *captured*). File
   names from the sample sheet URLs: `cut -d, -f2 | sed 's|.*/||'`
   (*captured*; another delimiter avoids escaping `/`). Core sed stops
   at substitution. FASTQ to FASTA moves to an optional worked contrast
   (collapsed box): `sed -n '1~4s/^@/>/p;2~4p'` on two records
   (*captured*; `1~4` is GNU-only, and it assumes four lines per
   record), beside the recipe readers should actually use,
   `pixi run seqkit fq2fa`.
   `sed -i` edits in place: one paragraph, with the rule "never on
   `data/raw/`, and test without `-i` first"; GNU vs BSD `-i` in
   Chapter 7. *`awk` next, hands-on, starting with a mistake:* on §5's
   practice table, `awk '{print $3}'` prints `3` for `sample_C`
   instead of `treated`, because awk splits on spaces by default and
   the run folder is `Run 3 final`; `awk -F'\t' '{print $3}'` is right
   (both *captured*). Same file, then `awk -F'\t' 'NR > 1 {s += $4}
   END {print s}'` → 194, and 164 after `sort -u` (§5's duplicate).
   Then fields and records on a GTF line
   (figure: `$1 … $9`, `-F'\t'` because attribute column 9 contains
   spaces too); `awk -F'\t' '$3 == "transcript"' | cut -f7 | sort | uniq -c`
   → `64 +`, `60 -` (*captured*; transcript **lines**, so one per
   transcript in this file, not a gene count). An optional extension,
   shown not taught: the three longest transcript **spans** with their
   gene IDs, `end − start + 1` (YAR050W 4,614 bp, *captured*; the
   `match()` one-liner is supplied). A span on the genome is not the
   spliced transcript length; coordinates are Chapter 17. Sum a column: `awk -F'\t' 'NR > 1
   {s += $4} END {print s}' ~/bioinf-computing-ch06/counts.tsv` → `100000`
   (*captured*), then the meaning check from Chapter 4: two mate files,
   so 50,000 read pairs. Two tools agree: N bases counted with awk,
   `awk 'NR % 4 == 2 {n += gsub(/N/, "")} END {print n}'` → 280 (R1)
   and 18,842 (R2), the same as seqkit's `sum_n` in Chapter 4 and the
   number of `#` quality characters (*captured*): an independent check
   is how you trust a one-liner. *Then name it:* `pattern {action}`,
   `NR`, `NF`, `$0`, `BEGIN`/`END`, `-F`, `-v OFS='\t'`. When a
   one-liner grows past one line, it belongs in R or Python (Chapters
   12–13) or a script (Chapter 8). [`fig-awk-fields`, `tbl-awk-basics`;
   tip; self-check]
9. **Compressed files.** *Start hands-on:* recall `gunzip -c`; write a
   compressed subset of the first 100 reads, `gunzip -c … | head -n 400
   | gzip > ~/bioinf-computing-ch06/small_R1.fastq.gz` (400 lines = 100
   reads only in a four-line file; `pixi run seqkit head -n 100` is the
   general recipe, Chapter 4), and check it (`gunzip -c … | wc -l` →
   400, *captured*). Compress a stream: 50,000 sequence lines
   `| gzip -c > ~/bioinf-computing-ch06/seqs.txt.gz` → 854,368 bytes
   (*captured*), vs 5.05 Mbases uncompressed. *Then name the family:* `gzip`, `gunzip`,
   `gunzip -c` = `zcat` (GNU), `zless` (Chapter 5), `zgrep`, `gzip -t`
   (Chapter 1). Why the book still writes `gunzip -c`: macOS's own
   `zcat` fails on `.gz` (*captured (Apple gzip)*: `zcat: can't stat:
   SRR6357070_1.fastq.gz (SRR6357070_1.fastq.gz.Z)`); on Linux and
   after Chapter 1's Homebrew `gzip`, `zcat` works the same (**check**
   that Homebrew's `gzip` puts `zcat` ahead of `/usr/bin/zcat`). Rules:
   do not decompress big files to disk, stream them; many tools read
   `.gz` directly (seqkit, and most aligners), so a decompressed copy is
   rarely needed; `bgzip` is a gzip variant that allows indexing
   (Chapter 17). Reading a 10 GB FASTQ through a pipe is real work:
   on a cluster, not on the login node (Chapter 10). `pigz` (parallel
   gzip) in one line, Chapter 35. [`tbl-compression`; pitfall:
   decompressing to disk; self-check]
10. **Text tools vs format-aware tools.** Short. *Start with a table*
    of tasks readers just did and the format-aware equivalent: count
    reads (`awk`/`wc -l / 4` vs `seqkit stats`), FASTQ→FASTA (`sed` vs
    `seqkit fq2fa`), first N reads (`head -n 400` vs `seqkit head -n
    100`), filter a GTF by feature (`awk` on column 3 is fine for this
    simple test; for real annotation work, an annotation package such as
    Bioconductor's rtracklayer/GenomicFeatures or a GTF-aware Python
    library, Chapter 17; bedtools works on intervals, not as a GTF
    feature filter), count alignments (vs `samtools view -c`,
    Chapter 16). Why the format-aware tool wins once files are real:
    multi-line FASTA/FASTQ (every `NR % 4`, `head -n 400` and `1~4`
    trick in this chapter assumed four lines per record), headers,
    quoting, binary formats (BAM), compression variants, and the
    `@`-quality trap. Text tools stay
    the best way to *look* and to check a result quickly; Part IV's
    opening principle says the same. [`tbl-text-vs-format`; key idea]
11. **Summary, exercises, further reading.** Summary as 5 bullets that
    mirror the learning goals; exercises (below); annotated further
    reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2,
corrected after the Codex review): data flowing through pipes and
results on stdout `given` (blue: our data and its re-organisations);
routine stderr (progress lines, messages) neutral (`muted`); `warn`
(vermillion) **only** for the pitfalls shown: the overwrite in
`fig-overwrite` and the decompression error in `fig-streams`; `good`
(green) only for a check (the safe `mv` route, the `cmp` check);
programs and shell neutral (`ink`, `line`).

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-pipeline` | 2 | stepped (5 steps) | `gunzip -c → awk 'NR%4==2' → awk length → sort → uniq -c`, on a toy of 3 reads (12 lines, two lengths) so every line fits: at each step, the box for the new program and the data that leaves it (12 lines → 3 sequences → 3 numbers → sorted → counted). One sentence per step. Ends with the real result `50000 101`. |
| `fig-streams` | 4 | static | A program as a box with one input (stdin, left) and two outputs (stdout `given`, stderr `muted`; the gzip error in
panel 3 is the one `warn` mark). Three panels: default (both to the terminal); `> file` (stdout to file, stderr still on screen, the seqkit progress line); `cmd1 \| cmd2` (only stdout enters the pipe; stderr goes around to the screen, the truncated-gzip case). |
| `fig-overwrite` | 3 | static (two frames) | `sort toy.txt > toy.txt`: frame 1, the shell opens `toy.txt` for writing and empties it (`warn`) *before* `sort` starts; frame 2, `sort` reads an empty file and writes nothing. Beside it, the safe version: `> toy.sorted.txt`, check, `mv`. |
| `fig-regex-anatomy` | 7 | static | `SRR[0-9]+_[12]\.fastq\.gz` with each piece labelled (literal, class, one-or-more, escaped dot), and three sample-sheet strings marked match / no match (`SRR6357070_1.fastq.gz` ✓, `SRR6357070_3.fastq.gz` ✗, `SRR6357070_1.fastqXgz` ✗ only because of `\.`). |
| `fig-awk-fields` | 8 | static | One real GTF line (the CDC19 transcript) split into `$1`…`$9` with tab marks, column names below (seqname, source, feature, start, end, score, strand, frame, attributes), and why `-F'\t'` matters: column 9 has spaces. Reused in Chapter 17. |

Not used here: Mermaid, screenshots.

### Interactive figure (Observable JS)

- **Decided (2026-11-17): build it.** A regex tester on 8 fixed lines (sample-sheet rows and
  FASTQ lines): the reader types a pattern and matching lines and the
  matched part are highlighted. Lesson in words: "change one character,
  see what matches". Labelled as using **JavaScript** regexes: similar
  to `grep -E` on the surface, but not guaranteed to match or highlight
  the same text (*captured*: GNU `grep -Eo 'a|ab'` on `ab` prints `ab`;
  JavaScript's `/a|ab/` picks `a`, per the ECMAScript spec). So: the
  supplied example patterns are a shared subset, each checked against
  GNU grep 3.12 with the same result; no JavaScript-only constructs;
  each line tested on its own, with `^`/`$` as line boundaries; an
  invalid pattern shows a message instead of breaking the figure. A
  short fixed prediction/result table beside it keeps the lesson when
  the figure does not load. Label `fig-regex-tester`, in §7 after
  `fig-regex-anatomy`.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-redirection` | 3–4 | Operator (`\|`, `>`, `>>`, `<`, `2>`, `2>&1`, `&>`, `>\|`, `tee`, `/dev/null`) · what it does · example on the book's files · danger |
| `tbl-text-tools` | 5 | Tool · what it does · flags used in this chapter · example (`wc`, `cut`, `sort`, `uniq`, `head`/`tail -n +2`, `paste`, `tr`, `column -t`) |
| `tbl-grep-flags` | 6 | Flag · meaning · example · output on the book's files |
| `tbl-glob-vs-regex` | 7 | Characters · in a glob (`ls`, `find -name`) · in a regex (`grep`, `sed`, R, Python) · example |
| `tbl-regex-basics` | 7 | Piece · meaning · basic (`grep`, `sed`) · extended (`grep -E`, `awk`, R, Python) · example |
| `tbl-awk-basics` | 8 | Piece (`$1`, `$0`, `NF`, `NR`, `-F`, `pattern {action}`, `BEGIN`/`END`, `OFS`) · meaning · example |
| `tbl-compression` | 9 | Task · command · note (`gzip -t`, `gunzip -c`/`zcat`, `zless`, `zgrep`, `\| gzip >`, `bgzip`, `pigz`) |
| `tbl-text-vs-format` | 10 | Task · text-tool way · format-aware tool · where text tools break |

### Code (§6)

- `filename="Terminal (laptop)"`, tier 2 (shown, not run at render);
  every step takes under a second on the test files. Cluster readers:
  the same commands work on a login node for files this small; one
  sentence in §9 that full-size files go to a compute node (Chapter 10).
- Every new command gets code annotations the first time; captured
  output in `.console` blocks. seqkit's progress line contains ANSI
  cursor codes (`ESC[1A ESC[J`): strip them from captures and say once
  that it is a progress line on stderr.
- Long pipelines broken with `\` at a `|`, one step per line, so the
  step-by-step build in §2 is visible.
- Version-dependent captures labelled (GNU grep 3.12, gawk 5.4.1,
  seqkit 2.14.0, GNU gzip 1.15). Truncated-file case recaptured with
  GNU gzip 1.15; **recapture on Linux/WSL** before drafting, and the
  §2 `PIPESTATUS` with GNU gzip.
- Locale: captures use `en_US.UTF-8`; state the locale where sort order
  is shown, and show the `LC_ALL=C` version beside it.
- macOS: after Chapter 1's setup, `grep`, `sed`, `awk`, `sort` are GNU
  (`sed --version` check from Chapter 1); the `1~4` address and `-P`
  need GNU. No BSD variants written (series rule: bash with GNU tools).
- Supplied toy files are created with `printf` in the chapter (no
  download): `toy.txt`, the 2-line BED, the 2-read FASTQ with a quality
  line starting with `@`, and for exercise 6 a 1-read FASTQ holding only
  the reverse complement of the adapter (`GCTCTTCCGATCT`).
- After the §5 recreate block, every command on the practice table uses
  the Chapter 6 copy, `~/bioinf-computing-ch06/samples.tsv`, so readers
  track one path.

### Plots

None. (The read-length and feature-count results are single numbers or
five rows; a table says it.)

### Animation (manim)

None. `fig-pipeline` is a stepped SVG.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | A pipe joins one program's output to the next one's input; build pipelines one step at a time and look at the output after each step |
| 3 | Pitfall | `cmd file > file` empties `file` before `cmd` reads it. Write to a new name, check, then `mv` |
| 3 | Misconception | "`sort data.txt > data.txt` sorts the file in place" (`redirect-to-same-file`) |
| 4 | Key idea | By convention results go to stdout and messages to stderr; `>` and `\|` carry only stdout, so errors still reach the screen, and a pipeline can "succeed" on broken input |
| 5 | Tip | Sort before `uniq -c`, so equal values are counted wherever they are; `LC_ALL=C sort` when order must be reproducible |
| 6 | Pitfall | `grep -c '^@'` is not a read count: `@` is also a quality character. Count by position in a four-line file, or with `seqkit stats` in general |
| 8 | Tip | Check a one-liner against an independent count (awk's N count = seqkit's `sum_n`) before trusting it |
| 10 | Key idea | Text tools to look and check; format-aware tools to process |

`pipe-stops-on-error`, `errors-go-to-file`, `uniq-finds-all-duplicates`,
`sort-is-numeric`, `glob-is-regex` are handled in the text and
self-checks, to stay under three callouts per screen.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: `gunzip -c reads.fastq.gz | head -n 4 | wc -l` prints what?
  (*4: `wc` only sees the four lines `head` passed on.*)
- §3: You run `grep -v '^#' notes.txt > notes.txt`. What is in
  `notes.txt` now? (*Nothing: the shell emptied it before `grep` ran.*)
- §4: A command prints a table and some warnings. You want the table in
  `out.tsv` and the warnings in `run.log`. Write the redirection.
  (*`cmd > out.tsv 2> run.log`.*)
- §5: `cut -d, -f1 samplesheet_upstream.csv | uniq -c` gives the right
  counts, but the same command on the practice `samples.tsv` (with
  `cut -f1`) does not. Why? (*In the sample sheet the duplicates are on
  neighbouring lines; in the practice table they are not, and `uniq`
  only merges neighbours. Sort first.*)
- §6: `grep -c 'CTG'` on the uncompressed R1 file gives 35,761. Is that
  the number of reads containing CTG? (*Only because quality lines here
  contain no `C`, `T`, `G`; in general count sequence lines only:
  `awk 'NR % 4 == 2' | grep -c CTG`; both give 35,761 here,
  *captured*.*)
- §7: Does `grep 'fastq.gz'` match `fastqXgz`? (*Yes: `.` is any
  character; use `'fastq\.gz'` or `grep -F`.*)
- §8: What does `awk -F'\t' '$7 == "-"' genes.gtf | wc -l` count?
  (*Lines on the minus strand, of every feature type, not genes.*)
- §9: Why stream a 10 GB `.fastq.gz` with `gunzip -c … |` instead of
  `gunzip file.fastq.gz` first? (*No 40+ GB uncompressed copy on disk
  or quota; one read pass.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
commands; outputs go to `~/bioinf-computing-ch06/`):

1. **Build a pipeline step by step.** Starting from the supplied first
   step `gunzip -c data/raw/SRR6357070_2.fastq.gz`, add one step at a
   time to report the distribution of read lengths in R2, checking the
   output after each step. Record the final command and result in
   `NOTEBOOK.md`. (*`50000 101`, the same as R1.*)
2. **Fix the redirections.** A supplied 4-line snippet (counts to the
   screen, errors in a results file, an overwrite of its own input, an
   append that should be an overwrite) is run on a copy of
   `counts.tsv`. Fix each line so results go to files, messages to a
   log, and no input is overwritten. (*Answer key: each line, its
   problem, the fix.*)
3. **Do the mates match?** Run the supplied commands from the chapter
   check (part 2): write the first header field of every R1 and R2
   record to `ids_R1.txt` and `ids_R2.txt`, count the lines, compare
   with `cmp`. Then make a copy of `ids_R2.txt` with line 3 changed
   (supplied `sed` command) and compare again. (*50,000 lines each;
   `cmp` silent, exit 0; the altered copy: `differ: char 54, line 3`,
   exit 1. Why count: `cmp` is also silent on two empty files. Why it
   matters: aligners pair reads by position, Chapter 15.*)
4. **Summarise the annotation.** Required, with `cut`, `sort`,
   `uniq -c`, and `awk -F'\t'` on `data/ref/genes.gtf.gz` and the
   labelled nine-column line from `fig-awk-fields`: feature types (the
   chapter check), sequence names, transcript lines per strand (64 `+`,
   60 `-`). Which line is on a sequence that is not in the genome?
   (*Line 1, `not_in_genome`.*) **Extension** (optional; the attribute
   commands are supplied, since quoted GTF attributes are Chapter 17):
   distinct gene IDs (124) and gene biotypes on transcript lines (116
   protein_coding, 4 tRNA, 2 pseudogene, 1 ncRNA, 1 snoRNA); all
   *captured*.
5. **Regex practice on the sample sheet.** Write one `grep -E` that
   matches only the R2 file names, and count them. (*4: the
   paired-end runs.*) Then one `awk -F,` that prints the sample labels
   of single-end rows (empty `fastq_2`; *captured*:
   `RAP1_UNINDUCED_REP1` and `RAP1_UNINDUCED_REP2` twice).
6. **Check with a second tool.** Count the reads in R1 containing the
   exact motif `AGATCGGAAGAGC` with `grep -c` on the sequence lines
   only, then with `pixi run seqkit grep -s -P -p AGATCGGAAGAGC … |
   pixi run seqkit stats -T` (`-s` sequence, `-P` positive strand only;
   or count directly with seqkit's `-C`, not grep's `-c`). Do the
   numbers agree? (*Yes: 1,916 both ways, *captured*, seqkit 2.14.0.*)
   Then run both on the supplied 1-read toy file that holds only the
   reverse complement `GCTCTTCCGATCT`, once with and once without `-P`.
   (*grep 0, seqkit `-P` 0, seqkit default 1, *captured*: by default
   seqkit searches both strands. On the real files both settings give
   1,916 and 1,910, *captured*, so only the toy shows the difference.*)

## Examples and data

- Running dataset (all already in the project from Chapter 3; nothing
  new to download, so **no new rows in `data/README.md`**):
  `data/raw/SRR6357070_1.fastq.gz` and `_2` (50,000 reads each, 101 bp),
  `data/ref/genes.gtf.gz` (600 lines, 124 genes, yeast chromosome I
  plus one `not_in_genome` line), `data/ref/genome.fa.gz` (one
  sequence `>I`, 230,218 bases in 60-character lines, *captured*),
  `data/meta/samplesheet_upstream.csv` (7 runs, header `sample,fastq_1,
  fastq_2,strandedness`).
- Toy files written in the chapter: `toy.txt`, a 2-line BED, a 2-read
  FASTQ with a quality line starting with `@`, `broken.fastq.gz`
  (Chapter 4's truncated copy, `head -c 1000000`).
- Chapter 5's practice table `~/bioinf-computing-ch05/share/meta/samples.tsv`
  (read only; fixed layout per the Chapter 5 plan), or its copy made by
  §5's recreate block in `~/bioinf-computing-ch06/samples.tsv`.
- Captured outputs (2026-11-17; versions in the status line): `200000`
  lines; read lengths `50000 101`; `grep -c '^@SRR'` 50,000 in both
  mates; quality characters in R1 `/ # < 7 B F` only (R2 the same set);
  N bases 280 (R1), 18,842 (R2), equal to the `#` counts; reads with
  ≥1 N 63 (R1), 295 (R2); adapter `AGATCGGAAGAGC` in 1,916 (R1) and
  1,910 (R2) reads; `GAATTC` 2,818 lines, `GA.TTC` 11,404; 21,662
  distinct sequences in R1, top one 208 copies; GC fraction of R1 0.402
  (not used unless a section needs it); GTF feature counts (check);
  `599 I` / `1 not_in_genome`; transcripts `64 +` / `60 -`; biotypes
  as in exercise 4; longest transcript YAR050W 4,614 bp; sample-sheet
  label counts in both locales; strandedness `2 auto` / `5 reverse`;
  7 run IDs and 11 file names by regex; `sort toy.txt > toy.txt` → 0
  bytes; noclobber message; seqkit progress line on stderr with
  `> counts.tsv`; truncated file: `[ERRO]` on stderr, header on stdout;
  `gunzip -c broken | wc -l` → error + `89515`, `PIPESTATUS 1 0` (GNU
  gzip 1.15; Apple gzip: `89253`); `head` pipeline `PIPESTATUS 141 0`
  (Apple gzip); `grep` no match → `0`, exit 1; awk sum of `num_seqs`
  100,000; first-field mate IDs: 50,000 each, identical in order, first
  `@SRR6357070.25017281`; `cmp` on two empty files exit 0; altered copy
  `differ: char 54, line 3`, exit 1; stripping `/1$` from whole headers
  does nothing (the marker is mid-header); seqkit `grep -s` with and
  without `-P`: 1,916 (R1), 1,910 (R2) both ways; reverse-complement toy:
  default 1, `-P` 0, grep 0; GNU `grep -Eo 'a|ab'` on `ab` → `ab`;
  `sed 's/^chr//'`, basename, and FASTQ→FASTA outputs.
- **Side finding for Chapter 4 (*captured*, seqkit 2.14.0):** `seqkit
  stats -T good.fastq.gz broken.fastq.gz` prints **only the header**
  on stdout: the good file's row is lost too, and the exit status is
  still 0. Added to Chapter 4 (see *Decisions*). Narrowed while
  drafting the upstream issue (*captured*): with `-j 1` the good row
  is printed, so it is a multi-threading problem; without `-T` nothing
  is printed; `seqkit seq` on the same file exits 255, so only `stats`
  exits 0. Issue text drafted for Austin to post (not posted).
- Where commands run: laptop (or login node for these small files).

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters), to add when this plan is agreed. None of these ids
exist yet (checked 2026-11-17). Where each is handled is in brackets.

- `redirect-to-same-file`: "`sort data.txt > data.txt` sorts the file
  in place." The shell empties `data.txt` before `sort` starts, so the
  result is an empty file. Write to a new file, check, then `mv`.
  Probe: what is in `toy.txt` after `sort toy.txt > toy.txt`? (Nothing:
  0 bytes.) [callout, §3; `fig-overwrite`; self-check]
- `errors-go-to-file`: "`> file` saves everything the command prints."
  It saves standard output only; messages on standard error still go
  to the screen and are not in the file. Probe: after `seqkit stats …
  > counts.tsv`, why is a progress line still on screen? [text, §4;
  `fig-streams`]
- `pipe-stops-on-error`: "If one command in a pipeline fails, the
  pipeline fails." By default the pipeline's status is the last
  command's, and the later commands keep working on whatever they got.
  Probe: `gunzip -c broken.fastq.gz | wc -l` prints an error and a
  number (`89515` with GNU gzip 1.15); what does `echo $?` say? (`0`.)
  Is the number a read count? (No: partial output.) [text, §4; self-check;
  Chapter 8 for `pipefail`]
- `uniq-finds-all-duplicates`: "`uniq` removes or counts all duplicate
  lines." It only merges identical neighbouring lines; sort first.
  Probe: `cut -f1 samples.tsv | uniq -c` on Chapter 5's practice
  table misses its duplicated sample. [text, §5; self-check]
- `sort-is-numeric`: "`sort` puts numbers in numeric order." By default
  it compares text character by character, so `10091` sorts before
  `1807`; use `sort -n` (and `-k` for a column). [text, §5]
- `grep-at-counts-reads`: "`grep -c '^@'` counts the reads in a FASTQ
  file." `@` is also a quality character, so quality lines can start
  with it; it happened to work on the book's file. Count by position or
  with seqkit. Probe: the 2-read toy file gives 3. [callout, §6]
- `glob-is-regex`: "`*` means the same in `grep` as in `ls`." In a glob
  `*` is "any characters"; in a regex it is "zero or more of the
  previous character", and `.` is "any character". [table and text, §7;
  self-check]

## Links to other chapters and books

- Builds on: Chapter 1 (the pipes and redirections used there),
  Chapter 3 (project files, the `.tmp` then `mv` pattern, logs),
  Chapter 4 (stderr, exit status, the truncated file, the adapter,
  seqkit's `sum_n`), Chapter 5 (paths, globs, quoting, `less`, `head`,
  `tail`, `zless`).
- Leads to: Chapter 7 (`cat -A` and line endings, GNU vs BSD `sed -i`,
  processes and Ctrl-C, `PATH`); Chapter 8 (`set -o pipefail`, exit
  status 141 from `head`, `grep`'s exit 1 in scripts, logging stdout
  and stderr, variables in pipelines, loops over files); Chapter 10
  (where to run heavy pipelines, `slurm-*.out` holding both streams,
  `find … | wc -l` for inode counts); Chapters 12–13 (the same regexes
  in R and Python; when a one-liner should become R or Python); Chapter
  14 (CSV with quoted commas defeats `cut -d,`; joining tables);
  Chapter 15 (Phred `@` = 31, multi-line FASTQ, `chr1` vs `1`, mate
  order); Chapter 16 (`samtools view | …`); Chapter 17 (GTF columns,
  `bgzip`, bedtools); Chapter 35 (GNU parallel, `pigz`); Genomics and
  Transcriptomics books (duplication and adapter content as QC).

## Official links to include

- GNU Bash manual: *Pipelines* and *Redirections*
  (gnu.org/software/bash/manual)
- GNU coreutils manual: `sort`, `uniq`, `cut`, `wc`, `tee`, `head`,
  `tail`, `paste`, `tr` (gnu.org/software/coreutils/manual)
- GNU grep manual (gnu.org/software/grep/manual), GNU sed manual
  (gnu.org/software/sed/manual), GNU Awk user's guide
  (gnu.org/software/gawk/manual), GNU gzip manual
  (gnu.org/software/gzip/manual)
- POSIX regular expressions: The Open Group Base Specifications,
  chapter 9 *Regular Expressions* (pubs.opengroup.org)
- SeqKit docs (bioinf.shenwei.me/seqkit): `stats`, `fq2fa`, `grep`,
  `head`
- Software Carpentry, *The Unix Shell*: "Pipes and Filters" and
  "Finding Things" episodes (swcarpentry.github.io/shell-novice)
- R `regex` help page and Python `re` module docs, one line each, for
  §7's cross-language note

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Books have no DOI
to verify with scite; check editions and fetch metadata from the
publisher before adding to `references.bib`.

- Shotts, *The Linux Command Line* (recurring anchor; 2nd ed., No
  Starch Press 2019, also free online): chapters on redirection,
  regular expressions, and text processing. Main pick.
- Software Carpentry, *The Unix Shell* (recurring anchor): "Pipes and
  Filters" as a second walk-through with exercises.
- Buffalo 2015, *Bioinformatics Data Skills* (O'Reilly), chapter 7
  "Unix Data Tools": the closest match in audience and examples
  (genomic text files, `sort -k`, `join`, awk on GTF).
- Aho, Kernighan & Weinberger 2023, *The AWK Programming Language*,
  2nd ed. (Addison-Wesley): for readers who want more awk; optional.
- GNU grep manual's regex chapter: short, exact reference for basic vs
  extended syntax.

## Austin's notes

-

## Review responses (2026-11-17)

Codex (`chapter_06_codex_review.md`). Each testable claim was rechecked
here first (GNU coreutils 9.11, grep 3.12, gawk 5.4.1, GNU gzip 1.15,
seqkit 2.14.0, the checksum-matched files); all reproduced. Accepted
and applied above:

- **Mate IDs (high).** My error in wording: the plan said "without their
  `/1` and `/2` endings", but the marker sits mid-header (confirmed:
  `sed 's|/1$||'` changes nothing). The check now compares the first
  header field (50,000 each, identical, first `@SRR6357070.25017281`),
  adds the line count because `cmp` is silent on two empty files
  (confirmed), and a negative example with one changed ID (confirmed:
  `differ: char 54, line 3`, exit 1). Exercise 3 rewritten to match.
- **GNU gzip partial output (high).** Confirmed 89,515 with GNU gzip
  1.15 vs 89,253 with Apple gzip. §4 now uses the GNU number labelled
  with its version, states the lesson as "partial output, incomplete
  count", drops "not a multiple of 4" as a damage test, hedges the 141
  status, and separates what `pipefail` catches from Chapter 4's
  seqkit exit 0.
- **Adapter exercise (medium).** Confirmed: seqkit with and without
  `-P` gives 1,916 / 1,910, the same as grep. Exercise 6 now expects
  agreement, uses `-s -P`, and adds a reverse-complement toy where
  the strand setting matters (confirmed: default 1, `-P` 0). "Exact
  motif", not adapter contamination; `grep -c` counts lines.
- **Scratch paths and `pixi run` (high).** All writing commands use full
  `~/bioinf-computing-ch06/` paths; the `tee` example uses `pixi run`
  and keeps `-T`; `noclobber` demonstrated in a subshell, with what it
  does not guard; the `NOTEBOOK.md` exception stated.
- **Regex tester (medium).** Confirmed `grep -Eo 'a|ab'` → `ab`. The
  tester is labelled JavaScript, uses a shared subset of patterns
  checked against GNU grep, handles invalid patterns, and has a static
  fallback table. §7 names the separate engines.
- **Four-line assumption (medium).** Every `NR % 4`, `head -n 400`, and
  `1~4` use is labelled "this four-line file", with the seqkit recipe
  beside it; the sed FASTQ→FASTA one-liner moved to an optional box;
  the `grep -A 3` pattern escapes its dot.
- **Smaller points:** one canonical copy of the practice table after
  §5's recreate block; header removed before `sort -u`; `sort -u`
  removes identical rows, not conflicting records; the purpose of
  sorting before `uniq -c`; a pipe avoids an intermediate file but not
  memory or `sort`'s temporary files; `gunzip -c | head` does not check
  the rest of the file; stdout/stderr called a convention; GTF
  extension work (gene IDs, biotypes, longest spans) made optional with
  supplied commands, and "span (`end − start + 1`), not spliced
  length"; bedtools removed as a GTF feature filter in §10's table.
- **Colours.** Corrected to STYLE-GUIDE §2: results `given`, routine
  stderr `muted`, `warn` only for the overwrite and the gzip error,
  `good` only for checks.

Not adopted: nothing rejected. One partial: the review suggests a
small fixed table to back up the regex tester; adopted as a short
prediction/result table, not a full duplicate of the figure.

## Decisions (2026-11-17, open questions round)

Austin's choices:

- **Keep `gunzip -c`** in every command, as in Chapters 1–5. §9 says
  in one line that `zcat` does the same thing (GNU gzip runs `gzip -cd`
  for both), so readers recognise it in other people's scripts, and
  why the book avoids it (macOS's built-in `zcat` fails on `.gz`).
- **Build the regex tester** (`fig-regex-tester`, Observable JS, §7).
- **Scratch folder only.** All Chapter 6 output goes to
  `~/bioinf-computing-ch06/`; the GTF summary becomes Chapter 8's second
  numbered script (note for the Chapter 8 plan).
- **seqkit drops the good file's row: Chapter 4, after checking
  upstream.** Latest release is still v2.14.0 (2026-09-24) and no
  matching issue was found in shenwei356/seqkit (*checked*
  2026-11-17). One sentence added after the exit-status example in
  `chapters/04-getting-help.qmd`. Opening an upstream issue is left
  to Austin.

- **Chapter 5's practice table as §5's warm-up** (decided after the
  scratch-folder rename): `~/bioinf-computing-ch05/share/meta/samples.tsv`
  opens §5 (`uniq` missing a non-adjacent duplicate, then `sort | uniq
  -c`), before the real sample sheet and GTF. It replaces the made-up
  `printf 'a\nb\na\n'` example. A recreate block covers readers who
  skipped Chapter 5. Rows final in the Chapter 5 plan (2026-11-17);
  §5's and §8's outputs on it *captured* (MD5
  `971d8f742cb76a8d181d3bdc3dcbceaa`). **Dependency:** if Chapter 5
  changes the rows, update the recreate block and recapture; the
  duplicate must stay on non-adjacent rows.

- **Plan agreed** (2026-11-17): its 7 misconceptions added to
  `misconceptions.yml` under "Chapter 6".

Resolved by checking: the `not_in_genome` line is deliberate (nf-core
commit `1b17b24`, 2019-08-30); §5 updated.

## Implementation notes (2026-11-17, chapter drafted)

`chapters/06-text-tools.qmd` written from this plan after a final review
against the built Chapter 5. Every output recaptured in a clean `bash
--norc` with GNU tools **and GNU gzip 1.15** (so §2's `PIPESTATUS` and
§4's truncated file are now GNU captures). What changed from the plan:

- **Builds on Chapter 5 as built:** §5 says the `not_in_genome` line was
  already seen in Chapter 5's Exercise 5 (now "counting shows it is the
  only one"); `noclobber` is introduced as `cp -n` for `>`; Chapter 5's
  `history | tail`, `head`/`tail`, `zless`, `file` are assumed, not
  retaught.
- **Builds on Chapter 3's script:** §4 explains its `seqkit stats
  --quiet` (turns the progress line off) and `{ … } 2>&1 | tee "$log"`.
- **Figure label:** `fig-pipeline` became `fig-pipeline-steps`
  (`figures/pipeline-steps.svg`), matching `shell-steps`/`cd-steps`.
- **GNU gzip details:** a blank line before `gzip: … unexpected end of
  file`; `seqs.txt.gz` is 853,893 bytes (854,368 with Apple gzip), so the
  text says "about 850 KB" and that size depends on the gzip version.
- **Exercise 3's negative example:** now `sed '3s/$/x/'` (adds an `x`),
  so `cmp` says `differ: char 61, line 3` (the plan's 54 came from a
  different edit).
- **Exercise 2:** written as four concrete broken lines with full paths
  (`pixi run` must run from `~/bioinf-computing`, so no `cd` into the
  scratch folder).
- **Glob vs regex:** a new captured example, `grep -c '*.fastq.gz'` → 0
  vs `'.*\.fastq\.gz'` → 7.
- **New small checks, captured:** `Permission denied` redirecting into
  read-only `data/raw/` (macOS; the file is untouched); every `N` base
  has quality `#` and no other base does (280 / 18,842), so §8 states
  it; the strand counts print `60 -` before `64 +` in `en_US.UTF-8`.
- **Regex tester:** 8 lines, 8 example patterns (in a datalist); all 12
  candidate patterns gave identical lines and matches in GNU grep 3.12
  and Node's JavaScript engine. Static fallback `tbl-regex-tester` added.
  Checked in headless Chrome over `http://`: the tester runs.
- **References:** `buffalo2015bioinformatics` (metadata from Open
  Library; O'Reilly's page refused the fetch, so the chapter says "its
  chapter on Unix data tools" without a chapter title), `aho2023awk`
  (InformIT page), `gnu2025grep` (the installed grep 3.12 manual; gnu.org
  refused connections). Shotts is the existing `shotts2025linux`.
- `index.qmd` and `README.md` now say Chapters 1–6 are drafted.

## Open questions

1. **Still to check on Linux/WSL:** the truncated-file count and the
   `head` pipeline's `141 0` (both done with GNU gzip 1.15 on the Mac);
   the default locale and `sort` order on WSL Ubuntu and on Nova/Ceres;
   the `Permission denied` wording there. (Done while drafting: the
   regex tester patterns, `Permission denied` on macOS, Exercise 6.)
2. **Upstream seqkit issue:** Austin decided to post it from a
   draft; draft written 2026-11-17 (outside the repo). If seqkit fixes
   it, recapture Chapter 4's exit-status example.
