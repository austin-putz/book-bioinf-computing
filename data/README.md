# Data used in this book

Every third-party dataset used in the book, with its source, accession,
license, and citation (series rule: `../CLAUDE.md`, "Data"). No human data.
Third-party data keeps its own license; it is not covered by the book's
CC BY-NC-SA or MIT licenses.

## Yeast RNA-seq test set (running dataset)

| Field | Value |
|:------|:------|
| What | *Saccharomyces cerevisiae* RNA-seq test data of nf-core/rnaseq: 5 samples (`WT_REP1`, `WT_REP2`, `RAP1_UNINDUCED_REP1`, `RAP1_UNINDUCED_REP2`, `RAP1_IAA_30M_REP1`) from 7 runs in `samplesheet/v3.10/samplesheet_test.csv`, each run sub-sampled to 50,000 reads (pairs, for paired runs; 4 runs paired-end, 3 used single-end). The book's own files so far: run SRR6357070 (`WT_REP1`), paired. Counts checked 2026-11-17 |
| Source | [nf-core/test-datasets](https://github.com/nf-core/test-datasets), branch `rnaseq`, folder `testdata/GSE110004/` |
| Version | Last commit touching `SRR6357070_1.fastq.gz`: `58ec9dc30549f0f28a01fae5971bdb2f1386f185` (2021-04-12); checked 2026-11-13 |
| Accession | GEO [GSE110004](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110004) (reads in SRA, e.g. SRR6357070) |
| License | Sub-sampled files: MIT (license of nf-core/test-datasets). Original reads: public GEO/SRA data under NCBI's data-use policy, which places no restrictions on use; credit the study below |
| Citation | Wu, A. C. K., Patel, H., Chia, M., Moretto, F., Frith, D., Snijders, A. P., & van Werven, F. J. (2018). Repression of divergent noncoding transcription by a sequence-specific transcription factor. *Molecular Cell*, 72(6), 942–954.e7. <https://doi.org/10.1016/j.molcel.2018.10.018> (verified with scite 2026-11-13; no editorial notices) |

Checksums of the files the book downloads. SHA-256 is the book's record;
MD5 is what Chapter 3 teaches readers to check with `md5sum -c`
(MD5 values computed 2026-11-17):

| File | Size (bytes) | Reads | MD5 | SHA-256 |
|:-----|-------------:|------:|:----|:--------|
| `SRR6357070_1.fastq.gz` | 2,239,317 | 50,000 | `d19f3c7a8b4016fa641458257b99a1a1` | `3f50541fa9cf2bedc87e7b682ada0fccfdfcd6d27b9bb81f17be230ff140ebe7` |
| `SRR6357070_2.fastq.gz` | 2,232,117 | 50,000 | `d126cc66ed169f69af2c07da0dd73e02` | `8590e1e01e568fba256aa7dced40519604cbb111ee44ab106a3dcb869660aaf4` |

`SRR6357070_2.fastq.gz`: same last commit as R1 (`58ec9dc`, 2021-04-12);
used in Chapter 1, exercise 1. Checked 2026-11-13.

### Files used only to measure sizes (Chapter 1)

Downloaded by `scripts/ch01_file_sizes.R`, not by readers. The BAMs are
nf-core/rnaseq (STAR) output stored with the test data, added in commit
`4963d6b` (2025-09-09); `genes.gtf` is the test annotation (yeast
chromosome I only), last changed in commit `3792314` (2023-11-16). Same
source and license as above. Checked 2026-11-13.

| File | Size (bytes) | SHA-256 |
|:-----|-------------:|:--------|
| `WT_REP1.sorted.bam` | 6,582,836 | `9d17fefdd5e1b4e3af57636941cfe198037d6b26db7756efa285522e8810e25f` |
| `WT_REP2.sorted.bam` | 3,277,856 | `2ca4e9a00b47bc50e3d05f5993457094b8bc1a6f69fa88c6ade9cb0f4b246343` |
| `RAP1_IAA_30M_REP1.sorted.bam` | 3,507,259 | `09ac49a9a5e8c3e1c6d87e1700241e4b0ba026f9bc9374e3e9b081c590c4f359` |
| `RAP1_UNINDUCED_REP1.sorted.bam` | 1,576,089 | `449c373ddcd9d3f538952d6e6e7596be364439e1c64a91a27407d48b8512ff3b` |
| `RAP1_UNINDUCED_REP2.sorted.bam` | 3,017,901 | `ae5ac34d142ed93563b92e800c95538d2a9f33f703dc9f053f5b31c8b49784ec` |
| `genes.gtf` | 204,286 | `8d9e66311d90f14517cdb8683066d4b376547ea7c2153b05b510fb9ba7988835` |

The script also reads `SRR6357072_1.fastq.gz` and `SRR6357072_2.fastq.gz`
(sample WT_REP2) for their sizes: 2,148,269 and 2,167,239 bytes.

Add a row for each further file when a chapter starts using it.
