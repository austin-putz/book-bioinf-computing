-- svg.lua -----------------------------------------------------------------
-- {{< svg figures/name.svg >}} pastes an SVG file into the page as inline
-- markup. Inline (not <img>) so the drawing sees the page's CSS: diagram
-- colour classes follow the light/dark toggle and CSS animations respect
-- prefers-reduced-motion. Rules for the SVG file: STYLE-GUIDE.md §7.
--
-- The path is relative to the .qmd file. The root <svg> gets the class
-- "diagram" (which the colour classes are scoped to) and loses any fixed
-- width/height, so it scales to the column from its viewBox.

local function read_file(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local s = f:read("a")
  f:close()
  return s
end

local function strip_attr(tag, name)
  tag = tag:gsub("%s" .. name .. '="[^"]*"', "")
  tag = tag:gsub("%s" .. name .. "='[^']*'", "")
  return tag
end

local function prepare(svg)
  -- Drop anything before the root element (XML prolog, doctype, comments).
  local start = svg:find("<svg[%s>]")
  if not start then return nil end
  svg = svg:sub(start)

  local tag_end = svg:find(">", 1, true)
  local tag = svg:sub(1, tag_end)
  local rest = svg:sub(tag_end + 1)

  tag = strip_attr(tag, "width")
  tag = strip_attr(tag, "height")
  if tag:find('%sclass="') then
    tag = tag:gsub('%sclass="', ' class="diagram ', 1)
  else
    tag = tag:gsub("^<svg", '<svg class="diagram"', 1)
  end

  -- Pandoc ends a raw HTML block at a blank line; keep the SVG in one piece.
  rest = rest:gsub("\n%s*\n", "\n")
  return tag .. rest
end

return {
  ["svg"] = function(args)
    local rel = pandoc.utils.stringify(args[1] or "")
    if rel == "" then
      quarto.log.error("svg shortcode: give a file, e.g. {{< svg figures/x.svg >}}")
      return pandoc.Null()
    end

    local dir = pandoc.path.directory(quarto.doc.input_file)
    local path = pandoc.path.join({ dir, rel })
    local raw = read_file(path)
    if not raw then
      quarto.log.error("svg shortcode: cannot read " .. path)
      return pandoc.Null()
    end

    local svg = prepare(raw)
    if not svg then
      quarto.log.error("svg shortcode: no <svg> element in " .. path)
      return pandoc.Null()
    end

    -- A stepped diagram needs the controls script; load it only then.
    if svg:find("data%-step%-labels=") then
      quarto.doc.add_html_dependency({
        name = "bioinf-steps",
        version = "0.1.0",
        scripts = { "steps.js" },
      })
    end
    return pandoc.RawBlock("html", svg)
  end
}
