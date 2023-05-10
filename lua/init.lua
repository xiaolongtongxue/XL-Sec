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
-- Reding Config
require('config'):load_config()
local delay = 3
local timer = ngx.timer.at
timer(delay, function()
    -- 在timer回调函数中调用MySQL接口API
    Setdata = require('init-data')
    Setdata()
end)
