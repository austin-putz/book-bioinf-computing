# Computing for Bioinformatics

The first book in the series *Bioinformatics: A Worked Approach*: the Linux
command line, HPC and SLURM, R and Python, file formats, reproducibility,
workflows, and a high-level tour of the algorithms behind common tools.

**Status:** under construction. Every chapter is a placeholder.

## Build

Requires [Quarto](https://quarto.org) ≥ 1.7.

```bash
quarto render        # whole book -> _book/
quarto preview       # live preview while editing
```

The shared theme lives in `_extensions/bioinf/`, copied from
`book-bioinf-theme`. Update it with `quarto update austin-putz/book-bioinf-theme`
(or `quarto add ../book-bioinf-theme` from a local checkout).

## License

Text and figures: CC BY-NC-SA 4.0 (`LICENSE`). Code: MIT (`LICENSE-CODE`).
See `LICENSING.md`.
