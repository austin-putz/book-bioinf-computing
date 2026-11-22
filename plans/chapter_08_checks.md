---
title: "Chapter 8: Hands-on checks for Austin"
subtitle: "What to run with pixi on your Mac, and on Nova and SCINet (Atlas, Ceres)"
date: 2026-11-19
---

These are the checks Chapter 8 (`chapter_08.md`) still needs from
machines I can't reach from here. Much less than for Chapters 5–7: the
Linux behaviour was already captured in an Ubuntu 24.04 container (see
*Done in Docker*). What is left needs **pixi**, the **real clusters**, or
**you** (the environment change).

**How to work.**

- Each part stands alone. Do them in any order; skip what you can't do
  yet.
- Cluster parts run in a throwaway folder, `~/bioinf-computing-checks`
  (the same one as for Chapters 5–7; reuse it). Delete it at the end
  with `rm -r ~/bioinf-computing-checks`.
- Nothing here edits a startup file or your git settings: the git
  checks use a throwaway `HOME`.
- On a cluster, all of this is light enough for a login node: one 2 MB
  download and a few tiny files.
- **Recording:** Block D writes to a file. For the Mac part, paste the
  terminal output into the chat.

**Priority** if time is short:

1. Part 1.1: add ShellCheck to the book environment (needed before the
   environment is tagged).
2. Part 2: `git --version` on each cluster (decides the `git restore`
   fallback, *Open questions* 1 in the plan).
3. Everything else.

---

## Part 1: your Mac, with pixi

### 1.1 Add ShellCheck to the book environment (decision 1)

In the book repo's `setup/` folder:

```bash
cd ~/Claude/book-bioinf-series/book-bioinf-computing/setup
pixi add shellcheck
pixi run shellcheck --version
git diff --stat
```

**Record:** the version line, and that `pixi.toml` and `pixi.lock` both
changed. Commit both together (a `pixi.toml` without its matching lock
breaks `pixi install --locked` for readers, since `setup-url` points at
`main`). Optionally add a comment on the line, as for `nano` and `tree`:
`shellcheck = "*"   # finds bugs in shell scripts (Chapter 8)`.

### 1.2 The project steps through pixi

This is what Chapter 8 readers do, in your own `~/bioinf-computing`. It
adds two files to `src/` and one to `results/`; nothing in `data/` is
touched. (Skip if you have no project from Chapter 3 on this Mac.)

1. Save `src/02_gtf_summary.sh` and `src/run_all.sh` from `chapter_08.md`
   §10 (open each with `code`, paste, save).
2. Update the project's environment so it has ShellCheck (after 1.1:
   copy the new `pixi.toml` and `pixi.lock` into `~/bioinf-computing`,
   then `pixi install --locked`).
3. Run:

```bash
cd ~/bioinf-computing
pixi run bash src/run_all.sh; echo "exit $?"
cat results/gtf_feature_counts.tsv
pixi run shellcheck src/*.sh; echo "shellcheck exit $?"
pixi run bash -c 'echo "$BASH_VERSION"; command -v bash'
```

**Record:** everything. Expected: `01`'s log as in Chapter 3 (script MD5
`76fa8eb6a7b90f212042cfbe6d95cfcc` **only for the original `01`**;
after adding §9's `pixi.toml` guard the script MD5 changes, so record
the new one; output MD5
`e1d81de77934f7ab7b44bf72b7520b32`); `02`'s three log lines (start
with input MD5, `wrote …`, output MD5; plan revised 2026-11-22); a new
`logs/run_all_*.log` holding the whole run; the five
counts (`exon 129`, `transcript 124`, `CDS 118`, `start_codon 115`,
`stop_codon 114`); ShellCheck prints nothing, exit 0. The last line
tells us which bash `pixi run bash` uses (Homebrew's, or one from the
environment).

### 1.3 VS Code ShellCheck extension (wording only)

Install the **ShellCheck** extension (publisher `timonwong`) in VS Code.
Open a new file `~/bioinf-computing-checks/broken.sh`, paste:

```bash
#!/usr/bin/env bash
for f in */*_R1.f*q.gz; do
  gunzip -c $f | wc -l
done
```

**Record:** whether `$f` gets a squiggle, and the hover text (expected:
SC2086). No screenshot needed. Delete the file afterwards.

---

## Part 2: clusters (Nova, then Atlas and Ceres)

About 5 minutes per machine. Log in as usual and paste **Block D** in
one go.

### Block D: paste this; it saves everything to a file

```bash
mkdir -p ~/bioinf-computing-checks/ch08 && cd ~/bioinf-computing-checks/ch08 && {
h() { printf '\n=== %s\n' "$*"; }
h machine
hostname -s; grep PRETTY_NAME /etc/os-release
h versions
echo "bash $BASH_VERSION"
git --version
gzip --version 2>&1 | head -n 1
locale | head -n 2
h "shellcheck installed or as a module?"
command -v shellcheck && shellcheck --version | sed -n 2p
module -t avail shellcheck 2>&1 | head -n 5
h "git restore and init hint (throwaway HOME, your settings untouched)"
rm -rf repo fakehome && mkdir repo fakehome
(
  export HOME=$PWD/fakehome
  cd repo
  git init 2>&1 | head -n 3
  git config user.name test; git config user.email test@example.org
  printf 'a\n' > f.txt; git add f.txt; git commit -q -m one
  printf 'b\n' > f.txt
  git status --short
  git restore f.txt 2>&1; echo "restore status $?"
  cat f.txt
)
h "strict script: gunzip | head on the real file"
[ -f SRR6357070_1.fastq.gz ] || curl -fsSL -o SRR6357070_1.fastq.gz \
  https://raw.githubusercontent.com/nf-core/test-datasets/9dd6d014f560e182047992834a8d267214fbccd1/testdata/GSE110004/SRR6357070_1.fastq.gz
md5sum SRR6357070_1.fastq.gz
for i in 1 2 3; do
  bash -c 'set -euo pipefail; gunzip -c SRR6357070_1.fastq.gz | head -n 1 > /dev/null; echo reached'
  echo "status $?"
done
h "glob order"
mkdir -p g/run1 g/run2 "g/Run 3 final"
touch g/run1/a_R1.fq.gz g/run2/b_R1.fq.gz "g/Run 3 final/c_R1.fq.gz"
(cd g && printf '%s\n' */*_R1.fq.gz)
} 2>&1 | tee ~/bioinf-computing-checks/blockD-$(hostname -s).txt
```

**Record:** keep `blockD-<machine>.txt` and paste it into the chat (or
copy it with `scp`).

What each part settles:

- **`git --version`:** `git restore` needs 2.23 or newer. If a cluster
  is older, `restore status` is not 0 (`git: 'restore' is not a git
  command`), and the chapter adds `git checkout -- file` as a one-line
  fallback.
- **Init hint:** whether that git prints the `hint: Using 'master'…`
  block (2.28 and later do). The chapter sets `init.defaultBranch main`
  first either way.
- **ShellCheck:** whether readers on the cluster have it outside pixi.
  An empty result is fine: pixi provides it after Part 1.1.
- **`gunzip | head`:** expected `status 141` and no `reached`, three
  times, as in the container. A `reached` is recorded as a
  counterexample; §7 already says "in all six captured runs on this
  input and system", not "every time" (revised 2026-11-22).
- **Glob order:** expected `Run 3 final/…` first. A different order on
  a cluster changes only the order of the check's output lines.

---

## Done in Docker while writing this file (no action needed)

Ubuntu 24.04 container, 2026-11-19: bash 5.2.21, GNU gzip 1.12, git
2.43.0, ShellCheck 0.9.0, seqkit 2.14.0 (GitHub release binary), the
book's files from the pinned commit (MD5s match `data/README.md`), run
as an ordinary user. All recorded in `chapter_08.md` as *captured
(Linux)*. Highlights:

- `run_all.sh` end to end: Chapter 3's log reproduced exactly (same
  script and output MD5s); `02` gives Chapter 6's five counts.
- Strict `gunzip -c … | head -n 1` on the real file: status 141, 6 of 6
  runs. On the practice tree's two-read file it passes. §7 now says so.
- Chapter 3's script on a corrupted copy: exit 1, no results. Same
  without `pipefail`: **exit 0** (`tee` wins). With a truncated R2 and
  checksums made after truncation: seqkit `[ERRO]`, exit 0, header-only
  `read_counts.tsv`, despite strict mode.
- Chapter 3's script run from `~`: leaves `~/results` and `~/logs`
  behind, then fails at `cd data/raw`. Supports the guard (decision 4).
- ShellCheck: SC2086 and SC2154 on the §11 script; SC2068 and SC2086 on
  the exercise 1 skeleton; nothing on `01`, `02`, `run_all.sh`, or the
  finished `count_reads.sh`.
- `git init` without `init.defaultBranch`: the 11-line hint.

WSL is not needed for Chapter 8: nothing here depends on how a terminal
starts, and the container covers Ubuntu's tools.

---

## Results table

Fill in, or paste outputs into the chat and I'll fill it in.

| Check | Mac (pixi) | Nova | Atlas | Ceres | Chapter 8 section it changes |
|:------|:----------:|:----:|:-----:|:-----:|:-----------------------------|
| `pixi add shellcheck` done, lock committed | ✓ 0.11.0, `5ee4ad4` (2026-11-22) | — | — | — | §11, setup |
| `run_all.sh` through pixi: exit, counts | ✓ exit 0, five counts, `01` MD5s match (2026-11-22) | — | — | — | §10, check part 2 |
| `pixi run shellcheck src/*.sh` clean | ✓ 0.11.0, exit 0 (incl. guarded `01`) | — | — | — | §11 |
| bash used by `pixi run bash` | Homebrew 5.3.15, `/usr/local/bin/bash` | — | — | — | §11 (bash 3.2 note) |
| Failed rerun of `02` (§10): old result kept, `.tmp` left | ✓ exit 1, MD5 unchanged, partial `.tmp` (2026-11-22) | — | — | — | §8, §10 |
| VS Code extension: SC2086 on hover | ✓ dotted info underline; hover `Double quote to prevent globbing and word splitting. shellcheck(SC2086)` + Quick Fix; no setup prompt (2026-11-22) | — | — | — | §11 |
| `git --version` | — | 2.47.3 | 2.47.3 | 2.52.0 | §12, decision 6 |
| `git restore` works | — | ✓ status 0 | ✓ status 0 | ✓ status 0 | §12 |
| `init` hint shown | — | yes | yes | yes (new wording: "will change to main in Git 3.0") | §12 |
| ShellCheck outside pixi (path or module) | — | none | none | none | §11 |
| Strict `gunzip \| head`: 141 in all three runs | — | ✓ 141 ×3 | ✓ 141 ×3 | ✓ 141 ×3 | §7 |
| Glob order: `Run 3 final` first | — | **no: last** (en_US.UTF-8) | **no: last** (en_US.UTF-8) | **no: last** (en_US.UTF-8) | check part 1 |
| bash version | — | 5.1.8 | 5.1.8 | 5.1.8 | §11 |
