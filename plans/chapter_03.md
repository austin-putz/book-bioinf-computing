---
title: "Chapter 3 — Organizing projects and data"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** I — Getting set up · **Label:** core · **Status:** chapter
drafted 2026-11-17 (`chapters/03-organizing-projects.qmd`; see *Drafting
notes* for where it differs from this plan). Plan revised the same day
after the open-questions round and the Codex review
(`chapter_03_codex_review.md`; see *Decisions* and *Review responses*). Commands marked *checked* were run on 2026-11-17
(macOS 15 Intel, GNU coreutils 9.11 from Homebrew, the book environment
with pixi 0.84.2 and seqkit 2.14.0 in a scratch folder); the rest are to
be checked while drafting.

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
- Chapter 4 relies on this chapter's script log holding the tool's own
  messages and one log per run (§8).

## Outcome and check

- **Outcome:** readers turn `~/bioinf-book` into an organized project:
  raw reads moved in from Chapter 1, verified with checksums, and
  protected from accidental changes; a shared reference linked in, not
  copied; an inventory of the local read files and their sample
  metadata; a supplied numbered script run to produce a result with its
  own log; and a README, a data record, and a notebook entry that say
  where every file came from. They can also say which of their storage
  locations are backed up, and who would recover them.
- **Check:** from `~/bioinf-book` (all *checked* in a scratch copy of
  the project):

  ```bash
  cd data/raw
  md5sum -c checksums.md5              # SRR6357070_1.fastq.gz: OK
                                       # SRR6357070_2.fastq.gz: OK
  cd ~/bioinf-book
  ls -l data/ref                       # data/ref -> /home/you/bioinf-shared/…
  pixi run bash src/01_count_reads.sh  # both files OK, then the counts
  cat results/read_counts.tsv          # num_seqs 50000 for both files
  ls logs/                             # one log per run
  ```

  The checksum file lists bare file names, so `md5sum -c` runs inside
  `data/raw/` (*checked*: run from the project root it reports `No such
  file or directory` / `FAILED open or read` even for perfect files).

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Lay out a project folder that keeps raw data, reference, metadata,
   code, results, and logs apart, and name files so they sort well and
   avoid common path problems.
2. Verify downloaded files with checksums, and protect raw data from
   accidental changes and deletion.
3. Link shared data into a project with a symbolic link, and say what
   removing the link does and does not remove.
4. Record where every input and output came from (source, version,
   checksum, script, software version, log) in files kept in the project.
5. Say which of your storage locations are backed up, for how long, and
   who would restore them.

## Sections

Same pattern as Chapters 1–2: each section opens with something readers
run or look at, then names the idea. The hands-on thread is one project
built step by step in `~/bioinf-book`; each section adds one piece, so
the folder at the end of the chapter is the starting point for every
later chapter. Every section starts with `cd ~/bioinf-book`. Commands are
copy-and-run; `mkdir`, `mv`, `ln -s`, `chmod` and the rest are explained
in Part II (Chapters 5–7), as in Chapter 1. Practice and deliberately
broken files go in a scratch folder, `~/bioinf-ch03/`, never in the
project. Visual items in brackets are specified under *Visuals and
teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph: a
   month from now, you (or your PI, or a reviewer) will ask "which file
   is this, where did it come from, and how was this number made?"; this
   chapter sets up the folder and the habits that answer that without
   memory. Chapter 2's `~/bioinf-book` becomes the book's project.
2. **A folder for each project.** *Start hands-on:* one `mkdir -p` that
   creates the layout inside `~/bioinf-book`, then `ls` to see it beside
   `pixi.toml`. *Then name the parts* with the layout figure and table.
   The tree as it stands at the end of the chapter:

   ```
   ~/bioinf-book/
   ├── README.md          what this project is; how to rerun it
   ├── NOTEBOOK.md        dated log of what you did and why
   ├── pixi.toml  pixi.lock  .pixi/   software (Chapter 2)
   ├── data/
   │   ├── README.md      where every input came from (provenance)
   │   ├── raw/           reads as received, protected: never edited
   │   │   ├── SRR6357070_1.fastq.gz  SRR6357070_2.fastq.gz
   │   │   └── checksums.md5
   │   ├── meta/
   │   │   ├── reads.tsv                 which local files belong to which run and sample
   │   │   ├── samples.tsv               what each sample is (from the archive record)
   │   │   └── samplesheet_upstream.csv  nf-core's test sheet, unchanged (§7)
   │   └── ref  ->  ~/bioinf-shared/references/yeast_R64-1-1_test   (link)
   ├── src/
   │   └── 01_count_reads.sh
   ├── results/
   │   └── read_counts.tsv
   └── logs/
       └── 01_count_reads_2026-11-17T122453_7WFs.log   one per run
   ```

   Rules, one sentence each: one project, one folder; inputs, code, and
   outputs in separate folders; everything in `results/` should be
   rebuildable from `data/`, `src/`, the settings, and the software
   records, so you can practise rebuilding it (exercise 4); paths in
   scripts are relative to the project root, which makes the project
   easier to move (what else moving needs: §5). Name it as one
   reasonable layout among several (Noble 2009; Wilson et al. 2017),
   not the only right one; nf-core and Chapter 25 add `work/` later.
   *On a cluster* (short paragraph): the project lives in project
   storage (`/project` on SCINet, `/work` on Nova), not home (small
   quota) or scratch (purged); same layout. Large intermediate files
   may go to scratch, with only final results kept in the project
   (Chapters 10, 26). [`fig-project-layout`, `tbl-project-folders`;
   key idea; self-check]
3. **Names that work.** *Start with a sorting puzzle:* `ls` on a supplied
   set of names in `~/bioinf-ch03/names/` (`final.txt`, `final_v2.txt`,
   `Final FINAL (2).txt`, `run10.sh`, `run2.sh`, `11-3-25 counts.csv`)
   shows them in an order no one wants. Then the rules, with the fixed
   version beside each:
   - use only letters, digits, `_`, `-`, and `.` (no spaces, brackets,
     `&`, `#`, accents); spaces break commands unless quoted, and you
     will still learn to quote paths (Chapter 5);
   - lowercase, or one consistent case (macOS and Windows folders are
     usually case-insensitive, Linux clusters are case-sensitive, so
     `Data.csv` and `data.csv` are one file on a laptop and two on the
     cluster);
   - dates as `YYYY-MM-DD` (ISO 8601), so they sort in time order;
   - numbers zero-padded and scripts numbered in run order (`01_`, `02_`,
     …; `00_` for one-time setup such as downloads), so `ls` shows the
     pipeline in order;
   - say what is in the file, and keep the extension true (`.tsv` means
     tabs, `.gz` means compressed);
   - meaningful version labels are good (`yeast_R64-1-1_test`,
     `report_2026-11-17.html`); unexplained ones (`final_v2`,
     `final_final`) are not: say what changed, and later let git keep
     the history (Chapter 21).

   `11-3-25 counts.csv` has no single fix: is it 3 November or 11 March,
   2025 or 2011? Renaming cannot recover a meaning you do not know; ask
   whoever made it, then rename. Sample and run IDs from a facility or
   archive (`SRR…`, `WT_REP1`) are kept as given so they still match the
   records; rename only your own files. [`tbl-file-names`; self-check]
4. **Raw data: move it in, check it, protect it.** *Start hands-on:*
   `cd ~/bioinf-book`, then move both FASTQ files from `~/bioinf-ch01/`
   into `data/raw/`. Recovery, one mate at a time: readers who never
   downloaded R2 (an exercise in Chapters 1–2), or whose
   `~/bioinf-ch01` is gone, use the supplied `curl -fLO` for each missing
   file, pinned to one commit (see *Examples and data*). If a file is
   already in `data/raw/` from an earlier visit, skip it; never overwrite
   a protected file (check it with `md5sum -c` instead). `~/bioinf-ch01`
   keeps `fastq_summary.txt` and can be deleted later. Readers going back
   to Chapter 1–2 commands use the new `data/raw/` paths. Create
   `data/raw/checksums.md5` from the two lines the book supplies (in VS
   Code or nano: Chapter 2's editors), then `cd data/raw`,
   `md5sum -c checksums.md5` → two `OK`, `cd ~/bioinf-book`. One
   sentence: the file names in `checksums.md5` have no folder, so the
   check runs in the folder that holds them (sequencing facilities ship
   them the same way). *Then name the idea:* a checksum is a short
   fingerprint computed from every byte; one changed byte gives a
   different value. Facilities and ENA supply MD5 values; run `md5sum -c`
   after every download or transfer (Chapter 9 reuses it after `rsync`).
   `sha256sum` works the same way and is stronger; the book's own
   `data/README.md` records both. Two kinds of failure, told apart:
   `FAILED` (the bytes differ: download again, never "fix" the expected
   value by recomputing it from the damaged copy) and `FAILED open or
   read` / `No such file or directory` (the file is missing, misnamed,
   or you are in the wrong folder: check before assuming damage).
   *Then protect it, first on a toy:* in `~/bioinf-ch03/practice/`,
   make a folder with one small file, `chmod a-w` the file **and** the
   folder, and try to append, delete, move, and add a file: all four
   fail with `Permission denied` (*checked*). Why the folder too: a
   read-only file in a writable folder can still be deleted (*checked*:
   `rm` removed one without asking when not run interactively). Then
   apply the same two commands to `data/raw/` and its files. This guards
   against accidents, not against you: the owner can always undo it.
   Adding a file later: `chmod u+w data/raw`, add it, check it, add its
   line to `checksums.md5`, protect both again. Permissions are
   explained in Chapter 7. Raw reads stay compressed; never unzip them
   in place. [`fig-checksum`; key idea; misconception callout
   `checksum-proves-correct`; self-check]
5. **Shared data: link, don't copy.** *Start hands-on:* make a
   **stand-in** for a lab's shared folder (the text says plainly that on
   a cluster this would be something like `/project/<lab>/references/`):
   `~/bioinf-shared/references/yeast_R64-1-1_test/`. Download the test
   genome (`genome.fa.gz`, 71 kB) and annotation (`genes.gtf.gz`, 10 kB)
   into it with pinned `curl -fLO` commands, check them against supplied
   MD5 values, and give the folder a short README (source, commit, date,
   checksums). Then from `~/bioinf-book`:
   `ln -s ~/bioinf-shared/references/yeast_R64-1-1_test data/ref`,
   `ls -l data/ref` (the arrow), and `ls data/ref/` (the files, seen
   through the link). *Then name the idea:* a symbolic link is another
   route to the same data, not a copy. On a cluster, references and big
   shared datasets exist once (`/project/<lab>/…`), every project points
   at them, and no one's quota pays twice. Then two short demonstrations
   on a **toy** link in `~/bioinf-ch03/practice/` (never on the real
   reference): editing a file through the link changes the original;
   `unlink toylink` (or `rm toylink`, no slash, no `-r`) removes only
   the link and the target is untouched. A link whose target moves or is
   renamed is broken (`ls -l` shows it, in red in many terminals).
   **Moving the project:** relative paths in scripts help, but a link is
   only a pointer: on another machine (say, laptop to cluster) the
   target is not there. Moving a project means: copy the project files,
   reinstall the environment from `pixi.toml` + `pixi.lock`, and
   recreate `data/ref` to point at that machine's copy of the same
   reference, which `data/README.md` identifies by source, release, and
   checksums. Transfer commands: Chapter 9. A link is not a backup of
   its target, and someone (you, the lab, the site) must own that
   target's preservation (§6). **Pitfall, captured output labelled
   "macOS, GNU coreutils 9.11":** `rm -r data/ref/` with a trailing
   slash followed the link and deleted the shared folder itself (also
   with macOS's own `rm`; Linux/WSL behaviour to be tested, see open
   questions). Tab completion adds that slash. Rule: remove a link with
   `unlink` or `rm` and no slash. Shown as captured output only; readers
   do not run it. Reference versions (assembly vs release, chromosome
   names) are Chapter 15. [`fig-symlink`; pitfall; misconception callout
   `symlink-is-copy`; self-check]
6. **Backups: where do your files really live?** *Start with a
   table readers fill in:* for each place they keep files (laptop disk,
   cloud sync folder, cluster home, project, scratch, lab archive): is
   it backed up, for how long can deleted or changed files be recovered,
   and who restores them (you, IT, the site)? SCINet and Nova values
   come from the sites' current official docs, dated and linked, in
   Appendix A; nothing is inferred from a storage area's name. *Then
   name the rule:* 3-2-1: three copies, on two kinds of storage, one off
   site. For raw sequence data, the facility's copy or SRA/ENA (once
   submitted) can be one of the three, but only if you know it is kept
   and for how long, and an archive of the original reads does not
   preserve a subset you made from them. Short points: scratch is
   purged, not backed up; sync folders (OneDrive, Dropbox, Google Drive)
   copy deletions and overwrites too, so alone they are one copy in two
   places unless version history is kept and you know for how long;
   git tracks the history of code (Chapter 21), and only a copy stored
   somewhere else (a remote, Chapter 22) protects it if this machine is
   lost. *What to back up:* raw data, metadata, code, notebook, logs, and
   the records that explain results; important final results too. A
   result you can rebuild cheaply (this chapter's read counts) needs no
   backup of its own, but a large or published analysis may need days of
   compute, a reference no longer online, or an old software version to
   rebuild, so keep it. Disposable intermediate files can follow a
   different rule. Restore test: a backup you have never restored from
   is a hope. [`tbl-storage-backup`; misconception callouts
   `cluster-is-backed-up` (pitfall: scratch) and `sync-is-backup`;
   self-check]
7. **Sample sheets and metadata.** *Start hands-on:* download nf-core's
   test sample sheet, pinned, into `data/meta/` and save it **unchanged**
   as `samplesheet_upstream.csv`; open it in VS Code (as CSV, not with
   `column`, which can shift empty fields). Readers find, by eye: 7 rows
   but 5 sample labels; `WT_REP1` and `RAP1_UNINDUCED_REP2` each have two
   rows; three rows (two labels: `RAP1_UNINDUCED_REP1`,
   `RAP1_UNINDUCED_REP2`) have no `fastq_2`; a `strandedness` column. In
   this sheet each row is one sequencing run, with columns for its mate
   files, and rows that share a sample label are merged by the pipeline
   (nf-core's usage docs, Chapter 26). *Then the twist (checked against
   ENA, 2026-11-17):* the archive lists the seven runs as **seven
   different biological samples** (GSM2879618–24), all paired-end. The
   two `WT_REP1` runs are wild-type replicates 1 and 2; the sheet's
   `WT_REP2` is replicate 3. The sheet is a pipeline *test fixture*: its
   labels group runs to exercise merging and single-end handling, not to
   describe the experiment. Lesson: a sample label is a claim; check it
   against the source record, and never infer biology from names alone.
   (Experimental design: Transcriptomics.) *Then the project's own
   metadata,* for the files actually in `data/raw/`, from supplied
   starting files: `data/meta/reads.tsv` (one row: `sample`, `run`,
   `fastq_1`, `fastq_2`, mapping `WT_REP1` / `SRR6357070` to the two
   paths) and `data/meta/samples.tsv` (one row: `sample`, `run`,
   `geo_sample`, `condition`, `replicate`, from the ENA record:
   GSM2879618, wild type, biological replicate 1). *Then name the idea:*
   metadata is data, not a note: versioned, checked, and kept beside the
   reads. Rules: one row per run (or per sample) and one column per
   property; plain CSV/TSV; sample IDs agree across tables; file-path
   columns point at the right files (sample IDs and file names need not
   match: `WT_REP1` vs `SRR6357070_1.fastq.gz`); no merged cells or
   colour coding (spreadsheet pitfalls, Chapter 14). Run and sample
   tables are joined by ID (Chapter 14); nf-core's own sheet format is
   Chapter 26. [`fig-sample-sheet`; self-check]
8. **Provenance: where did this number come from?** *Start hands-on:*
   copy the supplied `src/01_count_reads.sh` (about twenty lines; also
   downloadable) into VS Code, run `pixi run bash src/01_count_reads.sh`,
   then `cat results/read_counts.tsv` and the new log in `logs/`. What
   the script does, in plain words (Chapter 8 explains every line): it
   checks the inputs against `checksums.md5` and stops if any fails;
   records the date, host, the script's own checksum, the seqkit
   version, and the command; counts the reads; writes the table to a
   temporary file and only then puts it in `results/`, so a failed run
   cannot replace a good result with an empty one; records the output's
   checksum; and saves everything the run printed, including seqkit's
   own messages, in a new log named by date **and time**, so a second
   run the same day keeps both (*checked*: success, same-day rerun, and
   a corrupted input, which stopped at `FAILED`, exited 1, kept the old
   result, and left the failure in its log). This replaces Chapter 1's
   hand-typed `fastq_summary.txt` with a result that knows how it was
   made. Then fill in `data/README.md` from a supplied template: for each
   input (reads, reference, upstream sample sheet) its source URL (the
   pinned commit), accession, date downloaded, MD5 and SHA-256, license,
   and citation, the same record the book keeps for its own data; for
   the reference, also where the shared copy lives. *Then name the idea*
   with the provenance chain figure: `read_counts.tsv` points back to
   the script (and its checksum), the command and its options, the
   software versions (`pixi.lock`, seqkit version in the log), the
   inputs it actually read (the two FASTQ files and their checksums),
   their sources (`data/README.md`), and the log. The reference and the
   sample sheet belong to the project's records but are not inputs to
   *this* result; they join the chain when a later analysis uses them.
   Most of it costs nothing if recorded at the time, and is impossible
   to rebuild later. What later chapters add: git commits for the script
   (Chapter 21), seeds and parameters (Chapter 23), pipeline versions
   and reports (Chapter 26). [`fig-provenance-chain`,
   `tbl-provenance-record`; key idea; misconception callout
   `ill-remember`; self-check]
9. **Writing it down: README, notebook, FAIR.** *Start hands-on:* extend
   Chapter 2's one-line `README.md` with a supplied outline (what the
   project is; layout; where the data came from, pointing to
   `data/README.md`; how to rerun: `pixi run bash src/01_count_reads.sh`;
   software). Start `NOTEBOOK.md` with a first dated entry
   (`## 2026-11-17`): what you did today, why, what went wrong, what is
   next. A notebook is for decisions and dead ends that scripts do not
   show; a plain Markdown file in the project is the default, and an
   electronic lab notebook your lab already uses is fine: the habit
   matters, not the tool. Markdown in one short box (`#` headings,
   lists, backticks; more with Quarto in Chapter 12). *Then FAIR,
   briefly:* one table: what Findable, Accessible, Interoperable,
   Reusable mean, and which habits from this chapter **support** each
   (accessions and persistent identifiers; standard formats and plain
   tables; metadata someone else can read; a stated license and
   citation). A README and a CSV do not by themselves make a project
   FAIR; depositing data with rich metadata does (Chapters 20, 22).
   Accessible does not have to mean open to everyone: access can
   require a login, as long as how to get it is clear. Wilkinson et al.
   2016 cited. [`tbl-fair`; background callout (FAIR); self-check]
10. **Summary, exercises, further reading.** Summary as 5 bullets that
    mirror the learning goals, ending with the project tree as it now
    stands; exercises (below); annotated further reading.

Length: the hands-on thread (sections 2–5, 7–8) and the backup check
(§6, a chapter goal) stay. If drafting runs long, shorten repeated
descriptions of the layout, keep FAIR to its table, and trim the §7
upstream-sheet discussion to the twist.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2):
reads, sample metadata, and results are `given` (blue: our data and every
re-organisation of it); the reference is `ref` (orange); checksums and
logs are `good` (green: checks); code, folders, and environment are
neutral (`ink`, `line`, `muted`); `warn` only in the symlink pitfall.

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-project-layout` | 2 | static | The `~/bioinf-book` tree with real file names, grouped into three bands: **inputs** (`data/raw` blue with a lock icon, `data/meta` blue, `data/ref` orange with a link arrow), **how** (`src/`, `pixi.toml`/`pixi.lock`, neutral), **outputs** (`results/` blue, marked "rebuildable"; `logs/` green, marked "keep"). One arrow: inputs + how → outputs. |
| `fig-checksum` | 4 | static | Two copies of a file go through the same checksum box: identical copy → identical fingerprint (green tick); a copy with one changed byte (highlighted) → a completely different fingerprint. Real first 8 hex digits of the real MD5 on the left. |
| `fig-symlink` | 5 | stepped (4 states) | Each from an intact link, not a command sequence: (1) the shared folder with the reference (orange) and the project's `data/ref` signpost pointing to it; (2) reading through the link: `ls data/ref/` shows the target's files; (3) editing a toy file through a toy link changes the original; (4) `unlink`: the signpost goes, the target stays. The recursive-delete pitfall is not a step: it is a separate captured-output box labelled with the tested platform. |
| `fig-sample-sheet` | 7 | static | Three columns: sample label → run → mate files. The upstream sheet's 5 labels, 7 runs, and their files (basenames only), with the two downloaded files marked; a side note from ENA: 7 runs = 7 biological samples, so the labels are a test grouping. |
| `fig-provenance-chain` | 8 | static | `results/read_counts.tsv` on the right; arrows back to `src/01_count_reads.sh` + its checksum and the command (code, options), `pixi.lock` + seqkit version (software), `data/raw/*.fastq.gz` + `checksums.md5` (the inputs this result read), `data/README.md` (source URL, commit, accession), and `logs/…log` (what happened). The reference and sample sheet sit greyed at the edge, labelled "project records, not inputs to this result". Reused and extended in Chapters 21, 23, 26. |

Five figures and five tables are the ceiling for this chapter.
Not used here: Mermaid (the provenance chain needs file labels and
colour roles), screenshots.

### Interactive figure (Observable JS)

None. Nothing here is an input → result relationship.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-project-folders` | 2 | Folder or file · what goes in it · who writes it (you / scripts / pixi) · back it up? (raw data, metadata, code, logs, notebook: yes; final results: yes if costly to rebuild; intermediates: by policy) · in git later? (Chapter 21) |
| `tbl-file-names` | 3 | Problem name · why it causes trouble · better name (e.g., `Final FINAL (2).txt` → `2026-11-17_read_counts.tsv`; `run10.sh` before `run2.sh` → `02_…`, `10_…`; `11-3-25 counts.csv` → "ask first, then `2025-11-03_counts.csv` or `2025-03-11_counts.csv`") |
| `tbl-storage-backup` | 6 | Location · example path (laptop, SCINet, Nova) · backed up? · how long can deleted files be recovered? · who restores them? · purged? · good for. Readers fill a "yours" column. Site values from current official docs only, dated; Appendix A holds the full site version |
| `tbl-provenance-record` | 8 | What to record · example from this project · where it lives (`data/README.md`, `checksums.md5`, `pixi.lock`, `logs/`, `NOTEBOOK.md`) |
| `tbl-fair` | 9 | Principle · what it means · habits from this chapter that support it (with an example from this project) |

### Code (§6)

- All commands `filename="Terminal (laptop)"`, tier 2 (shown, not run at
  render), every one cheap. A cluster note (§2) says the same steps work
  in project storage; file management like this is light enough for a
  login node, but checksumming many large files is not (Chapter 10).
- Files readers create get their own filename blocks:
  `filename="data/raw/checksums.md5"`, `filename="data/meta/reads.tsv"`,
  `filename="data/meta/samples.tsv"`, `filename="src/01_count_reads.sh"`,
  `filename="data/README.md"`, `filename="README.md"`,
  `filename="NOTEBOOK.md"`.
- No `$` prompt; code annotations on each new command; captured output in
  `.console` blocks (`md5sum -c` success and both kinds of failure,
  `ls -l data/ref`, the permission errors on the toy folder, the log, the
  macOS recursive-delete capture).
- Downloads use URLs pinned to one commit of `nf-core/test-datasets`
  (`9dd6d014f560e182047992834a8d267214fbccd1`, the `rnaseq` branch head
  on 2026-11-09), so the files cannot change under the reader. Kept in
  `_variables.yml` (e.g., `testdata-url`) so one line changes when the
  book re-pins.
- **Bash everywhere:** `md5sum`, `sha256sum` are GNU coreutils, present
  on macOS from Chapter 1's setup. No `md5` (BSD) variant. The script
  uses `date` format strings that work with any `date` (*checked*: GNU
  `date -Is` failed where BSD `date` came first on `PATH`).
- No OS tabsets expected. Possible exception: WSL readers who want to
  see the project in Windows Explorer (`explorer.exe .`) get one line,
  with Chapter 1's pitfall that work stays in the Linux home.
- Supplied script (*checked* 2026-11-17, 21 lines):

  ```bash
  #!/usr/bin/env bash
  # 01_count_reads.sh: check the raw FASTQ files, then count their reads.
  # Run from the project folder:  pixi run bash src/01_count_reads.sh
  set -euo pipefail

  mkdir -p results logs
  log="$(mktemp "logs/01_count_reads_$(date +%Y-%m-%dT%H%M%S)_XXXX.log")"

  {
    echo "started:  $(date "+%Y-%m-%d %H:%M:%S %z")"
    echo "host:     $(hostname)"
    echo "script:   $(md5sum src/01_count_reads.sh)"
    echo "seqkit:   $(seqkit version)"
    echo "checking inputs against data/raw/checksums.md5:"
    (cd data/raw && md5sum -c checksums.md5)
    echo "command:  seqkit stats -T data/raw/*.fastq.gz"
    seqkit stats --quiet -T data/raw/*.fastq.gz > results/read_counts.tsv.tmp
    mv results/read_counts.tsv.tmp results/read_counts.tsv
    echo "output:   $(md5sum results/read_counts.tsv)"
    echo "finished: $(date "+%Y-%m-%d %H:%M:%S %z")"
  } 2>&1 | tee "$log"
  ```

  Readers run it, not write it; Chapter 8 teaches every line. A log with
  no `finished:` line means the run failed. `--quiet` drops seqkit's
  progress line from the log. The shebang and `chmod +x` wait for
  Chapter 7; here it runs as `bash src/…` through `pixi run`. Captured
  log (success):

  ```
  started:  2026-11-17 11:08:55 -0600
  host:     <laptop>
  script:   76fa8eb6…  src/01_count_reads.sh
  seqkit:   seqkit v2.14.0
  checking inputs against data/raw/checksums.md5:
  SRR6357070_1.fastq.gz: OK
  SRR6357070_2.fastq.gz: OK
  command:  seqkit stats -T data/raw/*.fastq.gz
  output:   e1d81de7…  results/read_counts.tsv
  finished: 2026-11-17 11:08:55 -0600
  ```

### Plots

None.

### Animation (manim)

None. `fig-symlink` covers the one sequence as a stepped SVG.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | Keep inputs, code, and outputs apart, so you can rebuild outputs from preserved inputs, code, settings, and software records. That gives you the ingredients for reproducing an analysis; rebuilding it (exercise 4) is the test |
| 4 | Key idea | Raw data is read-only: check it once with checksums, protect it, and never edit it; every change happens in a script that writes somewhere else |
| 4 | Misconception | "Matching checksums mean my data are correct" (`checksum-proves-correct`) |
| 5 | Pitfall | Remove a link with `unlink data/ref` or `rm data/ref`, never `rm -r data/ref/`: on macOS that deleted the shared folder the link pointed to (captured) |
| 5 | Misconception | "A symlink is a copy" (`symlink-is-copy`); may merge with the pitfall if the screen gets crowded |
| 6 | Pitfall | Scratch is purged and not backed up; check which other areas are, and for how long (`cluster-is-backed-up`) |
| 6 | Misconception | "My Dropbox/OneDrive folder is my backup" (`sync-is-backup`) |
| 8 | Key idea | Record provenance when the file is made: source, version, checksum, script, command, software, log. It costs a minute now and cannot be rebuilt later |
| 8 | Misconception | "I'll remember where this file came from" (`ill-remember`) |
| 9 | Background | FAIR principles, with `tbl-fair` |

Section 6 has three callouts; keep them on separate screens or merge the
two misconceptions into the text with the table.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: You delete `results/read_counts.tsv` by mistake. What do you need
  to get it back? (*Rerun the script on `data/raw/` with the same
  environment: nothing else. For a large published analysis, rebuilding
  could cost days or need things no longer available, which is why
  important final results are backed up too.*)
- §3: In what order does `ls` list `run1.sh`, `run2.sh`, `run10.sh`? How
  would you rename them? (*`run1.sh`, `run10.sh`, `run2.sh`; `01_…`,
  `02_…`, `10_…`, with names that say what each does.*)
- §4: `md5sum -c` prints `FAILED` for a file you just copied from the
  cluster. What happened, and what do you do? (*The bytes differ from
  the original, usually an incomplete transfer: copy it again and
  recheck, and do not analyse it. If instead it says `FAILED open or
  read`, the file is missing or you are in the wrong folder.*)
- §5: You run `unlink data/ref`. Is the reference genome gone? What must
  you do on a second machine to use the project there? (*No, only the
  link. On the second machine, recreate the link to that machine's copy
  of the same reference, identified by its release and checksums in
  `data/README.md`.*)
- §6: Your raw FASTQ files are in cluster scratch and in a OneDrive
  folder on your laptop. Is that a backup you can rely on? What would
  you need to check? (*Not as it stands: scratch is purged and not
  backed up, and OneDrive copies deletions. Check how long OneDrive keeps
  old versions, whether the facility or SRA keeps the originals, and put
  a copy in backed-up storage.*)
- §7: The upstream sheet has two rows labelled `WT_REP1`. Are they two
  runs of one biological sample? How would you find out? (*Not here:
  ENA lists them as different biological samples, wild-type replicates
  1 and 2. The test sheet groups them to test merging. Check the archive
  record, not the label.*)
- §8: A reviewer asks which version of seqkit made `read_counts.tsv`.
  Where in the project is the answer? (*The run's log in `logs/`, and
  `pixi.lock`.*)
- §9: Which FAIR principle does citing `SRR6357070` and `GSE110004` in
  your README support? (*Findable, through persistent identifiers; also
  Reusable.*)

End-of-chapter exercises (core chapter, so required; all adapt supplied
commands or templates; practice files go in `~/bioinf-ch03/`):

1. **Rename a messy folder.** A supplied command creates
   `~/bioinf-ch03/messy/` with eight badly named files (spaces, `final`,
   unpadded numbers, an ambiguous date, a `.txt` that is really a TSV).
   Propose new names in a table, then apply them with supplied `mv`
   commands adapted to your names. For the ambiguous date, say what you
   would ask. (*Answer key: one good set of names, and why `ls` now
   sorts them in order.*)
2. **Catch a broken transfer.** Make a truncated copy in the practice
   folder (`head -c 1000000 ~/bioinf-book/data/raw/SRR6357070_1.fastq.gz
   > ~/bioinf-ch03/practice/SRR6357070_1.fastq.gz`), copy
   `checksums.md5` beside it, and run `md5sum -c` there (expected:
   `FAILED` for the copy, `FAILED open or read` for the missing R2; both
   are deliberate). Then run `gzip -t` on the copy. Which check caught
   it, and which would catch a file that is complete but the wrong
   sample? (*Both catch truncation; only the checksum, compared against
   the facility's list, catches a wrong file that is still valid gzip.
   Neither tells you whether the facility's own file was right:
   `checksum-proves-correct`.*)
3. **Labels vs records.** From the supplied ENA capture (run, GEO
   sample, sample title, layout for all seven runs), add `geo_sample`
   and `condition` columns to a copy of the upstream sheet in the
   practice folder. How many biological samples are there, how many
   runs are really paired-end, and why might a test fixture group them
   differently? What goes wrong if a sample ID in one table has a
   trailing space? (*7 samples, all paired; the fixture tests merging
   and single-end input. A trailing space makes a different ID, so the
   records fail to match: Chapter 14 shows how to detect it.*)
4. **Rebuild and compare.** Save a copy of the result outside
   `results/` (`cp results/read_counts.tsv ~/bioinf-ch03/read_counts_before.tsv`),
   delete `results/`, rerun `pixi run bash src/01_count_reads.sh`, and
   compare with `cmp ~/bioinf-ch03/read_counts_before.tsv
   results/read_counts.tsv` (no output means the files are identical).
   Look at `logs/`: both runs' logs are there. Add a `NOTEBOOK.md` entry
   for today. (*Identical; the two logs differ in date and time, which
   is why outputs and logs are kept apart.*)
5. **(Cluster readers)** Create the same layout in your project storage,
   link a reference your site or lab already provides (Appendix A) or
   the test reference, and fill in your column of `tbl-storage-backup`
   from your site's docs, including who restores files. (*No-cluster
   readers: fill in the laptop rows.*)

## Examples and data

- Toy examples: the sorting puzzle and messy folder (exercise 1), the
  protected toy folder and toy link in `~/bioinf-ch03/practice/`, a
  truncated copy (exercise 2), one changed byte for `fig-checksum`.
- Downloads pinned to commit `9dd6d014f560e182047992834a8d267214fbccd1`
  of `nf-core/test-datasets` (`rnaseq` branch head, 2026-11-09), URL
  pattern `https://raw.githubusercontent.com/nf-core/test-datasets/<commit>/<path>`.
  All five files at that commit are byte-identical to the ones already
  recorded (*checked* 2026-11-17). Chapter 1 used the branch URL;
  decided to move every chapter to this commit (open question 8).

  | File | Path | Size (bytes) | MD5 | SHA-256 |
  |:-----|:-----|-------------:|:----|:--------|
  | `SRR6357070_1.fastq.gz` | `testdata/GSE110004/` | 2,239,317 | `d19f3c7a8b4016fa641458257b99a1a1` | `3f50541f…40ebe7` |
  | `SRR6357070_2.fastq.gz` | `testdata/GSE110004/` | 2,232,117 | `d126cc66ed169f69af2c07da0dd73e02` | `8590e1e0…60aaf4` |
  | `samplesheet_test.csv` | `samplesheet/v3.10/` | 1,335 | `fb28ab0a8cda268b2befd974804b2925` | `beeb7811b14bfa973233616625a9648ba649736d97b2e84af51d619ac89691c4` |
  | `genome.fa.gz` | `reference/` | 71,440 | `4222a07bf01b12782245e0ff774459fe` | `dbfd9767961571e91a42022a728d7bcf5022c1078ee361cf475986520e2bc999` |
  | `genes.gtf.gz` | `reference/` | 10,452 | `504334f6741ee771c665ae845429087f` | `72dadd0ce0b719fa71f849f35e6b3c4475f3edc63cf9d3f60eb7911c2a787aaa` |

  `genome.fa.gz` holds one sequence, `>I` (yeast chromosome I only).
  Last commits touching each file: reads `58ec9dc` (2021-04-12), sheet
  `0a8d404` (2023-03-24), genome `bae247f` (2020-08-24), GTF `cfc925e`
  (2023-11-16). The `v3.10` folder name is nf-core's; which pipeline
  release the book runs is chosen and tested in Chapter 26.
- ENA records for the seven runs (*checked* 2026-11-17), for exercise 3
  and §7's twist: SRR6357070–75 are GSM2879618–23, wild type replicates
  1–3 (070–072) and "Rap1-AID degron no induction" replicates 1–3
  (073–075); SRR6357076 is GSM2879624, "Rap1-AID degron induction 30
  minutes" replicate 1. All `PAIRED`. Supplied as a dated capture in
  case the pages change.
- Add rows to the book's `data/README.md` for the sample sheet and the
  two reference files, with MD5 and SHA-256 and the pinned commit.
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
  through it is safe." It is another route to the same data: editing
  through it edits the original, and recursive deletes through it can
  remove the target (captured on macOS). Remove only the link with
  `unlink` or `rm` without a trailing slash. [callout/pitfall, §5;
  `fig-symlink`; self-check]
- `readonly-cant-delete`: "A read-only file can't be deleted." Deleting
  is controlled by the folder's permissions; protect the folder too.
  [text, §4; Chapter 7 head-on]
- `cluster-is-backed-up`: "Everything on the cluster is backed up."
  Scratch is purged and not backed up; which other areas are backed up,
  and for how long, differs by site. [pitfall, §6;
  `tbl-storage-backup`; Chapter 10]
- `sync-is-backup`: "My Dropbox/OneDrive/Google Drive folder is my
  backup." Sync copies deletions and overwrites; it is one copy in two
  places, unless version history is kept and you know for how long.
  [callout, §6; self-check]
- `ill-remember`: "I'll remember where this file came from and how I
  made it." Weeks later no one does; record source, version, checksum,
  script, command, and log when the file is made. [callout, §8]

## Links to other chapters and books

- Builds on: Chapter 1 (the FASTQ files in `~/bioinf-ch01`, the
  hand-made `fastq_summary.txt`, `curl -fLO`, `gzip -t`); Chapter 2
  (`~/bioinf-book`, pixi, `pixi run`, VS Code and nano for editing,
  `README.md` from exercise 3, project vs home storage on clusters).
- Leads to: Chapter 4 (finding the log; a good help request quotes the
  log and versions); Chapter 5 (paths, quoting, `ln -s`, `find`);
  Chapter 6 (`>` vs `>>`, `cut | sort | uniq` on the sample sheet);
  Chapter 7 (permissions, `chmod`, shebang); Chapter 8 (the script line
  by line; numbered scripts as a pipeline; first git commit of `src/`);
  Chapter 9 (checksums after `rsync`/Globus; moving a project); Chapter
  10 (storage tiers, quotas, purges); Chapter 12 (Quarto: the rendered
  summary in the recurring project); Chapter 14 (sample-sheet pitfalls,
  joining run and sample tables); Chapter 15 (reference releases,
  chromosome names); Chapter 20 (downloading from SRA/ENA with their
  MD5s; licenses and citation of public data); Chapter 21 (git,
  `.gitignore` keeping `data/` and `results/` out); Chapter 22 (remotes
  as an off-machine copy of code); Chapter 23 (provenance: versions,
  parameters, seeds); Chapter 26 (nf-core sample sheets, merging runs,
  pipeline versions and reports); Appendix A (site storage, backups,
  reference collections). Other books start from this layout and adapt
  it to their tools.

## Official links to include

- GNU coreutils manual: `md5sum`, `sha256sum` (`--check`), `ln`, `chmod`
  (gnu.org/software/coreutils)
- ISO 8601 date format: iso.org (ISO 8601 page)
- ENA: run records and file reports with MD5 (ebi.ac.uk/ena); NCBI SRA
  (ncbi.nlm.nih.gov/sra); GEO GSE110004
- nf-core/test-datasets (`rnaseq` branch, and the pinned commit);
  nf-core/rnaseq usage page, "multiple runs of the same sample"
  (versioned docs, nf-co.re/rnaseq)
- GO FAIR / FAIR principles: go-fair.org
- Git book, "Getting a Git Repository" (git-scm.com), for "a repository
  can live on the same disk"
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
- Shotts, *The Linux Command Line*: the chapters on links and
  permissions, for readers who want them before Chapters 5 and 7.
- Moved to Chapter 14: Broman & Woo 2018, "Data organization in
  spreadsheets", *Am Stat*, doi:10.1080/00031305.2017.1375989.

## Austin's notes

-

## Decisions (2026-11-17, open questions round)

Austin's choices (Codex's review agreed with each):

- **Dataset description: correct all three levels.** Original study
  (GSE110004), nf-core test fixture (5 sample labels, 7 runs, 4 used
  paired-end, 3 used single-end, every run sub-sampled to 50,000 reads
  or pairs: all 10 files counted 2026-11-17), and the book's own files
  (SRR6357070). Applied to `PLAN_CHAPTERS.md` (Conventions → Data) and
  `data/README.md`, then corrected again after the ENA check (see
  *Review responses*: the 7 runs are 7 biological samples, all
  paired). The samples' biology stays with Transcriptomics.
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

## Review responses (2026-11-17)

Codex (`chapter_03_codex_review.md`). Each testable claim was rechecked
before changing the plan (scratch copy of the project, the book
environment, the pinned files, ENA). Accepted and applied above:

- **1. Checksum working directory:** confirmed (`FAILED open or read`
  from the project root). The check now runs inside `data/raw/`, with
  the manifest's bare names kept as facilities ship them.
- **2. A manifest for the files the project holds:** the upstream sheet
  is saved unchanged as `samplesheet_upstream.csv`; new `reads.tsv`
  (local files) and `samples.tsv` (biology, from the archive record).
  Fixed my counting error: three rows but **two** sample labels lack
  `fastq_2`. Rules reworded (one row per run; sample IDs agree across
  tables; IDs need not match file names).
  **Found while checking:** ENA lists the seven runs as seven different
  biological samples (GSM2879618–24), all paired-end. The fixture's
  "two runs of `WT_REP1`" are wild-type replicates 1 and 2. This became
  §7's twist and exercise 3, and corrected the description in
  `PLAN_CHAPTERS.md` and `data/README.md` again.
- **3. Logging:** script rewritten and tested: inputs checked against
  the manifest, date-and-time log name (two same-day runs keep two
  logs), seqkit's messages in the log, script checksum and command
  recorded, result written to a temporary file and moved only on
  success, output checksum recorded. A corrupted input stopped the run,
  kept the old result, and left the failure in the log. "About ten
  lines" corrected to about twenty. The reference and sample sheet are
  shown as project records, not inputs to this result.
- **4. Results and backup:** "needs no backup" replaced: rebuildable is
  the goal; important final results, logs, and records are backed up;
  "ingredients for reproducing", tested by exercise 4.
- **5. Symlinks:** Codex reproduced the macOS deletion with both GNU and
  macOS `rm`. The pitfall stays as captured output labelled with the
  platform; "either way the data are gone" removed; Linux/WSL stays
  open. `fig-symlink` is now four states from an intact link, with
  edits and `unlink` shown on a toy link only.
- **6. Moving a project:** the migration steps (copy project, reinstall
  from the lockfile, recreate the link to that machine's copy, which
  `data/README.md` identifies) replace the claim that absolute links
  survive a move; someone must own the target's preservation.
- **7. Immutable sources:** downloads pinned to commit `9dd6d01`
  (files byte-identical to the recorded ones); checksums supplied for
  the reference and sheet too; "v3.10 matches current nf-core/rnaseq"
  dropped (Chapter 26 chooses the release).
- **Teaching points:** permissions shown on a toy folder first and
  described as guarding against accidents; recovery per mate file and
  for repeat visits; `~/bioinf-ch01` keeps `fastq_summary.txt`; practice
  files in `~/bioinf-ch03/`, not `/tmp`; exercise 4 saves outside
  `results/` and says what `cmp`'s silence means; two kinds of checksum
  failure told apart; join answer says "fail to match", not "silently
  drop"; backup table gains recovery period and who restores; git
  wording; the OneDrive self-check asks what to verify; allowed
  characters listed; meaningful version labels allowed; `11-3-25`
  left ambiguous; sample-sheet figure shows sample → run → files; CSV
  viewed in VS Code, not `column`; FAIR habits "support" FAIR, and
  accessible can mean behind a login; Broman & Woo moved to Chapter 14;
  backups no longer the first thing cut for length.

Where I differ from the review:

- **Running the checksum check:** Codex suggested a one-line subshell,
  `(cd data/raw && md5sum -c checksums.md5)`. In the chapter I use
  three plain lines (`cd data/raw`, `md5sum -c …`, `cd ~/bioinf-book`):
  readers already know `cd`, and parentheses would need explaining in
  Chapter 3. The supplied script, which readers do not have to read
  line by line, uses the subshell.
- **Log names:** Codex asked for "a timestamp plus a collision
  safeguard". I first judged a timestamp to the second enough; the
  chapter review (below) showed it is not, and the script now uses
  `mktemp`.

## Drafting notes (2026-11-17)

Every command in the chapter was rerun in a scratch home folder (macOS,
GNU coreutils 9.11, the book environment); captured outputs come from
that run, with paths and user names replaced by `/home/you` and `you`.
Where the chapter differs from the plan above:

- **Shared reference protected** with `chmod a-w` (files and folder),
  as a lab would. Tested: `rm -r link/` on a protected target stops
  with `Permission denied`; unprotected, it deleted the target folder
  silently (exit 0) and left a broken link. The pitfall says both.
  `fig-symlink` step 3 is therefore a *refused* write through the link
  (what readers would actually see); the successful edit through a link
  is shown on the toy link only.
- **Toy protection demo uses `rm -f`**: interactive GNU `rm` asks before
  removing a write-protected file, which would stall readers at a
  prompt; `-f` is what scripts do, and the text says so.
- **Sorting puzzle names changed** (`run1/2/10.sh`, `9-15-25` and
  `10-2-26` counts, `final.txt`, `Final FINAL (2).txt`). `ls` order
  depends on the locale: on a Mac `run1, run10, run2`; glibc locales may
  put `run10` first. The two lessons (run10 before run2; Oct 2026 before
  Sep 2025) hold in every locale; the text says the rest may differ.
  `11-3-25 counts.csv` stays as the ambiguous-date example in the text
  and exercise 1.
- **`reads.tsv` and `samples.tsv` written with `printf`**, not pasted:
  pasted tabs are not reliable. Tab output shown as a terminal shows it
  (8-column tab stops), with a note to view it in VS Code.
- **Script pasted only**, not also downloadable: there is no place to
  host project files yet. Add one if readers ask.
- **Backups table** filled from SCINet's storage guide (page updated
  2026-01-21), ISU's HPC file storage guide, and Nova's login banner
  (captured in Chapter 2), all checked 2026-11-17. Gaps are written
  "not stated" (SCINet: no backup for any cluster storage, "Cluster
  storage is not backed up"; Juno backup status, Nova home and `/lss`
  backup details not stated; Nova `/work` has daily ZFS snapshots, 7
  kept, restored by the file-system admins). Appendix A is still a stub
  and should take the full version.
- **Pinned URLs done:** `testdata-url` and `testdata-page` in
  `_variables.yml`; Chapters 1 and 2 switched (rendered and checked).
  `scripts/ch01_file_sizes.R` still reads the branch (its BAMs are
  recorded at their own commits).
- **Also done:** six misconceptions in `misconceptions.yml`; sample
  sheet, genome, and GTF rows plus the ENA records in `data/README.md`;
  `wilson2017good`, `noble2009quick`, `wilkinson2016fair` in
  `references.bib` (BibTeX from the DOIs).
- **Not done:** the WSL `explorer.exe .` line (no need found); links to
  the nf-core/rnaseq usage page and the Git book (the chapter points to
  @sec-nf-core and @sec-git instead).

## Chapter review responses (2026-11-17)

Codex's review of the written chapter
(`reviews/chapter_03_codex_review.md`). All four findings rechecked and
accepted:

- **1. Same-second runs shared one log** (medium). Reproduced: three
  quick runs without `pixi run` left one log (through `pixi run` its
  start-up took over a second here, so they did not collide, but
  readers in `pixi shell` would hit it). The script now names the log with
  `mktemp "logs/01_count_reads_<date-time>_XXXX.log"`: three runs in one
  second gave three logs on macOS and on Ubuntu. Script MD5 is now
  `76fa8eb6a7b90f212042cfbe6d95cfcc`; result MD5 unchanged. Captured
  log, `ls logs`, summary tree, and exercise 4 answer updated. `mktemp`
  creates logs readable only by you (`-rw-------`); fine for now, revisit
  if labmates need to read logs in shared project storage.
  Chapter 4's captured failed-run log (`chapters/04-getting-help.qmd`)
  recaptured with the new script the same way (R2 moved out of
  `data/raw/`): same lines, new name, time, and script MD5.
- **2. Adding a raw file left `checksums.md5` locked** (medium).
  Reproduced on Ubuntu (append refused after `chmod u+w data/raw`). The
  chapter now gives the four-line recipe: unlock folder and list, add,
  `md5sum -c`, lock again.
- **3. `rm` prompting** (low). Correct: GNU `rm` asks when its input is a
  terminal, even from a script. Wording and the code annotation fixed.
- **4. Case sensitivity** (low). Correct: the WSL home folder is
  case-sensitive like the cluster. Table row reworded ("usually" for
  macOS and Windows folders).

## Open questions

1. ~~Running dataset description~~, 2. ~~MD5 or SHA-256~~,
   3. ~~Simulated shared folder~~, 4. ~~Moving vs copying~~,
   5. ~~Notebook~~: all decided 2026-11-17 (see *Decisions*).
6. ~~Site backup facts~~: filled from official pages 2026-11-17 (see
   *Drafting notes*); the original question follows.
   **Site backup facts** for `tbl-storage-backup` (is SCINet `/project`
   backed up? Nova `/work`? Juno and `/lss` retention? who restores?)
   must come from the sites' current official docs, dated and linked in
   Appendix A, before drafting; nothing here is asserted yet beyond what
   Chapter 2's checks recorded (`/90daydata` and `/ptmp` are purged
   scratch; Nova `/lss` backed up, not on compute nodes).
7. ~~Linux checks~~: done 2026-11-17 in Docker (Ubuntu 24.04, GNU
   coreutils 9.4, non-root user). `rm -r link/` unprotected deleted every
   file inside the target, then failed with `Not a directory` (folder
   left empty; added to the pitfall); protected, `Permission denied`.
   `ls -1` puzzle in en_US.UTF-8: `run10.sh` before `run1.sh`, otherwise
   as on the Mac (text updated). Protection demo, `ls -l data/ref`,
   `ls -ld data/raw`: identical to the chapter. Script with seqkit 2.14.0
   via pixi: identical log, identical result (same MD5), and a corrupted
   input stopped at `FAILED`, exit 1, old result kept. Not tested on WSL
   itself (same Ubuntu userland). Originally: `rm -r link/` on Linux/WSL (behaviour
   not yet known there); the protected-folder demo on Linux/WSL; the
   script and its log on WSL; the `.tsv` metadata files open cleanly in
   VS Code.
8. ~~Chapter 1's download URL.~~ Decided (Austin, 2026-11-17): one
   pinned source for the whole book. When Chapter 3 is drafted, add a
   `_variables.yml` entry (e.g., `testdata-url` =
   `https://raw.githubusercontent.com/nf-core/test-datasets/9dd6d014f560e182047992834a8d267214fbccd1`)
   and switch Chapter 1's downloads, its browser-fallback link, and
   Chapter 2's R2 command to it, so every chapter uses the same commit.
   Files are byte-identical to the branch versions today (*checked*),
   so no captured output changes.
