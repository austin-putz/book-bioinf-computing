"""Render a book's manim clips into assets/video/. Shared by every book.

Manim never runs inside `quarto render`. A book keeps scene modules and a
small `manim/build.py` holding its MANIFEST, which calls ``main()``:

    python manim/build.py            # re-render only what is out of date
    python manim/build.py rnaseq     # only stems starting with "rnaseq"
    python manim/build.py --draft    # 480p preview, nothing copied

Each clip gives `assets/video/<stem>.mp4` and `<stem>.png`, the poster:
the final frame, which is what a reader sees before pressing play.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
MAX_INLINE_SECONDS = 90   # longer clips are chapter features; warn anyway


def find_manim(manim_dir: Path) -> list[str]:
    """A book-local venv first, then the author's shared one, then PATH."""
    for c in (manim_dir / "venv" / "bin" / "manim",
              Path.home() / "Claude" / "manim_test" / "venv" / "bin" / "manim"):
        if c.exists():
            return [str(c)]
    return ["manim"]


def objective(manim_dir: Path, module: str, scene: str) -> str | None:
    """Every clip states its learning objective in its docstring."""
    src = (manim_dir / f"{module}.py").read_text()
    m = re.search(rf"class {scene}\(.*?\):\s*\"\"\"(.*?)\"\"\"", src, re.S)
    if not m:
        return None
    hit = re.search(r"Objective:\s*(.+)", m.group(1))
    return hit.group(1).strip() if hit else None


def up_to_date(manim_dir: Path, out: Path, module: str, stem: str) -> bool:
    mp4, png = out / f"{stem}.mp4", out / f"{stem}.png"
    if not (mp4.exists() and png.exists()):
        return False
    sources = [manim_dir / f"{module}.py", *PKG.glob("*.py")]
    newest = max(p.stat().st_mtime for p in sources)
    return min(mp4.stat().st_mtime, png.stat().st_mtime) > newest


def duration(mp4: Path) -> float | None:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=nw=1:nk=1", str(mp4)],
                           capture_output=True, text=True, check=True)
        return float(r.stdout.strip())
    except Exception:
        return None


def render(manim_dir: Path, out: Path, module: str, scene: str, stem: str,
           draft: bool) -> None:
    media = manim_dir / "media"
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(PKG.parent),
                                                      env.get("PYTHONPATH")]))
    quality = ["-ql"] if draft else ["-r", "1920,1080"]
    cmd = find_manim(manim_dir) + quality + [
        "--fps", "30", "--format=mp4", "--media_dir", str(media),
        f"{module}.py", scene]
    print(f"  rendering {scene} -> {stem}.mp4" + ("  (draft)" if draft else ""))
    subprocess.run(cmd, cwd=manim_dir, env=env, check=True)

    hits = sorted((media / "videos" / module).rglob(f"{scene}.mp4"),
                  key=lambda p: p.stat().st_mtime)
    if not hits:
        sys.exit(f"ERROR: no mp4 produced for {scene}")
    mp4 = hits[-1]
    if draft:
        print(f"    draft: {mp4}")
        return

    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mp4, out / f"{stem}.mp4")
    # The poster is the last frame of the finished video, so it can never
    # disagree with what the clip ends on.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1",
                    "-i", str(out / f"{stem}.mp4"), "-frames:v", "1",
                    "-update", "1", str(out / f"{stem}.png")], check=True)

    secs = duration(out / f"{stem}.mp4")
    size = (out / f"{stem}.mp4").stat().st_size / 1e6
    if secs is not None:
        print(f"    {secs:.1f} s, {size:.1f} MB")


def main(manifest: list[tuple[str, str, str]], manim_dir: Path,
         out: Path, feature_stems: set[str] = frozenset()) -> None:
    """``manifest`` is (module, SceneClass, stem); ``feature_stems`` are
    chapter features, exempt from the inline length warning."""
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--force", action="store_true", help="ignore mtimes")
    ap.add_argument("--draft", action="store_true", help="480p preview only")
    args = ap.parse_args()

    stems = [m[2] for m in manifest]
    dupes = {s for s in stems if stems.count(s) > 1}
    if dupes:
        sys.exit(f"ERROR: duplicate stems in MANIFEST: {sorted(dupes)}")

    selected = [m for m in manifest if m[2].startswith(args.prefix)]
    if not selected:
        sys.exit(f"No clips match {args.prefix!r}")

    built = 0
    for module, scene, stem in selected:
        if objective(manim_dir, module, scene) is None:
            print(f"  WARNING: {scene} has no 'Objective:' line in its docstring.")
        if not (args.force or args.draft) and up_to_date(manim_dir, out, module, stem):
            print(f"  {stem}: up to date")
            continue
        render(manim_dir, out, module, scene, stem, args.draft)
        built += 1
        secs = duration(out / f"{stem}.mp4")
        if secs and secs > MAX_INLINE_SECONDS and stem not in feature_stems \
                and not args.draft:
            print(f"    WARNING: {stem} runs {secs:.0f} s. Inline clips are "
                  "one idea; split it or list it as a chapter feature.")
    print(f"\n{built} built -> {out}")
