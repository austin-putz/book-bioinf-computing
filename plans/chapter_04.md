---
title: "Chapter 4 — Getting help"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** I — Getting set up · **Label:** core · **Status:** chapter
drafted 2026-11-17 (`chapters/04-getting-help.qmd`; see *Drafting
notes*), from this plan as revised after the Codex review
(`chapter_04_codex_review.md`; see *Review responses*). Outputs marked
*captured* were recorded on 2026-11-17 with the book environment
(`setup/pixi.toml` + `pixi.lock`, pixi 0.84.2, seqkit 2.14.0, R 4.4.3)
installed in a scratch folder on macOS 15 Intel; the rest are to be
checked while drafting.

## From `PLAN_CHAPTERS.md`

- `--help`, `man` pages, tool documentation
- Routine troubleshooting: read the error or warning; find the log; check
  paths, inputs, and requested resources; know when to ask
- Reading a methods section to find tools, versions, parameters
- Searching well; Biostars, Bioconductor support site
- Asking for help: code, complete messages, session info; a minimal
  reproducible example
- Using AI coding assistants responsibly (verify output; no data or
  credentials pasted in)
- GitHub issues covered later (Part V)

## What this chapter builds on

- Chapter 1: the yeast FASTQ files, `gzip -t`, "a summary of `reads: 0`
  means the download failed"; stop-on-error checkpoints.
- Chapter 2: `pixi run`, `pixi info`, `pixi list`, why bare `seqkit` is
  "not found"; VS Code's terminal; `hostname` to know where you are.
- Chapter 3: the project in `~/bioinf-book` (raw data read-only, the log
  in `logs/`, `data/README.md`), checksums, and the provenance chain.
  A good help request is that chain written out for someone else.
  **Dependency:** Chapter 3's supplied script must write the tool's own
  messages (stderr) into its log, and not overwrite a same-day log, for
  §4's "find the log" step to work on it. That fix belongs to the
  Chapter 3 plan (its Codex review proposes it); until then §4 uses its
  own tested example and captured text.
- The book's own **Report an issue!** page and its *Something doesn't
  run* form (`.github/ISSUE_TEMPLATE/doesnt-run.yml`) ask for where it
  ran, OS, cluster, exact command, complete error as text, and
  `pixi info`. The chapter uses that form as the **starting model** and
  adds what a tool-specific question also needs: the failing tool's
  version, what you expected, what you tried, and a small example
  (decided: add those as optional fields to the form; see *Decisions*).

## Outcome and check

- **Outcome:** faced with a failing command, readers read the message,
  find the log, run a short checklist (where am I, which environment, do
  the inputs exist and look right, are resources short, what changed),
  and fix the common causes themselves. When they cannot, they search
  well and write a help request someone can answer: exact command,
  complete message as text, versions, and a small example that still
  fails, with nothing private in it. They can find tools, versions, and
  parameters in a methods section, look up a flag in `--help`, and check
  an AI-suggested command before running it.
- **Check:** two parts.
  1. Exercise 1's supplied script, `~/bioinf-ch04/count.sh`, holds one
     `seqkit stats` command with three faults. It fails three times, in
     this order (*captured*, seqkit 2.14.0): `Error: unknown flag:
     --paired` → `[ERRO] stat –T: no such file or directory` →
     `[ERRO] stat data/raw/SRR6357070_l.fastq.gz: no such file or
     directory`. After all three fixes it prints:

     ```
     file                            format  type  num_seqs  sum_len  min_len  avg_len  max_len
     data/raw/SRR6357070_1.fastq.gz  FASTQ   DNA   50000     5050000  101      101.0    101
     data/raw/SRR6357070_2.fastq.gz  FASTQ   DNA   50000     5050000  101      101.0    101
     ```

  2. Exercise 3's `help_request.md` passes one test: could someone else
     reproduce the failure from its commands and small input alone,
     without access to your home folder? The answer key shows a model
     request and the one missing fact that would force a follow-up
     question.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Look up how to use a tool with `--help`, `man`, and its official
   documentation, and read a usage line.
2. Read an error or warning: find which command printed it, what failed,
   and on what.
3. Work through a short checklist (message, log, location, environment,
   inputs, resources, recent changes) before asking for help.
4. Find the tools, versions, parameters, and reference reported in a
   paper's methods section, and say what the passage does not report.
5. Write a help request with the exact command, the complete message,
   versions, and a minimal example that still fails, with no passwords
   or private data, and check AI-suggested code before you run it.

## Sections

Same pattern as Chapters 1–3: each section opens with something readers
run, read, or diagnose, then names the idea. All examples use the book's
own files and environment, so every error readers see in the chapter is
one they can reproduce, or read in the captured output. Commands run on
the laptop, from `~/bioinf-book` unless a step says otherwise. Visual
items in brackets are specified under *Visuals and teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   things break for everyone, every day; the skill is not avoiding
   errors but getting from a message to a fix, and knowing when and how
   to ask. Most fixes take the steps in this chapter, not expertise.
2. **Asking the tool itself: `--help`, `man`, docs.** *Start hands-on:*
   `pixi run seqkit --help` (top: version, docs URL, source, "Please
   cite"; then the list of subcommands), then `pixi run seqkit stats
   --help` and find the flag for tabular output (`-T, --tabular`) and
   for threads (`-j, --threads`; both *captured*). Then `gzip --help`
   and `man gzip` (move with Space and arrows, search with `/`, quit
   with `q`; `less` keys in Chapter 5). Then `pixi run man seqkit` →
   `No manual entry for seqkit` (*captured*): many bioinformatics tools
   have only `--help` and a website. *Then name the parts* with the
   usage-line figure, on GNU's `Usage: gzip [OPTION]... [FILE]...`:
   square brackets = optional, `...` = may repeat; words in capitals or
   in angle brackets commonly mark a value you supply; none of the
   brackets are typed. Short (`-T`) and long (`--tabular`) forms of one
   flag; flags that take a value (`-j 4`, `--threads 4`). Subcommand
   tools (`seqkit stats`, `samtools sort`, `git commit`) have help at
   each level. Some tools use `-h`, some `help`, some print usage when
   run with no arguments. `--version` (or `seqkit version`) and why it
   matters: online docs describe the latest release; your installed
   version may differ (Chapter 2's `pixi list`). The help text also
   says what to cite: SeqKit's points to the SeqKit2 paper (Shen et al.
   2024). R's `?read.csv` and Python's `help()` get one line each;
   Chapters 12–13 use them.
   **macOS note (*checked*):** after Chapter 1's setup, `ls` and `sed`
   run the GNU tools but `man ls` and `man sed` open the macOS (BSD)
   pages. Chapter 1 will add the GNU manual folders (see *Decisions*),
   so this becomes a one-line note; the tip stays: `--help`
   comes from the program you actually run, so it always matches it.
   [`fig-usage-line`, `tbl-help-sources`; tip; self-check]
3. **Reading an error message.** *Start with a diagnosis round:* six
   failing commands on the book's files, each shown with its real
   output (*captured*, seqkit 2.14.0), and readers say what went wrong
   before opening the collapsed answer:

   | Command | Message (abridged) | Cause |
   |:--------|:-------------------|:------|
   | `seqkit stats data/raw/…` (no `pixi run`) | `bash: seqkit: command not found` | not on this shell's `PATH` (Chapter 2) |
   | `pixi run seqkit stats data/raw/SRR6357070_l.fastq.gz` | `[ERRO] stat …_l.fastq.gz: no such file or directory` | letter `l` typed for digit `1` |
   | `pixi run seqkit stats –T data/raw/…` | `[ERRO] stat –T: no such file or directory` | en dash copied from a PDF: not a flag, so seqkit took it as a file name |
   | `pixi run seqkit stats --paired data/raw/…` | `Error: unknown flag: --paired` | flag does not exist (see §8) |
   | `pixi run seqkit stats -T broken.fastq.gz` (truncated copy) | header line only on stdout; `[ERRO] broken.fastq.gz: unexpected EOF` on stderr; **exit status 0** | file cut short |
   | `pixi run Rscript -e 'read.csv("data/meta/samples.csv")'` | `Error in file(file, "rt") : cannot open the connection` … `Warning … cannot open file 'data/meta/samples.csv': No such file or directory` | wrong name (`.tsv` vs `.csv`); the reason is in the warning *after* the error |

   The first row's answer adds one sentence: bare `seqkit` fails only
   when no seqkit is on `PATH`; if another copy is installed, it runs
   that one instead, possibly a different version (Chapter 7).
   *Then a reading strategy* with the error-anatomy figure: look for
   **who** printed it (`bash:` = the shell could not start the program;
   otherwise the program you ran, which you know from the command;
   `[ERRO]` and `Error` are severity labels, not names; R's
   `Error in f(...)` names the function), **what** failed, and **on
   what** (the file, flag, or object, often quoted). Not every message
   has all three: `Killed` or a crash may say almost nothing, and then
   the log and the checklist (§4) carry the diagnosis. Read the whole
   message: find the earliest relevant failure in *this* run; later
   lines are often consequences, but the useful detail can sit in a
   later line (the R example), and old logs may hold errors from earlier
   runs. Errors and warnings: an error reports that an operation
   failed (whether a script carries on depends on the program and the
   script, Chapter 8); a warning asks you to look. Sometimes the result
   is still what you wanted, sometimes not:
   `as.integer(c("12","7","n/a"))` gives `NA` for `n/a` with only a
   warning, exit 0 (*captured*), which is right only if `n/a` really
   means missing in that column. *Exit status* in one paragraph:
   `echo $?` **immediately** after the command (any other command in
   between replaces it); `0` means the program reported success to the
   shell, `127` = command not found (*captured*). It does not prove the
   output answers your question: seqkit 2.14.0 printed `unexpected EOF`
   and still exited 0. SeqKit's current documentation describes a
   nonzero status for read errors, so this may change with the version,
   which is the lesson: read the messages and check the result against
   something you know (here, 50,000 reads). Pipeline status is
   Chapter 8. [`fig-error-anatomy`, `tbl-common-errors`; key idea;
   misconception callout `no-error-means-correct`; self-check]
4. **Before you ask: a troubleshooting checklist.** *Start hands-on with
   two cases:*
   - **Wrong folder.** Readers `cd ~` and rerun Chapter 3's
     `pixi run bash src/01_count_reads.sh`; pixi answers `could not
     find pixi.toml or pyproject.toml with tool.pixi at directory …`
     (*captured*; the text adds that the message can differ if another
     `pixi.toml` sits in a parent folder). Solved at the checklist's
     third question (`pwd`). Then `cd ~/bioinf-book` before going on.
   - **A pattern that matches nothing.** `pixi run seqkit stats -T
     data/raw/*.fq.gz` (the files end in `.fastq.gz`): bash passes the
     unmatched pattern on unchanged, and seqkit answers `[ERRO] stat
     data/raw/*.fq.gz: no such file or directory` (*captured*). The
     literal `*` in the message is the clue; `ls data/raw/` shows the
     real names. Solved at question four. Why bash does this:
     Chapter 5.

   *Then name the checklist* as a figure and a table. Stop as soon as
   the problem is solved; not every step is needed every time:
   1. **Read the message** (§3), all of it.
   2. **Find the log.** Here: the terminal and `logs/` (Chapter 3).
      Later: `slurm-<jobid>.out` (Chapter 10), `.nextflow.log` and the
      task's `.command.err` (Chapter 26). The terminal may show only
      the last lines; a log can hold the first error. Not every program
      writes a log, and a log does not always name the cause.
   3. **Where am I, with what?** `pwd`, `hostname`, `ls`; `pixi run` or
      not; on a cluster, which modules are loaded.
   4. **Do the inputs exist and look right?** `ls -l`, `head`,
      `gzip -t`, `md5sum -c` (Chapter 3), sample-sheet names vs file
      names.
   5. **Are resources short?** `No space left on device`, `Disk quota
      exceeded`, a time limit, `Killed` (often, but not always, out of
      memory; the scheduler's records confirm it, Chapter 10), from
      Chapter 1's `tbl-resource-limits`.
   6. **What changed** since it last worked? New data, new version, new
      folder, new machine?
   7. **Make it small.** Does it still fail on 100 reads, on one
      sample? (Leads into §7.)

   Then, if it is still not solved: **ask** (§6–7), the way out of the
   checklist, not an eighth step. *When to ask:* about an hour without
   progress is a useful point to stop and ask (your lab's norms win;
   it is not a rule you must reach first). Ask **at once** for anything
   about accounts, passwords, or keys; when a fix could damage data or
   affect other users; and when something that worked stops working in
   a way you cannot explain from your own changes (a slow or missing
   filesystem, a module that will not load, a quota). You do not need
   to know that the system is at fault: report what you saw and what
   you checked. [`fig-troubleshooting-checklist` (stepped),
   `tbl-checklist`; key idea; pitfall: changing many things at once;
   self-check]
5. **Reading a methods section.** *Start hands-on:* the RNA-seq methods
   of the running dataset's own paper, Wu et al. 2018 (CC BY, PMC6310685,
   so it can be quoted), excerpted: the *Software and Algorithms* rows
   of the Key Resources Table and the *Differential Expression
   Analysis* paragraph, with a short glossary box (adapter trimming,
   alignment, counting, differential expression: one line each,
   pointing to Transcriptomics). Readers fill in a table: step · tool ·
   version · parameters as printed · parameters as you would type them ·
   reference. Answers (*checked* in the paper's text): cutadapt 1.9.1
   (`--minimum-length=25 --quality-cutoff=20 -a AGATCGGAAGAGC -A
   AGATCGGAAGAGC`); RSEM 1.3.0 with STAR 2.5.2a
   (`--star-output-genome-bam --forward-prob 0`, all else default);
   *S. cerevisiae* genes from Ensembl, assembly R64-1-1, release 90;
   DESeq2 1.12.3 in R 3.3.1. *Then three discoveries:*
   - The paper prints `–minimum-length` and `–forward-prob` with a
     single en dash: typesetting turned `--` into `–`. Copied as is,
     they fail exactly like row 3 of §3's table. Retype dashes and
     quotes when copying from PDFs and web pages.
   - The paper reports a strandedness setting (`--forward-prob 0`).
     The nf-core test sheet the book uses (Chapter 3) says `auto` for
     `WT_REP1`, our sample: it asks the pipeline to *work out* the
     strandedness rather than stating it, so it is not an independent
     confirmation of the paper's value. (What strandedness is: Chapter
     26 and Transcriptomics.)
   - What this excerpt does not report: STAR/RSEM index settings,
     DESeq2's design and thresholds, and code. Whether they appear
     elsewhere (supplements, deposited code) needs checking before
     saying the paper omits them. Good methods (Chapter 3's chain) name
     tool, version, parameters, reference release, and where code and
     data are.

   One paragraph: the book later runs these reads through nf-core/rnaseq
   (Chapter 26); that is a different, newer analysis, not a
   reconstruction of the paper's. And methods sections can describe
   several libraries: this paper also has 76 bp single-end TSS-seq.
   Which paragraph describes *our* reads? Exercise 4 matches it against
   the run's public record. [`tbl-methods-extract`; pitfall: en dashes;
   self-check]
6. **Searching and choosing where to ask.** *Start hands-on:* turn a raw
   error into a search. Given `[ERRO] /home/<user>/proj/sample_17_R1.fq.gz:
   unexpected EOF`, remove what is yours (paths, sample names), keep the
   distinctive part in quotes, add the tool name: `seqkit "unexpected
   EOF"`. Search the tool's GitHub issues, **including closed ones**
   (reading only; filing an issue is Chapter 22). *Then where to ask,
   by kind of problem* (table): account, quota, node, module, or
   anything site-specific → your cluster's help desk (Appendix A has
   each site's contacts); how to use a package → its own support venue
   (Bioconductor packages: the Bioconductor support site and its
   posting guide; nf-core pipelines: nf-core's channels, Chapter 26;
   other tools: their docs, then GitHub issues or discussions);
   general bioinformatics questions → Biostars; general R, Python, or
   shell → Stack Overflow; a command from this book → the book's
   **Report an issue!** page. Your lab and local experts first, if
   that is your lab's habit. *Then judging an answer:* how old is it,
   which version does it assume, is it from the tool's authors or docs,
   does it explain *why*, and does it work on your small example. A
   2015 answer may name flags that no longer exist. [`tbl-where-to-ask`;
   tip; self-check]
7. **Asking for help.** *Start hands-on:* a bad request ("seqkit doesn't
   work on the cluster, help!!", with a screenshot) rewritten into a
   good one. Start from the book's *Something doesn't run* form (where
   it ran: laptop / login node / compute node, OS, cluster; exact
   command, copied; complete message as text; `pixi info`) and add what
   a tool question needs: what you were trying to do and expected; what
   you tried; the failing tool's version; a small example. Versions,
   each for its own question: `pixi info` (platform, pixi, which
   environment; *captured*: it does **not** list package versions);
   `pixi run seqkit version` (the tool that failed; with `pixi run`, so
   it reports the copy that actually ran); `pixi list` when several
   package versions matter; in R, `pixi run Rscript -e 'sessionInfo()'`.
   Do not paste the whole lockfile. *Then the minimal reproducible
   example:* shrink until it still fails, and **rerun after every cut
   to check it still fails the same way**. Fewer files, one sample, the
   first 100 reads:

   ```bash
   pixi run seqkit head -n 100 data/raw/SRR6357070_1.fastq.gz \
     -o ~/bioinf-ch04/small_R1.fastq.gz
   ```

   (*captured*: 100 reads, 10,100 bases; written to the exercise
   folder, never to `data/raw/`). The warning example (*captured*): the
   first 100 reads of the truncated file are intact, so the small copy
   no longer shows `unexpected EOF`. Shrinking removed the bug; the
   example is too small. Some failures need no real data at all (a
   wrong file name fails on any file). Often the shrinking finds the
   bug. R's `reprex` package gets one line (Chapter 12).
   *Text, not screenshots, for commands and messages:* text can be
   searched, copied, and read by screen readers; Markdown code blocks
   with three backticks (Markdown met in Chapter 3). A screenshot can
   **add** to text when the problem is something on screen (a VS Code
   panel, a dialog). For long logs, post the relevant part with a few
   lines around it and keep the full log to share as the venue asks.
   *Then privacy and etiquette:* replace user names, paths, and host
   names you would rather not share with placeholders, consistently,
   and without hiding the fault (keep the relative layout, the
   extension, the case, the `l` vs `1`, the en dash); `pixi info`
   prints home-folder paths (*captured*). Never post passwords, SSH
   private keys, tokens, unpublished data, or data under a use agreement
   (ask your PI if unsure); public forums are permanent and indexed.
   Say if you posted the same question elsewhere; when solved, post the
   answer and mark it. [`fig-good-request`, `tbl-request-checklist`;
   pitfall: secrets; misconception `screenshot-is-fine`; self-check]
8. **AI coding assistants.** Short. *Start hands-on:* a constructed
   example (labelled as written for the book, not captured from a
   particular assistant) of an answer to "count read pairs in my paired
   FASTQ files with seqkit" that suggests `seqkit stats --paired …`.
   Readers check it: (1) the flag in `pixi run seqkit stats --help` (not
   there); (2) run it: `Error: unknown flag: --paired` (*captured*); (3)
   run the corrected command with the two mate files named, and check
   the **meaning**: each row is one mate file with 50,000 reads, so the
   run has 50,000 read pairs, not 100,000 (Chapter 1). Syntax fixed is
   not question answered. *Then the rules:* treat suggestions as coming
   from a fast, confident colleague who is sometimes wrong; check every
   flag against `--help` for **your** version; test on small data with
   a known answer; understand any command before running it, above all
   ones that delete or overwrite (`rm`, `>`, `mv`), and never run them
   on raw data or shared systems unread; paste error text and small toy
   examples, never credentials, private or unpublished data, or anything
   your institution or data agreement restricts (check their current
   policy; no links, so nothing goes stale); follow your journal's and university's
   rules on disclosing AI use. Assistants are good at explaining an
   error message or drafting a help request, the two skills this
   chapter teaches, as long as you check the result. [`tbl-ai-checks`;
   pitfall; misconception `ai-code-is-tested`; self-check]
9. **Summary, exercises, further reading.** Summary as 5 bullets that
   mirror the learning goals; exercises (below); annotated further
   reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2):
our data and file names are `given` (blue); checks and fixes `good`
(green); software text and messages neutral (`ink`, `line`, `muted`);
`warn` only for the en-dash pitfall and secrets in `fig-good-request`.

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-usage-line` | 2 | static | `Usage: gzip [OPTION]... [FILE]...` and a `seqkit stats` flag line (`-T, --tabular  output in machine-friendly tabular format`), with brackets, `...`, short/long forms, and the description labelled; a note that brackets are not typed. |
| `fig-error-anatomy` | 3 | static | Two real messages, the seqkit typo and the R read error, with three labels each: *who* (the command run; `[ERRO]` marked as a severity label) / `Error in file(...)`, *what* (`stat` / `cannot open`), *on what* (the file name, `given`). The R one also marks "the reason is in the warning below". Caption: a reading strategy; not every message has all three. |
| `fig-troubleshooting-checklist` | 4 | stepped (7 steps + exit) | The checklist as a path with an exit at every step ("solved → stop") and "ask" as the way out after step 7. Each step shows the one command or place to look. The wrong-folder case exits at step 3, the `*.fq.gz` case at step 4. |
| `fig-good-request` | 7 | static | A help request built from the book's issue form plus the added fields (expected, tried, tool version, small example), each field labelled with why it matters. One `warn` mark on a home path and a token, replaced by consistent placeholders that keep the fault visible. |

Not used here: screenshots (the §7 bad request's screenshot is drawn
as a schematic), Mermaid.

### Interactive figure (Observable JS)

None.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-help-sources` | 2 | Source (`--help`/`-h`, subcommand help, `man`, official docs site, `--version`, R `?`, Python `help()`) · what it gives · matches your installed version? · example |
| `tbl-common-errors` | 3 | Message · who prints it · usual cause · first thing to check. **Now** (readers meet these in Part I): `command not found`, `No such file or directory`, `Permission denied` (Chapter 3's read-only raw data), `unknown flag` / `unrecognized option`, `unexpected EOF`, `No space left on device`, `Disk quota exceeded`, `Killed`. R `could not find function`, Python `ModuleNotFoundError`, and `Segmentation fault` move to their own chapters (12, 13, 10) |
| `tbl-checklist` | 4 | Step · question · commands or places to look · chapter that goes deeper |
| `tbl-methods-extract` | 5 | Step · tool · version · parameters as printed · as you would type them · reference/data · reported in this excerpt? (filled for Wu et al. 2018) |
| `tbl-where-to-ask` | 6 | Kind of problem · where to ask · who answers · before posting (search, posting guide) |
| `tbl-request-checklist` | 7 | Include · example · why · never include |
| `tbl-ai-checks` | 8 | Check · how · what it catches (flag exists, version, toy data with known answer, meaning of the output, destructive commands, data sent) |

### Code (§6)

- `filename="Terminal (laptop)"`, tier 2 (shown, not run at render),
  every step cheap. Cluster readers: the same commands work on a login
  node; one paragraph in §4 says where cluster logs live (Chapter 10).
- Failing commands are shown **with** their captured output in
  `.console` blocks, the cause hidden in a collapsed answer so readers
  diagnose first (§3 round). Captures keep stdout and stderr apart
  where it matters (the truncated file: header on stdout, `[ERRO]` on
  stderr), and give the exit status. ANSI colour codes stripped from
  seqkit output (`[ERRO]` is red in a terminal; say so). seqkit prints
  a `processed files` progress line on stderr when given several files
  (*captured*); drop it from captures or mention it once.
- Every capture that depends on a version is labelled with it ("seqkit
  2.14.0") and rechecked whenever `setup/pixi.lock` changes.
- The en dash in §3 and §5 must survive Quarto rendering as a real
  en dash (`–`, U+2013) inside code, and the corrected commands must
  keep ASCII `-`; check the rendered HTML, and that Quarto's smart
  punctuation does not touch code.
- `filename="~/bioinf-ch04/count.sh"` for exercise 1's script; the
  exercise folder is scratch, like `~/bioinf-ch01`, so the project
  stays clean. Starting version (*captured*):

  ```bash
  # count.sh: count reads in both raw files (has three faults)
  # Run from ~/bioinf-book:  pixi run bash ~/bioinf-ch04/count.sh
  seqkit stats –T --paired data/raw/SRR6357070_l.fastq.gz data/raw/SRR6357070_2.fastq.gz
  ```

  One command, so it stops at the first failure without any shell
  control flow; seqkit checks flags before files, so the order is fixed:
  invented flag, then en dash, then typo. The answer key keeps each
  intermediate version, its message, and its exit status.
- Bash everywhere: `man` and `--help` as on Linux; the macOS `man` note
  in §2 is the one OS difference.

### Plots

None.

### Animation (manim)

None.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Tip | `--help` comes from the program you are running, so it matches your version; online docs and (on macOS) `man` pages may not |
| 3 | Key idea | Look for who printed the message, what failed, and on what; read all of it and find the earliest relevant failure. Exit status 0 means "reported success", not "right answer" |
| 3 | Misconception | "No error message means the result is right" (`no-error-means-correct`) |
| 4 | Key idea | Most problems are found by the same few questions: where am I, with which software, on which inputs, with enough resources, and what changed. Stop when it is solved |
| 4 | Pitfall | Change one thing at a time; three changes at once leave you not knowing which one fixed (or broke) it |
| 5 | Pitfall | Copying commands from PDFs and web pages turns `--` into `–` and straight quotes into curly ones; retype them |
| 6 | Tip | Search the distinctive part of the message in quotes, without your paths and sample names, plus the tool name |
| 7 | Pitfall | Never post passwords, SSH private keys, tokens, or private data; forums and issues are public and permanent |
| 8 | Pitfall | Check every AI-suggested flag against `--help`, and test on data with a known answer, before running it on real data |
| 8 | Misconception | "Code from an AI assistant has been tested" (`ai-code-is-tested`) |

`last-line-is-the-error` and `screenshot-is-fine` are handled in the
text and self-checks, to stay under three callouts per screen.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: In `Usage: gzip [OPTION]... [FILE]...`, must you give a file?
  (*No: `[FILE]` is optional; with no file gzip reads standard input,
  Chapter 6.*)
- §3: A message starts `bash: samtools: command not found`. Did samtools
  run? (*No: the shell could not find it, so it never started. Check
  `pixi run` or `module load`.*)
- §4: A script worked yesterday and fails today with `No such file or
  directory`. Name two checklist questions to ask first. (*Where am I
  (`pwd`)? Do the inputs exist (`ls -l`)? What changed (moved folder,
  renamed file)?*)
- §5: The excerpt says "STAR (version 2.5.2a)" but not the index
  options. Can you reproduce the alignment exactly from the excerpt?
  (*Not for certain: index settings change results. Check the
  supplements and any deposited code, then assume defaults or ask the
  authors.*)
- §6: Your job on the cluster cannot write to `/project` and
  `my_quotas` shows you at your limit. Where do you ask? (*Your
  cluster's help desk, or your PI if the project quota is theirs to
  raise; not Biostars.*)
- §7: Why paste the error as text rather than a screenshot? (*Text can
  be searched, copied into a search engine, quoted, and read by screen
  readers; screenshots often cut off the first error.*)
- §8: An assistant suggests `pixi run seqkit stats --count-pairs
  data/raw/*.fastq.gz`. What do you check before trusting it? (*That
  `--count-pairs` is in `seqkit stats --help` for your version; it is
  not in 2.14.0, *captured*: `Error: unknown flag: --count-pairs`.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
material):

1. **Fix a broken script.** Copy the supplied `~/bioinf-ch04/count.sh`.
   Run it with `pixi run bash ~/bioinf-ch04/count.sh` from
   `~/bioinf-book`. It fails three times; fix one fault at a time from
   the message and `--help` alone, rerunning after each, and note in
   `NOTEBOOK.md` what each message said and what you changed. (*Order:
   unknown flag, en dash, typo; final output as in the check.*)
2. **Read the help.** From `pixi run seqkit stats --help`, find the
   flag that adds quartiles and N50 (`-a, --all`). Run
   `pixi run seqkit stats -a -T` on both raw files. Which columns
   appear that were not there before?
3. **Write a help request.** Pretend exercise 1's first error is one
   you cannot solve. Write the request in `~/bioinf-ch04/help_request.md`
   from the book's *Something doesn't run* form plus the added fields
   (expected, tried, `pixi run seqkit version`, small example), with
   `pixi info` output whose home path is replaced by `<home>`. For the
   example, make a 100-read file with the supplied `seqkit head`
   command and **check that the same error still appears with it**. Do
   not submit it. Then test it: could someone reproduce the failure from
   the request alone? (*Answer: an annotated model request, and the one
   missing fact (the tool version) that would force a follow-up.*)
4. **Match the paper to the data.** Open the ENA record for SRR6357070
   (link supplied; a dated capture of the fields is in the answer, in
   case the page changes). Find library layout, instrument, and the
   read count, and say what unit it is in. Which methods paragraph of
   Wu et al. 2018 describes this run: the RNA-seq one or the TSS-seq
   one? (*RNA-seq: ENA says `PAIRED`, Illumina HiSeq 2500, total
   RNA-seq, 47,629,288 read pairs (9.6 billion bases = 202 per pair);
   the RNA-seq paragraph says ~45 million 101 bp strand-specific
   paired-end reads on HiSeq 2500 or 4000; TSS-seq was 76 bp single-end
   on HiSeq 4000. Our file is a 50,000-pair subset made by nf-core;
   ENA's checksums are for the full files, not ours.*)
5. **Check an AI answer.** Use the supplied answer (or, optionally, ask
   an AI assistant you already use) for a command that counts read
   pairs in `data/raw/` with seqkit. Check every flag in `--help`, run
   it, and say whether the output answers the question (pairs, not
   reads). Record in `NOTEBOOK.md` what you checked. If you use an
   assistant, paste only the question, no files.

## Examples and data

- Toy examples: a truncated FASTQ copy (`head -c 1000000`, as in Chapter
  3's exercise 2), a 100-read FASTQ (`seqkit head -n 100`), the broken
  script, the bad and good help requests.
- Running dataset: `data/raw/SRR6357070_1.fastq.gz` and `_2` in
  `~/bioinf-book` (Chapter 3); nothing new to download, so no new rows
  in `data/README.md`.
- Paper: Wu et al. 2018, *Mol Cell* 72(6):942–954.e7,
  doi:10.1016/j.molcel.2018.10.018, PMC6310685, **CC BY** (Europe PMC,
  checked 2026-11-17), so short quotes and the Key Resources rows can be
  reproduced with credit. Already in `references.bib` as the dataset
  citation (check key).
- Public record: ENA run SRR6357070 (*checked* 2026-11-17): sample
  GSM2879618 "Wild-type total RNA-Seq biological replicate 1", `PAIRED`,
  RNA-Seq, TRANSCRIPTOMIC, cDNA, Illumina HiSeq 2500, `read_count`
  47,629,288 (read pairs for a paired run), `base_count` 9,621,116,176
  (= 101 + 101 per pair), with an MD5 per full FASTQ file (Chapter 20).
- Captured outputs (2026-11-17, seqkit 2.14.0, R 4.4.3, pixi 0.84.2):
  `command not found` (exit 127); seqkit `no such file or directory`
  (exit 255); en dash `stat –T: no such file or directory` (exit 255);
  `Error: unknown flag: --paired` (and `--count-pairs`) followed by
  usage (exit 255); unmatched `data/raw/*.fq.gz` passed literally
  (`stat data/raw/*.fq.gz: no such file or directory`); truncated file
  `[ERRO] … unexpected EOF` on stderr, header only on stdout, **exit
  0**; 100-read `seqkit head` copy of the truncated file is intact
  (100 reads, no error); R `Error in file(file, "rt") : cannot open the
  connection` + warning with the reason (exit 1); R `NAs introduced by
  coercion` (exit 0); pixi `could not find pixi.toml or pyproject.toml
  with tool.pixi at directory …` (exit 1); `No manual entry for
  seqkit`; `pixi info` lists platform, cache and manifest paths, and
  environments but no package versions.
- Where commands run: laptop. Cluster equivalents named in §4 and
  Appendix A (site help desks).

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters), to add when this plan is agreed. Where each is handled
is in brackets.

- `no-error-means-correct`: "If no error appears, the result is right."
  Warnings let runs continue, and some tool versions report success
  after printing an error (seqkit 2.14.0 on a truncated file). Check
  outputs against something you know. Probe: `as.integer(c("12","7",
  "n/a"))` finished without an error; is the result fine? (Only if
  `n/a` means missing in that column.) [callout, §3; self-check]
- `last-line-is-the-error`: "The last line of the output is the error
  that matters." Look for the earliest relevant failure in this run;
  later lines are often consequences, and the detail can sit in a
  warning. [text, §3; `fig-error-anatomy`]
- `asking-is-failure`: "Asking for help means I wasn't good enough to
  solve it." Everyone asks; a well-made request is a skill, and some
  problems (broken nodes, quotas) only admins can fix. [text, §1 and §4]
- `screenshot-is-fine`: "A screenshot of the error is the easiest way to
  ask." Text can be searched, copied, and quoted; screenshots crop the
  first error and hide the command. A screenshot can add to text, not
  replace it. [text, §7; self-check]
- `ai-code-is-tested`: "Code from an AI assistant works; I can assume it
  has been tested." It is generated text; flags can be invented or
  belong to another version, and even code reported as tested may have
  been tested on other inputs or environments. Check flags in `--help`
  and reproduce a known result. [callout, §8; exercise 5]
- `docs-match-my-version`: "The online documentation describes the
  version I have installed." Websites show the latest release; check
  `--version` and use `--help`. [tip, §2]

## Links to other chapters and books

- Builds on: Chapters 1–3 (files, environment, project, logs,
  checksums, provenance), the book's **Report an issue!** page.
- Leads to: Chapter 5 (`less` keys used by `man`; quoting; why an
  unmatched `*` is passed on literally); Chapter 6 (standard error vs
  standard output, so messages and results can be separated); Chapter 7
  (`PATH`, which explains `command not found` and the wrong copy
  running); Chapter 8 (exit status in scripts and pipelines,
  `set -euo pipefail`, logging errors); Chapter 10 (SLURM logs, `seff`,
  out-of-memory and time limits, `Segmentation fault`); Chapters 12–13
  (R `?`, `sessionInfo()`, `reprex`; Python `help()` and tracebacks);
  Chapter 15 (FASTQ records, why "four lines per read" is not a general
  rule); Chapter 20 (ENA/SRA records and their MD5s); Chapter 22 (filing
  a GitHub issue on a tool's repo); Chapter 23 (recording versions);
  Chapter 26 (nf-core logs, `.command.err`, strandedness `auto`, the
  nf-core help channels); Chapter 34 (debuggers, for code you write);
  Appendix A (site help desks and documentation).

## Official links to include

- GNU coreutils manual (`--help` and `--version` conventions); `man`
  (man7.org `man(1)` page, or the GNU/Linux man-pages project)
- SeqKit docs (bioinf.shenwei.me/seqkit), including its exit-status
  note, and GitHub issues (github.com/shenwei356/seqkit/issues)
- Bioconductor support site (support.bioconductor.org) and its posting
  guide (bioconductor.org/help/support/posting-guide/)
- Biostars (biostars.org)
- Stack Overflow help page "How to create a Minimal, Reproducible
  Example" (stackoverflow.com/help/minimal-reproducible-example)
- reprex (reprex.tidyverse.org)
- nf-core help / Slack (nf-co.re/join)
- Wu et al. 2018 in PMC (PMC6310685); ENA run SRR6357070
  (ebi.ac.uk/ena/browser/view/SRR6357070)
- Site help: SCINet and ISU Research IT, via Appendix A

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). DOIs below verified
with scite 2026-11-17 (all found, no editorial notices); fetch BibTeX
from the DOI when adding.

- Dall'Olio, Marino, Schubert et al. 2011, "Ten simple rules for getting
  help from online scientific communities", *PLoS Comput Biol*,
  doi:10.1371/journal.pcbi.1002202: written by people from Biostars and
  bioinformatics forums; the main pick for §6–7.
- Haller 2022, "Ten simple rules for reporting a bug", *PLoS Comput
  Biol*, doi:10.1371/journal.pcbi.1010540 (author confirmed with scite):
  what makes a report fixable; fits §7 and points ahead to Chapter 22.
- "Ten simple rules for using large language models in science,
  version 1.0" (2024), *PLoS Comput Biol*,
  doi:10.1371/journal.pcbi.1011767, or the newer "Ten simple rules for
  responsible use of AI and LLMs in computational biology" (2026),
  doi:10.1371/journal.pcbi.1014882: pick one for §8 after reading both;
  the 2026 one is closer to this book's audience.
- Stack Overflow, "How to create a Minimal, Reproducible Example"
  (url + urldate): short, official, widely linked.
- Software citation, not further reading: Shen et al. 2024, "SeqKit2: a
  Swiss army knife for sequence and alignment processing", *iMeta*,
  doi:10.1002/imt2.191 (cited in §2 and added to Chapter 2; see
  *Decisions*).

## Austin's notes

-

## Review responses (2026-11-17)

Codex (`chapter_04_codex_review.md`). Each testable claim was rechecked
here before changing the plan (seqkit 2.14.0, pixi 0.84.2, the paper,
the v3.10 sample sheet, scite). Accepted and applied above:

- **Broken-script order:** confirmed that seqkit rejects the invented
  flag before it looks at files, so the order is flag → en dash → typo.
  Kept one command (fixing one error reveals the next) and recorded the
  real order and messages in the check and exercise 1.
- **Versions:** confirmed `pixi info` shows no package versions. §7 now
  separates `pixi info`, `pixi run seqkit version`, `pixi list`, and
  `sessionInfo()`, and calls the issue form a starting model, not a
  complete list.
- **Strandedness:** my error. The v3.10 sheet says `auto` for
  `WT_REP1` (Chapter 3's plan even notes it). §5's second discovery
  rewritten: `auto` asks the pipeline to infer it, so it is not a
  confirmation. Added that the book's nf-core run is not a
  reconstruction of the paper's analysis, and "not reported in this
  excerpt" instead of "missing".
- **Exit status:** kept the seqkit 2.14.0 example (still exit 0 with
  `-T`; stderr and stdout captured apart), labelled with the version
  and tied to SeqKit's docs describing a nonzero status. Softened
  "an error stops" and the `NA` warning; `echo $?` immediately after.
- **Second checklist case:** replaced the vague empty-table case with
  `data/raw/*.fq.gz`, captured.
- **Small example:** switched to `seqkit head -n 100 … -o` (*captured*)
  and added "rerun after every cut". Checked the review's warning: the
  100-read copy of the truncated file is intact and no longer fails, so
  it is now the teaching example. Placeholders must keep the fault
  visible.
- **Log and starting state:** §4 no longer relies on Chapter 3's log
  until that plan is fixed (dependency noted at the top); return to
  `~/bioinf-book` after `cd ~`; note on another `pixi.toml` in a
  parent folder and on a different seqkit on `PATH`; exercise 2 uses
  `pixi run`.
- **Smaller points:** `[ERRO]` as a severity label; "earliest relevant
  failure"; reading strategy, not a rule; `Killed` is not proof of
  out-of-memory; checklist steps can stop early and "ask" is the exit,
  not an eighth step; the one-hour mark is a checkpoint, and readers
  report symptoms without diagnosing the system; route questions by
  kind of problem; screenshots can supplement text; constructed AI
  example plus a meaning check (pairs, not reads); `ai-code-is-tested`
  reworded; usage notation hedged; `tbl-common-errors` cut to Part I
  messages; methods glossary; exercise 4 states units and the subset;
  self-check §8 now uses an invented seqkit flag (`--count-pairs`,
  *captured*), since samtools is not in the environment; Haller added
  as the bug-paper author.

Not adopted, or left for Austin:

- **Changing the issue form** (`doesnt-run.yml` + `reporting.qmd`) to
  ask for the tool version, expected result, and what was tried: a good
  idea, but it changes the live reporting setup, so it went to Austin
  (decided: optional fields; see *Decisions*).
- **Making the help-request test a formal check** is adopted, but as a
  yes/no question readers ask of their own request, not something
  graded by a command; there is no exact output to compare.

## Decisions (2026-11-17, open questions round)

Austin's choices:

- **macOS `man` pages: fix in Chapter 1.** Add Homebrew's
  `libexec/gnuman` folders to `MANPATH` in Chapter 1's `~/.bash_profile`
  block, next to the `gnubin` lines, using `$(brew --prefix)` rather
  than a fixed `/usr/local`, keeping the default manual paths; test on
  Intel and Apple silicon. §2 keeps the "trust `--help`" tip, reduced to
  a one-line macOS note.
- **SeqKit citation: cite both.** Add SeqKit2 (Shen et al. 2024,
  doi:10.1002/imt2.191, verified) to `references.bib` and Chapter 2,
  keeping the 2016 paper where it still fits. §2 here cites SeqKit2.
- **Issue form: add optional fields.** `doesnt-run.yml` gets optional
  "What did you expect?", "What have you tried?", and "Version of the
  failing tool (e.g. `pixi run seqkit version`)"; `reporting.qmd`
  updated to match, so the form and §7 teach the same request.
- **AI guidance: generic, no links.** §8 says "check your institution's
  and your data agreement's current policy"; no policy links, so
  nothing goes stale. Removed from *Official links to include*.

**Applied 2026-11-17:** `MANPATH` loop in Chapter 1's macOS step 4
(tested in an empty home folder with Homebrew bash 5.3 on Intel: `man -w`
gives the GNU pages for `ls`, `sed`, `find`, `tar`, `grep`, `awk`, `wc`;
Apple silicon still to test); `shen2024seqkit2` in `references.bib`
(BibTeX from the DOI) and cited in Chapter 2; three optional fields in
`doesnt-run.yml` (`expected`, `tried`, `tool-version`) and the matching
paragraph in `reporting.qmd`. Note: Homebrew's `gzip` was not installed
on the test Mac, so `man gzip` there is Apple's page for Apple's gzip;
with GNU gzip installed, its page in `$(brew --prefix)/share/man` should
come first (as `bash`'s does). Check on a Mac with the full Chapter 1
setup before §2 uses `man gzip`.

Also resolved earlier: AI section stays one short final section;
three faults in the broken script; help desks named by role, contacts
in Appendix A.

## Drafting notes (2026-11-17)

Written from this plan; every output in the chapter was re-captured in
a scratch copy of the project (pixi 0.84.2, seqkit 2.14.0, R 4.4.3,
macOS 15 Intel), paths shown as `/home/you`. Changes from the plan:

- **§4 "find the log" now uses Chapter 3's script.** Its current plan
  version tees stdout and stderr into one timestamped log per run, so
  the chapter shows the captured log of a run that failed with a moved
  R2 file (`FAILED open or read`, no `finished:` line, old results left
  in `results/`). Resolves open question 1, as long as Chapter 3 keeps
  that script and log name.
- **Captures differ slightly from the plan:** seqkit 2.14.0 prints a
  second, empty `[ERRO]` line on the truncated file, and on a terminal
  the `[ERRO]` lines come before the header line. `unknown flag`
  prints the usage on stderr and repeats `unknown flag: --paired` on
  stdout at the end. Both shown as captured.
- **Setup step added:** `mkdir -p ~/bioinf-ch04` at the end of §1;
  exercise 1's script is copied from the page (no download yet).
- **Exercise 2** answer adds that R2 has lower quality and more `N`s
  (`sum_n` 18,842 vs 280), from the `-a` capture.
- **Further reading:** picked Auslander 2026 over Smith et al. 2024
  (rule headings read; closer to the audience). Four entries added to
  `references.bib`; six misconceptions added to `misconceptions.yml`.

## Chapter review responses (2026-11-17)

Codex review of the written chapter (`reviews/chapter_04_codex_review.md`).
All three findings accepted; each rechecked first.

- **Model help request (medium).** Confirmed that `pixi run seqkit stats
  --paired` with no input fails the same way (exit 255). Exercise 3 now
  ends with that last cut: the 100-read file still fails, then the file
  is dropped altogether. The model request uses the input-free command,
  labels the message as abbreviated with the full output attached, gives
  the exit status, and says where the environment comes from (Chapter 2's
  setup files) instead of a private manifest path. The answer explains
  why the first draft failed its own test. `fig-good-request`'s *Small
  example* field now says the error needs no input file.
- **Methods "as printed" column (low).** Confirmed in the PMC HTML that
  both parameter strings join two options with no space
  (`–minimum-length=25–quality-cutoff=20`,
  `–star-output-genome-bam–forward-prob 0`). The column now keeps the
  paper's spacing, the caption says so, and the first discovery became
  "the dashes and the spaces".
- **Cluster help route (low, publication dependency).** `tbl-where-to-ask`
  now links SCINet's VRSC contact page and ISU Research IT's contact page
  directly, alongside Appendix A. Appendix A itself still needs its
  support section before release (same item as the Chapter 1 and 2
  reviews).

## Open questions

1. **To check while drafting is reviewed:** WSL Ubuntu has `man` pages
   installed (no "minimized system" message); `man gzip` on a Mac with
   the full Chapter 1 setup opens GNU gzip's page (the test Mac had only
   Apple's gzip; `gzip --help` in the chapter was captured from
   conda-forge's GNU gzip 1.15); the R read error and the seqkit
   captures on Linux match macOS; recheck the seqkit exit-0 capture
   whenever `setup/pixi.lock` changes.
2. **Chapter 3 dependency:** §4 quotes Chapter 3's script name, log
   name pattern, and log lines. If Chapter 3's script changes, recapture
   the failed-run log.
3. **Homepage:** `index.qmd` still says only Chapters 1 and 2 are
   drafts; update it together with Chapter 3.
