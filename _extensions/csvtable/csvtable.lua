-- {{< csvtable data/toy.csv class="toy" >}}
-- Turns a small CSV file into an HTML table. "NA" cells get class="na".
-- No quoting rules: keep the file simple (no commas inside values).

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

local function split(line)
  local out = {}
  for v in (line .. ","):gmatch("([^,]*),") do
    out[#out + 1] = v:match("^%s*(.-)%s*$")
  end
  return out
end

return {
  ["csvtable"] = function(args, kwargs)
    local path = pandoc.utils.stringify(args[1])
    local class = pandoc.utils.stringify(kwargs["class"] or "")
    local f = io.open(path, "r")
    if not f and quarto.project.directory then
      f = io.open(quarto.project.directory .. "/" .. path, "r")
    end
    if not f then
      error("csvtable: cannot open " .. path)
    end
    local rows = {}
    for line in f:lines() do
      if line:match("%S") then rows[#rows + 1] = split(line) end
    end
    f:close()

    local html = { '<table class="' .. esc(class) .. '"><thead><tr>' }
    for _, h in ipairs(rows[1]) do html[#html + 1] = "<th>" .. esc(h) .. "</th>" end
    html[#html + 1] = "</tr></thead><tbody>"
    for i = 2, #rows do
      html[#html + 1] = "<tr>"
      for _, v in ipairs(rows[i]) do
        if v == "NA" then
          html[#html + 1] = '<td class="na">NA</td>'
        else
          html[#html + 1] = "<td>" .. esc(v) .. "</td>"
        end
      end
      html[#html + 1] = "</tr>"
    end
    html[#html + 1] = "</tbody></table>"
    return pandoc.RawBlock("html", table.concat(html))
  end
}
