---
title: "Chapter 3 — Organizing projects and data"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** I — Getting set up · **Label:** core · **Status:** draft for
review (2026-11-17). Commands marked *checked* were run on 2026-11-17
(macOS 15 Intel, GNU coreutils 9.11 from Homebrew); the rest are to be
checked while drafting.

## From `PLAN_CHAPTERS.md`

- Project folder structure (`src/`, `data/`, `results/`, …)
- File and script naming (`00_`, `01_`, …; no spaces)
- Raw data is read-only; link shared lab data and references into a
  project (symlinks) rather than copying them
- Checksums (`md5sum`) for raw data
- Backups (3-2-1); scratch is not a backup
- Sample sheets and metadata as first-class files
- Provenance: link each output to input accessions/checksums, reference
  release, software or pipeline version, parameters, and logs
- READMEs and a lab-notebook habit
- FAIR principles (brief)
- Start the recurring project

## Promises this chapter must keep

From the written Chapters 1 and 2 (check the wording again when drafting):

- Chapter 1 (§3): "`~/bioinf-ch01` is a scratch folder … this chapter
  starts the book's real project and brings this file, **and the address
  you downloaded it from**, into it."
- Chapter 2 (§2): "`~/bioinf-book` is the book's project folder from now
  on … this chapter organizes it." It already holds `pixi.toml`,
  `pixi.lock`, `.pixi/`, and `README.md` (Chapter 2 exercise 3).
- Chapter 2 plan: `pixi.toml` stays at the project root for the whole
  book, so the recurring project **is** `~/bioinf-book`.
- `PLAN_CHAPTERS.md` conventions: the recurring project collects input
  provenance, metadata, scripts or workflow config, environment info,
  logs, and a rendered summary as skills appear. This chapter starts the
  first five; the rendered summary waits for Chapter 12 (Quarto).

## Outcome and check

- **Outcome:** readers turn `~/bioinf-book` into an organized project:
  raw reads moved in from Chapter 1, verified with checksums, and made
  read-only; a shared reference linked in, not copied; the sample sheet
  saved as a file; a supplied numbered script run to produce a result
  with a log; and a README, a data record, and a notebook entry that say
  where every file came from. They can also say which of their storage
  locations are backed up.
- **Check:** three commands from `~/bioinf-book`:

  ```bash
  md5sum -c data/raw/checksums.md5     # SRR6357070_1.fastq.gz: OK
                                       # SRR6357070_2.fastq.gz: OK
  ls -l data/ref                       # data/ref -> /home/you/bioinf-shared/…
  pixi run bash src/01_count_reads.sh && cat results/read_counts.tsv
                                       # num_seqs 50000 for both files
  ```

  MD5 values *checked* 2026-11-17 (SHA-256 matches `data/README.md`):

  ```
  d19f3c7a8b4016fa641458257b99a1a1  SRR6357070_1.fastq.gz
  d126cc66ed169f69af2c07da0dd73e02  SRR6357070_2.fastq.gz
  ```

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Lay out a project folder that keeps raw data, reference, metadata,
   code, results, and logs apart, and name files so they sort and never
   need quoting.
2. Verify downloaded files with checksums, and protect raw data from
   being changed or deleted by accident.
3. Link shared data into a project with a symbolic link, and say what
   deleting the link does and does not remove.
4. Record where every input and output came from (source, version,
   checksum, script, software version, log) in files kept in the project.
5. Say which of your storage locations are backed up, and what a 3-2-1
   backup means for your raw data.

## Sections

Same pattern as Chapters 1–2: each section opens with something readers
run or look at, then names the idea. The hands-on thread is one project
built step by step in `~/bioinf-book`; each section adds one piece, so
the folder at the end of the chapter is the starting point for every
later chapter. Commands are copy-and-run; `mkdir`, `mv`, `ln -s`,
`chmod` and the rest are explained in Part II (Chapters 5–7), as in
Chapter 1. Visual items in brackets are specified under *Visuals and
teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph: a
   month from now, you (or your PI, or a reviewer) will ask "which file
   is this, where did it come from, and how was this number made?"; this
   chapter sets up the folder and the habits that answer that without
   memory. Chapter 2's `~/bioinf-book` becomes the book's project.
2. **A folder for each project.** *Start hands-on:* one `mkdir -p` that
   creates the layout inside `~/bioinf-book`, then `ls` to see it beside
   `pixi.toml`. *Then name the parts* with the layout figure and table:

   ```
   ~/bioinf-book/
   ├── README.md          what this project is; how to rerun it
   ├── NOTEBOOK.md        dated log of what you did and why
   ├── pixi.toml  pixi.lock  .pixi/   software (Chapter 2)
   ├── data/
   │   ├── README.md      where every input came from (provenance)
   │   ├── raw/           reads as received: read-only, never edited
   │   ├── meta/          sample sheet and sample metadata
   │   └── ref  ->  (link to a shared reference)
   ├── src/               numbered scripts: 01_…, 02_…
   ├── results/           everything the scripts make; can be deleted
   └── logs/              what each run printed
   ```

   Rules, one sentence each: one project, one folder; inputs, code, and
   outputs in separate folders; anything in `results/` can be rebuilt
   from `data/` + `src/` + the environment, so it is the one folder you
   may delete; paths in scripts are relative to the project root, so the
   folder can move (laptop → cluster) without edits. Name it as one
   reasonable layout among several (Noble 2009; Wilson et al. 2017), not
   the only right one; nf-core and Chapter 25 add `work/` later.
   *On a cluster* (short paragraph): the project lives in project
   storage (`/project` on SCINet, `/work` on Nova), not home (small
   quota) or scratch (purged); same layout. Large intermediate files
   may go to scratch, with only final results kept in the project
   (Chapters 10, 26). [`fig-project-layout`, `tbl-project-folders`;
   key idea; self-check]
3. **Names that work.** *Start with a sorting puzzle:* `ls` on a supplied
   set of names (`final.txt`, `final_v2.txt`, `Final FINAL (2).txt`,
   `run10.sh`, `run2.sh`, `11-3-25 counts.csv`) shows them in an order
   no one wants. Then the rules, with the fixed version beside each:
   - no spaces or special characters (use `_` or `-`); spaces break
     commands unless quoted (quoting in Chapter 5);
   - lowercase, or one consistent case (macOS and Windows folders are
     usually case-insensitive, Linux clusters are case-sensitive, so
     `Data.csv` and `data.csv` are one file on a laptop and two on the
     cluster);
   - dates as `YYYY-MM-DD` (ISO 8601), so they sort in time order;
   - numbers zero-padded and scripts numbered in run order (`01_`, `02_`,
     … ; `00_` for one-time setup such as downloads), so `ls` shows the
     pipeline in order;
   - say what is in the file, and keep the extension true (`.tsv` means
     tabs, `.gz` means compressed);
   - no `final`/`v2`: versions live in git (Chapter 21) and dates.

   Sample IDs from the sequencing facility are kept as given (`SRR…`,
   `WT_REP1`) so they still match the sample sheet; rename only your own
   files. [`tbl-file-names`; self-check]
4. **Raw data: move it in, check it, lock it.** *Start hands-on:* move
   (not copy) both FASTQ files from `~/bioinf-ch01/` into `data/raw/`
   (recovery: if `~/bioinf-ch01` is gone, two supplied `curl -fLO`
   commands download them straight into `data/raw/`). Create
   `data/raw/checksums.md5` from the two lines the book supplies (in VS
   Code or nano: Chapter 2's editors), then `md5sum -c` → two `OK`.
   *Then name the idea:* a checksum is a short fingerprint computed from
   every byte; one changed byte gives a different value. Sequencing
   facilities and ENA supply MD5 values; run `md5sum -c` after every
   download or transfer (Chapter 9 reuses it after `rsync`). `md5sum`
   and `sha256sum` work the same way; SHA-256 is the stronger one and is
   what the book's own `data/README.md` records; MD5 is enough to catch
   damaged transfers, which is the job here. *Then lock it:* `chmod a-w`
   on the files **and** on `data/raw/` itself; show that appending to a
   file and deleting it both fail. Why the folder too: a read-only file
   in a writable folder can still be deleted by `rm` (*checked*: `rm`
   removed a read-only file without asking when not run interactively).
   Unlocking when you really must add a file: `chmod u+w data/raw`, add,
   lock again. Permissions are explained in Chapter 7. A one-line note:
   raw reads stay compressed; never unzip them in place.
   [`fig-checksum`; key idea; misconception callout
   `checksum-proves-correct`; self-check]
5. **Shared data: link, don't copy.** *Start hands-on:* make a stand-in
   for a lab's shared folder, `~/bioinf-shared/references/yeast_R64-1-1_test/`,
   download the test genome (`genome.fa.gz`, 71 kB) and annotation
   (`genes.gtf.gz`, 10 kB) into it with `curl -fLO`, and give it a
   short README (source, commit, date). Then
   `ln -s ~/bioinf-shared/references/yeast_R64-1-1_test data/ref`,
   `ls -l data/ref` (the arrow), and `ls data/ref/` (the files, seen
   through the link). *Then name the idea:* a symbolic link is a
   signpost to a path, not a copy. Why: references and big shared
   datasets exist once on a cluster (`/project/<lab>/…`), every project
   points at them, and no one's quota pays twice. Absolute paths for
   links to shared data (the link keeps working if the project moves);
   a moved or renamed target leaves a broken link (`ls -l` shows it, in
   red in many terminals). On a real cluster readers link the lab's or
   the site's copy instead of downloading (Appendix A for site
   reference collections, if any).
   **Pitfall (*checked* on macOS with GNU `rm`; recheck on Linux/WSL):**
   `rm data/ref` removes only the link; `rm -r data/ref/`, **with a
   trailing slash**, follows the link and deleted the shared folder
   itself. Tab completion adds that slash. Rule: remove a link with
   `rm` and no slash (or `unlink`). Reference versions (assembly vs
   release, chromosome names) are Chapter 15; here, the folder name and
   README record which release it is. [`fig-symlink`; pitfall;
   misconception callout `symlink-is-copy`; self-check]
6. **Backups: where do your files really live?** *Start with a
   table readers fill in:* for each place they keep files (laptop disk,
   cloud sync folder, cluster home, project, scratch, lab archive), is
   it backed up, and by whom? (Answers for SCINet and Nova come from the
   sites' docs, in Appendix A.) *Then name the rule:* 3-2-1: three
   copies, on two kinds of storage, one off site. For raw sequence
   data, the original copy at the facility or in SRA/ENA (once
   submitted) can be one of the three, but only if you know it is kept
   and for how long. Short points: scratch is purged, not backed up;
   sync folders (OneDrive, Dropbox, Google Drive) copy deletions and
   overwrites too, so alone they are not a backup; a git repository
   (Chapter 21) backs up code, not data; `results/` needs no backup if
   `data/`, `src/`, and the environment are safe, which is the point of
   section 2's layout. Restore test: a backup you have never restored
   from is a hope. Transfers between machines (`rsync`, Globus) are
   Chapter 9. [`tbl-storage-backup`; misconception callouts
   `cluster-is-backed-up` (pitfall: scratch) and `sync-is-backup`;
   self-check]
7. **Sample sheets and metadata.** *Start hands-on:* download nf-core's
   test sample sheet into `data/meta/` with `curl -fLO` and look at it
   (`cat`, then `column -s, -t` for aligned columns). Readers find, by
   eye: 7 rows but 5 samples; `WT_REP1` has two rows (two sequencing
   runs of one sample, merged by the pipeline); three samples have no
   `fastq_2` (single-end); the `strandedness` column. *Then name the
   idea:* the sample sheet is the link between file names and biology;
   it is data, not a note, so it is versioned, checked, and kept beside
   the reads. Rules: one row per file (or run), one column per property,
   plain CSV/TSV, IDs that exactly match file names, no merged cells or
   colour coding (spreadsheet pitfalls in Chapter 14). Sample metadata
   (condition, replicate, batch, date) usually lives in a second table
   joined by sample ID (joins in Chapter 14). Readers create a small
   `data/meta/samples.tsv` (sample, condition, replicate) from a
   supplied start in exercise 3. The nf-core sample sheet's own format
   is Chapter 26. [`fig-sample-sheet`; self-check]
8. **Provenance: where did this number come from?** *Start hands-on:*
   copy the supplied `src/01_count_reads.sh` (about ten lines) into VS
   Code, run `pixi run bash src/01_count_reads.sh`, then
   `cat results/read_counts.tsv` and the new log in `logs/`. The script
   counts reads with `seqkit stats -T` for every file in `data/raw/`,
   and its log records the date, host, seqkit version, and the input
   checksums. This replaces Chapter 1's hand-typed `fastq_summary.txt`
   with a result that knows how it was made. Then fill in `data/README.md`
   from a supplied template: for each input (reads, reference, sample
   sheet) its source URL, accession, version (git commit for
   nf-core/test-datasets), date downloaded, checksum, license, and
   citation, the same record the book keeps for its own data. *Then name
   the idea* with the provenance chain figure: every output points back
   to the script and its parameters, the software versions
   (`pixi.lock`), the inputs and their checksums, the reference release,
   and the log. Most of it costs nothing if recorded at the time, and
   is impossible to rebuild later. What later chapters add to the chain:
   seeds and parameters (Chapter 23), git commits (Chapter 21), pipeline
   versions and their reports (Chapter 26). [`fig-provenance-chain`,
   `tbl-provenance-record`; key idea; misconception callout
   `ill-remember`; self-check]
9. **Writing it down: README, notebook, FAIR.** *Start hands-on:* extend
   Chapter 2's one-line `README.md` with a supplied outline (what the
   project is; layout; where the data came from, pointing to
   `data/README.md`; how to rerun; software). Start `NOTEBOOK.md` with a
   first dated entry (`## 2026-11-17`): what you did today, why, what
   went wrong, what is next. A notebook is for decisions and dead ends
   that scripts do not show; a plain-text file in the project is enough
   (paper or an electronic lab notebook work too; the habit matters, not
   the tool). Write in Markdown (one short box: `#` headings, lists,
   backticks; full Markdown with Quarto in Chapter 12). *Then FAIR,
   briefly:* one table translating Findable, Accessible, Interoperable,
   Reusable into what a student does (cite accessions; deposit in
   SRA/ENA/GEO; use standard formats and plain-text tables; record
   metadata and a license), with Wilkinson et al. 2016 cited. Sharing
   and depositing in depth: Chapters 20 and 22. [`tbl-fair`;
   background callout (FAIR); self-check]
10. **Summary, exercises, further reading.** Summary as 5 bullets that
    mirror the learning goals, ending with the project tree as it now
    stands; exercises (below); annotated further reading.

Length: this is the longest Part I chapter so far in topics. If drafting
runs long, sections 6 (backups) and 9 (FAIR part) are the ones to
shorten; the hands-on thread (sections 2–5, 7–8) stays.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2):
reads, sample sheet, and results are `given` (blue: our data and every
re-organisation of it); the reference is `ref` (orange); checksums and
logs are `good` (green: checks); code, folders, and environment are
neutral (`ink`, `line`, `muted`); `warn` only in the symlink pitfall.

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-project-layout` | 2 | static | The `~/bioinf-book` tree as folders with the role of each beside it, grouped into three bands: **inputs** (`data/raw` blue with a lock icon, `data/meta` blue, `data/ref` orange with a link arrow), **how** (`src/`, `pixi.toml`/`pixi.lock`, neutral), **outputs** (`results/` blue, marked "can be rebuilt"; `logs/` green). One arrow: inputs + how → outputs. |
| `fig-checksum` | 4 | static | Two copies of a file go through the same checksum box: identical copy → identical fingerprint (green tick); a copy with one changed byte (highlighted) → a completely different fingerprint. Real first 8 hex digits of the real MD5 on the left. |
| `fig-symlink` | 5 | stepped (3 steps) | (1) Shared folder with the reference (orange) and the project's `data/ref` signpost pointing to it; (2) `rm data/ref`: the signpost goes, the reference stays; (3) `rm -r data/ref/`: the signpost stays, the shared folder is gone (in `warn`), with the caption "the trailing slash follows the link". |
| `fig-sample-sheet` | 7 | static | The nf-core test sample sheet as a table on the left, FASTQ files on the right; lines from each row to its files. `WT_REP1` has two rows feeding one sample; three rows have one file (single-end). Shows the sheet as the map from files to samples. |
| `fig-provenance-chain` | 8 | static | `results/read_counts.tsv` on the right; arrows back to `src/01_count_reads.sh` (code, parameters), `pixi.lock` (software versions), `data/raw/*.fastq.gz` + `checksums.md5` (inputs), `data/README.md` (source URL, commit, accession), and `logs/…log` (what happened). Each box labelled with the file that holds it, so readers see that provenance is files, not memory. Reused and extended in Chapters 21, 23, 26. |

Not used here: Mermaid (the provenance chain needs file labels and
colour roles), screenshots.

### Interactive figure (Observable JS)

None. Nothing here is an input → result relationship.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-project-folders` | 2 | Folder or file · what goes in it · who writes it (you / scripts / pixi) · back it up? · in git later? (Chapter 21) |
| `tbl-file-names` | 3 | Problem name · why it causes trouble · better name (e.g., `Final FINAL (2).txt` → `2026-11-17_read_counts.tsv`; `run10.sh` before `run2.sh` → `02_…`, `10_…`; `11-3-25 counts.csv` → `2025-11-03_counts.csv`) |
| `tbl-storage-backup` | 6 | Location · example path (laptop, SCINet, Nova) · backed up? · purged? · good for. Readers fill a "yours" column. Site values from official docs only; Appendix A holds the full site version |
| `tbl-provenance-record` | 8 | What to record · example from this project · where it lives (`data/README.md`, `checksums.md5`, `pixi.lock`, `logs/`, `NOTEBOOK.md`) |
| `tbl-fair` | 9 | Principle · what it means · what you do as a student (with an example from this project) |

### Code (§6)

- All commands `filename="Terminal (laptop)"`, tier 2 (shown, not run at
  render), every one cheap. A cluster note (callout or short paragraph in
  §2) says the same steps work in project storage; file management like
  this is light enough for a login node, but checksumming many large
  files is not (Chapter 10).
- Files readers create get their own filename blocks:
  `filename="data/raw/checksums.md5"`, `filename="src/01_count_reads.sh"`,
  `filename="data/README.md"`, `filename="README.md"`,
  `filename="NOTEBOOK.md"`.
- No `$` prompt; code annotations on each new command; captured output in
  `.console` blocks (`md5sum -c`, `ls -l data/ref`, the permission
  errors, `seqkit stats -T`, the log).
- **Bash everywhere:** `md5sum`, `sha256sum`, `date -I` are GNU
  coreutils, present on macOS from Chapter 1's setup. No `md5` (BSD)
  variant.
- No OS tabsets expected. Possible exception: WSL readers who want to
  see the project in Windows Explorer (`explorer.exe .`) get one line,
  with Chapter 1's pitfall that work stays in the Linux home.
- Draft of the supplied script (to test while drafting):

  ```bash
  #!/usr/bin/env bash
  # 01_count_reads.sh: count reads in every raw FASTQ file.
  # Run from the project folder:  pixi run bash src/01_count_reads.sh
  set -euo pipefail                         # stop at the first error (Chapter 8)

  mkdir -p results logs
  log="logs/01_count_reads_$(date +%F).log"

  {
    echo "date:   $(date -Is)"
    echo "host:   $(hostname)"
    echo "seqkit: $(seqkit version)"
    echo "inputs:"
    md5sum data/raw/*.fastq.gz
  } > "$log"

  seqkit stats -T data/raw/*.fastq.gz > results/read_counts.tsv
  echo "wrote results/read_counts.tsv; log in $log"
  ```

  Readers run it, not write it; Chapter 8 teaches every line. The
  shebang and `chmod +x` wait for Chapter 7; here it runs as
  `bash src/…` through `pixi run`.

### Plots

None.

### Animation (manim)

None. `fig-symlink` covers the one sequence as a stepped SVG.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | Keep inputs, code, and outputs apart. If `results/` can be rebuilt from `data/`, `src/`, and the environment, your project is reproducible and `results/` needs no backup |
| 4 | Key idea | Raw data is read-only: check it once with checksums, lock it, and never edit it; every change happens in a script that writes somewhere else |
| 4 | Misconception | "Matching checksums mean my data are correct" (`checksum-proves-correct`) |
| 5 | Pitfall | `rm -r data/ref/` (trailing slash) deletes the shared folder the link points to; remove links with `rm data/ref` |
| 5 | Misconception | "A symlink is a copy" (`symlink-is-copy`); may merge with the pitfall if the screen gets crowded |
| 6 | Pitfall | Scratch is purged and not backed up; neither is all cluster storage (`cluster-is-backed-up`) |
| 6 | Misconception | "My Dropbox/OneDrive folder is my backup" (`sync-is-backup`) |
| 8 | Key idea | Record provenance when the file is made: source, version, checksum, script, software, log. It costs a minute now and cannot be rebuilt later |
| 8 | Misconception | "I'll remember where this file came from" (`ill-remember`) |
| 9 | Background | FAIR principles, with `tbl-fair` |

Section 6 has three callouts; keep them on separate screens or merge the
two misconceptions into the text with the table.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: You delete `results/` by mistake. What do you need to get it back?
  (*Nothing new: rerun the scripts in `src/` on `data/` with the same
  environment. If you cannot, something that belongs in `data/` or
  `src/` is living in `results/`.*)
- §3: In what order does `ls` list `run1.sh`, `run2.sh`, `run10.sh`? How
  would you rename them? (*`run1.sh`, `run10.sh`, `run2.sh`; `01_…`,
  `02_…`, `10_…`, with names that say what each does.*)
- §4: `md5sum -c` prints `FAILED` for a file you just copied from the
  cluster. What happened, and what do you do? (*The copy differs from the
  original, usually an incomplete transfer; copy it again and recheck.
  Do not analyse it.*)
- §5: You run `rm data/ref`. Is the reference genome gone? (*No: only the
  link is removed. With `rm -r data/ref/` it could be.*)
- §6: Your raw FASTQ files are in cluster scratch and in a OneDrive
  folder on your laptop. How many backups do you have? (*Arguably none:
  scratch is purged and not backed up, and OneDrive copies deletions.
  Put the originals in backed-up storage and keep the facility's or
  SRA's copy as the off-site one.*)
- §7: The sample sheet has 7 rows. How many samples are there, and how
  do you know? (*5: `WT_REP1` and `RAP1_UNINDUCED_REP2` each have two
  runs; count distinct values in the `sample` column, not rows.*)
- §8: A reviewer asks which version of seqkit made `read_counts.tsv`.
  Where in the project is the answer? (*The log in `logs/`, and
  `pixi.lock`.*)
- §9: Which FAIR principle does citing `SRR6357070` and `GSE110004` in
  your README serve? (*Findable, through persistent identifiers; also
  Reusable.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
commands or templates):

1. **Rename a messy folder.** A supplied command creates
   `~/bioinf-ch03-messy/` with eight badly named files (spaces, `final`,
   unpadded numbers, US-style dates, a `.txt` that is really a TSV).
   Propose new names in a table, then apply them with supplied `mv`
   commands adapted to your names. (*Answer key: one good set of names,
   and why `ls` now sorts them in order.*)
2. **Catch a broken transfer.** Make a truncated copy
   (`head -c 1000000 data/raw/SRR6357070_1.fastq.gz > /tmp/broken.fastq.gz`;
   to check: `/tmp` vs a scratch folder in `~`), checksum it with
   `md5sum`, compare it with `checksums.md5`, and run `gzip -t` on it.
   Which check caught it, and which would catch a file that is complete
   but the wrong sample? (*Both catch truncation; only the checksum,
   compared against the facility's list, catches a wrong file that is
   still valid gzip.*)
3. **Sample metadata.** Complete the supplied `data/meta/samples.tsv`
   (columns: `sample`, `condition`, `replicate`, `n_runs`, `layout`) for
   the 5 samples in the nf-core sample sheet. Which sample IDs would you
   join it to the sample sheet on, and what goes wrong if one ID has a
   trailing space? (*Join on `sample`; a trailing space makes it a
   different ID, so that sample silently drops out: Chapter 14.*)
4. **Rerun and compare.** Delete `results/`, rerun
   `pixi run bash src/01_count_reads.sh`, and compare the new
   `read_counts.tsv` with a copy you saved first, using `cmp`. Then add
   a `NOTEBOOK.md` entry for today. (*Identical; the log differs only in
   date and time, which is why outputs and logs are kept apart.*)
5. **(Cluster readers)** Create the same layout in your project storage,
   link a reference your site or lab already provides (Appendix A) or
   the test reference, and fill in your column of `tbl-storage-backup`
   from your site's docs. (*No-cluster readers: fill in the laptop
   rows.*)

## Examples and data

- Toy examples: the messy folder (exercise 1), a truncated copy
  (exercise 2), one changed byte for `fig-checksum`.
- Running dataset (yeast nf-core/rnaseq test data), all from the
  `rnaseq` branch of `nf-core/test-datasets`, *checked* 2026-11-17:
  - `testdata/GSE110004/SRR6357070_1.fastq.gz` and `_2` (from Chapter 1;
    moved in, or downloaded again). MD5 above; SHA-256 already in
    `data/README.md` and matches.
  - `samplesheet/v3.10/samplesheet_test.csv`: 1,335 bytes, 7 rows,
    5 samples; last commit `0a8d404` (2023-03-24); SHA-256
    `beeb7811b14bfa973233616625a9648ba649736d97b2e84af51d619ac89691c4`.
    Its `strandedness` is `auto` for `WT_REP1` and `reverse` for the
    rest; the older `samplesheet/samplesheet_test.csv` has `reverse`
    everywhere. Use the `v3.10` file (matches current nf-core/rnaseq;
    confirm against the version Chapter 26 runs).
  - `reference/genome.fa.gz` (71,440 bytes; one sequence, `>I`: yeast
    chromosome I only; last commit `bae247f`, 2020-08-24) and
    `reference/genes.gtf.gz` (10,452 bytes; last commit `cfc925e`,
    2023-11-16). Chapter 1's `data/README.md` lists the uncompressed
    `genes.gtf`; record the `.gz` here.
  - Add rows to the book's `data/README.md` for the sample sheet and the
    two reference files, with MD5 and SHA-256.
- Where commands run: laptop. Same commands in project storage on a
  cluster (section 2 note; exercise 5).

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters), to add when this plan is agreed. Where each is handled
is in brackets.

- `checksum-proves-correct`: "If the checksums match, my data are
  correct." A match proves the file is byte-for-byte the one the
  checksum was made from, not that the source file was the right sample
  or good data. Probe: the facility's file was mislabelled before they
  computed the MD5; does `md5sum -c` catch it? (No.) [callout, §4;
  exercise 2]
- `symlink-is-copy`: "A symbolic link is a copy, so deleting or editing
  through it is safe." It points to the original; editing through it
  edits the original, and `rm -r link/` can delete the target.
  [callout/pitfall, §5; `fig-symlink`; self-check]
- `readonly-cant-delete`: "A read-only file can't be deleted." Deleting
  is controlled by the folder's permissions; lock the folder too.
  [text, §4; Chapter 7 head-on]
- `cluster-is-backed-up`: "Everything on the cluster is backed up."
  Scratch is purged and not backed up; which other areas are backed up
  differs by site. [pitfall, §6; `tbl-storage-backup`; Chapter 10]
- `sync-is-backup`: "My Dropbox/OneDrive/Google Drive folder is my
  backup." Sync copies deletions and overwrites; it is one copy in two
  places, unless version history is kept and you know for how long.
  [callout, §6; self-check]
- `ill-remember`: "I'll remember where this file came from and how I
  made it." Weeks later no one does; record source, version, checksum,
  script, and log when the file is made. [callout, §8]

## Links to other chapters and books

- Builds on: Chapter 1 (the FASTQ files in `~/bioinf-ch01`, the
  hand-made `fastq_summary.txt`, `curl -fLO`, `gzip -t`); Chapter 2
  (`~/bioinf-book`, pixi, `pixi run`, VS Code and nano for editing,
  `README.md` from exercise 3, project vs home storage on clusters).
- Leads to: Chapter 4 (a good help request quotes the log and versions);
  Chapter 5 (paths, quoting, `ln -s`, `find`); Chapter 6 (`>` vs `>>`,
  `cut | sort | uniq` on the sample sheet); Chapter 7 (permissions,
  `chmod`, shebang); Chapter 8 (the script line by line; numbered
  scripts as a pipeline; first git commit of `src/`); Chapter 9
  (checksums after `rsync`/Globus); Chapter 10 (storage tiers, quotas,
  purges); Chapter 12 (Quarto: the rendered summary in the recurring
  project); Chapter 14 (sample-sheet pitfalls, joins); Chapter 15
  (reference releases, chromosome names); Chapter 20 (downloading from
  SRA/ENA with their MD5s; licenses and citation of public data);
  Chapter 21 (git, `.gitignore` keeping `data/` and `results/` out);
  Chapter 23 (provenance: versions, parameters, seeds); Chapter 26
  (nf-core sample sheets, pipeline versions and reports); Appendix A
  (site storage, backups, reference collections). Other books: every
  later book starts from this layout.

## Official links to include

- GNU coreutils manual: `md5sum`, `sha256sum` (`--check`), `ln`, `chmod`
  (gnu.org/software/coreutils)
- ISO 8601 date format: iso.org (ISO 8601 page)
- ENA: file reports with MD5 (ebi.ac.uk/ena); NCBI SRA (ncbi.nlm.nih.gov/sra)
- nf-core/test-datasets (`rnaseq` branch); nf-core/rnaseq usage page for
  the sample sheet format (nf-co.re/rnaseq)
- GO FAIR: go-fair.org (FAIR principles)
- Site storage and backup pages: SCINet (scinet.usda.gov, storage
  guides; Juno), ISU Research IT (Nova storage); linked from Appendix A
- Markdown: quarto.org's Markdown basics page (official, and the book's
  tool)

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). DOIs below verified
with scite 2026-11-17 (all found, no editorial notices); fetch BibTeX
from the DOI when adding.

- Wilson et al. 2017, "Good enough practices in scientific computing",
  *PLoS Comput Biol*, doi:10.1371/journal.pcbi.1005510: the closest
  match to this chapter (data management, project organization, keeping
  track of changes); the main pick.
- Noble 2009, "A quick guide to organizing computational biology
  projects", *PLoS Comput Biol*, doi:10.1371/journal.pcbi.1000424: the
  classic project layout and lab-notebook advice; compare with ours.
- Wilkinson et al. 2016, "The FAIR Guiding Principles for scientific data
  management and stewardship", *Sci Data*, doi:10.1038/sdata.2016.18:
  the source of FAIR (cited in §9).
- Broman & Woo 2018, "Data organization in spreadsheets", *Am Stat*,
  doi:10.1080/00031305.2017.1375989: for sample sheets kept in
  spreadsheets; may fit Chapter 14 better, so pick one chapter.
- Shotts, *The Linux Command Line*: the chapters on links and
  permissions, for readers who want them before Chapters 5 and 7.

## Austin's notes

-

## Decisions (2026-11-17, open questions round)

Austin's choices (Codex's review agreed with each):

- **Dataset description: correct all three levels.** Original study
  (GSE110004), nf-core test fixture (5 samples, 7 runs, 4 paired-end,
  3 used single-end, every run sub-sampled to 50,000 reads or pairs:
  all 10 files counted 2026-11-17), and the book's own files (SRR6357070).
  Applied to `PLAN_CHAPTERS.md` (Conventions → Data) and
  `data/README.md`. The samples' biology stays with Transcriptomics.
  Note: `_2` files also exist for SRR6357073 and SRR6357074, but the
  sheet uses those runs single-end (nf-core tests both layouts).
- **Checksum: teach `md5sum`, keep SHA-256 in the records.** §4 teaches
  `md5sum -c`; `sha256sum` mentioned as the same idea, stronger.
  `data/README.md` now has an MD5 column beside SHA-256 for the two
  FASTQ files.
- **Shared folder: keep the stand-in,** clearly labelled as standing in
  for a lab share such as `/project/<lab>/…`; its target path and
  source go in `data/README.md`.
- **Chapter 1 files: move,** with recovery notes: a missing or
  half-downloaded file is downloaded again with the supplied `curl`;
  readers returning to Chapters 1–2 find the files in `data/raw/`.
- **Notebook: `NOTEBOOK.md` by default;** one sentence that an electronic
  lab notebook the lab already uses is fine. The habit (dated decisions
  and dead ends) matters, not the tool.

Still to do: work through `chapter_03_codex_review.md` (corrections
1–7: checksum working directory, a local manifest, the log keeping
stderr and one file per run, backup wording, symlink portability,
immutable download URLs). Chapter 4's "find the log" step depends on
correction 3.

## Open questions

1. ~~Running dataset description~~, 2. ~~MD5 or SHA-256~~,
   3. ~~Simulated shared folder~~, 4. ~~Moving vs copying~~,
   5. ~~Notebook~~: all decided 2026-11-17 (see *Decisions*).
6. **Site backup facts** for `tbl-storage-backup` (is SCINet `/project`
   backed up? Nova `/work`? Juno and `/lss` retention?) must come from
   the sites' current docs before drafting; nothing here is asserted yet
   beyond what Chapter 2's checks recorded (`/90daydata` and `/ptmp` are
   purged scratch; Nova `/lss` backed up, not on compute nodes).
7. **To check while drafting:** `rm -r link/` on Linux/WSL (on macOS it
   removed the target folder itself; GNU on Linux may remove the
   contents and keep the folder: either way the data are gone);
   `chmod a-w data/raw` blocks `rm` and `mv` of its files; `column -s,
   -t` output on the sample sheet (empty fields may collapse);
   `date -Is` and the script's log on macOS and WSL.
