local redis = require "resty.redis"
local config = ngx.shared.w_config;
-- Redis主机、用户、密码
local REDIS_HOST = config:get('REDIS_HOST')
local REDIS_PORT = config:get('REDIS_PORT')
local REDIS_USER = config:get('REDIS_USER')
local REDIS_PASSWORD = config:get('REDIS_PASSWORD')

-- Redis连接池对象
local red_pool = {}

-- 连接池参数
local pool_max_idle_time = tonumber(config:get('REDIS_MAX_IDLE_TIME') or 60000)
local pool_size = tonumber(config:get('REDIS_POOL_SIZE') or 100)

-- RedisDao对象定义
local RedisDao = {}
RedisDao.__index = RedisDao

-- 创建RedisDao对象
function RedisDao:new()
    local self = setmetatable({}, RedisDao)
    self.red = redis:new()
    self.red:set_timeout(1000)
    local ok, err = self.red:connect(REDIS_HOST, REDIS_PORT)
    if not ok then
        ngx.log(ngx.ERR, "failed to connect to Redis: ", err)
        return nil, err
    end
    if REDIS_PASSWORD ~= "" then
        local res, err = self.red:auth(REDIS_PASSWORD)
        if not res then
            ngx.log(ngx.ERR, "failed to authenticate to Redis: ", err)
            return nil, err
        end
    end
    return self
end

-- 切换数据库
function RedisDao:select(index)
    local res, err = self.red:select(index)
    if not res then
        ngx.log(ngx.ERR, "failed to select Redis database: ", err)
        return false
    end
    return true
end

-- 设置键值对
function RedisDao:set(key, value)
    local res, err = self.red:set(key, value)
    if not res then
        ngx.log(ngx.ERR, "failed to set value to Redis: ", err)
        return false
    end
    return true
end

-- 获取值
function RedisDao:get(key)
    local res, err = self.red:get(key)
    if not res then
        ngx.log(ngx.ERR, "failed to get value from Redis: ", err)
        return nil, err
    end
    return res, nil
end

-- 删除值
function RedisDao:del(key)
    local res, err = self.red:del(key)
    if not res then
        ngx.log(ngx.ERR, "failed to del value from Redis: ", err)
        return nil, err
    end
    return res, nil
end

-- 自增值
function RedisDao:incr(key)
    local res, err = self.red:incr(key)
    if not res then
        ngx.log(ngx.ERR, "failed to incr value from Redis: ", err)
        return nil, err
    end
    return res, nil
end

-- 列表插入操作
function RedisDao:sadd(key, value)
    local res, err = self.red:sadd(key, value)
    if not res then
        ngx.log(ngx.ERR, "failed to sadd value to Redis: ", err)
        return false
    end
    return true
end

-- 设置过期时间
function RedisDao:expire(key, expire)
    local res, err = self.red:expire(key, expire)
    if not res then
        ngx.log(ngx.ERR, "failed to set expire to Redis: ", err)
        return false
    end
    return true
end

-- 事务操作
function RedisDao:multi()
    local ok, err = self.red:multi()
    if not ok then
        ngx.log(ngx.ERR, "failed to start multi: ", err)
        return false
    end
    return true
end

-- 事务提交
function RedisDao:exec()
    local res, err = self.red:exec()
    if not res then
        ngx.log(ngx.ERR, "failed to exec transaction: ", err)
        return false
    end
    return true
end

-- 回滚事务
function RedisDao:rollback()
    local res, err = self.red:discard()
    if not res then
        ngx.log(ngx.ERR, "failed to rollback transaction: ", err)
        return false
    end
    return true
end

-- 清空数据库
function RedisDao:flushdb()
    local res, err = self.red:flushdb()
    if not res then
        ngx.log(ngx.ERR, "failed to rollback transaction: ", err)
        return false
    end
    return true
end

-- 放回连接池
function RedisDao:release()
    if self.red then
        local ok, err = self.red:set_keepalive(pool_max_idle_time, pool_size)
        if not ok then
            ngx.log(ngx.ERR, "failed to set Redis keepalive: ", err)
            return false
        end
    end
    self.red = nil
    return true
end

return RedisDao
