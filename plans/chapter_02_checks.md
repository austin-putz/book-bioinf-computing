---
title: "Chapter 2 — Hands-on checks for Austin"
subtitle: "Step-by-step: Windows, SCINet, Nova, Apple Silicon"
date: 2026-11-13
---

These are the checks from `chapter_02.md` (*Open questions*) that need a
real Windows PC or a cluster account. Each part stands alone: do them in
any order, skip what you can't do yet, and write results in the table at
the end. Nothing here changes anything permanent: all test files go in a
folder you delete afterwards.

**Notes for Austin:** Austin is new to Windows and SCINet, so every step
is spelled out. If something on screen doesn't match what's written here
(menus move between versions), write down what you saw. That's useful for
the chapter too, because readers will hit the same thing. Where a step
says "your site's docs", the official page is linked; follow it and
record what it asked you to do.

---

## Part 1 — Windows PC

Needs: a Windows 10 or 11 PC you can install software on (admin rights for
step 1.1). About 45–60 minutes the first time, mostly waiting.

### 1.1 Install WSL and Ubuntu (skip if already done)

1. Click **Start**, type `PowerShell`, right-click **Windows PowerShell**,
   choose **Run as administrator**, and click **Yes**.
2. In the blue window, type this and press Enter:

   ```
   wsl --install
   ```

3. When it finishes, **restart the PC**.
4. After the restart, an **Ubuntu** window opens by itself (if not:
   Start → type `Ubuntu` → open it). It asks for a new **UNIX username**
   and **password**. Pick anything simple; this is only for Ubuntu. When
   you type the password nothing appears on screen; that's normal.
5. You now see a prompt ending in `$`. This is the Linux terminal the book
   calls "Terminal (laptop)" on Windows.

Official steps: <https://learn.microsoft.com/en-us/windows/wsl/install>

### 1.2 Check nano and vim in Ubuntu

In the Ubuntu window, type each line and press Enter:

```bash
which nano vim
nano --version | head -n 1
vim --version | head -n 1
```

**Record:** the three outputs. If `which` prints a path for each (like
`/usr/bin/nano`), both exist. If one prints nothing, it is missing.

### 1.3 Install VS Code on the Windows side

1. In a web browser go to <https://code.visualstudio.com/> and download
   **VS Code for Windows** (the big blue button).
2. Run the installer. On the **Select Additional Tasks** page, make sure
   **Add to PATH** is ticked. Keep everything else as offered.
3. Open VS Code from the Start menu.

Do **not** install VS Code inside Ubuntu; the Windows copy talks to
Ubuntu through an extension.

### 1.4 Install the two extensions

1. In VS Code, click the **Extensions** icon on the left edge (four small
   squares), or press `Ctrl+Shift+X`.
2. Search `WSL` and install **WSL** (publisher: Microsoft).
3. Search `Remote - SSH` and install **Remote - SSH** (publisher:
   Microsoft).

### 1.5 Check `code .` from Ubuntu

1. Close VS Code. In the **Ubuntu** window type:

   ```bash
   mkdir -p ~/vscode-test && cd ~/vscode-test
   code .
   ```

2. A VS Code window should open. Look at the **bottom-left corner**: it
   should say something like `WSL: Ubuntu`.
3. In VS Code, open a terminal: menu **Terminal → New Terminal**. Type
   `echo "$BASH_VERSION"` and `pwd`.

**Record:** did `code .` work the first time? What did the bottom-left
corner say? What did the two commands print?

### 1.6 The main question: which SSH config does Remote-SSH write?

You don't need a working cluster login for this part; we only want to see
which file VS Code uses.

1. In VS Code (any window), press `Ctrl+Shift+P` to open the **Command
   Palette** (a search box at the top).
2. Type `Remote-SSH: Add New SSH Host` and press Enter.
3. It asks for an SSH command. Type a made-up one:

   ```
   ssh testuser@example.org
   ```

4. It then asks **which SSH configuration file to update**, showing a
   list of paths. **Record every path in that list exactly** (a phone
   photo is fine). Pick the first one.
5. Now press `Ctrl+Shift+P` again, type `Remote-SSH: Open SSH
   Configuration File`, press Enter, and again **record the list of
   paths**. Pick the same one; the file opens, and you should see a
   `Host example.org` entry. Delete those lines and save (`Ctrl+S`).
6. Open **PowerShell** (not as administrator) and type:

   ```
   where.exe ssh
   ssh -V
   ```

   **Record both outputs.** This tells us which SSH program Windows uses
   (expected: `C:\Windows\System32\OpenSSH\ssh.exe`).
7. In the **Ubuntu** window type `ls -la ~/.ssh`, and record whether it
   exists. This shows that Ubuntu has its own, separate SSH folder.

What we expect (to confirm): VS Code writes to
`C:\Users\<you>\.ssh\config`, which is **not** the same file as Ubuntu's
`~/.ssh/config`. That's the "two config files" the chapter explains.

### 1.7 (Optional) Try the pixi trial in Ubuntu

If you have time, run Part 4 inside the Ubuntu window. It measures the
book environment on Linux without a cluster.

### 1.8 Clean up

In Ubuntu: `rm -rf ~/vscode-test`. Keep WSL and VS Code if you want them.

---

## Part 2 — SCINet (Ceres)

Needs: a SCINet account (apply through your PI or USDA contact; approval
can take a while). SCINet requires multi-factor authentication. Read
these official pages first; they change, so follow them over anything
here:

- Getting started / account: <https://scinet.usda.gov/guides/start>
- Accessing SCINet (hub): <https://scinet.usda.gov/guides/access/>
- SSH login: <https://scinet.usda.gov/guides/access/ssh-login>
- Open OnDemand: <https://scinet.usda.gov/guides/use/open-ondemand>
  (the Ceres site itself: <https://ceres-ondemand.scinet.usda.gov/>)
- VS Code on Ceres: <https://scinet.usda.gov/guides/ide/vscode>
- Storage locations: <https://scinet.usda.gov/guides/data/storage>
- Quotas (`my_quotas`):
  <https://scinet.usda.gov/guides/data/project-management>

(Links checked 2026-11-13.) SCINet's own advice is that for most work
you do **not** need SSH: Open OnDemand in a browser is the recommended
way in. So if SSH setup gets stuck, do 2.3 (Open OnDemand) first; its
shell and VS Code apps let you do 2.2 and 2.4 too.

**Notes for Austin:** if any link above has moved, start from
<https://scinet.usda.gov/guides/> and record the new address.

### 2.1 First login with SSH

1. Open a terminal on your Mac.
2. Follow the SSH login page. SCINet's SSH sign-in is not a plain
   password: it uses a small program called **step** (SmallStep CLI) that
   opens the USDA eAuthentication page in your browser (LincPass/AltLinc,
   or Login.gov for non-USDA users), about once a day. The page explains
   how to install and set it up; on the Mac it will likely be a Homebrew
   install. **Record each setup step** you had to do; readers will need
   the same list in Appendix A.
3. Then log in with:

   ```bash
   ssh your.username@ceres.scinet.usda.gov
   ```

4. The first time, SSH asks *Are you sure you want to continue
   connecting (yes/no/[fingerprint])?* Type the full word `yes`.
5. Complete the browser sign-in if it asks.

**Record:** the exact prompts you saw, in order (copy them from the
terminal, removing anything secret like codes). This becomes the captured
session in Chapter 2 §4, so it is valuable.

### 2.2 Look around (on the login node)

```bash
hostname
echo "$SHELL"
which nano vim
nano --version | head -n 1
```

Then check storage. Home directories have a 30 GB quota; your project
directory is under `/project/<project_name>/`. Run:

```bash
my_quotas
```

Record the output for home and project (bytes, and files if shown).

### 2.3 VS Code through Open OnDemand

Follow the VS Code guide (link above), **Method 1: VS Code Server in Open
OnDemand**:

1. Log in to Open OnDemand in a browser:
   <https://ceres-ondemand.scinet.usda.gov/>.
2. Start the **VS Code** app; choose a small request (e.g., 1–2 cores,
   1–2 hours) and your project account if asked.
3. When it says **Running**, click **Connect**. VS Code opens in the
   browser.
4. Open a terminal inside it (☰ menu → Terminal → New Terminal) and run
   `hostname`. It should be a compute node, not a login node.
5. **End the session:** back in Open OnDemand, go to **My Interactive
   Sessions** and click **Cancel** on the VS Code session.

**Record:** each screen's choices (a few screenshots help), the
`hostname` output, and confirm that Cancel ended it. Also note whether
the guide told you to move `~/.local/share/code-server` to project
storage, and whether you did.

(Optional: Method 2, the registered tunnel, needs a Microsoft account;
try it only if Method 1 is done.)

### 2.4 pixi trial on Ceres

Do Part 4 on a **compute node**, not the login node. Start an interactive
job first (SCINet's docs give the exact command; it looks like
`salloc` or `srun --pty bash` with a time limit), and use your project
directory as the base folder. Type `exit` when done to release the node.

---

## Part 3 — Nova (ISU)

Needs: a Nova account and the ISU network (on campus or the ISU VPN).
Official pages:

- VS Code on Nova: <https://research.it.iastate.edu/using-vs-code-cluster>
- Remote IDEs on compute nodes:
  <https://research.it.iastate.edu/launching-remote-ides-novas-compute-nodes>
- Nova main docs: <https://research.it.iastate.edu/> (search "Nova")

Same steps as Part 2, with Nova's names:

1. **SSH login** (record the prompts, as in 2.1).
2. **Look around** (2.2): `hostname`, `echo "$SHELL"`, `which nano vim`,
   and your `/work/<group>/<user>` space and quota.
3. **VS Code:** use the **VS Code Tunnel** app or **VS Code Server** app
   in Nova's Open OnDemand (first link). Run `hostname` in its terminal;
   record how you close or end it (the tunnel app allows ten
   connections; old ones are closed by right-click).
4. **pixi trial** (Part 4) on a compute node, in `/work/...`.

---

## Part 4 — pixi trial (any Linux or Mac)

This installs pixi and the draft book environment into **one test
folder** and measures it. It does not edit your `.bashrc`, and it keeps
pixi's cache in the test folder too, so it doesn't use home-directory
quota. Works in WSL Ubuntu, on a cluster compute node, or on an Apple
Silicon Mac.

1. Choose the base folder:
   - WSL or Mac: your home folder, `~`
   - SCINet: your project directory, e.g. `/project/<project_name>/<you>`
   - Nova: your work directory, e.g. `/work/<group>/<you>`
2. Copy this whole block, change the `BASE=` line, and paste it into the
   terminal:

   ```bash
   BASE=~                                   # <- change on a cluster
   T="$BASE/pixi-trial"
   mkdir -p "$T" && cd "$T"
   export PIXI_HOME="$T/pixi-home" PIXI_CACHE_DIR="$T/cache"
   export PIXI_NO_PATH_UPDATE=1 PIXI_NO_TELEMETRY=1
   curl -fsSL https://pixi.sh/install.sh | sh
   export PATH="$PIXI_HOME/bin:$PATH"
   mkdir -p book && cd book
   cat > pixi.toml <<'EOF'
   [workspace]
   name = "bioinf-book"
   channels = ["conda-forge", "bioconda"]
   platforms = ["linux-64", "osx-arm64", "osx-64"]

   [dependencies]
   python = "3.12.*"
   r-base = "4.4.*"
   seqkit = "*"
   nano = "*"

   [tasks]
   check = "python --version && R --version | head -n 1 && seqkit version"
   EOF
   curl -fLO https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq/testdata/GSE110004/SRR6357070_1.fastq.gz
   time pixi install
   pixi run check
   pixi run seqkit stats SRR6357070_1.fastq.gz
   echo "--- sizes"
   du -sh .pixi "$PIXI_CACHE_DIR"
   echo "files in .pixi:  $(find .pixi | wc -l)"
   echo "files in cache:  $(find "$PIXI_CACHE_DIR" | wc -l)"
   uname -m; pixi --version
   ```

3. Copy **everything it printed** from `pixi --version` downwards (and
   the `real` time line) into the results table, or paste it into a text
   file for me.
4. Clean up:

   ```bash
   cd ~ && rm -rf "$T"
   ```

   (On a cluster, also type `exit` to end the interactive job.)

What we expect: the check prints Python 3.12, R 4.4 and seqkit; `seqkit
stats` shows `50,000` reads and `5,050,000` bases. On an Intel Mac the
environment was 1.1 GB with about 14,000 files; the cluster numbers tell
us whether that is a problem for home and project quotas.

---

## Part 5 — Apple Silicon Mac (optional)

If you can borrow an M-series Mac (Apple menu → About This Mac says
"Apple M1/M2/…"), run Part 4 there with `BASE=~`. Record the output and
`uname -m` (should say `arm64`).

---

## Results

Fill in what you can; "not done" is fine. Paste long outputs below the
table or send them as text files.

| Check | Where | Result |
|:------|:------|:-------|
| nano / vim present | WSL Ubuntu | |
| `code .` opens VS Code, status bar text | WSL | |
| Config file list from *Add New SSH Host* | Windows VS Code | |
| `where.exe ssh`, `ssh -V` | Windows PowerShell | |
| First SSH login prompts (secrets removed) | SCINet | |
| First SSH login prompts (secrets removed) | Nova | |
| nano / vim present, `$SHELL` | SCINet login node | |
| nano / vim present, `$SHELL` | Nova login node | |
| Home and project quota (bytes, files) | SCINet | |
| Home and work quota (bytes, files) | Nova | |
| VS Code route used, `hostname`, how ended | SCINet | |
| VS Code route used, `hostname`, how ended | Nova | |
| pixi trial: time, sizes, file counts | WSL | |
| pixi trial: time, sizes, file counts | SCINet | |
| pixi trial: time, sizes, file counts | Nova | |
| pixi trial | Apple Silicon | |

## Questions or surprises

- (write anything confusing here; it probably belongs in the chapter)
