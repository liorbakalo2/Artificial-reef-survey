-- Pandoc Lua filter for the LaTeX build: sensible column widths, smaller type for wide tables,
-- landscape pages (with their caption paragraph) for tables with 9 or more columns.
local stringify = pandoc.utils.stringify

local function words_max(s)
  local m = 0
  for w in s:gmatch('%S+') do if #w > m then m = #w end end
  return m
end

local function analyse(tbl)
  local n = #tbl.colspecs
  local maxlen, sumlen, cnt, maxword = {}, {}, {}, {}
  for i = 1, n do maxlen[i] = 0; sumlen[i] = 0; cnt[i] = 0; maxword[i] = 0 end
  local function row(r)
    for i, c in ipairs(r.cells) do
      if i <= n then
        local s = stringify(c.contents)
        local l = #s
        if l > 0 then
          sumlen[i] = sumlen[i] + l; cnt[i] = cnt[i] + 1
          if l > maxlen[i] then maxlen[i] = l end
          local mw = words_max(s)
          if mw > maxword[i] then maxword[i] = mw end
        end
      end
    end
  end
  for _, r in ipairs(tbl.head.rows) do row(r) end
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do row(r) end end
  local w, tot = {}, 0
  for i = 1, n do
    local mean = cnt[i] > 0 and sumlen[i] / cnt[i] or 1
    local x = math.min(0.5 * maxlen[i] + 0.5 * mean, 48)
    x = math.max(x, maxword[i] + 2, 4)
    w[i] = x; tot = tot + x
  end
  for i = 1, n do
    local al = tbl.colspecs[i][1]
    tbl.colspecs[i] = {al, w[i] / tot}
  end
  return n
end

local function starts_with_table(b)
  if b.t ~= 'Para' and b.t ~= 'Plain' then return false end
  local f = b.content[1]
  return f and f.t == 'Strong' and stringify(f):match('^Table') ~= nil
end

function Blocks(blocks)
  local out = {}
  for _, b in ipairs(blocks) do
    if b.t == 'Table' then
      local n = analyse(b)
      local size = n >= 10 and '\\scriptsize' or (n >= 7 and '\\footnotesize' or nil)
      local land = n >= 9
      local cap
      if land and #out > 0 and starts_with_table(out[#out]) then cap = table.remove(out) end
      if land then out[#out + 1] = pandoc.RawBlock('latex', '\\begin{landscape}') end
      if cap then out[#out + 1] = cap end
      out[#out + 1] = pandoc.RawBlock('latex', '\\begingroup' .. (size and ('\\renewcommand{\\tablefont}{' .. size .. '}') or ''))
      out[#out + 1] = b
      out[#out + 1] = pandoc.RawBlock('latex', '\\endgroup')
      if land then out[#out + 1] = pandoc.RawBlock('latex', '\\end{landscape}') end
    else
      out[#out + 1] = b
    end
  end
  return out
end
