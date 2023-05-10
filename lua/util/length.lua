function length(t)
    local res = 0
    for k, v in pairs(t) do
        res = res + 1
    end
    return res
end
