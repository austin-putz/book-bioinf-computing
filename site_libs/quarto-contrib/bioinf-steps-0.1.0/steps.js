// steps.js ----------------------------------------------------------------
// Stepped diagrams: an inline SVG (svg shortcode) whose root has
// data-step-labels="DNA|Fragment|..." gets Back/Next controls below it.
// Rules: STYLE-GUIDE.md §7, Stepped diagrams.
//
// Elements in the SVG opt in with attributes, steps counted from 1:
//   data-show="k"   hidden before step k
//   data-hide="k"   hidden from step k on
//   data-move="k"   sits offset by --dx/--dy (and --rot) before step k, then
//                   slides to its drawn position
// plus an optional style="--delay: 0.3s" to stagger a group.
// <desc data-caption="k"> holds the sentence shown under step k.
//
// Without this script the SVG shows its drawn positions with data-hide
// elements removed: the finished picture, which is the last step.

(function () {
  "use strict";

  function setup(svg) {
    const labels = svg.dataset.stepLabels.split("|").map((s) => s.trim());
    const n = labels.length;
    const captions = {};
    svg.querySelectorAll("desc[data-caption]").forEach((d) => {
      captions[d.dataset.caption] = d.textContent.trim();
    });
    const items = svg.querySelectorAll("[data-show],[data-hide],[data-move]");

    const bar = document.createElement("div");
    bar.className = "steps-bar";
    const prev = button("steps-prev", "← Back");
    const next = button("steps-next", "Next →");
    const list = document.createElement("ol");
    list.className = "steps-list";
    const pills = labels.map((label, i) => {
      const li = document.createElement("li");
      const b = button("steps-pill", (i + 1) + " " + label);
      b.addEventListener("click", () => go(i + 1));
      li.appendChild(b);
      list.appendChild(li);
      return b;
    });
    bar.append(prev, list, next);

    const caption = document.createElement("p");
    caption.className = "steps-caption";
    caption.setAttribute("aria-live", "polite");

    svg.after(bar, caption);

    let at = 1;
    function go(k) {
      at = Math.max(1, Math.min(n, k));
      items.forEach((el) => {
        const show = Number(el.dataset.show || 1);
        const hide = Number(el.dataset.hide || Infinity);
        const move = Number(el.dataset.move || 0);
        el.classList.toggle("is-hidden", at < show || at >= hide);
        el.classList.toggle("is-away", at < move);
      });
      pills.forEach((b, i) => {
        b.classList.toggle("is-current", i + 1 === at);
        b.classList.toggle("is-done", i + 1 < at);
        if (i + 1 === at) b.setAttribute("aria-current", "step");
        else b.removeAttribute("aria-current");
      });
      prev.disabled = at === 1;
      next.disabled = at === n;
      caption.textContent = captions[at] || "";
    }

    prev.addEventListener("click", () => go(at - 1));
    next.addEventListener("click", () => go(at + 1));
    bar.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") { go(at - 1); e.preventDefault(); }
      if (e.key === "ArrowRight") { go(at + 1); e.preventDefault(); }
    });

    // Jump to step 1 without animating away from the finished picture.
    svg.classList.add("steps-on", "steps-still");
    go(1);
    requestAnimationFrame(() =>
      requestAnimationFrame(() => svg.classList.remove("steps-still")));
  }

  function button(cls, text) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = cls;
    b.textContent = text;
    return b;
  }

  function init() {
    document.querySelectorAll("svg.diagram[data-step-labels]").forEach(setup);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
