C_Attack = ngx.shared.c_attack
IP = ngx.req.get_uri_args()['ip']
if IP ~= nil then
    local reason = C_Attack:get("banned:reason:" .. IP)
    if type(reason) == "string" then
        C_Attack:set("auto-ip:banned:" .. IP, '0', 1)
        C_Attack:set("banned:reason:" .. IP, '0', 1)
        C_Attack:set(reason .. "-define:ip:" .. IP, '0', 1)
        C_Attack:set(reason .. "-banned-times:" .. IP, '0', 1)
    end
end
