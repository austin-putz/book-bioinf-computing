# Review of `PLAN_CHAPTERS.md` (Antigravity / Gemini)

**Reviewed:** 2026-11-13  
**Context:** Reviewed alongside `PLAN_CHAPTERS.md`, `PLAN_CHAPTERS_codex_review.md`, `book-bioinf-computing/PLAN.md`, and the parent series' `PLAN.md` and `CLAUDE.md`.  
**Target Audience:** Beginner-to-intermediate MS and new PhD students (often coming from biology/animal science backgrounds) who will primarily *use* existing tools, packages, and pipelines on Linux HPC clusters, rather than writing low-level tools (like STAR or FastQC) from scratch.

---

## Overall Assessment

The revised `PLAN_CHAPTERS.md` is in **excellent shape**. The collaboration between Claude and Codex already resolved the biggest structural risks: Part I was tightened, R and Python essentials were moved *before* file formats (so readers can actually inspect tables when learning about them), `nf-core` execution was placed before Nextflow authoring, and the boundary between **everyday tool/script use** (Parts I–VI) and **software development / advanced computing** (Part VIII) is crystal clear.

Because this is the **Foundations: Computing** book for a much larger book series (*Genomics*, *Transcriptomics*, *Proteomics & Metabolomics*, *Statistics for Omics*, *Biology*, and later *Advanced Algorithms*), it has to carry a heavy reference load while remaining approachable for a first-year graduate student. At 38 chapters, the secret to keeping this book from feeling overwhelming is **pacing, labeling, and strict scope boundaries with future books**.

Below are specific recommendations to polish the plan before moving to chapter outlines.

---

## 1. What Works Exceptionally Well (Keep As-Is)

1. **The "Using vs. Developing Code" Split:** Placing basic object assignment, function calls, subsetting, and script adaptation in Chapters 12–13 while postponing custom functions, data structures, CLI argument parsing (`argparse`/`optparse`), debuggers, and unit testing to Chapter 34 (Part VIII) matches how graduate students actually learn and work.
2. **HPC and Remote Work as First-Class Citizens:** Most introductory books assume everything happens on a local laptop and treat HPC as an appendix. Putting SSH, `tmux`, `rsync`/Globus, and SLURM in Chapters 9–10—and labeling every command as `[laptop]`, `[login node]`, or `[compute node]`—will save new grad students months of frustration (and save cluster admins from heavy jobs on login nodes).
3. **One Primary Setup (`pixi` + VS Code):** Deciding on `pixi` and VS Code (Remote-SSH) in Chapter 2 while moving RStudio, Positron, Conda, `uv`, and `renv` to comparison tables/later chapters avoids the "paradox of choice" that stalls beginners in Week 1.
4. **The Running Dataset Choice:** Using the `nf-core/rnaseq` yeast (*S. cerevisiae*, GSE110004) test dataset is a smart, pragmatic bridge. It is small enough to run locally, non-human (respecting `CLAUDE.md`), includes a real sample sheet, and prepares students directly for Chapter 26 (`nf-core`) and the *Transcriptomics* book, while tiny auxiliary files cover formats yeast RNA-seq doesn't highlight (like diploid VCFs).

---

## 2. Applying the `core` / `overview` / `optional` Labels

The conventions section states: *"each chapter (or section) is marked **core**, **overview**, or **optional**."* Currently, only Chapters 26, 27, and 34 have explicit tags in their titles. 

Because 38 chapters is a massive table of contents for a beginner MS student, **every chapter heading in `PLAN_CHAPTERS.md` should carry its label now**, and you should consider providing a **"First-Semester / Fast-Track Path"** in the preface (~20 core chapters) versus the **"Full Reference Path"**.

Suggested chapter-level labeling across Parts III–VIII:

| Part / Chapters | Suggested Label | Rationale for MS / New PhD Beginners |
|---|---|---|
| **Parts I & II (Ch. 1–10)** | **Core** | Essential survival skills for local and HPC work. |
| **Ch. 11: Language landscape** | **Overview** | Good context so they know what C/Rust/Perl are, without needing hands-on exercises. |
| **Ch. 12–13: R & Python essentials** | **Core** (pick 1 primary, 1 overview) | Students need sustained practice in one and reading literacy in the other. |
| **Ch. 14–17, 20: Tabular, FASTA/Q, SAM/BAM, BED/GTF/VCF, Ref data** | **Core** | Daily bread-and-butter formats and repositories. |
| **Ch. 18–19: Efficient formats & Databases** | **Overview / Optional** | Beginners should *recognize* `.rds`, Parquet, `.h5ad`, and SQLite, but rarely build SQL queries or Arrow pipelines in month one. |
| **Ch. 21–24: Reproducibility** | **Core** (Git, Envs, Containers) | Focus on *using* environments/containers and basic solo Git; advanced branching/PRs in Ch. 22 can be **Overview**. |
| **Ch. 25–26: Why workflows & Running nf-core** | **Core** | The capstone practical skill for modern bioinformatics grad students. |
| **Ch. 27–28: Writing Nextflow & Other systems** | **Optional / Overview** | Ch. 27 is a great extension; Ch. 28 is a recognition overview (Snakemake, WDL, Galaxy). |
| **Part VII (Ch. 29–33): Algorithms** | **Overview** (Ch. 29–31) & **Optional** (Ch. 32–33) | Crucial intuition for *why* tools behave as they do, but not a blocker for running `nf-core/rnaseq`. |
| **Part VIII (Ch. 34–38): Advanced topics** | **Optional** | Explicitly framed as "when you outgrow simple scripts or hit scale bottlenecks." |

---

## 3. Guarding the Boundaries with the Rest of the Book Series

Looking one directory back at `book-bioinf-series/PLAN.md`, the series has a strict rule: **"Shared material has one owner... Other books link, never re-teach."** Because this is the first book being written, there is a natural temptation to pack too much domain detail into Parts IV and VII.

### A. Algorithms (Part VII: Chapters 29–33)
Since students will **not** be implementing aligners or assemblers here, and a dedicated *Advanced Algorithms* book is planned for later (`PLAN.md` §5), Part VII should be framed around **"How algorithm concepts explain tool parameters and resource usage"**:
- **Ch. 29 (Thinking about algorithms):** Tie Big-O and sorting directly to why `samtools sort` uses RAM/temp files and why an index (`.bai`, `.tbi`) makes region queries instantaneous.
- **Ch. 30 (Sequence alignment):** Keep dynamic programming visual (no complex traceback code). For **BLAST**, cover only the core intuition (seed-and-extend, what an E-value vs. bit-score means, and running a basic CLI query or reading tabular `-outfmt 6`). Leave deep BLAST flavors (`blastp`, `psiblast`, taxonomy filtering, database masking) to the *Genomics* and *Proteomics* books.
- **Ch. 31 (Indexing genomes):** Frame k-mers, BWT/FM-index, and minimizers around **why aligners need a genome index build step** (`bwa index`, `star --runMode genomeGenerate`), why indexing takes 30–60 GB of RAM for mammalian genomes, and how pseudoalignment (Salmon/Kallisto) trades base-level alignment for speed (linking forward to *Transcriptomics*).
- **Ch. 32–33 (Graphs/Assembly & Probabilistic methods):** Keep these very high-level and visual. A new MS student doing bulk RNA-seq or variant calling does not need deep coverage of de Bruijn graphs, HMMs, EM, MinHash, and Bloom filters all at once. In particular, **Chapter 33** packs four distinct mathematical concepts into one chapter—consider making it strictly an **Overview / Spotlights** chapter ("Four ideas you will meet inside bioinformatics tools: HMMs in Pfam, EM in RSEM/Salmon, MinHash in Mash, Bloom filters in k-mer tools") with zero math derivations.

### B. File Formats (Part IV: Chapters 15–17)
- `PLAN.md` §6 notes that *Genomics (DNA)* owns "sequencing QC, trimming, read alignment, BAM in full" while *Computing* owns "File formats."
- In **Ch. 15–17**, make sure the focus stays on **file anatomy, coordinate systems (0-based vs 1-based), indexing, and safe manipulation** (`samtools view/sort/index`, `bedtools intersect`, `bgzip`/`tabix`), rather than turning into a full variant-calling or read-trimming tutorial. Mention that FastQC/MultiQC and trimming live in detail in the applied books (though MultiQC appears naturally in Ch. 26 when inspecting `nf-core` outputs).

---

## 4. Minor Practical Gaps & Refinements for Grad Students

A few small, high-value pain points for MS/PhD students on HPC clusters could be woven into existing chapters (no new chapters needed):

1. **The "Inode Quota" and Small-Files Trap on HPC (Chapter 10: HPC and SLURM):**
   - You already include storage tiers and disk quotas (`df`, `du`). Add a bullet on **file count (inode) quotas** and why creating millions of tiny files (e.g., an uncleaned Nextflow `work/` directory or local Conda environments in `$HOME`) breaks HPC accounts even when byte usage is low.
2. **SSH Port Forwarding / Open OnDemand vs. Remote-SSH (Chapter 2, 9, or 10):**
   - Since VS Code Remote-SSH is the primary editor, briefly note that some HPC centers restrict heavy VS Code server processes on login nodes or require **Open OnDemand** / SSH jump hosts (`ProxyJump`). A 1-paragraph pitfall box in Ch. 2 or Ch. 9 will save students on stricter clusters.
3. **Symlinks (`ln -s`) and File Paths (Chapter 3 or 5):**
   - In Chapter 3 ("Raw data is read-only") or Chapter 5 ("Filesystem tree, paths"), explicitly include **symbolic links (`ln -s`)**. On HPC clusters, lab groups almost always keep shared raw FASTQs and genome references in a central group directory and symlink them into project folders rather than copying 500 GB of reads.
4. **Conda/Apptainer Cache Directories on HPC (Chapter 23 & 24):**
   - When introducing `pixi`/Conda (Ch. 23) and Apptainer (Ch. 24), include the classic HPC pitfall: `~/.conda`, `~/.pixi`, and `~/.apptainer` default to `$HOME`, which immediately blows up a 10–20 GB home quota when pulling BioContainers or Nextflow images. Show how to point cache environment variables (`APPTAINER_CACHEDIR`, `NXF_SINGULARITY_CACHEDIR`) to project/scratch storage.
5. **Parent `PLAN.md` Sync:**
   - The parent series `PLAN.md` (§4, line 197) still lists the Computing running dataset as `[open]`. Since `PLAN_CHAPTERS.md` has marked the yeast `nf-core/rnaseq` dataset (GSE110004) as **[decided]**, you can update the parent `PLAN.md` and `CLAUDE.md` whenever you finalize this review.

---

## 5. Summary Verdict

**Ready to proceed to chapter outlines and the template chapter (Chapter 15: FASTA/FASTQ).**

The structure is logical, pedagogical, and pragmatic. By keeping the advanced programming topics tucked cleanly into Part VIII and framing Part VII (Algorithms) as "conceptual literacy for tool users" rather than computer science implementation, this book will hit the exact sweet spot for incoming MS and PhD students.
