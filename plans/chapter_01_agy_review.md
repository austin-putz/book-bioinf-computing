---
title: "Review of `chapter_01.md` (Antigravity / Gemini)"
subtitle: "Advisory review of the Chapter 1 plan"
date: 2026-11-13
---

**Reviewed:** [`plans/chapter_01.md`](chapter_01.md)  
**Context:** Checked against [`CLAUDE.md`](../CLAUDE.md), [`plans/PLAN_CHAPTERS.md`](PLAN_CHAPTERS.md), parent [`../CLAUDE.md`](../../CLAUDE.md) and [`../PLAN.md`](../../PLAN.md), and [`STYLE-GUIDE.md`](../../book-bioinf-theme/STYLE-GUIDE.md).

---

## Overall Assessment

`plans/chapter_01.md` is a **very strong opening chapter plan**. It hits the right pedagogical priorities for incoming MS and PhD students in biology/animal science:

1. **Immediate early win (§2–§3):** Readers open a terminal and inspect a real yeast FASTQ file from the book's running dataset (`SRR6357070_1.fastq.gz`) before reading a lecture on hardware or operating systems.
2. **"Examples first, then formalize":** Every concept section (§4 hardware, §5 data sizes) starts with a measurement or back-of-the-envelope calculation on the reader's own machine/file before naming the general rule.
3. **Tight alignment with the Style Guide:** OS tabsets (`group="os"`), semantic SVG color classes (`given`, `ref`, `muted`), pipe tables, `.check` blocks, and misconceptions mapped to `misconceptions.yml` are all cleanly specified.

Below are targeted suggestions—mostly around **first-hour beginner friction**, **cross-OS command behavior (`zsh` vs `bash`, macOS vs WSL2)**, and **one scientific/technical nuance on file sizes**—that could make the chapter even smoother in practice.

---

## 1. Guided First Session (§3 & Exercise 1): Reduce Syntax Shock on Command #4

In §3, the draft command sequence is:

```bash
mkdir -p ~/bioinf-ch01 && cd ~/bioinf-ch01
curl -LO https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
gunzip -c SRR6357070_1.fastq.gz | head -n 8
echo "SRR6357070_1 reads: $(( $(gunzip -c SRR6357070_1.fastq.gz | wc -l) / 4 ))" > fastq_summary.txt
cat fastq_summary.txt
```

### Suggestions
- **Show `gunzip -c SRR6357070_1.fastq.gz | wc -l` as its own step first.**  
  Right now, the line count (`200000`) is hidden inside nested command substitution and arithmetic expansion (`$(( $(...) / 4 ))`). For a student who opened a terminal five minutes ago, nested `$(( $(...) ))` is the densest bash syntax they will see before Chapter 8. Running `gunzip -c SRR6357070_1.fastq.gz | wc -l` on its own first lets them see `200000` on screen, which directly sets up the §3 self-check (*"A FASTQ file has 200,000 lines. How many reads?"*) and makes dividing by 4 feel obvious rather than magical.
- **Give an explicit hint for appending (`>>`) in Exercise 1.**  
  Exercise 1 asks readers to *"Download the matching read-2 file (`SRR6357070_2.fastq.gz`), count its reads, and append a second line to `fastq_summary.txt`."* Because `>` vs `>>` is not taught until Chapter 6, a reader who copies the §3 command and changes `_1` to `_2` will use `>` and overwrite line 1. Include a brief parenthetical in Exercise 1: *(Hint: use `>>` instead of `>` so you add a second line rather than replacing the first).*

---

## 2. Cross-OS Details in §2 and §4 (`zsh` vs `bash`, macOS, and WSL2)

Because Chapter 1 runs entirely on the reader's laptop across three operating systems, a few small OS differences will show up immediately on screen:

1. **`time` output differs between Linux (`bash`) and macOS (`zsh`) (§4 & Exercise 3):**
   - In §4 and Exercise 3, readers run `time` on the read-count command.
   - On Linux/WSL (`bash`), `time cmd1 | cmd2` prints the familiar 3-line `real` / `user` / `sys` block for the pipeline.
   - On macOS (where the default shell is `zsh`), `time cmd1 | cmd2` prints a single summary line per process (`0.04s user 0.01s system 95% cpu 0.052 total`).
   - Also, on a 2.2 MB file, `gunzip -c ... | wc -l` finishes in **~0.04 seconds** on a modern laptop. That is great for Exercise 3's scaling calculation (0.04 s × 600 ≈ 24 s per file, or ~40 minutes across 48 paired-end samples), but in §4 make sure the `.console` block or annotation tells macOS vs Linux users which number is wall-clock elapsed time (`real` in `bash`, `total` in `zsh`).
2. **Make `tbl-my-computer` RAM and disk outputs easier to read (§4):**
   - On macOS, `sysctl -n hw.memsize` prints raw bytes with no units (e.g., `17179869184`), whereas Linux `free -h` prints human-readable `15Gi`. In the macOS tab, either show how to read it (*"divide by roughly $10^9$ for GB, so `17179869184` is 16 GB"*) or use `sysctl -n hw.memsize | awk '{print $1/1073741824 " GB"}'`.
   - On Windows WSL2, `free -h` reports the **memory limit of the WSL2 virtual machine** (which Windows defaults to **50% of physical RAM**—e.g., `7.7Gi` on a 16 GB laptop), not the laptop's total physical RAM. A one-sentence note in the `Windows (WSL2)` tab will prevent Windows students from thinking half their RAM is missing.
   - On macOS APFS drives, `df -h ~` shows container-level `Size` where `Used + Avail` does not appear to equal `Size`. Tell readers to look specifically at the **`Avail`** column.
3. **`zsh` on macOS in `tbl-terminal-by-os` (§2):**
   - Note in one sentence under `tbl-terminal-by-os` that macOS defaults to `zsh` while Linux/WSL defaults to `bash`, and reassure readers that all interactive commands in this book work in both (and when we write scripts in Chapter 8, we will explicitly run them with `bash`).

---

## 3. Windows (WSL2) First-Time Onboarding Traps (§2 & §3)

For biology grad students on Windows, §2 is the highest-risk drop-off point in the book. Two tiny additions will prevent the most common stalls:

1. **The "invisible password" prompt in WSL2 / Linux:**  
   When Windows users install WSL2 with Ubuntu, it immediately prompts them to create a UNIX username and password—and **prints nothing on screen (no `*` or dots) as they type the password**. Almost every beginner thinks their terminal is frozen. Add a one-sentence note in the `Windows (WSL2)` tab: *"When Ubuntu asks for a password, nothing appears on screen as you type—this is normal security behavior; type your password and press Enter."*
2. **Browser fallback vs. the WSL `/mnt/c` pitfall (§2 & §3):**  
   §3 offers a browser download link as a fallback for `curl`. If a WSL2 user clicks the browser fallback in Windows, the file lands in Windows `Downloads` (`/mnt/c/Users/<name>/Downloads`), right after §2 warned them not to work under `/mnt/c/`. Keep `curl` as the strong default, and note that the browser fallback is only for inspecting or if a network firewall blocks `curl`.

---

## 4. Nuance on "Data Shrinks Down a Pipeline" (§5 & Exercise 2)

In §5, the Key Idea callout states:

> *"Raw reads are the biggest files you will handle; every later step makes the data smaller."*

And `fig-data-shrinks` shows `FASTQ → BAM → count matrix → results table`.

### Suggestion: Group FASTQ and BAM together as "read-level" vs. "summary-level" files
- In practice, a coordinate-sorted **BAM** file contains all the original sequences and base qualities from the FASTQ files *plus* alignment coordinates, CIGAR strings, and tags (and sometimes secondary/supplementary alignments). Because both `.fastq.gz` and `.bam` use `gzip`/`bgzf` compression, **a BAM file is often roughly the same size as—or occasionally slightly larger than—the compressed `.fastq.gz` files it came from**, especially before duplicate marking or if unmapped reads are retained.
- If a student later runs `nf-core/rnaseq` and sees that their `.bam` is slightly larger than their `.fastq.gz`, the statement *"every later step makes the data smaller"* can create confusion.
- **Refinement:** Frame `fig-data-shrinks` and the §5 Key Idea around **two regimes**:
  1. **Read-level files (`.fastq.gz`, `.bam`):** Store every sequencing read (gigabytes per sample; tens to hundreds of GB per study).
  2. **Feature- / variant-level summaries (count matrix, `.vcf.gz`, DE results table):** Collapse millions of reads into one row per gene or variant—shrinking the data by **100× to 10,000×** (megabytes or kilobytes, small enough for a laptop).
- **Exercise 2 follow-up (streaming vs. loading into RAM):**  
  Exercise 2 asks: *"Could your laptop hold one uncompressed 30-million-read FASTQ in RAM?"* (~7.5 GB uncompressed). In the collapsed answer, add one sentence pointing out **why our `gunzip -c ... | wc -l` command didn't need 7.5 GB of RAM**: good command-line tools *stream* through FASTQ files a few lines at a time instead of loading the entire file into memory at once—whereas tasks like indexing a large genome (Chapter 31) really do need 30+ GB of RAM all at once.

---

## 5. Minor Polish & Continuity Checks

- **Labeling where commands run:** `PLAN_CHAPTERS.md` states: *"Where commands run: label every command as laptop, login node, or compute node."* Since §3 and §4 use `filename="Terminal"`, consider using `filename="Terminal (laptop)"` (or establishing that convention in §2) so that when `filename="Terminal (login node)"` and `filename="Terminal (compute node)"` appear in Chapters 2, 9, and 10, the visual cue is already familiar.
- **Clean up or carry forward `~/bioinf-ch01`:** Let readers know at the end of §3 (or §9) that `~/bioinf-ch01` is a scratch folder for this orientation session, and that Chapter 3 will set up the structured project directory they will use for the rest of the book.
- **Open question on BAM/VCF/count-matrix sizes (§Open questions):** For the `SRR6357070` yeast test sample (50,000 paired-end reads), the paired `.fastq.gz` files total ~4.4 MB (`_1` = 2.2 MB, `_2` = 2.2 MB), a coordinate-sorted STAR `.bam` on those 50,000 pairs is ~3–5 MB, and a yeast gene count matrix (6 samples × ~6,600 yeast genes) is ~200–300 KB. Showing that `FASTQ.gz` (~4.4 MB) and `BAM` (~4 MB) sit at the same order of magnitude while the count matrix drops to kilobytes will reinforce the read-level vs. summary-level distinction nicely.
