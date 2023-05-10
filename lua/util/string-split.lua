return function(str, sep)
    local result = {}
    if str == nil or sep == nil or type(str) ~= "string" or type(sep) ~= "string" then return result end
    if string.len(sep) == 0 then return result end
    local pattern = string.format("([^%s]+)", sep)
    string.gsub(
        str,
        pattern,
        function(c)
            result[#result + 1] = c
        end
    )
    return result
end
