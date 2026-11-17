---
title: "Chapter 2 — Book setup and editors"
subtitle: "Chapter plan · core · draft"
date: 2026-11-13
---

**Part:** I — Getting set up · **Label:** core · **Status:** draft, revised
after the Codex and Antigravity reviews and the open-questions round
(2026-11-13; see *Review responses* and *Decisions*), then updated with
Austin's hands-on checks on Windows/WSL, Atlas, Ceres, and Nova
(2026-11-14 to 16; see *Hands-on checks*), then a final review
(2026-11-16; see *Final review*). **Chapter drafted** 2026-11-16 in
`chapters/02-book-setup.qmd` (see *Drafting notes*)

## From `PLAN_CHAPTERS.md`

- Install pixi and the book environment; run a first example
- VS Code as the primary editor, including Remote-SSH
- Just enough SSH to connect to a cluster (full treatment in Chapter 9)
- Pitfall: some clusters restrict the VS Code server on login nodes; fall
  back to Open OnDemand or a compute-node session
- nano and vim basics for editing on a server
- Reference table: RStudio / Positron, Jupyter, Quarto, Open OnDemand

## Outcome and check

- **Outcome:** readers have the book environment installed with pixi from
  the book's tested `pixi.toml` + `pixi.lock`, and can run a tool from it
  with `pixi run` on the FASTQ file from Chapter 1. They can open a folder
  in VS Code and use its terminal, and (if they have a cluster account)
  open a remote folder using their site's supported method. On a bare
  server they can edit, save, and quit a file in nano, and leave vim
  without saving.
- **Check:** two commands from `~/bioinf-computing`:
  - `pixi run check` prints the Python, R, and seqkit versions recorded
    for the book release (it checks the environment only, so it keeps
    working wherever data files later move).
  - `pixi run seqkit stats ~/bioinf-ch01/SRR6357070_1.fastq.gz` reports
    `num_seqs` = `50,000` and `sum_len` = `5,050,000` (50,000 reads × 101
    bases). This repeats Chapter 1's count with a real tool.
  - Verified 2026-11-13 (pixi 0.84.2, macOS 15 Intel, draft manifest):

    ```
    Python 3.12.16
    R version 4.4.3 (2025-02-28) -- "Trophy Case"
    seqkit v2.14.0

    file                   format  type  num_seqs    sum_len  min_len  avg_len  max_len
    SRR6357070_1.fastq.gz  FASTQ   DNA     50,000  5,050,000      101      101      101
    ```

    (Run from `~/bioinf-ch01` or the file column shows the full path.)

## Learning goals (draft of the opening callout)

By the end of this chapter you should be able to:

1. Install pixi and the book environment from its manifest and lockfile.
2. Run a tool with `pixi run`, and explain why the same command typed on
   its own is not found.
3. Open a project folder in VS Code and use its built-in terminal, and
   tell where it is running (the status bar in the desktop app,
   `hostname` in any terminal).
4. Open a folder on a remote machine with your site's supported method,
   and say where your files and commands live once connected.
5. Edit and save a file in nano, and leave vim without saving.

## Sections

Same pattern as Chapter 1: the reader gets a working environment early
(section 2), then learns where to type (VS Code), then how to reach a
server and edit there. Each section starts with something the reader runs,
then names the idea. Sections 4–5 are for readers with a cluster account;
everyone else reads the captured sessions and does sections 2, 3, and 6.
Visual items in brackets are specified under *Visuals and teaching aids*.

1. **What this chapter does.** Learning-goals callout. One paragraph: one
   environment and one editor for the book's core examples, so those
   chapters do not stop for installs. Container and pipeline runtimes and
   site software come later with their own setup (Chapters 24, 26).
   Alternatives appear only in the reference table (section 7) and in
   Chapter 23.
2. **Installing pixi and the book environment.** *Start hands-on:* one
   install command (OS tabset: `macOS` / `Windows (WSL2)` / `Linux`; the
   WSL2 and Linux tabs share the command, the WSL2 tab says "in the Ubuntu
   terminal, not PowerShell"). The installer picks the startup file from
   your login shell (`$SHELL`): for bash it appends `~/.pixi/bin` to
   `PATH` in `~/.bashrc` (checked in `install.sh`, 2026-11-13). On macOS
   that works because Chapter 1's `~/.bash_profile` reads `~/.bashrc`;
   the macOS tab says so and adds one check: if the installer reports
   `~/.zshrc`, bash is not yet the login shell, so go back to Chapter 1's
   macOS setup. Open a new terminal, then check `pixi --version`
   (the book states the pixi version it was tested with). Make
   `~/bioinf-computing`, download `pixi.toml` and `pixi.lock` from one fixed
   book release with `curl -fLO`, run `pixi install --locked`, then
   `pixi run check`, then `pixi run seqkit stats` on the Chapter 1 file.
   **Checkpoint:** if a download or the install fails, stop there (as in
   Chapter 1). *Then name the parts:* manifest (`pixi.toml`: what the
   project needs), lockfile (`pixi.lock`: the exact packages resolved for
   each supported platform), environment (`.pixi/envs/default/`: the
   installed files), channels (conda-forge, bioconda). Installing does not
   add these tools to every terminal: `pixi run` runs one command with
   them; `pixi shell` starts a shell with them until you type `exit`
   (changing folders does not end it). `pixi add` changes the manifest and
   lockfile; readers following the book do not need it yet. Depth
   (solving, `PATH`) deferred to Chapters 7 and 23. *On a cluster*
   (one short paragraph, tested on Ceres 2026-11-14): install in project
   storage (`/project` on SCINet, `/work` on Nova), not home (30 GB on
   SCINet, 10 GB on Nova) or purged scratch (`/90daydata`, `/ptmp`),
   with `PIXI_CACHE_DIR` there too; run the install from a
   compute session (OnDemand terminal or `salloc`), not a login node;
   expect the first install to take from seconds to several minutes
   depending on the site's storage (reinstall from cache: 57 s on
   Ceres, 2.4 s on Nova), and don't interrupt it; each cluster has its
   own storage, so install on the cluster you will use (SCINet's Ceres and Atlas do not
   share `/project`). [`fig-pixi-parts`,
   `tbl-pixi-commands`; key idea; pitfall: cluster cache; misconception
   callout "installed everywhere"; self-check]
3. **VS Code: a home for your work.** *Start hands-on:* install VS Code
   (OS tabset). macOS: open the Command Palette (`Cmd-Shift-P`), type
   `shell command`, and run *Shell Command: Install 'code' command in
   PATH* once (newer releases label it *Install 'code' and optionally
   'copilot' commands in PATH*), then reopen the terminal. Windows:
   install the normal **Windows** application plus its WSL extension;
   never a second Linux copy inside Ubuntu; open the folder with `code .`
   from the Ubuntu terminal. Check it is on `PATH` (`where.exe code` in
   PowerShell, `which code` in Ubuntu, which shows a
   `/mnt/c/Users/<you>/…/Microsoft VS Code/bin/code` path because WSL
   inherits the Windows `PATH`); if not found, close every terminal, run
   `wsl --shutdown`, reopen, and if still missing rerun the installer
   with **Add to PATH** ticked (ticked by default; tested 2026-11-14).
   Windows user names can contain spaces, so `/mnt/c/Users/…` paths may
   too: one more reason to keep work in the Linux home (quoting paths in
   Chapter 5). Linux: `code` is on `PATH` after install.
   File → Open Folder works everywhere. Open `~/bioinf-computing`, open the
   built-in terminal, and check it runs the same bash as Terminal:
   `echo "$BASH_VERSION"` shows 5.x (macOS) and `sed --version` says GNU.
   On macOS this should already hold: VS Code's terminal starts `$SHELL`
   (Homebrew bash after Chapter 1's `chsh`) and, on macOS, as a login
   shell, so it reads `~/.bash_profile` (VS Code terminal-profiles docs).
   Fallback if it shows zsh or bash 3.2 (`/bin/bash`): define a profile in
   `terminal.integrated.profiles.osx` with `"path"` set to Homebrew's bash
   (`/opt/homebrew/bin/bash`, or `/usr/local/bin/bash` on Intel) and
   `"args": ["-l"]`, and select it in
   `terminal.integrated.defaultProfile.osx`. Then run `pixi run check`
   there. *Then name the parts*
   with a labelled window schematic: explorer, editor, terminal panel,
   status bar, whose left end shows where you are connected (`WSL:
   Ubuntu`, later `SSH: <host>`) in the desktop app; browser VS Code on
   a cluster shows only an icon there (tested on Ceres and Nova), so the
   universal check is `hostname` in the terminal. Extensions the book uses, installed now
   from one table. Pointing the Python and R extensions at the pixi
   environment is deferred to Chapters 12–13, where readers first need it
   (the R extension also needs the `languageserver` package there).
   [`fig-vscode-window`, `tbl-vscode-extensions`; tip: `code .`;
   self-check]
4. **Just enough SSH.** *Start hands-on:* `ssh user@host` from the laptop
   terminal, `hostname`, `exit`. The captured `.console` session includes
   the first-connection host-key prompt, annotated: type the full word
   `yes` (OpenSSH rejects `y`), after which the host is remembered in
   `~/.ssh/known_hosts`. Then the site's sign-in (details in Appendix A,
   `@sec-cluster-sites`). The captured session is Nova's real first
   login (recorded 2026-11-16): host-key prompt, `yes`, "Permanently
   added", then `Verification code:` (from an authenticator app)
   **before** `Password:`, neither showing what you type, then the site
   banner. Cluster prompts look different from Ubuntu's (`[user@host
   ~]$` on Rocky Linux vs `user@host:~$`); one line says so. Site
   differences, one short paragraph each:
   - **Nova:** off campus, connect the ISU VPN first (Cisco Secure
     Client, formerly AnyConnect); username is the ISU NetID.
   - **SCINet:** no VPN; SCINet recommends Open OnDemand for most work,
     so readers may skip SSH and do §5 first. SSH needs SmallStep's
     `step` once (tested on a Mac 2026-11-16: `brew install step`, then
     `step ca bootstrap …` and `step ssh config …` copied from
     scinet.usda.gov/guides/access/ssh-login), then plain `ssh` to
     `ceres.scinet.usda.gov` or `atlas-login.hpc.msstate.edu`; a browser
     sign-in (eAuthentication, Login.gov for non-USDA users) about once
     a day. `step` adds only an `Include` block to `~/.ssh/config` and
     supplies the user, a short-lived certificate, and its own
     `known_hosts`, so SCINet readers **do not** see the `yes` prompt
     (confirmed). New accounts start in a `sandbox` project (2-hour
     jobs) until a PI adds them to a real one.

   Then a minimal `~/.ssh/config` entry
   (`Host`, `HostName`, `User`) so a short name works. Windows: say which
   home holds which config: the Ubuntu terminal uses the WSL file
   (`~/.ssh/config` in Linux); VS Code's Remote-SSH uses the Windows SSH
   client (built-in `C:\Windows\System32\OpenSSH\ssh.exe`) and its own
   config file (section 5). A fresh Ubuntu has no `~/.ssh` folder until the
   first `ssh` connection creates it, so `ls ~/.ssh` failing before then is
   normal (tested 2026-11-14). Keys, jump hosts, and
   `ProxyJump` wait for Chapter 9, unless the reader's site requires them
   to log in at all; then Appendix A gives that step. [self-check]
5. **Editing on a remote machine.** *First, the site check:* connecting
   is what starts a VS Code server, so look up your site's route in
   Appendix A before connecting. Both named sites keep VS Code off login
   nodes (checked 2026-11-13):
   - **Nova:** VS Code Tunnel app (from Open OnDemand) to a compute node,
     the recommended route; or the VS Code Server app in Open OnDemand;
     Remote-SSH only to compute nodes (ISU "Remote IDEs on Nova compute
     nodes": `salloc … sleep infinity` to hold a node, then a
     `~/.ssh/config` entry with `ProxyJump nova-login` whose host name
     must be edited to the assigned node each time; needs key-based
     login, so this route comes after Chapter 9, and the page gives no
     release step, so Appendix A adds `scancel`). SSH to
     `nova-vscode` is gone, and the May 19, 2026 maintenance moved VS
     Code off `nova-login-*` because "VSCode processes often rend login
     nodes unusable". Open OnDemand needs the campus network or VPN
     (off campus: Cisco Secure Client, formerly AnyConnect), and Nova
     login uses a code from an authenticator app (e.g. Google
     Authenticator). **Tested (2026-11-16):** Interactive Apps → Servers
     → *VS Code Server*; form: Account (group), Slurm Partition
     (`nova`), hours, tasks per node (CPUs), memory, Extra Modules,
     Working Directory (defaults to the last used folder; set it), and
     code-server version (4.97). It ran on a compute node
     (`nova18-69`) in `/work/<group>/<netid>`.
   - **SCINet (Ceres):** VS Code Server in Open OnDemand, or a registered
     tunnel started from the OnDemand "VS Code Tunnel" app, both on
     compute nodes. Tunnels need a Microsoft or GitHub account (USDA:
     Microsoft). Remote-SSH is not mentioned. **Tested on Ceres
     (2026-11-14/16):** Interactive Apps → Servers → *VS Code*; form:
     Account (your project, not `sandbox`), Queue and QOS (`ceres`),
     cores, memory (e.g. `8G`), hours, Working Directory (defaults to
     `$HOME`, but left blank the terminal opened in the session's
     ID-named folder under `~/ondemand/data/sys/…`; set to the project
     folder, explorer and terminal open there), and code-server version
     (4.17, much older than Nova's). It ran on a compute node
     (`ceres20-compute-2`). Atlas has its own OnDemand
     (atlas-ood.hpc.msstate.edu); whether it offers VS Code is not
     documented, so Ceres is the SCINet example.

   *Then hands-on:* readers with a site route (SCINet, Nova, many
   universities) follow its Appendix A recipe: start the OnDemand app or
   tunnel, open a folder in project space, open a terminal, run
   `hostname` (a compute node). Readers on sites that allow it use
   Remote-SSH (Connect to Host → pick the host → open a folder → terminal
   → `hostname`); Windows readers add the host with *Remote-SSH: Add New
   SSH Host*, which asks which config file to write: pick the first,
   `C:\Users\<you>\.ssh\config` (the second, `C:\ProgramData\ssh\ssh_config`,
   is system-wide and needs admin). It offers only Windows files even
   from a `WSL: Ubuntu` window, so Ubuntu's `~/.ssh/config` is never used
   by Remote-SSH (tested 2026-11-14). Both routes are
   shown as captured sessions for no-cluster readers. Open the project
   folder first (the form's Working Directory, or File → Open Folder…)
   and only then start commands: opening a folder reloads the window and
   stops whatever its terminal was running (happened on Ceres,
   2026-11-14). *Then name the
   idea:* the window is local; a VS Code server runs on the remote
   machine, with the files and terminal. Extensions split: UI ones
   (themes) stay local, most others run remotely; in browser code-server
   the extension catalogue may be Open VSX rather than Microsoft's.
   Laptop files and the laptop's pixi environment are **not** copied to
   the cluster. A compute session holds a node until it is cancelled or
   times out: end it with **Cancel** on its card in *My Interactive
   Sessions* (both sites; the card turns Completed, and Delete only
   clears the card), then close the tab yourself. Closing the tab alone
   does **not** end the session (checked on Nova: the card stays
   Running). Writing in the browser terminal: paste short blocks; a long
   pasted block broke on Nova (it started R's prompt). The server and its extensions live in your home
   directory (`~/.vscode-server` for Remote-SSH, `~/.local/share/
   code-server` for OnDemand) and can exceed the home quota; both sites
   recommend moving the code-server folder to project storage with a
   symlink (the Ceres form says so too). Chapter 2 only mentions it and
   points to Appendix A: with no extensions the folder is under 1 MB
   (976 KB on Ceres), so it only matters once extensions are installed. [`fig-remote-ssh`, `tbl-where-to-edit`;
   misconception callout "runs on my laptop"; pitfall: login-node
   limits; self-check]
6. **Editing in the terminal: nano and vim.** macOS first (one line in an
   OS note, not a tabset): macOS's `nano` is really pico, so run `brew
   install nano` to get GNU nano, the same editor as on Linux and the
   cluster (`nano --version` says GNU nano). *Start hands-on:* `nano
   notes.txt`, type a line, save (`Ctrl-O`, Enter), quit (`Ctrl-X`),
   `cat notes.txt`. (Clusters have both editors: Atlas has GNU nano
   5.6.1 and vim, WSL Ubuntu nano 8.7.1 and Vim 9.1; the basics taught
   here are the same in both nano versions.) Then vim, only enough to survive: open, `i` to type,
   `Esc`, `:wq` to save and quit, `:q!` to quit without saving. Why it
   matters: some tools (e.g., `git commit` without `-m`) open an editor.
   One sentence: to abort such an operation from vim, use `:cq`, not
   `:q!`. `export EDITOR=nano` makes nano the default for this terminal
   only; Chapter 7 makes it permanent (and Git's own setting can override
   it). [`fig-vim-modes`, `tbl-nano-vim`; tip: "stuck in vim";
   self-check]
7. **Other editors and tools (reference).** No exercises. One compact
   table: RStudio, Positron, Jupyter (Lab / notebooks), Quarto, Open
   OnDemand, VS Code tunnels, vim/nano: what it is, when readers might
   meet it, where in the book it returns. VS Code also edits Quarto and
   runs Jupyter notebooks, so nothing here is required. [`tbl-editors`]
8. **Summary, exercises, further reading.** Summary as 4–5 bullets that
   mirror the learning goals; exercises (below); annotated further reading.

## Visuals and teaching aids

Everything here follows `book-bioinf-theme/STYLE-GUIDE.md` and is
demonstrated in `book-bioinf-theme/example/`. Section numbers (§) refer
to STYLE-GUIDE.

### Figures (SVG, §7)

All hand-drawn SVGs in `figures/`, pasted with the `svg` shortcode inside a
`::: {#fig-…}` div, colours from theme classes only. Colour roles (§2):
our data and files are `given` (blue); software and infrastructure are
neutral (`ink`, `line`, `muted`).

| Label | Section | Kind | What it shows |
|:------|:-------:|:-----|:--------------|
| `fig-pixi-parts` | 2 | stepped (4 steps) | The book folder: (1) `pixi.toml` (what the project needs) and the supplied `pixi.lock` (exact packages per platform) arrive together; (2) `pixi install --locked` downloads this platform's packages from the channels into a shared cache; (3) they are installed into `.pixi/envs/default/`; (4) `pixi run seqkit …` runs with the environment, while bare `seqkit` in the same terminal is not found. One sentence per step. |
| `fig-vscode-window` | 3 | static | Schematic (not a screenshot) of the VS Code window with four labelled areas: explorer, editor, terminal panel, status bar. The status bar's left end reads `WSL: Ubuntu` or `SSH: <host>` (desktop app); the caption notes that browser VS Code shows only an icon there, so `hostname` is the universal check. |
| `fig-remote-ssh` | 5 | static | Laptop (VS Code window, UI extensions, local files) → SSH → generic remote host running the VS Code server (remote files, terminal, language extensions), with local and remote files labelled separately. Two remote targets: a login node and an allocated compute node, the second marked as the route many sites require. **Add the route both tested sites use:** a browser → Open OnDemand → VS Code server on a compute node, so the figure shows desktop Remote-SSH and browser OnDemand side by side (both: window local, files and terminal remote). Reuses the shapes from `fig-cluster-anatomy` (Chapter 1). |
| `fig-vim-modes` | 6 | static | Two boxes, Normal and Insert, with the keys on the arrows (`i` in, `Esc` out) and the exits from Normal (`:wq`, `:q!`, and `:cq` labelled "abort the tool that opened vim"). |

Not used here: screenshots (VS Code's look changes with every release and
theme), Mermaid (`fig-pixi-parts` needs labelled files, not just boxes).

### Interactive figure (Observable JS)

None. Nothing here is an input → result relationship.

### Tables (§5)

Pipe tables, caption above, `tbl-` label, cited by label.

| Label | Section | Columns |
|:------|:-------:|:--------|
| `tbl-pixi-commands` | 2 | Command · what it does · when you use it (`pixi install --locked`, `pixi run`, `pixi shell` / `exit`, `pixi list`, `pixi task list`, `pixi add` marked "changes the manifest and lockfile; not needed yet") |
| `tbl-vscode-extensions` | 3 | Extension · publisher · what it adds · runs where (local / remote) · needed from (Remote-SSH, WSL now; Python, R, Quarto configured in Chapters 12–13) |
| `tbl-where-to-edit` | 5 | Option (Open OnDemand VS Code Server · VS Code tunnel to a compute node · Remote-SSH to a compute session · Remote-SSH to a login node, where allowed · nano/vim over SSH) · what you need (e.g., VPN, Microsoft/GitHub account, SSH config) · good for · limits (incl. "end the session when done" where resources are allocated; login-node VS Code blocked at Nova and SCINet) |
| `tbl-nano-vim` | 6 | Action · nano · vim (open, start typing, save, quit, quit without saving, abort the calling tool, search) |
| `tbl-editors` | 7 | Tool · what it is · when you might meet it · where it returns in the book |

### Code (§6)

- Labels per STYLE-GUIDE §6: `filename="Terminal (laptop)"` for §2–3 and
  §6, and for the `ssh` command in §4; `filename="Terminal (login node)"`
  for what is typed after connecting. WSL readers are told in the text
  that "laptop" means their Ubuntu terminal. Config files keep their
  filenames (`filename="pixi.toml"`, `filename="~/.ssh/config"`) and the
  text names the machine and home directory where each is edited.
- Tier 2 (shown, not run at render). All steps are cheap except
  `pixi install --locked`, which gets a compute note with measured
  download size, installed size, and file count (from a script in
  `scripts/`, e.g., `ch02_env_size.sh`).
- **Bash everywhere** (book `CLAUDE.md`): every command and output assumes
  bash with GNU tools. macOS steps assume Chapter 1's setup (Homebrew
  bash as login shell, gnubin first on `PATH`, `~/.bash_profile` reading
  `~/.bashrc`); no zsh variants, and startup-file edits go in
  `~/.bashrc`. New macOS tools come from Homebrew (GNU nano), as in
  Chapter 1.
- OS tabsets (`group="os"`) in §2 (install pixi), §3 (install VS Code,
  `code` on `PATH`, WSL extension, macOS terminal profile), and §5 only if
  the Windows Remote-SSH step really differs. Everything else is
  Linux-only.
- No `$` prompt, code annotations for each new command, captured output
  in `.console` blocks, including one captured first SSH session (with
  the host-key prompt) for no-cluster readers.
- Keys with `{{< kbd >}}` (`Ctrl-O`, `Ctrl-X`, `Esc`).

### Plots

None.

### Animation (manim)

None. The one sequence (manifest + lock → install → run) is a short
stepped SVG.

### Callouts (§3, at most ~3 per screen)

| Section | Type | Content |
|:-------:|:-----|:--------|
| 1 | Learning goals | As drafted above |
| 2 | Key idea | The manifest describes the software the project needs; the lockfile records the exact packages resolved for each supported platform. Installing from both gives you the environment the book was tested with (same versions, not identical binaries across operating systems) |
| 2 | Misconception | "Once I install a tool, it works in every terminal" |
| 2 | Pitfall | On a cluster, pixi's download cache defaults to your home directory and can fill its quota; set `PIXI_CACHE_DIR` to the same project storage as your environments (site paths in Appendix A): on Linux pixi hard-links files from the cache into `.pixi/`, which only works within one filesystem, so a cache in `$HOME` with a project elsewhere doubles the space and lands the copy in home. Moving the cache does not move `.pixi/envs/`; that option (detached environments) is in Chapter 23. Also: the first install on a cluster can take from seconds to several minutes, depending on the site's storage, and is not stuck |
| 3 | Tip | `code .` opens the current folder in VS Code (from the Ubuntu terminal on Windows; on macOS after the one-time *Install 'code' command* step) |
| 5 | Misconception | "With Remote-SSH, my code runs on my laptop" |
| 5 | Pitfall | Check your site's VS Code route before connecting; many sites (including Nova and SCINet) keep VS Code off login nodes. Set the session's working directory to your project folder before you start (opening a folder later reloads the window and stops running commands). End compute sessions with Cancel on the session card (closing the tab does not), and move the VS Code/code-server folder out of `$HOME` if your site says to |
| 6 | Tip | Stuck in vim? Press `Esc`, type `:q!`, press Enter (`:cq` if you want the tool that opened vim, such as `git commit`, to stop) |

Misconceptions without a callout ("I need sudo to install these tools",
"I need RStudio for R / Jupyter for Python") are handled in the text and
in self-checks.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2 (a): In a fresh terminal in `~/bioinf-computing`, `seqkit stats …` says
  `command not found`, but `pixi run seqkit stats …` works. You have not
  installed seqkit any other way. Why? (*Installing the environment does
  not put its tools in every terminal; `pixi run` runs the command with
  the environment, or start `pixi shell`.*)
- §2 (b): Which file says exactly which version of each package you have:
  `pixi.toml` or `pixi.lock`? (*`pixi.lock`; `pixi.toml` says what the
  project needs, often as a range.*)
- §3: Where in the VS Code window can you see, at a glance, whether you
  are working on your own computer, in WSL, or on a remote machine? (*The
  left end of the status bar in the desktop app; in any terminal,
  including browser VS Code, `hostname` answers it.*)
- §4: After `ssh` you type `hostname` and see a login-node name. Which
  computer runs your next command? (*The cluster's login node.*)
- §5: In a remote window you open a terminal and run `ls`. Whose files do
  you see, and is `~/bioinf-computing` there? (*The cluster's; your laptop
  folder is not copied over.*)
- §6: A command opened vim and your terminal fills with `~` lines. How do
  you leave without saving? (*`Esc`, `:q!`, Enter.*)

End-of-chapter exercises (core chapter, so required):

1. Run `pixi list` and find the versions of Python, R, and seqkit. Do they
   match what `pixi run check` printed? Open `pixi.lock` in VS Code and
   search for seqkit to see where the same version is recorded.
2. Run `pixi run seqkit stats` on the read-2 file from Chapter 1's
   exercise (change `_1` to `_2`; if you skipped that exercise, the
   supplied `curl -fLO` command downloads it into `~/bioinf-ch01`). Do
   the two files have the same `num_seqs`?
3. In nano, create `README.md` in `~/bioinf-computing` with one line saying
   what the folder is for. Then open it in vim, add a second line, and
   save with `:wq`. Run `cat README.md` in VS Code's terminal to check
   both lines.
4. (Cluster readers) Open a folder on your cluster using your site's
   supported method (Appendix A), open a terminal there, and run
   `hostname` and `pwd`. Record where you landed, then end the session
   with Cancel on its card (closing the tab is not enough). (No-cluster readers: answer from the captured
   session.)

## Examples and data

- Toy example: `notes.txt` / `README.md` for the editor sections, one or
  two lines, so readers can check by eye that the save worked.
- Running dataset (yeast nf-core/rnaseq test data): `SRR6357070_1.fastq.gz`
  (and `_2` from Chapter 1's exercise), used **in place** in
  `~/bioinf-ch01/` (2,239,317 bytes, 50,000 reads of 101 bases, verified
  2026-11-13). Chapter 2 does not move data: Chapter 1 promises that
  Chapter 3 brings these files and their source URLs into the project,
  and Chapter 3 does so inside `~/bioinf-computing`.
- Folder plan: `~/bioinf-computing` is created here and holds `pixi.toml`,
  `pixi.lock`, and the README from exercise 3. Chapter 3 organizes the
  same folder into the recurring project (`data/`, `src/`, `results/`,
  …), so `pixi.toml` stays at the project root for the whole book.
- Draft `pixi.toml` (content to be settled; see open questions). The
  author solves it and publishes it with its `pixi.lock` from one tested
  book release; `pixi lock` across the three platforms is also the build
  check that every package exists on each.

  ```toml
  [workspace]
  name = "bioinf-computing"
  channels = ["conda-forge", "bioconda"]
  platforms = ["linux-64", "osx-arm64", "osx-64"]

  [dependencies]
  python = "3.12.*"
  r-base = "4.4.*"
  seqkit = "*"
  nano = "*"                 # fallback editor (pixi run nano)
  tree = "*"                 # folder layouts (pixi run tree), from Chapter 3

  [tasks]
  check = "python --version && R --version | head -n 1 && seqkit version"
  ```

  No `win-64` platform: bioconda does not build for Windows, which is one
  more reason Windows readers work in WSL2.
- Draft command sequence (laptop):

  ```bash
  curl -fsSL https://pixi.sh/install.sh | sh     # pixi docs, checked 2026-11-13
  # open a new terminal (installer added ~/.pixi/bin to PATH), then:
  pixi --version
  mkdir -p ~/bioinf-computing && cd ~/bioinf-computing
  curl -fLO https://raw.githubusercontent.com/austin-putz/book-bioinf-computing/<tag>/setup/pixi.toml
  curl -fLO https://raw.githubusercontent.com/austin-putz/book-bioinf-computing/<tag>/setup/pixi.lock
  pixi install --locked
  pixi run check
  pixi run seqkit stats ~/bioinf-ch01/SRR6357070_1.fastq.gz
  code .
  ```

- Where commands run: laptop for §2, §3, §6; laptop → remote host for
  §4–5. On a cluster, pixi installs in the reader's own space with no
  admin rights; site modules may provide some tools too (Appendix A says
  where pixi fits on each site).

## Misconceptions

New entries for the book's `misconceptions.yml` (id, claim, reality,
probe, chapters), to add when this plan is agreed. Where each is handled
is in brackets.

- `installed-everywhere`: "Once I install a tool, it works in every
  terminal." Installing the book environment does not add its tools to
  every terminal; `pixi run` (or `pixi shell`) runs commands with it.
  [callout, §2; self-check]
- `need-sudo-to-install`: "I need admin rights (sudo) to install the tools
  I use." Tools like these install into your own space with pixi or
  conda; some system components and container runtimes do need your
  site's admins. [text, §2; again Chapter 23]
- `remote-runs-on-laptop`: "With VS Code Remote-SSH, my code runs on my
  laptop." The window is local; files, terminal, and language support run
  on the remote machine, and laptop files are not copied over.
  [callout, §5; self-check]
- `ide-required`: "I need RStudio for R and Jupyter for Python." Any
  editor plus a terminal runs both; VS Code covers scripts, notebooks,
  and Quarto. [text, §7]
- `stuck-in-vim`: "If vim opens, I have to close the terminal." `Esc`,
  `:q!`, Enter (or `:cq` to abort the calling tool). [tip, §6;
  self-check]
- `closing-tab-ends-session`: "Closing the browser tab ends my OnDemand
  session." The job keeps its node until Cancel or the time limit
  (checked on Nova). [pitfall, §5; exercise 4] Added 2026-11-16.

## Links to other chapters and books

- Builds on: Chapter 1 (terminal, the FASTQ files in `~/bioinf-ch01`,
  laptop vs login node).
- Leads to: Chapter 3 (organizes `~/bioinf-computing` into the recurring
  project and brings the Chapter 1 files in); Chapter 7 (`PATH`,
  environment variables, permanent `EDITOR`); Chapter 9 (SSH keys,
  config, jump hosts; pitfall "Too many authentication failures" when
  `Host *` offers every key, seen on Nova and Atlas); Chapter 10 (login vs compute nodes, quotas; `df -h` shows shared
  filesystem size, not your limit);
  Chapters 12–13 (R and Python from the environment, editor interpreter
  setup); Chapter 23 (environments in depth, detached environments,
  alternatives to pixi); Appendix A (site routes and paths).

## Official links to include

- pixi: pixi.sh / pixi.prefix.dev (install, `pixi.toml`, lockfile,
  `pixi install --locked`, environment variables, VS Code integration)
- conda-forge: conda-forge.org; Bioconda: bioconda.github.io
- VS Code: code.visualstudio.com (macOS setup, WSL, Remote-SSH,
  troubleshooting, extension locations, tunnels)
- seqkit: bioinf.shenwei.me/seqkit (and its GitHub repo)
- GNU nano: nano-editor.org; Vim: vim.org / vimhelp.org (`:cq`)
- Open OnDemand: openondemand.org
- RStudio / Positron: posit.co; Jupyter: jupyter.org; Quarto: quarto.org
- OpenSSH: openssh.com; curl manual (`--fail`): curl.se
- Site VS Code guides: research.it.iastate.edu (Nova), scinet.usda.gov
  (SCINet); linked from Appendix A

## Further reading (candidates)

Final list: 3–6 annotated picks, cited by key (§9). Verify with scite /
fetch BibTeX from the DOI; items with no DOI get `url` + `urldate`.

- pixi documentation, "Getting started" and the manifest reference: the
  current install steps and every `pixi.toml` field.
- VS Code docs, "Remote Development using SSH": how the remote server
  works and its known limits.
- Grüning et al. 2018, "Bioconda: sustainable and comprehensive software
  distribution for the life sciences" (*Nature Methods*): why bioconda
  exists; verify with scite.
- Shen et al., SeqKit paper (*PLoS ONE* 2016): the tool used in the check;
  verify with scite.
- Shotts, *The Linux Command Line*: the chapter on editors (vi), for
  readers who want more than survival vim.

## Austin's notes

-

## Review responses (2026-11-13)

Codex (`chapter_02_codex_review.md`) and Antigravity
(`chapter_02_agy_review.md`). Accepted and applied above:

- Ship `pixi.toml` + `pixi.lock` from one tested release; install with
  `pixi install --locked`; record the tested pixi version; narrower key
  idea (same versions, not identical binaries across OSes).
- `check` task tests the environment only; `pixi run seqkit stats` is a
  separate, explicit command (also sets up exercise 2).
- Explain lookup by activation (`pixi run` / `pixi shell`), not by being
  in a folder; self-check rewritten to compare bare vs `pixi run` in the
  same folder.
- Site check before connecting a VS Code server; VS Code tunnels and
  compute-session routes in `tbl-where-to-edit` and `fig-remote-ssh`;
  ending allocated sessions; exercise 4 uses "your site's supported
  method".
- Windows: Windows VS Code app + WSL extension; Remote-SSH uses the
  Windows SSH client and config, added via *Add New SSH Host*.
- macOS one-time *Install 'code' command in PATH*; editor interpreter
  setup (Python, R + `languageserver`) deferred to Chapters 12–13.
- Extensions split local/remote; laptop files not copied to the remote.
- First-connection host-key prompt (`yes`, `known_hosts`) in the captured
  SSH session.
- `:cq` vs `:q!` for aborting a calling tool; `export EDITOR=nano`, this
  terminal only.
- `Terminal (laptop)` / `Terminal (login node)` labels; `curl -fLO` with
  a stop-on-failure checkpoint.
- One self-check per section (lockfile check moved to §2; new VS Code
  status-bar check for §3).
- `pixi add` marked as changing manifest and lockfile; sudo
  misconception narrowed; "never stop for installs" narrowed to core
  local examples.
- Measure download size, installed size, and file count before choosing
  the environment contents; `PIXI_CACHE_DIR` in the pitfall, detached
  environments deferred to Chapter 23 / Appendix A.

Not adopted:

- **Copying the Chapter 1 files into `~/bioinf-computing` in Chapter 2**
  (both reviews). Chapter 1 says Chapter 3 brings these files into the
  project; moving them here would put raw data in the folder root one
  chapter before Chapter 3 organizes it. Chapter 2 uses them in place in
  `~/bioinf-ch01/`. The reviews' main point, one book folder that
  Chapter 3 organizes, is adopted.

## Decisions (2026-11-13, open questions round)

- **Environment contents:** one environment for the core local examples
  (R, Python + pandas, seqkit, samtools, bedtools, bcftools, duckdb, …),
  plus pixi features for heavy parts (e.g., `workflows`, `align`),
  installed when those chapters arrive. Exact package list after
  measuring download size, installed size (`du -sh .pixi`), file count
  (`find .pixi | wc -l`), and `osx-arm64` availability.
- **Distribution:** two `curl -fLO` URLs for `pixi.toml` and `pixi.lock`,
  pinned to a tagged book release. Files live in `setup/` in the book
  repo (not the root, which is for building the book); URL pattern
  `https://raw.githubusercontent.com/austin-putz/book-bioinf-computing/<tag>/setup/pixi.toml`.
  Tag once the environment contents are settled.
- **Windows SSH:** two config files, said plainly. The Ubuntu terminal's
  `ssh` reads the WSL `~/.ssh/config`; VS Code Remote-SSH hosts are added
  with *Add New SSH Host* into the Windows-side config. The text names
  which file is which.

## Checked against official docs (2026-11-13)

- pixi: install command `curl -fsSL https://pixi.sh/install.sh | sh`,
  which adds `~/.pixi/bin` to `PATH` in the shell startup file (restart
  the terminal); manifest table is `[workspace]`; tasks run in
  `deno_task_shell`, which supports `&&` and `|`; `PIXI_CACHE_DIR` sets
  the cache (fallback `RATTLER_CACHE_DIR`); `install --locked` aborts if
  the lockfile is out of date with the manifest, rather than updating it
  (pixi.prefix.dev installation, manifest, advanced tasks,
  environment variables, `pixi install` reference).
- VS Code: install on the **Windows** side with the WSL extension, then
  `code .` from WSL; macOS command name as in §3; UI extensions run
  locally, most others on the remote host; *Add New SSH Host* asks which
  config file to write, and `remote.SSH.configFile` can point elsewhere
  (code.visualstudio.com remote/ssh, remote/wsl, setup/mac).
- Nova and SCINet VS Code routes, session ending, and code-server quota
  moves: as summarized in §5 (research.it.iastate.edu "Using VS Code on
  the cluster" and the May 19, 2026 maintenance notice;
  scinet.usda.gov/guides/ide/vscode, last updated 2025-12-12).

## Decisions (2026-11-13, second round)

- **Primary-setup wording:** "VS Code, connected to a cluster by the
  site's supported route (Remote-SSH, a VS Code tunnel, or Open
  OnDemand)". Updated in `CLAUDE.md`, `PLAN_CHAPTERS.md`, `index.qmd`,
  and the Chapter 2 stub.
- **Appendix A:** site VS Code routes, requirements, session ending, and
  the code-server quota move added as planned topics with official links
  (`appendices/a-cluster-sites.qmd`, `PLAN_CHAPTERS.md`).
- **Misconceptions:** the five Chapter 2 entries added to
  `misconceptions.yml` (a sixth on 2026-11-16, below).
- **nano fallback:** add `nano` (conda-forge) to the book environment so
  `pixi run nano` always works; vim is assumed present everywhere.

## Decisions (2026-11-13, bash on macOS)

- Chapter 2 follows Chapter 1's bash-everywhere setup: pixi's installer
  writes `~/.bashrc` (read via Chapter 1's `~/.bash_profile`); VS Code's
  terminal must open Homebrew bash, checked with `$BASH_VERSION` and
  `sed --version`; macOS readers `brew install nano` for GNU nano (macOS
  ships pico under that name), with `pixi run nano` still as the fallback.

## Trial install (2026-11-13)

Draft manifest above, pixi 0.84.2, macOS 15.7 Intel (`osx-64`), all
files kept in a scratch folder (`PIXI_HOME`, `PIXI_CACHE_DIR`,
`PIXI_NO_PATH_UPDATE`), nothing written to the real home directory.

- `pixi lock` solved all three platforms (`linux-64`, `osx-arm64`,
  `osx-64`) in under 2 s, so every draft package exists on each.
- `pixi install --locked`: 11 s on a warm network.
- `pixi run check` works, including the external `head` inside the task;
  versions: Python 3.12.16, R 4.4.3, seqkit 2.14.0, GNU nano 9.3.
- `pixi run seqkit stats` gives `num_seqs` 50,000, `sum_len` 5,050,000
  (output in *Outcome and check*).
- Bare `seqkit` in the same shell: `command not found` (the self-check
  and `installed-everywhere` misconception behave as written).
- **Size:** even this minimal environment is **1.1 GB** in `.pixi/` and
  **1.1 GB** in the cache, with **14,328** files in `.pixi/` and 18,490
  in the cache. `r-base` on macOS pulls in a compiler toolchain (clang,
  tapi, tk), which is most of it. So the "under ~1 GB" target in the
  environment decision cannot hold once R is in; the full core
  environment will be larger. The compute note must give real numbers,
  and the cluster pitfall (cache and `.pixi/` file counts against home
  quotas) matters more than planned.
- The installer sends an anonymous install ping (version, OS, arch) to
  prefix.dev; `PIXI_NO_TELEMETRY=1` turns it off. Mention in one line.
- macOS `/usr/bin/nano` is a link to UW PICO 5.09, confirming the `brew
  install nano` step.

### Linux run (2026-11-14, WSL Ubuntu, ThinkPad E14, `linux-64`)

Austin ran the Part 4 script from `chapter_02_checks.md` (`pixi install`
without `--locked`, fresh solve), pixi 0.84.2, `x86_64`, no errors or
warnings.

- Install: `real 0m9.779s`.
- Same versions and `seqkit stats` output as on macOS (Python 3.12.16,
  R 4.4.3, seqkit 2.14.0; 50,000 reads, 5,050,000 bases).
- **Size: 1.3 GB** in `.pixi/` with **15,524** files; the cache shows
  only **132 MB** (19,858 files).
- Why the cache looks small on Linux but was 1.1 GB on macOS: on Linux
  the environment's files appear to be **hard links** to the cache's
  copies, so `du` counts them once (under `.pixi`) and the cache shows
  only what isn't linked (likely the downloaded archives). On the Mac
  each file has a link count of 1 (copies or APFS clones), so `du`
  counted the data in both places. Real disk use on Linux is about
  **1.4 GB in total**, not 1.3 + 1.3. (Confirmed on Ceres: 12,408 linked
  files; see *Cluster run*.)
- **Cluster consequence:** hard links only work within one filesystem.
  If the cache stays in `$HOME` and the project is in `/project` or
  `/work`, every file is copied and the space (and file count) doubles,
  with the copy landing in the small home quota. So the §2 pitfall should
  say: put `PIXI_CACHE_DIR` on the **same** storage as your projects.

### Cluster run (2026-11-14, SCINet Ceres compute node, `linux-64`)

Same script, run in the terminal of an Open OnDemand VS Code Server
session on `ceres20-compute-2`, with the base folder (and cache) in
`/project/<project>/`. pixi 0.84.2, `x86_64`, no errors.

- **Install time not usable:** `real 8m23.733s`, but Austin opened the
  project folder in VS Code mid-run (which restarts the terminal), so
  the time includes an interrupted attempt and a restart. CPU time was
  only ~22 s. Re-time on a clean run if the number is needed.
- **Reinstall from the cache (no downloads):** `rm -rf .pixi && time
  pixi install` took **`real 0m57.127s`** (`user 0.9 s`, `sys 1.2 s`),
  versus 9.8 s for a *full* install, downloads included, on WSL. So
  writing ~15,500 files to project storage alone takes about a minute,
  almost all of it waiting on the filesystem. A first install with
  downloads will be at least that, likely a few minutes.
- Same versions and `seqkit stats` output as on macOS and WSL.
- **Size: 1.3 GB** in `.pixi/`, 15,524 files; cache 114 MB, 19,858 files.
- **Hard links confirmed:** 12,408 of the env's files have a link count
  above 1 (`find .pixi -type f -links +1`), so env and cache share one
  copy when they are on the same filesystem.
- **Chapter consequences:** still warn (Austin's call) that the first
  install on a cluster can be slow, since shared storage is slow with
  many small files, and is not stuck; run it on a compute node
  (OnDemand terminal or `salloc`), not a login node; it happens once,
  and later `pixi run` calls start without reinstalling.

## Hands-on checks (2026-11-14 to 16)

Austin's results, recorded in full in `chapter_02_checks.md`; the
sections above now use them.

- **Windows/WSL (ThinkPad E14):** nano and vim present in fresh Ubuntu;
  `code` on PATH on both sides; `code .` opens `WSL: Ubuntu` with bash
  5.3; *Add New SSH Host* offers only Windows config files, even from a
  WSL window; Windows uses its built-in OpenSSH 9.5; Ubuntu has no
  `~/.ssh` until first use; pixi trial 9.8 s, 1.3 GB.
- **Atlas login node:** bash, nano 5.6.1, vim; Rocky Linux 9; `my_quotas`
  works (home 30 GB, no file-count column).
- **Ceres SSH (2026-11-16, Mac):** `step` installed and configured in
  three commands; first `ssh` opened the browser (already signed in to
  Login.gov) and reached `ceres-login-1`.
- **Nova (2026-11-16):** login node: bash, nano 5.6.1, vim; lands in
  home. First attempts failed with "Too many authentication failures"
  (a `Host *` block offering every key), fixed with per-host entries.
  First-login session captured (code before password). `quota -s`
  prints nothing and `df -h` shows shared sizes (home 14 TB, group
  `/work` 143 TB); ISU docs: home **10 GB**, `/work` quota per group
  (usage in `/work/<group>/group_storage_usage`), `/ptmp` short-term,
  `/lss` backed up but not on compute nodes, no file-count limit stated.
  OnDemand **VS Code Server** on compute node `nova18-69` in
  `/work/<group>/<netid>`; form differs from Ceres (Slurm Partition vs
  Queue/QOS, tasks per node vs cores, Extra Modules, Working Directory
  defaults to last used; code-server 4.97 vs 4.17). Cancel on the card
  ended it (tab closed by hand); closing the tab alone did not. pixi
  trial in `/work`: reinstall from cache **2.4 s** (Ceres 57 s),
  `.pixi` **813 MB** for the same 15,524 files (likely compressed
  storage), 12,408 hard links. A long pasted block broke in the browser
  terminal; short blocks worked.
- **Ceres:** `my_quotas` (home 29.8 GB; same projects as Atlas but
  separate storage and quotas; Juno `/LTS` listed); OnDemand VS Code on
  a compute node, form fields and Cancel behaviour as in §5; pixi trial
  in `/project` (1.3 GB, hard links confirmed, ~1 min reinstall from a
  full cache); code-server folder 976 KB.

## Final review (2026-11-16)

Both outside reviews (Codex, Antigravity) were handled on 2026-11-13
(*Review responses*); nothing in them is still open. This pass checked
the plan against all hands-on results and fixed:

- Learning goal 3, the §3 self-check, and `fig-vscode-window`: the
  status bar names the connection only in the desktop app; `hostname`
  is the universal check (browser VS Code shows only an icon).
- §4 restructured: Nova's captured first login (code before password),
  then one short paragraph per site; SCINet's `step` setup and its
  skipped `yes` prompt; the "no VPN" sentence now clearly about SCINet.
- §5: both sites' tested OnDemand forms, Cancel on the card (closing
  the tab does not end a session), short pasted blocks; the Nova
  "to confirm" note resolved.
- §2: storage names per site (`/project`, `/work`; scratch `/90daydata`,
  `/ptmp`); install time "seconds to minutes" in the pitfall.
- `fig-remote-ssh`: add the browser → OnDemand route, since both tested
  sites use it.
- Proposed misconception `closing-tab-ends-session`; Chapter 9 and 10
  forward links for the SSH-keys pitfall and the `df` misreading.
- Open questions trimmed to what is still open.

## Decisions (2026-11-16, final review)

- **Environment size:** keep R in the core environment and drop the
  "under ~1 GB" target. The chapter's compute note states measured
  numbers (about 1.3 GB and 15,500 files with R; less on compressed
  storage such as Nova's `/work`). Measure the full core package list
  before tagging the release.
- **File-count limits:** measure the full environment's file count
  first; ask SCINet support and ISU Research IT only if it is large.
- **code-server folder:** defer the symlink to Appendix A (§5 mentions
  it in one line); readers do it when they first install extensions on
  a cluster.
- **Misconception:** `closing-tab-ends-session` added to
  `misconceptions.yml`.
- **Optional checks** (Atlas OnDemand app list; one Apple Silicon
  install): later, not blocking. Do the Apple Silicon install before
  tagging the release if a Mac is available.

## Drafting notes (2026-11-16)

Chapter written from this plan. Choices made while writing:

- **Setup files:** `setup/pixi.toml` and `setup/pixi.lock` added to the
  repo (the draft manifest above; lock solved for all three platforms).
  The chapter's download URLs come from `setup-url` in `_variables.yml`,
  which points at `main` until the release is tagged; tagging then means
  changing one line. The pixi version shown is also there.
- **Outputs** are real, captured 2026-11-16 (macOS Intel, pixi 0.84.2):
  `pixi install --locked`, `pixi run check`, `pixi list`, bare `seqkit`
  not found. The `seqkit stats` path shows `/home/you/…`.
- **Compute note** numbers (1.3 GB, ~15,500 files, seconds to minutes)
  name `scripts/ch02_env_size.sh`, which installs the setup files into a
  scratch folder and prints time, size, file count, and hard links.
  Rerun it on the final environment before tagging.
- **SSH:** Nova's captured first login with the user name as `<netid>`
  and the banner shortened; Nova look-around output (`nova-login-2`,
  `/bin/bash`) with the `logout` lines in the form captured on Ceres.
  SCINet's `step` commands are not copied into the book (the CA
  fingerprint could change); the table links SCINet's SSH page instead.
- **Site differences** as one table (`tbl-ssh-sites`) instead of two
  paragraphs, to keep the section short.
- **Callouts:** the code-server folder note is plain text, not a
  callout, to stay under three per screen in §5.
- Figures: `pixi-parts` (stepped, 4 steps), `vscode-window`,
  `remote-ssh` (desktop and OnDemand routes), `vim-modes`.
- **Codex review of the draft** (`reviews/chapter_02_codex_review.md`,
  2026-11-16), all six findings accepted and fixed: host-key fingerprint
  check before `yes`; Open OnDemand *Shell Access* is a login node, so
  install from the VS Code app's terminal after `hostname`; the `check`
  task now uses `Rscript --version` (the old `R --version | head -n 1`
  hid an R failure: confirmed in pixi 0.84.2, `false | head` returned
  0); vim teaches `G` then `o` for a new line (`i` typed before line 1);
  recovery step if `~/bioinf-ch01` was deleted; official ISU/SCINet
  guides linked where Appendix A is still a stub. The plan's draft
  `pixi.toml` above still shows the old task; `setup/pixi.toml` is the
  current one.
- **Data transfer nodes** (Austin, 2026-11-17): §4 now says file
  transfers go to the site's DTN, not the login node (Nova
  `novadtn.its.iastate.edu`; SCINet `ceres-dtn.scinet.usda.gov`,
  `atlas-dtn.hpc.msstate.edu`, from ISU's and SCINet's transfer pages),
  with a DTN row in `tbl-ssh-sites`; commands stay in Chapter 9 (topic
  added to `PLAN_CHAPTERS.md`, the Chapter 9 stub, and Appendix A).
  ISU publishes Nova's host-key fingerprints; the captured ED25519
  fingerprint matches, and the chapter links the page.
- **`fig-ssh-basics`** (Austin, 2026-11-17, for the spring genomics
  course): a simple stepped SVG at the start of §4: Connect, Sign in,
  Command, Reply (laptop keeps keyboard and screen; commands run on the
  login node; output comes back; `exit` closes).
- Citations added: `gruning2018bioconda`, `shen2016seqkit` (verified
  with scite), `prefix2026pixi`, `microsoft2026remotessh` (url +
  urldate).

## Decisions (2026-11-17, from the Chapter 4 plan)

- **SeqKit citation:** cite both papers. `seqkit --help` asks users to
  cite SeqKit2 (Shen, Sipos & Zhao 2024, *iMeta*, doi:10.1002/imt2.191,
  verified with scite, BibTeX from the DOI as `shen2024seqkit2`). Added
  beside `shen2016seqkit` at first use and in Further reading.

## Open questions

- None blocking. Before tagging the release: measure the full core
  environment (size, file count; ask the sites about file limits if
  large), and the optional checks above.
