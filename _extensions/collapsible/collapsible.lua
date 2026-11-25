-- Collapsible blocks: write
--
--   ::: {.acc}
--   ### **Listwise deletion**: drop the whole row
--   - details shown when opened
--   :::
--
-- The first heading (or, if there is none, the first paragraph) becomes the
-- clickable title; everything after it is hidden until the block is opened.
-- Add .open to start it opened: ::: {.acc .open}
-- Output is an HTML <details>/<summary> element, styled in custom.scss.

local function inlines_to_html(inlines)
  local html = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "html")
  return (html:gsub("\n$", ""))
end

function Div(el)
  if not el.classes:includes("acc") then return nil end
  if not quarto.doc.is_format("html") then return nil end

  local blocks = el.content
  local title, rest = nil, {}
  for i, b in ipairs(blocks) do
    if title == nil and (b.t == "Header" or b.t == "Para" or b.t == "Plain") then
      title = b.content
    else
      table.insert(rest, b)
    end
  end
  title = title or { pandoc.Str("Details") }

  local open = el.classes:includes("open") and " open" or ""
  local out = {
    pandoc.RawBlock("html", '<details class="acc"' .. open .. '>\n<summary>' ..
      inlines_to_html(title) .. '</summary>')
  }
  for _, b in ipairs(rest) do table.insert(out, b) end
  table.insert(out, pandoc.RawBlock("html", "</details>"))
  return out
end
