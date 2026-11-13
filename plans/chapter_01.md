---
title: "Chapter 1 — Orientation: computers and where you compute"
subtitle: "Chapter plan · core · written (first draft)"
date: 2026-11-13
---

**Part:** I — Getting set up · **Label:** core · **Status:** first draft
written 2026-11-13 (`chapters/01-orientation.qmd`); reviewed before
writing by Codex and Antigravity

## From `PLAN_CHAPTERS.md`

- CPU, cores vs threads; RAM vs disk; I/O as the usual bottleneck
- Typical data sizes (FASTQ, BAM, VCF, count matrix)
- macOS, Windows, Linux; Linux distributions briefly
- Laptop vs HPC cluster vs cloud: what runs where
- Windows: WSL2; macOS: Terminal, Homebrew
- Getting an account on SCINet / a university cluster
- Guided first session: open a terminal, look at a small FASTQ file, save a
  one-line summary (commands explained in Part II)

## Outcome and check

- **Outcome:** readers can open a terminal on their own computer, download
  one small FASTQ file, check it, look at it, and save a one-line read
  count to a file. They can also say, for a given job, whether it belongs
  on a laptop, a cluster, or the cloud, and which resources (CPU, RAM,
  disk, I/O) it might need.
- **Check:** `cat fastq_summary.txt` prints exactly
  `SRR6357070_1 reads: 50000`. Each mate file of a test sample holds
  50,000 reads; the two files together are 50,000 read pairs (100,000
  reads). Verified 2026-11-13.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Open a terminal on your computer and run a command you were given.
2. Download a FASTQ file, check that it arrived intact, look at its first
   records, and count its reads.
3. Find how many logical CPUs, how much RAM, and how much free disk your
   computer has.
4. Estimate a file's size from its read count, and name the resources
   (CPU, RAM, disk, I/O) a job can be limited by.
5. Decide whether a job belongs on a laptop, a cluster, or the cloud.

## Sections

Short chapter: first successful command comes early (sections 2–3), then
brief concept sections that point forward. Each concept section opens with
something the reader runs or computes, then names the idea (examples
first). Visual items in brackets are specified under *Visuals and teaching
aids* below.

1. **What this chapter does.** Learning-goals callout. One paragraph: by
   the end you will have run your first commands on a real sequencing file.
   What a "bioinformatics computer" is: usually someone else's Linux
   machine you reach from your laptop.
2. **Opening a terminal.** First, three words in one short paragraph: the
   *operating system* (macOS, Windows, Linux), the *terminal* (the window),
   and the *shell* (the program inside it that runs your commands). Then an
   OS tabset (`macOS` / `Windows (WSL2)` / `Linux`, STYLE-GUIDE §6):
   - macOS: Terminal, then a one-time setup (15–30 min): install
     Homebrew; `brew install bash coreutils findutils gnu-sed gnu-tar grep
     gawk gzip`; make Homebrew's bash the login shell (`/etc/shells`,
     `chsh`); write `~/.bash_profile` that puts each tool's `gnubin` first
     on `PATH`; reopen Terminal and check `$BASH_VERSION` and
     `sed --version`. (Changed 2026-11-13: was "zsh, Homebrew not
     required".)
   - Windows: a setup branch that takes longer (install, restart, create a
     Linux account). The install command runs in PowerShell *as
     administrator*; everything after that runs in Ubuntu. When Ubuntu
     asks for a new password, nothing appears as you type; that is normal.
     Managed (university-owned) laptops may block the install: ask your IT
     office. One sentence that Git Bash exists but the book does not
     support it.
   - Linux: already there; the shell is usually bash.

   What the prompt is, and that code blocks in this book leave it out so
   copy-paste works. Every code block is labelled with where it runs
   (`Terminal (laptop)` for this whole chapter).
   [`tbl-terminal-by-os`; pitfall: WSL files under `/mnt/c`]
3. **Guided first session.** Copy-and-run in small steps, each with its
   expected output right beside it and a "you'll learn this in Part II"
   note: make a scratch folder, download one yeast FASTQ file with `curl`,
   check it arrived (size, `gzip -t`), peek at the first two records,
   count its lines (200,000), then count reads (200,000 / 4 = 50,000) and
   save the one-line summary. Showing the line count first means the
   nested summary command only adds the division. **Checkpoint:** if a
   step prints an error, stop there; a summary of `reads: 0` means the
   file is missing or broken, not empty. Then the annotated FASTQ record:
   *this* file has four lines per read (full format, including files that
   break that rule, in Chapter 15). Close by saying `~/bioinf-ch01` is a
   scratch folder; Chapter 3 starts the real project and brings this file
   and its source URL into it. [`fig-fastq-record`; self-check]
4. **Parts of a computer that matter for analysis.** *Start hands-on:*
   readers look up their own logical CPUs, RAM, and free disk and fill in
   the "your computer" column. *Then name the parts:*
   - CPU: physical cores vs logical CPUs (one core can appear as two);
     the commands report logical CPUs. A program's *threads* are pieces of
     work the system schedules onto CPUs; tools take an option for how
     many to use (`--threads`, `-t`, `-p`, depending on the tool). More
     threads help only if the tool is written to use them.
   - RAM vs disk: working space vs storage. A file's size on disk is not
     what a program needs in RAM: the section 3 count *streams* through
     the file a few lines at a time, while some tools (e.g., building a
     genome index, Chapter 31) hold a lot in memory at once.
   - I/O: reading and writing files. Often the limit for simple steps over
     big files; heavier steps (alignment) are often limited by CPU, and
     some by RAM. Diagnosing which is Chapters 10 and 35.

   Close with what it looks like when each resource runs out.
   [`tbl-my-computer`, `fig-computer-parts`, `fig-cores-threads`,
   `tbl-resource-limits`; key idea; misconception callout "more cores";
   self-check]
5. **How big is the data?** *Start with arithmetic on the reader's own
   file:* one mate file of 50,000 reads is 2.2 MB compressed (12.8 MB
   uncompressed). A mate file with 30 million reads is 600 × larger:
   about 1.3 GB compressed, 7.7 GB uncompressed; a paired sample has two
   such files. This scales *the same kind* of file only: read length,
   header style, and compression all change the result. Sizes are decimal
   (1 MB = 1,000,000 bytes); some tools print binary units (`ls -lh`
   shows this file as `2.1M` on macOS, `2.2M` on Linux/WSL). *Then the table and figure,* in two groups:
   - **Read-level files** (FASTQ, BAM) hold every read: GB per sample.
     A BAM is often about as large as its compressed FASTQ, sometimes
     larger, and sorting it needs temporary space on top.
   - **Summary files** (count matrix, results table, and for DNA studies a
     VCF) hold one row per gene or variant: MB or less, laptop-sized.

   Each size says what it covers (one mate file, one sample, whole study).
   [`tbl-data-sizes`, `fig-pipeline-file-sizes`; key idea; self-check]
6. **Why Linux.** Short, and not a repeat of §2: clusters and most
   bioinformatics tools run on Linux; distributions in two sentences
   (Ubuntu, Rocky/RHEL) as a background callout. Teach Linux; note macOS
   and Windows only where they differ. If it ends up repeating §2 while
   writing, merge it into §2.
7. **Where you compute: laptop, cluster, cloud.** Compact comparison table
   (cost, size, who manages it, what to run there). Login node vs compute
   node in one paragraph, with the cluster diagram; full treatment in
   Chapter 10. Cloud only as "exists, costs money, see Chapter 38".
   [`tbl-where-compute`, `fig-cluster-anatomy`; misconception callout
   "cluster = faster computer"; pitfall "heavy work on the login node";
   self-check sorting jobs into laptop / cluster / cloud]
8. **Getting a cluster account.** Brief: apply early, since approval can
   take days or weeks; ask your PI or research computing office. A tip
   callout naming SCINet (USDA-affiliated users) and university clusters
   (e.g., ISU Nova), linking to Appendix A, *Cluster sites: SCINet and
   Nova* (`@sec-cluster-sites`), shared with Chapters 9–10. No-cluster
   readers can continue.
9. **Summary, exercises, further reading.** Summary as 4–5 bullets that
   mirror the learning goals; exercises (below); annotated further reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2): our
data is `given` (blue) everywhere, including inside hardware diagrams;
hardware and infrastructure are neutral (`ink`, `line`, `muted`).

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-fastq-record` | 3 | static | The first real record from `SRR6357070_1` (sequence truncated), each of the 4 lines labelled: header (read ID, `/1` = read 1), bases, `+` separator, one quality character per base. Read lines `given`; `+` line `muted`. |
| `fig-computer-parts` | 4 | CSS-animated | CPU ↔ RAM ↔ disk ↔ network, with relative speeds as labels (order of magnitude only). Captioned as *one example*: an I/O-limited job, where blue data blocks crawl from disk to RAM and the CPU waits. Final frame = blocks at rest in RAM. |
| `fig-cores-threads` | 4 | static | Assumes 8 cores and a tool that scales well. Two panels: the tool run with 4 threads keeps 4 cores busy; a single-threaded step keeps 1 busy while 7 sit idle. Busy cores hold `given` work; idle cores `muted`. |
| `fig-pipeline-file-sizes` | 5 | static | One sample down a pipeline: FASTQ → BAM → count matrix → results table, boxes sized on a log scale from *measured* values, each with its size and what it covers. Read-level files grouped on the left (BAM may be as large as FASTQ, or larger), summary files on the right. All `given`; reference (genome/GTF) enters as `ref`. |
| `fig-cluster-anatomy` | 7 | static | Laptop → SSH → login node; login node → scheduler queue → compute nodes (job submission). Shared storage is drawn as part of the cluster, connected to login and compute nodes by separate lines, so file data is not shown passing through the scheduler; the laptop reaches it only through the connection or file transfers. Labels "edit, submit" on the login node, "run" on compute nodes. Drawn so Chapters 9–10 can reuse it or turn it into a stepped figure. |

Not used here: Mermaid (no step-order diagram is needed), screenshots
(terminal windows differ too much by OS and version to be worth it).

### Interactive figure (Observable JS)

None (decided 2026-11-13). `tbl-data-sizes` and `fig-computer-parts`
carry the point; interactive figures are kept for chapters where moving an
input is the lesson.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-terminal-by-os` | 2 | OS · terminal app · default shell (zsh on macOS, bash on Ubuntu/WSL and most Linux) · supported in this book |
| `tbl-my-computer` | 4 | Resource · Linux/WSL command · macOS command · example output · *your value* (blank, readers fill in) |
| `tbl-resource-limits` | 4 | Resource · what runs out · what you see (e.g., RAM → job killed / `Killed` / out-of-memory; disk → `No space left on device`; CPU → slow, cores at 100%; I/O → slow, cores mostly idle) |
| `tbl-data-sizes` | 5 | Format · what it holds · read-level or summary · yeast test set (measured, and what it covers) · typical study (order of magnitude) |
| `tbl-where-compute` | 7 | Laptop · cluster · cloud, by cost, size, who manages it, what to run there |

`tbl-my-computer` commands (draft), as an OS tabset under the table:

| Resource | Linux / WSL | macOS | Note |
|:---------|:------------|:------|:-----|
| Logical CPUs | `nproc` | `sysctl -n hw.ncpu` | May be more than physical cores |
| RAM | `free -h` (the `total` column) | `echo "$(( $(sysctl -n hw.memsize) / 1000000000 )) GB"` | WSL sees only the memory given to its virtual machine (by default about half the laptop's RAM), not the full amount |
| Free disk | `df -h ~` | `df -h ~` | Read the `Avail` column; on macOS `Used` + `Avail` need not add up to `Size` |

`tbl-data-sizes`: VCF appears only in the typical-study column (the yeast
set is RNA-seq and has no VCF); the small VCF example stays in the formats
part.

### Code (§6)

- All commands run on the **laptop**, tier 2 style (shown, not run at
  render), but cheap enough that readers run every one.
- Blocks use `filename="Terminal (laptop)"`, establishing the label that
  later chapters vary (`Terminal (login node)`, `Terminal (compute
  node)`). No `$` prompt; code annotations (`# <1>` + numbered list) as in
  `example/code.qmd`. Output goes in a separate `.console` block with
  real captured output, directly after each step.
- OS tabsets (`group="os"`) in §2 (opening a terminal) and §4 (the
  `tbl-my-computer` commands).
- No compute notes needed: every step takes seconds.

### Plots

None. Nothing in this chapter is a measured quantity worth plotting; the
data-size comparison is a table plus `fig-pipeline-file-sizes`.

### Animation (manim)

None. Nothing here is a hard sequence of steps; `fig-computer-parts`
covers the one bit of motion with CSS. The first manim clip is more likely
in the algorithms tour (e.g., how a read is placed on a genome) or the
nf-core chapter.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Pitfall | WSL: keep work in your Linux home (`~`), not under `/mnt/c/…`; Windows folders are slow from Linux and invite line-ending and permission problems |
| 3 | Tip | Paste into a terminal: `Cmd-V` on macOS, `Ctrl-Shift-V` in most Linux/WSL terminals; `Ctrl-C` stops a command, it does not copy |
| 3 | Pitfall | If any step prints an error, stop and fix it before going on; a summary of `reads: 0` means the download failed |
| 4 | Key idea | A job can be limited by CPU, RAM, disk space, or I/O; extra cores help only when the work can use them |
| 4 | Misconception | "More cores always makes it faster" |
| 5 | Key idea | Read-level files (FASTQ, BAM) are large; summary files (count matrices, results tables) are usually far smaller. Intermediate and temporary files raise the peak disk space a pipeline needs |
| 6 | Background | Linux distributions (Ubuntu, Rocky/RHEL): same commands, different installers |
| 7 | Misconception | "The cluster is just a faster computer" |
| 7 | Pitfall | Heavy work on the login node slows it for everyone and may get your job killed |
| 8 | Tip | Apply for a cluster account now; approval can take weeks |

Section 3 has two callouts plus a figure; keep them on separate screens
(tip near the first command, pitfall at the checkpoint).

"I can run my analysis on the login node" gets the §7 pitfall callout.
Misconceptions with no callout ("RAM and disk are the same", "I need to
learn the commands first", "Windows needs a separate Linux computer") are
handled in the text, in `tbl-resource-limits`, or as self-check probes.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §3: This FASTQ file has 200,000 lines. How many reads? (*50,000; this
  file has four lines per read.*)
- §4: A step uses one core at 100% while seven sit idle. Will adding
  `--threads 8` help? (*Only if the tool supports threads; many steps
  don't, and some are limited by disk or memory, not CPU.*)
- §5: Our mate file holds 50,000 reads in 2.2 MB. About how large is a
  mate file of the same kind with 30 million reads? (*About 1.3 GB
  compressed; a paired sample has two.*)
- §7: Laptop, cluster, or cloud? Editing a script; aligning 48 samples;
  running DESeq2 on this book's small yeast count matrix; a one-off job
  needing 2 TB of RAM that your cluster lacks. (*Laptop; cluster compute
  nodes; laptop; cloud is one option if funding allows, or another shared
  facility that has such nodes.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
commands):

1. Download the matching read-2 file and add its count as a second line
   of `fastq_summary.txt`. Supplied: the R2 URL and the summary command
   with `>>` instead of `>`, with one sentence: `>` replaces a file, `>>`
   adds to it (Chapter 6). Do both files have the same count, and why
   should they? (*Answer notes that equal counts are expected for a pair,
   but do not by themselves prove the pairs match; Chapter 15.*)
2. Fill in your column of `tbl-my-computer`. Would an uncompressed
   30-million-read mate file (about 7.7 GB) fit in your RAM *if a program
   loaded it all at once*, leaving room for the system and other programs?
   (*Answer: the section 3 count never loads it; it streams. Some tools do
   need that much memory, which is one reason to use a cluster.*)
3. Run the supplied `time gunzip -c SRR6357070_1.fastq.gz | wc -l`. Find
   the elapsed time (`real` in bash, `total` in zsh). Make a rough
   estimate for a 30-million-read mate file (600 × larger), then name two
   reasons the real time could differ. (*Answer: start-up time and file
   caching dominate a file this small; a big file may come from a slower
   disk or a network filesystem. Measuring what limits a job is Chapters
   10 and 35.*)

## Examples and data

- Toy example: one FASTQ record drawn and labelled (4 lines), small
  enough to read by eye. Use the real first record of `SRR6357070_1`, so
  the figure matches what readers see on screen.
- Running dataset (yeast nf-core/rnaseq test data): one read-1 file from
  one sample, verified 2026-11-13:
  - URL: `https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz`
    (R2: same path with `_2`).
  - 2.2 MB compressed (2,239,317 bytes), 12.8 MB uncompressed, 50,000
    reads of 101 bases. R2 also 50,000 reads, IDs in the same order
    (checked by the Codex review).
  - Last commit touching the file on the `rnaseq` branch: `58ec9dc`
    (2021-04-12). SHA-256 of R1:
    `3f50541fa9cf2bedc87e7b682ada0fccfdfcd6d27b9bb81f17be230ff140ebe7`.
    Both are recorded in `data/README.md` with source, accession, license,
    and citation, so a changed file is caught. Chapter 3 teaches checksums;
    Chapter 1 adds no command for it.
  - Browser fallback, only if `curl` is blocked (e.g., by a firewall):
    the file's GitHub page and its download button, then one supplied
    command to move it into place: `mv ~/Downloads/SRR6357070_1.fastq.gz
    ~/bioinf-ch01/` (macOS/Linux) or `cp
    /mnt/c/Users/<your-windows-name>/Downloads/SRR6357070_1.fastq.gz
    ~/bioinf-ch01/` (WSL).
- Draft command sequence (laptop), each step with its expected output:

  ```bash
  mkdir -p ~/bioinf-ch01 && cd ~/bioinf-ch01
  curl -fLO https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
  ls -lh SRR6357070_1.fastq.gz                    # 2.1M (macOS) or 2.2M (Linux/WSL)
  gzip -t SRR6357070_1.fastq.gz                   # prints nothing if the file is intact
  gunzip -c SRR6357070_1.fastq.gz | head -n 8     # first two records
  gunzip -c SRR6357070_1.fastq.gz | wc -l         # 200000
  echo "SRR6357070_1 reads: $(( $(gunzip -c SRR6357070_1.fastq.gz | wc -l) / 4 ))" > fastq_summary.txt
  cat fastq_summary.txt                           # SRR6357070_1 reads: 50000
  ```

  (In the chapter, the comments become code annotations and `.console`
  blocks.) `-f` makes `curl` fail on an HTTP error instead of saving the
  error page under the file name. Without it, and with a missing file, the
  summary line still runs: it prints a `gunzip` error, writes
  `reads: 0`, and exits successfully (both checked 2026-11-13). Full
  error handling waits for Chapter 8.

  Use `gunzip -c`, not `zcat`: on macOS, `zcat file.gz` looks for
  `file.gz.Z` and fails (checked 2026-11-13). Not explained in the text
  beyond "works the same everywhere".

  First record, captured 2026-11-13 (for the `.console` block and
  `fig-fastq-record`):

  ```
  @SRR6357070.25017281 25017281/1 kraken:taxid|4932
  CCTGAATCGAGAAGGAGGTGTCCAGGGAGTTCATCATCAGAATGATTAGTATGATTTACTGTAGATTCAGTAAGTTTCTGGCCTAAGATGAAGGTCGTGCT
  +
  BBBBBFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFBFFFFFFF
  ```

  The header's `kraken:taxid|4932` (the NCBI taxon ID for
  *S. cerevisiae*) is left for Chapter 15; the figure labels only the read
  ID and `/1`.
- Where commands run (laptop / login node / compute node): all laptop.
  A short note that the same commands work on a login node later, and that
  heavy work never runs there (Chapter 10).

## Misconceptions

Each has an entry in the book's `misconceptions.yml` (id, claim,
reality, probe, chapters), created 2026-11-13. Where it is handled
in this chapter is in brackets.

- `more-cores-faster`: "More cores always makes it faster." Only tools
  written for threads gain, and only until disk, memory, or I/O becomes
  the limit. [callout, §4]
- `cluster-faster-computer`: "The cluster is just a faster computer." It
  is many computers shared by many people; you request resources and wait
  in a queue. [callout, §7]
- `run-on-login-node`: "I can run my analysis on the login node." Login
  nodes are for editing and submitting jobs. [pitfall, §7; head-on in
  Chapter 10]
- `ram-is-disk`: "RAM and disk/storage are the same thing." Running out
  of each fails differently (killed job vs full disk), and file size is
  not the RAM a program needs. [`tbl-resource-limits`, §4; exercise 2]
- `learn-commands-first`: "I need to learn the commands before I can try
  anything." The first session works by copying; understanding comes in
  Part II. [text, §3]
- `windows-needs-linux-pc`: "Windows users need a separate Linux
  computer." WSL2 gives a real Linux environment on Windows. [text, §2]

## Links to other chapters and books

- Builds on: nothing (first chapter)
- Leads to: Chapter 2 (book setup and editors); Chapter 3 (the recurring
  project takes in this chapter's file, source URL, and summary); Part II
  (shell; Chapter 6 for `>` and `>>`, Chapter 8 for error handling);
  Chapter 9 (SSH) and Chapter 10 (HPC and SLURM) for the cluster;
  Chapter 15 (FASTA and FASTQ, paired files); Chapter 31 (genome indexing
  and memory); Chapter 35 (performance) and Chapter 38 (cloud) for depth on
  resources.

## Official links to include

- WSL install: learn.microsoft.com/windows/wsl/install; WSL memory and CPU
  limits: learn.microsoft.com/windows/wsl/wsl-config
- Homebrew: brew.sh
- Ubuntu: ubuntu.com; Rocky Linux: rockylinux.org
- nf-core test datasets: github.com/nf-core/test-datasets (`rnaseq`
  branch); GEO accession GSE110004 at ncbi.nlm.nih.gov/geo
- SCINet: scinet.usda.gov; ISU research computing: the site's own docs
- `curl`: curl.se (manual, for `--fail`)
- `samtools sort`: htslib.org (temporary files), if section 5 mentions it

## Further reading (candidates)

Final list: 3–6 annotated picks, each cited by key so it lands on the
References page (STYLE-GUIDE §9). Verify with scite / fetch BibTeX from
the DOI; items with no DOI get `url` + `urldate`.

- Shotts, *The Linux Command Line*: opening chapters, for what a shell and
  terminal are.
- Software Carpentry, *The Unix Shell*: introduction episode, as a second
  explanation.
- Microsoft WSL install documentation: the current official steps.
- SCINet "Getting started" / account request pages, and ISU research
  computing docs: site-specific account steps.
- (Optional) A short open article on computing for biologists, e.g. "Ten
  simple rules" style; find and verify with scite before adding.

## Austin's notes

-

## Decisions (2026-11-13)

- FASTQ download: one `curl` command, with a browser download link as a
  fallback.
- Order: guided first session right after opening a terminal; concept
  sections follow.
- Data-size table: measured sizes for the yeast test set plus rough
  orders of magnitude for a typical study.
- Cluster accounts: brief in Chapter 1; step-by-step SCINet/Nova details
  in a site-specific appendix shared with Chapters 9–10.
- Windows: WSL2 with Ubuntu; Git Bash noted in one sentence as
  unsupported.

## Decisions (2026-11-13, open questions round)

- OS differences: OS tabsets (`group="os"`) where steps really differ;
  rule added to STYLE-GUIDE §6 with a demo in `example/code.qmd`.
- No interactive figure in Chapter 1 (`fig-read-time` dropped).
- `misconceptions.yml` (with the six Chapter 1 entries) and `figures/`
  created now; recorded in the book's `CLAUDE.md`.
- Site-specific appendix confirmed: Appendix A, *Cluster sites: SCINet
  and Nova* (`appendices/a-cluster-sites.qmd`, stub), shared by
  Chapters 1, 9, and 10.

## Decisions (2026-11-13, outside reviews)

Applied from `chapter_01_codex_review.md` and `chapter_01_agy_review.md`.
Not taken: estimated BAM and count-matrix sizes (agy) are left unfilled
until measured; the claim "100× to 10,000× smaller" (agy) is not used
without measured values; VCF stays in the size table as a typical-study
row (Codex suggested dropping it), because `PLAN_CHAPTERS.md` lists it.

- Data sizes: two groups (read-level vs summary), no claim that every
  step shrinks the data; figure renamed `fig-pipeline-file-sizes`.
- Resources: logical CPUs vs physical cores vs threads; the key idea no
  longer says most work waits on I/O.
- Reads vs read pairs and decimal vs binary units stated explicitly.
- First session: `curl -f`, a size and `gzip -t` check, the line count
  shown before the summary, and a stop-on-error checkpoint.
- Code blocks labelled `Terminal (laptop)`.

## Decisions (2026-11-13, open questions round 2)

- Data license: `data/README.md` records both the MIT license of
  nf-core/test-datasets and the original GEO/SRA source (NCBI data-use
  policy), and cites Wu et al. 2018 (DOI verified with scite). Created
  with the commit ID and checksum.
- Run labels are a series rule: `Terminal (laptop)` / `(login node)` /
  `(compute node)` added to STYLE-GUIDE §6, with the demo in
  `example/code.qmd` updated.
- BAM and count-matrix sizes are measured when Chapter 1 is written, from
  the nf-core/rnaseq test run set up for the book anyway.

## Written (2026-11-13): what changed from the plan

- **Measured sizes.** Docker would not start here, so the nf-core/rnaseq
  test run was not repeated. Instead `scripts/ch01_file_sizes.R`
  downloads the sorted BAMs that nf-core stores with the test data (STAR
  output of nf-core/rnaseq), counts them with featureCounts (Rsubread),
  and runs DESeq2. Measured for sample `WT_REP2` (one paired run,
  SRR6357072): FASTQ R1 + R2 4.3 MB, BAM 3.3 MB; count matrix 2.8 kB
  (124 genes × 5 samples); results table 12.7 kB. `WT_REP2` rather than
  the reader's own sample, because `WT_REP1` combines two runs
  (SRR6357070 + SRR6357071). The test reference is yeast chromosome I
  only, which the table caption says. Inputs and checksums are in
  `data/README.md`.
- **`fig-pipeline-file-sizes`** is drawn as bars on a log axis (1 kB to
  10 MB), from the measured values.
- **`tbl-my-computer`** columns: Resource · command (Linux/WSL) · what to
  read · example output · your value. The macOS commands moved to the OS
  tabset below the table: the long macOS RAM command wrapped badly in a
  table cell.
- **Further reading:** Shotts (TLCL, 7th Internet Edition, 25.12),
  Software Carpentry *The Unix Shell* (Zenodo DOI, June 2019 release),
  Microsoft's WSL install page, Wu et al. 2018. DOIs verified with scite;
  BibTeX fetched from the DOI. The SCINet and ISU pages are linked in the
  text instead of being cited.
- `SRR6357070_2.fastq.gz` (exercise 1) added to `data/README.md`:
  50,000 reads, SHA-256 recorded.

## Decisions (2026-11-13, after first draft)

- **Bash everywhere** (Austin): no zsh variants anywhere in the book. The
  macOS tab now installs Homebrew, GNU bash and the GNU tools, and makes
  bash the login shell. With GNU tools on the Mac, outputs are the same on
  every system: `ls -lh` shows `2.2M`, `wc -l` prints no leading spaces,
  `nproc` works on macOS, and `time` prints `real`. Recorded in the book's
  `CLAUDE.md` under Decided. The setup was tested in an empty home folder
  with Homebrew's bash 5.3 on macOS 15 (Intel).
- **Cluster readers** (Austin): a pitfall box before step 1 of the guided
  session: never on the login node; `srun --cpus-per-task=1 --mem=4G
  --time=01:00:00 --pty bash -l` first (options checked against the SLURM
  srun docs), `hostname` to check, `exit` after; site options (`-A`, `-p`)
  in Appendix A; some compute nodes have no internet. The §7 login-node
  pitfall and the top of the exercises point back to it.
- **iTerm2** (Austin): one optional paragraph at the end of the macOS tab
  (same bash either way; split panes, scrollback search, paste history;
  `brew install --cask iterm2`), linked to iterm2.com; never assumed.
  No screenshot: the official site shows it.
- Review fixes: RAM shown in GiB (the macOS command divides by 2^30, so a
  "64 GB" laptop shows 64, matching `free -h`); "compressing" removed from
  the examples of I/O-limited steps (gzip compression is usually limited by
  the CPU); FASTQ and BAM sizes in `tbl-data-sizes` marked as `WT_REP2`;
  "everything before Chapter 9" (not "up to").

## Open questions

- Austin to read the draft. The example outputs in the macOS tabs
  (16 CPUs, 68 GB, `df` line) come from Austin's Mac; replace them if you
  would rather show a more typical laptop.
