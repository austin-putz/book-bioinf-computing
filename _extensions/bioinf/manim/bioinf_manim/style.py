"""Palette, states, and reusable parts for every manim clip in the series.

The single source of truth for how a clip looks; the rules it implements are
in STYLE-GUIDE.md §2 (colour roles) and §7 (Animations). Adapted from the
linear-models book's ``manim/ambook/style.py``.

Chapter modules import from here and supply their own content:

    from bioinf_manim import *
"""

from manim import *  # noqa: F401,F403
import numpy as np

# ---------------------------------------------------------------- palette
# The same colours as the theme's dark mode (bioinf-dark.scss), so a clip
# and the page around it speak one colour language. Clips are rendered once,
# on a dark background, like a video player.

# --- theme: carries no meaning
BG = "#1b1f24"        # background
TITLE = "#f8f9fa"     # headings, punchlines, the active-state stroke
BODY = "#dee2e6"      # prose, operators, role-less shapes
SUBTEXT = "#adb5bd"   # captions, labels, discarded material
LINE = "#495057"      # outlines, rules, frames

# --- roles: one meaning each, the same in SVGs, clips, and maths
GIVEN = "#5BB4E5"     # our data, and every re-organisation of it:
                      #   blood -> RNA -> reads -> BAM -> counts; y, K
REF = "#F5B841"       # reference / structure we bring:
                      #   genome, annotation, adapters, beads; design matrix X
SOLVE = "#E3A3C7"     # what we solve for: beta-hat, fold changes, dispersions
GOOD = "#3FD3A8"      # a quality check
WARN = "#F08A4B"      # pitfalls ONLY

SANS = "Helvetica Neue"
MONO = "Menlo"

config.background_color = BG
config.frame_rate = 30

# States (STYLE-GUIDE §7, Animations). Attention is a light stroke and a small scale
# pulse, never a hue, so it composes with every role colour.
PENDING_OPACITY = 0.35
ACTIVE_STROKE = 3.0
ACTIVE_SCALE = 1.06

HOLD = 1.75           # the standard beat before any reveal


# ------------------------------------------------------------------- text
TEXT_OVERSAMPLE = 4


def txt(s, size=26, color=BODY, mono=False, bold=False):
    """All on-screen text goes through here, so fonts stay consistent.

    Pango lays text out at the requested size and rounds each glyph's
    position, which at small sizes jams letters together ("Ext ract",
    "countsrun"). Laying out at 4x and scaling down keeps the spacing true.
    """
    return Text(s, font=MONO if mono else SANS, font_size=size * TEXT_OVERSAMPLE,
                color=color, weight=BOLD if bold else NORMAL
                ).scale(1 / TEXT_OVERSAMPLE)


class Caption:
    """The narration line at the bottom of the frame. Clips have no audio,
    so this carries the story; keep each line under ~80 characters."""

    def __init__(self, scene):
        self.scene = scene
        self.mob = None

    def say(self, text, color=SUBTEXT, run_time=0.5, wait=None):
        # buff keeps the line above the bottom ~13% of the frame, where a
        # browser's player controls sit.
        new = txt(text, size=26, color=color).to_edge(DOWN, buff=1.05)
        anims = [FadeIn(new, shift=UP * 0.1)]
        if self.mob is not None:
            anims.append(FadeOut(self.mob))
        self.scene.play(*anims, run_time=run_time)
        self.mob = new
        if wait:
            self.scene.wait(wait)

    def clear(self, run_time=0.3):
        if self.mob is not None:
            self.scene.play(FadeOut(self.mob), run_time=run_time)
            self.mob = None


# ----------------------------------------------------------------- states
def pending(mob):
    """Not yet computed or not yet reached."""
    return mob.set_opacity(PENDING_OPACITY)


def activate(mob):
    """Light stroke plus a scale pulse: the active marker, no hue."""
    return mob.animate.scale(ACTIVE_SCALE).set_stroke(TITLE, ACTIVE_STROKE)


def settle(mob):
    return mob.animate.scale(1 / ACTIVE_SCALE).set_stroke(width=0)


# ------------------------------------------------------------ stage rail
class StageRail(VGroup):
    """The "you are here" bar across the top of every pipeline clip.

    ``stages`` are short labels; ``sections`` is a list of (label, first,
    last) index ranges, e.g. wet lab vs computer. Reached stages are solid,
    the current one carries the active stroke, later ones are pending.
    """

    def __init__(self, stages, sections=(), width=12.4, y=3.15, **kwargs):
        super().__init__(**kwargs)
        n = len(stages)
        xs = np.linspace(-width / 2, width / 2, n)
        self.dots, self.labels = VGroup(), VGroup()
        for x, s in zip(xs, stages):
            d = Circle(radius=0.11, color=BODY, fill_color=BODY,
                       fill_opacity=1, stroke_width=0).move_to([x, y, 0])
            self.dots.add(d)
            self.labels.add(txt(s, size=17, color=BODY).next_to(d, DOWN, buff=0.12))
        self.track = Line([xs[0], y, 0], [xs[-1], y, 0], color=LINE, stroke_width=2)
        self.sections = VGroup()
        for label, a, b in sections:
            lo, hi = xs[a] - 0.35, xs[b] + 0.35
            rule = Line([lo, y + 0.32, 0], [hi, y + 0.32, 0], color=LINE, stroke_width=1.5)
            tag = txt(label.upper(), size=14, color=SUBTEXT).next_to(rule, UP, buff=0.06)
            self.sections.add(VGroup(rule, tag))
        self.add(self.track, self.sections, self.dots, self.labels)
        self.current = None
        for d, l in zip(self.dots, self.labels):
            pending(d)
            pending(l)

    def goto(self, scene, i):
        anims = []
        if self.current is not None:
            prev = self.current
            anims += [self.dots[prev].animate.scale(1 / ACTIVE_SCALE)
                      .set_stroke(width=0).set_opacity(1)]
        anims += [
            self.dots[i].animate.set_opacity(1).scale(ACTIVE_SCALE)
            .set_stroke(TITLE, ACTIVE_STROKE),
            self.labels[i].animate.set_opacity(1).set_color(TITLE),
        ]
        if self.current is not None:
            anims.append(self.labels[self.current].animate.set_color(BODY))
        scene.play(*anims, run_time=0.5)
        self.current = i

    def finish(self, scene):
        """Every stage reached, none active: the end state of a pipeline."""
        anims = [d.animate.set_opacity(1).set_stroke(width=0) for d in self.dots]
        anims += [l.animate.set_opacity(1).set_color(BODY) for l in self.labels]
        if self.current is not None:
            anims.append(self.dots[self.current].animate.scale(1 / ACTIVE_SCALE))
        scene.play(*anims, run_time=0.5)
        self.current = None


# ------------------------------------------------------------- molecules
def strand(length, color=GIVEN, height=0.12, opacity=1.0):
    """A nucleic-acid strand or a read: always a horizontal bar, 5' on the
    left. Reads, fragments, and transcripts are all drawn this way."""
    return RoundedRectangle(width=length, height=height,
                            corner_radius=min(height / 2, 0.05),
                            stroke_width=0, fill_color=color,
                            fill_opacity=opacity)


def duplex(length, color=GIVEN, height=0.09, gap=0.05):
    """Double-stranded DNA (cDNA, a library fragment): two bars."""
    top = strand(length, color, height)
    bot = strand(length, color, height).next_to(top, DOWN, buff=gap)
    return VGroup(top, bot)


# ------------------------------------------------------------ file cards
class FileCard(VGroup):
    """A file is always this card: name on a tab, contents in monospace.
    ``notes`` (optional) are labels set to the right of each line."""

    def __init__(self, name, lines, notes=None, color=GIVEN, size=20,
                 note_color=SUBTEXT, **kwargs):
        super().__init__(**kwargs)
        # A fixed line pitch, so a short line ("+") does not pull its
        # neighbours closer and notes stay level with their lines.
        pitch = size / 48 + 0.1
        body = VGroup(*[txt(l, size=size, mono=True, color=BODY) for l in lines])
        for k, line in enumerate(body):
            line.move_to([0, -k * pitch, 0], aligned_edge=LEFT)
        box = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.5,
                               corner_radius=0.12, stroke_color=color,
                               stroke_width=2, fill_color=color, fill_opacity=0.08)
        box.move_to(body)
        tab_text = txt(name, size=17, mono=True, color=BG, bold=True)
        tab = RoundedRectangle(width=tab_text.width + 0.3, height=0.34,
                               corner_radius=0.08, stroke_width=0,
                               fill_color=color, fill_opacity=1)
        tab.next_to(box.get_corner(UL), UP, buff=0).shift(RIGHT * (tab.width / 2 + 0.1))
        tab_text.move_to(tab)
        self.body, self.box = body, box
        self.add(box, tab, tab_text, body)
        self.notes = VGroup()
        if notes:
            for line, note in zip(body, notes):
                n = txt(note, size=17, color=note_color)
                n.next_to(box, RIGHT, buff=0.3).match_y(line)
                self.notes.add(n)
            self.add(self.notes)


def tool_badge(name, color=BODY):
    """A tool is named in monospace, in a muted pill. Tools carry no role
    colour: what they read and write does."""
    t = txt(name, size=20, mono=True, color=color)
    pill = RoundedRectangle(width=t.width + 0.35, height=t.height + 0.22,
                            corner_radius=0.15, stroke_color=LINE,
                            stroke_width=1.5, fill_opacity=0)
    return VGroup(pill, t.move_to(pill))


def check_badge(text):
    """A QC result: green, with a tick. Checks report; they never change data."""
    t = txt("✓ " + text, size=20, color=GOOD)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.25,
                           corner_radius=0.12, stroke_color=GOOD,
                           stroke_width=1.5, fill_color=GOOD, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))


# --------------------------------------------------------- count matrix
class CountMatrix(VGroup):
    """Genes in rows, samples in columns: the series-wide orientation (the
    DESeq2 convention, K_ij for gene i in sample j).

    Cells start as pending "?" in GIVEN and are filled with ``fill``.
    ``groups`` is a list of (label, first_col, last_col) shown above the
    sample names.
    """

    def __init__(self, genes, samples, groups=(), cell_w=0.95, cell_h=0.6,
                 size=26, **kwargs):
        super().__init__(**kwargs)
        nr, nc = len(genes), len(samples)
        self.cell_w, self.cell_h = cell_w, cell_h
        self.cells = []
        body = VGroup()
        for r in range(nr):
            row = []
            for c in range(nc):
                t = txt("?", size=size, color=GIVEN, mono=True)
                t.move_to([(c - (nc - 1) / 2) * cell_w, -(r - (nr - 1) / 2) * cell_h, 0])
                pending(t)
                row.append(t)
                body.add(t)
            self.cells.append(row)
        self.body = body

        w = nc * cell_w / 2 + 0.12
        h = nr * cell_h / 2 + 0.05
        self.brackets = VGroup()
        for sign, x in ((1, -w), (-1, w)):
            b = VMobject(stroke_color=BODY, stroke_width=2.6)
            b.set_points_as_corners([[x + sign * 0.17, h, 0], [x, h, 0],
                                     [x, -h, 0], [x + sign * 0.17, -h, 0]])
            self.brackets.add(b)

        self.row_labels = VGroup(*[
            txt(g, size=21, color=BODY).move_to(
                [-w - 0.3, -(r - (nr - 1) / 2) * cell_h, 0], aligned_edge=RIGHT)
            for r, g in enumerate(genes)])
        for lab in self.row_labels:
            lab.align_to([-w - 0.3, 0, 0], RIGHT)
        self.col_labels = VGroup(*[
            txt(s, size=21, color=BODY).move_to(
                [(c - (nc - 1) / 2) * cell_w, h + 0.3, 0])
            for c, s in enumerate(samples)])
        self.group_labels = VGroup()
        for label, a, b in groups:
            x0 = (a - (nc - 1) / 2) * cell_w - cell_w * 0.4
            x1 = (b - (nc - 1) / 2) * cell_w + cell_w * 0.4
            rule = Line([x0, h + 0.62, 0], [x1, h + 0.62, 0], color=LINE, stroke_width=1.5)
            tag = txt(label, size=19, color=SUBTEXT).next_to(rule, UP, buff=0.08)
            self.group_labels.add(VGroup(rule, tag))
        self.add(self.brackets, self.body, self.row_labels, self.col_labels,
                 self.group_labels)

    def cell(self, r, c):
        return self.cells[r][c]

    def value_mob(self, r, c, value, size=26):
        return txt(str(value), size=size, color=GIVEN, mono=True).move_to(self.cells[r][c])

    def replace_cell(self, r, c, new):
        """Re-register a cell so later animations address the new value."""
        old = self.cells[r][c]
        self.body.remove(old)
        self.cells[r][c] = new
        self.body.add(new)
