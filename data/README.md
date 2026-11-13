# Data used in this book

Every third-party dataset used in the book, with its source, accession,
license, and citation (series rule: `../CLAUDE.md`, "Data"). No human data.
Third-party data keeps its own license; it is not covered by the book's
CC BY-NC-SA or MIT licenses.

## Yeast RNA-seq test set (running dataset)

| Field | Value |
|:------|:------|
| What | *Saccharomyces cerevisiae* paired-end RNA-seq, wild type vs Rap1 degron, 3 replicates each, sub-sampled to 50,000 read pairs per sample |
| Source | [nf-core/test-datasets](https://github.com/nf-core/test-datasets), branch `rnaseq`, folder `testdata/GSE110004/` |
| Version | Last commit touching `SRR6357070_1.fastq.gz`: `58ec9dc30549f0f28a01fae5971bdb2f1386f185` (2021-04-12); checked 2026-11-13 |
| Accession | GEO [GSE110004](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110004) (reads in SRA, e.g. SRR6357070) |
| License | Sub-sampled files: MIT (license of nf-core/test-datasets). Original reads: public GEO/SRA data under NCBI's data-use policy, which places no restrictions on use; credit the study below |
| Citation | Wu, A. C. K., Patel, H., Chia, M., Moretto, F., Frith, D., Snijders, A. P., & van Werven, F. J. (2018). Repression of divergent noncoding transcription by a sequence-specific transcription factor. *Molecular Cell*, 72(6), 942–954.e7. <https://doi.org/10.1016/j.molcel.2018.10.018> (verified with scite 2026-11-13; no editorial notices) |

Checksums (SHA-256) of the files the book downloads:

| File | Size (bytes) | Reads | SHA-256 |
|:-----|-------------:|------:|:--------|
| `SRR6357070_1.fastq.gz` | 2,239,317 | 50,000 | `3f50541fa9cf2bedc87e7b682ada0fccfdfcd6d27b9bb81f17be230ff140ebe7` |

Add a row for each further file when a chapter starts using it.
