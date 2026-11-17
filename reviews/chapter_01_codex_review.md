# Chapter 1 — Codex review

Reviewed: 2026-11-17  
Chapter: [Orientation: computers and where you compute](../chapters/01-orientation.qmd)  
Revision reviewed: working tree based on `3da72fc`, including the existing
uncommitted chapter edits. Chapter SHA-256:
`ca03d5cf5a5da5e4b082382373198487fab96406d3bbe684e78b901b59608bbc`.

The chapter renders successfully, and its downloaded FASTQ records, read
counts, checksums, and size calculations agree with the displayed examples.
I found three medium-priority issues and three low-priority corrections or
documentation gaps. The findings describe the written chapter, rather than
its earlier plan. No chapter, figure, or setup files were changed as part of
this review.

## Findings

### 1. WSL's `df` output can overstate the laptop's available disk space

**Priority: medium.** Locations: [chapter source](../chapters/01-orientation.qmd),
lines 428–432 and 455–465.

The Windows instructions tell readers to record the `Avail` column of
`df -h ~` as their computer's free disk space. In WSL2 this describes the
Linux filesystem inside a dynamically growing virtual disk. It does not
establish how much physical space remains on the Windows drive containing
that disk. Microsoft explicitly notes that WSL can report a virtual capacity
larger than the actual Windows device in its
[WSL disk-space guide](https://learn.microsoft.com/en-us/windows/wsl/disk-space#how-to-check-your-available-disk-space).

A beginner could therefore conclude that hundreds of gigabytes are available
for sequencing data when the Windows drive is nearly full. The chapter
already distinguishes WSL's memory limit from the laptop's RAM; disk needs
the same distinction.

**Suggested correction:** retain `df -h ~` as the Linux filesystem check, but
also tell WSL readers to check the free space of the Windows drive holding
their Ubuntu installation, using **File Explorer → This PC** or Windows
Storage settings. Explain that both limits apply and the smaller remaining
capacity constrains new data. Avoid assuming that every installation is on
`C:`.

### 2. The Windows browser-download fallback breaks on paths containing spaces

**Priority: medium.** Location: [chapter source](../chapters/01-orientation.qmd),
lines 301–306.

The fallback command is:

```bash
cp /mnt/c/Users/<your-windows-name>/Downloads/SRR6357070_1.fastq.gz ~/bioinf-ch01/
```

Replacing the placeholder with a Windows profile-folder name such as
`First Last` makes Bash pass two source arguments to `cp`. The copy fails
even though the downloaded file exists. The folder name under
`C:\Users` can also differ from the account's displayed name, so “your
Windows user name” does not always identify the right path.

**Reproduction:** with an equivalent temporary directory containing
`Users/First Last/Downloads`, the unquoted copy returned status `1` and two
missing-file errors. Quoting the source path returned `0`.

**Suggested correction:** quote the whole source path:

```bash
cp "/mnt/c/Users/<your-windows-name>/Downloads/SRR6357070_1.fastq.gz" ~/bioinf-ch01/
```

Tell readers to substitute the actual profile-folder name shown under
`C:\Users`, rather than necessarily their displayed account name. No broader
lesson on quoting is needed here.

### 3. Returning to the cluster exercises loses the scratch working directory

**Priority: medium.** Locations: [chapter source](../chapters/01-orientation.qmd),
lines 250–258, 798–809, and 849–850.

The guided session tells cluster readers to start an interactive shell,
change into `~/bioinf-ch01` there, and then type `exit` after steps 1–6.
The exercises correctly require another compute session, but never tell
readers to change back into the scratch folder.

Changing directory inside the first compute shell does not change the parent
login shell's directory. A fresh `srun` uses its caller's working directory
unless told otherwise, as documented in the
[`srun` manual](https://slurm.schedmd.com/srun.html#OPT_chdir).
For a reader who started in their home directory, Exercise 1 downloads R2
there and creates a new summary containing only the R2 line. Exercise 3
then cannot find R1. Resuming the exercises in a fresh laptop terminal has
the same problem.

**Reproduction:** I modeled the two interactive sessions with separate Bash
child processes in temporary storage. The first saved the R1 summary inside
`bioinf-ch01`; the second, started from the unchanged parent directory,
created a separate summary containing only `SRR6357070_2 reads: 50000`.
This reproduces the directory behavior without claiming a live Slurm test.

**Suggested correction:** add a short instruction and command before
Exercise 1, after cluster readers have obtained their compute session:

```bash
cd ~/bioinf-ch01
```

Say that the exercises use the files from the guided session and that readers
should repeat this directory change whenever they open a new session.

### 4. Name `ProcessPoolExecutor` rather than treating all of `concurrent.futures` as processes

**Priority: low.** Location: [chapter source](../chapters/01-orientation.qmd),
line 543, Python row of `tbl-language-threads`.

The row lists “`multiprocessing` and `concurrent.futures` (processes)” as
ways to use more cores. `concurrent.futures` also exposes
`ThreadPoolExecutor`; ordinary Python threads do not bypass the GIL for
CPU-bound Python code in the book's default CPython build. A reader choosing
that executor could follow the table and still fail to use multiple cores
for that workload. The
[Python documentation](https://docs.python.org/3.14/library/concurrent.futures.html)
distinguishes the thread, interpreter, and process executors.

**Suggested correction:** change the entry to “`multiprocessing` and
`concurrent.futures.ProcessPoolExecutor` (processes).” The rest of the row
can remain; a full concurrency tutorial belongs later.

### 5. RAM is released for reuse when a program exits, rather than emptied

**Priority: low.** Locations: [chapter source](../chapters/01-orientation.qmd),
lines 489–490; [computer-parts SVG](../figures/computer-parts.svg), line 43.

The text says RAM “is emptied when the program stops,” and the figure
repeats “emptied at the end.” A program's private memory is normally
released for reuse when it exits, but the machine's RAM is not emptied:
other programs and the operating system still use it, and file data may
remain cached. The chapter's own timing answer at lines 859–863 relies on
such caching. The
[Linux memory-management overview](https://docs.kernel.org/admin-guide/mm/concepts.html#page-cache)
explains how file contents are retained in the page cache to speed later
reads.

**Suggested correction:** use “The system reclaims a program's working
memory when it exits; save results to disk if you need to keep them.” In
the SVG, replace “emptied at the end” with “reused between jobs,” or another
short equivalent. This preserves the useful RAM-versus-storage distinction.

### 6. The promised site-specific cluster instructions are still a placeholder

**Priority: low; a publication dependency.** Locations:
[chapter source](../chapters/01-orientation.qmd), lines 260–264 and 770–774;
[cluster appendix](../appendices/a-cluster-sites.qmd), lines 3–17.

The chapter says the required site-specific `srun` options “are in” the
appendix and that it contains step-by-step account details. The appendix
currently contains an under-construction notice and planned topics, without
those instructions. A SCINet reader following the link to resolve the
explicitly required account option receives no working example.

**Suggested correction:** supply the relevant recipes before publication,
or describe the appendix as forthcoming and direct readers to their site's
official instructions or support for the missing account/partition settings.
The existing SCINet signup link already provides a useful account-application
route; the surrounding wording should accurately describe what the appendix
currently supplies. This is the same shared-appendix dependency noted in
the Chapter 2 review, now identified at Chapter 1's entry points.

## Verification performed

- Rendered with `quarto render chapters/01-orientation.qmd`: successful,
  without reported missing-reference or missing-citation warnings.
- Checked all **21 Bash blocks** with `bash -n`, after dedenting list
  blocks and substituting the documented Windows-name placeholder: no
  syntax errors. Parsing does not establish cross-platform runtime success.
- Downloaded both mate files from the actual chapter URLs. Both matched
  their SHA-256 checksums and compressed sizes in `data/README.md`.
- Confirmed that each mate decompresses to **12,776,642 bytes**, **200,000
  lines**, and **50,000 reads**, with 101 bases per read, matching
  sequence/quality lengths throughout, and matching mate IDs in order.
- Compared the first two quoted FASTQ records against the downloaded R1
  file: exact match. The 600-fold estimates correctly round to about
  **1.3 GB compressed** and **7.7 GB uncompressed** per mate file.
- Ran the compression check, preview, line count, summary, R2 append, and
  timing commands under Homebrew Bash **5.3.15** in temporary storage.
  The summaries matched the chapter. With GNU coreutils on `PATH`,
  `ls -lh` displayed the stated **`2.2M`**. The available decompressor was
  macOS's system version; GNU gzip installation was not repeated.
- Confirmed that all referenced section, figure, and table identifiers
  exist and that the chapter's citation keys exist in `references.bib`.
- Parsed all five included SVGs as XML. Checked the pipeline figure's
  square areas against the four recorded byte sizes: proportional within
  rounding of the drawn dimensions.
- Reproduced the path-with-spaces and separate-session directory issues
  in temporary workspaces, and consulted the official documentation linked
  in the findings.

## Limits and release notes

I did not perform a fresh Homebrew or WSL installation, change the laptop's
login shell, log into either cluster, or run a browser-based visual and
accessibility audit. Windows behavior was checked against Microsoft's
documentation and the relevant Bash path handling was reproduced locally.

I inspected `scripts/ch01_file_sizes.R` and the recorded input sizes, but did
not regenerate its BAM-to-counts-to-DESeq2 outputs: Rsubread is not installed
in the available R environment. The count-matrix and results-table sizes
therefore remain recorded measurements rather than independently reproduced
results of this review.
