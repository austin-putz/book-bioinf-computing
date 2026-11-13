# ch01_file_sizes.R ---------------------------------------------------------
# Measures the file sizes in Chapter 1 (tbl-data-sizes,
# fig-pipeline-file-sizes) from the yeast nf-core/rnaseq test data.
#
#   Rscript scripts/ch01_file_sizes.R [workdir]
#
# Downloads the sorted BAMs that nf-core stores with its test data (STAR
# output of nf-core/rnaseq) and the test annotation, counts reads per gene
# with featureCounts (Rsubread), runs DESeq2 (WT vs RAP1_UNINDUCED, 2 vs 2),
# and prints the size of every file. Values used in the book, 2026-11-13:
#
#   FASTQ R1 + R2 of WT_REP2 (SRR6357072)  4,315,508 bytes
#   WT_REP2.sorted.bam                     3,277,856 bytes
#   gene_counts.tsv (124 genes x 5)            2,834 bytes
#   deseq2_results.tsv (124 genes)            12,675 bytes
#
# The results table's size depends on how many digits are written; it is a
# size measurement, not an analysis (the test reference is chromosome I
# only). Needs Rsubread and DESeq2 (Bioconductor). Inputs and checksums:
# data/README.md.

args <- commandArgs(trailingOnly = TRUE)
workdir <- if (length(args) > 0) args[1] else tempfile("ch01-sizes-")
dir.create(workdir, showWarnings = FALSE, recursive = TRUE)
setwd(workdir)

base <- "https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq"
paired <- c("WT_REP1", "WT_REP2", "RAP1_IAA_30M_REP1")
single <- c("RAP1_UNINDUCED_REP1", "RAP1_UNINDUCED_REP2")
for (s in c(paired, single)) {
  f <- paste0(s, ".sorted.bam")
  if (!file.exists(f)) download.file(paste0(base, "/testdata/GSE110004/", f), f, mode = "wb")
}
fq <- c("SRR6357072_1.fastq.gz", "SRR6357072_2.fastq.gz")
for (f in c(fq, "genes.gtf")) {
  url <- if (f == "genes.gtf") paste0(base, "/reference/", f) else paste0(base, "/testdata/GSE110004/", f)
  if (!file.exists(f)) download.file(url, f, mode = "wb")
}

# Count read pairs (paired samples) or reads (single-end samples) per gene.
# The test libraries are reverse-stranded (strandSpecific = 2).
count <- function(samples, pe) {
  fc <- Rsubread::featureCounts(
    paste0(samples, ".sorted.bam"),
    annot.ext = "genes.gtf", isGTFAnnotationFile = TRUE,
    isPairedEnd = pe, countReadPairs = pe, strandSpecific = 2,
    nthreads = 4, verbose = FALSE
  )
  m <- fc$counts
  colnames(m) <- samples
  m
}
counts <- cbind(count(paired, TRUE), count(single, FALSE))
write.table(data.frame(gene_id = rownames(counts), counts, check.names = FALSE),
            "gene_counts.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

suppressMessages(library(DESeq2))
keep <- c("WT_REP1", "WT_REP2", "RAP1_UNINDUCED_REP1", "RAP1_UNINDUCED_REP2")
coldata <- data.frame(row.names = keep,
                      cond = factor(c("WT", "WT", "RAP1", "RAP1"), levels = c("WT", "RAP1")))
dds <- DESeqDataSetFromMatrix(counts[, keep], coldata, ~cond)
dds <- suppressMessages(DESeq(dds, quiet = TRUE))
res <- as.data.frame(results(dds))
write.table(data.frame(gene_id = rownames(res), res),
            "deseq2_results.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

files <- c(fq, "WT_REP2.sorted.bam", "gene_counts.tsv", "deseq2_results.tsv")
print(data.frame(file = files, bytes = format(file.size(files), big.mark = ",")))
cat("genes:", nrow(counts), " samples:", ncol(counts), "\n")
cat("work directory:", workdir, "\n")
