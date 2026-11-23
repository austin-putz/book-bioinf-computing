---
title: "Chapter 10: Hands-on checks for Austin"
subtitle: "What to run on Ceres, Nova, and Atlas before Chapter 10 is drafted"
date: 2026-11-22
---

These checks answer the *to capture* items in `chapter_10.md` (its
*Checks to capture* list, numbered 1–15 there; the same numbers appear
in brackets below). They need a cluster login: nothing here can be done
from the laptop.

**What is already done**, so you don't repeat it (all in Appendix A):

- `sinfo -s` on all three; your accounts (`sacctmgr … show assoc`);
  `srun --pty` works on all three (Ceres and Atlas need `-A`, Nova does
  not); compute nodes reach the internet; `exit` ends an `srun` job;
  the settings Ceres and Nova print on arrival (`TMPDIR=/tmp`,
  `TMOUT=5400`); the book environment is installed on all three
  (2026-11-22).

**How to work.**

- **Which clusters.** Do everything on **Nova** and **Ceres**. On
  **Atlas** do only the parts marked *Atlas too* (where it may differ).
- **One throwaway folder per cluster**, beside your book folder in
  project storage: `bioinf-computing-ch10-checks`. Everything is
  written there, and you delete it at the end. Nothing here edits a
  startup file or the book folder.
- **Small jobs only.** Every job asks for at most 4 CPUs, 2 GB, and 15
  minutes, and most finish in seconds. The one deliberate
  out-of-memory job is capped at 500 MB by Slurm.
- **Paste `srun` and `salloc` lines on their own** and wait for the
  prompt before typing more (lines pasted with them run on the login
  node afterwards; observed 2026-11-22).
- **Recording:** paste what each step prints into the chat. Claude
  fills in your real paths from `_private/` when giving you commands,
  and replaces user and project names with placeholders before
  anything goes into this file.

::: {.callout-tip}
## Ceres status (2026-11-23): complete
Parts 0–3 all done on Ceres in one session (results under each part
and in the table). Part 4 waits for Chapters 8 and 9.
:::

::: {.callout-tip}
## Nova and Atlas status (2026-11-23): complete
Nova: Parts 0–3 (one probe instead of two, since `NamespaceType`
already answered the per-job question). Atlas: the *Atlas too* parts
(1.1, 1.3, 2.2, 3.1) plus 3.5 and 3.6, because its settings differ.
Site differences found: Atlas's `salloc` stays on the login node;
Atlas's `TMPDIR` is `/local/scratch/<user>/<jobid>` (no `/tmp`
namespace); Atlas cancels jobs with a failed dependency; each site's
time limit comes from a different place (Ceres QOS 21 days, Atlas QOS
14 days, Nova partition 31 days); Nova's array limit is 1001; Nova's
GPUs are in the default partition. Everything else matched.
:::

**Priority** if time is short:

1. Part 3.1 (the probe job): what a batch job really sees. *Atlas too.*
2. Part 3.3 (the four failure jobs).
3. Part 1 (login-node facts).
4. Everything else.

---

## Part 0: Set up (each cluster, each session)

On the **login node**. Set three variables; the second line differs by
site. `export` matters for `PROJ`: the batch jobs read it, which is
itself one of the checks (3.1).

```bash
# Ceres and Atlas:
export PROJ=/project/<project>/<user>/bioinf-computing
ACCT="-A <project>"
# Nova:
export PROJ=/work/<group>/<netid>/bioinf-computing
ACCT=""
```

Then, on every cluster:

```bash
CHK="$(dirname "$PROJ")/bioinf-computing-ch10-checks"
mkdir -p "$CHK/logs" "$CHK/results" && cd "$CHK"
ls "$PROJ/pixi.toml" && pixi --version
[ -f SRR6357070_1.fastq.gz ] || curl -fLO https://raw.githubusercontent.com/nf-core/test-datasets/9dd6d014f560e182047992834a8d267214fbccd1/testdata/GSE110004/SRR6357070_1.fastq.gz
ls -l
```

`$ACCT` is written without quotes in the `sbatch` and `srun` lines
below on purpose: on Nova it is empty and disappears; on SCINet it
becomes the two words `-A <project>`. (Options given to `sbatch` on the
command line override the script's own `#SBATCH` lines, so the job
scripts below stay the same on every site.)

If you log out and come back, run Part 0 again (the variables are gone,
the folder is not).

---

## Part 1: Login-node facts (no jobs)

### 1.1 Machine, limits, and tools [checks 1, 2, 5, 6, 13] *Atlas too*

```bash
hostname; nproc; free -g | head -n 2
sacctmgr -n show assoc user=$USER format=account%30,partition%15,qos%40,defaultqos%15
sacctmgr -n show qos format=Name%25,MaxWall,MaxTRESPU%40 2>&1 | head -n 20
command -v seff || echo "no seff"
scontrol show config | grep -i -E 'MaxArraySize|DefMemPerCPU|DefMemPerNode|KillOnBadExit|MaxJobCount'
/usr/bin/time -v true 2>&1 | head -n 3
sinfo -o "%P %G" | sort -u
sinfo -N -o "%N %c %m %G" | head -n 5
```

What it answers: the login node's size (to compare with 2.1); which
QOS applies to your account and its limits (the second line may be
refused, that is an answer too); whether `seff` exists; the array size
limit and default memory; whether GNU `time -v` works; GPU partitions
and their `--gres` names.

::: {.callout-note}
## Ceres result, 2026-11-23: Part 0 and 1.1 done
Part 0 worked: throwaway folder made (`drwxr-s---`, project group,
as Chapter 7 found), `pixi.toml` found, pixi 0.84.2, test file
downloaded (2,239,317 bytes).

| Item | Ceres |
|:--|:--|
| login node | `ceres-login-1`: `nproc` **32**, `free -g` **376 GB** total (42 used, 331 cache) |
| association | two accounts, partition column blank (all partitions); QOS list `400thread,ceres,debug,memlimit,sandbox,+` (cut off by the width); default QOS column blank |
| QOS limits (`sacctmgr show qos`, allowed) | `ceres` **21-00:00:00**, `cpu=4000,mem=36T,node=32`; `normal` 21 days; `debug` 30 min, `cpu=288`; `sandbox` 2 h, `node=1`; `long` 60 days; `large` 1 day; `scavenger` 21 days; others `400thread`, `memlimit`, `limitless`, `galaxy`, `spff` |
| `seff` | `/usr/bin/seff` |
| `scontrol show config` | `MaxArraySize = 10001`, `MaxJobCount = 60000`, `DefMemPerNode = UNLIMITED`, no `DefMemPerCPU` line (cluster-wide; partition default checked next), `KillOnBadExit = 0` |
| GNU `time -v` | works (`Command being timed: "true"`) |
| GPUs | **none**: `sinfo -o "%P %G"` shows `ceres*` and `scavenger`, both GRES `(null)` |
| a node | `ceres20-compute-*`: 96 CPUs, 752,000 MB (about 734 GB) |

**For the plan:** the 3-week limit on the 60-day `ceres` partition is
the `ceres` **QOS** (`MaxWall 21-00:00:00`), now *observed* rather
than *inference*, provided that QOS is the one applied to jobs
(confirmed by the `QOS=` field in 2.1 and by 3.6).

**Follow-up (same day):** `sacctmgr -n -P show assoc …` gave the full
list: `400thread,ceres,debug,memlimit,sandbox,scavenger`, **default
QOS blank**, for both accounts. `scontrol show partition ceres`:
`QoS=ceres` (the partition attaches the `ceres` QOS to every job in
it, which settles where the 21 days comes from), `AllowQos=ceres,
memlimit,limitless,sandbox,spff`, `DefaultTime=02:00:00`,
`MaxTime=60-00:00:00`, **`DefMemPerCPU=2000`** (MB),
`MaxMemPerNode=UNLIMITED`. So a Ceres job that leaves out `--time`
gets 2 hours and one that leaves out `--mem` gets 2,000 MB per CPU.
:::

::: {.callout-note}
## Nova result, 2026-11-23: Part 0 and 1.1 done
Part 0 worked: folder `drwxrwsr-x` with the lab group (umask `0002`,
as Chapter 7 found), pixi 0.84.2, test file downloaded.

| Item | Nova |
|:--|:--|
| login node | `nova-login-1`: `nproc` **64**, **188 GB** |
| association | `<group>`: QOS `normal,scavenger`, **default QOS `normal`**; `<group>-scavenger`: `scavenger` only |
| QOS limits | `normal`, `scavenger`, two project QOS: **no `MaxWall`**; `instruction` `cpu=648,gres/gpu=11,mem=3888500M`; `jail` 1 min |
| `seff` | `/usr/bin/seff` |
| `scontrol show config` | **`MaxArraySize = 1001`**, `MaxJobCount = 100000`, `DefMemPerNode = UNLIMITED`, **`NamespaceType = namespace/tmpfs`**, `TmpFS = /tmp`, **`DependencyParameters = (null)`**, `KillOnBadExit = 0` |
| partition `nova` | `AllowQos=normal`, `QoS=N/A`, **`DefaultTime=04:00:00`**, `MaxTime=31-00:00:00`, **`DefMemPerCPU=3800`**, `MaxMemPerNode=UNLIMITED` |
| GNU `time -v` | works |
| GPUs | **in the default `nova*` partition** (also `interactive`, `instruction`, `scavenger`, `nova-arm`, `allnodes`), named by type: `gpu:a100`, `a100-pcie`, `a40`, `h200`, `gh200` (nova-arm), `l40s`, `rtx_2080_Ti`, `rtx_6000`, `rtx_pro_6000`, `v100`, `v100-sxm2-32G`; `reserved` has none |
| a node | `nova18-5`: 72 CPUs, 189,000 MB |

**For the plan:** Nova's time limit is the partition's 31 days (the
default QOS sets none), unlike Ceres where the QOS sets it. Same
per-job `/tmp` plugin and the same "a failed chain stays pending"
setting as Ceres, so the batch checks are expected to match. A GPU
request on Nova is `--gres=gpu:<type>:1` in the default partition, not
a GPU partition as on Atlas. Array limit ten times smaller than
Ceres's.
:::

::: {.callout-note}
## Atlas result, 2026-11-23: 1.1 and 1.3 done (association line to redo)
**The paste arrived damaged:** two long lines lost characters on the
way (`format=account,partition,qo` → `Unknown field 'qo'`; the
partition `grep` pattern lost `DefaultTime|MaxMemPer…`). The same
thing probably caused Nova's `>` prompt. Long lines pasted over SSH can
drop characters; short blocks are safer.

| Item | Atlas |
|:--|:--|
| login node | `atlas-login-1`: `nproc` **48**, **376 GB** |
| QOS limits | **`normal` 14-00:00:00, `cpu=1920,node=40`**; `debug` 30 min, `cpu=288`; `ood` 8 days; `sandbox` 2 h; `bigmem` 14 days, `cpu=192,node=4`; `v100`, `mig7`, `l40s` 2 days; `a100` 7 days, `mem=1500G`; `special`, `priority` no limit shown |
| `seff` | `/opt/slurm/bin/seff` |
| `scontrol show config` | `MaxArraySize = 10001`, `MaxJobCount = 30000`, `DefMemPerNode = UNLIMITED`, **`NamespaceType = (null)`** (no per-job `/tmp` plugin), `TmpFS = /tmp`, **`DependencyParameters = kill_invalid_depend`** |
| partition `atlas` | `AllowQos=ALL`, `QoS=N/A`, `Time=02:00:00` (the `DefaultTime`, matched by the damaged pattern), `MaxTime=UNLIMITED`, **`DefMemPerCPU=7686`** |
| GNU `time -v` | works |
| GPUs | `gpu-a100` `gpu:a100:8`; `gpu-a100-mig7` **`gpu:nvidia_a100_1g.10gb:56`**; `gpu-l40s` `gpu:l40s:4`; `gpu-v100` `gpu:v100:2`; `atlas`, `bigmem`, `development`, `service` none |
| a node | `atlas-0001`: 48 CPUs, 385,323 MB |

1.3: **13,001** files, **15,528** entries, **1.3G** (as Ceres).

**For the plan:** Atlas's limit is the `normal` QOS's 14 days (the
partition is unlimited). Unlike Ceres and Nova, Atlas has no per-job
`/tmp` plugin, and it **cancels** jobs whose dependency can never be
met (`kill_invalid_depend`), so 3.5 is worth running on Atlas too. The
MIG `--gres` name in `sinfo` (`nvidia_a100_1g.10gb`) differs from the
OnDemand form's (`a100_1g.10gb`).
:::

::: {.callout-note}
## Atlas follow-up, 2026-11-23: the MIG `--gres` name
`sbatch --test-only -A <project> -p gpu-a100-mig7 -t 5 --wrap=hostname`
with three `--gres` forms:

| `--gres` | Result |
|:--|:--|
| `gpu:a100_1g.10gb:1` (OnDemand form's name) | **refused**: `allocation failure: Requested node configuration is not available` |
| `gpu:nvidia_a100_1g.10gb:1` (`sinfo`'s name) | accepted: `Job <id> to start at … using 1 processors on nodes atlas-0241 in partition gpu-a100-mig7` |
| `gpu:1` | accepted (same) |

Partition: `QoS=mig7`, `DefaultTime=02:00:00`, `MaxTime=UNLIMITED`.
`srun -A <project> -p gpu-a100-mig7 -t 5 --gres=gpu:1 nvidia-smi -L`
(queued briefly): eight `NVIDIA A100-SXM4-80GB` cards listed, one
`MIG 1g.10gb Device 0` under GPU 2, the job's slice. **Answer:** use
`sinfo`'s name or plain `gpu:1`. (Appendix A does not quote the
OnDemand name, so it needs no fix.)
:::

### 1.2 Modules [check 6]

```bash
module avail 2>&1 | grep -E '^-+ ' | head
module spider samtools 2>&1 | head -n 25
```

::: {.callout-note}
## Ceres result, 2026-11-23: complete
Three module trees: `/software/el9/modulefiles`,
`/reference/containers/modulefiles`,
`/usr/share/lmod/lmod/modulefiles/Core`. `module spider samtools`:
`samtools/1.16.1`, `samtools/1.17`, with Lmod's "use the module's
full name" hint (`module spider samtools/1.17`).
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete
Nine module trees: four dated releases
`/opt/rit/el9/20250815`, `20240815`, `20240413`, `20230413`
(`…/modules/lmod/linux-rhel9-x86_64/Core`), plus
`/opt/rit/singularity/modules`, `/opt/rit/proprietary/modules`,
`/opt/hpc/modulefiles`, `/opt/rit/misc/modules`, Lmod's `Core`.
`module spider samtools`: `samtools/1.16.1-py310-d6uutpz`,
`samtools/1.19.2-py311-qlmoxzv`, `samtools/1.23.1-py313-3cgtvqh`
(Spack-style hash suffixes), and "Other possible modules matches:
`r-rsamtools`".
:::

### 1.3 File count of the book environment [check 12] *Atlas too*

```bash
cd "$PROJ" && find .pixi -type f | wc -l && find .pixi | wc -l && du -sh .pixi; cd "$CHK"
```

Regular files, then everything (files, folders, links). Nova only:
compare with the `OBJUSED` column for your name in
`/work/<group>/group_storage_usage` if you like (paste only your own
row, not other members').

::: {.callout-note}
## Ceres result, 2026-11-23: complete
`find .pixi -type f | wc -l` → **13,001** regular files;
`find .pixi | wc -l` → **15,528** entries in all; `du -sh .pixi` →
**1.3G** (as on the laptop: Ceres's project storage does not
compress, unlike Nova's `/work`).
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete
**13,001** files, **15,528** entries (identical to Ceres: same lock
file), `du -sh` **813M** (compressed `/work`).
:::

---

## Part 2: Interactive jobs

### 2.1 What the allocation says vs what the node has [check 1]

Paste this line **alone**:

```bash
srun $ACCT --cpus-per-task=2 --mem=2G --time=00:15:00 --pty bash -l
```

Once the compute-node prompt is back:

```bash
hostname; nproc; free -g | head -n 2
echo "cpus=$SLURM_CPUS_PER_TASK mem=$SLURM_MEM_PER_NODE tmpdir=${TMPDIR:-<not set>}"
scontrol show job "$SLURM_JOB_ID" | grep -E 'NumCPUs|mem=|QOS='
exit
```

Lesson to confirm: `nproc` and `free` may show the whole node, while
`SLURM_CPUS_PER_TASK` and the `scontrol` lines show your 2 CPUs and 2
GB.

::: {.callout-note}
## Ceres result, 2026-11-23: complete
`srun` printed `job … queued and waiting for resources`, then `has
been allocated resources` (seconds), then the site's arrival lines
(`TMPDIR=/tmp`, `TMOUT=5400`, `APPTAINER_TMPDIR=/tmp`,
`APPTAINER_CACHEDIR=/tmp`, the `my_quotas` hint). On
`ceres20-compute-6`:

| Line | Output | Shows |
|:--|:--|:--|
| `nproc` | **2** | the allocation (Slurm limits the job to its CPUs) |
| `free -g` | **754** GB total, 714 available | the whole node, not the 2 GB |
| `SLURM_*` | `cpus=2 mem=2048 tmpdir=/tmp` | the allocation (memory in MB) |
| `scontrol show job` | `QOS=ceres`; `NumCPUs=2 … CPUs/Task=2`; `ReqTRES=cpu=2,mem=2G,node=1,billing=1`; `AllocTRES` the same | the `ceres` QOS is applied |

`billing=1` for 2 CPUs suggests a Slurm CPU on Ceres is a hardware
thread (two per core), so 2 CPUs bill as one core (*inference*, not
needed for the chapter). `exit` printed `logout` and returned to
`ceres-login-1`.

**For the plan:** on Ceres `nproc` follows the allocation and `free`
does not, so §1's lesson is "`free` shows the node; `nproc` depends
on the site". Nova still to compare.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same pattern as Ceres)
No "queued" lines: the shell started at once, after Nova's arrival
lines (`TMOUT=5400`, `TMPDIR=/tmp`, `PTMPDIR=` (empty),
`APPTAINER_BINDPATH=/work:/work,/lustre:/lustre,/scratch:/scratch,/ptmp:/ptmp,/etc/hosts:/etc/hosts`,
`APPTAINER_TMPDIR=/tmp`, `APPTAINER_CACHEDIR=/tmp`,
`XDG_RUNTIME_DIR=/tmp`, `APPTAINERENV_SLURM_JOB_ID=<id>`). Austin's
own prompt hides the host name, so `hostname` is what shows the move.

| Line | Nova (`nova18-wide-13`) |
|:--|:--|
| `nproc` | **2** (the allocation) |
| `free -g` | **376** GB total (the node) |
| `SLURM_*` | `cpus=2 mem=2048 tmpdir=/tmp` |
| `scontrol show job` | `Account=<group> QOS=normal`; `NumCPUs=2`; `ReqTRES`/`AllocTRES` `cpu=2,mem=2G,node=1` (no `billing` term, unlike Ceres) |
| `ls -ld /tmp` | **`drwx------. 3 <netid> root 44`**: private to the job here too (one entry already inside, likely from `XDG_RUNTIME_DIR=/tmp`) |
:::

### 2.2 Does `salloc` release on `exit`? [check 14] *Atlas too*

Paste alone:

```bash
salloc $ACCT --cpus-per-task=1 --mem=1G --time=00:10:00
```

Then:

```bash
hostname
squeue -u $USER
exit
squeue -u $USER
```

What it answers: after `salloc`, are you on a compute node (Ceres) or
still on the login node (Atlas, per SCINet's differences page)? After
`exit`, is the job gone? If a job is still listed, release it with
`scancel <jobid>` and say so.

::: {.callout-note}
## Ceres result, 2026-11-23: complete
`salloc` printed `Pending job allocation …`, `queued and waiting for
resources`, `has been allocated resources`, `Granted job allocation
…`, `Nodes ceres20-compute-6 are ready for job`, then the arrival
lines. You land **on the compute node**: prompt and `hostname` show
`ceres20-compute-6`; `squeue` lists the job as `R` in partition
`ceres` with name **`interact`** (Ceres names `salloc` jobs that way).
`exit` printed `exit` and `salloc: Relinquishing job allocation …`;
back on `ceres-login-1`, `squeue` shows only the header. **Released
on `exit`; no `scancel` needed.**
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
`salloc: Granted job allocation …`, `Nodes nova21-swift-4 are ready
for job` (no "queued" lines), arrival lines; `hostname` →
`nova21-swift-4`; `squeue` → `R`, partition `nova`, name `interact`.
`exit` → `salloc: Relinquishing job allocation …`; back on
`nova-login-1`, `squeue` empty. **Compute node; released on `exit`.**
:::

::: {.callout-note}
## Atlas result, 2026-11-23: complete (differs from Ceres and Nova)
Association (redone with a short line): both accounts QOS
`debug,normal`, **default `normal`**.

`salloc -A <project> -c 1 --mem=1G -t 00:10:00`: `Pending job
allocation …`, `queued and waiting for resources`, `has been allocated
resources`, `Granted job allocation …`, `Nodes atlas-0006 are ready
for job`, then **the login-node prompt again** (no arrival lines).
`hostname` → **`atlas-login-1.hpc.msstate.edu`**; `squeue` → `R`,
partition `atlas`, name `interact`, node `atlas-0006`; **`srun
hostname` → `atlas-0006`**. `exit` → `salloc: Relinquishing job
allocation …`; `squeue` empty.

**Answer:** on Atlas, `salloc` holds a node but leaves you on the
login node; only `srun` reaches the node (as SCINet's differences page
says). Released on `exit`.
:::

---

## Part 3: Batch jobs

All from `$CHK` on the login node. Each block writes a small job script
with `cat > file <<'EOF'` (the quotes around `EOF` keep `$` signs as
they are), then submits it.

### 3.1 The probe: what a batch job sees [checks 3, 4, 11] *Atlas too*

```bash
cat > probe.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH --job-name=probe
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=logs/%x_%j.out
echo "host: $(hostname)"
echo "pwd: $PWD"
echo "submit dir: $SLURM_SUBMIT_DIR"
echo "PROJ seen: ${PROJ:-<not set>}"
echo "pixi: $(command -v pixi || echo 'not on PATH')"
echo "module command: $(type -t module || echo 'not defined')"
echo "TMPDIR: ${TMPDIR:-<not set>}"
t=${TMPDIR:-/tmp}
ls -ld "$t"
df -h "$t" | tail -n 1
touch "$t/ch10_probe_$SLURM_JOB_ID"
sleep 60
echo "probe files in $t: $(ls "$t" | grep -c ch10_probe)"
rm -f "$t/ch10_probe_$SLURM_JOB_ID"
EOF
sbatch $ACCT probe.sbatch
sbatch $ACCT probe.sbatch
sleep 90; squeue -u $USER
cat logs/probe_*.out
```

Two copies run at once. What it answers: does the job start in the
submit folder and see `PROJ` and `pixi` (the default `--export`)? Is
`module` defined in a batch shell? What is `TMPDIR` in a batch job (not
just an interactive one), and is it private to the job? If both jobs
landed on the same host and each counted **1** probe file, `TMPDIR` is
per job; **2** means a shared folder. (Different hosts: no answer on
that point; say so.)

::: {.callout-note}
## Ceres result, 2026-11-23: complete
Both jobs finished inside the 90 s (`squeue` empty). Identical logs
apart from the host (`ceres20-compute-6` and `ceres20-compute-69`):

| Line | Ceres batch job |
|:--|:--|
| `pwd`, submit dir | both the checks folder: **starts in the submit folder** |
| `PROJ seen` | the exported path: **`--export=ALL` default** |
| `pixi` | `/home/<user>/.pixi/bin/pixi`: on `PATH` |
| `module` | `function`: defined in a batch shell, no setup line needed |
| `TMPDIR` | **`/tmp`** |
| `ls -ld /tmp` | **`drwx------. 2 <user> root 6`**: owned by you, closed to others, empty |
| `df -h /tmp` | `/dev/nvme0n1p1 1.5T 11G 1.5T 1% /tmp`: local NVMe disk |
| probe files | **1** in each job |

The two jobs ran on **different nodes**, so the count alone does not
settle "private per job". The `ls -ld` line nearly does: a shared
`/tmp` is `drwxrwxrwt root root`, while this one belongs to you with
mode `700` and is empty at the start, the pattern of a `/tmp` made for
each job (Slurm's `job_container/tmpfs` or similar).

**Follow-up (same day): confirmed by configuration.** Two probes pinned
with `-w` to one node ran one after the other (the node had room for
one more job), so the counts again could not decide. The login node's
`/tmp` is `drwxrwxrwt. 127 root root` (the shared one). `scontrol show
config` gives **`NamespaceType = namespace/tmpfs`** and **`TmpFS =
/tmp`**, with `PrologFlags = Alloc,Contain,X11`: Slurm's per-job
namespace plugin (the newer name of `job_container/tmpfs`), which
gives every job its own empty `/tmp`, removed when the job ends.
`/etc/slurm/` holds `cgroup.conf slurm.conf slurm.key` (no
`job_container.conf`). **Answer: private per job.**
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
One probe (the per-job plugin was already shown by `NamespaceType =
namespace/tmpfs` in 1.1). On `nova18-72`: `pwd` and submit dir both
the checks folder; `PROJ` seen; `pixi` at `/home/<netid>/.pixi/bin/pixi`;
`module` is a `function`; `TMPDIR=/tmp`; **`drwx------. 2 <netid> root
6`** (private, empty); `/dev/nvme0n1p1 1.5T 12G 1.5T 1% /tmp`; probe
files 1.
:::

::: {.callout-note}
## Atlas result, 2026-11-23: complete (different `TMPDIR`)
Both jobs on **`atlas-0019`**, running together, so this time the count
decides.

| Line | Atlas batch job |
|:--|:--|
| `pwd`, submit dir | the checks folder |
| `PROJ`, `pixi`, `module` | seen; `/home/<user>/.pixi/bin/pixi`; `function` |
| **`TMPDIR`** | **`/local/scratch/<user>/<jobid>`** (one folder per job ID) |
| `ls -ld` | `drwxr-xr-x 2 <user> <user> 6`: new, empty, yours (readable by others, unlike Ceres/Nova's `700`) |
| `df -h` | `/dev/nvme0n1p1 1.7T 92G 1.6T 6% /local` |
| probe files | **1** in each, on the same node |

**Answer:** private per job, by a different route: no `/tmp`
namespace; Atlas points `TMPDIR` at a per-job folder on local disk,
and `/tmp` stays the node's shared folder. Scripts that use `$TMPDIR`
work the same on all three sites; scripts that hard-code `/tmp` do
not.
:::

### 3.2 A first real job [check 7, stand-in]

The chapter's real first job wraps Chapter 8's script, which is not on
the clusters yet (Part 4). This stand-in checks the same mechanics
with seqkit directly, including the local fallback.

```bash
cat > count.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH --job-name=count
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=logs/%x_%j.out
set -euo pipefail
job_id=${SLURM_JOB_ID:-local}
threads=${SLURM_CPUS_PER_TASK:-1}
echo "job $job_id on $(hostname), $threads threads, $(date)"
pixi run --manifest-path "$PROJ/pixi.toml" seqkit stats -j "$threads" -T SRR6357070_1.fastq.gz
echo "job $job_id finished $(date)"
EOF
bash count.sbatch
sbatch $ACCT count.sbatch
squeue -u $USER
```

`bash count.sbatch` runs it right here (seconds, one small file) and
should say "job local". When the `sbatch` job is gone from `squeue`
(a minute or so):

```bash
jid=<the number sbatch printed>
cat logs/count_$jid.out
sacct -j $jid --format=JobID,JobName,State,ExitCode,Elapsed,AllocCPUS,TotalCPU,ReqMem,MaxRSS
seff $jid 2>&1 | head -n 12
```

::: {.callout-note}
## Ceres result, 2026-11-23: complete
**Run here** (`bash count.sbatch` on the login node): `job local on
ceres-login-1…, 1 threads`, then seqkit's table (`50000` reads,
`5050000` bases, length `101`), `finished` one second later. **As a
job:** `squeue` first showed `PD` with reason **`(None)`** (just
submitted), then nothing a minute later. Log: `job <id> on
ceres20-compute-9, 2 threads`, the same table, finished after 1 s.

| `sacct` line | State | ExitCode | Elapsed | AllocCPUS | TotalCPU | ReqMem | MaxRSS |
|:--|:--|:--|:--|:--|:--|:--|:--|
| `<id>` (allocation) | COMPLETED | 0:0 | 00:00:02 | 2 | 00:00.246 | 2G | (blank) |
| `<id>.ba+` (batch) | COMPLETED | 0:0 | 00:00:02 | 2 | 00:00.246 | | 106944K |
| `<id>.ex+` (extern) | COMPLETED | 0:0 | 00:00:02 | 2 | 00:00:00 | | |

`seff`: `Cores per node: 2`, `CPU Utilized: 00:00:00`, **`CPU
Efficiency: 0.00% of 00:00:04 core-walltime`**, `Job Wall-clock time:
00:00:02`, `Memory Utilized: 104.44 MB`, **`Memory Efficiency: 5.10%
of 2.00 GB (2.00 GB/node)`**; `User/Group: <user>/<user>` (personal
group, as in Chapter 7).

**For the plan:** request on the allocation line, use on the `.batch`
line, as §9 says; `sacct` cuts JobIDs to 10 characters (`.ba+`), so
widen with `JobID%15`; a toy job's CPU efficiency is meaningless (0%),
as §7 assumed; `(None)` belongs in the pending-reasons table.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
Run here: `job local on nova-login-1, 1 threads`, same seqkit table.
Job on `nova18-wide-12`, 2 threads, same table. `.batch` `MaxRSS
102156K`; `seff` `Memory Utilized: 99.76 MB`, `4.87% of 2.00 GB`,
`CPU Efficiency: 0.00% of 00:00:00` (Nova's `Elapsed` rounds this
sub-second job to `00:00:00`). While pending: the count job `(None)`,
the four submitted just after it **`(Priority)`**.
:::

### 3.3 Four jobs that fail on purpose [check 8]

```bash
for name in ok oom timeout typo; do
  case $name in
    ok)      mem=500M; t=00:05:00; cmd='pixi run --manifest-path "$PROJ/pixi.toml" python -c "print(\"ok\")"' ;;
    oom)     mem=500M; t=00:05:00; cmd='pixi run --manifest-path "$PROJ/pixi.toml" python -c "x = bytearray(2 * 1024**3); print(\"allocated\")"' ;;
    timeout) mem=500M; t=00:01:00; cmd='sleep 300' ;;
    typo)    mem=500M; t=00:05:00; cmd='bash "$PROJ/src/01_count_raeds.sh"' ;;
  esac
  printf '%s\n' '#!/usr/bin/env bash' "#SBATCH --job-name=$name" "#SBATCH --mem=$mem" \
    "#SBATCH --time=$t" '#SBATCH --output=logs/%x_%j.out' 'set -euo pipefail' \
    'echo "start $(hostname) $(date)"' "$cmd" 'echo "end $(date)"' > "$name.sbatch"
done
cat oom.sbatch
for name in ok oom timeout typo; do sbatch $ACCT $name.sbatch; done
```

`cat oom.sbatch` shows one of the generated scripts so you can see it
is ordinary. Wait about 3 minutes (the timeout job needs its minute
plus Slurm's grace time), then:

```bash
squeue -u $USER
sacct -u $USER -S today --name=ok,oom,timeout,typo --format=JobID,JobName,State,ExitCode,Elapsed,ReqMem,MaxRSS
tail -n 5 logs/ok_*.out logs/oom_*.out logs/timeout_*.out logs/typo_*.out
```

What it answers: the exact `State`, `ExitCode`, and last log lines for
each failure on this site, including whether the memory job is
`OUT_OF_MEMORY`, `FAILED` with a Python `MemoryError`, or something
else; and which `sacct` line (the job, `.batch`, `.extern`) carries the
cause.

::: {.callout-note}
## Ceres result, 2026-11-23: complete
All four on `ceres24-compute-12`; finished within the 3 minutes.

| Job | `sacct` allocation line | `.batch` line | Last log lines |
|:--|:--|:--|:--|
| `ok` | `COMPLETED 0:0`, 4 s | `COMPLETED 0:0`, `MaxRSS 76200K` | `start …`, `ok`, `end …` |
| `oom` | **`OUT_OF_ME+` (OUT_OF_MEMORY) `0:125`**, 5 s | `OUT_OF_ME+ 0:125`, **`MaxRSS 1045816K`** (above the 500M request) | `slurm_script: line 8: <pid> Killed  pixi run …`; `error: Detected 1 oom_kill event in StepId=<id>.batch. Some of the step tasks have been OOM Killed.` |
| `timeout` | **`TIMEOUT 0:0`**, 00:01:07 | **`CANCELLED 0:15`**, 00:01:09, `MaxRSS 2636K` | `error: *** JOB <id> ON ceres24-compute-12 CANCELLED AT <time> DUE TO TIME LIMIT ***` |
| `typo` | **`FAILED 127:0`**, 3 s | `FAILED 127:0` | `bash: <path>/src/01_count_raeds.sh: No such file or directory` |

Every `.extern` line is `COMPLETED 0:0`. No Python `MemoryError`: the
kernel killed the process (`Killed`). Only `ok` printed `end`.

**For the plan:** the cause is on the allocation line for `TIMEOUT`
(the `.batch` line only says `CANCELLED`) and on both lines for the
others; `MaxRSS` can exceed `ReqMem` in an OOM kill; widen
`State%15` too (`OUT_OF_ME+`); the scheduler's lines carry a
timestamp and `error:` prefix and come last in the log.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
| Job | allocation line | `.batch` line | Log |
|:--|:--|:--|:--|
| `ok` | `COMPLETED 0:0` | `MaxRSS 75952K` | `start`, `ok`, `end` |
| `oom` | **`OUT_OF_MEMORY 0:125`** | same, **`MaxRSS 1G`** | `line 8: <pid> Killed  pixi run …`; `error: Detected 1 oom_kill event in StepId=<id>.batch. …` |
| `timeout` | **`TIMEOUT 0:0`**, 00:01:16 | **`CANCELLED 0:15`** | `error: *** JOB <id> ON <node> CANCELLED AT <time> DUE TO TIME LIMIT ***` |
| `typo` | **`FAILED 127:0`** | same | `bash: <path>/src/01_count_raeds.sh: No such file or directory` |

Identical states, exit codes, and messages to Ceres; the chapter can
show one site's capture and say the other matches.
:::

### 3.4 An array, mechanics only [check 9, stand-in]

The chapter's array uses four real runs (decided; Part 4). Here four
rows point at the same file under four made-up run names, which is
enough to check the selection, the logs, and the per-task outputs.

```bash
printf 'sample\trun\tfastq_1\tfastq_2\n' > reads_test.tsv
for r in runA runB runC runD; do printf 'S\t%s\tSRR6357070_1.fastq.gz\t-\n' "$r" >> reads_test.tsv; done
cat > array.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH --job-name=array
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=logs/%x_%A_%a.out
set -euo pipefail
task=${SLURM_ARRAY_TASK_ID:?run with sbatch --array, or set it to test}
threads=${SLURM_CPUS_PER_TASK:-1}
row=$(awk -F '\t' -v n="$task" 'NR == n + 1' reads_test.tsv)
[ -n "$row" ] || { echo "no row $task in reads_test.tsv" >&2; exit 1; }
run=$(cut -f 2 <<< "$row")
fq=$(cut -f 3 <<< "$row")
[ -r "$fq" ] || { echo "cannot read $fq" >&2; exit 1; }
echo "task $task: run $run, file $fq"
[ "${1:-}" = "--dry-run" ] && exit 0
pixi run --manifest-path "$PROJ/pixi.toml" seqkit stats -j "$threads" -T "$fq" > "results/stats_${run}.tsv"
EOF
for i in 1 2 3 4 5; do SLURM_ARRAY_TASK_ID=$i bash array.sbatch --dry-run; done
sbatch $ACCT --array=1-4 array.sbatch
squeue -u $USER
```

Expected from the dry run: tasks 1–4 name `runA`…`runD`, task 5 prints
`no row 5 in reads_test.tsv`. After a minute:

```bash
ls logs/array_* results/
sacct -j <array job id> --format=JobID,State,ExitCode,Elapsed
```

::: {.callout-note}
## Ceres result, 2026-11-23: complete
**Dry run:** `task 1: run runA, file SRR6357070_1.fastq.gz` … `task 4:
run runD, …`, then `no row 5 in reads_test.tsv` (as expected).
**Submitted** with `--array=1-4`: `squeue` showed one line,
**`<id>_[1-4] ceres array <user> PD 0:00 1 (None)`**; a minute later
nothing. Four logs `logs/array_<id>_1.out` … `_4.out` and four results
`results/stats_runA.tsv` … `stats_runD.tsv`; task 1's log is the one
`task 1: run runA …` line and its result is seqkit's table (50000
reads). `sacct -j <id>`: three lines per task (`<id>_1`,
`<id>_1.bat+`, `<id>_1.ext+`), all `COMPLETED 0:0`, 2–3 s.
**For the plan:** `JobID%15` still cuts array step names; use
`JobID%20`.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
Dry run `runA`…`runD`, then `no row 5`. Pending as one line
`<id>_[1-4] nova array <netid> PD (None)`; four logs, four results;
three `sacct` lines per task, all `COMPLETED 0:0` (`Elapsed 00:00:00`
on Nova). (A first try of this block in one long paste left the shell
at the `>` continuation prompt after the files were written, nothing
submitted; Ctrl-C and pasting in two shorter parts worked. Long pastes
with heredocs are fragile; the chapter's blocks should stay short.)
:::

### 3.5 A chain where the first job fails [check 10]

```bash
jid=$(sbatch --parsable $ACCT typo.sbatch)
sbatch $ACCT --dependency="afterok:$jid" ok.sbatch
sleep 60; squeue -u $USER
```

What it answers: after the first job fails, does the second stay
pending with `(DependencyNeverSatisfied)`, or is it cancelled? If it is
still listed, `scancel` it and say so.

::: {.callout-note}
## Ceres result, 2026-11-23: complete
At submission: second job `PD (Dependency)`, first `PD (None)`. After
60 s: first `FAILED 127:0` (`.batch` the same, `.extern` `COMPLETED`);
second **still listed, `PD (DependencyNeverSatisfied)`**, `sacct`
`PENDING`. `DependencyParameters = (null)`: no `kill_invalid_depend`,
so Ceres **leaves it pending**; it has to be cancelled by hand (or
submitted with `--kill-on-invalid-dep=yes`). Cancelled with `scancel`
afterwards.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (same as Ceres)
Second job `PD (Dependency)` while the first was `PD (Priority)`;
after the first `FAILED 127:0`, the second stayed **`PD
(DependencyNeverSatisfied)`** (`sacct` `PENDING`). Cancelled by hand.
:::

::: {.callout-note}
## Atlas result, 2026-11-23: complete (differs: cancelled automatically)
Run with `--wrap` jobs (no script files on Atlas): first `--wrap=false`,
second `-d afterok:<first> --wrap=hostname`. At submission: second `PD
(Dependency)`, first `PD (None)`. A minute later `squeue` was empty;
`sacct`: first **`FAILED 1:0`**, second **`CANCELLED 0:0`**. Atlas's
`DependencyParameters = kill_invalid_depend` cancels the waiting job
itself; no `scancel` needed. (Submitted from home, so the first job's
`slurm-<id>.out` landed in `~`: `--wrap` jobs without `-o` write there.)
:::

### 3.6 A request longer than the limit [check 2]

Ceres and Atlas: 30 days. Nova: 40 days (its partition allows 31).

```bash
sbatch $ACCT --time=30-00:00:00 --wrap="hostname"   # Ceres, Atlas
sbatch $ACCT --time=40-00:00:00 --wrap="hostname"   # Nova
squeue -u $USER
```

What it answers: is the request refused straight away (and with what
message), or accepted and left pending (and with what reason)? Cancel
it afterwards with `scancel <jobid>` if it was accepted.

::: {.callout-note}
## Ceres result, 2026-11-23: complete
**Refused at submission**, no job created:

```
sbatch: error: QOSMaxWallDurationPerJobLimit
sbatch: error: Batch job submission failed: Job violates accounting/QOS policy (job submit limit, user's size and/or time limits)
```

`squeue` empty. The reason names the **QOS** wall-time limit, which
confirms that the 21 days comes from the `ceres` QOS, not the 60-day
partition. (The pending chain job from 3.5 was cancelled first.)
:::

::: {.callout-note}
## Atlas result, 2026-11-23: complete (same message as Ceres)
`-t 30-00:00:00` refused: `sbatch: error: QOSMaxWallDurationPerJobLimit`,
`Batch job submission failed: Job violates accounting/QOS policy (job
submit limit, user's size and/or time limits)`. Atlas's limit is the
`normal` QOS's 14 days.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete
**Refused at submission**, with a different message from Ceres:

```
sbatch: error: Batch job submission failed: Requested time limit is invalid (missing or exceeds some limit)
```

Nova's limit is the `nova` partition's `MaxTime=31-00:00:00` (the
`normal` QOS sets none), so the message names no QOS.
:::

### 3.7 CPU efficiency, measured [check 15]

Two 2-minute jobs, each holding 4 CPUs: one keeps all 4 busy, the
other only 1. This gives the chapter a real efficiency example.

```bash
cat > cpu.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH --job-name=cpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=logs/%x_%j.out
set -euo pipefail
echo "busy workers: $BUSY"
pixi run --manifest-path "$PROJ/pixi.toml" python - "$BUSY" <<'PY'
import multiprocessing as mp, sys, time
def spin(_):
    end = time.time() + 120
    while time.time() < end:
        pass
n = int(sys.argv[1])
with mp.Pool(n) as pool:
    pool.map(spin, range(n))
PY
EOF
sbatch $ACCT --export=ALL,BUSY=4 cpu.sbatch
sbatch $ACCT --export=ALL,BUSY=1 cpu.sbatch
```

After about 3 minutes:

```bash
sacct -u $USER -S today --name=cpu --format=JobID,State,Elapsed,AllocCPUS,TotalCPU,MaxRSS
seff <first job id> 2>&1 | head -n 12; seff <second job id> 2>&1 | head -n 12
```

Expected: CPU efficiency near 100% for `BUSY=4` and near 25% for
`BUSY=1`.

::: {.callout-note}
## Ceres result, 2026-11-23: complete (as expected)
| | `BUSY=4` | `BUSY=1` |
|:--|:--|:--|
| `sacct` Elapsed / AllocCPUS / TotalCPU | 00:02:06 / 4 / 07:58.890 | 00:02:05 / 4 / 02:00.008 |
| `.batch` MaxRSS | 68064K | 71308K |
| `seff` CPU Utilized | 00:07:59 | 00:02:00 |
| `seff` **CPU Efficiency** | **95.04%** of 00:08:24 core-walltime | **24.00%** of 00:08:20 |
| `seff` Memory | 66.47 MB, 6.49% of 1.00 GB | 69.64 MB, 6.80% of 1.00 GB |

By hand: 478.9 / (126 × 4) = 95.0%; 120.0 / (125 × 4) = 24.0%. The
TotalCPU shows on the allocation and `.batch` lines alike.
:::

::: {.callout-note}
## Nova result, 2026-11-23: complete (as expected)
| | `BUSY=4` | `BUSY=1` |
|:--|:--|:--|
| Elapsed / AllocCPUS / TotalCPU | 00:02:03 / 4 / 07:57.640 | 00:02:03 / 4 / 01:59.843 |
| `.batch` MaxRSS | 107204K | 91396K |
| `seff` **CPU Efficiency** | **97.15%** of 00:08:12 | **24.39%** of 00:08:12 |
| `seff` Memory | 104.69 MB, 10.22% of 1.00 GB | 89.25 MB, 8.72% |

(The pending chain job from 3.5 was cancelled first.)
:::

### 3.8 Clean up

```bash
squeue -u $USER
cd "$(dirname "$PROJ")" && rm -r bioinf-computing-ch10-checks
```

Cancel anything still listed with `scancel <jobid>` before deleting.

::: {.callout-note}
## Ceres, 2026-11-23: cleaned up
`squeue` empty; checks folder deleted; the project folder lists only
the book folder, the pixi cache, and an unrelated older folder.
:::

::: {.callout-note}
## Nova and Atlas, 2026-11-23: cleaned up
Atlas: `squeue` empty, checks folder and the stray `~/slurm-<id>.out`
deleted. Nova: cleanup block given (step 21); output not pasted, to
confirm on the next Nova login (`ls -d /work/<group>/<netid>/bioinf-computing-ch10-checks`
should fail).
:::

---

## Part 4: Later, once Chapters 8 and 9 are done

These need the book project on the cluster (Chapter 9 moves it) and the
array data (decided: three more fixture runs, accessions still to
verify).

- **The real first job** [check 7]: from the project folder,
  `mkdir -p logs`, test `bash jobs/01_count_reads.sbatch` inside an
  `srun` session, then `sbatch`; record both logs,
  `results/read_counts.tsv`, `sacct`, and `seff`.
- **The real array** [check 9]: after the data step, dry-run tasks 1–5
  against `data/meta/reads.tsv`, submit `--array=1-4`, record logs,
  `results/stats_<run>.tsv`, `sacct`.
- **A dated log name** for exercise 2: `sbatch
  --output="logs/%x_%j_$(date +%F).out" jobs/01_count_reads.sbatch`.

---

## Results

Filled in as results come back (placeholders for names).

| Check | Ceres | Atlas | Nova |
|:--|:--|:--|:--|
| 1.1 login node CPUs / memory | 32 / 376 GB | 48 / 376 GB | 64 / 188 GB |
| 1.1 applicable QOS and its limits | partition `ceres` attaches QOS `ceres`: 21 days (partition 60); no default QOS | default QOS `normal`: 14 days (partition unlimited) | default QOS `normal`, no `MaxWall`: partition's 31 days |
| 1.1 `seff` installed? | yes | yes | yes |
| 1.1 `MaxArraySize`, default memory and time | 10001; partition `DefMemPerCPU=2000`, `DefaultTime=02:00:00` | 10001; `DefMemPerCPU=7686`, default 2 h | **1001**; `DefMemPerCPU=3800`, `DefaultTime=04:00:00` |
| 1.1 GNU `time -v` works? | yes | yes | yes |
| 1.1 GPU partitions, `--gres` names | none | 4 GPU partitions; `gpu:a100`, `gpu:nvidia_a100_1g.10gb`, `gpu:l40s`, `gpu:v100` | in `nova*` itself; `gpu:a100`, `v100`, `l40s`, `h200`, … |
| 1.2 module trees, `samtools` modules | 3 trees; 1.16.1, 1.17 | — | 9 trees; 1.16.1, 1.19.2, 1.23.1 (hash suffixes) |
| 1.3 `.pixi` files / all entries / size | 13,001 / 15,528 / 1.3G | 13,001 / 15,528 / 1.3G | 13,001 / 15,528 / 813M |
| 2.1 node shows vs allocation says | `nproc` 2 (allocation); `free` 754 GB (node); `QOS=ceres` | — | `nproc` 2; `free` 376 GB; `QOS=normal`; `/tmp` private |
| 2.2 `salloc`: where, released on `exit`? | compute node; released (`Relinquishing`) | **login node** (`srun` reaches the node); released | compute node; released |
| 3.1 starts in submit dir; sees `PROJ`, `pixi` | yes, yes, yes | yes, yes, yes | yes, yes, yes |
| 3.1 `module` defined in batch shell? | yes (`function`) | yes | yes |
| 3.1 batch `TMPDIR`; private per job? | `/tmp`; private per job (`namespace/tmpfs`), 1.5T NVMe | `/local/scratch/<user>/<jobid>`; private per job (same node, 1 each); 1.7T NVMe | same |
| 3.2 local fallback; job log; `sacct`; `seff` | `job local`, 1 thread; job 2 threads, 2 s; `MaxRSS` 104 MB on `.batch`; `seff` 0% CPU, 5% memory | — | same; `MaxRSS` 100 MB; `(Priority)` seen |
| 3.3 `ok` | `COMPLETED 0:0` | — | same |
| 3.3 `oom` | `OUT_OF_MEMORY 0:125`; `Killed` + `oom_kill event`; MaxRSS 1.0 GB > 500M | — | same (`MaxRSS 1G`) |
| 3.3 `timeout` | `TIMEOUT 0:0` (`.batch` `CANCELLED 0:15`); `DUE TO TIME LIMIT` | — | same |
| 3.3 `typo` | `FAILED 127:0`; `No such file or directory` | — | same |
| 3.4 array: dry run, logs, outputs | as expected; `<id>_[1-4]` pending; 4 logs, 4 results; 3 `sacct` lines per task | — | same |
| 3.5 failed chain: pending or cancelled? | stays pending, `DependencyNeverSatisfied`; `scancel` by hand | **cancelled automatically** (`kill_invalid_depend`) | same |
| 3.6 over-long request: refused or pending? | refused: `QOSMaxWallDurationPerJobLimit` | refused: `QOSMaxWallDurationPerJobLimit` (14-day QOS) | refused: `Requested time limit is invalid` |
| 3.7 efficiency, 4 busy / 1 busy | 95.04% / 24.00% | — | 97.15% / 24.39% |
