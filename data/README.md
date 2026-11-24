# Data used in this book

Every third-party dataset used in the book, with its source, accession,
license, and citation (series rule: `../CLAUDE.md`, "Data"). No human data.
Third-party data keeps its own license; it is not covered by the book's
CC BY-NC-SA or MIT licenses.

## Yeast RNA-seq test set (running dataset)

| Field | Value |
|:------|:------|
| What | *Saccharomyces cerevisiae* RNA-seq test data of nf-core/rnaseq: 5 sample labels (`WT_REP1`, `WT_REP2`, `RAP1_UNINDUCED_REP1`, `RAP1_UNINDUCED_REP2`, `RAP1_IAA_30M_REP1`) over 7 runs in `samplesheet/v3.10/samplesheet_test.csv`, each run sub-sampled to 50,000 reads (pairs, for paired runs; 4 runs used paired-end, 3 single-end). The labels group runs for pipeline testing: ENA lists the 7 runs as 7 biological samples (GSM2879618–24), all paired-end. The book's own files so far: run SRR6357070 (GSM2879618, wild type, biological replicate 1), paired; from Chapter 10, also runs SRR6357071, SRR6357072, and SRR6357076, paired (below). Counts and ENA records checked 2026-11-17 |
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

**Pinned source (from Chapter 3, 2026-11-17).** Readers download every
file from one commit of nf-core/test-datasets,
`9dd6d014f560e182047992834a8d267214fbccd1` (`rnaseq` branch head on
2026-11-09), through `testdata-url` in `_variables.yml`. The two FASTQ
files above and the three files below are byte-identical at that commit
to the versions recorded here (checked 2026-11-17). The size-measuring
files further down are fetched by `scripts/ch01_file_sizes.R` from the
branch, not from this commit.

Files added in Chapter 3 (same source and license):

| File | Path at the commit | Last changed | Size (bytes) | MD5 | SHA-256 |
|:-----|:-------------------|:-------------|-------------:|:----|:--------|
| `samplesheet_test.csv` | `samplesheet/v3.10/` | `0a8d404` (2023-03-24) | 1,335 | `fb28ab0a8cda268b2befd974804b2925` | `beeb7811b14bfa973233616625a9648ba649736d97b2e84af51d619ac89691c4` |
| `genome.fa.gz` | `reference/` | `bae247f` (2020-08-24) | 71,440 | `4222a07bf01b12782245e0ff774459fe` | `dbfd9767961571e91a42022a728d7bcf5022c1078ee361cf475986520e2bc999` |
| `genes.gtf.gz` | `reference/` | `cfc925e` (2023-11-16) | 10,452 | `504334f6741ee771c665ae845429087f` | `72dadd0ce0b719fa71f849f35e6b3c4475f3edc63cf9d3f60eb7911c2a787aaa` |

`genome.fa.gz` holds one sequence, `>I` (yeast chromosome I). Readers save
the sample sheet as `data/meta/samplesheet_upstream.csv` and keep the
reference in a stand-in shared folder linked into the project.

ENA records for the seven runs (Chapter 3, §7 and exercise 3), checked
2026-11-17 with ENA's file-report API: SRR6357070–75 are GSM2879618–23,
wild type biological replicates 1–3 and "Rap1-AID degron no induction"
replicates 1–3; SRR6357076 is GSM2879624, "Rap1-AID degron induction 30
minutes" replicate 1. All `PAIRED`.

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

Files added in Chapter 10 (same source, commit, and license; the job
array's inputs, `data/raw/` in the reader's project). Paired-end runs of
the fixture's samplesheet besides SRR6357070; SRR6357073–75 are
single-end there. Each file has 50,000 reads, and read 1 and read 2
names match. Downloaded from `testdata-url` + `/testdata/GSE110004/`
and checked 2026-11-23:

| File | Run's GEO sample (fixture label) | Size (bytes) | MD5 | SHA-256 |
|:-----|:---------------------------------|-------------:|:----|:--------|
| `SRR6357071_1.fastq.gz` | GSM2879619 (`WT_REP1`) | 2,189,243 | `fd11dc240712f88f1f800656fc59b6ab` | `06951c97884df8975d5419a2f0d03d435b9da722564000536524b01926970c93` |
| `SRR6357071_2.fastq.gz` | GSM2879619 (`WT_REP1`) | 2,183,711 | `3325feca06747fa80e34daed0dc57de4` | `00bbbf100ee90c5f681c3b4814637283732cd06e620171bd48718aa02de3a91d` |
| `SRR6357072_1.fastq.gz` | GSM2879620 (`WT_REP2`) | 2,148,269 | `63534a634de5efa0273fa812932b0ed1` | `6c92efe43dc8145951c4131cd30e3e169f9877f041fcf20c2577eeeb7ec2b6ed` |
| `SRR6357072_2.fastq.gz` | GSM2879620 (`WT_REP2`) | 2,167,239 | `4c7fb08dc831bc372bb6e827182f6ff7` | `4501eb0062d4005cc1a4c836a86c036c15d3c38d685138d02675c5ecef84c0a3` |
| `SRR6357076_1.fastq.gz` | GSM2879624 (`RAP1_IAA_30M_REP1`) | 2,268,588 | `e026fe5743035e52b7b40606b4c05fba` | `1ba6b60cd24c8abf1db57dec5a13b23eeb35beece6193af8ce6f9bac4fd4546f` |
| `SRR6357076_2.fastq.gz` | GSM2879624 (`RAP1_IAA_30M_REP1`) | 2,250,281 | `00377e768cfd005fb8556d17fd2ee239` | `4a04e6de648091eb42d703f67489d87e929544af478ce5e28b0c790f79a82a5d` |

Add a row for each further file when a chapter starts using it.
