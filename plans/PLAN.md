# PLAN.md

Very raw/basic ideas from Austin. 

## Topics to cover

**not in order** just ideas to cover in the book, later will be finalized

Computing:
- terminology and computer basics
  - CPU cores vs threads, RAM, hard disk, I/O as usual bottleneck
  - estimating job usage in memory, time, hard disk space, etc
- OSs -> Mac, Windows, Linux (distros)
  - Linux basics and structure may be the most important
  - permissions, users, groups, chmod, executable, shebang lines
  - PATH, env variables, .bashrc vs .bash_profile
  - env modules on HPC (module load, Lmod)
  - MacOS BSD vs Linux GNU (homebrew to install GNU, etc)
  - Windows: WSL2, line endings
- moving data
  - Globus
  - scp, rsync
  - checksums (md5sum to confirm)
- regular expressions
  - across languages
- vim or nano basics for editing files
- programming languages overview
  - cover most used in bioinformatics (can cover perl as a historic example but most do not use any longer)
  - bash (is this considered a language?)
  - R
  - Python
  - Julia??
  - C/C++/Java/Rust for compiled languages but most readers will not use these daily
- HPC & SLURM
  - module load system
  - storage tiers
- folder structures (scr, data, results, subfolder structures) and file name (00_, 01_, 02_, etc for scripts)
- file types
  - flat files (CSV, why bioinformatics uses tab so much)
  - binary formats (in R/Python)
  - Arrow + Parquet (others?)
  - basics of bioinformatics files such as fastq, fasta, sam, bam, etc
  - others: VCF, BED/GFF/GTF, CRAM, compression and indexing (bgzip, tabix, .bai/.fai)
- code editors adn interactive work
  - VS Code
  - RStudio / Positron
  - Jupyter
  - Quarto
  - Open OnDemand
- git, GitHub, GitLab, others (new Antrhopic one?)
- containers (docker, apptainer?, etc)
- environments (uv, conda, toml, etc)
- make and Snakemake (cmake as well)
- NextFlow
  - overview
  - config files
  - nf-core pipelines
- Cloud basics (maybe)

Algorithms:
- 



