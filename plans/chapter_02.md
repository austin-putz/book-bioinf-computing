---
title: "Chapter 2 — Book setup and editors"
subtitle: "Chapter plan · core · draft"
date: 2026-11-13
---

**Part:** I — Getting set up · **Label:** core · **Status:** draft, revised
after the Codex and Antigravity reviews and the open-questions round
(2026-11-13; see *Review responses* and *Decisions*)

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
- **Check:** two commands from `~/bioinf-book`:
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
   tell from the status bar where it is connected.
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
   `~/bioinf-book`, download `pixi.toml` and `pixi.lock` from one fixed
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
   (solving, `PATH`) deferred to Chapters 7 and 23. [`fig-pixi-parts`,
   `tbl-pixi-commands`; key idea; pitfall: cluster cache; misconception
   callout "installed everywhere"; self-check]
3. **VS Code: a home for your work.** *Start hands-on:* install VS Code
   (OS tabset). macOS: open the Command Palette (`Cmd-Shift-P`), type
   `shell command`, and run *Shell Command: Install 'code' command in
   PATH* once (newer releases label it *Install 'code' and optionally
   'copilot' commands in PATH*), then reopen the terminal. Windows:
   install the normal **Windows** application plus its WSL extension;
   never a second Linux copy inside Ubuntu; open the folder with `code .`
   from the Ubuntu terminal. Linux: `code` is on `PATH` after install.
   File → Open Folder works everywhere. Open `~/bioinf-book`, open the
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
   Ubuntu`, later `SSH: <host>`). Extensions the book uses, installed now
   from one table. Pointing the Python and R extensions at the pixi
   environment is deferred to Chapters 12–13, where readers first need it
   (the R extension also needs the `languageserver` package there).
   [`fig-vscode-window`, `tbl-vscode-extensions`; tip: `code .`;
   self-check]
4. **Just enough SSH.** *Start hands-on:* `ssh user@host` from the laptop
   terminal, `hostname`, `exit`. The captured `.console` session includes
   the first-connection host-key prompt, annotated: type the full word
   `yes` (OpenSSH rejects `y`), after which the host is remembered in
   `~/.ssh/known_hosts`. Then MFA if the site uses it (site details in
   Appendix A, `@sec-cluster-sites`). SCINet's SSH login
   (`ceres.scinet.usda.gov`) first needs the SmallStep `step` program
   and a browser eAuthentication sign-in about once a day, and SCINet
   recommends Open OnDemand over SSH for most work; so SCINet readers
   may do §5 through Open OnDemand before setting up SSH (checked
   2026-11-13, scinet.usda.gov/guides/access/ssh-login). Then a minimal `~/.ssh/config` entry
   (`Host`, `HostName`, `User`) so a short name works. Windows: say which
   home holds which config: the Ubuntu terminal uses the WSL file
   (`~/.ssh/config` in Linux); VS Code's Remote-SSH uses the Windows SSH
   client and its own config file (section 5). Keys, jump hosts, and
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
     nodes unusable". Open OnDemand needs the campus network or VPN.
   - **SCINet (Ceres):** VS Code Server in Open OnDemand, or a registered
     tunnel started from the OnDemand "VS Code Tunnel" app, both on
     compute nodes. Tunnels need a Microsoft or GitHub account (USDA:
     Microsoft). Remote-SSH is not mentioned.

   *Then hands-on:* readers with a site route (SCINet, Nova, many
   universities) follow its Appendix A recipe: start the OnDemand app or
   tunnel, open a folder in project space, open a terminal, run
   `hostname` (a compute node). Readers on sites that allow it use
   Remote-SSH (Connect to Host → pick the host → open a folder → terminal
   → `hostname`); Windows readers add the host with *Remote-SSH: Add New
   SSH Host*, which asks which config file to write (on Windows normally
   `C:\Users\<you>\.ssh\config`; *Remote-SSH: Open SSH Configuration
   File…* shows which one VS Code uses). Both routes are
   shown as captured sessions for no-cluster readers. *Then name the
   idea:* the window is local; a VS Code server runs on the remote
   machine, with the files and terminal. Extensions split: UI ones
   (themes) stay local, most others run remotely; in browser code-server
   the extension catalogue may be Open VSX rather than Microsoft's.
   Laptop files and the laptop's pixi environment are **not** copied to
   the cluster. A compute session holds resources: end it when done (on
   SCINet, *My Interactive Sessions* → Cancel); closing the window does
   not release it. The server and its extensions live in your home
   directory (`~/.vscode-server` for Remote-SSH, `~/.local/share/
   code-server` for OnDemand) and can exceed the home quota; both sites
   move the code-server folder to project storage with a symlink
   (recipe in Appendix A). [`fig-remote-ssh`, `tbl-where-to-edit`;
   misconception callout "runs on my laptop"; pitfall: login-node
   limits; self-check]
6. **Editing in the terminal: nano and vim.** macOS first (one line in an
   OS note, not a tabset): macOS's `nano` is really pico, so run `brew
   install nano` to get GNU nano, the same editor as on Linux and the
   cluster (`nano --version` says GNU nano). *Start hands-on:* `nano
   notes.txt`, type a line, save (`Ctrl-O`, Enter), quit (`Ctrl-X`),
   `cat notes.txt`. Then vim, only enough to survive: open, `i` to type,
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
| `fig-vscode-window` | 3 | static | Schematic (not a screenshot) of the VS Code window with four labelled areas: explorer, editor, terminal panel, status bar. The status bar's left end reads `WSL: Ubuntu` or `SSH: <host>`, so the same figure reads for local and remote work. |
| `fig-remote-ssh` | 5 | static | Laptop (VS Code window, UI extensions, local files) → SSH → generic remote host running the VS Code server (remote files, terminal, language extensions), with local and remote files labelled separately. Two remote targets: a login node and an allocated compute node, the second marked as the route many sites require. Reuses the shapes from `fig-cluster-anatomy` (Chapter 1). |
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
| 2 | Pitfall | On a cluster, pixi's download cache defaults to your home directory and can fill its quota; set `PIXI_CACHE_DIR` to project storage (site paths in Appendix A). Moving the cache does not move `.pixi/envs/`; that option (detached environments) is in Chapter 23 |
| 3 | Tip | `code .` opens the current folder in VS Code (from the Ubuntu terminal on Windows; on macOS after the one-time *Install 'code' command* step) |
| 5 | Misconception | "With Remote-SSH, my code runs on my laptop" |
| 5 | Pitfall | Check your site's VS Code route before connecting; many sites (including Nova and SCINet) keep VS Code off login nodes. End compute sessions when done, and move the VS Code/code-server folder out of `$HOME` if your site says to |
| 6 | Tip | Stuck in vim? Press `Esc`, type `:q!`, press Enter (`:cq` if you want the tool that opened vim, such as `git commit`, to stop) |

Misconceptions without a callout ("I need sudo to install these tools",
"I need RStudio for R / Jupyter for Python") are handled in the text and
in self-checks.

### Self-checks and exercises (§4)

Self-checks (`.check` blocks with collapsed answers), one per concept
section:

- §2 (a): In a fresh terminal in `~/bioinf-book`, `seqkit stats …` says
  `command not found`, but `pixi run seqkit stats …` works. You have not
  installed seqkit any other way. Why? (*Installing the environment does
  not put its tools in every terminal; `pixi run` runs the command with
  the environment, or start `pixi shell`.*)
- §2 (b): Which file says exactly which version of each package you have:
  `pixi.toml` or `pixi.lock`? (*`pixi.lock`; `pixi.toml` says what the
  project needs, often as a range.*)
- §3: Where in the VS Code window can you see, at a glance, whether you
  are working on your own computer, in WSL, or on a remote machine? (*The
  left end of the status bar.*)
- §4: After `ssh` you type `hostname` and see a login-node name. Which
  computer runs your next command? (*The cluster's login node.*)
- §5: In a remote window you open a terminal and run `ls`. Whose files do
  you see, and is `~/bioinf-book` there? (*The cluster's; your laptop
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
3. In nano, create `README.md` in `~/bioinf-book` with one line saying
   what the folder is for. Then open it in vim, add a second line, and
   save with `:wq`. Run `cat README.md` in VS Code's terminal to check
   both lines.
4. (Cluster readers) Open a folder on your cluster using your site's
   supported method (Appendix A), open a terminal there, and run
   `hostname` and `pwd`. Record where you landed, and end the session if
   it allocated resources. (No-cluster readers: answer from the captured
   session.)

## Examples and data

- Toy example: `notes.txt` / `README.md` for the editor sections, one or
  two lines, so readers can check by eye that the save worked.
- Running dataset (yeast nf-core/rnaseq test data): `SRR6357070_1.fastq.gz`
  (and `_2` from Chapter 1's exercise), used **in place** in
  `~/bioinf-ch01/` (2,239,317 bytes, 50,000 reads of 101 bases, verified
  2026-11-13). Chapter 2 does not move data: Chapter 1 promises that
  Chapter 3 brings these files and their source URLs into the project,
  and Chapter 3 does so inside `~/bioinf-book`.
- Folder plan: `~/bioinf-book` is created here and holds `pixi.toml`,
  `pixi.lock`, and the README from exercise 3. Chapter 3 organizes the
  same folder into the recurring project (`data/`, `src/`, `results/`,
  …), so `pixi.toml` stays at the project root for the whole book.
- Draft `pixi.toml` (content to be settled; see open questions). The
  author solves it and publishes it with its `pixi.lock` from one tested
  book release; `pixi lock` across the three platforms is also the build
  check that every package exists on each.

  ```toml
  [workspace]
  name = "bioinf-book"
  channels = ["conda-forge", "bioconda"]
  platforms = ["linux-64", "osx-arm64", "osx-64"]

  [dependencies]
  python = "3.12.*"
  r-base = "4.4.*"
  seqkit = "*"
  nano = "*"                 # fallback editor (pixi run nano)

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
  mkdir -p ~/bioinf-book && cd ~/bioinf-book
  curl -fLO <book release URL>/pixi.toml         # one fixed release
  curl -fLO <book release URL>/pixi.lock
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

## Links to other chapters and books

- Builds on: Chapter 1 (terminal, the FASTQ files in `~/bioinf-ch01`,
  laptop vs login node).
- Leads to: Chapter 3 (organizes `~/bioinf-book` into the recurring
  project and brings the Chapter 1 files in); Chapter 7 (`PATH`,
  environment variables, permanent `EDITOR`); Chapter 9 (SSH keys,
  config, jump hosts); Chapter 10 (login vs compute nodes, quotas);
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

- **Copying the Chapter 1 files into `~/bioinf-book` in Chapter 2**
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
  pinned to a tagged book release.
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
  `misconceptions.yml`.
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

## Open questions

- **Environment size target:** with R alone the environment is 1.1 GB
  and ~14k files on macOS. Keep R in the core environment and drop the
  1 GB target, or move R (or its heavy dependencies) into a feature?
  Measure `linux-64` (cluster) and the full core package list first.
- **Step-by-step guide for the checks below:**
  `chapter_02_checks.md` (Windows, SCINet, Nova, pixi trial script,
  results table).
- **Needs Austin (Windows machine):** run *Remote-SSH: Add New SSH Host*
  in Windows VS Code, record which config file it writes and whether the
  Windows OpenSSH client is used; in WSL Ubuntu, run `which nano vim` (or
  `dpkg -l nano vim-tiny`), since the WSL docs do not list packages.
- **Needs Austin (Nova, SCINet):** `which nano vim` on a login node; a
  trial `pixi install --locked` in project space to measure `linux-64`
  size and file count; confirm the VS Code routes with a real session,
  including how to end each.
- **Apple Silicon:** solved in the lockfile but not installed; one run on
  an `osx-arm64` Mac if one is available.
