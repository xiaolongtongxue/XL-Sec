_C = {}

function _C.load_config()
    local config_dict = ngx.shared.w_config;
    config_dict:set("MYSQL_HOST", "127.0.0.1")  -- MySQL主机地址
    config_dict:set("MYSQL_PORT", 3306)         -- MySQL端口（默认3306）
    config_dict:set("MYSQL_DATABASE", "xlsec")  -- MySQL数据库数据库名
    config_dict:set("MYSQL_USER", "root")       -- MySQL用户
    config_dict:set("MYSQL_PASSWORD", '123456') -- MySQL密码
    config_dict:set("MYSQL_MAX_IDLE_TIME", 30000)
    config_dict:set("MYSQL_POOL_SIZE", 50)

    config_dict:set("REDIS_HOST", "127.0.0.1")  -- Redis主机地址
    config_dict:set("REDIS_PORT", "6379")       -- Redis端口
    config_dict:set("REDIS_USER", "")           -- Redis用户（一般情况下留空）
    config_dict:set("REDIS_PASSWORD", "123456") -- Redis密码
    config_dict:set("REDIS_MAX_IDLE_TIME", 10000)
    config_dict:set("REDIS_POOL_SIZE", 200000)

    config_dict:set("REDIS_NUM_TOTAL_SWITCH", "0")
    config_dict:set("REDIS_NUM_WEB_SWITCHS_INFO", "1")
    config_dict:set("REDIS_NUM_RULES_INFO", "2")
    config_dict:set("REDIS_NUM_BLACK_RULES", "3")
    config_dict:set("REDIS_NUM_RESPS", "4")
    config_dict:set("REDIS_NUM_AUTO_INFO", "5")
    config_dict:set("REDIS_NUM_TO_PANEL", "6")

    config_dict:set("CC_FID", "09f7d9f9-bbfd-11ed-8b2c-0242ac110002:c1f3b026-b904-11ed-8b2c-0242ac110002")
    config_dict:set("GET_FID", "72def3d1-b992-11ed-8b2c-0242ac110002")
    config_dict:set("POST_FID", "09f7ddb2-bbfd-11ed-8b2c-0242ac110002")
    config_dict:set("UA_FID", "09f7dfbe-bbfd-11ed-8b2c-0242ac110002")
    config_dict:set("COOKIE_FID", "09f7e146-bbfd-11ed-8b2c-0242ac110002")
    config_dict:set("FORMDATA_FID", "0a20b32b-d54e-11ed-a9ed-0242ac110003")

    config_dict:set("ATTACK_CYCLE", "300")
    config_dict:set("ATTACK_RATE", "10")
    config_dict:set("ATTACK_BANNED_TIME", "120")
    config_dict:set("ATTACK_BIG_CYCLE", "1800")
    config_dict:set("ATTACK_BANNED_TIMES_MAX", "5")

    config_dict:set("CC_LEVEL", "3")
    config_dict:set("GET_LEVEL", "4")
    config_dict:set("POST_LEVEL", "4")
    config_dict:set("UA_LEVEL", "2")
    config_dict:set("COOKIE_LEVEL", "2")
    config_dict:set("FORMDATA_LEVEL", "5")
end

return _C