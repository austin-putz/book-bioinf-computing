---
title: "Appendix A — Cluster sites: SCINet and Nova"
subtitle: "Appendix plan · optional · tracking list"
date: 2026-11-17
date-modified: 2026-11-21
---

**Status:** tracking list (2026-11-17). Collects everything Chapters 1–4
send readers to Appendix A for, and the site facts already checked in
the chapter plans, so the appendix can be written in one pass. The
appendix itself (`appendices/a-cluster-sites.qmd`) is still a stub with
an "Under construction" notice.

**Why it matters now:** Chapters 1, 2, and 4 tell readers the appendix
*will* hold specific instructions, and three Codex reviews (Chapters 1,
2, 4) flagged the stub as a publication dependency. Chapter 4 now links
the sites' support pages directly as a stopgap.

## Purpose and rules

- The chapters stay site-neutral; every SCINet- or Nova-specific step,
  path, form field, and contact lives here (`PLAN_CHAPTERS.md`,
  Appendix A, confirmed 2026-11-13).
- **Every fact from the sites' official pages, dated and linked.** No
  inferences from a storage area's name. Where a page is silent, write
  "not stated". Site pages are the authority; say so at the top.
- **Observed facts are allowed, labelled** (decided 2026-11-17): what we
  saw only by logging in (OnDemand form fields, `my_quotas` output, the
  Working Directory default, login banners) may be stated, marked
  "observed" with the date, e.g. "(observed 2026-11-16)". Published
  facts get the page link instead. Nothing observed may carry private
  details (see next rule).
- **Nothing private:** no user names, project or group names, internal
  host addresses, or anything from the SCINet welcome email
  (`plans/scinet_welcome_email.md`, git-ignored) beyond what SCINet
  publishes. Use `<netid>`, `<user>`, `<project>`, `<group>`.
- **Atlas gets its own column in every table** (decided 2026-11-17),
  as in a Ceres | Atlas | Nova layout, not notes under Ceres. Merge a
  row's Ceres and Atlas cells only where the two are effectively
  identical (e.g. "SCINet: …"). Revisit once the tables are filled.
- Recheck date at the top of each section; recheck everything before
  each release (sites change: Nova moved VS Code off login nodes in May
  2026).

## What the chapters promise (must be delivered)

Each row is a place where a chapter's text points at the appendix.
"Promise" is what the reader is told they will find.

| Ch | Where in the chapter | Promise | Appendix section |
|:--:|:---------------------|:--------|:-----------------|
| 1 | §3 guided session, cluster pitfall (`srun` line) | the `srun` options each site needs (account `-A`, partition `-p`; SCINet requires `-A`) | Interactive sessions |
| 1 | §3, same pitfall | where to download when compute nodes have no internet | Interactive sessions |
| 1 | §8 getting an account, signup tip | "step-by-step details" for SCINet and Nova signup | Accounts |
| 2 | §2 pixi on a cluster, cache pitfall | site paths for `PIXI_CACHE_DIR` and the environment (project storage) | Storage; Software |
| 2 | §4 `tbl-ssh-sites` caption | the authoritative version of the login table | Logging in |
| 2 | §5 VS Code, site route | "look up your site's route" before connecting | VS Code |
| 2 | §5 `tbl-where-to-edit` caption | which routes each site supports | VS Code |
| 2 | §5 other routes | "will collect these recipes": VS Code tunnel, Nova's Remote-SSH to a held compute node | VS Code |
| 2 | §7 `tbl-editors`, VS Code tunnels row | the tunnel recipe | VS Code |
| 2 | Exercise 4 | each site's supported route to open a folder and end the session | VS Code |
| 3 | §6 `tbl-storage-backup` caption | full, dated storage and backup facts (the chapter has a short version) | Storage and backups |
| 3 | Exercise 5 | references a site or lab already provides | Shared references |
| 4 | §3 `tbl-common-errors`, `Disk quota exceeded` | each site's quota command | Storage and backups |
| 4 | §6 `tbl-where-to-ask`, first row | each site's help desk and when to use it (VRSC, ISU Research IT linked directly for now) | Getting help |

Implicit (no link, but readers will look for it): Chapter 2's `sandbox`
project note (2-hour jobs), the Nova VPN and authenticator steps,
SCINet's `step` setup, the DTN names (Chapter 2 §4), and Chapter 4 §4's
"on a cluster, which modules are loaded".

## Planned sections

Order follows a new user's first week. Facts marked *recorded* are
already checked in a chapter plan (source in brackets); the rest are to
look up.

### 1. Which site, and who can use it

- SCINet: ARS scientists and collaborators; Ceres and Atlas are separate
  clusters with **separate storage** (Chapter 2 says so).
- Nova: Iowa State users. Other universities: "your site's research
  computing office" plus what to ask for (account, allocation, storage,
  support contact).
- To look up: who sponsors an account at each site; how long approval
  takes.

### 2. Accounts (promised by Chapter 1)

- SCINet signup page (linked in Chapter 1: scinet.usda.gov/about/signup),
  eAuthentication and Login.gov for non-USDA users, a PI or project
  sponsor; new accounts start in `sandbox` (jobs up to 2 hours) until
  added to a real project (*recorded*, `chapter_02_checks.md`).
- Nova: ISU NetID, how a group gets access (to look up on ISU's pages).
- Step-by-step list for both, from the official pages, not the welcome
  email.

### 3. Logging in (Chapter 2 §4 is the short version)

- Hosts, user names, VPN, sign-in, one-time setup, host-key question:
  move `tbl-ssh-sites` here in full (*recorded*, Chapter 2).
- SCINet: install SmallStep `step` (`brew install step` on a Mac), the
  two setup commands from SCINet's SSH page (link, do not copy: the CA
  fingerprint could change), daily browser sign-in; `step` writes the
  SSH config entries (*recorded*).
- Nova: ISU VPN off campus (Cisco Secure Client), authenticator code
  then password, published host-key fingerprints (linked in Chapter 2)
  (*recorded*).
- Atlas: own login host (`atlas-login.hpc.msstate.edu`) and docs at
  MSU (*recorded*).
- To decide: whether Chapter 9's SSH keys and `ProxyJump` need a
  per-site note here (SCINet's `step` replaces keys for login).
- Observed 2026-11-20: SCINet prints a login banner (logo and USDA
  authorized-use notice) on every `ssh`, including `ssh host command`;
  it goes to stderr, so `scp`/`rsync` are unaffected. On all three
  sites an SSH login is a login shell whose `~/.bash_profile` reads
  `~/.bashrc`, and `ssh host command` reads `~/.bashrc` too. Nova's
  `which` is a shell function that shows aliases.

### 4. Data transfer nodes and moving files

- DTN names: Nova `novadtn.its.iastate.edu`; SCINet
  `ceres-dtn.scinet.usda.gov`, `atlas-dtn.hpc.msstate.edu` (*recorded*);
  transfers never through login nodes (both sites ask this).
- Globus endpoints for each site (to look up). Commands stay in
  Chapter 9; this section gives only the hosts and site rules.

### 5. Storage, quotas, and backups (promised by Chapters 2, 3, 4)

- Full version of Chapter 3's `tbl-storage-backup`: home, project or
  work, scratch, long-term (*recorded* 2026-11-17 in `chapter_03.md`
  drafting notes):
  - SCINet: home 30 GB fixed; `/project/<project>` quota per project;
    `/90daydata` no quota, files older than 90 days deleted permanently;
    "Cluster storage is not backed up"; Juno long-term storage
    (`/LTS/project/...`, Ceres only) for data that cannot be easily
    reproduced; Juno backup and retention "not stated".
  - Nova: home 10 GB; `/work/<group>` group quota, daily snapshots, 7
    kept, restored by the file-system admins; `/ptmp` deleted after 60
    days unused; `/lss/research/<group>` backed up (login banner), not
    on compute nodes.
- Quota commands (Chapter 4): SCINet `my_quotas` (works on Ceres and
  Atlas, *recorded*); Nova has no `my_quotas` equivalent found, `quota
  -s` prints nothing, usage in `/work/<group>/group_storage_usage`
  (*recorded*). Add the pitfall: `df -h` shows the shared filesystem's
  size, not your limit.
- **Observed 2026-11-20/21 (checks Parts 2–3; Chapter 7 now has the
  Nova-vs-Ceres table `tbl-cluster-quotas`):**
  - `my_quotas`: Ceres `/usr/local/bin/my_quotas` (home, each
    `/project/<project>`, Juno `/LTS/project/<project>`; header spelled
    `Availible`); Atlas `/apps/bin/my_quotas` (home and project only;
    `Available`). Columns `Path`, `Usage (GB)`, `Quota (GB)`,
    `Available (GB)`, `Consumed (%)`, `Status`. Home 30 GB on both
    (Ceres `quota -s`: 30518M quota, 50545M limit, no file limit).
    Atlas `quota -s` errors (`Operation not permitted` on
    `/atlas/90daydata`). Ceres and Atlas project allocations are
    separate and differ in size.
  - `df -h`: on home, the whole system (Nova 14T, Ceres 91T, Atlas
    6.8P); on group storage, the group's or project's own quota
    (Nova `/work/<group>`, Ceres and Atlas `/project/<project>`).
  - Nova `group_storage_usage`: group line `NAME AVAIL USED`, fraction
    used, then per member `TYPE NAME USED QUOTA OBJUSED OBJQUOTA`
    (`OBJ` = files). Lists every member's use, so show only headers.
  - Nova helpers from ISU's pages: `my_workdir` lower-cases the group
    name and fails for upper-case folder names; `cdw` not found.
    Reported to ISU (hpc-help) 2026-11-20.
- **Permissions and shared folders (observed; Chapter 7 §2 has them):**

  | | Ceres | Atlas | Nova |
  |:--|:--|:--|:--|
  | OS | RHEL 9.6 | Rocky Linux 9.6 | AlmaLinux 9.6 |
  | umask (site-wide) | `0027` | `0027` | `0002` |
  | primary group | personal (`<user>`) | personal | `domain users` |
  | group folder | `drwxrws--T.` `root`:`proj-<project>` | `drwxrws---` (no sticky, no SELinux label) | `drwxrws--T.` `root`:`its-hpc-nova-<group>` |
  | new file | `-rw-r-----`, project group | same | `-rw-rw-r--`, lab group |
  | Ctrl-Z | on | on | **off** (`/etc/profile.d/disable-control-z.sh`) |
- Where to put the book environment and the pixi cache on each site
  (Chapter 2's pitfall): `PIXI_CACHE_DIR` in the same project storage;
  example paths with placeholders.
- To look up: file-count limits (inodes), if any; Juno and `/lss`
  retention; how to request more project space.

### 6. Interactive sessions and the first `srun` (promised by Chapter 1)

- Chapter 1's command, `srun --cpus-per-task=1 --mem=4G --time=01:00:00
  --pty bash -l`, plus each site's required options: SCINet `-A
  <project>` (not `sandbox` for long work), partition `ceres`; Atlas
  partition names from `sinfo` (not on SCINet's pages, *recorded*);
  Nova `-A <group>` (to confirm) and partition `nova` (max 31 days,
  *recorded* from the OnDemand form).
- `salloc` alternative, and how to end a session (`exit`, `scancel`).
- Internet from compute nodes at each site: allowed or not; where to
  download instead (DTN, login node for small files?) (to look up; Chapter
  1 says "some sites block it").
- Full SLURM teaching stays in Chapter 10; this is the site recipe.

### 7. VS Code on each site (promised by Chapter 2)

- Routes per site, from Chapter 2's plan §5 (*recorded*, tested
  2026-11-14/16):
  - Nova: VS Code Tunnel app (recommended), VS Code Server app in Open
    OnDemand, Remote-SSH only to a held compute node (`salloc … sleep
    infinity`, `ProxyJump` entry edited per node, needs keys, so after
    Chapter 9; add the `scancel` release step ISU's page lacks). Open
    OnDemand needs campus network or VPN.
  - SCINet Ceres: VS Code in Open OnDemand, or the VS Code Tunnel app
    (Microsoft account for USDA). Remote-SSH not documented. Atlas
    OnDemand (atlas-ood.hpc.msstate.edu): VS Code app not documented;
    check.
- The OnDemand form field names per site (Account; Queue + QOS vs Slurm
  Partition; cores vs tasks per node; Working Directory defaults:
  Ceres a session folder under `~/ondemand/`, Nova the last folder)
  (*recorded*, `chapter_02_checks.md`).
- Ending a session: **Cancel** on the card (both sites); closing the tab
  does not end it.
- Moving the code-server folder off home: symlink
  `~/.local/share/code-server` (OnDemand) or `~/.vscode-server`
  (Remote-SSH) into project storage, as both sites recommend; only once
  extensions are installed (under 1 MB without). Ceres's code-server
  (4.17) is old and may not run current extensions (*recorded*).

### 8. Software on the site

- Modules (`module avail`, `module load`, `module list`), containers
  (Apptainer), and where pixi fits: the book environment in project
  storage; site modules for things pixi does not cover. Chapter 4's
  checklist asks "which modules are loaded".
- Requesting software: SCINet's "Request Software Installation" page
  (seen on the support page); ISU's equivalent (to look up).
- Teaching stays in Chapters 7, 23, 24; this section only names the
  site's mechanisms.

### 9. Shared references (Chapter 3, exercise 5)

- Does either site provide shared reference genomes or databases (for
  example, a site-wide `/reference` area or a module)? Where, and who
  maintains them? If not, the lab-shared folder pattern from Chapter 3.
- To look up on both sites.

### 10. Getting help (promised by Chapter 4)

- SCINet: the VRSC, via
  [scinet.usda.gov/support/contact](https://scinet.usda.gov/support/contact)
  (single-user questions and login problems to the VRSC; software
  requests through the software page). Link the page, not the e-mail
  address, so it does not go stale.
- Nova: ISU Research IT,
  [research.it.iastate.edu/contact-us](https://research.it.iastate.edu/contact-us).
  ISU's FAQ gives `hpc-help@iastate.edu` for Nova requests; other pages
  say `researchit@iastate.edu` (checked 2026-11-20). Per the rule above,
  link the contact page rather than print an address.
- What to include (from Chapter 4 §7): cluster, node, job ID, the exact
  command, the complete message, what you checked. Maintenance windows
  and status pages for each site (Nova's banner announces maintenance;
  to look up SCINet's).
- Both links are already in Chapter 4's `tbl-where-to-ask`; when this
  section exists, keep the direct links and add `@sec-cluster-sites`.

### 11. Ceres vs Atlas vs Nova at a glance

- One comparison table (hosts, DTN, OnDemand, sign-in, home and project
  sizes, quota command, scratch purge, backups, VS Code route, help):
  most cells already *recorded* (Chapter 2's `chapter_02_checks.md`
  table, Chapter 3's storage facts). Hardware and partitions to add
  when Chapter 10 is planned.

### 12. Your cluster is neither (decided 2026-11-17)

- A short checklist for readers on another site: what to find in its
  documentation, in the order of this appendix. Account and sponsor;
  login host, VPN, and sign-in method; transfer node or Globus endpoint;
  storage areas with quota, purge, and backup rules, and the quota
  command; whether compute nodes reach the internet; required `srun`
  options (account, partition); the supported VS Code route (Open
  OnDemand, tunnel, Remote-SSH to a compute node); modules or
  containers; the help desk.
- Could be a fill-in table with the same rows as section 11, so readers
  build their own column.

## Atlas gaps to fill

Because Atlas now has its own column, these are needed (most Atlas facts
so far are only the hosts):

- Signup differences, if any (SCINet account covers both?).
- Login: `step` or another method on `atlas-login.hpc.msstate.edu`.
- Storage: ~~home size, project quota~~ (home 30 GB, own project
  allocations, `my_quotas` in `/apps/bin`; observed 2026-11-21);
  `/90daydata` purge and backups ("not backed up" applies to both?);
  Juno is Ceres only (`my_quotas` on Atlas has no Juno section).
- Partitions and required `srun` options (from `sinfo` and MSU's docs).
- OnDemand form fields and whether a VS Code app exists on
  atlas-ood.hpc.msstate.edu; tunnel route.
- Help: same VRSC route, or MSU's?

## Later chapters that will add to it

Not needed for Chapters 1–4, but keep the slots:

- Chapter 9 (working remotely): SSH keys per site, `ProxyJump`, Globus.
- Chapter 10 (HPC and SLURM): partitions, QOS, limits, `seff` and job
  records, GPU nodes, fair share; the site columns of its tables.
- Chapter 23–24 (environments, containers): site Apptainer notes, pixi
  in project storage.
- Chapter 26 (nf-core): each site's Nextflow config or profile, if one
  exists.

## Before release (blocking)

1. Sections 2, 3, 5, 6, 7, 10 written, because the chapter text promises
   them, each with Ceres, Atlas, and Nova columns. Then drop the "Under
   construction" callout.
2. Reword the chapter pointers from "will collect" / "will add" to
   present tense (Chapter 1: `srun` options, signup tip; Chapter 2:
   "will collect these recipes").
3. Recheck every recorded fact against the live pages and date it.

## Decisions (Austin, 2026-11-17)

1. **Atlas:** its own column in every table, unless its cells are almost
   identical to Ceres's; separate for now. Applied in the rules and
   the "Atlas gaps to fill" list.
2. **Other sites:** yes, add the checklist (section 12).
3. **Observed facts:** allowed, labelled "observed" with a date. Applied
   in the rules.

## Status update (2026-11-21)

The Chapter 5–7 checks (WSL, Nova, Ceres, Atlas) filled most of
section 5 and parts of 3; `appendices/a-cluster-sites.qmd` has their
results as dated bullets under *Planned topics*, to be turned into the
section-5 tables when the appendix is written. Private details were
removed from the book text (an internal Nova server address in Chapter
7, a group name in the appendix stub).

## Draft written (2026-11-21)

`appendices/a-cluster-sites.qmd` now holds a full draft of sections
1–5, 7, 8, 10, and 12, plus partial 6 (from the pages) and 9; the
"Under construction" callout stays until 6, 9, and 11 are done. Every
table has Ceres, Atlas, and Nova columns. Facts come from web lookups
on 2026-11-21 (SCINet pages last updated 2024-09 to 2026-01; MSU's
Atlas docs footer 2025; ISU pages undated) and the Chapter 2 and
Chapter 5–7 checks (marked "observed"). E-mail addresses are not
printed; contact pages are linked.

**Conflicts found in the sources (resolved in the draft as shown):**

- Atlas sign-in: SCINet's SSH page sets up Atlas with `step`; MSU's
  connect page says password + Duo. Draft shows both, *to confirm*.
- Nova job length: ISU's pages say two weeks; the OnDemand form showed
  31 days for `nova`. Draft gives both.
- Nova `/ptmp`: "6 to 8 weeks" (page) vs 60 days unused (banner). Both.
- Nova snapshots: "7 daily snapshots" vs "deleted … after 5 days".
  Draft says "daily snapshots" and "frees space after about five days".
- Ceres `salloc` length: 2 hours (SLURM guide) vs 2 days with a
  1.5-hour idle timeout (Apptainer guide). Draft uses the SLURM guide.
- Atlas quota command: MSU says `my_quota`; observed `my_quotas`
  works. Draft uses the observed one.
- ISU's VS Code page says SSH to `nova-vscode` is no longer available;
  the SSH page still lists it. Not used in the draft.

## Login checks needed (step 2)

For Austin, on each cluster (results go in the checks file):

1. **Atlas sign-in:** how does `ssh atlas-login.hpc.msstate.edu`
   ask for sign-in: browser (`step`), or password + Duo? Host-key
   question on first login?
2. **Atlas OnDemand:** the Interactive Apps list; is there a VS Code
   Server or Tunnel app? Start-form field names.
3. **Interactive session, each cluster:** run the site's command from
   §6, then on the node `hostname`, `curl -sI https://pixi.sh | head
   -n 1` (internet from compute nodes?), `exit` (and `scancel` if
   needed). On Nova, check whether `-A` is needed.
4. **`sinfo -s`** on each cluster (partition names and limits).
5. **Reference folders:** `ls /reference` on Ceres and Atlas; anything
   similar on Nova?
6. **Nova containers:** `module avail apptainer` (or `which apptainer`).

### Step 2 results (2026-11-21)

- Done, in the appendix: 1 (Atlas uses `step` with a Login.gov
  sign-in; no host-key prompt), 2 (Atlas OnDemand has a *VSCode*
  server app, no Tunnel app; form fields not yet seen), 4 (Ceres and
  Atlas; partition limits are 60/21 days and unlimited, so QOS sets
  the real limits), 5 (Ceres and Atlas folder lists), 6 (Nova
  Apptainer 1.1.5 to 1.4.0 as modules).
- Later the same day: 3 done on all three (`srun ... --pty bash -l`
  works; Ceres and Atlas need `-A`, Nova does not; internet on every
  compute node, Atlas through a proxy with `https_proxy` set); 4 on
  Nova (`interactive` partition is 8 h); Atlas `/reference/README`.
  Section 11 (`tbl-sites-glance`) written. Fixed: wide-table captions
  sat outside the div, so no appendix table was numbered.
- Done: Nova `/shared` is site configuration, not reference data;
  `/reference/data` (same on Ceres and Atlas) is tool databases.
- Still to do: Atlas VSCode form fields (screenshot), and whether `pixi install` works
  through Atlas's proxy (when the book environment is installed there).

## Open questions

- None yet.

## Austin's notes

-
