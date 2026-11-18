<h1 align="left">Computing for Bioinformatics</h1>

<p align="left"><strong>The first book in the series <em>Bioinformatics: A Worked Approach</em>.</strong></p>

<p align="left">
<a href="https://austin-putz.github.io/book-bioinf-computing/"><img src="https://img.shields.io/badge/read-online-2E6E7E.svg?style=for-the-badge&logo=bookstack&logoColor=white" alt="Read online" /></a>
<a href="https://github.com/austin-putz/book-bioinf-computing/actions/workflows/publish.yml"><img src="https://img.shields.io/github/actions/workflow/status/austin-putz/book-bioinf-computing/publish.yml?branch=main&style=for-the-badge&label=publish&logo=githubactions&logoColor=white" alt="Publish" /></a>
<a href="https://austin-putz.github.io/book-bioinf-computing/"><img src="https://img.shields.io/badge/status-under%20construction-f5a623.svg?style=for-the-badge" alt="Status: under construction" /></a>
<a href="LICENSING.md"><img src="https://img.shields.io/badge/text-CC%20BY--NC--SA%204.0-lightgrey.svg?style=for-the-badge&logo=creativecommons&logoColor=white" alt="Text license: CC BY-NC-SA 4.0" /></a>
<a href="LICENSE-CODE"><img src="https://img.shields.io/badge/code-MIT-yellow.svg?style=for-the-badge" alt="Code license: MIT" /></a>
</p>

<p align="left">
<a href="https://quarto.org"><img src="https://img.shields.io/badge/built%20with-Quarto-39729E.svg?style=for-the-badge&logo=quarto&logoColor=white" alt="Built with Quarto" /></a>
<a href="https://pixi.sh"><img src="https://img.shields.io/badge/environment-pixi-F7D449.svg?style=for-the-badge" alt="Environment: pixi" /></a>
<a href="https://github.com/austin-putz/book-bioinf-computing/discussions"><img src="https://img.shields.io/badge/questions-discussions-6e5494.svg?style=for-the-badge&logo=github&logoColor=white" alt="Questions: GitHub Discussions" /></a>
</p>

**Read the book:** <https://austin-putz.github.io/book-bioinf-computing/>

The Linux command line, HPC and SLURM, R and Python, file formats,
reproducibility, workflows, and a high-level tour of the algorithms behind
common tools.

**Status:** under construction. Chapters 1–5 are drafted; the rest are
placeholders.

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
