-- identity.lua ------------------------------------------------------------
-- The only per-book styling in the series. Reads three values from the
-- book's _quarto.yml and turns them into
--   1. a favicon: a rounded badge in the accent color with a short label, and
--   2. CSS variables that colour the strip across the top of every page
--      (the strip itself is drawn in bioinf-rules.scss).
--
--   bioinf:
--     accent: "#2E6E7E"       # light mode; white label text must be readable on it
--     accent-dark: "#6FB3C2"  # dark mode strip
--     label: "CP"             # 1-3 letters or digits
--
-- The favicon is an inline SVG data URI, so books need no image files.

local DEFAULT_ACCENT = "#5A6B7B"

local function str(v)
  if v == nil then return nil end
  return pandoc.utils.stringify(v)
end

-- Only accept #RRGGBB, so nothing else can reach the page header.
local function hex(v, fallback)
  local s = str(v)
  if s and s:match("^#%x%x%x%x%x%x$") then return s end
  if s then
    quarto.log.warning("bioinf: ignoring invalid colour '" .. s .. "'; use #RRGGBB")
  end
  return fallback
end

local function clean_label(v)
  local s = str(v) or ""
  local cleaned = s:gsub("[^%w]", ""):sub(1, 3)
  if cleaned ~= s then
    quarto.log.warning("bioinf: label must be 1-3 letters or digits; using '" .. cleaned .. "'")
  end
  return cleaned
end

local function favicon_svg(accent, label)
  local size = ({ 40, 30, 23 })[#label] or 30
  return string.format(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' ..
    '<rect width="64" height="64" rx="14" fill="%s"/>' ..
    '<text x="32" y="32" dy="0.35em" text-anchor="middle" ' ..
    'font-family="Helvetica,Arial,sans-serif" font-weight="700" ' ..
    'font-size="%d" fill="#ffffff">%s</text></svg>',
    accent, size, label)
end

local function url_encode(s)
  return (s:gsub("[^%w%-%._~]", function(c)
    return string.format("%%%02X", string.byte(c))
  end))
end

function Meta(meta)
  if not quarto.doc.is_format("html") then return nil end

  local cfg = meta["bioinf"] or {}
  local accent = hex(cfg["accent"], DEFAULT_ACCENT)
  local accent_dark = hex(cfg["accent-dark"], accent)
  local label = clean_label(cfg["label"])

  local head = string.format(
    '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%s">\n' ..
    '<style>:root { --bioinf-accent: %s; --bioinf-accent-dark: %s; }</style>\n',
    url_encode(favicon_svg(accent, label)), accent, accent_dark)

  quarto.doc.include_text("in-header", head)
  return nil
end
