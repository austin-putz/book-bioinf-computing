---
title: "Review of `chapter_02.md` (Antigravity / Gemini)"
subtitle: "Advisory review of the Chapter 2 plan"
date: 2026-11-13
---

**Reviewed:** [`plans/chapter_02.md`](chapter_02.md)  
**Context:** Checked against [`CLAUDE.md`](../CLAUDE.md), [`plans/PLAN_CHAPTERS.md`](PLAN_CHAPTERS.md), [`plans/chapter_01.md`](chapter_01.md), parent [`../CLAUDE.md`](../../CLAUDE.md) and [`../PLAN.md`](../../PLAN.md), and [`STYLE-GUIDE.md`](../../book-bioinf-theme/STYLE-GUIDE.md).

---

## Overall Assessment

`plans/chapter_02.md` is a **clear, practical, and well-paced setup chapter**. It solves one of the hardest problems in introductory bioinformatics books—getting beginners past environment installation, editor configuration, and remote server access without derailing into system administration:

1. **One setup, used immediately (§2–§3):** Readers install `pixi`, build the book environment, and run `seqkit stats` on the exact yeast FASTQ file (`SRR6357070_1.fastq.gz`) they inspected by hand in Chapter 1. Seeing `num_seqs = 50,000` from a real bioinformatics tool validates their Chapter 1 line-count arithmetic (`200,000 / 4 = 50,000`).
2. **Strong mental models in the visual plan:** The 4-step `fig-pixi-parts` SVG (manifest → lockfile → `.pixi/envs/` → `pixi run`) and `fig-remote-ssh` (reusing Chapter 1's laptop/login-node visual language to show where the VS Code server actually lives) directly target the two biggest beginner misconceptions in this chapter.
3. **Realistic HPC guardrails (§2 & §5):** Calling out `$HOME` quota/inode limits from `.pixi/` and `~/.vscode-server/`, plus login-node restrictions on Remote-SSH with Open OnDemand / compute-node fallbacks, reflects how university and USDA clusters (SCINet Ceres/Atlas, ISU Nova) actually behave.

Below are targeted suggestions on **reproducibility with `pixi.lock`**, **continuity between Chapters 1–3 (`pixi run check` and folder structure)**, **cross-OS friction in VS Code and first-time SSH**, and **responses to the Open Questions**.

---

## 1. Distribute `pixi.lock` Alongside `pixi.toml` (§2 & Exercise 1)

In §2 (lines 62–66 and 274), readers download only `pixi.toml` (where dependencies are wildcarded: `python = "3.12.*"`, `r-base = "4.4.*"`, `seqkit = "*"`) and run `pixi install`.

### Why this matters
- If readers only download `pixi.toml`, `pixi install` solves dependencies from scratch on the day they run it. Over time, readers will get different versions of Python, R, and `seqkit` than what is shown in the book's `.console` blocks (and Exercise 1 asks them to check versions in `pixi.lock`).
- Solving from scratch is also slower and more memory-intensive on a cluster login node than installing from a pre-solved lockfile.
- Most importantly, §2's **Key idea** callout states: *"An environment belongs to a project folder; the lockfile lets anyone rebuild exactly the same one."* Having readers download **both** `pixi.toml` and `pixi.lock` demonstrates that lesson in action rather than just asserting it.

### Suggestions
1. **Have readers download both `pixi.toml` and `pixi.lock` with `curl -fLO`** (keeping `-f` as decided in Chapter 1 so an HTTP error fails loudly instead of writing an error page into `pixi.toml`).
2. **Use `platforms = ["linux-64", "osx-arm64", "osx-64"]` as a build-time verification tool:** Because `pixi lock` solves all listed `platforms` simultaneously into a single multi-platform `pixi.lock`, generating `pixi.lock` in the book repo will automatically verify that every package in the book environment has a valid solve across Linux, Apple Silicon macOS, and Intel macOS before a student ever runs it.

---

## 2. Decouple `pixi run check` from the File Path, or Align with Chapter 3's Layout (§2 & Open Questions)

In the draft `pixi.toml` (lines 257–261), the `check` task is defined as:

```toml
[tasks]
check = """
python --version && R --version | head -n 1 && seqkit version &&
seqkit stats SRR6357070_1.fastq.gz
"""
```

### Potential friction
- In Chapter 3 (*Organizing projects and data*), readers organize their project into subfolders (`data/`, `src/`, `results/`) and move raw FASTQ files out of the root folder into `data/` (or `data/raw/`). As soon as they do that, running `pixi run check` will fail with `file not found: SRR6357070_1.fastq.gz`.
- In addition, Learning Goal 2 states: *"Run a tool from the environment with `pixi run`"* and Exercise 2 asks readers to *"Run `pixi run seqkit stats` on the read-2 file"*. If §2 only runs `pixi run check` (a custom task), readers have not yet seen `pixi run <tool> <arguments>` before Exercise 2 asks them to run it on read 2.

### Suggestion
Split the §2 check into two commands:
1. **`pixi run check`** checks that the environment itself works (`python --version && R --version | head -n 1 && seqkit version`)—so `pixi run check` continues to work in every chapter regardless of where data files live.
2. **`pixi run seqkit stats SRR6357070_1.fastq.gz`** runs `seqkit` on the Chapter 1 FASTQ file. This teaches `pixi run <command>` directly in §2, makes the `num_seqs = 50,000` check explicit, and makes Exercise 2 (changing `_1` to `_2`) a natural one-character adaptation.

---

## 3. Cross-OS Friction in §3 (VS Code) and §4 (First-Time SSH)

### A. VS Code on macOS and Windows WSL2 (§3)
1. **`code .` on macOS requires a one-time step:**  
   Unlike Linux and WSL2 (where `code .` is on `PATH` immediately after installing VS Code), macOS users get `zsh: command not found: code` until they open VS Code, press `Cmd-Shift-P`, and run **Shell Command: Install 'code' command in PATH**. Include this one-line step in the `macOS` tab of §3's OS tabset, and keep `File → Open Folder…` as the universal GUI path.
2. **Where to install VS Code on Windows (WSL2):**  
   After Chapter 1's rule that everything runs inside Ubuntu (WSL2), some Windows students try to install a Linux build of VS Code *inside* Ubuntu. In the `Windows (WSL2)` tab of §3, state explicitly: **install VS Code in Windows as a normal Windows application**, install the **WSL** extension inside it, and then type `code .` from the Ubuntu terminal. Point out the green/colored remote indicator in the bottom-left corner of the status bar (`WSL: Ubuntu`), which also sets up the exact same status-bar check for `SSH: <host>` in §5.
3. **Pointing R and Python extensions at `.pixi/envs/default` (§3):**  
   Keep this part of §3 very lightweight (or mark it as a brief note that returns in Chapters 12–13). In Chapter 2, readers have not written any R or Python code yet; forcing them through interpreter-picker menus for two languages in Chapter 2 adds UI clicks they won't use until Part III. What they use immediately in Chapter 2 is the **VS Code file explorer, editor, and built-in terminal**.

### B. First-time SSH host-key verification prompt (§4)
When a student runs `ssh user@host` to a cluster for the very first time, OpenSSH pauses before asking for a password or MFA:

```text
The authenticity of host 'ceres.scinet.usda.gov (...)' can't be established.
ED25519 key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Beginners routinely get stuck here (or type `y` instead of `yes`, which OpenSSH rejects). Show this prompt in the captured `.console` block in §4 with a code annotation explaining that on first login you type the full word `yes` and press Enter, after which OpenSSH remembers the host in `~/.ssh/known_hosts`.

---

## 4. Style Guide & Self-Check Alignment

1. **Terminal run labels (`STYLE-GUIDE.md` §6):**  
   Line 170 currently says: *"Blocks use `filename="Terminal"` (or `filename="pixi.toml"`, `filename="~/.ssh/config"`)"*. Per the rule added to `STYLE-GUIDE.md` §6 during Chapter 1 (`Never a bare "Terminal"`), use **`filename="Terminal (laptop)"`** in §2, §3, §6 and **`filename="Terminal (login node)"`** (or laptop → login node) in §4–§5. Chapter 2 is where this label pays off most, because readers switch between their laptop and a remote login node for the first time.
2. **Swap or add a self-check for §3 (lines 206–212):**  
   Currently, the self-check listed for **§3** (*"Which file says exactly which version of each package you have: `pixi.toml` or `pixi.lock`?"*) tests **§2** (*Installing pixi and the book environment*), leaving §3 (*VS Code: a home for your work*) without a self-check on VS Code.  
   - Move the `pixi.toml` vs `pixi.lock` check to §2 (or combine it with the §2 check).
   - Add a §3 self-check tied to `fig-vscode-window`, e.g.: *"Where in the VS Code window can you check at a glance whether your editor and terminal are connected to your local machine, WSL, or a remote cluster?"* (*The left end of the status bar at the bottom of the window.*)
3. **One-line safety note on `EDITOR=nano` (§6):**  
   In §6 (line 110), when showing `export EDITOR=nano` so tools like `git commit` open `nano` instead of `vim`, mention in one phrase that setting it in a terminal lasts only for that terminal window (and Chapter 7 will show how to put it in `~/.bashrc` so it sticks).

---

## 5. Recommendations on the Open Questions (§Open Questions)

1. **What goes in the book environment now? (Option A vs. B vs. C):**  
   - **Recommend Option A (with a measured size cap) or an A/C hybrid.** Having one `pixi.toml` + `pixi.lock` that covers the core chapters (Python, R, `seqkit`, `samtools`, `bedtools`, `bcftools`, `fastqc`, `multiqc`, `duckdb`, plus core R/Python table & plotting libraries) honors the promise of *"one environment, installed in Chapter 2, so later chapters never stop for installs."*  
   - Before finalizing the list, measure three numbers on a clean install: **download size** (aim for < 1 GB), **extracted size on disk** (`du -sh .pixi`), and **file/inode count** (`find .pixi | wc -l`, important for HPC `$HOME` inode quotas). If heavy workflow or alignment tools in Parts VI–VII (`nextflow`, `apptainer`, `blast`, `bwa`, `minimap2`, `star`, `salmon`) push the size or `osx-arm64` compatibility too far, keep them in a named pixi feature (`pixi install -e workflows` / `-e align`) introduced when needed.
2. **Book folder (`~/bioinf-book/`) vs. Chapter 1 (`~/bioinf-ch01/`) and Chapter 3 project:**  
   - **Use `~/bioinf-book/` as the single recurring project folder from Chapter 2 onward.** Chapter 1 already tells readers that `~/bioinf-ch01/` is a scratch folder (`chapter_01.md` line 89). In Chapter 2, readers create `~/bioinf-book/`, copy or move `SRR6357070_1.fastq.gz` (and `_2.fastq.gz` from Ch. 1 Exercise 1) into it, and install the `pixi` environment there. Then in Chapter 3, instead of creating a third folder, readers **organize `~/bioinf-book/` itself** into `data/`, `src/`, `results/`, and `logs/`—so `pixi.toml` stays at the project root for the rest of the book.
3. **`pixi` cache and detached-environment settings on HPC:**  
   - The environment variable for the download/package cache is **`PIXI_CACHE_DIR`** (documented at `pixi.sh`; `RATTLER_CACHE_DIR` is also recognized underneath).  
   - To keep `.pixi/envs/` out of a small `$HOME` directory on a cluster, `pixi` supports **`detached-environments`** in `~/.pixi/config.toml` (e.g., `detached-environments = "/project/group_name/user/pixi-envs"` or via `pixi config set detached-environments <path>`). Mentioning `PIXI_CACHE_DIR` in the §2 Pitfall callout and deferring `detached-environments` to Chapter 23 and Appendix A is the right balance for Chapter 2.
