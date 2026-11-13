---
title: "Computing for Bioinformatics — Chapter Plan"
subtitle: "Draft structure: parts, chapters, topics. Not an outline yet."
date: 2026-11-13
format:
  html:
    toc: true
    toc-depth: 3
    embed-resources: true
---

**Status:** draft for review. Each chapter lists topics only; full chapter
outlines come later. Revised 2026-11-12 after `PLAN_CHAPTERS_codex_review.md`:
Part I shortened, Languages moved before Formats, nf-core before Nextflow
authoring, Trees & clusters dropped, routine troubleshooting / ID checks /
provenance added inside existing chapters. Revised 2026-11-13 after
`PLAN_CHAPTERS_review_agy.md`: core/overview/optional label on every
chapter, scope notes for Parts IV and VII, HPC quota and cache pitfalls.

**Guiding idea:** most readers will work on a Linux HPC cluster (SCINet
Ceres/Atlas, ISU Nova, and similar), with a laptop for editing, small
analyses (e.g., a small DESeq2 run), and collecting data. Teach Linux first;
mention macOS and Windows only where they differ.

**Audience boundary:** readers mostly *use* existing tools, packages, and
pipelines. Using code (calling functions, adapting a supplied script, reading
an error, checking inputs) is taught throughout, where it is needed.
Developing code (writing reusable functions, debuggers, automated tests) is
optional and lives in Part VIII.

## Conventions for every chapter

- **Primary setup [decided]:** one book environment with **pixi**, installed
  in Chapter 2, and **VS Code** (with Remote-SSH) as the primary editor.
  Alternatives (Conda, uv, renv/rv, RStudio, Positron, Jupyter) appear in
  compact comparisons, not as choices readers must make before continuing.
  On a managed cluster, say when the site's modules/containers replace it.
- **Labels:** every chapter heading carries one label, so readers know
  what to work through now and what to keep as reference for later:
  - **core**: work through it, with exercises. The core chapters together
    form the first-pass path (about 24 chapters), shown in the preface.
  - **overview**: read for understanding and recognition; no required
    exercises. Explains why tools behave as they do.
  - **optional**: reference for later, when a reader needs it (scale,
    writing code, other platforms).

  A mixed chapter marks its overview or optional sections inline.
- **Outcome and check:** each chapter states one practical outcome and one
  check readers can perform themselves. Early exercises ask readers to run,
  inspect, and adapt supplied examples, not to write from a blank file.
- **Where commands run:** label every command as laptop, login node, or
  compute node.
- **No cluster required:** readers without cluster access can complete the
  small local examples and read captured HPC output. SCINet/Nova details go
  in site-specific notes.
- **Data:** toy examples small enough to check by hand, plus one running
  dataset **[decided]**: the yeast (*S. cerevisiae*) paired-end RNA-seq
  subset used by nf-core/rnaseq's test profile (GEO GSE110004; Wu et al.
  2018, *Mol Cell*, doi:10.1016/j.molcel.2018.10.018): wild type vs Rap1
  degron, 3 replicates each, 50,000 read pairs per sample, with sample
  sheet and a sub-sampled R64-1-1 reference, from the `rnaseq` branch of
  `nf-core/test-datasets`. Computing runs and checks it; biological
  interpretation stays in Transcriptomics. Separate tiny files for formats
  and algorithms the running dataset does not illustrate (e.g., BAM, VCF).
- **Recurring project:** a small reproducible project started in Chapter 3
  and improved as skills appear: input provenance, metadata, scripts or
  workflow config, environment info, logs, rendered summary.
- **Further reading:** annotated, each pick with a purpose. Recurring
  anchors: Shotts, *The Linux Command Line*; Software Carpentry, *The Unix
  Shell*; official Nextflow training.

---

## Part I — Getting set up

Short: get readers to a first successful command quickly.

### 1. Orientation: computers and where you compute [core]

- CPU, cores vs threads; RAM vs disk; I/O as the usual bottleneck
- Typical data sizes (FASTQ, BAM, VCF, count matrix)
- macOS, Windows, Linux; Linux distributions briefly
- Laptop vs HPC cluster vs cloud: what runs where
- Windows: WSL2; macOS: Terminal, Homebrew
- Getting an account on SCINet / a university cluster
- Guided first session: open a terminal, look at a small FASTQ file, save a
  one-line summary (commands explained in Part II)

### 2. Book setup and editors [core]

- Install pixi and the book environment; run a first example
- VS Code as the primary editor, including Remote-SSH
- Just enough SSH to connect to a cluster (full treatment in Chapter 9)
- Pitfall: some clusters restrict the VS Code server on login nodes; fall
  back to Open OnDemand or a compute-node session
- nano and vim basics for editing on a server
- Reference table: RStudio / Positron, Jupyter, Quarto, Open OnDemand

### 3. Organizing projects and data [core]

- Project folder structure (`src/`, `data/`, `results/`, …)
- File and script naming (`00_`, `01_`, …; no spaces)
- Raw data is read-only; link shared lab data and references into a project
  (symlinks) rather than copying them
- Checksums (`md5sum`) for raw data
- Backups (3-2-1); scratch is not a backup
- Sample sheets and metadata as first-class files
- Provenance: link each output to input accessions/checksums, reference
  release, software or pipeline version, parameters, and logs
- READMEs and a lab-notebook habit
- FAIR principles (brief)
- Start the recurring project

### 4. Getting help [core]

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

---

## Part II — The Linux command line

### 5. Shell basics [core]

- What a shell is; bash
- Filesystem tree, paths (absolute vs relative), home directory
- Navigating, creating, copying, moving, deleting
- Symbolic links (`ln -s`)
- Wildcards and tab completion; quoting paths
- Finding files (`find`)
- Viewing files: `cat`, `less`, `head`, `tail`
- Command history and shortcuts

### 6. Text tools and pipes [core]

- Pipes and redirection; standard output vs standard error
- `>` overwrites: destructive redirection
- `grep`, `cut`, `sort`, `uniq`, `wc`
- `sed` and `awk` basics
- Regular expressions (shared across shell, R, Python)
- Working with compressed files (`zcat`, `gzip`)

### 7. The Linux system [core]

- Users, groups, permissions, `chmod`
- Executable files and shebang lines
- `PATH` and environment variables
- `.bashrc` vs `.bash_profile`
- Processes: `ps`, `top`; interrupting (Ctrl-C) and `kill`
- Disk usage: `df`, `du`
- GNU (Linux) vs BSD (macOS) tools
- Line endings (LF vs CRLF)

### 8. Shell scripts [core]

- Variables, quoting, loops, conditionals
- Script arguments
- `set -euo pipefail`: what it catches and what it does not
- Logging output and errors
- Numbered scripts as a simple pipeline
- Minimal git routine for saved scripts: check changes, commit, recover a
  previous version (full treatment in Chapter 21)

### 9. Working remotely [core]

- SSH and SSH keys; `~/.ssh/config`; jump hosts (`ProxyJump`)
- tmux / screen so work survives a dropped connection
- Moving data: `scp`, `rsync`, Globus
- Checksums to confirm a transfer

### 10. HPC and SLURM [core]

- Cluster anatomy: login vs compute nodes
- Environment modules (`module load`, Lmod)
- Storage tiers: home, project, scratch; quotas (site quota command) and
  purges
- File-count (inode) quotas: millions of small files (a Nextflow `work/`
  directory, environments in `$HOME`) can fill an account that has bytes
  to spare
- `sbatch` scripts and resource requests
- Estimating memory, time, and disk for a job; measuring a real one
- Interactive jobs
- Job arrays
- Monitoring and accounting (`squeue`, `sacct`, `seff`); cancelling
  (`scancel`)
- A running process vs a submitted job
- GPU partitions (brief)
- Etiquette: no heavy work on login nodes

---

## Part III — Languages

Goal: readers recognize and adapt a small script in both R and Python;
sustained practice in one is a fine first pass. Calling functions is core;
writing them is Part VIII.

### 11. The language landscape [overview]

- Bash as glue for running tools
- R and Python: who uses which, and for what
- Julia (brief)
- Perl as history
- Compiled languages (C/C++, Rust, Java): what your tools are written in
- Building tools from source (`make`, `cmake`) briefly
- The series' division of labour

### 12. R essentials [core]

- Running R scripts vs interactive work
- Objects and assignment; calling a function, changing a named argument,
  saving the result
- Types: strings, numbers, logicals, missing values (`NA`)
- Vectors, lists, matrices, data frames
- Selecting rows/columns; filtering with a condition; checking dimensions
  and sample names
- Packages: CRAN and Bioconductor; reading a vignette
- Base R vs tidyverse
- Running a supplied script: adjust paths, filenames, documented settings
- Reading an error; restart and run from a clean session
- Reading files and making a quick plot; rendering one small Quarto report

### 13. Python essentials [core]

- Running Python scripts vs interactive work
- Objects and assignment; calling a function with keyword arguments
- Types: strings, numbers, booleans, missing values (`None`, `NaN`)
- Lists, dicts, data frames (pandas / polars)
- Selecting and filtering; checking shape and sample names
- Packages: PyPI and Bioconda
- Biopython and pysam (brief)
- Running a supplied script; reading a traceback for the line that failed
- Reading files and making a quick plot

---

## Part IV — Data, formats, and references

Use format-aware tools for structured biological data. Focus on file
anatomy, coordinates, indexing, and safe manipulation; read QC, trimming,
alignment, and variant calling belong to the Genomics book (series
`PLAN.md`: shared material has one owner). mzML: a short recognition box
linking to the Proteomics & Metabolomics book.

### 14. Tabular data [core]

- CSV vs TSV; why bioinformatics uses tabs
- Tidy data
- Spreadsheet pitfalls (gene names turned into dates)
- Identifiers as text; missing or duplicate sample IDs
- Joining counts to metadata: unmatched rows, row multiplication, order
- Missing value vs zero
- Reading and writing tables in R and Python, including gzipped files

### 15. Sequence formats: FASTA and FASTQ [core]

- Which reference? Genome assemblies and versions; mixing builds by
  accident; chromosome naming (`chr1` vs `1`)
- FASTA structure; `.fai` index
- FASTQ structure
- Quality scores and Phred encoding (ASCII basics here only)
- Paired-end files
- Candidate template chapter (series `PLAN.md` §8)

### 16. Alignment formats: SAM, BAM, CRAM [core]

- SAM fields and flags
- BAM and CRAM: binary and compressed
- `samtools` basics
- Sorting and indexing (`.bai`)
- A BAM, its index, and its reference must stay matched

### 17. Intervals, annotation, and variants [core]

- BED, GFF3, GTF
- 0-based vs 1-based coordinates, shown on a tiny interval
- VCF structure
- `bgzip` and `tabix`
- `bedtools` basics

### 18. Efficient data formats [overview]

- Text vs binary
- R and Python native formats (`.rds`, pickle)
- Arrow and Parquet
- HDF5-based formats (e.g., `.h5ad`) briefly

### 19. Databases (basics) [core]

- What a relational database is
- Core SQL: `SELECT`, `WHERE`, `JOIN`
- SQLite and DuckDB
- Querying Parquet files with DuckDB
- Where databases sit in bioinformatics (annotation packages, Ensembl)

### 20. Reference data and public repositories [core]

- Ensembl, NCBI, UCSC: where references come from
- Basic downloads with `curl` / `wget`; verify the file and record its
  source
- Downloading reads: SRA, ENA, `fasterq-dump`
- NCBI Datasets, GEO
- Programmatic access (Entrez, biomaRt, REST APIs)
- Licenses and citation for public data

---

## Part V — Reproducibility

### 21. Version control with git [core]

- Why version control
- Repositories, commits, history (builds on Chapter 8's routine)
- `.gitignore`; keep data and secrets out of repos
- Branches and merging
- Undoing mistakes

### 22. GitHub and collaboration [core]

- Remotes: GitHub, GitLab, Bitbucket, Codeberg
- Issues; asking for help on a tool's repo
- Pull requests and code review (overview)
- Forks (overview)
- Licensing your code
- Archiving with Zenodo DOIs; citing software

### 23. Software environments [core]

- Why environments; dependency conflicts
- How the book's pixi environment works (set up in Chapter 2)
- Conda and Bioconda
- uv and `pyproject.toml`
- renv / rv for R
- Lockfiles
- Recording versions, parameters, and random seeds (provenance)
- HPC pitfall: package caches default to `$HOME` and fill its quota; move
  them to project storage

### 24. Containers [core]

- What a container is (vs a virtual machine)
- Docker
- Apptainer on HPC
- BioContainers and Seqera Containers
- Image caches on HPC (`APPTAINER_CACHEDIR`, Nextflow's image cache) on
  project or scratch storage, not `$HOME`
- When to use containers vs environments

---

## Part VI — Workflows

Core outcome: run and check an existing pipeline. Writing workflows is
optional.

### 25. Why workflow managers [core]

- From numbered scripts to a workflow
- Dependencies and re-running only what changed
- Make basics
- Overview of workflow managers

### 26. Running nf-core pipelines [core]

- What nf-core and Nextflow are
- Running a pipeline: sample sheets, parameters, profiles, resources
- Running on SLURM
- Logs, the work directory, and `-resume` after a failure
- Reading the outputs (MultiQC)
- Choosing pipeline versions; recording and citing them

### 27. Writing Nextflow [optional]

- Processes and channels
- Config files and profiles
- Containers in Nextflow
- Reading and adjusting an existing workflow; a small workflow of your own

### 28. Other workflow systems [overview]

- Snakemake (brief)
- WDL / CWL (Terra, GATK)
- Galaxy as a no-code option

---

## Part VII — Algorithms

High-level ideas: use the tool, explain the idea, no proofs. Frame each idea
around what it explains for a tool user: a parameter, a resource cost, a
build step. Tool-specific detail (e.g., BLAST in depth) lives in the
Genomics and Transcriptomics books. Clustering belongs to Statistics for
Omics; implementation detail to a later Advanced algorithms book.

### 29. Thinking about algorithms [overview]

- Big-O intuition
- Sorting and binary search (why BAMs are sorted and indexed; why
  `samtools sort` needs memory and temp files; why an index makes region
  queries fast)
- Hash tables (k-mer counting)
- Time vs memory trade-offs

### 30. Sequence alignment [overview]

- Dynamic programming intuition
- Global (Needleman–Wunsch) vs local (Smith–Waterman)
- Scoring matrices and gap penalties
- BLAST: seed and extend; E-values vs bit scores; one basic command-line
  query and its tabular output (`-outfmt 6`)

### 31. Indexing genomes [overview]

- Why aligners need an index build step, and why it takes so much memory
  for large genomes
- k-mers
- Suffix arrays
- BWT and FM-index (BWA, Bowtie)
- Minimizers (minimap2)
- Pseudoalignment (brief): trading base-level alignment for speed; link to
  Transcriptomics

### 32. Graphs and assembly [overview]

- Graph basics; trees as graphs (phylogenetic trees mentioned only; full
  treatment in a later Advanced algorithms book)
- Overlap graphs vs de Bruijn graphs
- Why assembly is hard (repeats, errors)

### 33. Probabilistic methods [overview]

Four ideas met inside common tools, each tied to where readers meet it; no
derivations.

- Hidden Markov models (gene finding, profile HMMs, Pfam)
- Expectation–maximization (multi-mapping reads in Salmon / RSEM)
- Sketching: MinHash (Mash, sourmash)
- Bloom filters (k-mer tools)

---

## Part VIII — Advanced topics (optional)

### 34. Writing reusable analysis code [optional]

- Data structures (beyond vectors, lists, dicts)
- Writing functions: inputs, return values, unusual inputs
- Command-line scripts with arguments (argparse, optparse)
- Debugging: breakpoints, stepping through functions, call stacks
- Automated tests; checking results on toy data
- Style and linting

### 35. Performance and parallelism [optional]

- Thread flags: when more threads stop helping
- Embarrassingly parallel work; GNU parallel
- Vectorization in R and Python
- Profiling time and memory

### 36. Numbers and text encodings [optional]

- Floating-point error, integer overflow
- Log-space probabilities (introduced earlier where an example needs it)
- Text encodings beyond ASCII

### 37. GPU computing [optional]

- What GPUs are good at; what CUDA is
- When GPUs help in bioinformatics
- GPU tools (e.g., Parabricks, deep-learning tools)
- Requesting GPUs on SLURM

### 38. Cloud basics [optional]

- What cloud computing is
- Costs and egress; avoiding surprise bills
- Running pipelines in the cloud (AWS Batch, Seqera Platform, Terra)

---

## Appendices

### A. Cluster sites: SCINet and Nova [optional] (confirmed 2026-11-13)

Step-by-step site details, shared by Chapters 1, 9, and 10, so the
chapters stay site-neutral.

- Who can get an account and how to apply; how long approval takes
- Logging in: host names, multi-factor authentication, first login
- Storage areas, quotas, and what is backed up
- Site software: modules, containers, and where pixi fits
- Open OnDemand and VS Code Remote-SSH on each site
- Each site's own documentation and support contacts

### Candidates

- Setup checklist (install everything needed for the book)
- Command cheat sheets (shell, git, SLURM)
- Glossary

---

## Resolved questions

- Running dataset: yeast nf-core/rnaseq test data (see Conventions).
- Databases: stays in Part IV as a core chapter (ch. 19).
- Phylogenetic trees: mentioned in ch. 32 only; proper treatment belongs to
  the later Advanced algorithms book (series `PLAN.md` §5, "Later").

## Open questions

- None at the moment.
