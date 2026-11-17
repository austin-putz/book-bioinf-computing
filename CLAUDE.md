# CLAUDE.md

**Computing for Bioinformatics**, the first book in the series
*Bioinformatics: A Worked Approach* (group: Foundations).

This file holds **book-specific decisions only**. Proposals and open questions
live in `plans/` (`plans/PLAN.md`, `plans/PLAN_CHAPTERS.md`); move an item here only
once it is decided.

## Parent directory: read this first

The parent folder `../` (`book-bioinf-series/`) holds the plan for the
**whole series**. Read these before starting work:

- `../CLAUDE.md`: series-wide decisions (audience, platform, naming,
  licensing, data, citations, diagrams, output) and **"Writing and
  visuals"** (examples first, plenty of SVGs and tables, stepped SVG
  before manim, ggplot2 / matplotlib, callouts, official links only).
  Read that section before writing or planning any chapter. They apply
  to this book. Do not copy them here.
- `../PLAN.md`: series plan: every book's outline (§6), which book owns
  which shared topic (§7), pedagogy (§4), and build order (§8).
- `../plans/`: series-level working notes (e.g., `animation-tools.md`).

Sibling repos in `../`:

- `../book-bioinf-theme/`: the shared Quarto theme extension
  (`_extensions/bioinf/`, format `bioinf-html`).
  - `STYLE-GUIDE.md`: usage rules for callouts, self-checks, tables, code
    tiers, figures/SVG, manim, citations (§9), cross-references.
  - `example/`: a test book showing every feature the series uses, one
    page each (`callouts.qmd`, `tables.qmd`, `code.qmd`, `figures.qmd`,
    `animations.qmd`, `references.qmd`). **Copy its `_quarto.yml` as the
    starting template** for this book, including the `bioinf:` block
    (accent, accent-dark, label). That block is the only per-book styling.
- `../book-bioinf-transcriptomics/`: the second book.
- `../../animal-models-test/`: the best existing book outside the series;
  reuse its conventions (`misconceptions.yml`, `notation.yml`, `Makefile`,
  `tests/`, `scripts/`, chapter layout) unless a plan says otherwise.

## What this book is for

The computing foundation every other book in the series assumes: the Linux
command line, HPC and SLURM, R and Python for everyday analysis, file
formats, reproducibility (git, environments, containers), workflows
(nf-core/Nextflow), and a high-level tour of the algorithms behind common
tools.

## Audience

- **MS and new PhD students with little computing background**, mostly from
  biology or animal science. Engineers and computer scientists may read it
  too, but are not the target.
- **Beginner to intermediate.** Readers mostly *use* existing tools,
  packages, and pipelines; they rarely write tools from scratch.
- Most will work on a Linux HPC cluster (e.g., SCINet Ceres/Atlas, ISU
  Nova) with a laptop for editing and small analyses.

## Scope: awareness, not depth

- **Make readers aware of every core item** a working bioinformatician
  meets, so nothing in later books is a first encounter. Each topic gets
  the idea, why it matters, and a hands-on use of the tool.
- **Do not write out full algorithms here.** Defer depth to the book that
  owns the topic (see `../PLAN.md` §7) and link forward.
  - Example: readers learn the idea of BLAST (seeds, extension, E-values in
    plain words) and run a BLAST search. The full BLAST algorithm is a
    chapter in the Genomics book.
  - Same pattern for alignment (Smith-Waterman/Needleman-Wunsch), genome
    indexing (BWT/FM-index), assembly graphs, and HMMs: intuition and a
    tool run here; the algorithm in Genomics, Transcriptomics, or a later
    Advanced Algorithms book.
- **This book owns file formats** for the series (`../PLAN.md` §7). Other
  books link here rather than re-teach them.
- Developing code (reusable functions, debuggers, tests), performance, GPUs,
  and cloud are optional and come last (Part VIII in `plans/PLAN_CHAPTERS.md`).

## Files in this folder

- `CLAUDE.md`: this file. `AGENTS.md` only points here, so other agents
  (Codex, Antigravity `agy`) read the same rules. Edit this file, not the
  pointer.
- `plans/`: all planning docs.
  - `PLAN.md`: Austin's raw topic list.
  - `PLAN_CHAPTERS.md` (+ rendered `.html`): current draft of parts and
    chapters, with conventions for every chapter (core/overview/optional
    labels, pixi + VS Code setup, running dataset). Still a draft.
  - `PLAN_CHAPTERS_codex_review.md`, `PLAN_CHAPTERS_review_agy.md`: outside
    reviews of the chapter plan. Advisory, not decisions.
  - `chapter_NN.md` (+ `.html`): one plan per chapter. See below.
- `_quarto.yml`: the book config, started from the theme's
  `example/_quarto.yml`. Its `chapters:` list mirrors `PLAN_CHAPTERS.md`
  (one `part:` per Part); keep the two in step.
- `index.qmd`: homepage (under-construction notice, audience, how to read,
  linked chapter list with labels, license). Update its chapter list and
  label counts whenever chapters change.
- `chapters/NN-slug.qmd`: one file per chapter, `{#sec-slug}` on the title.
  Unwritten chapters are stubs: an "Under construction" callout, the
  chapter's label, and its planned topics from `PLAN_CHAPTERS.md`.
- `appendices/X-slug.qmd`: confirmed appendices only, listed under
  `appendices:` in `_quarto.yml` (lettered A, B, …; `{#sec-slug}` on the
  title). Candidates stay in `PLAN_CHAPTERS.md`.
- `misconceptions.yml`: what students get wrong, and where the book
  confronts it (id, claim, reality, probe, chapters), as in
  `animal-models-test`. Misconception callouts and self-check probes are
  written from it. When a chapter plan is agreed, add its misconceptions
  here.
- `data/README.md`: every third-party dataset (source, version/commit,
  accession, license, citation, checksums), per series rule. Add a row
  whenever a chapter starts using a new file.
- `setup/`: `pixi.toml` + `pixi.lock`, the book environment readers
  download in Chapter 2. Its download URL is `setup-url` in
  `_variables.yml` (used in chapters as `{{< var setup-url >}}`); point
  it at a release tag, not `main`, once the environment is tagged.
- `scripts/`: code that produces numbers or files shown in the book, named
  by chapter (e.g., `ch01_file_sizes.R` measures Chapter 1's file sizes).
  Code, so MIT. The chapter names the script beside the result.
- `figures/`: hand-drawn SVGs, named after their figure label without
  `fig-` (e.g., `fastq-record.svg` for `fig-fastq-record`).
- `references.qmd` + `references.bib`: References page.
- `reporting.qmd`: "Report an Issue" page, the last sidebar entry, adapted
  from `../../linear-models-in-animal-breeding/reporting.qmd`. Reached from
  the left side only: that entry plus a bug icon in `sidebar: tools:`.
  Do not use `repo-actions` or `issue-url` (they put links in the right
  margin, which Austin does not want). GitHub links and issue forms get
  added once the remote exists.
- `_extensions/bioinf/`: copy of the shared theme (`quarto add`); never
  edit it here, change `book-bioinf-theme` and update.
- `LICENSE` (CC BY-NC-SA 4.0), `LICENSE-CODE` (MIT), `LICENSING.md`
  (plain-English split), as in series `PLAN.md` §7a.

## Book build

- `quarto render` from the root builds `_book/` (git-ignored).
- Repo: public, github.com/austin-putz/book-bioinf-computing. Published
  with GitHub Pages as in `linear-models-in-animal-breeding`:
  `.github/workflows/publish.yml` renders on every push to `main` and
  publishes to the `gh-pages` branch
  (austin-putz.github.io/book-bioinf-computing). Do not commit `_book/`.
- Identity: `bioinf:` accent `#2E6E7E` / `#6FB3C2`, label `CP` (the
  theme's demo values for this book).
- "Under construction" uses a red `callout-important` with
  `icon=false`, on the homepage and every stub. This is the one use of
  that callout outside its "Key idea" meaning; drop it from a chapter once
  it is written.

## Chapter plans (`plans/`)

One planning file per chapter in `plans/`, named `chapter_NN.md` with a
two-digit number matching `PLAN_CHAPTERS.md` (`chapter_01.md` …
`chapter_38.md`). Create them as we reach each chapter, not all at once.

- Start from `plans/_chapter_template.md`: outcome and check, sections,
  examples and data, misconceptions, links, further reading, open questions.
- **"Austin's notes" belongs to Austin.** Never delete or rewrite it; reply
  in the other sections or under "Open questions".
- If a chapter plan changes a chapter's topics, label, or order, update
  `PLAN_CHAPTERS.md` to match.

## Rendering planning docs to HTML

Planning docs are Markdown rendered by Quarto into one self-contained HTML
file beside the source (`embed-resources: true`: no `_files/` folder).

- `plans/_quarto.yml` (a standalone `project: type: default`) supplies the
  HTML format (`toc`, `toc-depth: 3`, `embed-resources: true`), so each file
  needs only `title`, `subtitle`, and `date` in its front matter.
- From `plans/`, render one file with `quarto render chapter_01.md`, or
  every doc with `quarto render`. Files starting with `_` (the template)
  are skipped.
- Re-render after every edit; the HTML does not update itself. The HTML
  is for viewing locally only: `plans/*.html` is git-ignored, so commit
  only the `.md`.
- `plans/` stays standalone after the book's own `_quarto.yml` is added at
  the root, because Quarto uses the nearest `_quarto.yml`.

## Decided

- Primary setup: one book environment with **pixi**, and **VS Code** as the primary editor,
  connected to a cluster by the site's supported route (Remote-SSH, a VS
  Code tunnel, or Open OnDemand; revised 2026-11-13, since Nova and SCINet
  keep VS Code off login nodes). Alternatives appear only in compact
  comparisons.
- **Shell: bash everywhere** (decided 2026-11-13). Commands, outputs, and
  explanations assume bash with GNU tools, as on Linux clusters. macOS
  readers install Homebrew, a current bash, and the GNU tools in Chapter 1
  (gnubin directories first on `PATH` in `~/.bash_profile`) and make bash
  their login shell. Do not write zsh variants. GNU vs BSD differences are
  taught in Chapter 7.
- Running dataset: the yeast (*S. cerevisiae*) paired-end RNA-seq subset
  from nf-core/rnaseq's test profile (GEO GSE110004). Details in
  `PLAN_CHAPTERS.md`.
