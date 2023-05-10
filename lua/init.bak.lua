local env_path = "/www/xl_sec/lua/"
local lua_list = {
    "?.lua;",
    "dao/?.lua;",
    "util/?.lua;"
}
package.path = package.path .. ";"
for _, v in pairs(lua_list) do
    package.path = package.path .. env_path .. v
end