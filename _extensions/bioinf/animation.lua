-- animation.lua -----------------------------------------------------------
-- {{< animation STEM >}} embeds assets/video/STEM.mp4 with STEM.png as its
-- poster. Use it inside a figure div, like the svg shortcode, so the clip
-- gets a number and a caption:
--
--   ::: {#fig-rnaseq-overview}
--   {{< animation rnaseq-overview >}}
--
--   Caption.
--   :::
--
-- Clips are made by the book's manim/build.py (STYLE-GUIDE.md §7, Animations). HTML
-- only. preload="none" so a chapter with several clips does not download
-- them all before the reader scrolls.
--
-- The book's _quarto.yml needs `resources: [assets/video/*.png]`: Quarto
-- finds the mp4 through <source src> but not the poster= attribute.

-- Raw HTML paths are not rewritten by Quarto, so a chapter in a subfolder
-- must reach the project root itself.
local function root_prefix()
  local ok, offset = pcall(function() return quarto.project.offset end)
  if ok and offset ~= nil and offset ~= "" then
    return offset .. "/"
  end
  return ""
end

return {
  ["animation"] = function(args)
    local stem = pandoc.utils.stringify(args[1] or "")
    if not stem:match("^[%w%-_]+$") then
      quarto.log.error("animation shortcode: give an asset stem, e.g. {{< animation rnaseq-overview >}}")
      return pandoc.Null()
    end
    local base = root_prefix() .. "assets/video/" .. stem
    return pandoc.RawBlock("html", table.concat({
      '<video class="animation" controls muted playsinline preload="none"',
      ' poster="', base, '.png">',
      '<source src="', base, '.mp4" type="video/mp4">',
      '<a href="', base, '.mp4">Download the video.</a>',
      '</video>',
    }))
  end
}
