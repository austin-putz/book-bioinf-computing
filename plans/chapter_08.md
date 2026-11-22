---
title: "Chapter 8 — Shell scripts"
subtitle: "Chapter plan · core · agreed"
date: 2026-11-19
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
draft plan, 2026-11-19. Outputs marked *captured* were recorded on
2026-11-19 on macOS 15 (Intel) in a scratch copy of Chapter 5's
practice tree, with Homebrew bash 5.3.15, GNU coreutils/sed/grep first
on `PATH` (as after Chapter 1), **Apple gzip 457.140.3** (GNU gzip not
installed on the test Mac; its messages are marked *captured (Apple
gzip)*), Apple git 2.50.1, and, for the bash 3.2 rows, the Mac's own
`/bin/bash` 3.2.57. seqkit and pixi were **not** on the test Mac, so
Chapter 3's script was run with a two-line stand-in for `seqkit`;
everything that needs the real project was then captured on Linux:
*captured (Linux)* marks outputs from an Ubuntu 24.04 container
(2026-11-19; bash 5.2.21, GNU gzip 1.12, git 2.43.0, ShellCheck 0.9.0,
seqkit 2.14.0 from its GitHub release, the book's files from the pinned
commit with MD5s matching `data/README.md`, run as an ordinary user, not
root). Without pixi: scripts ran with `bash src/…` and seqkit on `PATH`.
Still *to capture*: real terminals on WSL, clusters, and runs through
`pixi run` (`chapter_08_checks.md`). Open questions settled the same
day (see *Decisions*). **Revised 2026-11-22** after the Codex review
(`chapter_08_codex_review.md`): exercise 2 scaffold, temporary-output
promise, `grep`/`head` handling, sitting order, git `restore` source,
logging in `02`/`run_all.sh`, colour roles. Its bash claims were
re-checked on the Mac (Homebrew bash 5.3.15), marked *captured
(2026-11-22)*.

## From `PLAN_CHAPTERS.md`

- Variables, quoting, loops, conditionals
- Script arguments
- `set -euo pipefail`: what it catches and what it does not
- Logging output and errors
- Numbered scripts as a simple pipeline
- Minimal git routine for saved scripts: check changes, commit, recover a
  previous version (full treatment in Chapter 21)
- Reading a supplied script line by line (Chapter 3's); finding bugs
  with `bash -x` and ShellCheck (more in Chapter 34). *Added to
  `PLAN_CHAPTERS.md` 2026-11-19 by this plan (Austin: option a, keep it
  short).*

## What this chapter builds on

Chapters 1–7 are written, and they point here more than to any other
chapter. Each promise below is a forward link already in the text
(`@sec-shell-scripts`); the section that keeps it is in brackets.

- **Chapter 1:** the read count `$(( $(gunzip -c … | wc -l) / 4 ))` was
  copied on trust (§3). The pitfall "the shell does not stop on errors
  unless told to" (§7).
- **Chapter 3:** `src/01_count_reads.sh` was pasted and run, with
  "@sec-shell-scripts explains every line" (§9). Its lines: shebang,
  `set -euo pipefail`, `mkdir -p`, `log="$(mktemp "logs/…_$(date
  …)_XXXX.log")"`, a `{ … } 2>&1 | tee "$log"` group, `(cd data/raw &&
  md5sum -c checksums.md5)`, write to `.tmp` then `mv`. Chapter 3 also
  set the naming rule `01_`, `02_`, …, `10_report.sh` for scripts in
  run order (§10), and says git "arrives in @sec-git" (§12 gives only
  the minimal routine and keeps that link).
- **Chapter 4:** "whether the program or your script then stops depends
  on the program and the script" (§7); "how scripts and pipelines use
  exit status is @sec-shell-scripts" (§5, §7); seqkit 2.14.0 exiting
  `0` on a truncated file (§7, what `set -e` cannot see).
- **Chapter 5:** "variables and scripts are @sec-shell-scripts" (§3);
  word splitting of `$…` results, kept from step 1 of `fig-shell-steps`
  (§3); "inside double quotes bash still expands `$…`" (§3); changing
  what happens when a pattern matches nothing (`nullglob`, §4); brace
  ranges `{01..03}` "again in loops" (§4); "never `rm -rf` on a path
  built from a variable you have not previewed" (§3, §4); the `rows=(…)`
  list in the practice-tree block (§3). The practice tree
  `~/bioinf-computing-ch05/share/` was built "for Chapters 5–8": real
  gzipped FASTQ with 2, 3, 4 reads for samples A, B, C, a folder with
  spaces (`Run 3 final`), a stray `sample_B_R1.fastq.gz.tmp`, `.fq.gz`
  for sample C, and `../where.sh` (`relative-to-script`, which lists
  `08-shell-scripts`). Chapter 5's plan: "a Chapter 8 loop over
  `*_R1*` gets different counts" (§4).
- **Chapter 6:** `set -o pipefail` promised three times, including the
  `141 0` from `gunzip -c … | head` (§7); `grep` exit 1 = no match,
  "matters in scripts that stop on any nonzero status" (§5, §7); "the
  list and `printf` are explained in @sec-shell-scripts" (§3); "when a
  one-liner grows past one line, it belongs in a script" (§2).
  Decision in the Chapter 6 plan: **the GTF feature count becomes
  Chapter 8's second numbered script** (§10).
- **Chapter 7:** shebang `#!/usr/bin/env bash` and the `x` bit are
  taught and assumed (book decision: every bash script uses that
  shebang); `$0` (§6); functions "named groups of commands" (§8);
  `command -v` "in scripts" (§11, one line); "no spaces around `=`;
  quoting and the rest are @sec-shell-scripts" (§3); `&&` and `||`
  (§5); `#!/bin/bash` on a Mac means bash 3.2, "which lacks features …
  that @sec-shell-scripts may use" (§11); `f=$(…)` and `$( )` (§3);
  exercise 1's `count_lines.sh` with "`$1`, `$( )`, and `basename` are
  @sec-shell-scripts" (§6); CRLF in a field a script reads (§4).

**Boundaries.** Chapter 7 owns permissions, `PATH`, environment
variables, startup files; this chapter only uses them. Chapter 9 owns
`tmux` (a long script surviving a dropped connection); Chapter 10 owns
`sbatch` scripts, which are shell scripts with `#SBATCH` lines on top:
this chapter's scripts are what Chapter 10 submits, and §1 says so.
Chapter 21 owns git beyond the five-command routine (branches,
`.gitignore` rules in depth, undoing commits, remotes). Part VI owns
workflow managers; §10 ends by naming what a numbered-scripts pipeline
cannot do. Chapter 34 (optional) owns writing reusable functions and
tests; §8 defines a function only as "a named group of commands" for
logging.

## Outcome and check

- **Outcome:** readers turn commands they have run by hand into a
  script that takes file names as arguments, quotes every variable,
  loops over files safely, checks its inputs, stops on errors, and
  keeps results and messages apart. They can read every line of
  Chapter 3's script, add a second numbered step to the project, run
  the steps in order with one command, and save each change to the
  scripts with git and get an old version back.
- **Check:** two parts.
  1. **Practice tree** (*captured*). Readers finish a supplied script,
     `~/bioinf-computing-ch08/bin/count_reads.sh` (exercise 1), that
     prints one tab-separated line per file. From
     `~/bioinf-computing-ch05/share`:

     ```bash
     ~/bioinf-computing-ch08/bin/count_reads.sh */*_R1.f*q.gz
     ```

     ```
     sample_C_R1.fq.gz	4
     sample_A_R1.fastq.gz	2
     sample_B_R1.fastq.gz	3
     ```

     (Order follows bash's glob sort, which depends on the locale:
     `Run 3 final` first on the test Mac in `en_US.UTF-8` and on Linux
     in `C.UTF-8`, *captured*, since upper-case `R` sorts before
     lower-case `r` there; but **last** on Nova (AlmaLinux 9.6), Atlas
     (Rocky 9.6), and Ceres (RHEL 9.8), all `en_US.UTF-8` (*captured
     2026-11-22*), where glibc's
     `en_US.UTF-8` sorts names mostly ignoring case, giving A, B, C.
     The text shows one order and says in one sentence that the lines
     may come out in a different order on another system; the counts
     are what matter.)
     Then two failures that must **stop** the script with a message on
     stderr and a nonzero status, printing no count: no arguments
     (`usage: count_reads.sh FILE.fastq.gz [MORE.fastq.gz ...]`, exit
     2, *captured*), and a missing file (`gzip: missing.fastq.gz: No
     such file or directory`, exit 1, *captured (Linux)*; Apple gzip
     says `gunzip: can't stat: …`). The
     unfinished script, without quotes and `set -euo pipefail`, prints
     `… 0` for sample C and for a missing file and exits 0
     (*captured*): the reader sees the difference their edits made.
  2. **Project** (*captured (Linux)*, without pixi; through `pixi
     run` *to capture*). From
     `~/bioinf-computing`, `pixi run bash src/run_all.sh` runs
     `01_count_reads.sh` then `02_gtf_summary.sh` and leaves
     `results/gtf_feature_counts.tsv` with the five counts from
     Chapter 6's check (`129 exon`, `124 transcript`, `118 CDS`,
     `115 start_codon`, `114 stop_codon`, as two TSV columns under a
     `feature`/`count` header); `02` logs `wrote
     results/gtf_feature_counts.tsv (5 feature types)`; `git log
     --oneline -- src/` lists the reader's commits that touched the
     scripts (one commit holding both scripts is fine), and `git show
     --stat HEAD` shows which files the last commit contains.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Save commands as a script, run it, and read any line of one,
   including Chapter 3's.
2. Use variables, `$( )`, and `$(( ))`, and quote every expansion so
   file names with spaces stay whole.
3. Loop over files and over the rows of a sample table, and preview a
   loop before it changes anything.
4. Take file names as arguments, check inputs with `if` and tests, and
   explain what `set -euo pipefail` catches and what it misses.
5. Keep results and messages apart in a log, chain numbered scripts
   into a small pipeline, and save and recover script versions with
   git.

## Sections

Same pattern as Chapters 1–7: each section starts with something
readers run or diagnose, then names the idea. Practice happens in a
scratch folder, `~/bioinf-computing-ch08` (made in §1), reading Chapter
5's practice tree **read-only** (scripts that write go to
`~/bioinf-computing-ch08/`; nothing renames or deletes in `share/`, so
the tree stays as later readers expect). Project work is limited to
§9–§12: reading `src/01_count_reads.sh`, adding `src/02_gtf_summary.sh`
and `src/run_all.sh`, a supplied `.gitignore`, `git init` in
`~/bioinf-computing`, and notes in `NOTEBOOK.md`. Every seqkit call is
through pixi (`pixi run bash src/…`), as in Chapter 3. Visual items in
brackets are specified under *Visuals and teaching aids*.

**Length.** This is the longest Part II chapter by concept count. Teach
it as two sittings, marked in the text: **A. Writing scripts** (§1–§6)
and **B. Making them dependable** (§7–§12). The end of §6 is a natural
stop, with **exercise 1, part A** available there (quote the
arguments, print TSV, tighten the glob). Exercise 1 part B (strict
mode, the failure cases) and exercise 2 come after §7, since both need
`set -euo pipefail` and exit statuses (revised 2026-11-22, Codex
review). Error handling still comes after variables and loops.

1. **What this chapter does.** Learning-goals callout. One paragraph: in
   Chapters 1–7 readers typed commands and pasted blocks; a script is
   those commands saved in a file, so they rerun the same way, record
   exactly what was done, and can be shared, versioned, and (Chapter
   10) submitted to a cluster as a job. Chapter 3's
   `01_count_reads.sh` was one, run on trust; by §9 every line will be
   clear. Setup: `mkdir -p ~/bioinf-computing-ch08/bin && cd
   ~/bioinf-computing-ch08`. Readers who skipped Chapter 5 rerun its
   practice-tree block (linked).
2. **From the command line to a script.** *Start hands-on:* take
   Chapter 6's GTF count, which by now readers have typed or recalled
   several times:
   `gunzip -c ~/bioinf-computing/data/ref/genes.gtf.gz | cut -f3 | sort
   | uniq -c | sort -k1,1nr`. Save it with `code
   ~/bioinf-computing-ch08/gtf_types.sh` (nano fallback), add the
   shebang line and a comment header (what, how to run, inputs,
   outputs), run with `bash gtf_types.sh`, then `chmod u+x` and
   `./gtf_types.sh` (Chapter 7, one line each). *Then name it:* a script
   is a text file of commands run top to bottom by a new bash process;
   it does not see the aliases or unexported variables of the terminal
   it is started from (one sentence, link to Chapter 7's
   `tbl-variable-lifetime`), and changes it makes with `cd` or
   variables vanish when it ends. Relative paths are read from where
   it is **run**, not where it is stored: run `bash
   ~/bioinf-computing-ch05/where.sh` from `~` (Chapter 5's leftover
   file; `ls: cannot access 'data/raw'`, *captured* in the Chapter 5
   plan) to revisit `relative-to-script`. The book's convention: project
   scripts live in `src/`, are run from the project folder, and say so
   in their header; §9 shows the guard that checks it. Script layout:
   shebang, header comment, settings, inputs, work, outputs.
   [`fig-script-anatomy`; misconception `relative-to-script` revisited;
   self-check]
3. **Variables, quoting, and expansions.** *Start hands-on* in
   `share/`: `d="Run 3 final"`, then `ls $d` and `ls "$d"`
   (*captured*: three `ls: cannot access 'Run'` / `'3'` / `'final'`
   errors and exit 2; then the two read files). *Then name it:* `$d` is
   replaced by its value, and if unquoted in a command's arguments the
   value is **split at spaces** (and tabs, newlines: the default
   `IFS`) and each piece is matched as a wildcard; this is the word
   splitting that Chapter 5's `fig-shell-steps` set aside. Rule:
   **quote every `$…` in double quotes** unless you want splitting
   (rare at this stage). One sentence on context: a plain assignment
   (`x=$y`) and the inside of `[[ … ]]` do not split, so an unquoted
   `$n` there (as in §5's self-check) is not a bug, but quoting
   everywhere is the simpler habit. Single quotes stop all expansion
   (Chapter 5). Then the empty-variable trap:
   `outdir=~/bioinf-computing-ch08/out` then `echo "would delete:
   $outdri/"` prints `would delete: /` (*captured*): a typo gives an
   empty value, not an error, so `rm -rf "$outdri/"` would be handed
   the wrong argument `/` (shown as text only, never run; §7's `set
   -u` turns it into an error). Quoting keeps an argument whole; it
   does not check that the path is the one you meant. (What `rm` then
   does depends on its safeguards and your permissions; the point is
   that the command was built wrong.) Assignment rules from Chapter 7 in one
   line (no spaces around `=`); lower-case names for your own
   variables so they never collide with `PATH`, `HOME`, `USER`.
   *Then the expansions readers have already met,* now explained:
   `$( )` (command substitution: Chapter 3's `$(date …)`, Chapter 7's
   `f=$(…)`), `$(( ))` (integer arithmetic: Chapter 1's read count
   finally taken apart: inner `$( )` gives `200000`, `$(( … / 4 ))`
   gives `50000`; integers only, one sentence), `${name}` braces
   (`"${sample}_R1.fastq.gz"` vs `"$sample_R1.fastq.gz"`, which reads
   a variable called `sample_R1`), and trimming a value:
   `${f##*/}` → `sample_C_R1.fq.gz`, `${f%.gz}` → `Run 3
   final/sample_C_R1.fq`, `basename` (*captured*). Lists (arrays) in
   one short paragraph: the `rows=(…)` block from Chapters 5 and 6,
   `"${rows[@]}"` gives every item as its own word (`28 items`;
   `"${rows[5]}"` is `Run 3 final`, one item, *captured*), and
   `printf` reuses its format until the items run out, which is how
   four columns came out of 28 items. `printf` vs `echo`: prefer
   `printf` for anything with tabs or backslashes (one line).
   [`fig-word-splitting` (stepped), `tbl-expansions`; key idea: quote
   every expansion; misconceptions `quotes-are-style`,
   `typo-variable-errors`; self-check]
4. **Loops.** *Start hands-on:* count reads in every R1 file of the
   practice tree, first as the "obvious" version:

   ```bash
   cd ~/bioinf-computing-ch05/share
   for f in */*_R1*; do n=$(gunzip -c $f | wc -l); echo "$f $((n/4))"; done
   ```

   *Captured (Apple gzip):* three `gunzip: can't stat:` lines (`Run`,
   `3`, `final/sample_C_R1.fq.gz`), then `Run 3 final/sample_C_R1.fq.gz
   0`, `run1/… 2`, `run2/… 3`, **and** `run2/sample_B_R1.fastq.gz.tmp
   3`; exit status 0. Two bugs, both silent in the result: an unquoted
   `$f` (sample C counted as 0) and a pattern that also matched the
   `.tmp` copy (the Chapter 5 promise). Fix one at a time: quote `"$f"`
   (sample C → 4), then tighten the pattern to `*/*_R1.f*q.gz`
   (three lines, *captured*). *Then name it:* `for name in list; do …;
   done`; the list is expanded **once**, before the loop starts; the
   body runs once per word. Loop over a glob, never over `ls` output.
   **Preview first:** put `echo` in front of the command that changes
   things and read the list before removing `echo` (Chapter 5's `rm`
   habit, now as a loop habit). *When nothing matches:* `for f in
   */*.bam` runs once with `f` set to the literal `*/*.bam`
   (*captured*); `shopt -s nullglob` makes it run zero times
   (*captured*), which keeps Chapter 5's promise; recommend it at the
   top of scripts that loop over globs, **with a check that the list is
   not empty**, shown explicitly, because zero passes would otherwise
   be a silent "success" on no data:

   ```bash
   shopt -s nullglob
   files=(*/*_R1.f*q.gz)
   if (( ${#files[@]} == 0 )); then echo "no R1 files found" >&2; exit 1; fi
   for f in "${files[@]}"; do …; done
   ```

   (Script lines, shown with a script `filename=`: typed in a terminal,
   `exit` would close it. `if` is formalized in §5; here it is read as
   "stop if the list is empty".) Brace ranges in one line: `for i in {01..03}`.
   *Paired files:* from each R1 name, make the R2 name with
   `"${r1/_R1/_R2}"` and check it exists (*captured*: three pairs).
   Warn in one sentence that `_R1` replacement changes the **first**
   `_R1` in the whole path, so it relies on the naming rule from
   Chapter 3.
   *Rows of a table:*

   ```bash
   tail -n +2 meta/samples.tsv | while IFS=$'\t' read -r sample folder cond reads; do
     if [[ -d "$folder" ]]; then echo "$sample: folder '$folder' found"
     else echo "$sample: folder '$folder' MISSING"; fi
   done
   ```

   (*captured*: `sample_E` → `run5` and `sample_D` → `run4` MISSING,
   which Chapter 6 said a sample table and the files on disk can
   disagree about.) Explain `IFS=$'\t'` (split this line at tabs only),
   `read -r` (keep backslashes), and that the folder `Run 3 final`
   arrives whole. Then the wrong way, `for line in $(tail -n +2
   meta/samples.tsv)`, which yields `[sample_C] [Run] [3] [final] …`
   one word at a time (*captured*). One sentence that a `while` loop at
   the end of a pipe runs in a subshell, so variables set inside it are
   gone afterwards (no `lastpipe`, no `< <( )` taught here; a sum is
   done with `awk`, Chapter 6). This matters as soon as a script must
   **remember** something across rows, e.g. "did any row fail?": with
   `bad=0; tail -n +2 … | while …; do bad=1; done; exit "$bad"` the
   script exits 0 even with a missing folder (*captured (Codex,
   2026-11-22)*). The repair, supplied ready-made for exercise 2 (after
   §7), feeds the file to a `{ … }` group with `<` instead of a pipe,
   so the loop runs in the script's own shell and `bad` survives:

   ```bash
   bad=0
   {
     IFS= read -r _   # skip the header line
     while IFS=$'\t' read -r sample folder _; do
       if [[ ! -d "$folder" ]]; then
         printf '%s: missing folder %s\n' "$sample" "$folder" >&2
         bad=1
       fi
     done
   } < "$table"
   exit "$bad"
   ```

   New details to explain: the `<` after `}` feeds the whole group;
   the first `read` consumes the header; `_` is the conventional name
   for "a value I don't need" (the rest of the line here), which also
   keeps ShellCheck from warning about unused variables (SC2034, seen
   with `header`, `cond`, `reads`). **Limit, one sentence:**
   this recipe is for the supplied table, where every field is filled.
   A tab counts as "whitespace" to `read`, so two tabs in a row do not
   give an empty field: `sample_C<TAB><TAB>control<TAB>12` gives
   `folder=control`, `cond=12`, empty `reads` (*captured (Codex,
   2026-11-22)*). General table parsing is Chapter 14 (R/Python).
   And Chapter 7's CRLF trap, now inside
   a loop: reading `samples_from_excel.csv` with `IFS=,` the last field
   is `12\r`, so `[[ "$reads" == 30 ]]` never matches and `(( reads >
   10 ))` fails with `arithmetic syntax error` (*captured*). The `\r`
   sits in the **last** field, so a script that only uses the folder
   name would never notice it. `IFS=,` works for this simple fixture
   only; it is not a CSV parser (quoted commas). Check tables with
   `cat -A` before a script reads them.
   [`tbl-loop-patterns`; pitfall: loop over globs, not `ls` or `$(cat)`;
   misconception `for-reads-lines`; self-check]
5. **Exit status and conditionals.** *Start hands-on:* recall `$?` from
   Chapter 4 and `grep`'s `0` / `1` / `2` from Chapter 6. Run `grep -q
   sample_E meta/samples.tsv && echo listed || echo "not listed"`
   (Chapter 7's line, now explained: `&&` runs the next command only on
   success, `||` only on failure; `a && b || c` is not a true if/else,
   because `c` also runs if `b` fails, one sentence). *Then name it:*
   `if command; then …; elif …; else …; fi` tests a command's exit
   status, nothing else. `[[ … ]]` is a command that only tests:
   files (`-e`, `-f`, `-d`, `-s` non-empty, `-r`), strings (`==`,
   `!=`, `-z` empty, `-n`), and numbers with `-lt`, `-gt`, `-eq` or
   `(( a < b ))`. The trap: `[[ 9 < 30 ]]` is **false**, because `<`
   inside `[[ ]]` compares text (*captured*); `(( 9 < 30 ))` and
   `[ 9 -lt 30 ]` are true. `[ ]` (older, POSIX) in one sentence:
   seen in other people's scripts, needs every variable quoted; the
   book uses `[[ ]]` in bash scripts. `case` in one line (matching
   a value against patterns, e.g. `*.fq.gz|*.fastq.gz`), shown, not
   exercised. Early exits: `exit 0` success, any nonzero for failure;
   the script's status is its last command's unless it calls `exit`.
   [`tbl-tests`; misconception `sort-is-numeric` echoed for `[[ < ]]`
   in text; self-check]
6. **Script arguments.** *Start hands-on:* Chapter 7's exercise 1
   script, `count_lines.sh`, run again from
   `~/bioinf-computing-ch07/bin/` (readers who skipped it get the
   one-line version in a block), now read line by line: `$1` is the
   first word after the script name, `$( )` runs `wc -l < "$1"`,
   `basename` drops the folders. Then a supplied `args.sh` that prints
   `$0`, `$#`, and each argument, run with `a.fq.gz "Run 3
   final/c.fq.gz"`: `"$@"` gives two arguments, unquoted `$*` gives
   four (*captured*). *Then name it:* positional parameters `$1`…`$9`,
   `${10}`, `$#`, `"$@"` (always this, in quotes), `$0`. A usage check
   at the top: `if [[ $# -lt 1 ]]; then echo "usage: …" >&2; exit 2;
   fi` (*captured*: message, exit 2). `>&2` sends the message to stderr
   (Chapter 6's streams), so it never ends up in a results file;
   exit 2 is the common convention for "used wrongly". Options with
   `getopts` and long `--threads` flags: one sentence, pointing to
   Chapter 34 and to "use R or Python when arguments get complicated".
   Arguments vs editing a variable at the top vs reading a config
   file: one short table row each, recommending arguments for file
   names and a variable at the top for settings (threads).
   *End of sitting A:* exercise 1, part A is available here; part B
   and exercise 2 follow §7.
   [`tbl-special-params`; self-check]
7. **Stopping on errors: `set -euo pipefail`.** *Start hands-on:* a
   five-line `count.sh` (no strict mode) run on a missing file prints
   the gunzip error, then `missing.fastq.gz: 0 reads` and `done`, exit
   0; with no argument at all it prints `: 0 reads` and `done`, exit 0
   (*captured (Apple gzip)*). Add one line, `set -euo pipefail`, and
   rerun: missing file → error, no count, exit 1; no argument →
   `./count.sh: line 4: $1: unbound variable`, exit 1 (*captured*).
   *Then name each letter,* each with its own captured demo:
   - `-e`: stop when a command fails (exit status nonzero). By default
     bash goes on to the next line (Chapter 1's pitfall).
   - `-u`: an unset variable is an error, not an empty string (§3's
     `$outdri` now stops with `outdri: unbound variable`).
   - `-o pipefail`: a pipeline fails if **any** stage fails, not only
     the last. Shown with `set -e` alone: `lines=$(gunzip -c missing.gz
     | wc -l)` sets `lines=0` and the script goes on (*captured*);
     with `pipefail` it stops. `PIPESTATUS` (`1 0`, *captured*) shows
     each stage's status, for diagnosing by hand.
   *Then what it does not catch,* a table built from captures:
   - **A "failure" that is not one:** `n=$(grep -c ZZZ file)` stops the
     script, because `grep` exits 1 for "no match" (*captured*). But
     `grep` also exits **2** for a real error (missing or unreadable
     file), and the tempting fix `|| true` accepts that too: on a
     missing file the error prints, `n` is empty, and the script goes
     on to exit 0 (*captured (Codex, 2026-11-22)*). So the reference
     fix keeps the two apart:

     ```bash
     if n=$(grep -c ZZZ "$file"); then
       :                                   # a match: carry on
     else
       status=$?
       [[ "$status" -eq 1 ]] || exit "$status"   # 1 = no match is fine; 2 = error
     fi
     ```

     `:` is a command that does nothing and succeeds. Zero matches →
     `n=0`, script continues; missing file → exit 2 (*captured
     (2026-11-22)*). When only a yes/no is needed, `if grep -q …` is
     enough; say in the text that it treats a missing file as "no",
     so check the file exists first (`[[ -r "$file" ]]`).
   - **`head` closing a pipe early:** `gunzip -c
     data/raw/SRR6357070_1.fastq.gz | head -n 1` in a strict script
     prints the first header and then stops the script with status
     141, in all six captured runs on this input and system
     (*captured (Linux)*; `seq 1 1000000 | head -n 1` the same, also on
     the Mac). It is a matter of timing, not a guarantee either way: on
     a tiny input it does not (*captured*: the practice tree's two-read
     file passed), so a script tested on toy data can fail on real
     data. This is Chapter 6's `141`, and Chapter 1's `gunzip -c … |
     head` idiom is exactly the one that bites. Fix: keep `| head` for
     looking at files in the terminal, not inside strict scripts.
     (`… | head -n 1 || true` is **not** offered as the repair: it
     would also hide a real decompression error.)
   - **Inside conditions:** commands tested by `if` and `while` are
     exempt by design, and so is everything inside a function called
     from an `if` (*captured*: `after false in f`, then `ok`). In an
     `&&`/`||` list only the commands before the last are exempt: `false
     && echo skipped` does not stop a strict script, but `true &&
     false` does (*captured (2026-11-22)*, exit 1). Two tiny examples,
     no longer table.
   - **Masked statuses:** `local x=$(false)` and `export x=$(false)`
     succeed, because `local`/`export` succeeded (*captured* for
     `local`). Assign on its own line.
   - **Tools that report success despite a problem:** Chapter 3's own
     script, given a truncated R2 whose checksum was (wrongly) made
     after truncation: seqkit prints `[ERRO] … unexpected EOF`, exits
     0, and the script finishes with exit 0 and a `read_counts.tsv`
     holding **only the header line** (*captured (Linux)*, real
     seqkit 2.14.0; Chapter 4's finding, now inside a strict script).
     A valid gzip stream with no content gives `0 reads` and passes
     both strict mode and `gzip -t` (*captured (Linux)*; a zero-byte
     file named `.gz` is different: gunzip and `gzip -t` reject it,
     *captured (2026-11-22, Apple gzip)*).
     Strict mode only sees exit statuses. The remedy is explicit
     checks of what you expect: a results file with more than a header
     line, a read count above zero (or equal to the expected one),
     `gzip -t` before counting (it catches a damaged stream, not a
     valid but empty one), `md5sum -c` against checksums made from the
     source (Chapter 3).
   Close with the book's rule: **every script starts with `set -euo
   pipefail`**, and it is a seatbelt, not a guarantee.
   *After §7:* exercise 1, part B and exercise 2 are available.
   [`fig-strict-mode`, `tbl-strict-mode`; key idea; pitfall: `grep`
   and `head` in strict scripts; misconceptions `script-stops-on-error`,
   `strict-mode-catches-all`, `pipe-stops-on-error` and
   `no-error-means-correct` revisited; self-check]
8. **Logging output and errors.** *Start hands-on:* run the finished
   `count_reads.sh` with stdout to a file and stderr to another
   (`> counts.tsv 2> run.log`), then on a missing file: the TSV stays
   clean and the error is in the log (Chapter 6's streams, now in a
   script). *Then name it:* results on stdout, messages on stderr, in
   every script you write. A two-line function, the first use of one
   (Chapter 7's promise: a named group of commands):

   ```bash
   log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }
   die() { log "ERROR: $*"; exit 1; }
   ```

   `"$*"` here is the one place the book joins arguments on purpose.
   Functions are defined before use; deeper use is Chapter 34. Then
   **keeping a log of a whole run**: `2>&1 | tee "$log"` around a
   `{ … }` group (Chapter 3's form, previewed here, explained in §9),
   date-stamped log names with `date +%Y-%m-%dT%H%M%S` (Chapter 3's
   ISO dates), `mktemp` so two runs in the same second never share a
   log. One sentence (decided 2026-11-22): this needs GNU `mktemp`,
   which fills in X's before a suffix such as `.log`; the Mac's own
   `/usr/bin/mktemp` only replaces X's at the very end, so without
   Chapter 1's gnubin setup the log is literally named `…_XXXX.log`
   every run (*captured (2026-11-22)*, Mac without gnubin). Chapter 3's
   script stays as written. **Write to a temporary name, then `mv`:** the result is
   published under its real name only after the step succeeds, so a
   step that fails halfway never overwrites a good result with a
   partial one (Chapter 6's `>` lesson, now as a habit for every
   output). What it does **not** do: on a failed rerun, the previous
   run's finished file is still there, and so may be the half-written
   `.tmp`. The rule as the chapter states it: *publish a new result
   only after the step succeeds; on failure, an older result may still
   exist, so use the run's exit status and log to decide whether it
   belongs to this run.* (§10 shows this on a rerun.) One sentence on
   the assumption: a fixed `name.tmp` is fine when one run writes that
   output at a time, as in this book's pipeline; two simultaneous runs
   would share it (unique log names do not help), and that needs a
   unique temporary name and a deliberate policy, beyond this chapter.
   What to log: start and
   end time, host, tool versions, input checksums, the exact command,
   output checksum: Chapter 3's provenance list. `set -x` / `bash -x`
   as a way to see every command as it runs, in §11.
   [`tbl-log-recipes`; tip: write to `.tmp` then `mv`; self-check]
9. **Reading Chapter 3's script, line by line.** *Start hands-on:*
   `cat ~/bioinf-computing/src/01_count_reads.sh`; readers annotate
   each line in `NOTEBOOK.md` in their own words **before** opening the
   collapsed answer. Then the script shown as a code block with
   Quarto code annotations, one per line (the payoff of §2–§8):
   shebang; `set -euo pipefail`; `mkdir -p results logs` (no error if
   present); `log="$(mktemp "logs/…_$(date …)_XXXX.log")"` (nested
   substitutions, inner first); the `{ … }` group sends all its output
   through one pipe; `(cd data/raw && md5sum -c checksums.md5)` (a
   subshell, so the `cd` does not leak; `&&` stops if `cd` fails);
   `seqkit stats --quiet -T data/raw/*.fastq.gz > ….tmp` then `mv`;
   `} 2>&1 | tee "$log"` (stderr joins stdout, both to screen and log).
   *Then break it on purpose,* never in `data/raw/` (read-only,
   Chapter 3): copy the inputs and the script to scratch, append a
   byte to one copied input, and run the copy there in
   `~/bioinf-computing-ch08/proj-copy/` (decided 2026-11-19).
   *Captured with a stand-in seqkit:* `md5sum -c`
   prints `SRR6357070_2.fastq.gz: FAILED` and `md5sum: WARNING: 1
   computed checksum did NOT match`; the script exits 1; `results/`
   gets **no** `read_counts.tsv` (and no `.tmp`), and the log keeps the
   failure (*captured (Linux)* with real seqkit too). Why it stops
   although the failing command sits inside a piped group: `set -e` is
   inherited by the group's subshell, which exits 1, and `pipefail`
   passes that through `tee`'s success. With `set -eu` only (no
   `pipefail`), the same run prints the same `FAILED` lines but the
   script **exits 0** (*captured (Linux)*): `tee`'s status wins. Then
   run it from the wrong folder: `cd ~ && bash
   bioinf-computing/src/01_count_reads.sh` prints `md5sum:
   src/01_count_reads.sh: No such file or directory`, an empty
   `script:` line, then `cd: data/raw: No such file or directory`,
   exit 1, **and leaves empty `results/` and `logs/` folders in `~`**
   (*captured (Linux)*; the `md5sum` failure inside `echo "…$(…)"`
   does not stop the script, one more `set -e` exception). Readers
   add the guard after `set -euo pipefail` (decided 2026-11-19) and
   commit it in §12:

   ```bash
   [[ -f pixi.toml ]] || { echo "run from the project folder" >&2; exit 1; }
   ```

   The script's MD5 in the log changes, and §9 says so: that is what
   the `script:` line is for. Chapter 3's text stays as written.
   The `proj-copy/` test above used the unguarded copy; to repeat it
   with the guarded script, copy the project's `pixi.toml` into
   `proj-copy/` first, or it stops at the guard instead of the
   checksum (one sentence). One sentence on what the guard proves: it catches the common
   wrong-folder mistake (no `pixi.toml` here), not that this is the
   intended project.
   [code annotations; key idea: a failed step must stop the run, leave
   a log, and publish no new result; self-check]
10. **Numbered scripts as a simple pipeline.** *Start hands-on:* turn
    §2's `gtf_types.sh` into `src/02_gtf_summary.sh` (Chapter 6's
    decision): same header and strict mode as `01`; reads
    `data/ref/genes.gtf.gz`; writes `results/gtf_feature_counts.tsv`
    (`feature<TAB>count`, sorted by count, written via `.tmp` + `mv`,
    with a header line). It is **deliberately shorter than `01`**, and
    the text says so: its `log` lines go to stderr (no log file of its
    own), and it records input and output MD5s but not tool versions
    (recording versions is Chapter 23). The whole-run log file comes
    from `run_all.sh` below. The awk that prints two
    TSV columns is supplied (`awk -v OFS='\t' '{print $2, $1}'` after
    `uniq -c`; Chapter 6 taught `-v OFS`). Draft script (ShellCheck
    clean, *captured (Linux)* before the two MD5 lines were added;
    *to recapture*), with the guard and `log`/`die` from §8:

    ```bash
    #!/usr/bin/env bash
    # 02_gtf_summary.sh: count the feature types in the reference annotation.
    # Run from the project folder:  pixi run bash src/02_gtf_summary.sh
    # Input:  data/ref/genes.gtf.gz
    # Output: results/gtf_feature_counts.tsv (feature, count; most common first)
    set -euo pipefail

    log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }
    die() { log "ERROR: $*"; exit 1; }

    [[ -f pixi.toml ]] || die "run from the project folder"

    gtf="data/ref/genes.gtf.gz"
    out="results/gtf_feature_counts.tsv"
    [[ -s "$gtf" ]] || die "missing or empty: $gtf"

    mkdir -p results
    log "start; input md5: $(md5sum "$gtf")"
    {
      printf 'feature\tcount\n'
      gunzip -c "$gtf" | cut -f3 | sort | uniq -c | sort -k1,1nr \
        | awk -v OFS='\t' '{print $2, $1}'
    } > "$out.tmp"
    mv "$out.tmp" "$out"
    log "wrote $out ($(( $(wc -l < "$out") - 1 )) feature types)"
    log "output md5: $(md5sum "$out")"
    ```

    Output: the five counts as in *Outcome and check* (*captured
    (Linux)*); run from `~` it stops with `ERROR: run from the project
    folder`, exit 1. Then `src/run_all.sh`, which keeps the log of the
    **whole run** in `logs/` using exactly `01`'s pattern from §9
    (decided 2026-11-22 in reply to the Codex review: readers already
    know this form, and because `pipefail` is set inside the script,
    `tee`'s success cannot hide a failed step; a caller-side `… | tee`
    in the terminal would recreate the masking bug §9 just showed):

    ```bash
    #!/usr/bin/env bash
    # run_all.sh: run every numbered step in order; stop at the first failure.
    # Run from the project folder:  pixi run bash src/run_all.sh
    # Log: logs/run_all_<date>_XXXX.log (01 also keeps its own log)
    set -euo pipefail
    [[ -f pixi.toml ]] || { echo "run from the project folder" >&2; exit 1; }
    mkdir -p logs
    log="$(mktemp "logs/run_all_$(date +%Y-%m-%dT%H%M%S)_XXXX.log")"
    {
      bash src/01_count_reads.sh
      bash src/02_gtf_summary.sh
    } 2>&1 | tee "$log"
    ```

    (*Captured (2026-11-22, Mac, through `pixi run`):* exit 0; `01`'s
    log as in Chapter 3 (script `76fa8eb6…`, output `e1d81de7…`); `02`'s
    three lines, output MD5 `3b9c2b4c…`; ShellCheck 0.11.0 clean on all
    three scripts; the whole run in `logs/run_all_…log`. With the §9
    guard, `01`'s MD5 becomes `f2867b2a…`, and run from `~` it stops
    with `run from the project folder`, exit 1, leaving no `~/results`
    or `~/logs`.)
    *A failed rerun* (keeps §8's narrower promise honest), in
    `~/bioinf-computing-ch08/proj-copy/` with a copy of `02`,
    `genes.gtf.gz`, and the project's `pixi.toml`: run `02` once
    (succeeds; `md5sum results/gtf_feature_counts.tsv`), then replace
    the copied GTF with a truncated copy (`head -c` on a copy, as in
    Chapters 4 and 6) and rerun. *Captured (2026-11-22, Mac, Apple
    gzip; GTF cut to 5000 of its 10452 bytes):* the log's input MD5
    changes (`7e468876…`), then `gunzip: data/ref/genes.gtf.gz:
    unexpected end of file` and `… uncompress failed`, exit 1, **no**
    `wrote …` line; the old `results/gtf_feature_counts.tsv` keeps its
    MD5 `3b9c2b4c…`; and a leftover `.tmp` holds plausible-looking
    partial counts (`CDS 39`, `exon 39`, `start_codon 39`, `stop_codon
    38`, `transcript 38`). Show that `.tmp`: it is why the step never
    writes straight to the final name. The lesson in one sentence: the file on disk
    is the *last good* result, not this run's; the exit status and the
    log say which run you are looking at. The existing fresh-folder
    failure in §9 cannot show this, since there was no earlier result.

    Steps listed **by name**, not with a `src/[0-9]*.sh` glob, so a
    stray `03_old_try.sh` never runs by accident (one sentence; this
    is a choice, the glob version is shown as the alternative).
    *Then name it:* each step reads only raw inputs or earlier
    results, writes only its own outputs, and can be rerun safely
    (overwriting its own result, never an input), assuming one run at
    a time (§8). The number is the
    order; the name says what it does (Chapter 3's naming rule). *Then
    its limits,* as a short list that motivates Part VI: it reruns
    every step even if nothing changed; it runs one step at a time
    when steps 02 and 03 could run side by side; it cannot resume after
    a failure; it does not know which result came from which input
    version. Workflow managers (Chapter 25) and `make` (one sentence,
    with the GNU make manual link) solve these; nf-core (Chapter 26) is
    the one readers will use. A cluster version (each step as an
    `sbatch` job) is Chapter 10.
    [`fig-numbered-pipeline`; self-check]
11. **When a script misbehaves (short).** About one screen; decided
    2026-11-19 to keep it short, with depth in Chapter 34. *Start with
    a diagnosis:* a supplied script with two bugs from §3–§7 (unquoted
    `$f` on `Run 3 final`, a typo'd variable). Readers run it with
    `bash -x` and read the trace, which shows the split words
    (`+ gunzip -c Run 3 final/…`). Then `shellcheck` on the same file
    names both bugs before the script runs (*captured (Linux)*,
    ShellCheck 0.9.0: `SC2086 (info): Double quote to prevent globbing
    and word splitting`, with a "Did you mean" line, and `SC2154
    (warning): outdri is referenced but not assigned`, exit 1). The
    `bash -x` trace makes the typo vivid: `$outdri/counts.txt` became
    `/counts.txt`, refused with `Permission denied` only because an
    ordinary user cannot write to `/` (*captured (Linux)*). One
    sentence each: the VS
    Code ShellCheck extension underlines the same problems as you type
    (decided: also in the book environment; *checked 2026-11-22* on the
    Mac: install `timonwong.shellcheck` (tell readers to search that
    exact ID; plain searches were hard to find it with), no further
    setup; `$f` gets a dotted info underline and the hover reads
    `Double quote to prevent globbing and word splitting.
    shellcheck(SC2086)` with a Quick Fix), and the Mac's old bash (Chapter 7's
    promise): `/bin/bash` 3.2 lacks `mapfile`, `declare -A`, and
    `${x,,}` (*captured*), which `#!/usr/bin/env bash` plus Chapter 1's
    Homebrew bash avoids. No table; Chapter 34 covers debuggers and
    linting properly. [tip: run ShellCheck on every script; self-check]
12. **Saving scripts with git: the minimal routine.** *Start
    hands-on:* readers make `~/bioinf-computing` a git repository and
    commit their scripts, then break and recover one. One-time setup:
    check `git --version` (Xcode Command Line Tools on a Mac, from
    Homebrew's install in Chapter 1; preinstalled on Ubuntu/WSL and
    clusters; *to check* minimum versions, since `git restore` needs
    2.23), `git config --global user.name` / `user.email` and
    `git config --global init.defaultBranch main` **before** `git init`
    (without it, git 2.43 prints an 11-line `hint: Using 'master'…`
    block, *captured (Linux)*). Supplied `.gitignore` (`data/`,
    `results/`, `logs/`, `.pixi/`), explained in one sentence each and
    taught properly in Chapter 21. Then the routine (*captured*):
    `git init`; `git status --short` (`?? src/`); `git add .gitignore
    src/ README.md NOTEBOOK.md pixi.toml pixi.lock`; `git commit -m
    "Add read-count and GTF summary scripts"`; `git log --oneline`.
    Break it: comment out `set -euo pipefail` with `sed -i`; `git
    status --short` → ` M src/01_count_reads.sh`; `git diff` shows
    `-set -euo pipefail` / `+# set -euo pipefail` (*captured*), read
    **before** discarding anything; `git restore src/01_count_reads.sh`
    puts it back. One sentence on where that comes from: `git restore
    file` copies the **staged** version (the one `git add` recorded),
    which here is the same as the last commit because nothing was
    staged since; Chapter 21 explains the staging area fully. Then a
    small second change and commit (e.g. a clearer header comment in
    `02`; the first commit already holds the §9 guard and both
    scripts, which is fine), so `HEAD~1` exists. Recover an older version after that later commit:
    `git show HEAD~1:src/…` to look, `git restore --source=HEAD~1
    src/…` to bring it back (*captured*), rerun to check it works, and
    commit the recovery as a new commit. `git show --stat HEAD` shows
    which files a commit contains (`git log --oneline` shows only the
    messages).
    *Then name it:* a commit is a saved snapshot of the files you added,
    with a message saying why; git does not save `data/` or `results/`
    here, by design (they are rebuilt or backed up elsewhere, Chapter
    3), and a repository on the same disk is not an off-machine backup;
    pushing it to another machine is one way to make an independent
    copy (Chapter 22; Chapter 3 already says this). Habit: commit
    each time a script works and before changing it. Everything else
    (branches, undoing commits, remotes, `core.autocrlf`) is Chapter
    21. Link VS Code's Source Control view in one sentence.
    [`fig-git-routine`, `tbl-git-routine`; misconception
    `git-is-backup` (or reuse Chapter 3's `sync-is-backup`, see
    *Misconceptions*); self-check]
13. **Summary, exercises, further reading.** Summary as five bullets
    matching the learning goals, plus a one-screen "script template"
    readers can copy (no unconditional `|| true` in it; shebang, header comment, `set -euo pipefail`,
    `shopt -s nullglob` only if it loops over globs, usage check,
    `log`/`die`, work, write via `.tmp`). Exercises, then annotated
    further reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

Hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2):
the reader's files, values, and results `given` (blue, through the
whole pipeline); the reference annotation `ref`; `good` (green) only
for a check (a checksum that matches, a check badge); split words,
failures, and wrong results `warn`; shell and system text neutral
(`ink`, `line`, `muted`). (Revised 2026-11-22: `good` is not for
"correct or fixed" in general.)

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-script-anatomy` | 2 | static | Chapter 3's `01_count_reads.sh` (shortened) with brackets in the margin naming its parts: shebang, header comment (what, how to run), settings (`set -euo pipefail`), inputs and checks, work, outputs (via `.tmp` + `mv`), log. Reused in §9 as the map for the annotations. |
| `fig-word-splitting` | 3 | stepped (4 steps) | `gunzip -c $f` with `f="Run 3 final/sample_C_R1.fq.gz"`: (1) the line as typed; (2) `$f` replaced by its value; (3) the value split at spaces into three words (`warn`); (4) gunzip receives three file names and fails on each. A final frame shows `"$f"` arriving as one word (`given`, whole again). Same visual style as Chapter 5's `shell-steps.svg`, which set this step aside. |
| `fig-strict-mode` | 7 | static | Two columns, one script (`count.sh`) run on a missing file: left without strict mode (error line, then `0 reads`, `done`, exit 0: a wrong result in `warn`); right with `set -euo pipefail` (error line, stop, exit 1, no result). Below, three small strips for what it misses: `grep` no match (stops too early), `head` (status 141), tool exit 0 on bad input (does not stop). |
| `fig-numbered-pipeline` | 10 | static | `data/raw/*.fastq.gz` → `01_count_reads.sh` → `results/read_counts.tsv`; `data/ref/genes.gtf.gz` → `02_gtf_summary.sh` → `results/gtf_feature_counts.tsv`; `01` and `run_all.sh` drop a log into `logs/` (`02` logs through `run_all.sh`); `run_all.sh` above, calling them in order with a stop sign at a failure. FASTQ inputs and both results `given`; the GTF `ref`; `good` only for the `md5sum -c` check badge on `01`. A faint "Part VI" box on the right: what a workflow manager adds (skip unchanged steps, run in parallel, resume). Order-of-steps only, so Mermaid would be allowed, but an SVG matches the project-layout figures of Chapter 3. |
| `fig-git-routine` | 12 | static | Three boxes: your files (working folder) → `git add` → staged → `git commit` → history (a row of commits with messages); arrows back: `git restore file` (from the staged copy; normally the last commit here) and `git restore --source=HEAD~1 file` (from an older commit); `git status` and `git diff` as "look" labels on the first arrow. Kept minimal so Chapter 21 can draw the full model. |

Not used: screenshots (VS Code's Source Control view described in
text), manim.

### Interactive figure (Observable JS, optional)

- **Candidate, not for the first draft:** a "what does bash pass?"
  explorer: a text box for a variable's value and a toggle quoted /
  unquoted, showing the list of words the command receives. It would
  reinforce §3, but the stepped `fig-word-splitting` covers the
  lesson, and the self-check does too. Recommend: skip for now,
  revisit after readers test the chapter.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-expansions` | 3 | Form · what it gives · example on the practice tree · output (*captured*) — rows: `"$f"`, `"${f}"`, `$(cmd)`, `$(( expr ))`, `${f##*/}`, `${f%.gz}`, `${f/_R1/_R2}`, `"${rows[@]}"`, `${#rows[@]}` |
| `tbl-loop-patterns` | 4 | Task · pattern · pitfall it avoids — rows: every file matching a glob (`for f in */*_R1.f*q.gz`, with quotes), R1/R2 pairs, a numbered range, rows of a TSV (`while IFS=$'\t' read -r`), and the two "don't" rows (`for f in $(ls)`, `for line in $(cat file)`) |
| `tbl-tests` | 5 | Test · true when · example — files (`-e -f -d -s -r`), strings (`== != -z -n`), numbers (`-eq -ne -lt -le -gt -ge`, `(( ))`), with the `[[ 9 < 30 ]]` row marked as the trap |
| `tbl-special-params` | 6 | Name · holds · example with `./args.sh a.fq.gz "Run 3 final/c.fq.gz"` — `$0 $1 ${10} $# "$@" $* $? $$` |
| `tbl-strict-mode` | 7 | Setting · stops when · captured demo · does **not** catch · fix — rows `-e`, `-u`, `-o pipefail`, plus the five exceptions from §7. The `grep` row's fix is the status-sensitive `if` (1 = fine, 2 = error), never a blanket `\|\| true`; the `head` row's fix is "keep it in the terminal" |
| `tbl-log-recipes` | 8 | Goal · recipe — results to a file, messages to a log; both to screen and log (`2>&1 \| tee` **inside** a script with `pipefail`, as in `01` and `run_all.sh`); a message to stderr (`>&2`); a date-stamped unique log (`mktemp` + `date`); publish only on success (`.tmp` + `mv`; one run at a time) |
| `tbl-git-routine` | 12 | When · command · what it does — first time (`config`), once per project (`init`), every change (`status`, `diff`, `add`, `commit`), look back (`log --oneline`, `show HEAD~1:file`), undo an edit (`restore file`), bring back an old version (`restore --source=…`); a last row "everything else → Chapter 21" |

### Code (§6)

- `filename="Terminal (laptop)"` for commands; `filename="src/02_gtf_summary.sh"`
  etc. for script files. Tier 2 (shown, not run at render)
  throughout; everything is cheap. Cluster notes in prose only; no
  cluster commands in this chapter (scripts on a cluster are Chapter
  10).
- Scripts are shown whole, with **code annotations** for new lines (§9
  annotates every line). Readers adapt supplied scripts; no blank-file
  writing until exercise 4, which still starts from a skeleton.
- Failing runs are shown with their captured output and exit status in
  `.console` blocks. Where gzip wording differs (Apple vs GNU), the
  chapter shows GNU wording once captured and says messages vary.
- `rm -rf` with a variable appears only as text in the §3 pitfall,
  never in a runnable block.
- Every script in the chapter passes ShellCheck with no warnings
  (except the deliberately broken ones in §4 and §11), checked while
  drafting.
- Supplied files (`args.sh`, `count.sh`, the broken §11 script,
  `count_reads.sh` skeleton, `.gitignore`, `02_gtf_summary.sh`) are
  shown as code blocks with a `filename=` label; readers open the file
  with `code path/to/file`, paste, and save (Chapter 3's way; nano as
  the fallback), decided 2026-11-19. No heredocs in reader-facing
  blocks.

### Plots

None.

### Animation (manim)

None. The one sequence (word splitting) is a stepped SVG.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 3 | Key idea | Put double quotes around every `$…`; an unquoted value is split at spaces and matched as a wildcard |
| 3 | Pitfall | A misspelled variable is empty, not an error: `rm -rf "$outdri/"` is handed the argument `/`. Quotes keep an argument whole but do not check it; preview with `echo`, and use `set -u` (§7) |
| 4 | Pitfall | Loop over a glob, not over `ls` or `$(cat file)`; read table rows with `while IFS=$'\t' read -r` |
| 4 | Misconception | `for-reads-lines` |
| 7 | Key idea | `set -euo pipefail` stops a script when a command *reports* failure; it cannot see a wrong result from a command that reports success, so check outputs too |
| 7 | Pitfall | In a strict script, `grep` with no match and `… \| head` can stop the script although nothing is wrong |
| 7 | Misconception | `strict-mode-catches-all` |
| 8 | Tip | Write each output to `name.tmp`, then `mv` it into place, so a new result is published only after the step succeeds. On failure an older result may still exist: the exit status and log say whether it belongs to this run |
| 9 | Key idea | A failed step should stop the run, leave a log, and publish no new result |
| 11 | Tip | Run ShellCheck on every script before you trust it |
| 12 | Background | What git stores and what it does not (data and results are ignored here by design; a repository on the same disk is not an off-machine backup) |

`quotes-are-style`, `typo-variable-errors`, `script-stops-on-error`,
and the revisited entries are handled in text and self-checks to stay
under three callouts per screen.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: You run `bash ~/bioinf-computing/src/01_count_reads.sh` from
  `~`. What goes wrong, and why? (*`mkdir -p results logs` makes them
  in `~`, then `md5sum` cannot find `src/01_count_reads.sh` and `cd
  data/raw` fails (captured, Linux): relative paths are read from
  where you run it. Run from the project folder; §9 adds a guard.*)
- §3: `sample=WT_REP1; echo "$sample_R1.fastq.gz"`. What prints?
  (*`.fastq.gz`: bash read a variable called `sample_R1`, which is
  unset. Write `"${sample}_R1.fastq.gz"`.*)
- §4: A loop `for f in data/raw/*.fq.gz` prints `data/raw/*.fq.gz`
  once and then a tool says no such file. Why? (*No file matched, so
  bash passed the pattern unchanged. The files end in `.fastq.gz`;
  `shopt -s nullglob` would have made the loop run zero times.*)
- §5: `n=9; if [[ $n < 10 ]]; then echo small; else echo big; fi`.
  What prints? (*`big` (captured): `<` inside `[[ ]]` compares text,
  and `9` sorts after `1`. `(( n < 10 ))` prints `small`. The
  unquoted `$n` is not the problem: `[[ ]]` does not split, §3.*)
- §6: `./run.sh "sample A.fq.gz" b.fq.gz`. What are `$#` and `$1`?
  (*`2` and `sample A.fq.gz`.*)
- §7: Which of these stops a script with `set -euo pipefail`: (a) `grep
  -c XYZ file` with no match; (b) `seqkit stats` on a truncated file
  (seqkit 2.14.0); (c) `gunzip -c missing.gz | wc -l`? (*(a) yes,
  exit 1, although nothing is wrong; (b) no, seqkit exits 0; (c) yes,
  thanks to `pipefail`. For (a), the fix keeps `grep`'s status 2 (a
  real error) fatal, not a blanket `|| true`.*)
- §8: Why does `count_reads.sh` print its usage message with `>&2`?
  (*So it goes to stderr: with `> counts.tsv`, the message stays on
  screen and the file holds only results.*)
- §9: In Chapter 3's script, why `(cd data/raw && md5sum -c …)` in
  parentheses? (*A subshell: the `cd` ends with it, so the next line
  still runs from the project folder.*)
- §10: You add `03_plot.sh` but forget to list it in `run_all.sh`.
  What happens? (*It never runs; listing by name is deliberate, so
  check `run_all.sh` after adding a step.*)
- §11: ShellCheck says `SC2086: Double quote to prevent globbing and
  word splitting` on `gunzip -c $f`. Which section's rule is this?
  (*§3: quote every expansion.*)
- §12: You edited `02_gtf_summary.sh`, it broke, and you have not
  committed or staged. How do you get the last working version?
  (*Look with `git diff` first, then `git restore
  src/02_gtf_summary.sh`; check with `git status`. It restores the
  staged copy, which is the last commit when nothing was staged.*)

End-of-chapter exercises (core chapter, so required; all adapt
supplied material):

1. **Finish `count_reads.sh` (the check).** A supplied skeleton in
   `~/bioinf-computing-ch08/bin/count_reads.sh` loops over its
   arguments and prints a count per file, but has no quotes, no
   strict mode, and no usage check. Run it on `*/*_R1*` in the
   practice tree and record what is wrong (sample C `0`, the `.tmp`
   copy counted). Fix it in this order, rerunning after each change.
   **Part A** (after §6): quote `"$f"`, add the usage check, print the
   base name and count separated by a tab, and run with the tighter
   pattern. **Part B** (after §7): add `set -euo pipefail` and run the
   two failure cases, explaining what changed. Expected output and the
   failure cases as in *Outcome and check*. Record each change in
   `NOTEBOOK.md`.
2. **Check a sample table against the disk** (after §7). Start from
   the supplied `check_samples.sh TABLE`: §4's redirected `{ … } <
   "$table"` loop with the argument and file checks, header handling,
   and the `bad` flag already working, plus a scaffold comment where
   the R1 check goes. Readers add: for each row of `meta/samples.tsv`,
   whether its run folder holds an R1 file (only when the folder
   exists), problems to stderr, exit 1 if any row has a problem, and
   every bad row reported, not just the first. Then a
   separate prediction: a copy with `IFS=,` reading
   `samples_from_excel.csv`, which also tests the `reads` column
   numerically (`(( reads > 0 ))`), as in §4's example. Folder and R1
   checks alone pass; the number test fails with `arithmetic syntax
   error`. Explain why from Chapter 7's CRLF lesson (the `\r` is in
   the last field). The comma version is for this fixture only, not a
   CSV parser.

   **Answer, captured 2026-11-22** (Mac, Homebrew bash 5.3.15, the
   practice tree rebuilt from Chapter 5's block, `samples.tsv` MD5
   `971d8f74…`; scripts ShellCheck 0.11.0 clean). The supplied file is
   the §4 scaffold with usage/readable checks (`usage:
   check_samples.sh TABLE`, exit 2; `cannot read: nope.tsv`, exit 1)
   and the comment "Your turn: when the folder exists, check that it
   holds an R1 file for this sample". Run as supplied, it prints only
   the two `missing folder` lines, exit 1. The finished `else` branch:

   ```bash
       else
         r1=("$folder/${sample}"_R1.f*q.gz)      # needs shopt -s nullglob at the top
         if (( ${#r1[@]} == 0 )); then
           printf '%s: no R1 file in %s\n' "$sample" "$folder" >&2
           bad=1
         else
           printf '%s\t%s\n' "$sample" "${r1[0]}"
         fi
       fi
   ```

   Output on `meta/samples.tsv`, run from `share/`:

   ```
   sample_C	Run 3 final/sample_C_R1.fq.gz
   sample_A	run1/sample_A_R1.fastq.gz
   sample_B	run2/sample_B_R1.fastq.gz
   sample_E: missing folder run5
   sample_B	run2/sample_B_R1.fastq.gz
   sample_D: missing folder run4
   ```

   exit 1; with `2>/dev/null` only the four found rows remain (stdout
   and stderr apart, §8). The duplicate `sample_B` row is listed twice:
   a good "what else would you check?" follow-up, not required. A
   test table with an extra row `sample_Z<TAB>run1` adds `sample_Z: no
   R1 file in run1`; the first three data rows alone give exit 0. The
   piped version (`tail -n +2 … | while …; bad=1 …; exit "$bad"`) exits
   **0** on the same table (*captured 2026-11-22*). CSV copy (`IFS=,
   read -r sample folder _ reads`, plus `if ! (( reads > 0 ))`): every
   row prints `((: 12: arithmetic syntax error: invalid arithmetic
   operator (error token is "")` and the script's own `sample_C: reads
   is not a positive number: 12` (the `\r` is invisible, which is the
   puzzle); the folder and R1 lines are the same as for the TSV; exit
   1. The error does not stop the script, because it sits in an `if`.
   After `tr -d '\r'`, the CSV gives the TSV's result. Error wording
   differs by bash version (bash 5.1 on the clusters says `syntax
   error: invalid arithmetic operator`); the text says so.
3. **What strict mode misses.** A supplied script counts reads in a
   file and then reports "OK". Three supplied bad inputs: a missing
   file, a truncated `.gz`, and a valid gzip stream with **no content**
   (made with `gzip < /dev/null > empty.fastq.gz`; not the same as a
   zero-byte file named `.gz`, which `gunzip` rejects). First add `set
   -euo pipefail` and predict which inputs it stops (*captured
   (Linux)*: missing → `gzip: missing.fastq.gz: No such file or
   directory`, exit 1; truncated → `gzip: trunc.fastq.gz: unexpected
   end of file`, exit 1; empty stream → `empty.fastq.gz: 0 reads`,
   `OK`, exit 0). Then add a **positive read-count check** (stop if
   the count is not above zero) for the empty stream. Note in the
   answer that `gzip -t` and `[[ -s … ]]` both pass the empty stream
   (it is valid and has a nonzero compressed size), so they are not
   the check here. The count is lines ÷ 4, which holds only for these
   plain four-line toy records; it is not a FASTQ validator (Chapter
   15's tools are).
4. **Add a step to the project.** Write `src/02_gtf_summary.sh` from
   the supplied skeleton (header, strict mode, `log`, `.tmp` + `mv`),
   add it to `run_all.sh`, run the whole pipeline through pixi, and
   compare `results/gtf_feature_counts.tsv` with Chapter 6's check.
   Then commit both scripts with a message saying what they do (one
   commit for both is fine; check with `git show --stat HEAD`).
5. **Break, see, recover.** In the project, make a deliberate change to
   `src/02_gtf_summary.sh` (e.g. drop the header line), commit it (so
   at least two commits exist), then use `git log --oneline --
   src/02_gtf_summary.sh`, `git diff HEAD~1`, and `git restore
   --source=HEAD~1` to bring back the working version, rerun
   `run_all.sh` to verify, and commit the recovery as a new commit.
   Record the commands in `NOTEBOOK.md`.

## Examples and data

- **Toy files**, made by readers in `~/bioinf-computing-ch08`:
  `gtf_types.sh`, `count.sh`, `args.sh`, `bin/count_reads.sh`
  (skeleton), the broken §11 script, exercise 2 and 3 scripts and
  inputs. A truncated `.gz` for exercise 3 is made from a practice-tree
  file (`head -c` on a **copy**), as in Chapters 4 and 6.
- **Chapter 5 practice tree** `~/bioinf-computing-ch05/share/`, read
  only: the R1/R2 files in `run1/`, `run2/`, `Run 3 final/`, the
  `.tmp` copy, `meta/samples.tsv` (MD5
  `971d8f742cb76a8d181d3bdc3dcbceaa`, recaptured 2026-11-19) and
  `meta/samples_from_excel.csv`, and `../where.sh`.
- **Running dataset:** the project `~/bioinf-computing` from Chapter 3:
  `src/01_count_reads.sh`, `data/raw/SRR6357070_{1,2}.fastq.gz`,
  `data/raw/checksums.md5`, `data/ref/genes.gtf.gz`. New files the
  reader adds: `src/02_gtf_summary.sh`, `src/run_all.sh`,
  `.gitignore`, `.git/`, `results/gtf_feature_counts.tsv`. Nothing new
  to download, so no new rows in `data/README.md`.
- **Captured** (2026-11-19, macOS 15 Intel, Homebrew bash 5.3.15, GNU
  coreutils/sed/grep, Apple gzip 457.140.3, Apple git 2.50.1):
  - Unquoted loop over `*/*_R1*`: three `gunzip: can't stat:` lines,
    sample C `0`, the `.tmp` file counted as `3`, exit 0. Quoted: C
    `4`. With `*/*_R1.f*q.gz` and `basename`: three TSV lines, C 4, A
    2, B 3 (glob order on the test Mac: `Run 3 final` first).
  - `for f in */*.bam` with no match → one pass with the literal
    pattern; with `shopt -s nullglob` → zero passes.
  - `d="Run 3 final"; ls $d` → three `ls: cannot access` errors,
    exit 2; `ls "$d"` → the two files.
  - `echo "would delete: $outdri/"` → `would delete: /`; with `set -u`
    → `outdri: unbound variable`.
  - `[[ 9 < 30 ]]` false; `(( 9 < 30 ))` and `[ 9 -lt 30 ]` true.
  - `${f##*/}` → `sample_C_R1.fq.gz`; `${b%%_R1*}` → `sample_C`;
    `${f%.gz}` → `Run 3 final/sample_C_R1.fq`.
  - `rows` list: `28 items`; `"${rows[5]}"` → `Run 3 final`.
  - Pairs with `"${r1/_R1/_R2}"`: three pairs found.
  - `while IFS=$'\t' read -r …` on `samples.tsv`: `sample_E` (`run5`)
    and `sample_D` (`run4`) MISSING, others found, `Run 3 final`
    whole. `for line in $(…)`: one word per item. CSV with `IFS=,`:
    `== 30` never matches; `(( r > 10 ))` → `((: 12: arithmetic syntax
    error: invalid arithmetic operator (error token is "")`.
  - `count.sh` without strict mode: missing file → error, `0 reads`,
    `done`, exit 0; no argument → `gunzip: can't stat:  (.gz)`, `: 0
    reads`, exit 0. With `set -euo pipefail`: missing → exit 1, no
    count; no argument → `./count.sh: line 4: $1: unbound variable`,
    exit 1.
  - `set -e` alone: `lines=$(gunzip -c missing.gz | wc -l)` →
    `lines=0`, script continues, exit 0. `PIPESTATUS` → `1 0`.
  - Strict mode: `n=$(grep -c ZZZ file)` → exit 1 with no message;
    `|| true` → `n=0` (but also masks a missing file, *captured
    (Codex)*); status-sensitive `if` → `n=0` on no match, exit 2 on a
    missing file (*captured 2026-11-22*). `true && false` → stops,
    exit 1; `false && echo skipped` → continues (*2026-11-22*).
    `read` with `IFS=$'\t'` on `a<TAB><TAB>b<TAB>c` → `a`, `b`, `c`,
    empty fourth field (*2026-11-22*). `seq 1 1000000 | head -n 1` → prints `1`, exit
    141. `gunzip -c` of a two-read file `| head -n 1` → continues.
    `if grep -q …` with no match → continues. Function with `false`
    called from `if` → continues past `false`. `local x=$(false)` →
    continues. `wc -l < empty.txt` → `0`, continues.
  - `bash -c 'set -u; …'` exits **127** on an unbound variable, while a
    script file exits 1: use script files for the demos so the status
    shown is 1.
  - `/bin/bash` 3.2.57: `mapfile: command not found`; `declare: -A:
    invalid option`; `${x,,}: bad substitution`.
  - `args.sh`: no arguments → usage on stderr, exit 2; with `a.fq.gz
    "Run 3 final/c.fq.gz"` → `$#` = 2, `"$@"` two items, `$*` four.
  - Chapter 3's script with a stand-in `seqkit`: good inputs → log as
    in Chapter 3 and `results/read_counts.tsv`; one input with a byte
    appended → `SRR6357070_2.fastq.gz: FAILED`, `md5sum: WARNING: 1
    computed checksum did NOT match`, exit 1, `results/` empty, log
    file written.
  - git: `git init` → `Initialized empty Git repository in …/.git/`;
    `git status --short` before adding → `?? .gitignore`, `?? src/`;
    after an edit → ` M src/01_count_reads.sh`; `git diff` hunk
    `-set -euo pipefail` / `+# set -euo pipefail`; `git restore` →
    clean; `git restore --source=HEAD~1` → ` M` with the older text.
- **Captured (Linux)** (2026-11-19, Ubuntu 24.04 container, details
  in the status line): GNU gzip messages (`gzip: Run.gz: No such file
  or directory`, `gzip: missing.fastq.gz: …`, `gzip: trunc.fastq.gz:
  unexpected end of file`); the exercise 1 skeleton (unquoted `$@` and
  `$f`) prints `Run 0`, `3 0`, `final/sample_C_R1.fq.gz 0`, the A and B
  counts, and the `.tmp` copy, exit 0; the finished `count_reads.sh`
  as in the check; glob order `Run 3 final` first in `C.UTF-8`;
  `run_all.sh` end to end with real seqkit (`01`'s log as in Chapter
  3, same script MD5 `76fa8eb6…`, same output MD5 `e1d81de7…`; `02`'s
  five counts); `02` from `~` → `ERROR: run from the project folder`;
  `01` from `~` (no guard) → stray `~/results` and `~/logs`; strict
  `gunzip -c … | head` → 141, 6 of 6; corrupted copy → exit 1, no
  results; same without `pipefail` → exit 0; truncated R2 with
  regenerated checksums → seqkit `[ERRO]`, exit 0, header-only
  results; ShellCheck 0.9.0 on the broken script (SC2086 info, SC2154
  warning), on the skeleton (SC2068 error for `$@`, SC2086 ×2), and
  no findings on `01`, `02`, `run_all.sh`, `count_reads.sh`; exercise
  3's three inputs; git 2.43.0 `init` hint, `status`, `diff`,
  `restore`.
- **Checks done 2026-11-22** (`chapter_08_checks.md`, results
  table): Mac through `pixi run` (`run_all.sh`, ShellCheck 0.11.0,
  failed rerun, VS Code extension); Nova, Atlas, Ceres (git, bash
  5.1.8, no ShellCheck outside pixi, strict `gunzip | head` 141 ×3,
  glob order); exercise 2's full answer (§ Exercises). **Still to
  capture (optional):** `run_all.sh` through pixi on a cluster; nothing
  cluster-specific was found.
- Where commands run: laptop only. A one-paragraph note in §1 says the
  same scripts run unchanged on a cluster login node for small inputs
  and as jobs for real ones (Chapter 10).

## Misconceptions

New entries for the book's `misconceptions.yml`, to add when this plan
is agreed. Existing entries revisited here get `08-shell-scripts` added
to `chapters` where missing: `relative-to-script` (already lists it),
`pipe-stops-on-error` (already lists it), `no-error-means-correct`,
`script-needs-bash` (already lists it), `csv-is-csv`,
`program-sees-wildcard`, `sort-is-numeric`.

- `script-stops-on-error`: "If a command in my script fails, the script
  stops." By default bash moves on to the next line, so later steps
  run on missing or partial results and the script can still exit 0.
  `set -e` changes that. Probe: a script without `set -e` runs `gunzip
  -c missing.gz | wc -l`, then `echo done`. What prints, and what is
  the exit status? (An error, `0`, `done`; exit 0.) [text and
  `fig-strict-mode`, §7; first raised as Chapter 1's pitfall]
- `strict-mode-catches-all`: "With `set -euo pipefail` my script stops
  on every error." It stops on a nonzero exit status, except in
  conditions, some function calls, and masked assignments, and it
  cannot see a tool that reports success on bad input; it can also stop
  on harmless statuses (`grep` no match, `head` closing a pipe). Probe:
  which stops a strict script: `grep -c XYZ file` with no match, or
  seqkit 2.14.0 on a truncated file? (The `grep`; seqkit exits 0.)
  [callout and self-check, §7]
- `quotes-are-style`: "Quotes around variables are just style; the
  script works without them." Unquoted values are split at spaces and
  matched as wildcards, so a name with a space becomes several
  arguments. Probe: `f="Run 3 final/a.fq.gz"; ls $f`: how many names
  does `ls` get? (Three.) [key idea and `fig-word-splitting`, §3]
- `typo-variable-errors`: "If I misspell a variable, bash gives an
  error." An unset variable expands to nothing, silently, unless `set
  -u` is on. Probe: what argument does `rm -rf "$outdri/"` receive if
  `outdri` is unset? (`/`.) [pitfall, §3; resolved in §7]
- `for-reads-lines`: "`for line in $(cat file)` goes through a file
  line by line." It goes word by word, split at spaces and tabs, and
  matches wildcards; read lines with `while IFS= read -r line`. Probe:
  how many passes for a two-line file whose first line is `sample_C
  Run 3 final`? (More than two: one per word.) [misconception callout,
  §4]
- `git-is-backup` (decided: a new entry, decision 10): "My scripts are in git, so they are backed
  up." A repository on the same disk is not an off-machine backup; a
  local `.git/` is lost with the disk (pushing to another machine is
  one way to make an independent copy). **Check first** whether Chapter 3's `sync-is-backup`
  or its git sentence already covers this; if so, extend that entry's
  `chapters` instead of adding a new id. [background callout, §12]

## Links to other chapters and books

- Builds on: Chapter 1 (read-count line, stop-at-first-error pitfall),
  Chapter 3 (`01_count_reads.sh`, naming rule, provenance, project
  layout), Chapter 4 (exit status, `no-error-means-correct`), Chapter 5
  (quoting, globs, practice tree, `where.sh`), Chapter 6 (streams,
  pipes, `grep` status, `141`, the GTF count), Chapter 7 (shebang, `x`
  bit, `$0`, functions, `command -v`, bash 3.2, CRLF).
- Leads to: Chapter 9 (running a long script under tmux); Chapter 10
  (the same scripts with `#SBATCH` lines; job arrays replace the `for`
  loop over samples; `SLURM_*` variables as inputs); Chapters 12–13 (R
  and Python scripts: same habits, `Rscript`/`python3` shebangs,
  arguments via `commandArgs` / `sys.argv`); Chapter 14 (sample sheets
  read by code); Chapter 21 (git in full; `.gitignore`); Chapter 22
  (pushing to GitHub as the off-machine copy); Chapter 23 (recording
  versions in the log); Chapter 25 (what a workflow manager adds over
  `run_all.sh`); Chapter 26 (nf-core runs as the real pipeline);
  Chapter 34 (functions, `getopts`, tests); Genomics and
  Transcriptomics books (per-sample loops over real pipelines).

## Official links to include

- GNU Bash manual (gnu.org/software/bash/manual): *Shell Parameters*,
  *Shell Expansions* (word splitting, parameter expansion, filename
  expansion and `nullglob`), *Looping Constructs*, *Conditional
  Constructs*, *Bash Conditional Expressions*, *The Set Builtin*
  (`-e` exceptions listed exactly), *Shell Functions*.
- POSIX Shell Command Language (pubs.opengroup.org), for "`[ ]` vs
  `[[ ]]`" background only.
- ShellCheck (shellcheck.net; github.com/koalaman/shellcheck) and its
  wiki pages per code (e.g. SC2086); VS Code ShellCheck extension on
  the Visual Studio Marketplace (official publisher page).
- Git: git-scm.com docs for `git init`, `status`, `diff`, `add`,
  `commit`, `log`, `restore`, `show`; *Pro Git* book (git-scm.com/book,
  CC BY-NC-SA) chapter 2 "Git Basics".
- VS Code docs: *Source Control* overview (code.visualstudio.com/docs).
- GNU make manual (gnu.org/software/make/manual), one sentence in §10.
- Software Carpentry *The Unix Shell*, episodes "Loops" and "Shell
  Scripts" (swcarpentry.github.io/shell-novice).

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Keys already in
`references.bib` need no new verification; new ones are verified with
scite or the publisher and BibTeX fetched from the DOI or official page
before adding.

- `shotts2025linux`, *The Linux Command Line*: Part 4 "Writing Shell
  Scripts" (variables, `if`, loops, positional parameters) is the
  closest one-to-one match. Main pick. *(In bib.)*
- `wilson2019swcarpentry`, *The Unix Shell*: "Loops" and "Shell
  Scripts" episodes, a second walk-through with exercises. *(In bib.)*
- `wilson2017good`, "Good enough practices in scientific computing"
  (PLoS Comput Biol): the software and project sections back §10 and
  §12 (name scripts by order, version control, one command to rerun).
  *(In bib.)*
- `ramey2025bash`, GNU Bash manual: *The Set Builtin* for the exact
  `-e` exceptions; desk reference. *(In bib.)*
- `buffalo2015bioinformatics`, *Bioinformatics Data Skills*, chapter
  12 "Bioinformatics Shell Scripting, Writing Pipelines, and
  Parallelizing Tasks": same audience, covers `set -euo pipefail`,
  loops over samples, and `make`. *(In bib.)*
- *Pro Git* (Chacon & Straub, 2nd ed., Apress; CC BY-NC-SA online),
  chapter 2, for readers who want more git before Chapter 21. New key;
  check edition and fetch metadata before adding. Optional.

## Austin's notes

-

## Decisions (2026-11-19, open questions round)

Austin's choices, all as recommended:

1. **ShellCheck: both.** Add `shellcheck` to `setup/pixi.toml` and
   mention the VS Code ShellCheck extension. **To do:** `pixi add
   shellcheck` in `setup/` on a machine with pixi, so `pixi.lock` is
   regenerated with it; not done here (pixi is not installed on the
   machine this plan was written on, and editing `pixi.toml` without
   the lock would break `pixi install --locked` for readers, since
   `setup-url` points at `main`). Listed in `chapter_08_checks.md`.
   Still not in `setup/pixi.toml` (checked 2026-11-22): a drafting
   dependency. The chapter also needs a short upgrade step for readers
   who downloaded the Chapter 2 environment earlier (download the new
   `pixi.toml`/`pixi.lock` into `~/bioinf-computing`, then `pixi
   install --locked`; or `pixi add shellcheck` in the project).
2. **Supplied files: VS Code paste.** `code file`, paste, save; nano as
   fallback; no heredoc blocks for readers.
3. **Breaking Chapter 3's script: copies in scratch.** Inputs, checksums,
   and script copied to `~/bioinf-computing-ch08/proj-copy/`; nothing
   in `data/raw/` is touched.
4. **Edit Chapter 3's script: yes.** Readers add the `[[ -f pixi.toml
   ]]` guard in §9 and commit it in §12; the changed MD5 in the log is
   explained. Chapter 3's text is unchanged.
5. **`git init` in Chapter 8**, on `~/bioinf-computing`, with
   `init.defaultBranch main` set first and the supplied four-line
   `.gitignore`. Chapter 21 starts from that repository.
6. **git version: check clusters first.** Austin runs `git --version`
   on Nova, Ceres, and Atlas; if any is older than 2.23, add a
   one-line `git checkout -- file` fallback (see *Open questions*).
7. **Runner: `run_all.sh`**, steps listed by name; `make` gets one
   sentence; Chapter 25 keeps "Make basics".
8. **Checks file: written now** (`chapter_08_checks.md`).

## Decisions (2026-11-22, after the Codex review)

9. **Whole-run log inside `run_all.sh`**, with `01`'s `{ … } 2>&1 |
   tee "$log"` pattern (not a terminal capture command), as drafted in
   §10.
10. **New misconception `git-is-backup`**, separate from Chapter 3's
    `sync-is-backup` (which is about sync services, not git).
11. **Plan agreed.** The Chapter 8 misconceptions were added to
    `misconceptions.yml`, and `08-shell-scripts` was added to
    `csv-is-csv` and `sort-is-numeric`. The other revisited entries
    already listed it.

## Open questions

1. ~~**git versions on the clusters**~~ (decision 6), **closed
   2026-11-22:** Nova 2.47.3, Atlas 2.47.3, Ceres 2.52.0. `git restore`
   works on all three, so **no `git checkout --` fallback is needed**.
   All print the `master` hint, worded differently (2.52: `will change
   to "main" in Git 3.0`), so §12 describes the hint rather than
   quoting it.
2. ~~**Misconceptions**~~: done 2026-11-22 (decisions 10–11).
