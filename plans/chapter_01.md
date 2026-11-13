---
title: "Chapter 1 — Orientation: computers and where you compute"
subtitle: "Chapter plan · core · draft"
date: 2026-11-13
---

**Part:** I — Getting set up · **Label:** core · **Status:** draft, not yet
reviewed

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
  one small FASTQ file, look at it, and save a one-line read count to a
  file. They can also say, for a given job, whether it belongs on a laptop,
  a cluster, or the cloud, and which resource (CPU, RAM, disk, I/O) is
  likely to limit it.
- **Check:** `cat fastq_summary.txt` prints exactly
  `SRR6357070_1 reads: 50000` (each test sample has 50,000 reads; verified
  2026-11-13).

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Open a terminal on your computer and run a command you were given.
2. Download a FASTQ file, look at its first records, and count its reads.
3. Find how many cores, how much RAM, and how much free disk your
   computer has.
4. Estimate a file's size from its read count, and say which resource
   (CPU, RAM, disk, I/O) is likely to limit a job.
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
2. **Opening a terminal.** OS tabset (`macOS` / `Windows (WSL2)` /
   `Linux`, STYLE-GUIDE §6) so each reader sees only their steps. macOS: Terminal (Homebrew mentioned, not
   required, since pixi in Chapter 2 covers installs). Windows: install
   WSL2 with Ubuntu and work inside it; one sentence that Git Bash exists
   but the book does not support it. Linux: already there. What the prompt
   is, and that code blocks in this book leave it out so copy-paste works.
   [`tbl-terminal-by-os`; pitfall: WSL files under `/mnt/c`]
3. **Guided first session.** Copy-and-run, with "you'll learn this in
   Part II" notes: make a folder, download one yeast FASTQ file with one
   `curl` command (browser download link as a fallback), peek at the first
   two records, count reads, save a one-line summary. Each command is
   explained with code annotations, and the real output is shown in a
   `.console` block so readers can compare. Then the annotated FASTQ record
   (full format in Chapter 15). [`fig-fastq-record`; self-check]
4. **Parts of a computer that matter for analysis.** *Start hands-on:*
   readers run `time` on the read count from section 3, then look up their
   own cores, RAM, and free disk and fill in the "your computer" column.
   *Then name the parts:* CPU, cores vs threads (and why tools ask for
   `--threads`); RAM vs disk (working space vs storage); I/O (reading and
   writing files) as the usual bottleneck. Close with what it looks like
   when each resource runs out. [`tbl-my-computer`, `fig-computer-parts`,
   `fig-cores-threads`, `tbl-resource-limits`; key idea; misconception
   callout "more cores"; self-check]
5. **How big is the data?** *Start with arithmetic on the reader's own
   file:* 50,000 reads → 2.2 MB compressed (12.8 MB uncompressed), so a
   25-million-read sample is about 500 × larger, roughly 1.1 GB. *Then the
   table:* FASTQ, BAM, VCF, and count matrix, measured sizes for our yeast
   test set beside rough orders of magnitude (MB / GB / TB) for a typical
   study, with a note that sizes vary. Takeaway: raw reads are large,
   results get smaller down a pipeline. [`tbl-data-sizes`,
   `fig-data-shrinks`; key idea; self-check]
6. **Operating systems.** macOS, Windows, Linux; why clusters run Linux;
   distributions in two sentences (Ubuntu, Rocky/RHEL) as a background
   callout. Teach Linux; note macOS and Windows only where they differ.
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
   Nova* (`@sec-cluster-sites`), shared with Chapters 9–10. No-cluster readers can continue.
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
| `fig-computer-parts` | 4 | CSS-animated | CPU ↔ RAM ↔ disk ↔ network, with relative speeds as labels (order of magnitude only). Blue data blocks flow from disk to RAM to CPU, slowly on the disk/network leg and quickly on the RAM ↔ CPU leg, so the bottleneck is visible. Final frame = blocks at rest in RAM. |
| `fig-cores-threads` | 4 | static | Two panels: a tool run with `--threads 4` keeps 4 of 8 cores busy; a single-threaded step keeps 1 busy while 7 sit idle. Busy cores hold `given` work; idle cores `muted`. |
| `fig-data-shrinks` | 5 | static | One sample down a pipeline: FASTQ → BAM → count matrix → results table, boxes sized on a log scale with the size written in each. All `given`, because the data only gets re-organised; reference (genome/GTF) enters as `ref`. |
| `fig-cluster-anatomy` | 7 | static | Laptop → SSH → login node → scheduler queue → compute nodes, all sharing one storage system. Labels "edit, submit" on the login node, "run" on compute nodes. Drawn so Chapters 9–10 can reuse it or turn it into a stepped figure. |

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
| `tbl-terminal-by-os` | 2 | OS · terminal app · shell you get · supported in this book |
| `tbl-my-computer` | 4 | Resource · Linux/WSL command · macOS command · example output · *your value* (blank, readers fill in) |
| `tbl-resource-limits` | 4 | Resource · what runs out · what you see (e.g., RAM → job killed / `Killed` / out-of-memory; disk → `No space left on device`; CPU → slow, cores at 100%; I/O → slow, cores mostly idle) |
| `tbl-data-sizes` | 5 | Format · what it holds · yeast test set (measured) · typical study (order of magnitude) |
| `tbl-where-compute` | 7 | Laptop · cluster · cloud, by cost, size, who manages it, what to run there |

`tbl-my-computer` commands (draft): cores `nproc` / `sysctl -n hw.ncpu`;
RAM `free -h` / `sysctl -n hw.memsize`; free disk `df -h ~` on both.

### Code (§6)

- All commands run on the **laptop**, tier 2 style (shown, not run at
  render), but cheap enough that readers run every one.
- OS tabsets (`group="os"`) in §2 (opening a terminal) and §4 (the
  `tbl-my-computer` commands, as runnable blocks under the table).
- Blocks use `filename="Terminal"`, no `$` prompt, and code annotations
  (`# <1>` + numbered list) to explain each command, as in
  `example/code.qmd`. Output goes in a separate `.console` block with
  real captured output (first record shown below).
- No compute notes needed: every step takes seconds.

### Plots

None. Nothing in this chapter is a measured quantity worth plotting; the
data-size comparison is a table plus `fig-data-shrinks`.

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
| 4 | Key idea | Most analysis waits on reading and writing files, not on the CPU |
| 4 | Misconception | "More cores always makes it faster" |
| 5 | Key idea | Raw reads are the biggest files you will handle; every later step makes the data smaller |
| 6 | Background | Linux distributions (Ubuntu, Rocky/RHEL): same commands, different installers |
| 7 | Misconception | "The cluster is just a faster computer" |
| 7 | Pitfall | Heavy work on the login node slows it for everyone and may get your job killed |
| 8 | Tip | Apply for a cluster account now; approval can take weeks |

Misconceptions not given a callout ("RAM and disk are the same", "I need
to learn the commands first", "Windows needs a separate Linux computer",
"I can run my analysis on the login node") are handled in the text, in
`tbl-resource-limits`, or as self-check probes.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §3: A FASTQ file has 200,000 lines. How many reads? (*50,000; four lines
  per read.*)
- §4: A step uses one core at 100% while seven sit idle. Will adding
  `--threads 8` help? (*Only if the tool supports threads; many steps
  don't, and some are limited by disk, not CPU.*)
- §5: Our file holds 50,000 reads in 2.2 MB. About how large is a
  30-million-read sample? (*About 1.3 GB.*)
- §7: Laptop, cluster, or cloud? Editing a script; aligning 48 samples;
  running DESeq2 on a finished count matrix; a one-off job needing 2 TB
  RAM that your cluster lacks. (*Laptop; cluster compute nodes; laptop;
  cloud.*)

End-of-chapter exercises (core chapter, so required):

1. Download the matching read-2 file (`SRR6357070_2.fastq.gz`), count its
   reads, and append a second line to `fastq_summary.txt`. Do both files
   have the same count, and why should they?
2. Fill in your column of `tbl-my-computer`. Could your laptop hold one
   uncompressed 30-million-read FASTQ in RAM?
3. Time the read count on the compressed file (`time` in front of the
   command). Scale it up: about how long would the same count take on a
   30-million-read sample, 600 times larger? Which resource is your
   computer waiting on?

## Examples and data

- Toy example: one FASTQ record drawn and labelled (4 lines), small
  enough to read by eye. Use the real first record of `SRR6357070_1`, so
  the figure matches what readers see on screen.
- Running dataset (yeast nf-core/rnaseq test data): one read-1 file from
  one sample, verified 2026-11-13:
  - URL: `https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz`
  - 2.2 MB compressed (2,239,317 bytes), 12.8 MB uncompressed, 50,000
    reads of 101 bases.
  - Browser fallback: the same file's page on GitHub, with its download
    button.
- Draft command sequence (laptop):

  ```bash
  mkdir -p ~/bioinf-ch01 && cd ~/bioinf-ch01
  curl -LO https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
  gunzip -c SRR6357070_1.fastq.gz | head -n 8
  echo "SRR6357070_1 reads: $(( $(gunzip -c SRR6357070_1.fastq.gz | wc -l) / 4 ))" > fastq_summary.txt
  cat fastq_summary.txt
  ```

  Use `gunzip -c`, not `zcat`, because macOS `zcat` does not read `.gz`.
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

- `more-cores-faster`: "More cores always makes it faster." Often disk or
  I/O is the limit, and many steps use one core. [callout, §4]
- `cluster-faster-computer`: "The cluster is just a faster computer." It
  is many computers shared by many people; you request resources and wait
  in a queue. [callout, §7]
- `run-on-login-node`: "I can run my analysis on the login node." Login
  nodes are for editing and submitting jobs. [pitfall, §7; head-on in
  Chapter 10]
- `ram-is-disk`: "RAM and disk/storage are the same thing." Running out
  of each fails differently (killed job vs full disk).
  [`tbl-resource-limits`, §4]
- `learn-commands-first`: "I need to learn the commands before I can try
  anything." The first session works by copying; understanding comes in
  Part II. [text, §3]
- `windows-needs-linux-pc`: "Windows users need a separate Linux
  computer." WSL2 gives a real Linux environment on Windows. [text, §2]

## Links to other chapters and books

- Builds on: nothing (first chapter)
- Leads to: Chapter 2 (book setup and editors); Part II (shell); Chapter 9
  (SSH) and Chapter 10 (HPC and SLURM) for the cluster; Chapter 15 (FASTA
  and FASTQ); Chapter 35 (performance) and Chapter 38 (cloud) for depth on
  resources.

## Official links to include

- WSL install: learn.microsoft.com (WSL documentation)
- Homebrew: brew.sh
- Ubuntu: ubuntu.com; Rocky Linux: rockylinux.org
- nf-core test datasets: github.com/nf-core/test-datasets (`rnaseq`
  branch); GEO accession GSE110004 at ncbi.nlm.nih.gov/geo
- SCINet: scinet.usda.gov; ISU research computing: the site's own docs
- `curl`: curl.se

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

## Open questions

- Measured BAM, VCF, and count-matrix sizes for the yeast test set: take
  them from an nf-core/rnaseq test run (BAM, counts) and the small VCF
  file used in the formats part; fill in when writing.
