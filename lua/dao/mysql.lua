local mysql = require "resty.mysql"

local config = ngx.shared.w_config

-- MySQL主机、用户、密码、端口号等参数
local MYSQL_HOST = config:get('MYSQL_HOST')
local MYSQL_PORT = tonumber(config:get('MYSQL_PORT'))
local MYSQL_USER = config:get('MYSQL_USER')
local MYSQL_PASSWORD = config:get('MYSQL_PASSWORD')
local MYSQL_DATABASE = config:get('MYSQL_DATABASE')

-- 连接池参数
local pool_max_idle_time = tonumber(config:get('MYSQL_MAX_IDLE_TIME') or 60000)
local pool_size = tonumber(config:get('MYSQL_POOL_SIZE') or 100)

-- MysqlDao对象定义
local MysqlDao = {}
MysqlDao.__index = MysqlDao

-- 创建MysqlDao对象并连接MySQL
function MysqlDao:new()
    local self = setmetatable({}, MysqlDao)
    self.db, err = mysql:new()

    if not self.db then
        ngx.log(ngx.ERR, "failed to create mysql object: ", err)
        return nil, err
    end

    self.db:set_timeout(1000)

    local ok, err, errno, sqlstate = self.db:connect {
        host = MYSQL_HOST,
        port = MYSQL_PORT,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD,
        database = MYSQL_DATABASE,
        charset = 'utf8mb4',
        max_packet_size = 1024 * 1024,
    }

    if not ok then
        ngx.log(ngx.ERR, "failed to connect to MySQL: ", err, ": ", errno, " ", sqlstate)
        return nil
    end

    return self
end

-- 执行SQL查询语句
function MysqlDao:query(sql_query)
    local res, err, errno, sqlstate = self.db:query(sql_query)
    if not res then
        ngx.log(ngx.ERR, "failed to execute SQL query: ", err, ": ", errno, " ", sqlstate)
        return nil, err
    end
    return res, nil
end

-- 放回连接池
function MysqlDao:release()
    if self.db then
        local ok, err = self.db:set_keepalive(pool_max_idle_time, pool_size)
        if not ok then
            ngx.log(ngx.ERR, "failed to set MySQL keepalive: ", err)
            return false
        end
    end
    self.db = nil
    return true
end

return MysqlDao
