# Chapter 10 — Codex review

Reviewed: 2026-11-23  
Chapter: [HPC and SLURM](../chapters/10-hpc-slurm.qmd)  
Revision reviewed: clean working tree at `0272367`. Chapter SHA-256:
`0e615c7aa8dd6bb136d22e5d5302eb4738b7a6f7c072fad8efbc5767d5a917ca`.

The chapter renders successfully as part of the book. The original
two-input job, staging example, array selections, and four valid array
tasks work in local checks. I found one high-priority issue, five
medium-priority issues, and one low-priority correction. These findings
concern the written chapter and its current prerequisites, rather than
the earlier plan. Only this Markdown review was added; all runtime
checks and rendering used disposable copies outside the repository.

The chapter follows through on much of the plan review: it distinguishes
hardware from allocations, investigates the effective time limits,
supplies a complete staging script, uses unique run accessions for array
outputs, and captures the different invalid-dependency policies. The
Nova acquire/connect/release walkthrough also closes Chapter 9's
unfinished connection route. Keep those examples and the distinction
between scheduler status, logs, and actual results.

## Findings

### 1. Adding the array inputs breaks the inherited read-count script

**Priority: high.** Locations: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 1810–1879, 2055–2060, and 2294–2315; prerequisite:
[Chapter 8](../chapters/08-shell-scripts.qmd), lines 1782–1797.

Chapter 8 explicitly tells readers to add a result check to
`src/01_count_reads.sh`: its temporary table must have exactly three
lines, a header plus the two original FASTQ files. Chapter 10 then adds
six FASTQs and says the unchanged script will produce eight data rows.
It cannot publish that table: the inherited check rejects its nine
lines. The first-job rerun, Exercise 2 after the data step, and the
suggested `run_all.sh` job therefore fail on valid inputs. A later
`afterok` chain also cannot demonstrate success with that predecessor.

**Reproduction:** I reconstructed Chapter 8's supplied script with both
required additions, the project-folder guard and result-row check. On
the original pair it exited **0** and produced the chapter's MD5,
**`e1d81de77934f7ab7b44bf72b7520b32`**. After adding the six verified
files and their checksums, all eight checksum checks passed, but the
wrapper exited **1**, printing `read_counts: expected a header and 2
rows`. Its temporary table had **nine lines**; the published table
remained the old **three-line** result.

**Suggested correction:** make updating the result check an explicit
part of the data-expansion step. Derive the expected rows from the same
input list passed to SeqKit, rather than changing the constant from 3
to 9:

```bash
fastqs=(data/raw/*.fastq.gz)
seqkit stats --quiet -T "${fastqs[@]}" > results/read_counts.tsv.tmp
[[ $(wc -l < results/read_counts.tsv.tmp) -eq $(( ${#fastqs[@]} + 1 )) ]] ||
  { echo "read_counts: unexpected number of rows" >&2; exit 1; }
```

Keep the existing checksum check and final `mv`. In the disposable
script, this approach accepted both the original pair and the enlarged
eight-file project. Explain the changed script checksum and verify the
post-expansion wrapper and chain again. Removing the result check would
lose the protection Chapter 8 deliberately teaches.

### 2. The array reintroduces the known successful exit on damaged input

**Priority: medium.** Location: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 1907–1913 and 1924–1928.

The array checks that its FASTQ is readable, but publishes SeqKit's
output without checking that it contains a data row. With the installed
SeqKit **2.14.0**, the exact damaged-gzip behavior demonstrated in Chapter
8 still applies: an error can leave a header-only table while the tool
returns 0. Writing through `.tmp` protects against interruption; it does
not establish that the output is complete.

**Reproduction:** after successfully running task 1 on its intact file,
I truncated the copied R1 to 1,000,000 bytes and reran the unchanged
array script. It printed `unexpected EOF`, then `task 1 finished`,
returned **0**, and replaced the previous valid result with a
**one-line** table. The readable-file check passed. This is a local
script result; no scheduler submission was needed.

**Suggested correction:** apply Chapter 8's result-check pattern here
too. Each task processes one input, so require a header plus one data
row before `mv`:

```bash
[[ $(wc -l < "results/stats_${run}.tsv.tmp") -eq 2 ]] || {
  echo "expected one stats row for $run" >&2
  exit 1
}
```

The repaired disposable script exited **1** on the truncated file and
preserved its previous good result. The earlier checksum verification
remains useful; this small addition preserves the chapter's separate
lesson about checking outputs when a tool reports success incorrectly.

### 3. Correcting the deliberate typo still does not produce a working job

**Priority: medium.** Locations: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 1514–1525 and 2324–2327.

Exercise 3 offers fixing the spelling as one way to make a broken job
complete. However, `typo.sbatch` runs
`bash "$project/src/01_count_raeds.sh"` from the sibling scratch folder.
After correcting `raeds` to `reads`, the script still starts outside
the project and stops at Chapter 8's project-folder guard. It also
bypasses `pixi run`, unlike the successful environment route established
by `ok.sbatch`. The absolute script path locates the script but does not
change its working directory or activate its software environment.

**Reproduction:** I changed only the spelling in a disposable copy,
using the reconstructed Chapter 8 script. It exited **1** with
`run from the project folder`, rather than completing. Changing the
call to the following route succeeded after the input-count correction
in finding 1:

```bash
cd "$project"
pixi run bash src/01_count_reads.sh
```

**Suggested correction:** give the deliberate typo job this correct
directory/environment setup from the start, leaving only the filename
misspelled. Readers can then fix one error and see the intended
transition from `FAILED 127:0` to successful execution.

### 4. The first wrapper never connects its CPU request to SeqKit

**Priority: medium.** Locations: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 940–947 and 1224–1246; also
[sbatch anatomy figure](../figures/sbatch-anatomy.svg).

The resource section correctly tells readers to pass the requested CPU
count to the tool, and the array does so. The first job instead wraps
Chapter 8's unchanged `seqkit stats` call, which has no `-j`, and sets
no `SEQKIT_THREADS`. Its one-CPU request therefore does not explicitly
control the tool, despite being the model readers copy for Exercise 2
and the chain wrapper.

The accompanying claim that SeqKit always defaults to four also needs
qualification. Its [version 2.14.0 source](https://github.com/shenwei356/seqkit/blob/v2.14.0/seqkit/cmd/root.go)
sets the default to the smaller of four and the CPUs reported by the
runtime, unless `SEQKIT_THREADS` overrides it. CPU visibility can vary
inside an allocation, as the opening section already explains. I did
not establish that this exact job oversubscribed CPUs on the clusters;
the defect is the missing explicit connection and the unconditional
description of the default.

**Suggested correction:** preserve the Chapter 8 script and set the
supported variable in its wrapper before `pixi run`:

```bash
export SEQKIT_THREADS="${SLURM_CPUS_PER_TASK:-1}"
```

Update the figure and copied wrappers consistently. I confirmed that
the installed 2.14.0 binary's help reports a default of **1** with
`SEQKIT_THREADS=1`. Describe four as the usual capped default, and
explicit settings as the way to make the request and tool agree.

### 5. The required efficiency comparison uses jobs too short to measure

**Priority: medium.** Locations: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 2363–2382; relevant explanation at lines 1301–1318 and 1745–1750.

The chapter explains that its two-second first job is too short for
`seff`'s rounded CPU time to give useful efficiency. Exercise 4 then
uses array tasks whose captures take **zero to one second**, and its
answer asks readers to check that efficiency fell with the larger
request. Both runs may report 0%, or otherwise fluctuate with startup,
accounting resolution, and I/O. Readers can follow every instruction
and fail to see the stated comparison.

Also, the array sets `-j` from `SLURM_CPUS_PER_TASK`: requesting eight
CPUs changes the tool setting to eight as well. It is not the
controlled four-workers-versus-one-worker comparison already captured
in the resource section. A thread setting alone does not establish
actual CPU use or a predictable efficiency change.

**Suggested correction:** use the existing two-minute captures in
`tbl-cpu-efficiency` for the required CPU calculation and comparison.
Keep the tiny array exercise for choosing a conservative memory/time
request and recording observations, but explicitly accept that CPU
efficiency is uninformative at this duration. A longer live comparison
can be optional. Preserve the existing warning that queue wait times
have no guaranteed ordering.

### 6. “The strictest limit wins” is not Slurm's general limit rule

**Priority: medium.** Locations: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 168–169, 217–226, 290–296, and 2191–2193.

The dated captures support the reported Ceres, Atlas, and Nova wall-time
limits. The problem is the broader rule readers are told to apply to
every limit. Slurm uses a precedence hierarchy for many limits, with
exceptions for partition time/node bounds and aggregate group limits.
It does not always take the smallest value found in the association,
job QOS, partition QOS, and partition.

The linked [SchedMD resource-limit documentation](https://slurm.schedmd.com/resource_limits.html#hierarchy)
gives a concrete counterexample: a partition-QOS `MaxJobs=20` overrides
a user-association `MaxJobs=4`, producing a limit of **20**, not 4.
Partition QOS and job QOS are also distinct policy layers;
`scontrol show job`'s `QOS=` does not replace inspecting the partition's
attached QOS.

**Suggested correction:** say “Several policy layers can limit a job;
inspect the partition, association, and applicable QOS settings. Slurm
defines which layer takes precedence.” Explain the measured wall-time
restriction separately and retain the observed rejection examples.
There is no need to teach the full hierarchy here, but the introductory
rule and self-check should not promise a universal minimum operation.

### 7. The fictional site card substitutes filesystem space for quota

**Priority: low.** Location: [chapter source](../chapters/10-hpc-slurm.qmd),
lines 2255–2286.

Exercise 1 asks for the quota command and current use, but its fictional
outputs supply neither. The answer suggests asking the site **or**
using `df -h`. The latter describes filesystem capacity and availability;
it does not supply the user's or project's quota and usage. This weakens
the distinction the storage section is trying to teach.

Likewise, the fictional `short` partition's name and four-hour maximum
do not establish that the site's policy designates it for interactive
work. A time limit alone does not determine permitted workloads.

**Suggested correction:** add a fictional quota capture and a sentence
of site policy identifying the interactive partition, or mark those
fields “not provided; consult site documentation.” Keep `df -h` as a
separate filesystem-space check if it is mentioned.

## Teaching and presentation improvements

- Give beginners an explicit first-sitting route. The first batch job
  starts at line 924, after substantial QOS, storage, module, and SSH
  material. A short route through account/path setup, one successful
  submission, and its three checks would help readers reach the central
  outcome before revisiting the reference sections.
- At lines 478–480, avoid promising that Linux supplies `TMPDIR`.
  The script deliberately rejects an unset value, which is useful, but
  local readers need the small remedy: choose an existing writable
  temporary root, for example `TMPDIR=/tmp bash
  jobs/ch10_staging.sbatch`. The script still creates and removes only
  its own subdirectory.
- Tighten the accounting definition at lines 1737–1740. `MaxRSS` is
  reported on a step row, but the [sacct manual](https://slurm.schedmd.com/sacct.html)
  defines it as the maximum seen for one task in that step, rather than
  a universal total for the whole step. The distinction matters when
  readers later encounter multiple tasks; the present one-task examples
  can stay.
- The backfill introduction at lines 1328–1329 says three jobs are
  running; the figure, caption, and algorithm have two running jobs
  plus one waiting reservation. Change the introductory count to two.

## Verification performed

- Rendered the chapter, then the complete **42-document book**, in a
  disposable copy with the current theme, chapters, figures, variables,
  and bibliography. The full render succeeded without reported missing
  references or citations. Chapter 10's final HTML contains no unresolved
  cross-reference markers. The initial chapter-only render lacked the
  other chapters' generated reference index; the full render resolved
  those warnings.
- Extracted all **45 Bash blocks** and checked them with Bash `-n`.
  No syntax errors after replacing command-template placeholders such
  as `<project>` with ordinary tokens. This does not validate Slurm
  directives or establish runtime success for every block.
- Reused temporary FASTQ fixtures from earlier chapter work only after
  verifying **all eight SHA-256 hashes** against `data/README.md`.
  The six newly shown MD5s also match that registry. No new data was
  downloaded.
- Reconstructed the current Chapter 8 read-count script and both
  required guards. Confirmed the original successful output checksum,
  the post-expansion failure, preservation of the old result, and the
  input-list-based repair for both two and eight files.
- Ran the staging script on the original result with an explicit
  temporary root. It produced a three-line sorted table, copied it
  back, removed its own work folder, and returned **0**.
- Dry-ran array tasks **0–5**: tasks 1–4 selected the stated runs; task
  0 failed on the header's `fastq_1`; task 5 failed on its empty row.
  Ran tasks 1–4 on intact inputs: all returned **0** with one
  **50,000-read** result each. Reproduced the damaged-input publication
  and verified the proposed row guard preserves a good prior output.
- Reproduced the failed spelling-only repair of `typo.sbatch`, and
  checked the corrected project-directory/environment route locally.
- Replayed the project-copy permission pattern with local rsync:
  an initial read-only raw directory and checksum list, followed by
  added files and an updated list, transferred successfully with
  `-av --no-p --no-g`. I found no local transfer-permission defect in
  that recipe.
- Confirmed all **71 distinct referenced section/table/figure labels**
  exist and the **four citation keys** are present. All **five SVGs**
  parse as XML and include accessible titles. Checked their source
  descriptions against the chapter, including the six lifecycle steps.
- Evaluated the backfill start-time algorithm across all **192 integer
  CPU/hour settings** offered by its controls. Its three tabulated
  examples give the stated starts: now, 2 hours, and 13 hours.

## Limits and release notes

Local checks used macOS **15.7.9** on Intel, Bash **5.3.15**, rsync
**3.5.0**, GNU core utilities, and the already installed book-environment
SeqKit **2.14.0**. For script replay, a disposable `pixi` launcher removed
the `run` prefix and invoked the real installed tools through `PATH`.
That checks shell behavior and actual SeqKit results; it does **not**
test Pixi activation, dependency installation, or the cluster's runtime
environment. No existing environment or reader project was changed.

I consulted official SchedMD documentation, pinned SeqKit source, and
SCINet/ISU storage documentation. I did not connect to a cluster, submit
or cancel jobs, allocate memory deliberately, edit SSH configuration,
or independently reproduce QOS enforcement, resource accounting,
private temporary namespaces, GPU availability, or ProxyJump access.
Those dated observations remain the author's captures. No live CPU
efficiency or queue-time comparison was performed.

The book was rendered and figure sources checked, but browser layout,
dark mode, mobile sizing, stepped controls, and Observable execution
were not visually tested. Bibliographic metadata and editorial notices
were not re-audited. The chapter source hash remained unchanged.
