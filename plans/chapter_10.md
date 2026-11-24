---
title: "Chapter 10 — HPC and SLURM"
subtitle: "Chapter plan · core · agreed · drafted"
date: 2026-11-23
---

**Part:** II — The Linux command line · **Label:** core · **Status:**
first draft written 2026-11-23 (`chapters/10-hpc-slurm.qmd`; see
*Drafting notes*); agreed 2026-11-23, after the hands-on checks on all three clusters
(`chapter_10_checks.md`) and a consistency pass against the Chapter 8
and 9 drafts; ready to draft. Drafted 2026-11-22; revised the same day after
`chapter_10_codex_review.md` (what changed and why: *Review response*
at the end); open questions decided by Austin the same day
(*Decisions*). Site facts come from Appendix A (checked 2026-11-21/22
against the sites' pages and by logging in to Ceres, Atlas, and Nova).
Rows marked *observed* were seen on those logins; every
check has been run (`chapter_10_checks.md`); anything not checked is
said in place. Where a site behaviour is inferred rather than
confirmed, the plan says *inference*.

## From `PLAN_CHAPTERS.md`

- Cluster anatomy: login vs compute nodes
- Environment modules (`module load`, Lmod)
- Storage tiers: home, project, scratch; quotas (site quota command) and
  purges
- File-count (inode) quotas: millions of small files (a Nextflow `work/`
  directory, environments in `$HOME`) can fill an account that has bytes
  to spare
- `sbatch` scripts and resource requests
- Estimating memory, time, and disk for a job; measuring a real one
- Interactive jobs
- Job arrays
- Monitoring and accounting (`squeue`, `sacct`, `seff`); cancelling
  (`scancel`)
- A running process vs a submitted job
- GPU partitions (brief)
- Etiquette: no heavy work on login nodes

**Proposed additions** (small; inside existing topics, no new
chapter): accounts, partitions, and QOS as the three things a request
names (§2); node-local temporary space as a fourth storage tier (§3);
Open OnDemand sessions are jobs too (§5); job states and pending
reasons as the way to read a failure (§8); one short overview section
on job dependencies (`--dependency=afterok`), because Chapter 8
promised "a cluster version (each step as an `sbatch` job) is Chapter
10" (§11). `PLAN_CHAPTERS.md` is to be updated to match once this plan
is agreed (that file has uncommitted edits from the Chapter 8/9
session, so not edited now).

## What this chapter builds on

Earlier chapters made promises this chapter must keep (each is a
forward link in the written text):

- **Chapter 1:** `fig-cluster-anatomy` (login node, scheduler, compute
  nodes, shared storage); the first-session box `srun --cpus-per-task=1
  --mem=4G --time=01:00:00 --pty bash -l`; "many sites need more options,
  such as an account (`-A`) or a partition (`-p`) … `@sec-hpc-slurm`
  explains all of this properly"; "finding which one [CPU, RAM, I/O]
  limits a real job is part of `@sec-hpc-slurm`"; "a small run is not a
  fair sample"; misconceptions `run-on-login-node`,
  `cluster-faster-computer`, `ram-is-disk`, `more-cores-faster`.
- **Chapter 2:** pixi installed in project storage from a compute
  session; `PIXI_CACHE_DIR`; Open OnDemand VS Code sessions with
  Account, Partition, hours, cores, memory; **Cancel** ends a session
  (`closing-tab-ends-session`).
- **Chapter 3:** "large intermediate files may live in scratch while a
  job runs, with only the final results kept in the project
  (`@sec-hpc-slurm`)"; `logs/`; `data/meta/reads.tsv` (one row per run:
  `sample`, `run`, `fastq_1`, `fastq_2`) and `data/meta/samples.tsv`
  (one row per sample); `data/raw/` write-protected, with
  `checksums.md5`; sample labels in the nf-core fixture repeat, so runs
  are the unique key; `cluster-is-backed-up`.
- **Chapter 4:** `tbl-common-errors` row "`Killed` … often, not always,
  out of memory → the scheduler's records (`@sec-hpc-slurm`)";
  `slurm-<jobid>.out` as a place to look; troubleshooting steps 2 and 5
  ("Where is the log?", "Are resources short?").
- **Chapter 5:** `tail -f` to watch job logs; `find … -type f | wc -l`
  to count files "when a cluster limits how many you may have"; the
  host name in the prompt tells login from compute node.
- **Chapter 6:** `sort` writes temporary files ("where, on a cluster, is
  `@sec-hpc-slurm`"); reading a 10 GB file is a job, not login-node
  work; `errors-go-to-file`.
- **Chapter 7:** `#!/usr/bin/env bash`; `module load` works by changing
  `PATH`; `TMPDIR` and `SLURM_*` rows of the environment-variable
  table; "do not load modules or start environments from startup
  files"; `ps -u "$USER"` on a login node; `closed-window-decides` ("or
  as a scheduler job"); `tbl-cluster-quotas` and "your real limit is a
  quota".
- **Chapter 8 (drafted, `chapters/08-shell-scripts.qmd`):** "`sbatch` scripts … are shell scripts with
  `#SBATCH` lines on top: this chapter's scripts are what Chapter 10
  submits"; job arrays replace the `for` loop over samples; `SLURM_*`
  variables as inputs; `set -euo pipefail`; `src/01_count_reads.sh`
  (run from the project root; writes `results/read_counts.tsv` and its
  own log in `logs/`), `src/02_gtf_summary.sh`, `src/run_all.sh`.
  In the draft: `01` first checks `data/raw/checksums.md5`, writes
  `results/read_counts.tsv` through a `.tmp` name, and keeps a dated
  log `logs/01_count_reads_<date>_XXXX.log`; `02` writes
  `results/gtf_feature_counts.tsv`; `run_all.sh` runs the steps by
  name, stops at the first failure, and keeps
  `logs/run_all_<date>_XXXX.log`. Exercise 4 adds
  `src/03_transcript_biotypes.sh` (`results/transcript_biotypes.tsv`)
  and says `02` and `03` "could run at the same time"; the pipeline
  section lists "runs one step at a time" as a limit. Its two forward
  links: scripts handed to a cluster as a job (opening) and "running
  each step as a cluster job" (pipeline section).
  (Chapter 8's practice `samples.tsv` in `~/bioinf-computing-ch05/` is a
  deliberately imperfect fixture, not a project file; it is not used
  here.)
- **Chapter 9 (drafted, `chapters/09-working-remotely.qmd`):** tmux keeps a **shell** alive on a login
  node; "heavy work goes to a job, which survives without tmux";
  `.pixi` not copied because of file-count quotas; storage tiers
  deferred here. **ProxyJump** (Chapter 9 decision 11, 2026-11-22):
  Chapter 9 explains the two hops and shows a minimal `Host
  <allocated-node>` / `ProxyJump nova` block with a placeholder, but
  runs nothing; **this chapter teaches the whole route live**
  (acquire → connect → release, §5), and Appendix A keeps only the
  per-site config block. Chapter 9's `fig-proxyjump` and its
  `nova`/`nova-dtn` aliases are reused, not redrawn. Chapter 2's
  `tbl-where-to-edit` row "Remote-SSH to a compute node: SSH keys, a
  held compute node" is also kept here.
  The draft's forward links (11), each kept here: jobs on compute
  nodes (§4–§6); what the storage areas are and why the project lives
  in `/work/<group>/<netid>` or `/project/<project>/<you>` (§3); how to
  get a node, connect with `ssh -J nova <allocated-node>`, and give it
  back (§5); ISU's `ForwardAgent yes` and `StrictHostKeyChecking no`
  (§5); heavy work in a job, which needs no tmux (§5, §6); the file
  limits that keep `.pixi/` from being copied (§3); `pixi install
  --locked` in an interactive job when it is slow (§5); VS Code
  Remote-SSH on a compute node (§5). Its project move ends with the
  project at `/work/<group>/<netid>/bioinf-computing` (no `results/`
  or `logs/` copied), the reference at
  `/work/<group>/<netid>/bioinf-shared/references/yeast_R64-1-1_test`
  with `data/ref` linked to it, and `pixi run bash src/run_all.sh` run
  **on the login node** as the test (exit 0, same checksums as the
  laptop). Its aliases: `nova`, `nova-dtn`, `ceres`, `ceres-dtn`,
  `atlas`, `atlas-dtn`.

**Boundaries.** Appendix A owns per-site recipes and numbers (hosts,
quota commands, partition lists); the chapter shows the general idea
with Nova and SCINet as worked examples in one compact table, and
links there. Chapter 24 owns containers (Apptainer); here only "a
module or a container can provide software". Chapter 26 owns running
nf-core on SLURM (Nextflow submits the jobs itself). Chapter 35 owns
threads and parallel speed-up in depth; here only "ask for as many
CPUs as the tool is told to use". Chapter 37 owns GPUs; here one short
overview section.

## Outcome and check

- **Outcome:** readers can read a cluster's layout (`sinfo`, their
  accounts), choose where files go (home, project, scratch, node-local
  temporary space) and check their quotas; load software with modules
  or the book environment; hold a compute node interactively and
  release it; write, submit, watch, and cancel a batch job; read why a
  job is pending or failed; measure what a finished job used and use
  that as a starting estimate for the next request; and run one script
  over many inputs with a job array.
- **Check (cluster path):** from the project folder, submit the
  chapter's job script, which wraps Chapter 8's `src/01_count_reads.sh`,
  then confirm it three ways:

  ```bash
  mkdir -p logs
  sbatch jobs/01_count_reads.sbatch
  sacct -j <jobid> --format=JobID%20,JobName,State%15,ExitCode,Elapsed,AllocCPUS,ReqMem,MaxRSS
  cat logs/01_count_reads_<jobid>.out
  cat results/read_counts.tsv
  ```

  Expected: `State` `COMPLETED` and `ExitCode 0:0` on the job and its
  `batch` step; the scheduler log shows the job's start line, host, and
  Chapter 8's own messages; `results/read_counts.tsv` holds 50,000 for
  each of the two `SRR6357070` files (the same numbers as Chapters
  1–3). The text says plainly that `COMPLETED` means the script exited
  0, not that the result is right: the count check is what confirms the
  result (Slurm's exit-code guide makes the same point). `MaxRSS` is
  well below `ReqMem` (Nova, *observed* 2026-11-23: `COMPLETED 0:0`
  on all three lines, `Elapsed 00:00:02`, `MaxRSS 116244K` on `.batch`
  against `ReqMem 2G`, `AllocCPUS 2` for a 1-CPU request, see §7).
- **Check (no-cluster path):** the job script is a bash script with
  local fallbacks for the `SLURM_*` values (`job_id=${SLURM_JOB_ID:-local}`),
  so `bash jobs/01_count_reads.sbatch` runs on the laptop from the
  project folder, says "job local", and leaves the same
  `results/read_counts.tsv`. Bash ignores the `#SBATCH` lines; it does
  not create Slurm's environment, which is why the fallbacks exist.
  Then readers answer three questions from a supplied, annotated
  captured `sacct` table (which job ran out of memory, which hit its
  time limit, which asked for far more memory than it used).

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Tell a login node from a compute node, list a cluster's partitions
   and your accounts, and say which work belongs where.
2. Choose the right storage area for a file, and check your use against
   your quota (bytes, and files where the site counts them).
3. Load software with `module load` or the book environment, and keep
   the two from clashing.
4. Write and submit a batch job with sensible resource requests, then
   watch, read, and cancel it.
5. Find out why a job is waiting or failed, measure what a finished job
   used, size the next request from it, and run one script over many
   inputs with a job array.

## Sections

Same pattern as Chapters 1–9: each section opens with something readers
run, then names the idea. Practice uses the book project on the cluster
(`/project/<project>/<user>/bioinf-computing` on SCINet,
`/work/<group>/<netid>/bioinf-computing` on Nova, set up in Chapters 2
and 9), submitted **from the project folder**, plus a scratch folder
`bioinf-computing-ch10` beside it (not in home: §3 says why). New in the
project: `jobs/` (job scripts); `logs/` exists from Chapter 3.

**Minimum route.** For a reader in a hurry, the path through the
chapter is: §2's first two commands (partitions, accounts) → §5 (a
shell on a compute node) → §6 (first job) → §8 (reading a failure) →
§10 (array). The rest (QOS details, the storage comparison, module
trees, the option and state tables) is written so readers can come back
to it; tables sit in collapsible or clearly labelled reference blocks,
and §11–§12 are labelled overview inline.

Visual items in brackets are specified under *Visuals and teaching
aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph:
   so far readers have used a compute node only by asking for a shell
   (Chapter 1's `srun`); real analyses run as **jobs** that the
   scheduler starts when resources are free, while you are logged out.
   Recall `fig-cluster-anatomy`; one new idea: the scheduler is a queue
   in front of the compute nodes. *Start hands-on:* `hostname`, `nproc`,
   `free -g` on the login node, then inside `srun … --pty bash -l` the
   same three **plus** `echo "$SLURM_CPUS_PER_TASK"` and `scontrol show
   job "$SLURM_JOB_ID" | grep -E 'NumCPUs|mem='`. Lesson: a different
   machine; `free` describes the whole node, and what `nproc` shows
   depends on site configuration, so the allocation lines, not the
   hardware ones, say what **you** may use (Ceres, *observed*
   2026-11-23, 2 CPUs and 2 GB on `ceres20-compute-6`: `nproc` → 2,
   `free -g` → 754 GB total, `SLURM_CPUS_PER_TASK` → 2,
   `SLURM_MEM_PER_NODE` → 2048, `scontrol` → `NumCPUs=2`,
   `AllocTRES=cpu=2,mem=2G`, `QOS=ceres`; Nova the same pattern on
   `nova18-wide-13`: `nproc` → 2, `free -g` → 376 GB, `QOS=normal`). No-cluster readers: which sections work locally (§6's job
   script with `bash`, §10's array selection with test values) and
   which are captured sessions. [`fig-cluster-anatomy` reused; key idea
   "work runs as jobs"]

2. **Look at the cluster: nodes, partitions, accounts, QOS.** *Start
   hands-on:* `sinfo -s` (*observed* 2026-11-21: Ceres `ceres*` 60 days
   and `scavenger` 21 days; Atlas `atlas*`, `bigmem`, four GPU
   partitions, `development`, `service`, all `infinite`; Nova `nova*`
   31 days, `interactive` 8 h, `instruction` 2 days, `scavenger`, …).
   Read the columns: `*` marks the default partition; `A/I/O/T` =
   allocated / idle / other / total nodes. Then `sacctmgr -n show assoc
   user=$USER format=account%30` (*observed* on all three: the accounts
   you may charge). *Then name it:* a **partition** is a group of nodes
   with its own limits; an **account** is who is charged (your project
   or group); a **QOS** (quality of service) is another set of limits
   that can apply to a request. Limits apply at several levels, and the
   strictest wins (Slurm's resource-limits page). Motivating example,
   labelled as such: Ceres's `ceres` partition shows 60 days, while
   SCINet's guide gives 3 weeks; the explanation is the `ceres` QOS,
   whose `MaxWall` is `21-00:00:00` (*observed* 2026-11-23 with
   `sacctmgr show qos`; `scontrol show partition ceres` shows
   `QoS=ceres`, so the partition attaches that QOS to every job in it;
   *observed* 2026-11-23). Showing a partition's own settings is the
   reader's tool for this: `scontrol show partition <name>` lists
   `DefaultTime`, `MaxTime`, `DefMemPerCPU`, and `QoS` (Ceres:
   2 hours, 60 days, 2,000 MB per CPU, `ceres`; Nova's `nova`: 4 hours,
   31 days, 3,800 MB per CPU, `QoS=N/A`, and your association's
   default QOS `normal` has no `MaxWall`, so the partition's 31 days is
   the limit; Atlas's `atlas`: 2 hours default, `MaxTime=UNLIMITED`
   (the `infinite` in `sinfo`), 7,686 MB per CPU, `QoS=N/A`, and the
   `normal` QOS sets **14 days** (`MaxWall 14-00:00:00`,
   `cpu=1920,node=40`); *observed* 2026-11-23). Reference block: how to see
   your own applicable limits (`sacctmgr show assoc user=$USER
   format=account,partition,qos,defaultqos`; `sacctmgr show qos
   format=Name,MaxWall,MaxTRESPU%30`; the `QOS=` field of `scontrol
   show job` for a real job; all readable as an ordinary user on the
   three sites, *observed* 2026-11-23: `QOS=ceres` on Ceres,
   `QOS=normal` on Nova). A request
   that breaks a limit may be **rejected when you submit** or left
   **pending** with a reason (§8), depending on site settings. Ceres
   rejects it at once (*observed* 2026-11-23, `--time=30-00:00:00`):
   `sbatch: error: QOSMaxWallDurationPerJobLimit` then `sbatch: error:
   Batch job submission failed: Job violates accounting/QOS policy (job
   submit limit, user's size and/or time limits)`; no job is created.
   Nova also rejects it, with a different message because its limit is
   the partition's, not a QOS (*observed* 2026-11-23,
   `--time=40-00:00:00`): `sbatch: error: Batch job submission failed:
   Requested time limit is invalid (missing or exceeds some limit)`.
   Atlas refuses a 30-day request with Ceres's message
   (`QOSMaxWallDurationPerJobLimit`; its `normal` QOS allows 14 days).
   All three sites refuse at submission, so the pending reasons
   `QOSMaxWallDurationPerJobLimit` and `PartitionTimeLimit` appear only
   on sites configured to accept such jobs; say so beside the table.
   **Scavenger** partitions run on idle nodes and can be stopped
   (preempted). What one node has: `sinfo -N -o "%N %c %m %G" | head`
   (CPUs, memory in MB, GPUs; *observed* 2026-11-23: Ceres
   `ceres20-compute-*` 96 CPUs, 752,000 MB; Nova `nova18-5` 72 CPUs,
   189,000 MB; Atlas `atlas-0001` 48 CPUs, 385,323 MB). Site table
   (`tbl-sites-slurm`), linking Appendix A for the full lists.
   [`tbl-slurm-vocab`, `tbl-sites-slurm`; self-check]

3. **Where files go: storage tiers and quotas.** *Start hands-on:* the
   site's quota command (`my_quotas` on SCINet; `cat
   /work/<group>/group_storage_usage` on Nova), then, in the cluster
   project folder, `find .pixi -type f | wc -l` and `du -sh .pixi`
   (laptop: about 15,500 files and 1.3 GB, *measured* 2026-11-16;
   Ceres: 13,001 regular files, 15,528 entries in all, 1.3 GB,
   *observed* 2026-11-23; Nova the same 13,001 and 15,528 but `du`
   813 MB, because Nova's `/work` compresses, *observed* 2026-11-23). Say that this counts regular files only; a
   site's object or inode count also includes folders and links, so the
   two numbers need not match. *Then name it:* four tiers in
   `fig-storage-tiers`: **home** (small; config and the `pixi` program
   only), **project/group** (your work, shared with the lab, quota per
   project; also the `bioinf-shared/references` folder Chapter 9 made,
   which `data/ref` links to), **scratch** (big, purged: `/90daydata` 90 days on SCINet,
   `/ptmp` 60 days unused on Nova; never backed up), **node-local
   temporary space** (on the compute node itself; SCINet's scratch guide
   and ISU's storage page say it is deleted when the job ends; often
   faster than network storage for many small files, but that depends on
   the site and workload). Plus long-term archive (Juno on SCINet;
   `/lss` on Nova, not visible from compute nodes). Observed: Ceres and
   Nova set `TMPDIR=/tmp` at the start of an interactive session. In a
   Ceres **batch** job (*observed* 2026-11-23) `TMPDIR` is also `/tmp`,
   but that `/tmp` is an empty folder owned by you, mode `drwx------`
   (a normal `/tmp` is `drwxrwxrwt`, shared by everyone), on a 1.5 TB
   local NVMe disk, and `scontrol show config` shows `NamespaceType =
   namespace/tmpfs`, `TmpFS = /tmp`: Slurm gives each job its own empty
   `/tmp`, removed when the job ends. Readers can check their own site
   with `scontrol show config | grep -i -E 'NamespaceType|JobContainer'`.
   Atlas does **not** (`NamespaceType = (null)`, *observed*
   2026-11-23); instead an Atlas batch job gets **`TMPDIR=/local/
   scratch/<user>/<jobid>`**, a new empty folder for each job (mode
   `drwxr-xr-x`, owned by you) on a 1.7 TB local NVMe disk mounted at
   `/local`; two jobs on the same node each saw only their own file
   (*observed* 2026-11-23). There, `/tmp` itself is the node's shared
   one, which is why the chapter says "use `$TMPDIR`", not "use
   `/tmp`". Whether Atlas deletes the folder when the job ends is not
   observed (SCINet's guide says node-local space is temporary).
   Nova has the same setting as Ceres (`namespace/tmpfs`, `TmpFS = /tmp`,
   *observed* 2026-11-23; a Nova batch job shows the same private
   `drwx------` `/tmp` on a 1.5 TB NVMe disk). So the chapter
   teaches "make your own folder under it", never "clean `$TMPDIR`".
   *Then file counts:* many systems limit **files** as well as bytes; a
   Nextflow `work/` folder can reach millions (Chapter 26). Nova and
   SCINet do not state a file-count limit (Appendix A), but Nova's
   usage file reports `OBJUSED`, and many other sites do limit it.
   *Then the staging pattern* (Chapter 3's promise), complete, shown
   here and used in exercise 6:

   ```bash
   project=$PWD                                   # submit from the project folder
   out="$project/results/sorted_counts.tsv"       # absolute path, decided before cd
   tmp_root=${TMPDIR:?TMPDIR is not set}          # stop if the site did not set it
   work=$(mktemp -d "$tmp_root/ch10_${SLURM_JOB_ID:-local}_XXXX")
   cp "$project/results/read_counts.tsv" "$work/"
   LC_ALL=C sort -T "$work" -t $'\t' -k4,4n "$work/read_counts.tsv" > "$work/sorted.tsv"
   cp "$work/sorted.tsv" "$out.tmp" && mv "$out.tmp" "$out"
   rm -rf "$work"                                 # only the folder this job made
   ```

   Points named under it: the job makes and removes **its own**
   folder; output paths are fixed before changing folder; `sort -T`
   tells `sort` where to write its temporary files (keeps Chapter 6's
   promise; putting inputs in a folder does not configure a tool's
   temporary files); `-t $'\t' -k4,4n` sorts on `num_seqs`, the fourth
   column of seqkit's table, and the header stays on top because a
   word counts as 0 in a numeric sort (checked 2026-11-23 on the
   laptop with GNU sort: the earlier `-k2,2n` keyed on `FASTQ` and
   moved the header to the bottom); `pixi run` finds the environment from the project
   folder, so commands that need it run there or with `pixi run
   --manifest-path "$project/pixi.toml"`; a job killed by a time or
   memory limit never reaches the copy-back line, so anything that must
   survive a long run is written to project storage as it goes; disk
   checks stay inside the job's own folder (`du -sh "$work"`). The
   chapter uses a tiny file, so this is about the habit, not speed.
   Nova, *observed* 2026-11-23, the block as a 1 GB, 5-minute job
   submitted from the project folder: log `work folder:
   /tmp/ch10_<id>_3FzT on nova18-71`, `8.0K` for that folder, then
   `ls: cannot access '/tmp/ch10_<id>_3FzT': No such file or
   directory` after the `rm -rf` (the folder is gone), and `done: 3
   lines in …/results/sorted_counts.tsv`, header on top; `COMPLETED
   0:0`, `MaxRSS 2376K`. The same script run with `bash` on the laptop
   used macOS's `TMPDIR` and gave the same file.
   *Real-world note (observed 2026-11-22):* moving 2 GB of R packages
   (67,000 small files) from home to `/work` with `mv` took hours and
   died with the SSH connection; small files are slow on network
   storage, and big moves run as a job or with `rsync` in tmux (Chapter
   9). [`fig-storage-tiers`, `tbl-storage-tiers`; misconception
   `cluster-is-backed-up` (revisited), new `space-means-room`;
   self-check]

4. **Software: modules and the book environment.** *Start hands-on
   (login node):* `module avail apptainer` (*observed* on Nova: three
   dated software trees, versions 1.1.5–1.4.0), `module spider
   samtools` (Ceres: `samtools/1.16.1`, `samtools/1.17` in three
   module trees, *observed* 2026-11-23; Nova:
   `samtools/1.16.1-py310-d6uutpz`, `1.19.2-py311-qlmoxzv`,
   `1.23.1-py313-3cgtvqh` across nine module trees, four of them dated
   software releases (`/opt/rit/el9/20230413` … `20250815`); the hash
   suffixes are why readers copy the full name from `module spider`), `module load <name>/<version>`, `module
   list`, `type -a samtools`, `module purge`. *Then name it:* Lmod
   modules change `PATH` and a few other variables (Chapter 7), for
   this shell only; `module spider` searches everything, including
   modules hidden until a compiler is loaded (SCINet: some Atlas modules
   appear only after a `gcc` module). Always load a named version in a
   job script, because the default can change (Nova's "Find First
   Rules" message, *observed*). In a job, load modules **inside the
   script**, not by relying on what was loaded when you submitted; if
   the `module` command is missing in a batch job, the site's setup
   line goes at the top of the script (Ceres, *observed* 2026-11-23:
   `type -t module` → `function` in a batch job, so no setup line is
   needed there; Nova the same, *observed* 2026-11-23; check 4). *Then the
   book's way:* `pixi run` for everything the book environment has; a
   module only for what it lacks; never both for the same tool in one
   job (`type -a` shows which wins, Chapter 7). Do not put `module
   load` in `~/.bashrc` (Chapter 7's rule). [`tbl-module-commands`; tip
   "load a version, not a default"; self-check]

5. **Interactive jobs.** *Start hands-on:* the Chapter 1 `srun` line
   with the site's options (*observed*: Ceres and Atlas need `-A
   <project>`; Nova charges the default account), pasted **alone**;
   then `hostname`, `echo "$SLURM_JOB_ID"`, and `squeue -u $USER` from a
   second terminal (the session is a job, with an ID and a time limit);
   `exit`; `squeue` again (gone; *observed* on all three after `srun
   --pty`). *Then name it:* `srun --pty` starts a shell inside a new
   job; `salloc` first reserves resources and then you start commands
   in them. After leaving an `salloc` shell, check `squeue -u $USER`
   and `scancel <jobid>` anything left; SCINet's differences page
   documents that Ceres and Atlas behave differently here (Atlas needs
   `srun` inside the allocation). Ceres, *observed* 2026-11-23:
   `salloc` lands you **on the compute node** (`Nodes ceres20-compute-6
   are ready for job`, prompt and `hostname` both show the node; the
   job is named `interact` in `squeue`), and `exit` prints `salloc:
   Relinquishing job allocation …`, after which `squeue` is empty.
   Nova behaves the same (`nova21-swift-4`, job `interact`, released;
   *observed* 2026-11-23). **Atlas differs** (*observed* 2026-11-23):
   after `Nodes atlas-0006 are ready for job` the prompt is still the
   login node's and `hostname` prints `atlas-login-1`; only `srun
   hostname` runs on `atlas-0006`. So on Atlas, commands typed after
   `salloc` run on the **login node** unless prefixed with `srun`; use
   `srun --pty bash -l` for an interactive shell there. `exit` still
   releases the job (`Relinquishing job allocation`). Worth a pitfall
   callout: the same `salloc` line means different things on Ceres and
   Atlas. *Then connecting to the node you
   hold* (completes Chapter 9's `ProxyJump`; cluster only, Nova as the
   worked example, from ISU's "Launching remote IDEs on Nova's compute
   nodes"). Four steps, all in one place so nothing is left running:
   1. **Acquire** (login node): hold one node for a set time with
      `salloc` and the site's options; ISU's recipe keeps the
      allocation busy with `sleep infinity` so it lasts until released
      or its time limit. ISU's page gives `salloc -N1 -n 8
      --time=2:00:00 --mem=8G sleep infinity` ("use your standard
      SLURM arguments"); the chapter uses a small request. Nova,
      *observed* 2026-11-23 with `salloc -N1 -n1 --time=00:20:00
      --mem=2G sleep infinity`: `Granted job allocation <id>`,
      `Waiting for resource configuration`, `Nodes nova18-71 are ready
      for job`, then no prompt: the terminal stays busy while you
      hold the node, so the next steps use a second terminal.
   2. **Find the node** (login node): `squeue -u $USER` → the
      `NODELIST` column (Nova names *observed* in the checks:
      `nova18-71`, `nova18-72`, `nova18-wide-33`, `nova21-swift-4`;
      the held job shows as `interact`, state `R`). From the laptop,
      `ssh nova 'squeue -u $USER'` does the same in one line.
   3. **Connect** (laptop): put that name into the `Host
      <allocated-node>` block from Chapter 9 (`ProxyJump nova`), check
      it with `ssh -G <allocated-node> | grep -i proxyjump`, then `ssh
      <allocated-node> hostname` or VS Code Remote-SSH to it (Windows:
      the block must be in the Windows config, Chapter 2). The node
      name changes every time, so the block is edited each time.
      **The block needs a `User` line** (ISU's has one): the `nova`
      alias sets the user name only for the login node, so without it
      ssh uses the laptop's user name for the compute node. Nova,
      *observed* 2026-11-23 from the Mac on the VPN: `ssh -J nova
      <netid>@nova18-71 hostname` printed `nova18-71`, with no password
      or code (the key came from the agent; no `-i` needed). It first
      asked the host-key question (`The authenticity of host 'nova18-71
      (<no hostip for proxy command>)' can't be established`); answering
      `yes` added it to `known_hosts`. A second node showed the **same
      fingerprint** and said `This host key is known by the following
      other names/addresses: … nova18-71`: Nova's compute nodes share
      one host key, so the question comes once per node name but
      always with the same fingerprint. You can SSH to a compute node
      only while you hold a job there: on a node not held, `Access
      denied by pam_slurm_adopt: you have no active jobs on this node`
      then `Connection closed by UNKNOWN port 65535` (*observed*). That
      line is worth quoting: it is what readers see when the allocation
      has ended (§5 self-check).
   4. **Release** (login node): `scancel <jobid>`, then `squeue -u
      $USER` shows nothing; an idle held node still uses the
      account's allocation and blocks others (etiquette, §13). ISU's
      page does not say how to release, so the chapter does. Nova,
      *observed* 2026-11-23: after `scancel`, the waiting `salloc`
      terminal printed `salloc: Job allocation <id> has been revoked.`
      and returned to the prompt; `squeue` empty. (Ctrl-C in that
      terminal is the other way; not tested.)
   ISU's own block adds `ForwardAgent yes` (lets the node use your
   laptop's agent, e.g. for git; anyone with root on the node could
   use it while you are connected) and `StrictHostKeyChecking no`
   (skips the host-key question, because each node is new to your
   `known_hosts`; on Nova the fingerprint is the same for every node,
   *observed*, so answering `yes` once per node is little work); both are explained here as **ISU's choices for that
   one compute-node entry**, never for `Host *`, and the generic
   Chapter 9 block keeps host-key checking on. SCINet: Open OnDemand
   is the supported route to an editor on a compute node (Chapter 2;
   whether direct SSH to a held Ceres/Atlas node works was not
   checked; the chapter does not teach it there). [`fig-proxyjump` reused from Chapter 9; self-check] An
   Open OnDemand VS Code, RStudio, or JupyterLab session is also a job,
   with a web page in front (`closing-tab-ends-session`). Settings the
   site prints on arrival (*observed* on Ceres and Nova: `TMPDIR`,
   Apptainer cache, `TMOUT=5400`, so an idle shell logs out after 90
   minutes). Use interactive jobs for trying commands and short tests,
   and for setup work too slow for a login node: Chapter 9 promised
   `pixi install --locked` here (25 to 40 minutes on Nova in November
   2026), so the worked example is `srun … --pty bash -l`, `cd` to the
   project, `pixi install --locked`, `exit`.
   *Pitfall (observed 2026-11-22):* lines pasted together with `srun`
   wait in the terminal and run **on the login node after the session
   ends**. *Then the comparison* the outline calls "a running process
   vs a submitted job", in three columns (`tbl-process-vs-job`): a
   command on the login node, an interactive job (`srun --pty`,
   `salloc`, OnDemand), and a batch job; rows: where it runs, when it
   starts, what a dropped connection or a sleeping laptop does, where
   output goes, how to stop it, what records remain. Wording for the
   middle column: "do not rely on it surviving a lost connection";
   batch jobs are built to run without one. [`tbl-process-vs-job`;
   pitfall callout; self-check]

6. **Your first batch job.** One sentence first: Chapter 9 ran
   `run_all.sh` on the login node to test the move, which was fine
   because it takes seconds; anything longer is a job, starting now.
   *Start hands-on:* readers save the
   supplied `jobs/01_count_reads.sbatch` into the project, read it, and
   **test it inside an interactive job** (§5) with `bash
   jobs/01_count_reads.sbatch`: it runs and rewrites
   `results/read_counts.tsv`. It does **not** say "job local": an
   interactive job is a job, so Slurm has set `SLURM_JOB_ID`, and the
   first line names the interactive job (Nova, *observed* 2026-11-23:
   `job 17719911 on nova18-72`, the same ID the `srun` banner printed
   as `APPTAINERENV_SLURM_JOB_ID`; Chapter 8's log lines followed, both
   checksums `OK`, exit 0, `read_counts.tsv` MD5 the same as the
   laptop's). "job local" appears only outside any job (laptop, login
   node). Worth one sentence: the `SLURM_*` variables are there in
   every job, interactive or batch. Then on the login node, from the project
   folder: `mkdir -p logs` (Slurm opens the log file before the script
   starts, so its folder must already exist), `sbatch
   jobs/01_count_reads.sbatch` → `Submitted batch job 1234567`; `squeue
   -u $USER` (`PD`, then `R`); `tail -f logs/01_count_reads_<jobid>.out`;
   Ctrl-C stops `tail`, not the job. A 2-second job may be gone before
   `R` shows (Nova, *observed* 2026-11-23: `PD … (None)`, then nothing),
   so say so. Run `sbatch` from the project folder: from `~` it fails
   with `sbatch: error: Unable to open file jobs/01_count_reads.sbatch`
   (*observed*). The script (shown, not run in the book build; tested
   2026-11-23 on Nova without the `--account` line, against Chapter 8's
   drafted script):

   ```bash
   #!/usr/bin/env bash
   #SBATCH --job-name=01_count_reads
   #SBATCH --account=<project>       # SCINet; Nova: delete this line
   #SBATCH --nodes=1
   #SBATCH --ntasks=1
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=2G
   #SBATCH --time=00:10:00
   #SBATCH --output=logs/%x_%j.out   # %x job name, %j job ID
   set -euo pipefail
   job_id=${SLURM_JOB_ID:-local}     # set by Slurm in a job; "local" with plain bash
   echo "job $job_id on $(hostname), started $(date)"
   pixi run bash src/01_count_reads.sh
   echo "job $job_id finished $(date)"
   ```

   *Then name it* with `fig-sbatch-anatomy`: shebang; `#SBATCH` lines
   must come before the first command (bash treats them as comments,
   `sbatch` reads them; after a command they are ignored); they are
   read as plain text, so `$(date)` or `$HOME` in them is not expanded;
   options on the `sbatch` command line override them; `set -euo
   pipefail` so a failed step fails the job. *Then the job's world:* it
   starts in the folder you submitted from (Chapter 8's script needs the
   project root, which is why readers submit from there); it gets a copy
   of your environment at submission time (`--export=ALL` default, so
   `~/.pixi/bin` is on `PATH`; Ceres, *observed* 2026-11-23: the job
   started in the submit folder, saw an exported `PROJ`, and found
   `~/.pixi/bin/pixi`; Nova the same, *observed* 2026-11-23; check 11); it has no
   terminal, so nothing can ask a question; `SLURM_*` variables tell
   the script about itself (`tbl-slurm-env`). **Two logs:** the
   scheduler's (`logs/01_count_reads_<jobid>.out`, everything the job
   prints; stdout and stderr together unless `--error` is set,
   `errors-go-to-file` revisited) and Chapter 8's own log written by
   `01_count_reads.sh` (`logs/01_count_reads_<date>_XXXX.log`, the
   `XXXX` filled in by `mktemp`; both names start `01_count_reads_`, so
   `ls logs` shows them side by side, *observed*). **What runs is fixed late:** `sbatch` keeps a
   copy of the job script, but `src/01_count_reads.sh` is read when the
   job starts, so editing it while the job waits changes what runs;
   note the job ID and the script's git commit in `NOTEBOOK.md`
   (Chapter 8's routine). `fig-job-lifecycle` (stepped) walks the
   whole path. [`fig-sbatch-anatomy`, `fig-job-lifecycle`,
   `tbl-slurm-env`; key idea "a job is a script plus a resource
   request"; misconception `job-runs-in-my-shell`; self-check]

7. **Asking for resources.** *Start hands-on:* read the §6 request line
   by line against `fig-resource-box`. *Then name it:* a request is a
   box of CPUs × memory × time on one node. Going over **memory** gets
   the job killed; going over **time** gets it killed; asking for
   **CPUs** the tool does not use leaves them idle but still reserved.
   The tool's own option decides how many threads it starts: seqkit's
   `-j` defaults to **4** (and reads `SEQKIT_THREADS`), so with
   `--cpus-per-task=1` an unadjusted seqkit starts more threads than it
   was given, and with `--cpus-per-task=8` and no `-j` it uses four.
   Pass the request to the tool: `-j "$threads"` with
   `threads=${SLURM_CPUS_PER_TASK:-1}` (used in §10's script).
   `more-cores-faster` revisited, new `cpus-sets-threads`. Request
   shape: most bioinformatics tools are one program with threads, so
   `--nodes=1 --ntasks=1 --cpus-per-task=N`; `--ntasks` counts
   separate tasks (copies of a program), which the book's tools do not
   need. A Slurm "CPU" may be a core or a hardware thread, depending on
   the site. Nova, *observed* 2026-11-23: the §6 job asks for
   `--cpus-per-task=1` and `sacct` shows `AllocCPUS 2` (`seff`: `Cores
   per node: 2`), because `SelectTypeParameters = CR_CORE_MEMORY`
   allocates whole cores and the nodes have `ThreadsPerCore=2`; so
   odd requests round up, and `seff`'s efficiency is measured against
   the 2. One sentence and a `sacct` line in the text: "check
   `AllocCPUS`, not only what you asked for". `--mem` (per node) vs `--mem-per-cpu` in one sentence; use
   `--mem`. Time format `D-HH:MM:SS`. What you get if you leave
   `--time` or `--mem` out is the partition's default, not "as much as
   needed" (Ceres: 2 hours and 2,000 MB per CPU; Nova: 4 hours and 3,800 MB
   per CPU; Atlas: 2 hours and 7,686 MB per CPU; *observed* 2026-11-23 with `scontrol show partition`), so always set both. `tbl-sbatch-options` lists the
   dozen options readers need. CPU efficiency is taught with one
   captured, longer job (Ceres, *observed* 2026-11-23: two 2-minute
   Python jobs holding 4 CPUs each; 4 workers busy → `seff` `CPU
   Efficiency: 95.04% of 00:08:24 core-walltime`, `TotalCPU 07:58.890`;
   1 worker busy → `24.00% of 00:08:20`, `TotalCPU 02:00.008`; both
   about 70 MB of the 1 GB asked for; Nova the same pair: 97.15% and
   24.39%),
   not with the toy count, which finishes too fast to show anything
   (Ceres, *observed* 2026-11-23: the 2-CPU count ran 2 s and `seff`
   reported `CPU Efficiency: 0.00%`).
   *Then why accurate requests matter:* the scheduler can fit small,
   short jobs into gaps while it waits to start a large one
   (**backfill**), so a shorter request **can** start sooner; it is not
   guaranteed. Fair share is based on what your jobs actually used while
   they ran (allocated resources × elapsed time, weighted as the site
   chooses), so asking for 3 days and finishing in 10 minutes does not
   by itself charge 3 days; CPUs reserved but idle while the job runs do
   count. `fig-backfill` (interactive) lets readers try it. New
   misconception `ask-big-to-be-safe`. [`fig-resource-box`,
   `tbl-sbatch-options`, `fig-backfill`; self-check]

8. **When jobs wait or fail.** *Start hands-on: break it on purpose.*
   Four supplied scripts in `bioinf-computing-ch10/`, each starting
   with `project=<path to your project>` and running tools through
   `pixi run --manifest-path "$project/pixi.toml"` (the folder is
   outside the project, and pixi would otherwise not find the
   environment). The book environment is already installed (Chapter 2),
   so no job installs anything under a small memory limit. (0)
   `ok.sbatch` runs a tiny Python command by the same route and
   completes: proof the route works. (a) `oom.sbatch` asks for
   `--mem=500M` and allocates 2 GB in Python → Ceres (*observed*
   2026-11-23): `OUT_OF_MEMORY`, `ExitCode 0:125` on the allocation and
   `.batch` lines, after 5 s; log: `slurm_script: line 8: <pid> Killed
   pixi run …` then `error: Detected 1 oom_kill event in
   StepId=<id>.batch. Some of the step tasks have been OOM Killed.` No
   Python `MemoryError`. `MaxRSS` showed `1045816K`, **above** the
   500M request (the kernel kills a moment after the limit is passed,
   and sampling adds noise), so say "MaxRSS near or above ReqMem plus
   `OUT_OF_MEMORY`". Keeps Chapter 4's `Killed` promise. Cluster only:
   not run on a laptop. Nova gives the same state, exit code, and both
   log lines (`MaxRSS` printed as `1G`; *observed* 2026-11-23). (b) `timeout.sbatch` asks
   for `--time=00:01:00` and runs `sleep 300` → Ceres: allocation line
   `TIMEOUT 0:0` at `00:01:07`, but the `.batch` line `CANCELLED 0:15`
   (signal 15, SIGTERM) — the reason is on the allocation line here;
   log line `error: *** JOB <id> ON <node> CANCELLED AT <time> DUE TO
   TIME LIMIT ***`. (c) `typo.sbatch` runs `bash
   "$project/src/01_count_raeds.sh"` (a misspelled script name) →
   Ceres: `FAILED`, `127:0` on both lines, log `bash: <path>/src/
   01_count_raeds.sh: No such file or directory`. In all three
   failures the script's final `echo "end …"` never ran, which is how
   the log shows where it stopped. `ExitCode` is `code:signal`
   (`127:0` the script's own status; `0:15` and `0:125` mean stopped
   from outside). `sacct` cuts `OUT_OF_MEMORY` to `OUT_OF_ME+`, so the
   chapter's command widens `State%15` as well as `JobID%20`. *Then read the records together:* `sacct -j <id>
   --format=JobID%20,State%15,ExitCode,Elapsed,ReqMem,MaxRSS` shows the
   allocation line and one line per step (`.batch`, and numbered steps
   if the script uses `srun`); read those lines **and** the log, since
   the most useful one varies. `tbl-job-states`. *Then waiting:*
   `squeue -u $USER`, `NODELIST(REASON)` column: `Priority` and
   `Resources` are normal waiting; `QOSMaxWallDurationPerJobLimit` or
   `PartitionTimeLimit` mean the request cannot run as written (fix and
   resubmit; some sites reject it at submission instead);
   `AssocGrpCpuLimit` and other `AssocGrp…` reasons mean your group has
   reached a limit set for the whole group; `ReqNodeNotAvail` means a
   node the job needs is down, drained, or reserved (maintenance is one
   cause). Spellings as on the site's own capture and Slurm's reason-code
   page. `scontrol show job <id>` for everything; `squeue --start` for
   an estimate (often empty). New misconception `pending-means-broken`.
   `last-line-is-the-error` revisited: the log's last line may be the
   scheduler's; the cause is above it. [`tbl-job-states`,
   `tbl-pending-reasons`; troubleshooting callout tying back to Chapter
   4's steps 2 and 5; self-check]

9. **Measuring a job and sizing the next one.** *Start hands-on:* one
   annotated capture of `sacct
   --format=JobID%20,State%15,Elapsed,AllocCPUS,TotalCPU,ReqMem,MaxRSS` for a
   finished job, with the cells to compare marked: the allocation line
   holds the request (`ReqMem`, with its unit; older versions add a
   per-node or per-CPU suffix), the step lines hold use (`MaxRSS` is the
   peak of one step, sampled, not a sum over everything in the job);
   blank or zero values can mean the site does not collect that metric.
   Ceres capture (2026-11-23, the stand-in count job, 2 CPUs, 2 GB):
   allocation line `COMPLETED 0:0 00:00:02 2 00:00.246 2G` with
   `MaxRSS` blank; `.batch` line `MaxRSS 106944K`; `.extern` line
   all zero. `sacct` cuts long names to 10 characters (`22918876.ba+`),
   so the chapter's command widens the column (`JobID%20`, which array
   step names also need). `seff`:
   `Memory Utilized: 104.44 MB`, `Memory Efficiency: 5.10% of 2.00
   GB`, `Cores per node: 2`.
   Then `seff <jobid>` if the site has it (all three have it,
   *observed* 2026-11-23); CPU
   efficiency computed by hand once (`TotalCPU / (Elapsed ×
   AllocCPUS)`) so `seff`'s number is not magic: with the Ceres pair,
   478.9 s / (126 s × 4) = 95.0% and 120.0 s / (125 s × 4) = 24.0%,
   matching `seff`. *Then estimate:* test
   on a small input, measure, scale with care (Chapter 1: small runs are
   not a fair sample; memory often depends on the reference, time on the
   reads). For the next run of a **comparable job that succeeded**,
   start from measured peak memory plus about 25% and measured time
   scaled to the input plus a margin; it is a starting estimate, since
   sampling can miss short peaks, and a job killed for memory tells you
   only that it needed more than it was given. Disk: `du -sh` of outputs
   and of the job's own temporary folder. *Then the habit:* record
   request, use, job ID, and wait time in `NOTEBOOK.md` (Chapter 3).
   `/usr/bin/time -v` in one sentence as a GNU/Linux tool for a single
   command (cluster; macOS's `/usr/bin/time` has no `-v`).
   [`tbl-measure-cmds`; self-check with the supplied captured `sacct`
   table]

10. **Job arrays: one script, many inputs.** The manifest is Chapter
    3's `data/meta/reads.tsv` (tab-separated, one row per **run**:
    `sample`, `run`, `fastq_1`, `fastq_2`), so each task is keyed by its
    run accession, which is unique where sample labels may not be.
    *Start hands-on, no cluster needed:* the selection lines, run for
    every task number before submitting:

    ```bash
    for i in 1 2 3 4 5; do
      SLURM_ARRAY_TASK_ID=$i bash jobs/02_stats_array.sbatch --dry-run
    done
    ```

    prints the run and file each task would use, and task 5 stops with
    "no row 5 in data/meta/reads.tsv" (the check below). The script's
    core:

    ```bash
    task=${SLURM_ARRAY_TASK_ID:?run with sbatch --array, or set it to test}
    threads=${SLURM_CPUS_PER_TASK:-1}
    row=$(awk -F '\t' -v n="$task" 'NR == n + 1' data/meta/reads.tsv)   # row 1 is the header
    [ -n "$row" ] || { echo "no row $task in data/meta/reads.tsv" >&2; exit 1; }
    run=$(cut -f 2 <<< "$row")
    fq=$(cut -f 3 <<< "$row")
    [ -r "$fq" ] || { echo "cannot read $fq" >&2; exit 1; }
    pixi run seqkit stats -j "$threads" -T "$fq" > "results/stats_${run}.tsv"
    ```

    (`--dry-run` stops after the checks; full script supplied.) Then
    `sbatch --array=1-4 jobs/02_stats_array.sbatch`; `squeue -u $USER`
    shows `1234567_[1-4]` then individual tasks; logs
    `logs/%x_%A_%a.out`. *Then name it* with `fig-job-array`: one
    submission, N tasks, each with the same request and its own
    `SLURM_ARRAY_TASK_ID`; it replaces Chapter 8's `for` loop over
    samples, and the tasks can run independently when resources allow:
    at once, one after another, on one node or several, finishing in any
    order, so each writes its own output (`stats_<run>.tsv`).
    `--array=1-40%5` runs at most 5 at once (etiquette). `scancel
    1234567_3` cancels one task; `sacct -j 1234567` shows each (Ceres,
    *observed* 2026-11-23 with the stand-in array: pending shows as one
    line `<id>_[1-4] … PD (None)`; logs `array_<id>_1.out` … `_4.out`;
    `sacct` lists `<id>_1`, `<id>_1.batch`, `<id>_1.extern` per task, so
    array JobIDs need `JobID%20`; dry run printed `runA`–`runD`, then
    `no row 5 in reads_test.tsv`). The real array, Nova, *observed*
    2026-11-23 with the four fixture runs: the dry run on the login node
    printed SRR6357070, 071, 072, 076 (`1 threads`, no Slurm), then `no
    row 5 in data/meta/reads.tsv`; `sbatch --array=1-4` → `squeue`
    `<id>_[1-4] … PD (None)`; logs `02_stats_array_<id>_1.out` …
    `_4.out`, each `task N: run …, 2 threads, on <node>`; four
    `results/stats_<run>.tsv`, 50,000 reads each; `sacct` all
    `COMPLETED 0:0`, `AllocCPUS 2`, `MaxRSS` 72–88 MB, `Elapsed` 0–1 s,
    and the tasks ran on **three different nodes** (`nova18-69`,
    `nova18-wide-10`, `nova18-wide-21` twice): the "one node or
    several" point, seen. Why the
    checks matter: `awk` prints nothing and exits 0 for a row past the
    end, so `set -e` alone would not catch `--array=1-5` with four rows.
    Site maximum array size (`scontrol show config | grep -i
    MaxArraySize`: Ceres and Atlas 10001, Nova **1001**, *observed* 2026-11-23;
    the largest task ID is one less, so Nova allows `--array=1-1000`). [`fig-job-array`; pitfall "header row
    and the last task"; self-check]

11. **Chains of jobs (overview, short).** Chapter 8's numbered pipeline
    as jobs: `jid=$(sbatch --parsable jobs/01_count_reads.sbatch)`, then
    `sbatch --dependency="afterok:$jid" jobs/02_gtf_summary.sbatch`;
    `squeue` shows the second as `(Dependency)`. `afterok` never starts
    the second job after a failed first one; whether it then stays
    pending (`DependencyNeverSatisfied`, cancel it) or is cancelled
    automatically depends on the site (`--kill-on-invalid-dep`). Ceres,
    *observed* 2026-11-23: the second job showed `(Dependency)` while
    the first waited, then **stayed** `PD (DependencyNeverSatisfied)`
    after the first `FAILED 127:0`; `DependencyParameters = (null)`, so
    nothing cancels it: `scancel` it yourself, or submit with
    `--kill-on-invalid-dep=yes`. Nova has the same setting
    (`DependencyParameters = (null)`) and the same result: the second
    job stayed `PD (DependencyNeverSatisfied)` (*observed* 2026-11-23).
    **Atlas differs:** `DependencyParameters = kill_invalid_depend`, so
    Slurm cancels the waiting job itself (*observed* 2026-11-23: after
    the first job `FAILED 1:0`, the second went from `PD (Dependency)`
    to `CANCELLED` with no `scancel`). This is the site difference the
    chapter names: "check `squeue`; on some sites the job waits forever,
    on others it is cancelled". Say that here the two steps have independent inputs:
    `afterok` imposes the order you chose, it does not pass data.
    Tie back to Chapter 8: the simplest route is one job that runs
    `src/run_all.sh` (its order and stop-at-first-failure unchanged);
    separate jobs earn their keep when steps need different resources
    or can run side by side, as Chapter 8 said `02` and `03` could
    (readers who did its Exercise 4 can submit `03` with no
    dependency and see both run at once). One
    paragraph on the limit: this is where a workflow manager (Part VI)
    takes over; nf-core submits its own jobs (Chapter 26). Exercise 5
    (optional). [self-check]

12. **GPU partitions (overview, brief).** What a GPU request looks like:
    `--partition=<gpu partition> --gres=gpu:1`; the exact `--gres`
    form is site-specific (Atlas's OnDemand form shows
    `gpu:a100_1g.10gb`, which `sbatch` refuses; see below); `nvidia-smi` inside the
    job shows the card. Only tools built for GPUs use one (deep-learning
    tools, Parabricks, some basecallers); an ordinary tool on a GPU node
    leaves it idle. Sites: Atlas `gpu-v100`, `gpu-a100`,
    `gpu-a100-mig7`, `gpu-l40s` (*observed*; `sinfo -o "%P %G"`
    on 2026-11-23 gives `gpu:a100:8`, `gpu:l40s:4`, `gpu:v100:2`, and
    for the MIG partition `gpu:nvidia_a100_1g.10gb:56`. Tested with
    `sbatch --test-only` on 2026-11-23: **`--gres=gpu:nvidia_a100_1g.10gb:1`
    and plain `--gres=gpu:1` are accepted**; the OnDemand form's
    `gpu:a100_1g.10gb:1` is refused (`allocation failure: Requested node
    configuration is not available`). So the chapter uses the name
    `sinfo` shows, and teaches `sbatch --test-only` as the safe way to
    check a request. `srun … -p gpu-a100-mig7 --gres=gpu:1 nvidia-smi
    -L` listed the node's eight `NVIDIA A100-SXM4-80GB` cards with one
    `MIG 1g.10gb` device under one of them: the slice the job holds.
    Partition `QoS=mig7` (2 days); QOS time limits 2 days for
    `v100`, `mig7`, `l40s` and 7 days for `a100`); Nova has no separate GPU
    partition: GPU nodes sit in the default `nova` partition (and
    `interactive`, `instruction`, `scavenger`, `nova-arm`), and the card
    type goes in `--gres`, e.g. `--gres=gpu:a100:1` (types `a100`,
    `a100-pcie`, `a40`, `h200`, `gh200`, `l40s`, `rtx_2080_Ti`,
    `rtx_6000`, `rtx_pro_6000`, `v100`, `v100-sxm2-32G`; *observed*
    2026-11-23 with `sinfo -o "%P %G"`); Ceres has none (`sinfo -o "%P
    %G"`: GRES `(null)` on both partitions, *observed* 2026-11-23). Depth:
    Chapter 37. [one row in `tbl-sites-slurm`]

13. **Etiquette and a checklist.** *Start with a quick audit:* `ps -u
    "$USER"` on the login node (Chapter 7), `squeue -u $USER`, the quota
    command. *Then the rules* in `tbl-etiquette` (do / don't): login
    nodes for editing, `sbatch`, small file moves, `module spider`; not
    for alignment, sorting big files, installing large environments, or
    loops over many samples; don't request whole nodes "to be safe";
    throttle arrays; prefer one array over thousands of tiny jobs; delete
    your own temporary folders and scratch copies; cancel what you no
    longer need (`scancel -u $USER` cancels all your jobs, with care).
    `run-on-login-node` closes here. Summary bullets, then the
    exercises. [`tbl-etiquette`; summary]

## Visuals and teaching aids

### Figures (SVG, §7)

Colour roles (STYLE-GUIDE §2): `given` only for data (FASTQ files,
count tables); `good` only for checks (the count check, `COMPLETED`
confirmed by the result); `warn` only for pitfalls (purges, a limit
exceeded); storage, nodes, and CPU allocations in neutral `ink`,
`line`, and `surface`; idle or ignored parts `muted`. Every outcome is
also labelled in text and shape, never by colour alone. Text as real
SVG text.

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-cluster-anatomy` | 1 | reused from Chapter 1 | Not redrawn; one new caption sentence pointing at the queue. |
| `fig-storage-tiers` | 3 | static | Four neutral bands beside a login node and a compute node: **home** (small), **project** (large, shared with lab), **scratch** (large; purge clock icon in `warn`), **node-local temporary space** drawn *inside* the compute node box ("deleted when the job ends"). Per band: size scale (GB / TB), backed up?, purge rule, who sees it. A dashed line: archive (Juno, `/lss`) "not on compute nodes (Nova)". A strip under it: "read from project → work in your own temporary folder → copy results to project", with the FASTQ and result files in `given`. |
| `fig-sbatch-anatomy` | 6 | static | The §6 script with labelled brackets: shebang; `#SBATCH` block "read by `sbatch`, comments to bash; before the first command; not expanded"; `set -euo pipefail`; the fallback line; commands "run on a compute node, in the folder you submitted from"; `%x`/`%j` decoded beside `--output`. |
| `fig-job-lifecycle` | 6 | stepped (6 steps) | (1) you write a script on the login node; (2) `sbatch` → job ID, the job joins the queue (`PENDING`, reason shown); (3) the scheduler finds a node with free CPUs and memory (`RUNNING`); (4) the script runs there, reading and writing shared storage and its log; you can log out (laptop drawn closed from here on); (5) it ends: `COMPLETED`, or `FAILED` / `OUT_OF_MEMORY` / `TIMEOUT`, each with its own icon and label; (6) `sacct` and `seff` read the records, and the result file is checked (`good`). |
| `fig-resource-box` | 7 | static | One compute node as a grid of CPU squares and a memory bar; your request a shaded box (e.g. 4 CPUs, 16 GB) on a time axis. Three panels: memory past the box top → "killed (`OUT_OF_MEMORY`)" (`warn`, pitfall); time past the box end → "killed (`TIMEOUT`)" (`warn`, pitfall); tool using 1 of 4 CPUs → three squares `muted`, "idle, still reserved". |
| `fig-job-array` | 10 | static | One `sbatch --array=1-4` arrow fans out to four task boxes `_1` … `_4`, each pointing at one row of `reads.tsv` drawn beside it (header row `muted`, "row 1 is the header"), each writing `results/stats_<run>.tsv` (`given`) and `logs/…_<A>_<a>.out`. A fifth, dashed task points past the last row: "no row 5: the script stops". Under it, Chapter 8's `for` loop: one box, runs one after another. |

### Interactive figure (Observable JS)

- **`fig-backfill` (§7): "A smaller request can start sooner."** A toy
  scheduler for one 8-CPU node over a 24-hour timeline (simulated, said
  in the caption). Fixed: three running jobs with known end times and
  one big waiting job (8 CPUs, 10 h) that holds a reservation starting
  when the running ones finish. The reader sets their own job's
  **CPUs** (1–8) and **requested hours** (1–24) with two sliders; the
  figure places it at the earliest start that does not delay the
  reservation and prints "in this example, your job starts in N hours".
  Lesson in words, so it survives without JavaScript: here a 2-hour,
  2-CPU request fits in the gap now, while the same work requested as 12
  hours waits until after the big job (a fixed three-row table of slider
  settings and start times sits beside it). Caption: real schedulers
  also weigh priority, fair share, and other jobs arriving, so this is
  a possibility, not a promise. Follows STYLE-GUIDE §7: two inputs in
  their own cells, `echo: false`, hand-built `htl.svg` with
  `class="diagram"` and theme classes, no data.
- Considered and not proposed: an array-index explorer (the dry-run
  loop in §10 teaches the same with a real command).

### Tables (§5)

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-slurm-vocab` | 2 | Term · plain meaning · where you see it — node, partition, account, QOS, job, job step, task, Slurm CPU (a core or a hardware thread, by site), allocation, fair share, preemption (scavenger) |
| `tbl-sites-slurm` | 2 | Ceres · Atlas · Nova — `-A` needed?, default partition and its `sinfo` limit, **where the real time limit comes from**, default time and memory per CPU, interactive partition, scavenger, GPU partitions and `--gres` form, `MaxArraySize`, `seff` available?, Appendix A link (all *observed*; values in *Site differences observed* below). A second, shorter table in §5/§6/§11 or a callout covers the behaviour differences: `salloc`, batch `TMPDIR`, failed chains |
| `tbl-storage-tiers` | 3 | Tier · what goes there · size · backed up? · purged? · visible on compute nodes? — home, project/group, scratch, node-local temporary space, archive (general wording; site names in one column linking Appendix A) |
| `tbl-module-commands` | 4 | Command · what it does — `module avail`, `module spider <name>`, `module spider <name>/<version>`, `module load <name>/<version>`, `module list`, `module unload`, `module purge`, `module show` |
| `tbl-process-vs-job` | 5 | · command on the login node · interactive job (`srun --pty`, `salloc`, OnDemand) · batch job — where it runs, when it starts, lost connection or sleeping laptop, output goes to, stop it with, records afterwards |
| `tbl-slurm-env` | 6 | Variable · meaning · example use — `SLURM_JOB_ID`, `SLURM_JOB_NAME`, `SLURM_CPUS_PER_TASK`, `SLURM_MEM_PER_NODE`, `SLURM_SUBMIT_DIR`, `SLURM_ARRAY_TASK_ID`, `SLURM_ARRAY_JOB_ID`, `TMPDIR` (set by the site, if at all) |
| `tbl-sbatch-options` | 7 | Option · short form · what it asks for · example · notes — `--job-name`, `--account`, `--partition`, `--qos`, `--time`, `--nodes`, `--ntasks`, `--cpus-per-task`, `--mem`, `--output`/`--error` (`%x`, `%j`, `%A`, `%a`), `--array`, `--dependency`, `--mail-type`/`--mail-user` (whether mail works is site-specific), `--gres` |
| `tbl-slurm-commands` | 8 | Command · what it shows or does · example — `sinfo`, `squeue -u $USER`, `squeue --start`, `scontrol show job`, `sacct`, `seff`, `scancel`, `sbatch --parsable`, `sacctmgr show assoc` (the chapter's cheat sheet; candidate for the "Command cheat sheets" appendix) |
| `tbl-job-states` | 8 | State · short · what happened · what to do — `PENDING` `PD`, `RUNNING` `R`, `COMPLETED` `CD` (script exited 0; check the result), `FAILED` `F`, `OUT_OF_MEMORY` `OOM`, `TIMEOUT` `TO`, `CANCELLED` `CA`, `PREEMPTED` `PR`, `NODE_FAIL` `NF` |
| `tbl-pending-reasons` | 8 | Reason · meaning · fix — `None` (just submitted, not yet considered; *observed* on Ceres and Nova), `Priority` (*observed* on Nova for jobs submitted together), `Resources`, `Dependency`, `DependencyNeverSatisfied`, `QOSMaxWallDurationPerJobLimit`, `PartitionTimeLimit`, `AssocGrpCpuLimit` (and other `AssocGrp…`), `ReqNodeNotAvail` (exact spellings from the site capture) |
| `tbl-measure-cmds` | 9 | Question · command · field · read from which line — how long?, how much memory?, were the CPUs used?, how much disk?; `sacct` fields `Elapsed`, `MaxRSS` (step line), `TotalCPU`, `AllocCPUS`, `ReqMem` (allocation line); `seff`; `du -sh` |
| `tbl-etiquette` | 13 | Do · don't · why |

### Code (§6)

- **`sacct` widths:** every `sacct` command in the chapter uses
  `JobID%20` and `State%15` (Ceres cut `22918896_1.batch` and
  `OUT_OF_MEMORY` at the default width).
- **Where commands run:** `filename="Terminal (login node)"` for
  `sinfo`, `sbatch`, `squeue`, `sacct`, `module`, quotas;
  `filename="Terminal (compute node)"` inside `srun` sessions (including
  the first test of the job script); `filename="jobs/01_count_reads.sbatch"`
  for job scripts (the caption says they run on a compute node); laptop
  only for the no-cluster path.
- **Tier:** every cluster command is *shown, not run* in the book build,
  with *captured* output in `.console` blocks from Nova or Ceres (dated;
  user and project names replaced by placeholders; job IDs kept). The
  no-cluster commands (`bash jobs/01_count_reads.sbatch`, the dry-run
  loop) are *precomputed* on the laptop.
- **Annotations** on the first job script, the staging block, the array
  selection lines, and the first `sacct` line.
- **Supplied files:** `jobs/01_count_reads.sbatch`,
  `jobs/02_stats_array.sbatch`, `jobs/02_gtf_summary.sbatch` (§11), and
  the four §8 scripts (`ok`, `oom`, `timeout`, `typo`). Download
  location not yet defined: add a pinned `jobs-url` (or extend
  `setup-url`) in `_variables.yml` before reader-facing commands are
  written, and say exactly where each file is saved. Each script has a
  placeholder `--account=<project>` line with a comment for Nova.

### Plots

- None required. Optional (decide in drafting): one precomputed ggplot
  of requested vs used memory for the four array tasks and the
  successful jobs only (log scale, Okabe-Ito, units GB), from captured
  `sacct` output; script `scripts/ch10_requested_vs_used.R`. A job
  killed for memory is not plotted as if its recorded peak were its
  need.

### Animation (manim)

- None. The job lifecycle is a sequence of states the reader steps
  through (stepped SVG); backfill is "change an input, see the result"
  (Observable JS).

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | the five goals above |
| 1 | Key idea | Real work runs as jobs: a script plus a resource request, started by the scheduler when a node is free, whether or not you are logged in. |
| 3 | Misconception | `space-means-room` |
| 3 | Pitfall | Moving thousands of small files on network storage is slow; run big moves as a job or with `rsync` in tmux (observed: 67,000 files). |
| 4 | Tip | Load a named version, inside the job script. |
| 5 | Pitfall | Lines pasted with `srun` run on the login node after the session ends. |
| 5 | Misconception | `closing-tab-ends-session` (OnDemand sessions are jobs). |
| 6 | Key idea | A job script is a bash script; `#SBATCH` lines are comments to bash and instructions to `sbatch`. |
| 6 | Misconception | `job-runs-in-my-shell` |
| 7 | Misconception | `ask-big-to-be-safe` |
| 7 | Misconception | `cpus-sets-threads` |
| 8 | Misconception | `pending-means-broken` |
| 8 | Background | Reading `ExitCode` `a:b` (exit status : signal); `COMPLETED` means exit 0, not a correct result. |
| 10 | Pitfall | The header row and the task past the last row (`awk` exits 0). |
| 13 | Misconception | `run-on-login-node` (closing the thread from Chapter 1). |

Spread §6–§8 so no screen has more than three (the backfill figure sits
between the two misconceptions of §7).

### Self-checks and exercises (§4)

- **Self-checks** (one per concept section, answer folded):
  - §2: `sinfo` says 60 days for a partition but the site's guide says
    3 weeks. How do you find which limit applies to **your** job?
    (Look at your association's QOS and its limits, or submit a test
    and read the `QOS=` field and any pending reason; the strictest
    limit wins.)
  - §3: Your project has 400 GB free but an install fails with "Disk
    quota exceeded". Two possible causes? (A file-count limit; or it is
    writing into home.)
  - §4: `samtools --version` prints different versions in your shell and
    in your job. Two reasons? (A module loaded in one and not the
    other; `pixi run` in one and the bare command in the other.)
  - §5: Your laptop sleeps during an `srun` shell and while a batch job
    runs. Which can you rely on afterwards? (The batch job; don't rely
    on the interactive shell having survived.)
  - §5 (ProxyJump): Yesterday `ssh <allocated-node>` worked through
    `ProxyJump nova`; today the same command fails. Two likely reasons?
    (The allocation ended or was cancelled, so you no longer hold that
    node; or today's allocation is on a different node and the `Host`
    block still names yesterday's. `squeue -u $USER`.)
  - §6: You move `#SBATCH --mem=8G` below `set -euo pipefail`. What
    memory does the job get? (The site default: `#SBATCH` lines after a
    command are ignored.)
  - §7: A job asked for 16 CPUs and ran `seqkit stats -j 2`. How many
    CPUs did it use, and what should the request be? (At most 2;
    request 2, or raise `-j` to match.)
  - §8: A job's state is `FAILED`, exit code `127:0`. First guess? (A
    command or script was not found: a typo, or a missing `pixi run` or
    module.)
  - §9: `MaxRSS` 1.2 GB, `ReqMem` 32 GB, `Elapsed` 0:04:10 of a 2-day
    request, on the same input as next time. What do you request? (About
    1.5–2 GB and well under an hour.)
  - §10: With the `awk` line as written and four data rows, what do
    tasks 0, 1, and 5 read? (Task 0 the header, task 1 the first run,
    task 5 nothing, and the check stops it; so `--array=1-4`.)
  - §11: The first job of a chain fails. What happens to the second?
    (It never starts; it stays pending as `DependencyNeverSatisfied` or
    is cancelled, depending on the site.)
- **Exercises** (core: run, inspect, adapt supplied scripts; each has a
  no-cluster route):
  1. **Know your cluster.** Fill a five-row card in `NOTEBOOK.md` for
     your site: default partition and its limit, your accounts, the
     interactive partition, quota command and current use, whether
     `seff` exists. No cluster: fill it from a supplied fictional site's
     captured outputs.
  2. **Adapt the first job.** Change `jobs/01_count_reads.sbatch` to a
     smaller request (1 GB, 5 minutes) and a different job name;
     predict the new log file name, submit, confirm with `sacct`, the
     log, and `results/read_counts.tsv`. Then give the log a date: since
     `#SBATCH` lines are not expanded, do it on the command line
     (`sbatch --output="logs/%x_%j_$(date +%F).out" …`). No cluster: run
     it with `bash` and predict the log name.
  3. **Diagnose three failures.** Submit `ok`, then the three broken
     scripts; record `State`, `ExitCode`, and the key log line for each;
     fix one. No cluster: the same from supplied captured `sacct` lines
     and logs.
  4. **Right-size a request.** Run `jobs/02_stats_array.sbatch` as an
     array over four runs with a generous request; use `seff` or
     `sacct` to choose a smaller one; resubmit; record efficiency and
     queue wait (`sacct --format=JobID%20,Submit,Start`) for both in
     `NOTEBOOK.md`. Wait times depend on the queue at that moment, so
     they are recorded, not compared for a "right" answer. No cluster:
     supplied captured `sacct` tables for both runs.
  5. **(Optional) Chain two steps** with `--dependency="afterok:$jid"`,
     then make the first fail and see what your site does with the
     second.
  6. **(Optional) Use temporary space.** Add §3's staging block to a
     copy of the array script so each task works in its own temporary
     folder and copies `stats_<run>.tsv` back; confirm the result and
     that the folder is gone. The aim is the habit; with tiny files
     the time will not change.

## Examples and data

- **Toy examples:** the four §8 scripts (no data); the backfill figure
  (simulated); captured `sacct` tables and logs for the no-cluster
  path; a fictional site card for exercise 1.
- **Running dataset:** the book's two files, `SRR6357070_1.fastq.gz`
  and `SRR6357070_2.fastq.gz` (50,000 reads each, in `data/raw/` with
  `checksums.md5` from Chapter 3), for §6–§9. For the array (§10): four
  rows in `data/meta/reads.tsv`. Decided (*Decisions* 3): add three more paired-end
  runs of the nf-core fixture (read 1 and read 2, so `reads.tsv` stays
  complete). This is a project change, done as one supplied step:
  - temporarily make `data/raw/` writable, download from the pinned
    `testdata-url`, add the files to `checksums.md5`, run `md5sum -c`,
    and write-protect it again (Chapter 3's routine). Recommended
    route: do this in the **laptop** project, then send it with
    Chapter 9's `rsync` through the DTN and run `md5sum -c` on the
    cluster ("data still moves with rsync", Chapter 9); this is how the
    Part 4 check ran on Nova (rsync sent only the new files; all 8
    `OK`). Downloading on a login node is the alternative, if the site
    allows it;
  - add one row per run to `reads.tsv` (and to `samples.tsv` for any new
    sample) and to `data/README.md` (source, accession, license,
    checksums);
  - note that Chapter 8's `01_count_reads.sh` counts every file in
    `data/raw/`, so its `results/read_counts.tsv` grows from 2 to 8 rows
    after this step; the chapter's check (§6, Outcome) is run **before**
    the download, or its expected output says 8 rows.
  **Verified 2026-11-23** against `samplesheet/v3.10/samplesheet_test.csv`
  at the pinned commit: the fixture's other paired-end runs are
  SRR6357071 (label `WT_REP1`, the same label as SRR6357070: a second
  run, which is why runs are the key), SRR6357072 (`WT_REP2`), and
  SRR6357076 (`RAP1_IAA_30M_REP1`); SRR6357073–75 are single-end in the
  samplesheet. Downloaded from `testdata-url` + `/testdata/GSE110004/`;
  every file has 50,000 reads and read 1 and 2 names match:

  | File | Bytes | MD5 |
  |:-----|------:|:----|
  | `SRR6357071_1.fastq.gz` | 2,189,243 | `fd11dc240712f88f1f800656fc59b6ab` |
  | `SRR6357071_2.fastq.gz` | 2,183,711 | `3325feca06747fa80e34daed0dc57de4` |
  | `SRR6357072_1.fastq.gz` | 2,148,269 | `63534a634de5efa0273fa812932b0ed1` |
  | `SRR6357072_2.fastq.gz` | 2,167,239 | `4c7fb08dc831bc372bb6e827182f6ff7` |
  | `SRR6357076_1.fastq.gz` | 2,268,588 | `e026fe5743035e52b7b40606b4c05fba` |
  | `SRR6357076_2.fastq.gz` | 2,250,281 | `00377e768cfd005fb8556d17fd2ee239` |

  SHA-256 values (the book's record) go into `data/README.md` with
  these rows when the chapter is drafted.
- **Where commands run:** laptop (only `ssh`, and the no-cluster path);
  login node (`sinfo`, `sbatch`, `squeue`, `sacct`, `seff`, `module`,
  quotas, editing job scripts); compute node (everything inside a job
  or an `srun` shell, including the first test of a job script).

## Misconceptions

New entries, added to `misconceptions.yml` on 2026-11-23 when the plan was agreed (with `10-hpc-slurm` added to `more-cores-faster` and `no-error-means-correct`):

- `ask-big-to-be-safe`: "Asking for lots of memory and time is the safe
  choice." Reality: a big or long request can wait longer, because the
  scheduler can fit smaller, shorter jobs into gaps; resources you hold
  but do not use while the job runs are unavailable to others and can
  count toward your group's usage. Measure a test run and add a margin.
  Probe: two identical jobs, one asking for 2 hours and one for 3 days:
  which **may** start first, and why? [§7 callout, `fig-backfill`]
- `cpus-sets-threads`: "If I ask SLURM for 8 CPUs, my tool uses 8."
  Reality: SLURM reserves CPUs; the tool starts as many threads as its
  own option says (seqkit: 4 by default, whatever was reserved). Pass
  `$SLURM_CPUS_PER_TASK` to the tool. Probe: `--cpus-per-task=8` and
  `seqkit stats` with no `-j`: how many threads does seqkit use?
  [§7 callout, `fig-resource-box`]
- `pending-means-broken`: "My job is pending, so something is wrong."
  Reality: `Priority` and `Resources` are normal waiting; only some
  reasons (a limit the request breaks) need a fix. Read the reason
  column. Probe: your job shows `(Priority)` after 20 minutes; what do
  you do? (Wait; check `squeue --start`; ask if hours pass.) [§8
  callout, `tbl-pending-reasons`]
- `space-means-room`: "If my quota shows free space, I can keep making
  files." Reality: many systems also limit the number of files; an
  environment is about 15,000 files, a pipeline's work folder can be
  millions. Count with `find … -type f | wc -l`, and read the site's own
  file count where it gives one. Probe: `Disk quota exceeded` with 400
  GB free: what do you check? [§3 callout]
- `job-runs-in-my-shell`: "A job sees my terminal as it is now."
  Reality: it runs later, on another node, with a copy of the
  environment from when you submitted, starting in the folder you
  submitted from, with no terminal; scripts it calls are read when it
  starts. Probe: you `cd` elsewhere after `sbatch`; where do the job's
  relative paths point? [§6 callout and self-check]

Existing entries revisited (add `10-hpc-slurm` where missing):
`run-on-login-node` (closed in §13), `cluster-faster-computer` (§1: many
computers behind a queue), `ram-is-disk` (§7 memory vs §3 storage),
`more-cores-faster` (§7, with `cpus-sets-threads`),
`closing-tab-ends-session` (§5), `closed-window-decides` (§5–§6),
`last-line-is-the-error` (§8), `cluster-is-backed-up` (§3),
`errors-go-to-file` (§6: `--output` holds both streams unless `--error`
is set), `no-error-means-correct` (§6 and §8: `COMPLETED` is not a
correct result).

## Links to other chapters and books

- Builds on: Chapters 1–9 (see *What this chapter builds on*);
  Chapter 9's `fig-proxyjump`, `~/.ssh/config` aliases, and keys for
  §5's compute-node connection.
- Leads to: Chapters 12–13 (R and Python scripts submitted the same way);
  Chapter 16 (`samtools sort -@ "$threads" -T "$work"`); Chapter 23
  (environments vs modules in depth); Chapter 24 (Apptainer in jobs;
  `APPTAINER_CACHEDIR` already set by Nova and Ceres); Chapter 25 (why
  workflow managers, after §11's chain); Chapter 26 (nf-core on SLURM:
  Nextflow submits the jobs; `work/` and file counts); Chapter 35
  (threads, profiling, GNU parallel inside one job); Chapter 37 (GPUs);
  Appendix A (site details).
- Other books: Genomics and Transcriptomics run every heavy step as a
  job and assume readers can read a job's records; they link here.

## Official links to include

- SLURM documentation (SchedMD): [quick
  start](https://slurm.schedmd.com/quickstart.html),
  [`sbatch`](https://slurm.schedmd.com/sbatch.html) (incl.
  `--kill-on-invalid-dep`), [`srun`](https://slurm.schedmd.com/srun.html),
  [`salloc`](https://slurm.schedmd.com/salloc.html),
  [`squeue`](https://slurm.schedmd.com/squeue.html),
  [`sacct`](https://slurm.schedmd.com/sacct.html) (field meanings),
  [`scancel`](https://slurm.schedmd.com/scancel.html),
  [`sinfo`](https://slurm.schedmd.com/sinfo.html), [job
  arrays](https://slurm.schedmd.com/job_array.html), [resource
  limits](https://slurm.schedmd.com/resource_limits.html), [job reason
  codes](https://slurm.schedmd.com/job_reason_codes.html), [job exit
  codes](https://slurm.schedmd.com/job_exit_code.html), [CPU
  management](https://slurm.schedmd.com/cpu_management.html),
  [scheduling configuration
  (backfill)](https://slurm.schedmd.com/sched_config.html#backfill-scheduling),
  [multifactor priority and fair
  share](https://slurm.schedmd.com/priority_multifactor.html).
- `seff` in SLURM's
  [contribs](https://github.com/SchedMD/slurm/tree/master/contribs/seff)
  (*to check* the path at drafting).
- [Lmod documentation](https://lmod.readthedocs.io).
- [SeqKit usage](https://bioinf.shenwei.me/seqkit/usage/) (thread
  default, `SEQKIT_THREADS`; check against the pinned version).
- Sites: [SCINet SLURM guide](https://scinet.usda.gov/guides/use/slurm),
  [SCINet scratch guide](https://scinet.usda.gov/guides/use/scratch),
  [Ceres and Atlas
  differences](https://scinet.usda.gov/guides/resources/CeresAtlasDifferences),
  [MSU Atlas docs](https://docs.hpc.msstate.edu/), [ISU SLURM
  page](https://research.it.iastate.edu/slurm), [ISU file storage
  (TMPDIR)](https://research.it.iastate.edu/file-storage); full list in
  Appendix A.
- [Open OnDemand](https://openondemand.org) (sessions are jobs).
- All links rechecked at drafting (several were added from the review).

## Further reading (candidates)

To verify with scite and fetch BibTeX from the DOI before adding:

- HPC Carpentry, *Introduction to High-Performance Computing*
  (hpc-carpentry.github.io/hpc-intro): a hands-on lesson on the same
  ground. Official Carpentries lesson.
- SchedMD, *SLURM quick start user guide*: the reference behind every
  command here.
- Yoo, Jette, and Grondona (2003), "SLURM: Simple Linux Utility for
  Resource Management" (JSSPP, LNCS 2862): where SLURM's design comes
  from. *DOI to fetch.*
- Lmod paper (*to find*; only if a citable one exists).
- Your site's own SLURM page (Appendix A): the authority for limits.

## Consistency with the Chapter 8 and 9 drafts (2026-11-23)

Both drafts read against this plan after the cluster checks. The file
and script names match (`src/01_count_reads.sh`,
`src/02_gtf_summary.sh`, `src/run_all.sh`, `results/read_counts.tsv`,
`logs/`), and every forward link has a home here (listed under *What
this chapter builds on*). Changes made: the two "(planned)" entries
now describe the drafts; §3 names the `bioinf-shared/references`
folder; §5 shows `pixi install --locked` in an interactive job, as
Chapter 9 promised; §6 opens by noting that Chapter 9's test ran on
the login node; §11 links back to `run_all.sh` and to `02`/`03`
running side by side; §12 no longer calls the OnDemand `--gres` name
correct. Nothing needs changing in the drafts.

## Site differences observed (2026-11-23)

From `chapter_10_checks.md` (Ceres and Nova: Parts 0–3; Atlas: the
parts where it may differ; Nova: Part 4, the real first job and
array). The chapter's text, `tbl-sites-slurm`, and
the pitfall callouts are written from this table. User and project
names are placeholders.

::: {.wide-table}
: Where Ceres, Atlas, and Nova differ for Chapter 10 (*observed*). {#tbl-ch10-site-diffs}

| Topic | Ceres | Atlas | Nova | Chapter section |
|:--|:--|:--|:--|:--|
| Real time limit and its source | 21 days, from the `ceres` **QOS** the partition attaches (`sinfo` shows 60 days) | 14 days, from the `normal` **QOS** (`sinfo` shows `infinite`) | 31 days, from the **partition** (default QOS `normal` sets none) | §2 |
| Over-long request | refused: `QOSMaxWallDurationPerJobLimit` | refused: same message | refused: `Requested time limit is invalid (missing or exceeds some limit)` | §2, §8 |
| Default time / memory if left out | 2 h / 2,000 MB per CPU | 2 h / 7,686 MB per CPU | 4 h / 3,800 MB per CPU | §7 |
| `-A <account>` needed | yes | yes | no (default account) | §2, §6 |
| `salloc` puts you on | the compute node | **the login node** (`srun` reaches the node) | the compute node | §5 (pitfall) |
| Batch job's `TMPDIR` | `/tmp`, private to the job (`namespace/tmpfs`), 1.5 TB NVMe | **`/local/scratch/<user>/<jobid>`**, per job, 1.7 TB NVMe; `/tmp` is the node's shared one | as Ceres | §3 |
| Failed `afterok` chain | second job waits forever, `DependencyNeverSatisfied`; `scancel` it | **cancelled automatically** (`kill_invalid_depend`) | as Ceres | §11 |
| `MaxArraySize` | 10001 | 10001 | **1001** | §10 |
| GPUs | none | four GPU partitions (`gpu-a100`, `gpu-a100-mig7`, `gpu-l40s`, `gpu-v100`); MIG slice `--gres=gpu:nvidia_a100_1g.10gb:1` or `gpu:1` (the OnDemand form's `a100_1g.10gb` is refused) | GPU nodes **in the default partition**; `--gres=gpu:<type>:1` | §12 |
| `samtools` modules | 1.16.1, 1.17 (3 trees) | not checked | 1.16.1, 1.19.2, 1.23.1 with hash suffixes (9 trees, dated) | §4 |
| `.pixi` on disk | 1.3 GB | 1.3 GB | 813 MB (compressed `/work`); same 13,001 files everywhere | §3 |
| A 1-CPU request gets | not checked (2-CPU jobs bill as `billing=1`) | not checked | **2 CPUs**: `CR_CORE_MEMORY`, `ThreadsPerCore=2` | §7 |
| Login node | 32 CPUs, 376 GB | 48 CPUs, 376 GB | 64 CPUs, 188 GB | §1 |
:::

**The same on all three** (one capture can stand for all): a batch job
starts in the submit folder and sees exported variables, `pixi`, and
`module`; `seff` and GNU `time -v` exist; inside a job `nproc` shows
the allocation and `free` the whole node; `salloc`'s `exit` releases
the job; the failure states (`OUT_OF_MEMORY 0:125` with `Killed` and
an `oom_kill event` line, `TIMEOUT` on the allocation line with
`.batch` `CANCELLED 0:15`, `FAILED 127:0`) on Ceres and Nova; CPU
efficiency about 95–97% with 4 of 4 CPUs busy and 24% with 1 of 4.

**What this means for the text:** teach `scontrol show partition` and
`sacctmgr show qos` as the way to find *your* limit, since the number
in `sinfo` is wrong on two of three sites; always set `--time` and
`--mem`; always use `$TMPDIR`, never a hard-coded `/tmp`; after
`salloc`, check `hostname`; after a failed chain, check `squeue`.

## Checks to capture

**Status 2026-11-23:** checks 1–15 done, results in
`chapter_10_checks.md` (7 and 9 with the real job and array on Nova).
Check 16 (ProxyJump to a held node) done the same day on Nova from the
Mac (§5 updated; VS Code Remote-SSH and Windows not tried). §3's
staging block also ran as a job on Nova the same day (§3 updated).
**All checks done.**

Written as the brief for `chapter_10_checks.md` (on Nova and Ceres; Atlas where the
answer may differ). User and project names replaced in anything
committed (`_private/` holds the real ones). Run as one end-to-end pass
once the job scripts, the array manifest, and the staging block are
final.

1. `hostname; nproc; free -g` on the login node; inside `srun` the same
   plus `echo "$SLURM_CPUS_PER_TASK"` and the `scontrol show job`
   allocation lines.
2. Applicable limits: `sacctmgr show assoc user=$USER
   format=account,partition,qos,defaultqos`, `sacctmgr show qos
   format=Name,MaxWall,MaxTRESPU%30` (may be denied), and the `QOS=` of
   a real job; does a 30-day request on Ceres's default partition get
   rejected at submission or pend, and with which reason?
3. **Inside a batch job:** `echo "$TMPDIR"`, `ls -ld "$TMPDIR"`, free
   space there (`df -h "$TMPDIR"`), and whether a file made there is
   visible from a second job on the same node (is it per job?). Atlas
   too.
4. Inside a batch job: `type module` (is the `module` command defined
   in a non-interactive batch shell?), `module load` of one named
   version.
5. `command -v seff`; `scontrol show config | grep -i -E
   'MaxArraySize|DefMemPerCPU|DefMemPerNode|KillOnBadExit'`;
   `command -v /usr/bin/time` and whether `-v` works.
6. `module spider samtools`; `module avail` header lines.
7. The §6 job: test inside `srun`, `sbatch`, `squeue` states seen, both
   logs, `results/read_counts.tsv`, `sacct`, `seff`.
8. The four §8 jobs: `sacct` lines (allocation and steps) and the key
   log line for each; exact OOM behaviour per site.
9. The array of four (after the data step): dry-run output for tasks
   1–5, `squeue` display, logs, results, `sacct -j`.
10. A dependency chain, and what the site does when the first job fails
    (pending as `DependencyNeverSatisfied`, or cancelled).
11. Whether a job starts in the submit folder and sees `~/.pixi/bin` on
    `PATH` with the default `--export` (expected yes).
12. `find .pixi -type f | wc -l` in the cluster project, beside the
    site's own file count where shown.
13. GPU partitions and `--gres` form on Nova and Ceres (`sinfo -o "%P
    %G"`; no job needed).
14. `salloc` then `exit` on each site: is the allocation released, or
    left for `scancel`?
15. One longer captured job (minutes, several threads) for the CPU
    efficiency example in §7 and §9.
16. **ProxyJump to a held node (Nova; Ceres/Atlas if allowed):** ISU's
    `salloc … sleep infinity` line as published; the `NODELIST` name
    format; from the laptop `ssh -J nova <node> hostname` with **no**
    `ForwardAgent` or `StrictHostKeyChecking no` (does the host-key
    question appear, and does it work on the VPN with a key?); the
    message when SSH-ing to a node you do not hold; VS Code Remote-SSH
    to the node from Mac and Windows; `scancel` and an empty `squeue`.

## Drafting notes (2026-11-23)

First draft in `chapters/10-hpc-slurm.qmd`, with five new figures
(`storage-tiers`, `sbatch-anatomy`, `job-lifecycle` (stepped),
`resource-box`, `job-array`) and `fig-backfill` (Observable JS). Every
captured output is from the check sessions (`chapter_10_checks.md`),
quoted verbatim apart from placeholders; laptop outputs were rerun on
the Mac the same day. Where the draft differs from this plan:

- **No `jobs-url`.** Readers save each job script from the page, as
  Chapter 3 does for `src/01_count_reads.sh`: written on the laptop and
  sent with Chapter 9's `rsync`, or written on the login node with nano
  or vim. `_variables.yml` is unchanged. The four §8 scripts are shown
  in full in a tabset, each with a `project=` line.
- **"Line", not "row", for the array manifest:** task *n* reads line
  *n* + 1 of `reads.tsv` (line 1 is the header), so "no row 5" (the
  script's message, data rows) and the figure's line numbers agree.
  The script comment changed to match; the code is as tested.
- **`${VAR:-default}` and `${VAR:?message}`** are explained in place
  (§3 and §6): Chapter 8's `tbl-expansions` does not list them.
- **§8's `Killed` line** shows `line <n>`: the test scripts had no
  `--account` or `project=` line, so their line number differs from the
  chapter's scripts.
- **§9's capture** is Ceres's stand-in count (2 CPUs), as the plan
  says; §6 uses Nova's real first job.
- **§11** suggests `run_all.sh` in one job as the simplest route, and
  makes `jobs/02_gtf_summary.sbatch` exercise 5 instead of a supplied
  file.
- **Exercise 1's no-cluster card** is a fictional site (`main*`/`short`,
  a 7-day QOS on a 30-day partition, no `seff`); exercise 3 adds a
  three-job captured table for the no-cluster route, written for the
  book.
- **Spelling:** "SLURM" throughout, as in Chapters 1–9 (also in
  `misconceptions.yml`).
- **Not checked in a browser yet:** `fig-backfill`'s logic was tested in
  Node (the three cases in `tbl-backfill-cases` and four more); the page
  itself still needs a look over `http://`.
- `data/README.md` has the three new runs (MD5 and SHA-256);
  `references.bib` has `yoo2003slurm` (DOI checked with scite),
  `hpccarpentry2026intro`, `schedmd2026quickstart`, `lmod2026docs`.

## Austin's notes

-

## Change from Chapter 9 (2026-11-22)

Chapter 9's plan (decision 11, Austin) made `ProxyJump` recognition
only there and moved the live route here. Added: §5's four-step
acquire → find → connect → release block with ISU's extra options
explained, a self-check, check 16, and the *builds on* note. No new
section, figure, or table; `fig-proxyjump` is Chapter 9's. Appendix A
keeps the per-site config block and links to §5.

## Decisions (Austin, 2026-11-22)

All six open questions answered; each took the proposed option.

1. **`sacct` first.** The chapter teaches `sacct` fields as the main way
   to measure a job, since every site has it; `seff` appears as "if your
   site has it". All three have `seff` (check 5, *observed*
   2026-11-23), so that sentence says "if your site has it; Ceres,
   Atlas, and Nova do".
2. **Job scripts wrap Chapter 8's scripts.** The §6 job runs `pixi run
   bash src/01_count_reads.sh`, and the check reads
   `results/read_counts.tsv`. §10's array script calls seqkit directly,
   because it works one run at a time and needs `-j`. Final wording waits
   until Chapter 8's script is settled.
3. **Three more paired-end fixture runs** for the array (pinned,
   checksummed, a few MB), added as the supplied project step in
   *Examples and data*. Accessions verified 2026-11-23:
   SRR6357071, SRR6357072, SRR6357076 (*Examples and data*).
4. **§11 (chains) and §12 (GPUs) stay** as short sections labelled
   overview inline; the chain exercise is optional. Chains stay here
   because Chapter 8 promised them.
5. **`fig-backfill` is built in the first draft.**
6. **Email notifications: table only,** one row in `tbl-sbatch-options`
   noting that it is site-specific; no demonstration.

## Open questions

- None at the moment. Remaining unknowns are site facts, listed under
  *Checks to capture*.

## Review response (2026-11-22)

Response to `chapter_10_codex_review.md`. All eight corrections and the
teaching points were accepted; the plan above now reflects them:

1. First job: local fallbacks for `SLURM_*` (the plain-`bash` route
   now works), one log name (`01_count_reads`) throughout, `mkdir -p
   logs` before `sbatch`, `#!/usr/bin/env bash`, `--nodes=1
   --ntasks=1`, first test inside an interactive job, and "`#SBATCH`
   lines are not expanded" for the dated-log exercise.
2. Array: the self-check answer was wrong and is fixed (`--array=1-4`
   with the header at row 1); the manifest is Chapter 3's
   `data/meta/reads.tsv`, keyed by run, with an empty-row and
   readable-file check, unique outputs, and all task numbers dry-run
   first; "can run independently" replaces "at the same time on
   different nodes"; the `%5` typo fixed; the data download is spelled
   out as a project change.
3. Temporary space: site facts attributed to SCINet's and ISU's pages;
   the observed `TMPDIR=/tmp` is marked interactive-only, batch
   behaviour *to capture*; a complete staging block (own folder,
   absolute output path, `sort -T`, pixi from the project, copy-back
   caveat, bounded `du`); `find .pixi` run in the cluster project and
   distinguished from site file counts.
4. Failure jobs: explicit `--manifest-path`, an `ok` job first, OOM
   behaviour a site capture and cluster-only, the typo defined (`127`),
   and allocation and step lines read together with the log.
5. Measurement: no promised efficiency from the toy job (a captured
   longer job instead), the `sacct` lines and units explained, "peak +
   25%" limited to comparable successful runs, wait times recorded not
   graded, `/usr/bin/time -v` labelled GNU/Linux.
6. Threads and scheduling: seqkit's default of 4 and `SEQKIT_THREADS`;
   "Slurm CPU"; `--ntasks` described as counting tasks; backfill as a
   possibility; fair share based on use, not the requested time.
7. Limits: the Ceres 3-week QOS marked *inference*; applicable QOS to
   capture; submission-time rejection mentioned; `ReqNodeNotAvail`
   broadened; `AssocGrpCpuLimit` spelling; dependency failure
   site-dependent, quoted `"afterok:$jid"`.
8. Wrapper and model: the §6 job wraps Chapter 8's `01`; the check reads
   the result file and explains the two logs; `COMPLETED` is not a
   correct result; three-column process/interactive/batch table; the
   `salloc` release step and Chapter 9's ProxyJump route.

Also taken: a minimum route through the chapter; no-cluster material
for every required exercise; allocation lines beside `nproc`/`free`;
`sort -T` to keep Chapter 6's promise; module setup checked in a batch
shell; a pinned download location for job scripts; "scripts called by
the job are read when it starts"; colour roles corrected (`given` for
data only, neutral for storage and CPUs, outcomes labelled in text and
shape).

**Where this plan differs from the review (minor):**

- **Section order kept.** The review suggests moving the reference
  material out of the reader's way; the plan keeps the thirteen
  sections in order and adds a stated minimum route plus reference
  blocks instead, because storage (§3) has to come before the first job
  writes logs and results, and Chapter 3 promised it here.
- **`warn` kept for the two "limit exceeded" panels** of
  `fig-resource-box` and the purge icon: under STYLE-GUIDE §2 these are
  pitfalls, which is what `warn` is for. Job outcomes in
  `fig-job-lifecycle` use labels and icons, not `warn`, as the review
  asks.
