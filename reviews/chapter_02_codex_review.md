# Chapter 2 — Codex review

Reviewed: 2026-11-16  
Chapter: [Book setup and editors](../chapters/02-book-setup.qmd)  
Revision reviewed: `c3afc65` (`Draft Chapter 2: book setup and editors`)

The chapter renders successfully, and its displayed Python, R, and SeqKit
versions agree with the committed lockfile on all three declared platforms.
I found five medium-priority issues and one low-priority documentation gap.
The findings below describe the current chapter, rather than its earlier plan.
No chapter or setup files were changed as part of this review.

## Findings

### 1. Verify the SSH host key before telling readers to accept it

**Priority: medium.** Location: [chapter source](../chapters/02-book-setup.qmd),
lines 516–520; repeated in the summary at lines 896–897.

The explanation correctly says SSH cannot yet establish the server's identity,
but immediately instructs the reader to type `yes`. It omits the action that
resolves that uncertainty: comparing the displayed fingerprint with one
obtained from the institution's official documentation or support staff.
Accepting an unverified key saves it as trusted; a mistyped host or intercepted
first connection could then receive the reader's password and verification
code. The captured fingerprint in this chapter is an example, not an
independently verified institutional source.

**Suggested correction:** add a short verification step before `yes`, and
qualify the summary accordingly. Tell readers to stop and contact their site's
support if they cannot verify the fingerprint or it differs. The
[OpenSSH manual's host-key verification section](https://man.openbsd.org/ssh.1#VERIFYING_HOST_KEYS)
explains matching a presented fingerprint against a known one.

### 2. An Open OnDemand terminal is not necessarily a compute session

**Priority: medium.** Location: [chapter source](../chapters/02-book-setup.qmd),
lines 263–265.

The installation rule offers “an Open OnDemand terminal” as an example of a
compute session. Both named sites also expose a browser shell on a login/head
node. A beginner selecting that obvious terminal option could install the
environment on the login node while believing they followed the chapter's
rule.

This distinction is explicit in the official documentation:
[SCINet's Shell Access](https://scinet.usda.gov/guides/use/open-ondemand#shell-access)
opens on a login node, and
[Nova OnDemand](https://research.it.iastate.edu/nova-ondemand)
separately describes a head-node shell and obtaining a compute-node shell.

**Suggested correction:** say “the terminal inside the VS Code interactive
app launched below,” and require the `hostname` check before installation.
Explicitly distinguish it from the portal's **Clusters → Shell Access**.
The existing `srun` alternative can remain.

### 3. The environment check succeeds even when R fails

**Priority: medium.** Locations: [setup manifest](../setup/pixi.toml), line 19;
[chapter source](../chapters/02-book-setup.qmd), lines 137–148.

The task is:

```bash
python --version && R --version | head -n 1 && seqkit version
```

The pipeline can hide R's nonzero exit status because `head` succeeds. Python
and SeqKit can therefore succeed while R fails, and the overall check still
returns success. This matters because the chapter presents this task as
confirmation that the environment works.

**Reproduction:** I ran the exact task string using pixi **0.84.2** in an
isolated, dependency-free test workspace. Test executables made Python and
SeqKit return `0`, and R print `R-failed` to standard error and return `42`.
`pixi run check` still returned **0**, printed both other tools' output, and
continued after R failed. This was tested in pixi's task runner, not inferred
solely from Bash behavior. Pixi documents that tasks use `deno_task_shell` in
its [run command reference](https://pixi.prefix.dev/latest/reference/cli/pixi/run/).

**Suggested correction:** remove the truncating pipeline:

```toml
[tasks]
check = "python --version && R --version && seqkit version"
```

Show R's full version output, or capture its output successfully before
shortening it. If retaining a pipeline, explicitly enable and verify failure
propagation in the task runner; setting `pipefail` only in the reader's parent
Bash session is insufficient.

### 4. The Vim walkthrough does not explain how to add a second line

**Priority: medium.** Location: [chapter source](../chapters/02-book-setup.qmd),
lines 795–804; Exercise 3 at lines 955–971 relies on the same skill.

After nano creates `First note.`, Vim opens the existing file. The next
instruction is to press `i` and “type a second line.” With a clean Vim
configuration, `i` inserts before the cursor at the start of the existing
line. Typing text does not create a new line or append below it. The chapter
never teaches the positioning/newline step needed for the exercise's expected
two-line result.

**Reproduction:** using `vim -Nu NONE -i NONE -n -es` on a temporary file,
the key sequence `iSecond line.<Esc>:wq<Enter>` saved:

```text
Second line.First note.
```

**Suggested correction:** after opening the file, press `G`, then `o` to
open a line below the last line and enter Insert mode; type the second line,
then use the existing `Esc`, `:wq`, `Enter` instructions. Alternatively,
teach `G`, `A`, `Enter` before typing if retaining `i` as the only initial
mode demonstration is important. Explain the chosen keys in Exercise 3 too.

### 5. The required Chapter 1 file can legitimately be missing

**Priority: medium.** Locations: [chapter source](../chapters/02-book-setup.qmd),
lines 151–166 and 113–114; [Chapter 1](../chapters/01-orientation.qmd),
lines 402–404.

Chapter 1 explicitly says `~/bioinf-ch01` is a scratch folder that readers
“can delete ... whenever you like.” Chapter 2's first real tool demonstration
then requires `~/bioinf-ch01/SRR6357070_1.fastq.gz`, without a recovery step.
A reader following Chapter 1's cleanup guidance gets a missing-file error
immediately after a successful environment installation.

**Suggested correction:** either retain the Chapter 1 folder explicitly
until Chapter 3, or add a short recovery block before the first SeqKit run:

```bash
mkdir -p ~/bioinf-ch01
curl -fL -o ~/bioinf-ch01/SRR6357070_1.fastq.gz \
  https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
```

The directory creation also matters for Exercise 2's read-2 download if the
whole scratch folder has been deleted.

### 6. Several promised cluster recipes lead to an unwritten appendix

**Priority: low; a publication dependency.** Locations:
[chapter source](../chapters/02-book-setup.qmd), lines 700–701 and 733–737;
[cluster appendix](../appendices/a-cluster-sites.qmd), lines 3–28.

The chapter says the tunnel/compute-node Remote-SSH routes “are recipes” in
the appendix and that the appendix “shows how” to move VS Code's storage.
The appendix currently contains only an under-construction notice and a
planned-topic list. Readers seeking these instructions reach a dead end;
the latter omission affects the chapter's advice about avoiding home quotas.

**Suggested correction:** link directly to the relevant official site
instructions until the appendix is written, or describe these as forthcoming
material. In particular, readers can presently use
[ISU's VS Code guide](https://research.it.iastate.edu/using-vs-code-cluster)
and [SCINet's VS Code guide](https://scinet.usda.gov/guides/ide/vscode).
The worked Open OnDemand route in the chapter itself remains usable.

## Verification performed

- Rendered with `quarto render chapters/02-book-setup.qmd`: successful,
  without reported missing-reference or missing-citation warnings.
- Checked all 24 Bash blocks with `bash -n` after substituting the setup URL
  and documented user-name placeholders: no syntax errors. This checks
  parsing, not whether every command succeeds on every system.
- Verified that all referenced section, figure, and table identifiers exist
  in the book source, and all chapter citation keys exist in `references.bib`.
- Parsed all four included SVGs as XML and checked their inclusion in the
  generated HTML. This was not a browser-based visual/accessibility audit.
- Parsed the manifest and checked the lockfile's Python, R, SeqKit, and nano
  versions for `linux-64`, `osx-64`, and `osx-arm64`. Python `3.12.16`, R
  `4.4.3`, and SeqKit `2.14.0` match the chapter on each platform.
- Downloaded both setup files from the actual URLs in `_variables.yml`:
  both returned HTTP 200 and matched the local files byte for byte.
- Reproduced the R-check and Vim issues in temporary workspaces.
- Consulted the official tool and cluster documentation linked above, and
  the repository's recorded Windows/cluster checks for context.

## Limits and release notes

I did not install the full book environment, log into either cluster, or
repeat the Windows/Apple Silicon GUI setup. Existing measurements in
`plans/chapter_02_checks.md` are useful evidence, but they are not fresh tests
performed during this review. Cluster form defaults and policies should
continue to be checked against each site's documentation.

The setup files intentionally come from `main` while the environment is a
draft. The repository already records the decision to switch to a release
tag later, so this is not counted as a newly discovered bug. Before release,
also reconcile the introduction's promise that all core software is installed
(lines 23–25) with the manifest's explicit draft status and its current four
direct dependencies.
