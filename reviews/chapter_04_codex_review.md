# Chapter 4 — Codex review

Reviewed: 2026-11-17  
Chapter: [Getting help](../chapters/04-getting-help.qmd)  
Revision reviewed: working tree based on `842a29e`, including the existing
uncommitted chapter edits and four new figures. Chapter SHA-256:
`0cb727332df85deabc9e20e79f0dea17760c84a719d7c6e81f743ee7f62eff6d`.

The chapter renders successfully. Its tested error messages, exit statuses,
read statistics, broken-script sequence, and ENA numbers agree with the
examples. I found one medium-priority teaching issue and two low-priority
corrections or publication dependencies. These findings concern the written
chapter, rather than its earlier plan. No chapter, figure, or setup files
were changed as part of this review.

The examples-first structure works particularly well here: readers diagnose
six failures before learning the reading strategy, and the checklist starts
with two concrete cases. The truncated-file example is also unusually
effective: it demonstrates both a misleading success status and how shrinking
an input can remove the failure. Keep the distinction between running a
command successfully and answering the biological question correctly.

## Findings

### 1. Make the model help request pass its own completeness and reproduction test

**Priority: medium.** Locations: [chapter source](../chapters/04-getting-help.qmd),
lines 1125–1135 and 1148–1174; compare the attachment wording in
[the request figure](../figures/good-request.svg).

Exercise 3 asks whether someone could reproduce the failure from the request
alone. The answer says yes, but its model labels a message containing `...`
as **complete**, describes a small FASTQ without attaching it or giving a
download/creation recipe, and invokes `pixi run` without supplying or linking
the manifest and lockfile. The shown manifest path is a private local path,
not something a helper can obtain.

There is a further path mismatch: the earlier `seqkit head` command writes
`~/bioinf-ch04/small_R1.fastq.gz`, whereas the request uses the relative path
`small_R1.fastq.gz` from an unspecified working directory. In this particular
example the mismatch is hidden because SeqKit rejects the flag before
looking for the input. The figure handles the message more clearly by saying
the full output is attached; the exercise's model does not.

**Reproduction:** SeqKit 2.14.0 returns status `255` with the same unknown-flag
failure for `seqkit stats --paired`, with no input argument at all. The full
diagnostic includes the usage and flag list on standard error and a repeated
`unknown flag: --paired` on standard output. Neither a FASTQ nor a particular
file location is needed to reproduce this failure.

**Suggested correction:** use this as a final example of minimizing further:
remove the data argument, rerun, and report that no input data are required.
State the required SeqKit version and how to obtain the book environment
(a link to Chapter 2 or the setup files is sufficient). Supply the complete
captured message as text or an attachment, or explicitly label the printed
message as abbreviated and state that the full output accompanies the
request. If retaining the FASTQ example, actually attach it or provide a
complete recipe, and specify the working directory and matching file path.
Then qualify the answer's claim of reproducibility to match what is supplied.

### 2. The methods table silently repairs spaces in its “as printed” column

**Priority: low.** Locations: [chapter source](../chapters/04-getting-help.qmd),
lines 669–689 and 695–704.

The caption explicitly says this column keeps the paper's typography, but
the linked [PMC methods section](https://pmc.ncbi.nlm.nih.gov/articles/PMC6310685/)
joins adjacent long options without a space in both the cutadapt and RSEM
parameter strings. The chapter inserts those spaces in the “as printed”
column. The proposed commands in the next column have the correct spacing;
the problem is that the exercise hides a second copying fault while teaching
readers to notice exactly these faults.

**Verification:** inspecting the linked article's HTML confirmed that both
option boundaries lack whitespace. The article's tool versions and reference
assembly/release otherwise agree with the chapter's table.

**Suggested correction:** preserve the missing spaces in the “as printed”
column and explain that both spaces and hyphens need repairing. Alternatively,
say that spacing has been normalized in that column, but the first approach
provides the stronger troubleshooting example.

### 3. The cluster help route still ends at a placeholder appendix

**Priority: low; a publication dependency.** Locations:
[chapter source](../chapters/04-getting-help.qmd), lines 478–480 and 778;
[cluster appendix](../appendices/a-cluster-sites.qmd), lines 3–35.

The chapter correctly directs account, node, module, and quota problems to
the cluster's own staff, and gives the appendix as the route to that help.
The appendix currently contains an under-construction notice and a topic
list, including a future item for support contacts, but no contact details.
For a chapter teaching readers when to stop troubleshooting and ask, that
leaves an important next step unfinished.

**Suggested correction:** add the official SCINet and Nova support routes to
the appendix before publication, or link them directly from this table while
the appendix is being written. This is the same shared-appendix dependency
identified in the Chapter 1 and Chapter 2 reviews, now at Chapter 4's help
entry point; it does not require restructuring this chapter.

## Verification performed

- Rendered with `quarto render chapters/04-getting-help.qmd`: successful,
  without reported missing-reference or missing-citation warnings.
- Checked all **23 Bash blocks** with `bash -n`, including the indented
  command in the AI walkthrough: no syntax errors. This checks parsing,
  not execution on every supported system.
- Confirmed that all referenced section, figure, and table identifiers
  exist in the book source and all six citation keys exist in
  `references.bib`.
- Parsed all four included SVGs as XML and confirmed their inclusion in
  the generated HTML. The seven-step checklist's step metadata and
  `steps.js` are present in the output.
- Reused local copies of both FASTQ files after checking their SHA-256
  hashes against `data/README.md`; all practice outputs were written in
  an isolated temporary workspace.
- Used SeqKit **2.14.0** and Rscript **4.4.3** from an existing book
  environment. Its lockfile is byte-identical to the current
  `setup/pixi.lock`; the manifest differs in comments and the `check`
  task, which was not used for the chapter examples. Confirmed the
  SeqKit version through `pixi run` with Pixi **0.84.2** as well.
- Reproduced the filename typo, en dash, invented flag, unmatched-pattern
  argument, truncated-file error with status **0**, R missing-file error
  with status **1**, and R coercion warning with status **0**. Compared
  the relevant SeqKit help entries with the chapter.
- Reproduced all three faults of Exercise 1 in the stated order, each
  returning **255**, followed by the successful corrected command.
- Confirmed that a 100-read copy made from the truncated input is valid
  and contains **10,100 bases**. Confirmed both full-file read counts and
  Exercise 2's extended columns, quality values, and `N` counts.
- Extracted Chapter 3's current script and confirmed its quoted MD5
  (`1a687bb7ac6b89b9aa3ae1db438e54f4`). Replayed the missing-R2 case:
  status **1**, the quoted checksum failure, and no `finished:` line.
- Inspected `pixi info`: it describes the environment and paths but does
  not list installed package versions, consistent with the chapter.
- Compared the methods extraction and library descriptions with
  [Wu et al.'s article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6310685/),
  which also confirms its CC BY license. Checked the current
  [SeqKit input/error documentation](https://bioinf.shenwei.me/seqkit/usage/#input-and-output-files)
  and the cited
  [Auslander article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014882).
- Queried the official
  [ENA file-report API](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR6357070&result=read_run&fields=run_accession,sample_alias,library_layout,instrument_model,read_count,base_count&format=tsv):
  GSM2879618, `PAIRED`, Illumina HiSeq 2500, **47,629,288** reads/pairs
  and **9,621,116,176** bases match the answer. Their ratio is **202**
  bases per pair, consistent with two 101-base mates.

## Limits and release notes

Runtime checks were performed on macOS Intel using the available book
environment; I did not repeat them on Linux, WSL, or a live cluster, or
perform a fresh environment installation. I did not verify GNU gzip's
manual-page selection after a complete Homebrew setup or the availability
of `man` in a fresh WSL installation. Those remain the platform checks
already recorded in the chapter plan.

The browser tool reported that no browser was available, so visual layout,
mobile table widths, dark-mode appearance, and interactive checklist
controls were not tested in a browser. XML and generated-HTML inspection
do not establish visual or accessibility correctness. The ENA fields were
checked through its API rather than the browser record's presentation.
This review did not recheck editorial notices for every cited paper or
audit institution-specific AI policies.
