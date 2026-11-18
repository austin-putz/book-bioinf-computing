# Chapter 5 — Codex review

Reviewed: 2026-11-18  
Chapter: [Shell basics](../chapters/05-shell-basics.qmd)  
Revision reviewed: working tree based on `7c0b8f7`. Chapter SHA-256:
`f3376c8bf46177140d38fe70275658f7ddcbe9001427694a4a6eaf54ee63d798`.

The chapter renders successfully. The practice-tree builder, wildcard
exercise, and six-link cleanup exercise work as described. I found one
medium-priority issue and three low-priority corrections. These findings
concern the written chapter, rather than its earlier plan. No chapter,
figure, environment, or user startup files were changed for this review.

The chapter follows through well on the plan review: it distinguishes
parsing from word splitting, demonstrates that globbed names retain their
spaces, previews directory operands with `ls -d --`, and checks both the
new links and the source cleanup. The paired wrong/right relative links
are particularly effective. Keep the practice tree and the prediction
rounds; they make the shell's behavior something readers can test.

## Findings

### 1. `ln -s` does not necessarily refuse an existing destination

**Priority: medium.** Location: [chapter source](../chapters/05-shell-basics.qmd),
line 735, the `ln -s target name` row in `tbl-file-commands`; related
directory-destination example at lines 1695–1699.

The safety table says `ln -s target name` “refuses if `name` exists.”
When `name` is a directory, or a symbolic link to a directory, `ln`
instead creates the new link **inside it**. This matters for a chapter
teaching safe file management: repeating a command that creates a
directory link can unexpectedly write into the directory it points to.
The later exercise correctly uses this behavior with `.` as the
destination, but the table does not state the exception.

**Reproduction:** in a disposable fixture, using GNU coreutils **9.11**:

```bash
mkdir shared replacement
ln -s "$PWD/shared" ref
ln -s "$PWD/replacement" ref
```

The second `ln` returns **0** and creates `shared/replacement`, visible
through `ref/replacement`; it does not report that `ref` already exists.
Adding `-T` to that second command makes it fail with `File exists`.
The [GNU `ln` manual](https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html)
documents both directory destinations and following a destination link
to a directory by default.

**Suggested correction:** say “does not replace an existing file; if the
destination is a directory or a link to one, creates the link inside it.”
If a strict refusal is useful here, give `ln -sT target name` as the GNU
form that treats `name` as the exact link name. The exercise's use of
`ln -s target .` should remain unchanged.

### 2. The displayed first FASTQ record has an extra quality character

**Priority: low.** Location: [chapter source](../chapters/05-shell-basics.qmd),
lines 1442–1446, output from `gunzip -c … | head -n 4`.

The printed sequence has **101 bases**, but the quality line has **102
characters** and also differs from the actual quality string near its
end. This is not the output of the supplied command on the pinned input.
Although FASTQ anatomy is taught later, the chapter should not present
an invalid record as its first look at the real data.

**Reproduction:** I verified the input's SHA-256 against `data/README.md`
and decompressed its first record. The real sequence and quality lines
are both **101** characters long. Saving the four lines printed in the
chapter and running `seqkit seq` with SeqKit **2.14.0** returns **255**:

```text
[ERRO] fastx: unequal sequence and quality
```

**Suggested correction:** replace the console block with a fresh capture
of the command on the pinned R1 file. Preserve the quality line exactly,
including its final `B` characters.

### 3. Use `file -h` for the link-inspection example on macOS

**Priority: low.** Locations: [chapter source](../chapters/05-shell-basics.qmd),
lines 803–814; the platform qualification at lines 1429–1431; related
diagnostic text in [the link-target figure](../figures/link-targets.svg).

The relative-link demonstration shows `file` reporting both the broken
link and the working link as links. However, macOS's `file` follows a
working link by default, so it reports the target as compressed data
instead of printing the stored relative target. The chapter acknowledges
this difference later for `data/ref`, but it also affects this earlier
example, where seeing the stored path is the point.

**Reproduction:** with macOS `file` **5.41**, the supplied command reports
`wrong.fastq.gz` as a broken link and classifies `right.fastq.gz` as gzip
data. Adding `-h` produces the two link descriptions printed in the book.
The upstream [`file` manual](https://github.com/file/file/blob/master/doc/file.man)
defines `-h` as disabling symbolic-link following.

**Suggested correction:** use
`file -h ../tidy/wrong.fastq.gz ../tidy/right.fastq.gz` and explain `-h`
briefly. Keep ordinary `file` for the later content-identification
example, with its existing macOS qualification. Make the figure's
diagnostic command consistent if it is intended to reproduce the same
link inspection.

### 4. Exiting one shell does not refresh another shell's history

**Priority: low.** Location: [chapter source](../chapters/05-shell-basics.qmd),
lines 1562–1566.

The paragraph says Bash saves history when a shell exits, “so two open
terminals do not see each other's newest commands until then.” That
implies exiting one shell makes its commands available in the other
already-open shell. With Bash's default behavior, history is loaded at
startup and saved at exit; the other shell does not automatically reread
the history file. This can confuse a reader trying to find a command with
Ctrl-R immediately after closing the terminal that ran it.

**Reproduction:** I started two Bash **5.3.15** shells without startup
files, sharing a disposable `HISTFILE`. After shell B saved a unique
command and exited, shell A's `history` still lacked that command. It
appeared after `history -n`. The
[Bash history documentation](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html)
describes startup loading and exit saving; the
[`history` builtin documentation](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html)
describes explicitly importing new entries.

**Suggested correction:** say “Each shell normally loads history when it
starts and saves it when it exits. Commands from another terminal may
therefore be missing from an already-open shell's history.” No additional
history-management lesson is necessary here; settings and optional
synchronization can stay in Chapter 7.

## Verification performed

- Rendered with `quarto render chapters/05-shell-basics.qmd`: successful,
  without reported missing-reference or missing-citation warnings.
- Checked all **41 Bash blocks**, including indented exercise blocks,
  with `bash -n`: no syntax errors. Parsing checks do not establish that
  every command succeeds on every supported system.
- Ran the practice-tree builder in an isolated temporary directory using
  Bash **5.3.15**, GNU coreutils **9.11**, and GNU findutils **4.11.0** on
  macOS Intel. Repeated the builder after changing a note: its guard
  refused the existing `share` directory and preserved the changed file.
  Only the chapter's absolute practice-path prefixes were redirected
  into temporary storage; the user's home and project were not modified.
- Decompressed all six toy read files: the A, B, and C files each contain
  **2**, **3**, and **4** records respectively. The sample TSV's MD5 is
  **`971d8f742cb76a8d181d3bdc3dcbceaa`**, matching the earlier plan's
  fixture and the next chapter's expected input.
- Replayed the creation, copying, moving, overwrite, no-clobber,
  interactive-deletion, and option-like-filename examples. The intended
  failures occurred, and successful commands produced the described
  file states. Checked the distinction between listing directory
  contents and previewing directory operands.
- Replayed the wrong/right relative-link example, its unlink cleanup,
  glob expansion with spaces, unmatched and quoted patterns, grouped
  `find` alternatives, and the unquoted `find -name` failure. Checked
  the positive size match and the two deliberately backdated files.
- Ran Exercise 2's six wildcard predictions and Exercise 3's complete
  answer. The latter produced exactly the six expected link mappings;
  the other three verification commands printed nothing. Directory
  traversal and sorting order can differ by system and locale.
- Reused local copies of both real FASTQ files, `genome.fa.gz`, and
  `genes.gtf.gz` only after verifying their SHA-256 hashes against
  `data/README.md`. Confirmed the first read's sequence, the R1
  uncompressed size of **12,776,642 bytes**, and the FASTQ discrepancy
  above. The annotation has **600** lines: the first names
  `not_in_genome`, and all **599** remaining lines name `I`. The genome
  contains one sequence, `I`, supporting Exercise 5's answer.
- Extracted Chapter 3's current saved script and confirmed its MD5,
  **`76fa8eb6a7b90f212042cfbe6d95cfcc`**, matches the log excerpt here.
- Confirmed all **43** referenced section, figure, and table identifiers
  exist in the book source and all **four** citation keys exist in
  `references.bib`. Parsed the six included SVGs as XML and confirmed
  their presence, with `steps.js`, in the generated HTML.

## Limits and release notes

Runtime checks used macOS Intel with the book's recommended GNU tools.
I did not repeat the walkthrough on Linux or WSL, log into Nova or SCINet,
install a fresh book environment, or reproduce the cluster-specific
captures. The SeqKit validation used the available official **2.14.0**
binary directly. Project-navigation examples were checked against the
source layout; the complete earlier-chapter project and log workflow was
not rebuilt for this review.

The browser tool reported no available browser. Visual layout, narrow
screens, dark mode, stepped-figure controls, and browser accessibility
were therefore not tested. XML and generated-HTML checks do not establish
visual correctness. Interactive completion, pager navigation, terminal
key bindings, and macOS settings-menu paths also remain platform checks.
