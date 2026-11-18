---
title: "Chapter 5 plan — Codex review"
subtitle: "Advisory review · corrections, gaps, and suggested improvements"
date: 2026-11-17
---

Reviewed [chapter_05.md](chapter_05.md) against the repository and series
instructions, [chapter outline](PLAN_CHAPTERS.md), chapter template,
shared theme style guide, written Chapters 1–4, and the Chapter 6–7
plans. Locations and line numbers refer to the plan as reviewed on
2026-11-17. The source plan and Austin's notes are unchanged.

**Overall assessment:** keep this structure. It meets the outline,
explains commands readers have already used, and gives paths, quoting,
and links appropriate attention. The shared practice tree is a good
choice. The main corrections concern the model of shell expansion,
the deletion-preview habit, and a chapter check that currently verifies
less than the stated outcome.

## Corrections before drafting

### 1. Make the shell's word handling accurate without teaching the full parser

**Priority: high. Locations:** section 2, lines 121–126; section 7,
lines 238–246; `fig-shell-steps`; section 2's key-idea callout.

“Split the line into words at spaces, expand `~`, wildcards, and `$…`”
is too loose as the central explanation. Bash recognizes quoted words
while parsing; expansion can subsequently change the number of arguments.
In particular, a matched filename containing spaces is **not split
again** into several arguments. Otherwise a reader could reasonably
conclude that `ls *` cannot handle `plot 1.png`.

Use a restricted but accurate explanation for the commands taught here:

> Bash recognizes words and operators, respecting quotes and escapes.
> It performs the permitted expansions, removes the syntactic quotes,
> and passes the resulting arguments to the command. Quoting controls
> which expansions and splitting can happen.

Do not call the initial recognition of words “word splitting” in the
figure: that term has a later, specific meaning for unquoted expansion
results. Leave its full treatment to Chapter 8. The
[Bash expansion rules](https://www.gnu.org/software/bash/manual/bash.html#Shell-Expansions)
provide the authoritative sequence.

Add one prediction using an existing name with spaces:

```bash
printf '<%s>\n' analysis/*
```

Each matched filename is one argument, including `analysis/plot 1.png`.
I checked this behavior with Bash 5.3.15. This also connects quoting to
the actual argument list, rather than making it a rule to memorize.

Correct the quoted-tilde callout too: `"~/data"` is a relative path
whose first component is literally `~`, not a folder whose whole name
is `~/data`. The slash still separates path components. The proposed
fixes `~/"My Data"` and `"$HOME/My Data"` are correct.

### 2. Preview the names being removed, including directory operands

**Priority: high. Locations:** section 5, lines 192–200; section 7,
lines 225–228; related pitfall/key-idea callouts.

“`ls` the exact names or pattern first, then edit `ls` to `rm`” needs
one qualification: ordinary `ls directory` shows the directory's
**contents**, while `rm -r directory` removes the directory and its
tree. With a wildcard that includes directories, the preview can obscure
which operands Bash actually supplied.

Teach this form when inspecting operands:

```bash
ls -d -- pattern
```

Here `pattern` means the actual unquoted glob the reader is inspecting.
`-d` lists directory operands themselves; `--` ends option parsing.
Keep the actual deletion example restricted to a disposable practice
file, and use `rm -i --` for that first deletion. Explain `--` once:
quotes preserve a filename as one argument, but do not stop a name
beginning with `-` from being interpreted as an option. `./name` is
another useful way to disambiguate a local name.

Keep Austin's decided `echo` prediction round. Change “safe way to
preview **any** pattern” to “a quick preview for these example names.”
`echo` flattens argument boundaries, so one name containing spaces and
several separate names can look identical. Its handling of names such
as `-n` can also be surprising. One `printf '<%s>\n' …` demonstration
is enough to show the boundaries; no new major section is needed.

### 3. Check the source cleanup as well as the new links

**Priority: high. Locations:** outcome/check, lines 67–80; exercise 3,
lines 471–480.

The proposed checks inspect only `tidy/`. They cannot establish that
`share/ref` was unlinked or that the source `.tmp` file was deleted,
although both are required by the exercise. They also do not establish
that each link points to the **correct** source: six working links to
the same read file would pass a simple link-count/broken-link check.

Keep the six expected link mappings, and add a source-tree inspection:

```bash
find ~/bioinf-computing-ch05/share \( -xtype l -o -name '*.tmp' \) -print
```

After the specified cleanup this should print nothing. Compare the
first check's targets against all six expected source paths, including
`Run 3 final`, and show that no extra ordinary files are in
`tidy/fastq/`. Say that the leading home-directory prefix will differ
by machine; “exact output” should mean the same relative mappings,
with the reader's own home path substituted.

This chapter uses `sort` in its check and `history | tail`, despite
the scope statement saying pipes occur only in previously encountered
commands. That is manageable: explicitly mark these as supplied checks
whose pipe mechanics are explained in Chapter 6, or remove the `sort`
and give an order-independent comparison. It is a boundary-description
issue, not a reason to move pipe teaching here.

### 4. Finish the practice-tree recipe and make repeat visits predictable

**Priority: medium. Locations:** section 1; section 7's hidden-file
example; examples/data, lines 498–567; open question 1.

The tree is still a specification, not a runnable setup block. Several
promised examples depend on details that do not yet line up:

- Section 7 runs in `share/run1`, but the listed hidden file is
  `share/.old_settings`; the captured `.hidden` is not in the proposed
  tree. Put a named hidden file in the directory used by that example,
  or run the hidden-file prediction from `share` and update its output.
- Tiny gzipped FASTQ files will generally be smaller than the
  `find -size +1k` threshold. Provide a deterministic larger toy file
  if the lesson needs a positive match. Say that `find -size` on a
  `.gz` measures the compressed file's size.
- All newly generated files have recent modification times. A
  `-mtime -1` example needs a stated observation time or a deliberate
  older example if it is meant to discriminate among files.
- The setup promise that sections 5–8 explain “every command” is
  inaccurate: gzip/pipes are Chapter 6, and the array/expansion syntax
  is explicitly not taught here. Say that later chapters explain the
  setup machinery and that readers can inspect the resulting files now.

Preserve the now-agreed table rows and their checksum. I independently
recreated the array/`printf` table and obtained MD5
`971d8f742cb76a8d181d3bdc3dcbceaa`, matching Chapters 5–6. Its nonadjacent
duplicate and space-containing field are useful teaching choices.

Because Chapters 6–8 reuse the tree, describe what happens when the
setup is pasted a second time. A naive `ln -s` will complain about an
existing link; rerunning the setup can also restore a deliberately
removed `.tmp` or broken link. Give a deliberate reset instruction for
book-created practice files, without automatically deleting an entire
possibly modified scratch directory. Later chapters should depend on
the fixture files, not on completing exercise 3.

Keep `~/bioinf-computing-ch05/share/`: Chapters 6–7 already use it, and
the repository's naming decision supports it. Close the stale question
about choosing the name in a future Chapter 6 planning session.

### 5. Either defer `find -delete` or teach its actual evaluation rule

**Priority: medium. Locations:** section 8, lines 255–275;
`tbl-find-tests`.

The useful core is already sufficient: starting directory, quoted
`-name`, `-type`, recursion depth, size/age, and grouped alternatives.
`-delete` and `-exec` are actions, not tests. “Tests are ANDed” should
say that adjacent tests are implicitly ANDed, while `-o` introduces OR.

If `-delete` stays, one sentence saying “preview without it first” is
not a complete rule. Its position matters, it suppresses the default
print action, and it implies depth-first traversal. Putting it before
the intended tests can delete far more than the reader meant. The
[GNU deletion documentation](https://www.gnu.org/software/findutils/manual/find.pdf)
explicitly discusses these traps.

Prefer mentioning it as a later capability without a runnable deletion
exercise here. If retained as practical teaching, give one tightly
bounded example with tests first, an explicit preview, and the action
last. Keep the regular cleanup exercise on `unlink` and `rm -i`.

### 6. Remove Pixi's manifest lookup from the working-directory probe

**Priority: medium. Locations:** `relative-to-script` misconception,
lines 602–607; section 3's wrong-folder explanation.

The misconception probe runs
`pixi run bash ~/bioinf-computing/src/01_count_reads.sh` from `~`, then
says the script looks for `~/data/raw`. With the intended setup, Pixi
first searches the working directory and its parents for a workspace
manifest. The manifest is in a **child** directory,
`~/bioinf-computing`, so Pixi normally refuses to run the script at all.
I reproduced that earlier failure with Pixi from a directory outside a
workspace: `could not find pixi.toml or pyproject.toml with tool.pixi`.

Keep Pixi's failure as the real-project diagnostic inherited from
Chapter 4. To test relative-path resolution itself, use plain Bash on
a tiny supplied script in scratch containing only `pwd` and a relative
`ls data/raw`, and invoke it by absolute path from another scratch
directory. That isolates the intended concept without requiring a
workspace, SeqKit, or Chapter 8 scripting knowledge. The general rule
about paths being relative to the current working directory is correct;
the current probe fails before it demonstrates that rule.

## Teaching and presentation improvements

### Keep a clear minimum path through a large chapter

Nine concept sections, six figures, ten tables, and six exercises could
be substantial for beginners. The sections are reasonable; prioritize
within them rather than adding more commands. Treat `readlink -f`,
`realpath`, brace ranges, `find` age/size filters, and history expansion
as recognition/reference material if the draft becomes too long.

Keep navigation, copy/move/delete, relative link targets, quoting,
globbing, and basic viewing as the first-pass spine. Continue using
supplied examples instead of asking readers to invent six link commands
from a blank prompt: show one completed mapping and let them adapt it.

### Distinguish filename matching from program-controlled patterns

The “program never sees the `*`” statement is correct for a successful
unquoted shell glob, not for all commands. `find -name '*.fastq.gz'`
deliberately receives the pattern and performs its own matching. Use
these two commands side by side; this will make the quoted-pattern
pitfall much easier to understand.

Keep unmatched glob behavior explicitly conditional on Bash's default
settings. The plan already recognizes `nullglob` as a Chapter 8 topic;
there is no need to teach it here.

### Make the viewing and completion claims modest

`head` is a good first look, but `less` is not a promise of constant
memory use for every input and action. Reading a regular file differs
from paging a decompression pipe, and searching or jumping to the end
can require reading far more input. Say “browse without loading the
whole file into an editor at startup,” rather than promising that
neither tool ever reads or retains the whole file.

Likewise, unsuccessful Tab completion is a clue, not proof that a name
does not exist: the prefix may be ambiguous, permissions can interfere,
and command-specific completion varies. `cd ~/bioi` is likely ambiguous
after several `bioinf-computing-chNN` folders exist. Use that to teach
the second Tab and typing a longer prefix.

### Keep the project-state handoffs explicit

The written Chapter 3 now supplies `data/ref/README.md`, a `seqkit:`
version line, and a `finished:` log line, so those dependencies are
sound. Exercise 4 should select a successful Chapter 3 log explicitly:
the newest log might instead be Chapter 4's deliberately failed run,
with no `finished:` line. Provide a short captured fallback.

The chapter says the project is read-only, but exercises ask readers to
write in its `NOTEBOOK.md`. Qualify that statement to distinguish data
inspection from the deliberate notebook entries; the practice mutations
still belong outside the project.

Keep figure colors consistent with the shared style guide: the current
directory can be highlighted with an outline/position, while `good`
means a check. File contents and reorganized data remain `given`.

## Verification and remaining limits

I checked argument preservation for globbed names with spaces, the
directory-preview distinction, and the toy-table checksum locally using
Bash 5.3.15 and GNU coreutils 9.11 on macOS. Documentation checks used
official Bash and GNU findutils sources. No source plan, chapter text,
environment, or user startup file was modified.

The complete practice-tree builder is not supplied yet, so its full
exercise sequence still needs an end-to-end run. The planned
Ubuntu/WSL and Nova captures, availability of `zless`, and site-specific
completion behavior remain drafting checks; this review does not claim
to have verified them on those systems.
