---
title: "Chapter 10 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-22
---

Reviewed [chapter_10.md](chapter_10.md) against the repository and series
instructions, [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared theme style guide, relevant written Chapters 1–3 and 7,
the current Chapter 8–9 plans, and the written
[Appendix A](../appendices/A-cluster-sites.qmd). Locations and line
numbers refer to the plan as reviewed on 2026-11-22. The source plan,
chapter text, appendix, and Austin's notes are unchanged.

**Overall assessment:** keep the chapter's practical direction. A small
successful batch job, three recognizable failure modes, and an array
are appropriate outcomes for the end of Part II. The backfill figure
also has a clear teaching purpose. The main corrections concern a
local check that currently cannot run, inconsistent array metadata and
indexing, the temporary-storage recipe, and stronger claims about
resource measurements and site policy than the evidence supports.

## Corrections before drafting

### 1. Make the first job agree with both checks and its actual log name

**Priority: high. Locations:** outcome/check, lines 112–128;
section 6, lines 266–307; exercise 2, lines 576–578.

Running the supplied script with plain Bash does **not** print the
promised SeqKit table: `set -u` stops at `$SLURM_JOB_ID`, which is unset
outside Slurm. `$SLURM_CPUS_PER_TASK` would fail next. I extracted the
exact script and ran it locally with Slurm variables absent; it exited
1 before reaching Pixi.

Keep the no-cluster route, but make its local defaults explicit:

```bash
job_id=${SLURM_JOB_ID:-local}
threads=${SLURM_CPUS_PER_TASK:-1}
```

Use those variables in the message and thread option. Alternatively,
run the ordinary analysis script locally and reserve the wrapper for
Slurm, explaining that Bash ignores the directives but does not invent
Slurm's runtime environment. A command-local assignment of test values
is another possible demonstration, provided it is labeled as a
simulation rather than an allocation.

There is a separate filename mismatch: `--job-name=count_reads` and
`--output=logs/%x_%j.out` produce `logs/count_reads_<jobid>.out`, whereas
the opening check and `tail -f` look for
`logs/01_count_reads_<jobid>.out`. Choose one name and use it throughout.
Create `jobs/` and `logs/` before submission; a log directory must be
available when Slurm opens the output, before script-body setup can run.

Use the book's decided `#!/usr/bin/env bash` shebang, and include the
single-node/single-task options that section 7 recommends in the actual
first script. Run the preliminary cluster test **inside the interactive
allocation just taught in section 5**, keeping the login-node rule
consistent and avoiding another rule about which small exceptions count.

Exercise 2's date request needs one sentence about evaluation:
`#SBATCH` directives do not evaluate `$(date …)` or shell variables.
Use a shell-expanded `sbatch --output=…` option or create a dated
application log in the body. The official
[`sbatch` documentation](https://slurm.schedmd.com/sbatch.html)
distinguishes directives from shell syntax.

### 2. Fix the array self-check and define one actual task manifest

**Priority: high. Locations:** section 10, lines 371–391;
`fig-job-array`, line 435; self-check, lines 565–567;
examples/data, lines 600–608; open question 3, lines 754–757.

The self-check's answer is reversed. For the expression as written:

```bash
awk -v n="$SLURM_ARRAY_TASK_ID" 'NR == n + 1 {print $1}' meta/samples.tsv
```

task **0 reads the header**, task 1 reads the first data row, and task
4 reads the fourth data row. Thus `--array=1-4` is correct for four
data rows; `--array=0-3` is wrong. I reproduced all those selections.
A task beyond the end also gets an empty value with `awk` exit status
0, so strict mode does not catch that mistake. Add an explicit
nonempty-selection/input-file check before running the tool.

The named input table is inconsistent with the existing project:

| File | Existing purpose and columns |
|:-----|:-----------------------------|
| `data/meta/reads.tsv` | Project table: `sample`, `run`, `fastq_1`, `fastq_2` |
| `data/meta/samples.tsv` | Project metadata: `sample`, `run`, `geo_sample`, `condition`, `replicate` |
| `~/bioinf-computing-ch05/share/meta/samples.tsv` | Practice fixture used in Chapter 8: `sample`, `run_folder`, `condition`, `reads`; deliberately duplicated/missing entries |

There is no existing four-row project `meta/samples.tsv` with
“Chapter 8's columns.” Do not carry the deliberately imperfect practice
table into a real project or infer FASTQ paths from its sample labels.

Use an explicitly supplied task manifest, preferably extending
`data/meta/reads.tsv` or creating a clearly named chapter-specific
table with one row per **run/input** and an explicit path. Select with
`awk -F '\t'` and explain the exact columns. Use run accessions as
unique task/output keys: the upstream fixture reuses sample labels,
as Chapter 3 already explains. Two tasks writing the same result name
would otherwise race.

Supply the complete array script: manifest selection, bounds/input
checks, thread setting, unique result path, and `%A_%a` log pattern.
Then show all four local selections before submission, not only task
3. If the chosen route downloads three more inputs, update both the
provenance registry and `data/raw/checksums.md5`, deliberately restore
the raw-data write protection, and state how the enlarged input glob
changes Chapter 8's `01` output. Those are project changes, not just
new entries in a planning table.

Also change “tasks run at the same time on different nodes” to “tasks
can run independently when resources permit.” They can run serially,
share a node, and finish out of order. Correct “`%2` throttle” beside
the example ending in `%5`. The
[official array guide](https://slurm.schedmd.com/job_array.html)
supports the independent-task model and concurrency limit.

### 3. Separate node-local scratch from assumptions about `$TMPDIR`

**Priority: high. Locations:** section 3, lines 197–220;
section 9, line 365; optional exercise 6, lines 589–591;
storage figure/table, lines 431 and 468.

The sites document temporary local storage and cleanup at job end:
[SCINet scratch guide](https://scinet.usda.gov/guides/use/scratch),
[Nova storage guide](https://research.it.iastate.edu/file-storage#temporary-local-storage-tmpdir).
Keep those attributed site facts. But observing `TMPDIR=/tmp` in an
interactive session alone does not establish whether that path is
job-private, namespaced, or a shared node directory, nor how batch jobs
set it. Capture it **inside a batch job** before prescribing staging
or cleanup there; Atlas is still explicitly unverified.

Supply the promised staging example completely. Have each job/task
create its own subdirectory beneath a verified temporary root, work
there, and copy its own final output back to an absolute project path
only after success. Check that the temporary root is set and writable;
avoid making the example depend silently on a missing variable. Never
teach cleanup of the root `$TMPDIR` itself based only on the observed
value `/tmp`.

Changing directory also affects Pixi discovery and relative inputs.
Locate the project/environment before staging, or explicitly select
its manifest. Likewise, capture output paths before `cd`, so copying
back does not put the results inside the temporary directory again.
A failed or timed-out job cannot be assumed to reach the copy-back
line; distinguish expendable intermediates from files that need to be
preserved during a long run.

Keep disk inspection bounded to the job's own directory. `du -sh
"$TMPDIR"` could otherwise traverse other work if the value names a
shared root. “Fastest” should be a site/workload expectation, not a
universal ranking of every node-local and network filesystem.

The first quota example also points back to `~/bioinf-computing/.pixi`
despite this chapter putting the project in `/work` or `/project`.
Run it from the cluster project as `find .pixi -type f …`, and distinguish
this approximate regular-file count from the site's authoritative
object/inode accounting. Directories, links, and hard links mean those
numbers need not coincide.

### 4. Ensure the failure exercises fail for the intended reason

**Priority: high. Locations:** section 8, lines 331–353;
supplied files, lines 494–499; exercise 3, lines 579–582.

The OOM script is placed in the sibling `bioinf-computing-ch10/`
directory and runs `pixi run python …`. That directory is outside the
project workspace. Unless its script explicitly selects or enters the
project, Pixi fails at manifest discovery before Python allocates
anything. I reproduced this in a manifest-free temporary directory:
Pixi exited 1 with “could not find pixi.toml or pyproject.toml with
tool.pixi.”

Give every failure script an explicit working-directory/environment
recipe. Install the locked environment beforehand in the supported
compute session, so the OOM exercise is not accidentally measuring an
environment solve/install under a 500 MB limit. Demonstrate that a
small successful Python command runs by the same route before
deliberately exceeding the job's memory allocation.

Keep the OOM test small and bounded, but its exact state/message must
remain a site capture: memory enforcement and reporting determine
whether the process is killed, allocation fails in Python, or a
different step is marked. Do not run this deliberate 2 GB allocation
on a laptop as a no-cluster equivalent. Captured logs are the right
local route.

Define the typo precisely too. `bash missing.sh` commonly returns 127,
whereas a failing file-reading command can return 1; “calls a missing
file” does not establish the advertised status. The finished supplied
script and its capture should determine the expected answer.

For all three exercises, read the allocation record, relevant step
record(s), and log together. If future wrappers use `srun`, the failing
application can be in a numbered step rather than `.batch`; the latter
does not universally carry the most informative cause.

### 5. Do not promise a particular efficiency or treat accounting as exact

**Priority: medium. Locations:** opening check, lines 118–122;
sections 7 and 9, lines 309–311 and 355–369;
exercise 4, lines 583–586; optional plot, lines 503–507.

`seqkit stats -j 1` with two allocated CPUs does not imply CPU
efficiency near 50%. This tiny task includes startup and I/O, may
finish very quickly, and need not saturate even one CPU. Keep it as a
successful submission example; use a captured longer workload or a
clearly labeled numerical example for the utilization calculation.
Do not require a reproducible performance difference from the toy
files.

Explain the accounting table before asking readers to right-size from
it: the allocation row and job-step rows describe different things;
`ReqMem` has scope suffixes such as per-node/per-CPU; `MaxRSS` is a
step statistic, not a general sum across every concurrent process in
the allocation. Blank or zero values can reflect unavailable metrics.
Use one annotated capture showing which cells are compared and their
units. [Official `sacct` field documentation](https://slurm.schedmd.com/sacct.html).

Make “peak plus 25%” a starting estimate for a comparable **successful**
run, not a rule for failed/OOM runs or a guarantee that sampled memory
captures every spike. Keep the existing warning about reference size
and nonlinear scaling. The optional plot should not treat a killed
job's recorded RSS as its known full memory requirement.

A smaller resubmission may wait longer simply because the queue changed.
Exercise 4 can ask readers to record wait times, but should not grade
whether the second job started sooner. The controlled backfill figure
is the place to isolate the effect of request size.

Finally, `/usr/bin/time -v` does **not** work everywhere: Apple's
`/usr/bin/time` rejects `-v`, which I reproduced on this Mac. Label it
as GNU/Linux syntax, give a short macOS-specific alternative if needed,
or keep the reference on the cluster route only.

### 6. Correct the thread example and qualify scheduling/fair-share claims

**Priority: medium. Locations:** section 7, lines 313–326;
`tbl-slurm-vocab`, line 466; self-check, lines 557–559;
misconceptions, lines 618–629.

The `cpus-sets-threads` lesson is useful, but SeqKit is a poor example
of an assumed one-thread default. Its documented default is **four**,
and it also accepts `SEQKIT_THREADS`. State the explicit `-j` setting
in the demonstration. If the final wrapper calls Chapter 8's `01`,
that script currently has no `-j` option, so the wrapper's two-CPU
request does not automatically control it. Use an explicit supported
thread setting and verify it with the pinned version.
[SeqKit usage documentation](https://bioinf.shenwei.me/seqkit/usage/).

Use “Slurm CPU” in the vocabulary table, not simply “CPU (core).” A
CPU can correspond to a hardware thread or a core according to site
configuration. The existing one-node, one-task, multiple-CPU pattern
is the right introductory request for these tools; say that
`--ntasks` describes tasks rather than defining it as an MPI-only
option. [Slurm CPU-management guide](https://slurm.schedmd.com/cpu_management.html).

Backfill can let a smaller or shorter eligible job fit an earlier
gap; it does not guarantee “2 hours starts sooner than 3 days.” Keep
the interactive figure and phrase its title/lesson as a possibility.
The chosen official scheduling page is appropriate; no replacement
source is needed. [Backfill documentation](https://slurm.schedmd.com/sched_config.html#backfill-scheduling).

Distinguish requested wall-time limit from elapsed charged use.
Requesting three days and finishing in ten minutes does not universally
charge three days to fair share. Allocated-but-idle CPUs can count
during execution; memory weights and other billing rules are
site-configurable. Revise both the prose and misconception entry rather
than teaching a universal penalty for every requested resource.
[Slurm fair-share and billing explanation](https://slurm.schedmd.com/priority_multifactor.html#fair-share-factor).

### 7. Treat the applicable limits and terminal states as things to establish

**Priority: medium. Locations:** section 2, lines 183–192;
section 8, lines 343–347; section 11, lines 393–399;
self-checks, lines 542–544 and 568–569.

The mismatch between `sinfo`'s partition limit and an older documented
limit is good motivation to investigate QOS, but does not by itself
identify the effective QOS or prove a three-week maximum for this
reader. The chapter's capture list currently requests all QOS rows
without tying them to the user's association, chosen partition, and
actual submitted job.

Capture the applicable association/default and job QOS alongside their
limits. Preserve the observed partition values as dated observations;
mark the limiting-policy explanation as an inference until checked.
Do not make the Ceres 30-day self-check depend on an unverified exact
QOS value/reason. A request can also be rejected during submission
instead of remaining pending. Slurm applies limits at several levels,
as its [resource-limit documentation](https://slurm.schedmd.com/resource_limits.html)
explains.

For pending reasons, `ReqNodeNotAvail` can reflect unavailable,
reserved, down, or drained required nodes; “usually maintenance is
coming” is too narrow. Association group limits are configured
aggregate limits, not synonyms for fair-share priority. Use the exact
reason spelling from the site's capture; the current official list
uses `AssocGrpCpuLimit`, rather than the table's `AssocGrpCPULimit`.
[Official reason codes](https://slurm.schedmd.com/job_reason_codes.html).

Keep the dependency lesson, but qualify “the second stays pending”:
invalid-dependency policy can cancel it instead. The invariant is that
`afterok` does not release the successor after an unsuccessful
predecessor. Quote `"afterok:$jid"` in the supplied command, and
capture the site's actual result. The relevant option is documented
under [`--kill-on-invalid-dep`](https://slurm.schedmd.com/sbatch.html#OPT_kill-on-invalid-dep).

### 8. Align the final wrapper, assessment, and interactive-session model

**Priority: medium. Locations:** section 5, lines 243–264;
section 6, lines 289–291; section 11; self-check, lines 552–553;
open questions 2 and 4, lines 749–761.

I agree with the proposal to wrap Chapter 8's scripts. Their names are
already the cross-chapter contract, and reusing their input checks,
result publication, and logs is more instructive than maintaining a
second counting implementation. Resolve the choice before capturing
the final check: `01` writes the table to `results/read_counts.tsv`;
its application log does **not** contain that table. Update the check
to inspect the result file as well as the scheduler log, and explain
the two log layers. Adjust the read-2-only exercise if the wrapper now
calls a script that deliberately processes all raw files.

`COMPLETED`/`0:0` establishes successful reported execution, not
scientifically correct output. Keep Chapter 8's explicit count/shape
check; a wrapper does not repair a tool that reports success on bad
input. Slurm's own [exit-code guide](https://slurm.schedmd.com/job_exit_code.html)
explicitly discusses a successful script hiding an unsuccessful
application.

The comparison table should distinguish at least a login-shell
process, an interactive allocation/step, and a batch job. The
interactive shell **is** part of a scheduler job, so “process in your
terminal vs job” is not a strict opposition. Replace the self-check's
absolute “the shell ends when the laptop closes” with “do not rely on
an unprotected interactive session surviving; batch work is designed
to run independently of that connection.”

Keep the documented Ceres/Nova versus Atlas `salloc` behavior in site
notes, and show how to verify/release any remaining allocation after
exiting its shell. This matters particularly to the complete
ProxyJump acquire/connect/release route Chapter 9 deferred here.
The [SCINet differences guide](https://scinet.usda.gov/guides/resources/CeresAtlasDifferences#salloc)
documents that distinction.

## Teaching and presentation improvements

### Give readers a first successful job before the reference tour grows

Thirteen sections and twelve tables are substantial for the target
reader. Keep a short minimum route: identify the site/account and
project path, obtain a shell, submit one known script, inspect its
result/log/status, diagnose failure, then run the array. Put full QOS
inspection, the storage comparison, option tables, and module-tree
details where readers can revisit them as references.

Accept the proposed inline overview labels for chains and GPUs, with
the chain exercise optional. Keep chains here: they fulfill Chapter
8's explicit promise, while Chapter 25 can develop the limitations.
The read-count and GTF steps happen to have independent inputs; say
that `afterok` imposes the chosen order rather than implying `02`
consumes `01`'s output.

No-cluster readers need supplied material for each required exercise,
including a fictional or captured site card and the resource-sizing
comparison. Make those alternatives explicit, not only the failure-log
exercise. Continue using the real tiny script for local success and
captured scheduler evidence for cluster behavior.

### Close the remaining script/setup and figure details

- `nproc` and `free -g` help compare machines, but are not proof of the
  CPU/memory allocation: `free` describes node memory, and CPU
  visibility depends on affinity/configuration. Put allocated resources
  beside the hardware display rather than inviting readers to use all
  the reported RAM.
- Supply the promised temporary-file example for `sort`, or narrow
  the section's forward-link promise. Setting or choosing a temporary
  root matters only if the tool uses it; merely placing inputs there
  does not configure every tool's temporary output.
- Capture module initialization in a **noninteractive batch shell**,
  not just `module spider` on login. If a job needs a site setup line,
  show that explicit line. An inherited `PATH` does not by itself
  establish the whole module environment.
- The download location for job scripts is not yet defined in
  `_variables.yml`. Pin the finished bundle and show the exact save
  locations before reader-facing download commands are written.
- Keep a copy of the original request and its job ID for each attempt.
  `sbatch` stores the submitted wrapper; an analysis script it calls
  by pathname is read when executed, so editing that file while the
  job waits can change what runs. Existing git commits/checksums can
  document the intended version without a new version-control lesson.
- Use neutral styling for storage hardware and CPU allocations.
  `given` represents data, not everything the reader writes or the
  home filesystem; `good` marks checks. Label lifecycle outcomes with
  text and shape as well as color. Keep purging as a pitfall cue and
  the six-step lifecycle figure as planned.

## Verification and remaining limits

I ran focused checks in fresh `/private/tmp/` directories with Bash
5.3.15, the installed Pixi CLI, and macOS system tools. These reproduced
the first script's unbound-variable failure, the exact array index
mapping and empty successful selection past the last row, Pixi's
manifest-discovery failure outside a workspace, and Apple's rejection
of `/usr/bin/time -v`. I also checked the local-default repair using a
clearly identified stand-in for Pixi; that verifies argument/control
flow only, not SeqKit output or Slurm behavior.

Documentation checks used official SchedMD, SeqKit, SCINet, and ISU
pages. Existing login observations in the plan/appendix are useful
evidence, but I did not make new cluster connections, submit jobs,
allocate memory deliberately, download additional datasets, or change
the environment.

The final wrapper, four-row manifest, per-task results, staged-output
recipe, failure jobs, applicable QOS, batch `$TMPDIR`, and accounting
captures still need an end-to-end run together. Keep those tasks in
the proposed `chapter_10_checks.md`, with local prerequisites and
site-dependent expected outcomes made explicit.
