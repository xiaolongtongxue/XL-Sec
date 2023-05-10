return function()
    local err_log = "Error executing SQL query: "
    local semaphore = require "ngx.semaphore"
    Split = require('string-split')
    require('util.nil_exit')
    local json = require('cjson.safe')
    local config = ngx.shared.w_config
    local switches = ngx.shared.w_switches
    local rules = ngx.shared.w_rules
    local ips = ngx.shared.w_ips
    local resps = ngx.shared.w_resps
    local mysql_dao = require('dao.mysql'):new()
    local redis_dao = require('dao.redis'):new()
    Nil_to_exit(mysql_dao, err_log)
    Nil_to_exit(redis_dao, err_log)
    local lock = semaphore.new(1)
    lock:wait(1)



    -- 清空预留数据
    redis_dao:select(config:get('REDIS_NUM_TO_PANEL'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_TOTAL_SWITCH'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_TOTAL_SWITCH'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_WEB_SWITCHS_INFO'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_RULES_INFO'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_BLACK_RULES'))
    redis_dao:flushdb()
    redis_dao:select(config:get('REDIS_NUM_RESPS'))
    redis_dao:flushdb()


    -- 为面板服务的数据
    local sql_get_total_attack_logs = "SELECT COUNT(`aeid`) as count FROM `w_attack_log`;"
    local sql_get_total_bans_logs = "SELECT COUNT(`ieid`) as count FROM `w_auto_ip_bans`;"
    local res_total, err = mysql_dao:query(sql_get_total_attack_logs)
    Nil_to_exit(res_total, err_log)
    local res_total1, err = mysql_dao:query(sql_get_total_bans_logs)
    Nil_to_exit(res_total1, err_log)
    redis_dao:select(config:get('REDIS_NUM_TO_PANEL'))
    redis_dao:set("attack:count", res_total[1]['count'])
    redis_dao:set("attack:bans:count", res_total1[1]['count'])

    -- 【【【开关数据相关】】】
    -- 总开关数据
    local sql_total = "SELECT `switch` FROM `w_switch`"
    res_total, err = mysql_dao:query(sql_total)
    Nil_to_exit(res_total, err_log)
    TOTAL_SWITCH = res_total[1]['switch']
    redis_dao:select(config:get('REDIS_NUM_TOTAL_SWITCH'))
    redis_dao:set("switch:waf-status:total:total", TOTAL_SWITCH)
    switches:set("switch:waf-status:total:total", TOTAL_SWITCH)

    -- 分类型的开关数据
    local sql_t_switches = "SELECT `t_switchs` FROM `w_switch`"
    res_total = mysql_dao:query(sql_t_switches)
    Nil_to_exit(res_total, err_log)
    T_CC_SWITCH = Split(res_total[1]['t_switchs'], ' ')[1]
    T_INJECT_SWITCH = Split(res_total[1]['t_switchs'], ' ')[2]
    T_FORMDATA_SWITCH = Split(res_total[1]['t_switchs'], ' ')[3]
    redis_dao:select(config:get('REDIS_NUM_TOTAL_SWITCH'))
    redis_dao:set("switch:waf-status:total:cc", T_CC_SWITCH)
    redis_dao:set("switch:waf-status:total:inject", T_INJECT_SWITCH)
    redis_dao:set("switch:waf-status:total:formdata", T_FORMDATA_SWITCH)
    switches:set("switch:waf-status:total:cc", T_CC_SWITCH)
    switches:set("switch:waf-status:total:inject", T_INJECT_SWITCH)
    switches:set("switch:waf-status:total:formdata", T_FORMDATA_SWITCH)

    -- 分网站开关数据(开关数据选用1号数据库)
    local sql_webs = "SELECT `wid`,`iscdn`,`total_switch`,`switchs`,`host` FROM `w_web_info`"
    local res_webs = mysql_dao:query(sql_webs)
    Nil_to_exit(res_webs, err_log)
    for _, v in pairs(res_webs) do
        redis_dao:select(config:get('REDIS_NUM_WEB_SWITCHS_INFO'))
        redis_dao:set("switch:waf-status:" .. v['wid'] .. ":total", v['total_switch'])
        redis_dao:set("switch:waf-status:" .. v['wid'] .. ":iscdn", v['iscdn'])
        redis_dao:set("switch:waf-status:" .. v['wid'] .. ":cc", Split(v['switchs'], ' ')[1])
        redis_dao:set("switch:waf-status:" .. v['wid'] .. ":inject", Split(v['switchs'], ' ')[2])
        redis_dao:set("switch:waf-status:" .. v['wid'] .. ":formdata", Split(v['switchs'], ' ')[3])

        switches:set("switch:waf-status:" .. v['wid'] .. ":total", v['total_switch'])
        switches:set("switch:waf-status:" .. v['wid'] .. ":iscdn", v['iscdn'])
        switches:set("switch:waf-status:" .. v['wid'] .. ":cc", Split(v['switchs'], ' ')[1])
        switches:set("switch:waf-status:" .. v['wid'] .. ":inject", Split(v['switchs'], ' ')[2])
        switches:set("switch:waf-status:" .. v['wid'] .. ":formdata", Split(v['switchs'], ' ')[3])
        for _, vv in pairs(Split(v['host'], ' ')) do
            redis_dao:set("webname:" .. vv, v['wid'])
            switches:set("webname:" .. vv, v['wid'])
        end
    end

    -- Web规则的正则数据(这条SQL是为了避免黑白名单的冲突)（正则等配置使用2号数据库）
    local sql_rules =
    "SELECT `ruid`,`fid`,`content` FROM `w_rules_info` WHERE `isalive` = 1 AND `ptid` NOT IN (SELECT `ptid` FROM `w_rules_table` WHERE `nickname`='ip-white' OR `nickname`='ip-black' OR `nickname`='url-white') ORDER BY `fid`;"
    local re_data = mysql_dao:query(sql_rules)
    Nil_to_exit(re_data, err_log)
    redis_dao:select(config:get('REDIS_NUM_RULES_INFO'))
    local fid_tmp, table_tmp = "", {}
    for _, v in pairs(re_data) do
        -- ngx.say(v['content'])
        if v['fid'] .. ":" .. v['ruid'] == config:get('CC_FID') then
            rules:set("rules:" .. v['fid'] .. ":" .. v['ruid'], v['content'])
        else
            if v['fid'] ~= fid_tmp then
                if fid_tmp ~= "" then
                    rules:set("rules:" .. fid_tmp, json.encode(table_tmp))
                end
                fid_tmp = v['fid']
                table_tmp = {}
                table_tmp[v['ruid']] = v['content']
            else
                table_tmp[v['ruid']] = v['content']
            end
        end
        redis_dao:set("rules:" .. v['fid'] .. ":" .. v['ruid'], v['content'])
        -- rules:set("rules:" .. v['fid'] .. ":" .. v['ruid'], v['content'])
    end
    rules:set("rules:" .. fid_tmp, json.encode(table_tmp))

    -- 黑白名单的获取（黑白名单使用3号数据库）
    local sql_blackip =
    "SELECT `content` FROM `w_rules_info` WHERE `isalive` = 1 AND `ptid` = (SELECT `ptid` FROM `w_rules_table` WHERE `nickname`='ip-black');"
    local sql_whiteip =
    "SELECT `content` FROM `w_rules_info` WHERE `isalive` = 1 AND `ptid` = (SELECT `ptid` FROM `w_rules_table` WHERE `nickname`='ip-white');"
    local sql_whiteurl =
    "SELECT `content` FROM `w_rules_info` WHERE `isalive` = 1 AND `ptid` = (SELECT `ptid` FROM `w_rules_table` WHERE `nickname`='url-white');"
    local black_ips = mysql_dao:query(sql_blackip)
    local white_ips = mysql_dao:query(sql_whiteip)
    local white_url = mysql_dao:query(sql_whiteurl)
    Nil_to_exit(black_ips, err_log)
    Nil_to_exit(white_ips, err_log)
    Nil_to_exit(white_url, err_log)
    redis_dao:select(config:get('REDIS_NUM_BLACK_RULES'))
    redis_dao:del("rules:ip-black")
    redis_dao:del("rules:ip-white")
    redis_dao:del("rules:url-white")
    local ips_black, ips_white, urls_white = {}, {}, {}
    for _, v in pairs(black_ips) do
        if string.find(v['content'], " ") == nil then
            redis_dao:sadd("rules:ip-black", v['content'])
            table.insert(ips_black, v['content'])
        else
            for _, v__ in pairs(Split(v['content'], " ")) do
                redis_dao:sadd("rules:ip-black", v__)
                table.insert(ips_black, v['content'])
            end
        end
    end
    for _, v in pairs(white_ips) do
        if string.find(v['content'], " ") == nil then
            redis_dao:sadd("rules:ip-white", v['content'])
            table.insert(ips_white, v['content'])
        else
            for _, v__ in pairs(Split(v['content'], " ")) do
                redis_dao:sadd("rules:ip-white", v__)
                table.insert(ips_white, v['content'])
            end
        end
    end
    for _, v in pairs(white_url) do
        redis_dao:sadd("rules:url-white", v['content'])
        table.insert(urls_white, v['content'])
    end
    ips:set("rules:ip-black", json.encode(ips_black))
    ips:set("rules:ip-white", json.encode(ips_white))
    ips:set("rules:url-white", json.encode(urls_white))


    -- 拦截后响应内容的获取（响应内容使用4号数据库）
    local sql_resps =
    "SELECT `nickname`,`return_html` FROM `w_resps_info` INNER JOIN `w_rules_table` ON `w_rules_table`.`ptid`=`w_resps_info`.`ptid`;"
    local data_resps = mysql_dao:query(sql_resps)
    Nil_to_exit(data_resps, err_log)
    redis_dao:select(config:get('REDIS_NUM_RESPS'))
    for _, v in pairs(data_resps) do
        redis_dao:set("resps:lua:" .. v['nickname'], v['return_html'])
        resps:set("resps:lua:" .. v['nickname'], v['return_html'])
    end

    lock:post(1)
    redis_dao:release()
    mysql_dao:release()
end
