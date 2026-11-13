---
title: "Chapter 1 outline — Codex review"
subtitle: "Advisory review for Claude · original outline unchanged"
date: 2026-11-13
---

Reviewed [chapter_01.md](chapter_01.md) against
[PLAN_CHAPTERS.md](PLAN_CHAPTERS.md), the chapter template, both repository
guidance files, the series plan, the shared style guide, and the existing
misconceptions registry. Line references below refer to the reviewed
`chapter_01.md`.

**Overall assessment:** the outline is sound and fits the book. Keep the
guided first session before the hardware discussion, the single supported
setup, the small real dataset, and the separation between this orientation
and the later shell, formats, HPC, and performance chapters. No major topic
or section is missing. The main corrections concern claims about resources
and data sizes; the other suggestions make the first session easier to
follow and recover when something fails.

This review proposes changes for Claude to assess. It does not change the
original outline, the overall chapter plan, or `misconceptions.yml`.

## Corrections before drafting

### 1. Replace the claim that every pipeline step makes data smaller

**Locations:** section 5, lines 79–86; `fig-data-shrinks`, line 123;
section 5 key idea, line 183.

“Raw reads are the biggest files you will handle; every later step makes
the data smaller” is incorrect. A BAM can exceed the compressed FASTQ
inputs, depending on alignment records, tags, and compression. Sorting can
also create substantial temporary files while inputs and outputs still
exist. The [samtools sort documentation](https://www.htslib.org/doc/samtools-sort.html)
explicitly describes these temporary files. Peak storage therefore cannot
be estimated from the final output alone.

Suggested key idea:

> Read-level files can be large; count matrices and summary tables are
> usually much smaller. Intermediate files and temporary work can increase
> the disk space a pipeline needs.

Keep the size figure, but let the measured values determine its shape.
It should allow FASTQ → BAM to grow. Label whether each value represents
one mate file, both mates of one sample, or the whole study; a count matrix
usually covers multiple samples. A neutral name such as
`fig-pipeline-file-sizes` would avoid building the incorrect conclusion into
the figure's name.

The small VCF already identified in the open question should stay a
separate formats example. There is no need to introduce variant calling
into this RNA-seq orientation to fill the size table.

### 2. Distinguish physical cores, logical CPUs, and software threads

**Locations:** learning goal 3, lines 38–39; section 4, lines 70–78;
`fig-cores-threads`, line 122; hardware commands, lines 147–148.

The proposed “cores” commands do not necessarily count physical cores.
[`nproc`](https://www.gnu.org/s/coreutils/manual/html_node/nproc-invocation.html)
reports processing units available to the current process; Apple's
[`hw.ncpu`](https://developer.apple.com/documentation/kernel/1387446-sysctlbyname/determining_system_capabilities)
reports the maximum logical CPU count. On a system with simultaneous
multithreading, that can exceed the number of physical cores.

Either label the existing row **logical CPUs / available processing
units**, or add a distinct physical-core measurement. Explain in a few
sentences that a program's threads are units of work scheduled onto CPUs;
`--threads 4` does not guarantee four physical cores remain busy. The
figure can explicitly assume eight physical cores and a tool that scales
well, rather than imply a universal mapping. Also mark `--threads` as an
illustrative flag whose spelling depends on the tool.

For WSL, add one qualification: Linux sees the CPUs and RAM exposed to its
virtual machine, which may differ from the laptop's installed resources.
Microsoft documents these limits in its
[WSL configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).
Convert the macOS RAM result from bytes into a useful unit before asking
readers to compare it with `free -h` output.

### 3. Do not use the tiny timing exercise to diagnose an I/O bottleneck

**Locations:** section 4, lines 70–78; animated hardware figure, line 121;
key idea, line 181; exercise 3, lines 218–221.

The outline turns “I/O as the usual bottleneck” into “Most analysis waits
on reading and writing files, not on the CPU.” That is too broad. Alignment
and other computational steps can be CPU-bound; reference indexes can be
memory-limited; gzip decompression itself uses CPU.

This particular exercise reads only 2.2 MB, after the file has already
been read. Process startup and filesystem caching can strongly affect its
timing. Elapsed time alone does not tell a beginner which resource limited
the command, and multiplying it by 600 is not a reliable runtime forecast.

Keep `time` as an introduction to elapsed time, with a note that this file
is too small for dependable extrapolation. Change the exercise to ask
what assumptions a proportional estimate would require, or use a supplied
timing from a larger run and label the estimate as rough. Leave actual
bottleneck diagnosis in Chapters 10 and 35.

Suggested hardware key idea:

> A job can be limited by CPU, RAM, storage, or I/O; extra cores help only
> when the work can use them.

The animation can show **an example of an I/O-limited job**, rather than
suggest every analysis has the same slow leg. These refinements still
cover the resource-awareness topic in `PLAN_CHAPTERS.md`.

### 4. Make reads, read pairs, file size, and RAM requirements explicit

**Locations:** outcome check, lines 28–30; section 5, lines 79–86;
self-check, lines 204–205; exercises 1–2, lines 213–217.

The arithmetic is correct for one mate file, but “each test sample has
50,000 reads” conflicts with the overall plan's **50,000 read pairs per
sample**. Say that each mate file has 50,000 reads, together representing
50,000 pairs / 100,000 reads. Likewise, define whether a “30-million-read
sample” means 30 million individual reads or 30 million pairs.

Using this file's compression ratio, 30 million reads in **one mate file**
would be about 1.34 GB compressed and 7.67 GB uncompressed. At 30 million
pairs, there are two such files. Treat this as scaling the same kind of
file, not a general prediction for sequencing data: read length, headers,
quality strings, and compression change the result. State MB/GB as decimal
units, while acknowledging that system tools may display binary units.

Exercise 2 also needs to distinguish file size from a program's RAM
requirement. The supplied counting pipeline streams data; it does not
hold the whole uncompressed FASTQ in memory. Ask whether a file would fit
**if loaded entirely into RAM**, then explain that this command does not
need to do so. Compare against memory available for work, leaving room
for the operating system and other programs.

## Strengthen the first-session instructions

### 5. Add a small failure checkpoint to the download sequence

**Locations:** section 3, lines 63–69; command sequence, lines 235–245.

The normal path works, but `curl -LO` can save an HTTP error response as
`*.fastq.gz`: curl does not treat HTTP error status codes as failures by
default. Add `--fail`, for example `curl -fLO …`, as supported by the
[curl manual](https://curl.se/docs/manpage.html#--fail).

I also reproduced a misleading failure: with the input missing, the exact
count-and-save command prints a decompression error, writes
`SRR6357070_1 reads: 0`, and exits successfully. The expected 50,000-read
check catches the discrepancy, but the reader needs an explicit instruction
to stop and fix the input rather than continue with the summary.

Add a short checkpoint before counting: the download completed, the file
passes `gzip -t`, and the preview resembles the supplied record. Explain
that successful `gzip -t` normally prints nothing. Show the commands as
separate steps, with expected output immediately beside the relevant step.
Full pipeline error handling can remain in Chapter 8.

The existing summary command packs a pipe, command substitution, arithmetic
expansion, quoting, and redirection into one line. Copying it is reasonable
here, but show the intermediate **200,000 lines → 50,000 reads** calculation
first. Readers should be able to check the result without understanding
every shell construct yet.

### 6. Make the OS setup handoff and exercises self-contained

**Locations:** opening a terminal, lines 56–62; exercises, lines 211–221;
browser fallback, lines 233–234.

Add just enough distinction between **operating system**, **terminal**, and
**shell** to identify where commands go. Windows installation commands run
in administrator PowerShell; the FASTQ commands run in Ubuntu/WSL.
Microsoft's [installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install)
also require a restart and initial Linux account setup. Treat that as a
setup branch which may take longer, rather than promise every step takes
seconds. Give readers on managed laptops a pointer to institutional IT if
they cannot install WSL.

On macOS, identify the default shell as zsh where applicable. These first
commands work there; the book can introduce Bash explicitly in Chapter 5
without changing the reader's login shell now. Keep Homebrew as a mention,
as already planned.

The browser fallback needs one concrete instruction for getting the file
into `~/bioinf-ch01`, especially when a Windows browser saves it outside
WSL. Otherwise it leaves beginners stranded at a path problem before paths
are taught.

Exercises should adapt supplied commands, following the book convention:
provide the matching R2 URL and an append example using `>>`. Explain in
one sentence that `>` replaces a file while `>>` adds to it. Neither
redirection nor appending is taught until Chapter 6. Also give readers a
supplied timing command rather than require them to construct one around
the nested summary expression.

## Order, scope, and smaller refinements

- **Keep the present main order.** Introduce the three OS names briefly
  in section 2; section 6 can remain a short explanation of why Linux is
  the common working environment. If it repeats section 2, merge it there
  rather than expand both. No broader restructuring is needed.
- **Carry the first result into Chapter 3.** Add a forward link saying
  the scratch folder, source URL, and summary will become the first inputs
  to the recurring project. The current outline links forward to Chapter
  2 but misses this useful connection to the project begun in Chapter 3.
- **Keep resource-placement answers conditional.** For the 2 TB RAM
  question, “cloud is a possible option if suitable resources and funding
  are available” is better than a categorical “cloud.” Another shared
  facility may also be appropriate. DESeq2 on a laptop should be explicitly
  the small bulk count matrix used here. No additional cloud tutorial is
  needed.
- **Clarify the cluster diagram.** Shared storage belongs to the cluster
  nodes; the laptop accesses it through remote connections or transfers.
  Draw job submission through the scheduler separately from storage access
  so the arrows do not imply all file data pass through the scheduler.
- **Scope the four-line rule to this example.** “This unwrapped FASTQ has
  four lines per read” is sufficient. Leave general FASTQ validation and
  paired-read synchronization checks for Chapter 15. Equal mate counts
  are expected here, but equal counts alone do not prove the pairs match.
- **Narrow the `zcat` explanation.** The chosen `gunzip -c` is a good
  portable choice. The macOS issue is filename handling: on this Mac,
  `zcat file.fastq.gz` looked for an added `.Z` suffix, while `zcat` reading
  the same gzip data from standard input worked. “Avoids a macOS `zcat`
  filename-handling difference” is more accurate than “does not read
  `.gz`.” No need to teach these alternatives here.
- **Record the verified data version.** The `rnaseq` branch URL can
  change. Preserve a commit identifier and checksum in the author-facing
  data record, alongside source/accession/license/citation in
  `data/README.md`. Chapter 3 can teach checksums; Chapter 1 need not add
  another command.

## Verification performed

Downloaded both linked mate files on 2026-11-13 into temporary storage.
Checked the decompressed records and ran the preview/count/save portion
of the proposed session under Bash and zsh on macOS.

| Check | Result |
|:------|:-------|
| R1 compressed size | 2,239,317 bytes, as stated |
| R1 uncompressed size | 12,776,642 bytes, correctly rounded to 12.8 MB |
| R1 records | 200,000 lines; 50,000 reads; all sequences 101 bases |
| Quoted first record | All four lines match the downloaded record |
| Sequence/quality lengths | Match throughout R1 |
| Matching R2 | 50,000 reads; corresponding record IDs match R1 in order |
| Summary in Bash and zsh | Exactly `SRR6357070_1 reads: 50000` |
| Missing-input behavior | Error printed, but zero-read summary written and exit status 0 |

R1 SHA-256 for this check:
`3f50541fa9cf2bedc87e7b682ada0fccfdfcd6d27b9bb81f17be230ff140ebe7`.

Windows/WSL was checked against the official documentation, not executed
on a Windows machine. BAM/VCF/count-matrix sizes remain explicitly open
in the outline; this review does not treat them as measured.

**Recommended disposition:** retain the outline and its main order. Correct
items 1–4, make the first-session additions in items 5–6, and consider the
smaller refinements while drafting. This chapter needs more precise
claims and a few connecting instructions, not more subject matter.
