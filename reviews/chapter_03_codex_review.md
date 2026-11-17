# Chapter 3 — Codex review

Reviewed: 2026-11-17  
Chapter: [Organizing projects and data](../chapters/03-organizing-projects.qmd)  
Revision reviewed: working tree based on `842a29e`, including the existing
uncommitted chapter and figure changes. Chapter SHA-256:
`f9af3276f9deedd5f1c23f41b58e13faca45c827c8b5377f0baa4a4fd2713828`.

The chapter renders successfully. The read-count script produces the exact
result and checksums shown, and the seven ENA records support the chapter's
distinction between biological samples and nf-core's test labels. I found
two medium-priority issues and two low-priority corrections. The findings
describe the written chapter, rather than its earlier plan. No chapter,
figure, or setup files were changed as part of this review.

## Findings

### 1. Runs within the same second overwrite the previous log

**Priority: medium.** Locations: [chapter source](../chapters/03-organizing-projects.qmd),
lines 848–849 and 863; explanation at lines 912–919; Exercise 4 answer at
lines 1303–1305.

The script names its log using a timestamp with one-second precision:

```bash
log="logs/01_count_reads_$(date +%Y-%m-%dT%H%M%S).log"
```

`tee "$log"` overwrites an existing file with that name. These inputs are
small enough that two ordinary, sequential invocations can start within
the same second, so a run does not reliably get its own log. A quick failed
retry can also replace the successful run's record. This contradicts the
chapter's central promise to preserve a log of every run.

**Reproduction:** I ran the exact script with SeqKit **2.14.0** on the
downloaded inputs. Sequential runs starting in the same second reused
`01_count_reads_2026-11-17T121600.log`; the number of logs did not increase.
A subsequent checksum-failure test in that second replaced its contents
with the failed run's record. No clock substitution or concurrent execution
was needed.

**Suggested correction:** use `mktemp` to allocate a unique log filename,
retaining the timestamp as a readable prefix, and then send `tee` to that
path. Update the example filename and Exercise 4 accordingly. Appending to
the existing filename would preserve text but would not deliver the promised
one-file-per-run layout.

### 2. The instructions for adding raw data leave the checksum list read-only

**Priority: medium.** Location: [chapter source](../chapters/03-organizing-projects.qmd),
lines 395–415.

The initial protection command correctly removes write permission from both
the raw directory and every file in it, including `checksums.md5`. The
later-file recipe says to run `chmod u+w data/raw`, add a file, and add its
line to `checksums.md5`. Unlocking the directory permits creating the new
file, but does not permit editing the existing checksum list. A beginner
following those steps reaches `Permission denied` while trying to record
the new input.

**Reproduction:** in an equivalent temporary directory, I applied the
chapter's protection command and then its unlock command. Creating a new
file succeeded; appending to `data/raw/checksums.md5` failed with status
`1` and `Permission denied`.

**Suggested correction:** explicitly unlock both the directory and the
checksum list:

```bash
chmod u+w data/raw data/raw/checksums.md5
```

Then add the new file and its checksum from the trusted source, verify the
updated list, and restore protection:

```bash
chmod a-w data/raw/* data/raw
```

The existing raw files can stay read-only throughout.

### 3. `rm` can still ask for confirmation when called from a script

**Priority: low.** Location: [chapter source](../chapters/03-organizing-projects.qmd),
lines 389–391; related annotation at line 368.

The explanation says that without `-f`, `rm` asks about a read-only file
“only when you type it in a terminal; a script does not ask.” The relevant
distinction is whether standard input is a terminal, rather than whether
the command was typed directly or read from a script. A script launched
from a terminal normally inherits terminal input and can prompt too.

**Reproduction:** I ran a Bash script containing `rm readonly.txt` with
terminal standard input, using GNU coreutils **9.11**. It printed:

```text
rm: remove write-protected regular file 'readonly.txt'?
```

Answering `n` preserved the file. This used a disposable file in temporary
storage.

**Suggested correction:** say “Without `-f`, `rm` may ask before deleting a
write-protected file when its input is a terminal. With `-f`, it does not
ask; unattended jobs also cannot rely on an interactive prompt.” The
demonstration's `rm -f` command and the explanation of directory permissions
remain correct.

### 4. Filename case sensitivity depends on the filesystem, including WSL

**Priority: low.** Location: [chapter source](../chapters/03-organizing-projects.qmd),
line 205, the case rule in `tbl-file-names`.

The table says `Data.csv` and `data.csv` are “one file on a Mac or Windows
laptop, two files on a Linux cluster.” However, this book's Windows readers
work in Ubuntu under WSL2 and keep the project in its Linux home directory.
That filesystem treats the names as distinct, just as the cluster does.
Microsoft explicitly describes this default in its
[WSL case-sensitivity guide](https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity#differences-between-windows-and-linux-case-sensitivity).
macOS also supports case-sensitive filesystems, so the Mac statement needs
a default qualifier.

**Suggested correction:** use “usually the same name on default macOS and
Windows filesystems; distinct names on Linux, including your WSL home
folder.” Keep the recommendation to use consistent case: it remains useful
when projects move between filesystems.

## Verification performed

- Rendered with `quarto render chapters/03-organizing-projects.qmd`:
  successful, without reported missing-reference or missing-citation warnings.
- Checked all **23 Bash blocks** with `bash -n`, substituting the pinned
  download URL for the Quarto variable: no syntax errors.
- Downloaded the two FASTQ files, compressed genome and annotation, and
  upstream sample sheet from the exact pinned commit in `_variables.yml`.
  All five sizes, MD5 values, and SHA-256 values matched `data/README.md`
  and the chapter's checksum examples. Confirmed that the FASTA contains
  one sequence.
- Retrieved ENA's file report separately for each of **SRR6357070–76**.
  The GEO aliases, sample titles, replicate numbers, and `PAIRED` layouts
  matched Exercise 3. Inspected the actual upstream CSV: seven runs, five
  labels, four rows with both mates and three with only read 1, as stated.
- Downloaded the official SeqKit **2.14.0** macOS Intel release and ran
  the chapter's exact saved script under Homebrew Bash **5.3.15**, with
  GNU coreutils on `PATH`, in an isolated temporary project. The script's
  MD5 was **`1a687bb7ac6b89b9aa3ae1db438e54f4`** and the output's MD5 was
  **`e1d81de77934f7ab7b44bf72b7520b32`**, both exact matches to the chapter.
  The table reported 50,000 reads and 5,050,000 bases in each mate file.
- Deleted the temporary result and reran the script: the regenerated table
  was byte-identical. Changed one byte of a temporary input: the script
  returned `1`, omitted `finished:`, and preserved the previous result.
- Reproduced the four intended permission failures, deletion of a read-only
  file from a writable directory, writing through and removing a toy
  symlink, and the broken-transfer exercise. Checksums distinguished the
  truncated R1 from the missing R2; `gzip -t` also rejected the truncation.
- Confirmed the platform-specific trailing-slash `rm` warning in a disposable
  symlink fixture: GNU `rm` on this Mac removed the target directory and
  left the broken link. No real shared reference was involved.
- Ran the metadata-writing commands and checked their TSV structure.
  Reproduced the checksum figure's halfway-byte change (`6a` to `6b`):
  the changed copy's MD5 was **`78027ba85c64c39f05ad03a1f0ddca55`**, matching
  the shortened value in the SVG.
- Checked that all section, figure, and table references resolve and all
  chapter citation keys exist in `references.bib`. Parsed the five included
  SVGs as XML and confirmed their inclusion in the rendered HTML, along
  with expansion of the pinned download URLs.
- Compared the storage table against the linked official SCINet and ISU
  storage guides, and checked the FAIR summary against the linked
  principles. The documented distinctions between unbacked cluster
  storage, temporary storage, and retained copies are supported by those
  sources. [SCINet storage](https://scinet.usda.gov/guides/data/storage),
  [ISU storage](https://research.it.iastate.edu/file-storage),
  [FAIR principles](https://www.gofair.foundation/fair-principles).

## Limits and release notes

I did not install the full pixi environment, repeat the walkthrough on a
Windows or Linux machine, log into either cluster, or perform a
browser-based visual and accessibility audit. The executable checks used
the matching official SeqKit release directly, rather than `pixi run`.
WSL case behavior was checked against Microsoft's documentation.

Storage policies can change. Nova details attributed specifically to its
login banner were inspected in the book's existing capture, not verified
through a new login. The ISU storage page itself mentions both seven daily
snapshots and deletion from primary storage after five days; readers seeking
a guaranteed restoration window should confirm retention and recovery with
the site, as the chapter already advises.
