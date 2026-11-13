# Review of `PLAN_CHAPTERS.md`

Reviewed November 12, 2026, alongside this book's `PLAN.md` and the parent series' `PLAN.md` and `CLAUDE.md`.

Revised after clarification that the main audience will use existing packages and pipelines, with programming beyond everyday analysis kept toward the end.

## Overall assessment

The plan has the right ingredients for an introductory graduate book. Its strongest choices are Linux and HPC as the main working environment, explicit attention to formats and reference versions, and a progression toward reproducible workflows. These are worth preserving. The series' separation of computing, biology, statistics, and applied omics also gives this book a useful boundary.

**I would refine the learning path before adding topics.** Forty chapters could work as short, browsable lessons, but treating all forty as equally necessary would make the book feel much broader than its intended introduction. The principal risk is that students encounter many tools before becoming comfortable completing and checking a small analysis.

My priorities would be:

1. Get readers doing something useful sooner.
2. Teach the concepts needed to use and adapt analysis scripts early; keep writing reusable code and software debugging optional and later.
3. Give the examples one supported software setup and one recurring dataset.
4. Add a little more emphasis on checking data and diagnosing failed work.
5. Mark deeper algorithms, alternative tools, and infrastructure as optional.

These changes should mostly redistribute or shorten material, rather than add chapters.

## 1. Improve the order without rebuilding the whole plan

### Shorten the route to the first command

Part I contains useful material, but five chapters before the shell is a long introduction. Open with a short orientation and a first successful task: locate a small FASTQ file, inspect it, and save a simple summary. The student should know what they accomplished before learning the full computing landscape.

Keep CPU/RAM/disk vocabulary early, but revisit resource estimation when students have an actual job to measure. Likewise, introduce one editor first; put the comparison of VS Code, RStudio, Positron, Jupyter, and terminal editors in a reference section.

Do **not** move all of project organization and getting help until after Part II. Students need a working directory, protected raw data, and a way to interpret `--help` immediately. Give those essentials early, then expand them where they become useful.

For the HPC route, introduce enough SSH to connect before asking readers to use Remote-SSH or a remote shell. The fuller treatment of transfers and persistent sessions can remain in Chapter 10. Clearly label commands as running on the laptop, login node, or allocated compute node.

### Put language basics before language-dependent examples

The current formats part includes reading tables in R and Python before either language has been introduced. My preferred solution is to move the language essentials ahead of the formats part. A small FASTQ preview can still appear in the opening exercise without teaching the entire formats curriculum there.

My original recommendation to move “functions, basic control flow, debugging” forward was too broad for this audience. Keep Chapter 36 toward the end. Bring forward only the concepts students need to follow a package vignette, adapt a supplied analysis script, and inspect their inputs and outputs. Calling an existing function belongs early; defining a function can wait. Basic loops already have an applied home in shell scripting; R/Python control flow can be introduced only when an example needs it.

### Separate using code from developing code

Use the task a student needs to complete as the boundary, rather than whether a topic appears in a programming course:

| Earlier: everyday applied use | Later: optional programming |
|---|---|
| Assign an object and understand that later lines use it. | Design reusable functions and decide their inputs and return values. |
| Call a package function, change a named argument, and save its returned object. | Write functions, handle unusual inputs, and organize reusable analysis code. |
| Recognize strings, numbers, logical values, missing values, vectors, matrices, and tables. | Study additional data structures and their implementation. |
| Select rows/columns, filter with a logical condition, and inspect dimensions and sample names. | Write general-purpose data-processing utilities. |
| Run a supplied script in order; adjust paths, filenames, and documented settings. | Build a command-line interface with `argparse` or `optparse`. |
| Read the reported error, check inputs and package help, and collect information for support. | Use breakpoints, step through function internals, and investigate call stacks or package source. |
| Check that an imported table has the expected samples and dimensions. | Write automated unit tests and use testing frameworks. |

For example, an early R lesson might unpack `counts <- read.delim("counts.tsv", row.names = 1)`: assignment, a function call, a filename string, a named argument, and a returned table. Follow with `head(counts)`, `dim(counts)`, and column selection. Students can do useful analysis without defining a function themselves.

Writing a small function can help an analyst avoid repetition, even without developing a package, so it remains a worthwhile optional topic. Package architecture, distribution, and developer tooling need not become requirements anywhere in this introduction. Consider renaming Chapter 36 **“Writing reusable analysis code (optional)”** so its placement does not imply that everyday language essentials have been postponed.

Also preview a minimal Git routine when students first save scripts: inspect changes, commit, recover a previous version. Branches, remotes, and collaboration can stay in Part V. Reproducibility should become a habit before it becomes a named part of the book.

### Introduce reference identity before reference-dependent formats

Bring the assembly/version and chromosome-naming material from Chapter 18 forward to the start of the formats part, or introduce it alongside the first FASTA. Readers should understand that an alignment or coordinate is interpreted against a particular reference before working with BAM, BED, or VCF. Downloads and repository APIs can remain later.

### Teach running workflows before substantial workflow authoring

Keep Nextflow as the main example, but distinguish two outcomes:

- **Core:** run an existing pipeline, supply a sample sheet, choose a profile and resources, inspect logs and outputs, and resume a failed run.
- **Extension:** write a small workflow and understand how processes and channels connect.

A brief nf-core demonstration can precede detailed Nextflow authoring. Reading or adjusting a workflow is a more approachable first goal than building a production pipeline. Make and the other workflow systems need only enough space to explain the ideas and help readers recognize alternatives.

An overall route could therefore be: **short orientation → shell and remote/HPC basics → R/Python essentials → formats and references → fuller reproducibility → workflows → algorithms tour → optional scale topics.**

## 2. Fill a few practical gaps inside existing chapters

The important gaps are mostly in working habits, rather than missing technologies. I would prioritize these three additions.

| Addition | Existing home | Useful introductory outcome |
|---|---|---|
| Troubleshoot routine tool use and stop failed work | Getting help; shell scripts; HPC; R/Python essentials | Read an error or warning; locate the relevant log; interrupt a command; cancel a SLURM job; check paths, inputs, and requested resources; know when to ask for help. |
| Check identifiers and table operations | Tabular data; R/Python essentials | Preserve identifiers as text; detect missing or duplicate sample IDs; check unmatched rows and unexpected row multiplication after a join. |
| Record enough provenance to rerun a result | Project organization; environments; workflows | Connect an output to input accessions/checksums, reference release, software or pipeline version, parameters, and logs. |

A small worked input problem would teach more than a long troubleshooting catalogue: a supplied script cannot find its input file; the student checks the working directory and filename, corrects the path, and reruns the command. There is no need to enter a debugger or inspect package internals.

For an applied example, the [DESeq2 vignette's count-matrix section](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#count-matrix-input) explicitly checks that count-matrix columns and sample-metadata rows agree in identity and order. Understanding and following that check is a user skill. Investigating the implementation of `DESeqDataSetFromMatrix()` can remain advanced. The same vignette's [support guidance](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#how-can-i-get-support-for-deseq2) asks users to consult help and supply code, complete messages, and session information. Students should learn how to prepare that request without being expected to solve a package bug. The actual differential-expression workflow still belongs in Transcriptomics.

For shell/HPC troubleshooting, briefly include processes (`ps` or `top`), disk usage (`df`, `du`, and the site's quota command), and the distinction between a running process and a submitted job. `scancel` deserves a place beside `squeue` and `sacct`.

For tables, demonstrate the danger of joining counts to metadata in the wrong order. Checking sample identity and alignment belongs here even though downstream statistical interpretation belongs in the omics books. The distinction between missing values and zero is another worthwhile example.

A few small details can fit naturally into existing bullets:

- **Shell:** finding files (`find`), quoting paths, standard output versus standard error, and destructive redirection. Explain `set -euo pipefail` through examples and limitations rather than presenting it as a correctness guarantee.
- **Downloads:** a basic `curl` or `wget` example before repository-specific clients; verify the downloaded file and its provenance.
- **Formats:** use format-aware tools for structured biological data; demonstrate a coordinate boundary on a tiny interval. Explain why corresponding reference and index files must stay associated.
- **Notebooks/Quarto:** restart and run from a clean session, then render one small report. Listing these tools in Chapter 3 does not yet give students a reporting habit.

These should be short additions or exercises, not new standalone chapters.

## 3. Reduce the number of choices students must make

The environments chapter currently names Conda, Bioconda, pixi, uv, renv/rv, and lockfiles. The editors and language chapters have similar menus. Exposure is useful; requiring beginners to choose among them before proceeding would be distracting.

The parent plan already proposes **pixi for the book environment**. If that proposal is adopted, give readers the maintained environment files and a few commands to run the examples near the beginning. Explain dependency resolution and alternatives later. Students should not wait until Chapter 24 to learn how to launch the software used in Chapter 12 or 20.

Apply the same rule elsewhere: one primary editor route, one primary environment route, and one primary workflow example. On a managed cluster, explain when the site's module/container route replaces the local setup. Keep alternative tools visible through compact comparisons and further reading.

For R and Python, make the goal explicit: students should recognize and adapt a small script in both languages; sustained practice in one is a reasonable first pass. Use side-by-side examples when the comparison teaches something, rather than duplicating every exercise.

## 4. Trim or label optional material

The algorithms tour fits the series, but its current scope could become a second textbook. I would protect alignment intuition, k-mers/indexing, computational cost, and a short assembly-graph explanation. Teach enough to understand a tool's assumptions and practical trade-offs.

| Current material | Suggested treatment |
|---|---|
| Suffix arrays, BWT/FM-index, minimizers | Visual overview of indexing strategies; detailed construction is further reading. |
| HMMs, EM, MinHash, Bloom filters | Optional method spotlights. Avoid requiring four new conceptual frameworks in one introductory chapter. |
| Trees and clusters | Put clustering methods and interpretation in Statistics for Omics, consistent with the parent plan. Keep only computational motivation here; link phylogenetic inference to an appropriate later treatment. |
| Databases and efficient formats | One short optional unit is enough initially: a useful query/join and why a different storage format helps. |
| GPU computing and cloud | Optional orientation. Keep recognizing appropriate resources and understanding costs; move detailed CUDA and platform setup to external resources. |
| Julia, Perl, source builds, other workflow languages | Brief landscape/reference material, not separate practical learning requirements. |

Chapter 38 can also be divided by need: introduce numerical precision and log-space ideas when an example requires them; leave the broader survey optional. Basic text/line-ending problems already have a natural home earlier.

The parent's high-level outline mentions mzML, which the chapter plan omits. A short recognition box or link to the MS omics book would resolve that discrepancy. It does not justify another formats chapter.

## 5. Make the existing pedagogy visible in this plan

The parent plan's toy examples, recurring real dataset, self-checks, and annotated further reading are excellent. Bring those commitments into the chapter plan so they guide scope while chapters are drafted.

Choose one small, public, nonhuman dataset with a sample sheet and recorded provenance. Reuse it to inspect files, summarize data, write scripts, submit a job, and run a workflow. Keep separate tiny examples for algorithms and formats that the main dataset does not naturally illustrate; there is no need to force every format into one biological analysis.

Use the same deliverable as a recurring checkpoint: **a small, reproducible project containing input provenance, metadata, scripts or workflow configuration, environment information, logs, and a rendered summary.** Begin it early and improve it as new skills appear. That provides integration without adding a large capstone chapter.

For each chapter, specify a practical outcome and one check students can perform themselves. Early exercises should ask students to run, inspect, and adapt supplied examples; writing an analysis from a blank file need not be the standard. Label material **core**, **overview**, or **optional**. A reader without cluster access should be able to complete the small local examples and understand the captured HPC outputs; SCINet/Nova details can sit in site-specific notes.

## 6. Use external resources to hold the depth

Keep the series' existing annotated Further reading sections, but give each resource a clear purpose. Three recurring anchors would be sufficient to start:

- [William Shotts, *The Linux Command Line*](https://linuxcommand.org/tlcl.php/index.php): the deeper shell and scripting companion. Keep this book's shell examples focused on biological files, remote work, and jobs.
- [Software Carpentry, *The Unix Shell*](https://swcarpentry.github.io/shell-novice/): an alternative practice route through navigation, pipes, loops, and scripts for readers who need more repetition.
- [Official Nextflow training](https://training.nextflow.io/latest/): the next step for readers who want to develop workflows beyond the book's small example.

Link to the relevant lesson or section as chapters are written. Avoid making completion of another whole book a prerequisite for this one.

## Decisions to settle before drafting

There is no need for a wholesale rewrite of the topic list. I would settle five decisions now:

1. Adopt a shorter opening and move R/Python essentials ahead of dependent examples. Include function calls, objects, subsetting, and routine troubleshooting; keep function writing and software debugging in the optional later material.
2. Select the supported software setup and recurring dataset.
3. Add routine input/log checks, identifier/join checks, and practical provenance within existing chapters, without requiring developer debugging or automated testing.
4. Define running and checking an existing workflow as the core workflow outcome.
5. Mark optional material and confirm the clustering boundary with Statistics for Omics.

With those decisions made, the plan should support an introductory book that students can finish and then return to as a reference.
