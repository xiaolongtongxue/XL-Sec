Split = require('string-split')
require('length')
require('uuid')

Json = require('cjson.safe')
Config = ngx.shared.w_config
Switches = ngx.shared.w_switches
Rules = ngx.shared.w_rules
Ips = ngx.shared.w_ips
Resps = ngx.shared.w_resps
-----
C_Attack = ngx.shared.c_attack
-----
Method = ngx.req.get_method()
Uri = ngx.var.uri
MySql_Dao = require('dao.mysql'):new()
Redis_Dao = require('dao.redis'):new()
if MySql_Dao == nil or Redis_Dao == nil then return end


--[[运行SQL记录攻击or封禁行为]]
Sql_Rem = function(reason, locktime, isbans, level)
    local keyword, sql_log = "", ""
    local ruid, fid
    if isbans then isbans = '1' else isbans = '0' end
    if reason == "cc" then
        keyword = ndk.set_var.set_quote_sql_str("CC攻击域名为 :: " .. Server_host .. " ::，是大面积的流量攻击，本次HTTP数据包不做记录")
        ruid, fid = Split(Config:get('CC_FID'), ":")[2], Split(Config:get('CC_FID'), ":")[1]
    else
        HTTPREQ = HTTP_Get()
        keyword = ndk.set_var.set_quote_sql_str(HTTPREQ) -- HTTPREQ
        ruid, fid = RUID, Config:get(string.upper(reason .. '_FID'))
    end
    if Real_Host_wid ~= nil then
        sql_log =
            "INSERT INTO `w_attack_log` (`remote_ip`,`atid`,`isbans`,`level`,`wid`,`time_remain`,`fid`,`ruid`,`http`) VALUES ('" ..
            Client_IP .. "',(SELECT `atid` FROM `w_rules_info` WHERE `ruid` = '" .. ruid .. "')" ..
            "," .. isbans .. "," .. level .. ",'" .. Real_Host_wid ..
            "'," .. tostring(locktime) .. ",'" .. fid .. "','" .. ruid .. "'," .. keyword .. ");"
    else
        sql_log =
            "INSERT INTO `w_attack_log` (`remote_ip`,`atid`,`isbans`,`level`,`time_remain`,`fid`,`ruid`,`http`) VALUES ('" ..
            Client_IP .. "',(SELECT `atid` FROM `w_rules_info` WHERE `ruid` = '" .. ruid .. "')" ..
            "," .. isbans .. "," .. level .. ",'" .. tostring(locktime) ..
            "','" .. fid .. "','" .. ruid .. "'," .. keyword .. ");"
    end
    local ok, err = MySql_Dao:query(sql_log)
    local html = Resps:get('resps:lua:' .. reason)
    ngx.header.content_type = "text/html"
    -- ngx.say(sql_log)
    -- ngx.say('/n****************/n')
    ngx.say(tostring(html))
    Redis_Dao:select(Config:get('REDIS_NUM_TO_PANEL'))
    Redis_Dao:incr('attack:count')
    if isbans then
        -- 出现封禁情况立刻计数
        Redis_Dao:incr('attack:bans:count')
    end
    ngx.exit(403)
end
--[[由于获取HTTP完整请求包的话，会是对系统资源的一个较大考验，所以只有在需要进行封禁或拦截动作的时候才运行此函数]]
HTTP_Get = function()
    -- 获取当前请求的完整请求体，后边会用到
    HTTPREQ = Method .. " " .. Uri
    if length(Args) > 0 then
        HTTPREQ = HTTPREQ .. "?"
        for k, v in pairs(Args) do
            HTTPREQ = HTTPREQ .. k .. "=" .. tostring(v) .. "&"
        end
        HTTPREQ = string.sub(HTTPREQ, 1, -2)
    end
    HTTPREQ = HTTPREQ .. " HTTP/" .. ngx.req.http_version() .. "\n"
    for k, v in pairs(Headers) do
        HTTPREQ = HTTPREQ .. k .. ": " .. v .. "\n"
    end
    if ngx.req.get_body_data() ~= nil then
        HTTPREQ = HTTPREQ .. "\n" .. ngx.req.get_body_data()
    end
    return HTTPREQ
end
--[[在from-data情况下获取boundary]]
Get_Boundary = function()
    local header = ngx.var.content_type
    if not header then return nil end
    if ngx.re.find(header, [[multipart]], 'ijo') then
        if not ngx.re.match(header, '^multipart/form-data; boundary=') then
            ngx.say("Content-type ERROR")
            ngx.exit(400)
        end
        local multipart_data = ngx.re.match(string.gsub(header, "\r", ""), [[^multipart/form-data;.*boundary=(.*)$]],
            "jo")
        if type(multipart_data) == "table" and #multipart_data > 0 then
            return multipart_data[1]
        else
            ngx.say("Content-type Boundary ERROR")
            ngx.exit(400)
        end
        ngx.say(type(multipart_data))
        for k, v in ipairs(multipart_data) do
            ngx.say(k .. "\t\t" .. v)
        end
        ngx.say(not multipart_data)
        if not multipart_data then
            ngx.say("Content-type Boundart ERROR")
            ngx.exit(400)
        end
    else
        return nil
    end
end

-- 总开关状态，出现异常则默认开启
Waf_Status = Switches:get('switch:waf-status:total:total')
if Waf_Status == '0' or Waf_Status == 0 then return end

-- 类型开关状态，出现异常则默认开启
CC_switch, Inject_switch, Formdata_switch =
    tonumber(Switches:get('switch:waf-status:total:cc')) ~= 0,
    tonumber(Switches:get('switch:waf-status:total:inject')) ~= 0,
    tonumber(Switches:get('switch:waf-status:total:formdata')) ~= 0

-- 获取当前的请求的网站信息开关状态

Server_name = ngx.var.server_name
Server_host = (ngx.var.server_port == '80' or ngx.var.server_port == '443')
    and ngx.var.host or ngx.var.host .. ":" .. ngx.var.server_port
Real_Host_wid = Switches:get("webname:" .. Server_name)
if Real_Host_wid == nil then
    Real_Host_wid = Switches:get("webname:" .. Server_host)
end
if Real_Host_wid == nil then
    Total_Switch, CC_switch, Inject_switch, Formdata_switch, Iscdn = true, true, true, true, false
else
    Total_Switch, CC_switch, Inject_switch, Formdata_switch, Iscdn =
        tonumber(Switches:get('switch:waf-status:' .. Real_Host_wid .. ':cc')) ~= 0,
        tonumber(Switches:get('switch:waf-status:' .. Real_Host_wid .. ':cc')) ~= 0,
        tonumber(Switches:get('switch:waf-status:' .. Real_Host_wid .. ':inject')) ~= 0,
        tonumber(Switches:get('switch:waf-status:' .. Real_Host_wid .. ':formdata')) ~= 0,
        tonumber(Switches:get('switch:waf-status:' .. Real_Host_wid .. ':iscdn')) ~= 0
end
if not Total_Switch then return end


-- 获取客户端的真实IP地址以及完整的请求URL
Headers = ngx.req.get_headers()
if Iscdn then
    Client_IP = (Headers["X-REAL-IP"] or Headers["X_FORWARDED_FOR"]) or ngx.var.remote_addr
else
    Client_IP = ngx.var.remote_addr
end
Full_Url = ngx.var.scheme .. "://" .. Server_host
if ngx.var.args == nil then
    Full_Url = Full_Url .. ngx.var.uri
else
    Full_Url = Full_Url .. ngx.var.uri .. ngx.var.args
end

-- 自动封禁的结果校验
if C_Attack:get("auto-ip:banned:" .. Client_IP) ~= nil then
    local reason = C_Attack:get("banned:reason:" .. Client_IP)
    local html = Resps:get('resps:lua:' .. reason)
    ngx.header.content_type = "text/html"
    ngx.say(tostring(html))
    ngx.exit(403)
end


-- 判断黑白名单的状态(黑名单的情况都是用户通过面板手动添加的或者是通过面板进行封禁的)
Ips_black, Ips_white, Urls_white = Json.decode(Ips:get('rules:ip-black')), Json.decode(Ips:get('rules:ip-white')),
    Json.decode(Ips:get('rules:url-white'))
for _, v in ipairs(Ips_white) do if Client_IP == v then return end end
for _, v in ipairs(Ips_black) do
    if Client_IP == v then
        ngx.say(Resps:get('resps:lua:ip-black') or "Black,Stop metting!")
        ngx.exit(403)
    end
end
for _, v in ipairs(Urls_white) do if Full_Url == v then return end end

-- 对CC攻击的校验
CC = function()
    local cc_rules = Json.decode(Rules:get('rules:' .. Config:get('CC_FID')))
    local cycle, rate, lock_time, tolerate_times =
        tonumber(cc_rules['cycle']), tonumber(cc_rules['rate']),
        tonumber(cc_rules['lock-time']), tonumber(cc_rules['tolerate-times'])
    if C_Attack:get("cc-define:ip:" .. Client_IP) == nil then
        -- 第一次访问，开始计算频率，并设定有效期为循环周期
        C_Attack:set("cc-define:ip:" .. Client_IP, 1, cycle)
        C_Attack:set("cc-banned-times:" .. Client_IP, 0, 1800)
    else
        -- 不是第一次访问的话
        C_Attack:incr("cc-define:ip:" .. Client_IP, 1)
        local times = C_Attack:get("cc-define:ip:" .. Client_IP)
        if tonumber(times) >= rate then
            local t_lock_time = lock_time * (tonumber(C_Attack:get("cc-banned-times:" .. Client_IP)) + 1) -- 实际封禁时间
            C_Attack:set("banned:reason:" .. Client_IP, 'cc', t_lock_time)
            -- 超限了，需要封禁，这又分为了几种情况
            if tonumber(C_Attack:get("cc-banned-times:" .. Client_IP)) == 0 then
                -- 第一次犯事儿，就按照最轻的来
                C_Attack:incr("cc-banned-times:" .. Client_IP, 1)
                C_Attack:set("auto-ip:banned:" .. Client_IP, '1', t_lock_time)
                Sql_Rem('cc', t_lock_time, true, Config:get('CC_LEVEL'))
            else
                if tonumber(C_Attack:get("cc-banned-times:" .. Client_IP)) > 0 and tonumber(C_Attack:get("cc-banned-times:" .. Client_IP)) <= tolerate_times then
                    -- 限制时间内多次犯事儿，逐级增加
                    C_Attack:incr("cc-banned-times:" .. Client_IP, 1)
                    C_Attack:set("auto-ip:banned:" .. Client_IP, '1', t_lock_time)
                    Sql_Rem('cc', t_lock_time, true, Config:get('CC_LEVEL'))
                else
                    -- 超限了，永封
                    C_Attack:delete("cc-banned-times:" .. Client_IP)
                    C_Attack:set("auto-ip:banned:" .. Client_IP, '1', 0)
                    Sql_Rem('cc', 0, true, Config:get('CC_LEVEL')) -- 关于这一段，后续还有要和其他部分对一下，如果
                end
            end
        end
    end
end
if CC_switch then CC() end


-- 在开始对参数进行合法性校验钱获取一些必要的变量
Args = ngx.req.get_uri_args()

--[[这一段是为了将Injection这些注入类型的攻击进行重新的整理整合，统计攻击频率，进行IP封禁的行为]]
Injections_Bans = function(types)
    local isbans = false
    local t_lock_time = -1
    local cycle, rate, lock_time, big_circle, tolerate_times =
        tonumber(Config:get('ATTACK_CYCLE')),
        tonumber(Config:get('ATTACK_RATE')),
        tonumber(Config:get('ATTACK_BANNED_TIME')),
        tonumber(Config:get('ATTACK_BIG_CYCLE')),
        tonumber(Config:get('ATTACK_BANNED_TIMES_MAX'))
    if C_Attack:get(types .. "-define:ip:" .. Client_IP) == nil then
        -- 第一次犯事儿被逮住，没必要封禁，记一下就好了
        C_Attack:set(types .. "-define:ip:" .. Client_IP, 1, cycle)
        C_Attack:set(types .. "-banned-times:" .. Client_IP, 0, big_circle)
    else
        -- 不是第一次犯事儿的话，就先把这一次的先加上，然后再判断
        C_Attack:incr(types .. "-define:ip:" .. Client_IP, 1)
        local times = C_Attack:get(types .. "-define:ip:" .. Client_IP)
        if tonumber(times) > rate then
            -- 该封禁IP了
            isbans = true
            t_lock_time =
                lock_time * (tonumber(C_Attack:get(types .. "-banned-times:" .. Client_IP)) + 1) -- 实际封禁时间
            if tonumber(C_Attack:get(types .. "-banned-times:" .. Client_IP)) > tolerate_times then
                t_lock_time = 0
            end
            -- auto-ip:banned:
            C_Attack:set("auto-ip:banned:" .. Client_IP, '1', t_lock_time)
            C_Attack:set("banned:reason:" .. Client_IP, types, t_lock_time)
        end
    end
    Sql_Rem(types, t_lock_time, isbans, Config:get(string.upper(types .. "_LEVEL")))
end

-- 校验GET注入，检查其中的URI和请求参数
Get = function()
    local get_key = "rules:" .. Config:get("GET_FID")
    local rules_list = Json.decode(Rules:get(get_key))
    if rules_list == nil then return true end
    if length(Args) > 1000 then return false end
    local res = true
    for ruid, content in pairs(rules_list) do
        res = (ngx.re.match(Uri, content) == nil) and res
        if not res then
            RUID = ruid
            return res
        end
    end
    if length(Args) > 0 then
        for ruid, content in pairs(rules_list) do
            for k, v in pairs(Args) do
                local res1 = ngx.re.match(string.lower(k), content) == nil
                local res2 = ngx.re.match(string.lower(tostring(v)), content) == nil
                res = res and res1 and res2
                if not res then
                    RUID = ruid
                    return res
                end
            end
        end
    end
    return res
end

-- 校验POST注入，检查请求参数（非form-data格式，json或x-www-form-urlencoded格式）
Post = function()
    local get_key = "rules:" .. Config:get("POST_FID")
    local rules_list = Json.decode(Rules:get(get_key))
    if rules_list == nil then return true end
    local res = true
    local content_type = ngx.var.content_type
    if content_type == nil then return true end -- 这不是我们是所能处理的了
    if string.match(content_type, "application/from-data%") then return true end
    local post_args = ngx.req.get_body_data()
    if type(post_args) == "string" then
        for ruid, content in pairs(rules_list) do
            res = ngx.re.match(string.lower(post_args), content) == nil
            if not res then
                RUID = ruid
                return res
            end
        end
    elseif type(post_args) == "table" then
        for k, v in pairs(post_args) do
            for ruid, content in pairs(rules_list) do
                local res1 = ngx.re.match(string.lower(k), content) == nil
                local res2 = ngx.re.match(string.lower(v), content) == nil
                res = res1 or res2
                if not res then
                    RUID = ruid
                    return res
                end
            end
        end
    else
        return true
    end
    return true
end

-- UA检测
UA = function()
    local ua = ngx.var.http_user_agent
    if ua == nil then return true end
    local get_key = "rules:" .. Config:get("UA_FID")
    local rules_list = Json.decode(Rules:get(get_key))
    if rules_list == nil then return true end
    for ruid, content in pairs(rules_list) do
        local res = ngx.re.match(string.lower(ua), string.lower(content)) == nil
        if not res then
            RUID = ruid
            return res
        end
    end
    return true
end

-- Cookie检测
Cookie = function()
    local cookie = ngx.var.http_cookie
    if cookie == nil then return true end
    local get_key = "rules:" .. Config:get("COOKIE_FID")
    local rules_list = Json.decode(Rules:get(get_key))
    if rules_list == nil then return true end
    for ruid, content in pairs(rules_list) do
        local res = ngx.re.match(string.lower(cookie), string.lower(content)) == nil
        if not res then
            RUID = ruid
            return res
        end
    end
    return true
end


-- 注入类型的一系列攻击内容及其相关的函数和操作
if Inject_switch then
    local res = Get()
    if not res then
        Injections_Bans('get')
    end
    if Method == 'POST' then
        res = Post()
        if not res then
            Injections_Bans('post')
        end
    end
    res = UA()
    if not res then
        Injections_Bans('ua')
    end
    res = Cookie()
    if not res then
        Injections_Bans('cookie')
    end
end

FormData = function()
    local boundary = Get_Boundary()
    if boundary == nil then
        boundary = ""
    else
    end
    local request_body = ngx.req.get_body_data()
    if type(request_body) ~= "string" then
        ngx.say("Request Body fail")
        ngx.exit(400)
        return false
    end
    local pattern = "=[^%-%-]+" ..
        boundary ..
        '[\r\n]Content%-Disposition: ; name="([^"]+)"%s*(; filename="([^"]+)")?[\r\n]Content%-Type: ([^\r\n]+)[^\r\n]*[\r\n][\r\n](.*)'
    local matches = ngx.re.match(request_body, pattern, "jo")
    if matches ~= nil then
        for match in matches do
            local header = match[0]
            local filename = match[1]
            -- 检查header和filename是否符合规范，可以根据实际情况进行扩展
            if not header or not filename then
                ngx.log(ngx.ERR, "invalid form-data format")
                return false
            end
        end
    end
    -- if type(ngx.req.get_body_data()) == "string" then return true end
    -- local data = string.gsub(ngx.req.get_body_data(), '\r', '')
    -- local boundary = ngx.re.match(ngx.var.content_type, [[^multipart/form-data;.*boundary=(.*)$]], "jo")
    -- if boundary ~= nil and type(boundary) == "table" then
    --     boundary = "\n--" .. boundary[1]
    -- end
    -- if boundary ~= nil and type(boundary) == "string" then

    -- else
    -- end
    -- -- ngx.say(data_)
    -- -- for k, v in ipairs(data_) do
    -- --     ngx.say(k .. "\t::\t" .. v)
    -- -- end
    return true
end

Formdata_switch = true
if Formdata_switch and Method == 'POST' then
    local res = FormData()
    if not res then
        Injections_Bans('formdata')
    end
end

Redis_Dao:release()
MySql_Dao:release()
