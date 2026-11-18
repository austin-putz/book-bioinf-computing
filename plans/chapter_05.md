---
title: "Chapter 5 — Shell basics"
subtitle: "Chapter plan · core · draft"
date: 2026-11-17
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
draft plan, 2026-11-17, revised the same day after the Codex review
(`chapter_05_codex_review.md`; see *Review responses*). **Chapter drafted
2026-11-17** in `chapters/05-shell-basics.qmd`; see *Drafting notes*
for where the draft departs from this plan. Outputs marked *captured* were recorded on
2026-11-17 with Homebrew bash 5.3.15, GNU coreutils 9.11, and GNU
findutils 4.11.0 (the Chapter 1 macOS setup, macOS 15 Intel) in a
scratch folder; recheck on Ubuntu/WSL while drafting. The rest are to be
captured while drafting.

## From `PLAN_CHAPTERS.md`

- What a shell is; bash
- Filesystem tree, paths (absolute vs relative), home directory
- Navigating, creating, copying, moving, deleting
- Symbolic links (`ln -s`)
- Wildcards and tab completion; quoting paths
- Finding files (`find`)
- Viewing files: `cat`, `less`, `head`, `tail`
- Command history and shortcuts

## What this chapter builds on

Part I used many shell commands "explained in Part II". This chapter is
where they are explained, so it opens by pointing back at them rather
than pretending they are new.

- **Chapter 1:** terminal, prompt, shell, bash (glossary: first met in
  Ch 1 §2, taught here); `mkdir -p … && cd …`, `ls -lh`, `cat`,
  `head -n 8`, `wc -l`, `mv`, `cp` with a quoted Windows path, `curl
  -fLO`. Pipes, `$(…)`, and `>`/`>>` were used there too, but belong
  to Chapter 6 (pipes, redirection) and Chapter 8 (variables).
- **Chapter 2:** `pixi run`, `which code`, nano and vim, `code .`,
  `hostname`, `pwd`; `~/bioinf-computing` as the project folder.
- **Chapter 3:** the project layout (`data/raw` read-only, `data/meta`,
  `data/ref` symlink, `src/`, `results/`, `logs/`, `README.md`,
  `NOTEBOOK.md`); naming rules (no spaces, "you will still learn to
  quote paths, Chapter 5"); `ln -s` and `unlink`, and the
  `symlink-is-copy` misconception (trailing slash on `rm -r link/`);
  `chmod a-w` (explained in Chapter 7); `touch`; the messy folder with
  `"plot 1.png"`.
- **Chapter 4:** `--help`, `man` ("`less` keys in Chapter 5"); the
  unmatched `data/raw/*.fq.gz` passed on literally ("why bash does
  this: Chapter 5"); the wrong-folder case (`cd ~` then a relative
  script path fails); `command not found`.

Out of scope here (owned elsewhere): pipes, redirection, `grep`, `sort`,
`zcat` (Chapter 6); permissions, `PATH`, `.bashrc`, processes, `du`
(Chapter 7); variables, loops, scripts (Chapter 8); `rsync`, `tmux`
(Chapter 9). Chapter 5 uses `|` in a few supplied commands readers copy
without needing to understand it: `gunzip -c … | head` (met in Chapter
1), `history | tail`, and the `sort` in the chapter check. Each is
labelled "pipes: Chapter 6".

## Outcome and check

- **Outcome:** readers move around the filesystem with absolute and
  relative paths and always know where they are; create, copy, move,
  rename, link, and delete files and folders without overwriting or
  deleting by accident; predict what a wildcard matches before using it,
  quote names with spaces, and use tab completion; find files by name,
  type, size, and age with `find`; look inside text files of any size
  with `less`, `head`, and `tail`, and recognise a compressed or binary
  file before `cat` floods the screen; and recall and edit earlier
  commands instead of retyping them.
- **Check:** Exercise 3, *Tidy a lab share*. Readers start from the
  supplied messy folder `~/bioinf-computing-ch05/share/` (built by a
  paste block in §1). They end with `~/bioinf-computing-ch05/tidy/fastq/`
  holding one link per read file, each pointing to the **right** source
  and named consistently, and with the broken link and the temporary
  file removed from `share/`. Four supplied check commands (the `sort`
  is a pipe, explained in Chapter 6):

  ```bash
  find ~/bioinf-computing-ch05/tidy -type l -printf '%f -> %l\n' | sort
  find ~/bioinf-computing-ch05/tidy -xtype l      # broken links: prints nothing
  find ~/bioinf-computing-ch05/tidy -type f       # ordinary files: prints nothing
  find ~/bioinf-computing-ch05/share \( -xtype l -o -name '*.tmp' \) -print   # prints nothing
  ```

  Expected output of the first (*captured* 2026-11-17 by running the
  answer key against the setup block; `/home/you` is your own home
  folder, so compare everything after it):

  ```
  sample_A_R1.fastq.gz -> /home/you/bioinf-computing-ch05/share/run1/sample_A_R1.fastq.gz
  sample_A_R2.fastq.gz -> /home/you/bioinf-computing-ch05/share/run1/sample_A_R2.fastq.gz
  sample_B_R1.fastq.gz -> /home/you/bioinf-computing-ch05/share/run2/sample_B_R1.fastq.gz
  sample_B_R2.fastq.gz -> /home/you/bioinf-computing-ch05/share/run2/sample_B_R2.fastq.gz
  sample_C_R1.fastq.gz -> /home/you/bioinf-computing-ch05/share/Run 3 final/sample_C_R1.fq.gz
  sample_C_R2.fastq.gz -> /home/you/bioinf-computing-ch05/share/Run 3 final/sample_C_R2.fq.gz
  ```

  The other three print nothing. Six working links that all point to
  one file would pass the second check but not the first, which is why
  the first lists every target.

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Say what the shell does with a command line before a program runs,
   and tell a shell builtin from a program.
2. Move around the filesystem with absolute and relative paths, `~`,
   `.`, and `..`, and check where you are with `pwd`.
3. Create, copy, move, rename, link, and delete files and folders, and
   avoid the commands' silent overwrites and permanent deletes.
4. Predict what a wildcard matches, quote names with spaces or special
   characters, and use tab completion and history to type less.
5. Find files with `find`, and look inside files with `less`, `head`,
   `tail`, and `file`.

## Sections

Same pattern as Chapters 1–4: each section opens with something readers
run or predict, then names the idea. Commands run on the laptop unless a
step says otherwise; a cluster note in §3 shows the same tree on a login
node. Practice happens in the scratch folder `~/bioinf-computing-ch05`, so
mistakes cannot touch the project. In `~/bioinf-computing` readers only
look at files; the one thing they write there is their own notes in
`NOTEBOOK.md`, as in Chapters 3–4. Visual items in brackets are
specified under *Visuals and teaching aids*.

**Minimum path.** The chapter is large, so the first pass is:
navigating (§3), `ls` (§4), copy/move/delete with the preview habit
(§5), relative link targets (§6), wildcards and quoting (§7), basic
`find` (§8: `-name`, `-type`, `-maxdepth`), and `head`/`less`/`tail`
(§9). Marked as recognition/reference in the text: `readlink -f` and
`realpath`, brace ranges, `find` size and age tests, `-exec`/`-delete`,
history expansion (`!!`, `!$`). Exercises show one completed example
and ask readers to adapt it, never to write from a blank prompt.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   you have already run about thirty shell commands by copying them; now
   you learn what each part does, so you can change them and predict
   what they will do. Set-up block: one paste that builds the practice
   tree `~/bioinf-computing-ch05/share/` (block and contents under
   *Examples and data*; tested end to end). Readers are told it is safe
   to paste without understanding yet: this chapter explains `mkdir`,
   `cd`, `cp`, `touch`, and `ln -s`; the rest (`printf`, `gzip` and the
   pipe, the `rows=(…)` list) is explained in Chapters 6 and 8 or not at
   all, and readers can look at the files it makes now. The block ends
   with `ls -A share` and its expected output. **Pasting it twice is
   safe:** the second time `mkdir` stops with `File exists` and nothing
   else runs (*captured*). To rebuild the tree on purpose (Chapters 6–8
   may say so), rename the old one first, `mv
   ~/bioinf-computing-ch05/share ~/bioinf-computing-ch05/share_old`,
   and paste again; the book never deletes a scratch folder for you.
2. **What a shell is.** *Start hands-on:* type `ls`, then `lss`
   (`bash: lss: command not found`, Chapter 4's table), then `type cd`
   and `type ls` (*captured*: `cd is a shell builtin`; `ls is
   /usr/bin/ls` on Linux, the gnubin path on macOS). *Then name the
   parts:* terminal (the window), shell (the program reading what you
   type: bash), command (a program or builtin the shell starts). The
   shell's job on every line, kept short but accurate for the commands
   in this chapter: (1) bash reads the line into **words**, at spaces
   but respecting quotes and backslashes (`"plot 1.png"` stays one
   word); (2) it expands `~`, wildcards, and `$…` where quoting allows;
   (3) it removes the quote characters themselves; (4) it finds the
   command and starts it with the resulting **arguments**. Quoting
   decides what happens in steps 1–2. A file name produced by a
   wildcard is one argument even if it contains spaces (§7 shows it with
   `printf '<%s>\n'`). Do not call step 1 "word splitting": bash uses
   that term for something later (splitting unquoted `$…` results),
   which is Chapter 8. This is the frame for the whole chapter: quoting
   and wildcards (§7) are steps 1–3; `PATH` (Chapter 7) is step 4.
   Authoritative order: the Bash manual's *Shell Expansions*. The
   command-line anatomy: command, options, arguments, as in Chapter 4's
   usage line. Builtins (`cd`, `pwd`, `echo`, `type`, `history`) are
   part of bash; why `cd` must be one (a separate program could not
   change *your* shell's folder) in one sentence. Bash vs zsh in two
   sentences, pointing at Chapter 1's decision: the book uses bash
   everywhere; `echo "$BASH_VERSION"` checks it. The prompt again: what
   `you@host:~/bioinf-computing$` tells you (user, machine, folder),
   and that clusters set it up for you. [`fig-shell-steps` (stepped);
   key idea; self-check]
3. **The filesystem tree and paths.** *Start hands-on:* `pwd`, `cd
   ~/bioinf-computing`, `pwd`, `ls`, `cd data/raw`, `pwd`, `cd ..`,
   `cd ../..`, `cd -`, `cd` alone. Readers predict each `pwd` before
   running it. *Then name the parts* with the tree figure: one tree
   starting at `/` (root); the home folder and `~`; absolute paths
   start with `/` (or `~`, which bash turns into one), relative paths
   start from the **current working directory**; `.` and `..`. Where
   home is (table): Linux and WSL `/home/you`, macOS `/Users/you`,
   clusters `/home/you` plus project and scratch areas elsewhere
   (`/project/…`, `/90daydata/…` on SCINet, `/work/…` on Nova; details
   in Appendix A and Chapter 10). WSL's `/mnt/c` recalled (Chapter 1's
   pitfall). Case sensitivity recalled in one line (Chapter 3). The
   rule: a relative path means "from where I am now", not "from where
   the script is". *Shown with a two-line scratch script*, made by §1's
   setup block: `~/bioinf-computing-ch05/where.sh` holds only `pwd` and
   `ls data/raw`. Run it by its absolute path from two places: from
   `~/bioinf-computing` it lists the raw files; from `~` it prints
   `/home/you` and `ls: cannot access 'data/raw': No such file or
   directory` (*captured*). Same script, different working directory,
   different result. Chapter 4's wrong-folder case is related but not
   the same: there `pixi run` itself refused to start (`could not find
   pixi.toml…`), because pixi looks for its manifest in the current
   folder and its parents; one sentence says so. Tab completion
   introduced here as a tip (full treatment in §7): type `cd ~/bioi`
   and press Tab; after Chapters 1–4 several folders start with
   `bioinf-computing`, so it stops at the common part; press Tab twice
   to see the choices, type a few more letters, Tab again. Errors met:
   `cd: nowhere: No such file or directory` (*captured*), `cd: …: Not
   a directory`. **Cluster note:** the same commands on a Nova login
   node (decided; capture while drafting): `pwd` after login shows the
   cluster home, which is not the laptop's. Home only: project and
   scratch areas are left to Chapter 10 and Appendix A.
   [`fig-filesystem-tree`, `fig-cd-steps` (stepped),
   `tbl-path-shortcuts`, `tbl-home-by-system`; tip: Tab; misconception
   `relative-to-script`; self-check]
4. **Looking around: `ls` and its options.** *Start hands-on:* in
   `~/bioinf-computing`, `ls`, `ls -l`, `ls -lh data/raw`, `ls -a`,
   `ls -lt logs`, `ls -ld data/raw`, `ls -F`. *Discovery:* `ls -a`
   shows `.pixi/`, the hidden folder where Chapter 2's environment
   lives (do not edit it by hand; `pixi install` rebuilds it), plus `.`
   and `..`. Names starting with `.` are hidden by convention, not
   protected. *Then read one `ls -l` line* with a figure: type and
   permissions (first column; `d` folder, `l` link, `-` file; the rest
   is Chapter 7), owner and group, size (`-h` for human units; a
   folder's size is not its contents', Chapter 7's `du`), modification
   time, name (and `-> target` for links). Options combine (`-lh` =
   `-l -h`), as in Chapter 4. `ls` with names as arguments lists only
   those; `ls -d` lists a folder itself. [`fig-ls-long`; self-check]
5. **Creating, copying, moving, and deleting.** *Start hands-on in
   `~/bioinf-computing-ch05/practice`:* `mkdir`, `mkdir p/q` fails (*captured*:
   `cannot create directory 'p/q': No such file or directory`) and
   `mkdir -p p/q` works; `touch`; `cp a b`; `cp -r`; `cp deep deep2`
   without `-r` (*captured*: `-r not specified; omitting directory`);
   `mv` to move and to rename (one command, two jobs); `rmdir` on a
   non-empty folder and `rm` on a folder (*captured*: `Directory not
   empty`, `Is a directory`); `rm -r`. *Then three surprises, run on
   throw-away files:*
   - `cp new old` and `mv new old` overwrite `old` **without asking**
     (*captured*). `-i` asks first; `-n` never overwrites (*captured*,
     GNU coreutils 9.11: skips silently).
   - `rm` has **no trash folder** and no undo. `rm -i` asks per file;
     `rm -r` on the wrong folder is the classic disaster.
   - A trailing slash matters for links: recalled from Chapter 3
     (`symlink-is-copy`), with the habit: remove a link with `unlink
     name` or `rm name`, no slash.

   *Then the safe habits* as a key idea: preview the exact arguments
   first with `ls -d -- <the same pattern>`, then run `rm` with the same
   arguments (press Up, change `ls -d` to `rm -i`; §10). `-d` matters:
   plain `ls run*` shows what is *inside* the folders, while `rm -r run*`
   removes the folders themselves; `ls -d -- run*` lists `run1` and
   `run2`, the things `rm` would get (*captured*). `--` ends the
   options, so a file whose name starts with `-` is not read as an
   option; quotes keep a name as one argument but do not stop that
   (`./-name` is another way). The first real deletion is `rm -i --` on
   a throw-away practice file. Never `rm -rf` a path built from a
   variable or a wildcard you have not previewed; keep raw data read-only (Chapter 3:
   `chmod a-w` turned a slip into `Permission denied`); backups
   (Chapter 3) are the only undo. One sentence: some sites snapshot
   home folders (Appendix A); do not count on it. Why the book does not
   suggest `alias rm='rm -i'`: the habit stops protecting you on a
   machine without the alias. [`tbl-file-commands`; pitfall: no undo;
   misconceptions `rm-has-undo`, `cp-mv-warn`; self-check]
6. **Symbolic links, revisited.** Chapter 3 made `data/ref` and the
   `toylink` practice link; this section adds what Chapter 3 left out.
   *Start hands-on:* `ls -l data/ref`, `readlink data/ref`, `readlink
   -f data/ref`, `realpath data/raw/../ref`. Then in the practice tree:
   `share/ref` is a **broken link** (its target does not exist):
   `ls -l` still shows it, `cat` says `No such file or directory`
   (*captured*), and `find . -xtype l` lists it (*captured*; GNU
   `find`). *Then relative vs absolute targets* (table): `ln -s
   ~/bioinf-shared/… data/ref` stores an absolute path, which survives
   moving the link but breaks if the target moves or on another machine;
   `ln -s ../raw/x.fastq.gz y` stores a path relative to **the link's
   folder**, not to where you ran the command: the most common way to
   make a broken link. When to use which: absolute for shared lab data
   and references (as in Chapter 3), relative inside one project that
   moves as a whole. Hard links get one sentence (exist; not used in
   this book). `ln -s target linkname`: target first, as in `cp`.
   [`fig-symlink` (reuse Chapter 3's, or a second panel for relative
   targets); `tbl-link-targets`; pitfall: relative to the link's folder;
   self-check]
7. **Wildcards, quoting, and tab completion.** *Start with a prediction
   round* in `~/bioinf-computing-ch05/share/run1`: readers write down what each
   line prints, then run it: `echo *`, `echo *.fastq.gz`, `echo
   *_R1*`, `echo sample_?_R1.fastq.gz`, `echo *.fq.gz` (no match:
   prints `*.fq.gz` itself); then, one level up in `share`, `echo *`
   and `echo .*` (*captured* outputs for all under *Examples and data*).
   *Then name it:* **bash expands an unquoted pattern before the
   command starts** (globbing); when it matches, the program receives
   a list of names and never sees the `*`. So `echo` is a quick preview
   for names like these, and an unmatched pattern is passed on
   unchanged (bash's default setting; changing it is Chapter 8), which
   explains Chapter 4's `stat data/raw/*.fq.gz: no such file or
   directory` and `ls`'s `cannot access '*.fq.gz'` (*captured*).
   *Argument boundaries:* `echo` joins its arguments with spaces, so
   `plot 1.png` (one argument) and `plot` `1.png` (two) look the same.
   One demonstration shows the real list: `printf '<%s>\n' analysis/*`
   prints `<analysis/counts FINAL.txt>`, `<analysis/plot 1.png>`,
   `<analysis/plot 2.png>`, one argument per line, spaces kept
   (*captured*). That is why `ls *` handles names with spaces fine:
   bash does not split a matched name again. *Programs that match
   patterns themselves:* in `find . -name '*.fastq.gz'` the quotes stop
   bash, and `find` receives the `*` on purpose and does its own
   matching. Shown side by side with `ls *.fastq.gz`, this sets up §8's
   pitfall. `*` does not match a leading `.`: in `share`, `echo *`
   skips `.old_settings` and `echo .*` shows only `.old_settings`
   (*captured* in bash 5.3; bash before 5.2 also lists `.` and `..`;
   check on WSL/cluster bash).
   Patterns: `*`, `?`, `[12]`; brace expansion `{1,2}` and `{01..03}`
   (*captured*) looks similar but makes names whether or not files
   exist. Patterns match file names, not file contents (that is
   `grep`, Chapter 6), and are not regular expressions (Chapter 6).
   *Quoting:* the space-splitting step from §2, on Chapter 3's
   `"plot 1.png"`: `ls plot 1.png` looks for two files (*captured*).
   Three fixes: double quotes, single quotes, backslash (`plot\ 1.png`,
   what Tab inserts). Double vs single in one line (double still
   expands `$…`, single expands nothing; variables are Chapter 8).
   Quoting turns globbing off (`ls "*.fastq.gz"` looks for a file
   named `*.fastq.gz`), and also `~`: `ls "~/bioinf-computing"` fails
   (*captured*: `cannot access '~/bioinf-computing'`). The path is then
   relative: a folder literally named `~` inside the current folder,
   then `bioinf-computing` inside that (the `/` still separates
   folders). Write `~/"My Data"` or `"$HOME/My Data"`. Curly quotes
   from PDFs are not quotes (Chapter 4's en dash, again). *Tab
   completion:* one Tab completes as far as the name is unique; two
   Tabs list the choices; it completes commands, paths, and (with
   bash-completion, often installed) options. Tab as a typo clue: if it
   will not complete, check the name with `ls`. It is a clue, not
   proof: the prefix may match several names, permissions can get in
   the way, and completion differs between commands. It would have
   flagged Chapter 4's `_l` typo.
   [`fig-glob-expansion` (stepped), `tbl-glob-patterns`, `tbl-quoting`;
   key idea; pitfall: `~` inside quotes; misconception
   `program-sees-wildcard`; self-check]
8. **Finding files with `find`.** *Start hands-on:* `find
   ~/bioinf-computing-ch05/share` (everything, recursively), then `find
   ~/bioinf-computing-ch05/share -name "*.fastq.gz"`, `-type f`, `-type d`,
   `-type l`, `-iname`, `-maxdepth 1`, and combining (`\( -name
   "*.fastq.gz" -o -name "*.fq.gz" \)`, which finds all six read files,
   *captured*). Reference level: `-size +1k` finds only
   `analysis/counts FINAL.txt` (the toy FASTQ files are about 45 bytes
   each, and on a `.gz` `-size` measures the compressed file);
   `-mtime +30` finds `notes.txt` and `.old_settings`, which the setup
   block back-dates to 2025-03-01 (both *captured*). The structure:
   `find <where> <tests> [action]`; tests written next to each other
   must all be true (an implicit AND), `-o` means OR, and `\( … \)`
   groups. The default action is to print. *Then the
   pitfall, which follows from §7:* the pattern after `-name` must be
   quoted. Unquoted, bash expands it first: with two matches in the
   current folder `find . -name *.fastq.gz` fails with `paths must
   precede expression` (*captured*); with exactly one match it runs and
   **silently misses** files in subfolders (*captured*: found
   `./a_1.fastq.gz` and not `./deep/b_1.fastq.gz`), the worse case
   (Chapter 4's `no-error-means-correct`). Uses readers meet soon:
   finding where a pipeline wrote its outputs (Chapter 26); counting
   files with `find … -type f | wc -l` for inode quotas (Chapter 10,
   pipe explained in Chapter 6); finding broken links. `-exec` and
   `-delete` are **actions**, not tests, and are mentioned only as later
   capabilities, with no runnable deletion here: `-delete` depends on
   where it sits in the expression (placed before the tests it deletes
   everything `find` reaches), turns off printing, and changes the order
   of the search (GNU findutils manual). Clean-up in this chapter uses
   `unlink` and `rm -i`. macOS note: GNU
   `find` after Chapter 1's setup (`-printf` and `-xtype` are GNU;
   Chapter 7 for GNU vs BSD). `locate` gets one line (not on most
   clusters, index can be stale). [`tbl-find-tests`; pitfall: quote the
   pattern; self-check]
9. **Looking inside files.** *Start hands-on in `~/bioinf-computing`:*
   `cat data/meta/samples.tsv` (short: fine); `head -n 3` and `tail -n
   3` on `data/raw/checksums.md5` and the newest log (`ls -t logs`);
   `less` on the Chapter 3 log and on `data/ref/README.md`; then `file`
   on a FASTQ `.gz`, a `.tsv`, a folder, and a link (*captured* for
   gzip and ASCII text; rest while drafting). *Then the `less` keys*
   (table): Space/`b` page, `g`/`G` start/end, `/pattern` then `n`/`N`,
   `-S` to chop long lines (useful for wide tables and SAM later),
   `-N` line numbers, `q` quit; the same keys work in `man` (Chapter 4
   forward reference). *Then compressed and binary files:* `cat` on a
   `.fastq.gz` prints binary noise and can garble the terminal (fix:
   `reset`, or close the tab); `file` tells you first; read compressed
   text with `zless`, or `gunzip -c file | head` as in Chapter 1 (pipe
   explained in Chapter 6). Whether plain `less` opens `.gz` files
   depends on the system (`LESSOPEN`/lesspipe on many Linux
   distributions, not on macOS by default): do not rely on it.
   `tail -f` to watch a growing log, stopped with Ctrl-C (used for
   SLURM output in Chapter 10). `wc -l` recalled (Chapter 1).
   `head -c` recalled (Chapter 3's truncated copy). One line: VS Code
   (`code file`) for files you want to edit; `less` to browse a file
   without loading all of it into an editor at the start. Keep the
   claim modest: `head` reads only the start, but `less` may read far
   more when you search or jump to the end (`G`), and paging through a
   decompression pipe is slower than a plain file. [`tbl-viewers`,
   `tbl-less-keys`; pitfall: `cat` on binary; misconception
   `open-to-look` (open a 5 GB file in an editor); self-check]
10. **History and shortcuts.** *Start hands-on:* Up arrow to recall the
    `seqkit stats` command from Chapter 4; `history | tail` (pipe: Ch 6);
    Ctrl-R and type `seqkit` (reverse search; Ctrl-R again for older,
    Enter to run, Right arrow or Esc to edit first); then the editing
    keys on a long recalled line: Ctrl-A/Ctrl-E start/end, Alt-B/Alt-F
    word back/forward, Ctrl-W delete word, Ctrl-U delete to start,
    Ctrl-K to end, Alt-. last argument of the previous command (the
    `ls` → `rm` habit from §5). Ctrl-C cancels the line or stops a
    program (one line; processes, Ctrl-Z, and `kill` are Chapter 7);
    Ctrl-D ends input (and closes a shell at an empty prompt:
    a pitfall on a login node); Ctrl-L clears the screen. `!!` and `!$`
    get one line with a warning (they run without showing you first).
    Where history is kept (`~/.bash_history`), that it is saved when a
    shell exits (so two terminals do not share it at once), and that a
    password typed as a command argument stays in it (never put
    secrets on the command line; Chapter 4's privacy rule). History
    size settings: Chapter 7 (`.bashrc`). macOS: Alt/Option keys need
    "Use Option as Meta key" in Terminal (or iTerm2's equivalent);
    VS Code's terminal may take some shortcuts for itself. [`tbl-shortcuts`;
    tip; self-check]
11. **Summary, exercises, further reading.** Summary as 5 bullets that
    mirror the learning goals; a one-page command table (also a
    candidate for the cheat-sheet appendix); exercises (below);
    annotated further reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode
inside a `::: {#fig-…}` div, colours from theme classes only. Colour
roles (§2): the reader's files and folders `given` (blue); checks
`good` (green); the current working directory shown by an outline or
a "you are here" marker, not by a colour role; `warn` only for
overwrite, delete, and broken-link marks; shell and program text
neutral.

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-shell-steps` | 2 | stepped (4 steps) | What bash does with `ls -lh "my data"/*.fastq.gz` (or a similar line with one quoted part): (1) the line read into words, the quoted part kept as one; (2) the pattern expanded into file names; (3) the quote characters removed; (4) `ls` found and started with the resulting arguments, drawn as separate boxes. One sentence per step; the step-1 label says "read into words", never "word splitting". Reused by §7 as a back-reference. |
| `fig-filesystem-tree` | 3 | static | One tree from `/`: `home/you/` with `bioinf-computing/` (data/raw, data/meta, data/ref ↗, src, results, logs) and `bioinf-computing-ch05/`; `usr/bin/` for programs; a faded cluster branch (`project/`, `scratch/`). One absolute path and one relative path (from `data/raw` to `data/meta`: `../meta`) drawn as routes. Caption: macOS uses `/Users/you`. |
| `fig-cd-steps` | 3 | stepped (6 steps) | The hands-on `cd` sequence on a small tree: the current folder marked with an outline and "you are here", the `pwd` output under each step (`cd data/raw`, `cd ..`, `cd ../..`, `cd -`, `cd`). |
| `fig-ls-long` | 4 | static | One real `ls -lh` line for a FASTQ file and one for the `data/ref` link, with each field labelled (type, permissions → Chapter 7, links count, owner, group, size, time, name, `-> target`). |
| `fig-glob-expansion` | 7 | stepped (4 steps) | `seqkit stats data/raw/*.fastq.gz` expanded into two names before seqkit starts; then `*.fq.gz` with no match passed on unchanged and seqkit's error; then `"*.fastq.gz"` quoted, passed as one literal word (the `find -name` case). |
| `fig-symlink` | 6 | static (reuse) | Chapter 3's `figures/symlink.svg`; add, if needed, a second panel: a relative target resolved from the link's folder, and the same link broken after it is moved. Decide while drafting whether to extend the existing file or make `fig-link-targets`. |

Not used: screenshots, Mermaid, manim.

### Interactive figure (Observable JS, optional)

- None (decided 2026-11-17): §7's `echo` prediction round in the
  terminal does the job. Revisit a glob playground only if §7 still
  feels thin once drafted.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-path-shortcuts` | 3 | Symbol (`/`, `~`, `.`, `..`, `-` with `cd`) · meaning · example · result of `pwd` |
| `tbl-home-by-system` | 3 | System (Linux, WSL, macOS, cluster) · home folder · other places you will work · note |
| `tbl-file-commands` | 5 | Command · does · overwrites or deletes without asking? · safer form · undo? (`mkdir -p`, `touch`, `cp`, `cp -r`, `mv`, `rm`, `rm -r`, `rmdir`, `ln -s`, `unlink`) |
| `tbl-link-targets` | 6 | Target written as · resolved from · survives moving the link? · survives moving the target? · use for |
| `tbl-glob-patterns` | 7 | Pattern · matches · example on the practice tree · notes (`*`, `?`, `[12]`, `[!1]`, `{a,b}` marked as brace expansion, not a match) |
| `tbl-quoting` | 7 | Form (none, `"…"`, `'…'`, `\`) · spaces kept? · `*` expanded? · `~` expanded? · `$…` expanded? |
| `tbl-find-tests` | 8 | Part · meaning · example. Tests: `-name`, `-iname`, `-type f/d/l`, `-xtype l`, `-maxdepth`; reference rows: `-size`, `-mtime`. Operators: implicit AND, `-o`, `\( … \)`. Actions (mentioned only): default print, `-exec`, `-delete` |
| `tbl-viewers` | 9 | Command · best for · whole file read? · works on `.gz`? (`cat`, `less`, `head`, `tail`, `tail -f`, `zless`, `file`, `wc -l`) |
| `tbl-less-keys` | 9 | Key · action (shared with `man`) |
| `tbl-shortcuts` | 10 | Keys · action · macOS note |

### Code (§6)

- `filename="Terminal (laptop)"`, tier 2 (shown, not run at render),
  every step instant. One `filename="Terminal (login node)"` block in
  §3's cluster note (captured on Nova, home folder only), safe on a
  login node since it only lists files.
- Practice commands run in `~/bioinf-computing-ch05` (scratch, like
  `~/bioinf-computing-ch01`, `~/bioinf-computing-ch03`, `~/bioinf-computing-ch04`); the project
  `~/bioinf-computing` is only looked at, never changed, in this
  chapter. Every `rm`, `mv`, and overwrite example acts on files made in
  the same block.
- Prediction rounds (§3, §7) show the command, then the output in a
  collapsed block, so readers predict first.
- Captured outputs in `.console` blocks, labelled with the tool
  versions; GNU messages (`cannot access '…'`) differ from macOS BSD
  ones (`ls: *.fq.gz: No such file or directory`, *captured*): the book
  shows GNU, as everywhere (bash decision). `LC_ALL` and colour: strip
  ANSI codes; say once that `ls` colours names on most systems.
- Annotations (`# <1>`) for new options the first time they appear.
- Bash everywhere; macOS notes only for Option-as-Meta (§10) and
  `less` with `.gz` (§9).

### Plots

None.

### Animation (manim)

None: the stepped SVGs cover every process in this chapter.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | Before any program starts, bash reads your line into words (respecting quotes), expands `~`, wildcards, and `$…` where quoting allows, and removes the quotes; the program gets the resulting arguments. Most surprises in this chapter come from that step |
| 3 | Tip | Press Tab: it completes names, lists choices, and catches typos |
| 3 | Misconception | "A relative path is relative to the script or file" (`relative-to-script`) |
| 5 | Pitfall | `rm` has no trash and no undo; `cp` and `mv` overwrite silently. Preview with `ls -d -- <same names>` first |
| 5 | Misconception | "Deleted files go to a trash folder" (`rm-has-undo`) |
| 6 | Pitfall | A relative link target is read from the link's folder, not from where you ran `ln -s` |
| 7 | Key idea | Bash expands an unquoted wildcard; the program sees the matching names, each as one argument. No match means the pattern is passed on as is. Quote a pattern when the program should match it itself (`find -name`) |
| 7 | Pitfall | `~` and wildcards are not expanded inside quotes: `"~/data"` means a folder literally named `~`, then `data` inside it |
| 8 | Pitfall | Quote the pattern after `find -name`; unquoted, it can fail or silently miss files |
| 9 | Pitfall | Do not `cat` a compressed or binary file; check with `file`, read with `zless` or `gunzip -c … \| head` |
| 10 | Tip | Ctrl-R searches your history; Alt-. inserts the last argument |

`cp-mv-warn`, `program-sees-wildcard`, and `open-to-look` are handled
in the text, tables, and self-checks, to stay under three callouts per
screen.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2: Why can't `cd` be a separate program like `ls`? (*A program runs
  as its own process; changing its folder would not change your shell's.
  `type cd` says builtin.*)
- §3: You are in `~/bioinf-computing/data/raw`. Give a relative and an
  absolute path to `data/meta/samples.tsv`. (*`../meta/samples.tsv`;
  `~/bioinf-computing/data/meta/samples.tsv`, or `/home/you/…`.*)
- §4: `ls` shows nothing in a folder, but `du` says it holds 2 GB. What
  do you try? (*`ls -a`: hidden files or folders, like `.pixi`.*)
- §5: You run `mv results_new.tsv results.tsv` and `results.tsv`
  already existed. What happened to the old one? (*Gone, replaced
  without a question. `mv -i` or `-n` would have stopped it; only a
  backup brings it back.*)
- §6: In `~/proj/data/` you run `ln -s raw/x.fq.gz ~/proj/results/x.fq.gz`.
  Does the link work? (*No: the target `raw/x.fq.gz` is read from
  `~/proj/results/`, where there is no `raw/`. Use `../data/raw/x.fq.gz`
  or an absolute path.*)
- §7: In a folder with no `.bam` files you run `ls *.bam`. What does `ls`
  receive, and what does it print? (*The literal word `*.bam`;
  `ls: cannot access '*.bam': No such file or directory`.*)
- §8: Why is `find . -name *.fastq.gz` wrong even when it seems to
  work? (*Bash may expand the pattern first; with one match in the
  current folder, find looks only for that exact name and misses the
  rest, without an error.*)
- §9: A colleague's 4 GB `counts.tsv` freezes their editor. How do you
  look at the first rows and the column names? (*`head -n 5`, which
  reads only the start; or browse with `less -S`, which does not load
  the whole file at the start.*)
- §10: Name two ways to rerun the `seqkit stats` command from yesterday
  without retyping it. (*Up arrow until it appears; Ctrl-R `seqkit`;
  `history` then copy.*)

End-of-chapter exercises (core chapter, so required; all on supplied
material, or on the reader's own project for looking only, apart from
notes in `NOTEBOOK.md`):

1. **Where am I?** Starting from `~`, reach `~/bioinf-computing/data/raw`
   twice: once with one absolute path, once with relative steps. From
   there, without `cd`, list `data/meta` and the reference folder
   through `data/ref` with relative paths. Record each command in
   `NOTEBOOK.md`. (*Answer key: `ls ../meta`, `ls ../ref/`.*)
2. **Predict the wildcard.** For six supplied patterns in
   `~/bioinf-computing-ch05/share` (including `*/*_R1*`, `run?/*`, `*.f*q.gz`,
   one that matches nothing, and one hidden-file case), write down what
   `echo` prints, then check. (*Answer key with the captured output.*)
3. **Tidy a lab share (the check).** From `~/bioinf-computing-ch05/share`: use
   `find` to list every read file, under both `.fastq.gz` and `.fq.gz`
   and inside the folder with a space in its name; make
   `~/bioinf-computing-ch05/tidy/fastq/` and link each file there with an
   absolute target, renaming `.fq.gz` to `.fastq.gz`. The exercise
   gives the first link complete (`ln -s
   ~/bioinf-computing-ch05/share/run1/sample_A_R1.fastq.gz .` from
   inside `tidy/fastq`) and one renamed one (`ln -s
   ~/bioinf-computing-ch05/share/"Run 3 final"/sample_C_R1.fq.gz
   sample_C_R1.fastq.gz`); readers adapt them for the other four.
   Then remove the broken link `share/ref` (with `unlink`, no slash),
   and delete the leftover `.tmp` file: preview with `ls -d --
   run2/*.tmp`, then `rm -i -- run2/*.tmp`. Run the four check commands.
   (*Expected output in the check, captured from this answer key; the
   key also shows the most common mistake: a relative target that
   breaks.*)
4. **Read a log without opening it.** In `~/bioinf-computing/logs`, list
   the logs newest first with `ls -t`. Pick the newest log from a run
   that **finished**: Chapter 4 made a deliberately failed run, which
   may be the newest and has no `finished:` line, so check with
   `tail -n 3` and move to the next one if needed. Show its first 3 and
   last 3 lines with `head` and `tail`, and use `less` with `/finished`
   to jump to the end line. Which seqkit version did the run use?
   (*From the log's `seqkit:` line; the answer gives a captured log as a
   fallback for readers without one.*)
5. **Peek into compressed data.** Run `file` on
   `data/raw/SRR6357070_1.fastq.gz` and `data/ref/genes.gtf.gz`, then
   look at the first read with `zless` and at the first two GTF lines
   with `gunzip -c … | head -n 2`. Note in `NOTEBOOK.md` which chromosome
   the GTF starts on. (*Answer: chromosome I only, the test reference;
   formats themselves are Chapters 15 and 17.*)
6. **History drill.** Using only Ctrl-R and the editing keys, recall
   Exercise 4's `head` command and change it to `tail` without retyping
   the path. (*Self-assessed.*)

## Examples and data

- **Practice tree** `~/bioinf-computing-ch05/share/` (built by §1's paste block;
  no download; decided 2026-11-17): a former lab member's folder,
  **designed for Chapters 5–8**, which reuse it rather than each
  building their own.

  ```
  share/
  ├── .old_settings                  (hidden; dated 2025-03-01)
  ├── notes.txt                      (dated 2025-03-01)
  ├── run1/   sample_A_R1.fastq.gz  sample_A_R2.fastq.gz          (2 reads each)
  ├── run2/   sample_B_R1.fastq.gz  sample_B_R2.fastq.gz          (3 reads each)
  │           sample_B_R1.fastq.gz.tmp
  ├── Run 3 final/   sample_C_R1.fq.gz  sample_C_R2.fq.gz         (4 reads each)
  ├── analysis/   plot 1.png  plot 2.png  counts FINAL.txt        (seq 1 1000, 3.9 kB)
  ├── meta/   samples.tsv  samples_from_excel.csv
  └── ref -> /no/such/genome         (broken link)
  ../where.sh                        (pwd; ls data/raw — for §3)
  ```

  **Setup block** (tested end to end 2026-11-17 in an empty home
  folder, bash 5.3.15, GNU coreutils 9.11, findutils 4.11.0; GNU
  `touch -d` is needed, which macOS has after Chapter 1's setup):

  ```bash
  mkdir -p ~/bioinf-computing-ch05
  mkdir ~/bioinf-computing-ch05/share && cd ~/bioinf-computing-ch05/share && {
  mkdir run1 run2 "Run 3 final" analysis meta
  printf '@A.%s\nACGTACGTAC\n+\nIIIIIIIIII\n' 1 2 | gzip > run1/sample_A_R1.fastq.gz
  printf '@A.%s\nGTACGTACGT\n+\nIIIIIIIIII\n' 1 2 | gzip > run1/sample_A_R2.fastq.gz
  printf '@B.%s\nACGTACGTAC\n+\nIIIIIIIIII\n' 1 2 3 | gzip > run2/sample_B_R1.fastq.gz
  printf '@B.%s\nGTACGTACGT\n+\nIIIIIIIIII\n' 1 2 3 | gzip > run2/sample_B_R2.fastq.gz
  cp run2/sample_B_R1.fastq.gz run2/sample_B_R1.fastq.gz.tmp
  printf '@C.%s\nACGTACGTAC\n+\nIIIIIIIIII\n' 1 2 3 4 | gzip > "Run 3 final/sample_C_R1.fq.gz"
  printf '@C.%s\nGTACGTACGT\n+\nIIIIIIIIII\n' 1 2 3 4 | gzip > "Run 3 final/sample_C_R2.fq.gz"
  touch "analysis/plot 1.png" "analysis/plot 2.png"
  seq 1 1000 > "analysis/counts FINAL.txt"
  rows=(sample run_folder condition reads
    sample_C "Run 3 final" treated 12
    sample_A run1 control 9
    sample_B run2 control 30
    sample_E run5 treated 105
    sample_B run2 control 30
    sample_D run4 control 8)
  printf '%s\t%s\t%s\t%s\n' "${rows[@]}" > meta/samples.tsv
  printf '%s,%s,%s,%s\r\n' "${rows[@]}" > meta/samples_from_excel.csv
  printf 'Reads from runs 1-3. Ask Sam about run 3.\n' > notes.txt
  printf 'colour=on\n' > .old_settings
  touch -d 2025-03-01 notes.txt .old_settings
  ln -s /no/such/genome ref
  printf 'pwd\nls data/raw\n' > ../where.sh
  cd ~/bioinf-computing-ch05 && ls -A share
  }
  ```

  If `share` already exists, the second `mkdir` fails with `File
  exists` and nothing inside `{ … }` runs (*captured*), so a second
  paste cannot restore the `.tmp` file or the broken link a reader
  removed in exercise 3, and cannot overwrite changes. Rebuild on
  purpose by renaming the old folder first (§1).

  - Read files are **real tiny gzipped FASTQ** (2, 3, and 4 reads per
    file for samples A, B, C), so `file` and `zless` show real content
    and a Chapter 8 loop over `*_R1*` gets different counts.
  - `meta/samples.tsv`: tab-separated, a header and 6 rows (sample,
    run folder, condition, read count), with one duplicated sample and
    unsorted rows, for `cut`, `sort`, `uniq`, `grep` in Chapter 6.
    **Rows final (2026-11-17); Chapter 6 repeats these exact lines in a
    recreate block, so tell the Chapter 6 plan if they change.** Both
    files come from one list, so they cannot drift apart:

    ```bash
    rows=(sample run_folder condition reads
      sample_C "Run 3 final" treated 12
      sample_A run1 control 9
      sample_B run2 control 30
      sample_E run5 treated 105
      sample_B run2 control 30
      sample_D run4 control 8)
    printf '%s\t%s\t%s\t%s\n' "${rows[@]}" > meta/samples.tsv
    printf '%s,%s,%s,%s\r\n' "${rows[@]}" > meta/samples_from_excel.csv
    ```

    What each row is for (all *captured* with GNU coreutils 9.11):
    header + 6 rows, so `wc -l` gives 7; `sample_B` is on rows 3 and 5,
    **not next to each other**, so `cut -f1 | uniq -c` misses the
    duplicate and `cut -f1 | sort | uniq -c` finds it (`2 sample_B`);
    conditions `4 control`, `2 treated`; `reads` sorts as `105 12 30 30
    8 9` as text and `8 9 12 30 30 105` with `-k4,4n`. `sample_D` and
    `sample_E` have no read files in the tree, a realistic metadata
    mismatch for a later exercise. `Run 3 final` holds spaces inside a
    field: fine with tabs, but it breaks commands that split on spaces
    (awk's default; Chapter 6 should use `-F'\t'`). `reads` are the
    facility's reported counts, not the 2–4 reads in each toy file.
    MD5 of `samples.tsv`: `971d8f742cb76a8d181d3bdc3dcbceaa` (matched
    by the Chapter 6 session); Chapter 6 prints it, and also relies on
    the reads total (194 with the duplicate, 164 without) and on
    `Run 3 final` for its awk splitting example, so any change here
    must be passed on.
    The array syntax is not explained in Chapter 5 (paste-safe; arrays
    are not needed later either).
  - `meta/samples_from_excel.csv`: the same table, **comma-separated**,
    with **CRLF** line endings, for Chapter 7's line endings (`cut -d,
    -f2` gives the run folder). *Captured:* `cat -A` shows `^M$` at each
    line end, but macOS's `file` 5.41 reports only `CSV text`, with no
    CRLF mention: Chapter 5 should not claim `file` reveals CRLF, and
    Chapter 7 should check `file` on Ubuntu/WSL before relying on it
    (`cat -A` is the reliable test).
  - Chapter 5's exercise 3 adds `~/bioinf-computing-ch05/tidy/`; later chapters
    must not depend on whether a reader finished it.
  - The block is 30 lines. Keep it one copyable block, and offer the
    same commands as a downloadable script if it proves error-prone in
    reader testing (see Decisions).
  - *Captured* in the built tree: `ls -A share` → `.old_settings
    analysis meta notes.txt ref Run 3 final run1 run2` (one per line);
    in `run1`: `echo *` and `echo *.fastq.gz` → `sample_A_R1.fastq.gz
    sample_A_R2.fastq.gz`; `echo *_R1*` and `echo sample_?_R1.fastq.gz`
    → `sample_A_R1.fastq.gz`; `echo *.fq.gz` → `*.fq.gz`; in `share`:
    `echo .*` → `.old_settings`; `printf '<%s>\n' analysis/*` → three
    lines, spaces kept; `ls -d -- run*` → `run1 run2`; `find . -size
    +1k` → `./analysis/counts FINAL.txt` (a toy `.fastq.gz` is 43–46
    bytes); `find . -mtime +30` → `./notes.txt`, `./.old_settings`;
    `find . \( -xtype l -o -name '*.tmp' \) -print` → `./ref`,
    `./run2/sample_B_R1.fastq.gz.tmp`; `file` → `gzip compressed data`,
    `CSV text` (no CRLF mention), `ASCII text`, `broken symbolic link to
    /no/such/genome`. Exercise 3's answer key, run against the tree,
    gives the check output shown under *Outcome and check*.
- **Running dataset:** `~/bioinf-computing` from Chapters 2–3, looked at
  only: `data/raw/SRR6357070_{1,2}.fastq.gz`, `checksums.md5`,
  `data/meta/samples.tsv`, `data/ref` (link to the test reference),
  `logs/`. Nothing new downloaded, so no new rows in `data/README.md`.
- **Captured outputs** (2026-11-17, bash 5.3.15, GNU coreutils 9.11,
  findutils 4.11.0, macOS 15 Intel with gnubin first):
  `type cd` → `cd is a shell builtin`; `cd nowhere` → `cd: nowhere: No
  such file or directory` (exit 1); `ls *.fq.gz` with no match →
  `ls: cannot access '*.fq.gz': No such file or directory` (exit 2);
  `ls "~/x"` → `cannot access '~/x'` (exit 2); `ls plot 1.png` → two
  `cannot access` lines (`plot`, `1.png`); `cp y x` and `mv n k`
  overwrite silently; `cp -n` skips silently; `mkdir p/q` → `cannot
  create directory 'p/q': No such file or directory`; `cp dir dir2` →
  `-r not specified; omitting directory 'dir'`; `rmdir` → `failed to
  remove 'sub': Directory not empty`; `rm sub` → `cannot remove 'sub':
  Is a directory`; broken link: `cat` → `No such file or directory`,
  `find . -xtype l` lists it, `readlink` prints the stored target;
  `echo a_{1,2}.fastq.gz`, `echo sample_{01..03}`; `echo .*` →
  `.old_settings` only; `find . -name *.fastq.gz` with two matches →
  `paths must precede expression: 'a_2.fastq.gz'` + `possible unquoted
  pattern after predicate '-name'?` (exit 1); with one match → only
  `./a_1.fastq.gz`, missing `./deep/b_1.fastq.gz` (exit 0); `file` on a
  gzip file → `gzip compressed data`, on a small FASTQ → `ASCII text`.
  For comparison, macOS's BSD `ls` says `ls: *.fq.gz: No such file or
  directory` and Apple's `find` (bfs on this Mac) did not fail on the
  two-match case: a reason the book shows GNU tools only.
- Where commands run: laptop; one login-node capture in §3.

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters); **added 2026-11-17**, once the plan was agreed. Where each is handled
is in brackets.

- `relative-to-script`: "A relative path is relative to the script (or
  file) that contains it." It is relative to the current working
  directory of the shell that runs the command. Probe: from `~` you run
  `bash ~/bioinf-computing-ch05/where.sh`, which contains `ls
  data/raw`; which folder does `ls` look in? (`~/data/raw`, which does
  not exist: *captured*, `ls: cannot access 'data/raw'`.) [callout, §3;
  `where.sh` demonstration]
- `rm-has-undo`: "Deleted files go to a trash folder I can restore
  from." `rm` removes the name at once; there is no trash on the command
  line, and only backups or site snapshots can bring files back. Probe:
  you `rm` a results file by mistake on a cluster; where do you look?
  (Not in a trash folder; ask whether your site keeps snapshots of that
  storage, Appendix A, or rerun from raw data.) [callout, §5]
- `cp-mv-warn`: "`cp` and `mv` warn me before overwriting a file."
  They overwrite silently unless given `-i` or `-n`. Probe: what does
  `mv new.tsv old.tsv` do if `old.tsv` exists? (Replaces it without a
  question.) [text and `tbl-file-commands`, §5; self-check]
- `program-sees-wildcard`: "The program reads the `*` and finds the
  matching files itself." For an unquoted pattern, bash expands it
  first; the program gets names, or the unchanged pattern when nothing
  matches. Only a quoted pattern reaches the program, which some
  programs (`find -name`) want. Probe: why
  did seqkit's error in Chapter 4 contain a literal `*`? (Nothing
  matched, so bash passed `*.fq.gz` on unchanged.) [`fig-glob-expansion`,
  key idea, §7; self-check]
- `open-to-look`: "To see what is in a file I open it in an editor."
  Large files freeze editors and compressed ones show noise; `head`,
  `less`, and `file` look without loading the whole file. Probe: how do
  you see the first read of a 10 GB `.fastq.gz`? (`gunzip -c … | head
  -n 4`, or `zless`.) [text, §9; self-check]
- Existing `symlink-is-copy` (already lists `05-shell-basics`): §5 and §6
  recall it; no change to its entry.

## Links to other chapters and books

- Builds on: Chapters 1–4 (see *What this chapter builds on*).
- Leads to: Chapter 6 (pipes and redirection, `>` overwriting, `grep`
  vs wildcards, regular expressions vs globs, `zcat`); Chapter 7
  (permission column of `ls -l`, `PATH` and `type`/`which`, `.bashrc`
  history settings, `du`, GNU vs BSD); Chapter 8 (variables inside
  double quotes, `rm -rf "$dir"` safety, loops over `*.fastq.gz`, the
  nullglob question); Chapter 9 (paths on a remote machine, `tmux`);
  Chapter 10 (home vs project vs scratch, inode counts with `find`,
  `tail -f` on SLURM output); Chapters 15–17 (looking inside FASTQ, SAM
  with `less -S`, GTF); Chapter 21 (git as the undo `rm` lacks, for
  code); Chapter 26 (finding outputs in `results/` and `work/`);
  Appendix A (site storage paths, snapshots); cheat-sheet candidate
  appendix.

## Official links to include

- GNU Bash Reference Manual: *Shell Expansions*, *Filename Expansion*,
  *Quoting*, *Bash History Facilities*, *Readline* (gnu.org/software/bash/manual)
- GNU Coreutils manual: `ls`, `cp`, `mv`, `rm`, `ln`, `mkdir`,
  `readlink`/`realpath`, `head`, `tail` (gnu.org/software/coreutils/manual)
- GNU findutils manual (gnu.org/software/findutils/manual)
- GNU less (greenwoodsoftware.com/less, the official less site)
- `file(1)` (darwinsys.com/file, the official site), or the man7.org page
- Filesystem Hierarchy Standard (refspecs.linuxfoundation.org/fhs.shtml),
  one link for the tree's top-level folders
- Software Carpentry, *The Unix Shell* (swcarpentry.github.io/shell-novice)
- SCINet and ISU storage pages, via Appendix A

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Verify with scite
where a DOI exists and fetch BibTeX before adding.

- Shotts, *The Linux Command Line* (2nd ed., No Starch, 2019; free
  online edition at linuxcommand.org): chapters on navigation,
  exploring the system, manipulating files, and "Seeing the world as
  the shell sees it" (expansion and quoting) match §3–§7 almost one to
  one. Recurring anchor.
- Software Carpentry, *The Unix Shell*: episodes *Navigating Files and
  Directories*, *Working with Files and Directories*, *Finding Things*;
  CC BY, with exercises. Recurring anchor.
- GNU Bash Reference Manual, §3.5 *Shell Expansions*: the exact order of
  expansions, for readers who want the rule behind §2 and §7.
- Candidate paper: Perkel 2021, "Five reasons why researchers should
  learn to love the command line", *Nature* (news feature,
  doi:10.1038/d41586-021-00263-0; verify with scite and check access):
  motivation, not instruction; keep only if open to read.

## Austin's notes

-

## Decisions (2026-11-17, open questions round)

Austin's choices:

- **Wildcards: `echo` prediction round only.** No Observable JS glob
  playground for now; revisit only if §7 feels thin once drafted.
- **Practice tree: paste block with real tiny gzipped FASTQ.** No
  download for now. If the longer block proves error-prone in testing,
  the fallback is a `make_share.sh` at a stable URL (like `setup-url`).
- **The tree serves Chapters 5–8.** Designed now with a TSV for Chapter
  6 and a CRLF file for Chapter 7 (see *Examples and data*). The
  Chapter 6–8 plans should start from it; tell the Chapter 7 planning
  session about the CRLF file.
- **Cluster capture: Nova, home folder only.** Project and scratch
  paths stay in Chapter 10 and Appendix A.
- **Scratch folders renamed `~/bioinf-computing-chNN`** (was
  `~/bioinf-chNN`), so they cannot clash with another book's scratch
  folders. Applied the same day to Chapters 1–4 (chapters and plans)
  and the Chapter 5–7 plans; dated review files left as they were.
  Recorded in the book's `CLAUDE.md`.

## Review responses (2026-11-17)

Codex (`chapter_05_codex_review.md`). Each testable point was rechecked
here first, by building the practice tree from a real setup block and
running exercise 3's answer key against it (bash 5.3.15, GNU coreutils
9.11, findutils 4.11.0). All six corrections accepted:

1. **Shell steps:** §2, `fig-shell-steps`, and the key idea now say
   "read into words respecting quotes → expand → remove quotes →
   arguments"; "word splitting" kept for Chapter 8. Added the
   `printf '<%s>\n' analysis/*` demonstration (*captured*: names with
   spaces stay one argument). Quoted-tilde callout corrected (`~` is a
   folder named `~`, then the rest of the path).
2. **Deletion preview:** `ls -d -- <pattern>` before `rm`, `rm -i --`
   for the first deletion, `--` and `./name` explained once (*captured*:
   `ls -d -- run*` vs `ls run*`). `echo` is now "a quick preview for
   these names", not "safe for any pattern".
3. **Chapter check:** four commands, including the source-tree check
   for the broken link and `.tmp` file and a check for ordinary files
   in `tidy/`; the six mappings are listed exactly, with the home
   prefix explained. Pipes in supplied commands are now described
   honestly in the scope paragraph.
4. **Practice tree:** a full setup block, tested end to end; the
   hidden-file example moved to `share`; `-size` and `-mtime` given
   files that really match (`counts FINAL.txt` from `seq`, two files
   back-dated with `touch -d`); the "explains every command" promise
   corrected; pasting twice is safe and a rebuild means renaming the
   old folder. The folder-name question is closed: keep
   `~/bioinf-computing-ch05/share/`.
5. **`find -delete`:** now mentioned only, with why it is risky;
   "tests are ANDed" corrected to implicit AND, `-o`, grouping, and
   actions.
6. **Working-directory probe:** replaced pixi (which fails before the
   path matters) with the scratch script `where.sh` (*captured*).

Teaching suggestions also adopted: a minimum path through the chapter;
`find -name` with a quoted pattern beside `ls *` in §7; modest claims
for `less` and for Tab (with `cd ~/bioi` now teaching the second Tab);
exercise 4 picks a finished Chapter 3 log; `NOTEBOOK.md` named as the
one thing written in the project; current-folder marking by outline,
not the `good` colour.

Not adopted: nothing.

## Drafting notes (2026-11-17)

Final review of the plan before drafting found two stale details (the
captured `echo .*` output still said `.hidden`; §2's `type ls`, which
prints an alias on Ubuntu and many clusters). While drafting, every
output was recaptured against a stand-in project built from the real
test data (pinned commit, checksums matching Chapter 3) and the setup
block, with bash 5.3.15, GNU coreutils 9.11, findutils 4.11.0, and an
en_US.UTF-8 locale; owner, group, home path, and folder sizes are shown
as on Linux (`you you`, `/home/you`, `4096`). Changes from the plan:

- **§2:** `type mkdir` instead of `type ls` (aliases are Chapter 7); a
  note that `type ls` may say "aliased".
- **§4 and setup output:** GNU `ls` in a terminal quotes names with
  spaces (`'Run 3 final'`); the text explains the quotes. `ls -l` of
  whole folders replaced by `ls -lh data/raw`, `ls -ld`, `ls -lt logs`.
- **§6:** the relative-target demonstration uses `file` (`broken
  symbolic link to …`) rather than `gunzip`, whose macOS message
  differs. New figure `fig-link-targets` (`figures/link-targets.svg`)
  rather than extending Chapter 3's `symlink.svg`.
- **§9:** `file` on a link says `symbolic link to …` on Linux; macOS's
  `file` follows the link (`directory`): noted in the text. `file` is
  shown only on the real FASTQ, not on the toy `.gz` files (macOS's
  `file` 5.41 reported the toy files as `truncated`).
- **§8:** `find` prints in directory order, which differs between
  systems; the text says so. The `-delete` link points to the findutils
  manual's front page (gnu.org was unreachable when checking deeper
  links; recheck).
- **Exercise 2:** `*/*.f*q.gz` replaces `*.f*q.gz` (which matches
  nothing at the top of `share`); answers captured.
- **Exercise 5:** the plan's answer ("chromosome I only") was wrong: the
  test GTF's first line is on `not_in_genome` and the other 599 on `I`.
  The exercise now asks which chromosome each of the first two lines
  names, and uses that as a "look before you trust" lesson.
- **Cluster note (§3):** captured on a Nova login node by Austin
  (2026-11-17): `pwd` and `$HOME` → `/home/<user>`; `type ls` → `ls is
  aliased to `ls --color=auto'`. The reader's `ls` of their cluster home
  is not shown (personal files). Also from Nova: bash 5.1.8 (so `echo
  .*` lists `.` and `..`: noted in §7), GNU coreutils 8.32, findutils
  4.8.0 (`-xtype`, `-printf` available), file 5.39, `/usr/bin/zless`
  present, `LESSOPEN=||/usr/bin/lesspipe.sh %s` (plain `less` opens
  `.gz`: noted in §9), bash-completion active (`complete -F _longopt
  ls`). Checked locally: macOS `less` has no `LESSOPEN` and shows gzip
  bytes.
- **Further reading:** Shotts, Software Carpentry, the Bash manual
  (`ramey2025bash`), and the findutils manual (`gnu2025findutils`), both
  new `@manual` entries with URL and access date (no DOIs). Perkel 2021
  dropped.
- Figures drawn: `shell-steps`, `filesystem-tree`, `cd-steps`,
  `ls-long`, `glob-expansion`, `link-targets` (all in `figures/`).

## Open questions

1. **To check while drafting:** all captures on Ubuntu/WSL bash
   (`echo .*` differs before bash 5.2: WSL Ubuntu 24.04 ships 5.2, so
   likely the same); whether `zless` is present on WSL, the clusters,
   and macOS after Chapter 1 (GNU gzip from Homebrew includes it);
   whether `less` on WSL Ubuntu opens `.gz` via lesspipe; that
   bash-completion completes seqkit options or not (then do not claim
   it).
2. **Still to capture:** GNU
   gzip's toy-file sizes and messages on Linux (the Mac capture used
   Apple's gzip); deeper findutils manual links once gnu.org responds.

**Naming payoff added (2026-11-17, after Austin's read-through).** New
subsection "Why careful names pay off" closes §7, with
`tbl-name-costs`: each naming rule from Chapter 3's `tbl-file-names`
next to what breaking it cost in this chapter (quotes for
`Run 3 final`, `run?` missing it, case-sensitive Tab, special
characters and the `(` syntax error, `-n`, hidden dotfiles). A
paragraph on CamelCase follows: it works but needs memorised capitals,
and `MyData`/`mydata` collide on a Mac (checked: `touch Data.csv
data.csv` leaves one file). It also recommends `_` between words and
`-` within a part, and notes that Python cannot import a hyphenated
file name (checked). Exceptions: archive IDs and the conventional
`README.md`, `LICENSE`, `Makefile`, `NOTEBOOK.md`. The summary bullet
on wildcards gained one sentence. Chapter 3 still owns the rules;
Chapter 5 shows what they save you.

**Part II opener added (2026-11-17, Austin).** A new first section,
"Why the command line" (`sec-shell-basics-why`), sits before "What this
chapter does". Real work runs on Linux machines reached by terminal
(clusters, and cloud servers at companies). `tbl-why-command-line`
gives the five reasons: the tools are command-line programs, it scales,
it leaves a record, it runs unattended, and it works over any
connection. A "Why bash" paragraph follows, then `tbl-part2-roadmap`,
one row per chapter 5–10. The homepage gained a short "Why so much
command line?" paragraph linking to it. Chapter 1's "Why Linux" is
unchanged.
