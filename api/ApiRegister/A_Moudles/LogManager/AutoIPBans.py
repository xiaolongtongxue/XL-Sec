import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER, PANEL_LUA_DB_NUM, PANEL_DB_NUM
from dao import MYSQL
from dao import REDIS
from dao.LoggingApi import log_waf
from util.TimeToStamp import to_timestamp
from util.UpdateLuaCache import update_lua_cache, update_lua_cache_unlock
from util.DeleteBlackCacheByIP import del_cache_by_ip

API_attack_ip_bans = Blueprint('AttackIpBans', __name__, template_folder=TEMPLATE_FOLDER)


@API_attack_ip_bans.route('/ip-bans/logs/', methods=['GET', 'POST'])
def table_info():
    redis = REDIS()
    try:
        try:
            # 前端发来的页数和每页限制的行数
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
        except TypeError:
            page = 1
            limit = 10
        sql_ip_bans = "SELECT `ieid`,`remote_ip`,1,`wid`,`w_auto_ip_bans`.`aeid`,`time_remain`,`lock_time`," \
                      "`unlock_time` FROM `w_auto_ip_bans` INNER JOIN `w_attack_log` ON " \
                      "`w_attack_log`.`aeid`=`w_auto_ip_bans`.`aeid` ORDER BY `lock_time` DESC LIMIT ?,?;"
        sql_data = (str((page - 1) * limit), str(limit))
        # 查询到的数据总数（先从redis里边拉(本次需要调用的redis数据库需要和lua那边进行联动，需要一个string和一个zset)）
        redis.select(PANEL_LUA_DB_NUM)
        try:
            count = int(redis.get('attack:bans:count'))
        except TypeError:
            count = None
        logs, i = [], 0
        if count is None:
            # 第一次redis没查出来，说明已经出问题了，这一次全部跟着MySQL走
            count = int(MYSQL.sql_with_select(sql="SELECT COUNT(`ieid`) FROM `w_auto_ip_bans`;", data=())[0][0])
            redis.set('attack:bans:count', str(count))
            redis.select(PANEL_DB_NUM)
            redis.select(PANEL_DB_NUM)
            logs = get_attack_logs_with_sql(sql_select_ipbans_logs=sql_ip_bans, sql_data=sql_data,
                                            redis=redis, page=page, limit=limit, count=count)
        else:
            # 第一次redis查询没问题，说明还好，先跟着redis走，不行就扒拉MySQL
            redis.select(PANEL_DB_NUM)
            logs_rem = redis.zrange("attack:logs:cache", count - count % page - page * limit,
                                    count - count % page - (page * limit + limit))
            # 这边的REDIS调用的时候，使用的数量有问题，我暂时先给他噶了，后续再说
            if len(logs_rem) == 0 or 1 == 1:
                # redis里边键值出了问题
                logs = get_attack_logs_with_sql(sql_select_ipbans_logs=sql_ip_bans, sql_data=sql_data,
                                                redis=redis, page=page, limit=limit, count=count)
            else:
                # redis没出问题
                for log in logs_rem:
                    append_log = json.loads(log)
                    logs.append(append_log)
                    redis.expire("attack:bans:logs:cache", 60)
                    i = i + 1
        result = {
            "code": 0,
            "count": count,
            "data": logs
        }
    except Exception as e:
        print(e)
        result = {"msg": "接口出错"}
    return Response(json.dumps(result), mimetype='application/json')


@API_attack_ip_bans.route('/ip-bans/logs/info/', methods=['GET'])
def ip_bans_info():
    sql_ip_bans_info = "SELECT `lock_time`,`lock_reason`,`content`,`unlock_time`,`http` FROM `w_auto_ip_bans` INNER " \
                       "JOIN `w_attack_log` ON `w_attack_log`.`aeid`=`w_auto_ip_bans`.`aeid` INNER JOIN " \
                       "`w_rules_info` ON `w_attack_log`.`ruid`=`w_rules_info`.`ruid` WHERE `ieid`=? AND (SELECT " \
                       "`remote_ip` FROM `w_attack_log` WHERE `w_attack_log`.`aeid` = `w_auto_ip_bans`.`aeid` AND " \
                       "`remote_ip`=?) ORDER BY `lock_time`; "
    ieid = request.args.get('ieid')
    ip = request.args.get('ip')
    if ieid is None or ip is None:
        result = {"msg": "传入参数出错"}
        return Response(json.dumps(result), mimetype='application/json')
    res_data = MYSQL.sql_with_select(sql=sql_ip_bans_info, data=(ieid, ip))
    try:
        import datetime
        ip_bans_data = res_data[0]
        result = {
            "ban-time": str(int(float(to_timestamp(str(ip_bans_data[0]))))) + "000",
            "ban-reasons": ip_bans_data[1] if ip_bans_data[1] != "" else "自动封禁，暂无描述",
            "tag-rules": ip_bans_data[2],
            "unban-time": str(int(float(to_timestamp(str(ip_bans_data[3]))))) + "000" if ip_bans_data[
                                                                                             3] < datetime.datetime.now() else "暂未解封",
            "warn-http": ip_bans_data[4]
        }
    except IndexError:
        result = {"msg": "数据库信息缺失"}
    return Response(json.dumps(result), mimetype='application/json')


@API_attack_ip_bans.route('/ip-bans/logs/to-black', methods=['POST'])
def ip_to_black():
    try:
        ip = request.json['ip']
        aeid = request.json['aeid']
        try:
            ieid = request.json['ieid']
            isbans = check_data_ip_bans(ip=ip, aeid=aeid, ieid=ieid)
        except KeyError:
            ieid = MYSQL.sql_with_select(sql="SELECT `ieid` FROM `w_auto_ip_bans` WHERE `aeid`=? AND ?=(SELECT "
                                             "`remote_ip` FROM `w_attack_log` WHERE aeid=?);",
                                         data=(aeid, ip, aeid))
            if len(ieid) == 0:
                isbans = False
            else:
                ieid = ieid[0][0]
                isbans = check_data_ip_bans(ip=ip, aeid=aeid, ieid=ieid)
        check_res = True
        if check_res:
            # 证明该组数据真实存在，接下来直接拉黑
            #   1. 第一步，数据库中的简单记录表中所有该IP相关的解封时间标记为永久拉黑（方便表格重新恢复回来）
            #   2. 第二步，数据库中的黑名单需要添加相应的记录
            #   3. 第三步，通过调用内置的Lua程序将Redis缓存数据同步更新
            sql2 = "UPDATE `w_auto_ip_bans` SET `unlock_time`=ADDDATE(NOW(),INTERVAL 1000 YEAR) WHERE `aeid` IN (" \
                   "SELECT `aeid` FROM `w_attack_log` WHERE `remote_ip`=?); "
            if isbans:
                sql1 = ""
            else:
                sql1 = "INSERT INTO `w_auto_ip_bans` (`aeid`,`lock_time`,`unlock_time`,`ipaddress`) VALUES(?,NOW()," \
                       "ADDDATE(NOW(),INTERVAL 1000 YEAR),?) "

            sql3 = "INSERT INTO `w_rules_info` (`ptid`,`content`,`isalive`) VALUES ((SELECT `ptid` " \
                   "FROM`w_rules_table` WHERE `nickname`='ip-black'),?,1); "
            try:
                MYSQL.reconnect()
                if not isbans:
                    # redis = REDIS()
                    # redis.select(PANEL_LUA_DB_NUM)
                    # redis.incr('attack:bans:count')
                    MYSQL.cursor.execute(sql1, (aeid, ip))
                MYSQL.cursor.execute(sql2, (ip,))
                MYSQL.cursor.execute(sql3, (ip,))
                MYSQL.connection.commit()
            except Exception as error:
                print(error)
                MYSQL.connection.rollback()
                result = {"msg": "数据库出错"}
                return Response(json.dumps(result), mimetype='application/json')
            update_lua_cache()
            result = {"msg": "封禁成功"}
            log_waf(
                type_=7,
                detail={
                    "uid": Session.get('is_login'),
                    "del": True,
                    "attack": False,
                    "ip-bans": True,
                    "isban": True,
                    "msg": ip
                }
            )
        else:
            result = {"msg": "数据库信息缺失"}
    except KeyError as e:
        print(e)
        result = {"msg": "传参错误"}
    except IndexError as e:
        print(e)
        result = {"msg": "数据库错误"}
    return Response(json.dumps(result), mimetype='application/json')


@API_attack_ip_bans.route('/ip-bans/logs/to-un-black/', methods=['POST'])
def ip_undo_black():
    try:
        ip = request.json['ip']
        aeid = request.json['aeid']
        try:
            ieid = request.json['ieid']
        except KeyError:
            ieid_res = MYSQL.sql_with_select(sql="SELECT `ieid` FROM `w_auto_ip_bans` WHERE `aeid`=? AND ?=(SELECT "
                                                 "`remote_ip` FROM `w_attack_log` WHERE aeid=?);",
                                             data=(aeid, ip, aeid))
            if len(ieid_res) == 0:
                result = {"msg": "数据库出错，可尝试从“IP封禁日志”或黑名单中尝试解封"}
                return Response(json.dumps(result), mimetype='application/json')
            else:
                ieid = ieid_res[0][0]
        sql_check = "SELECT COUNT(`ieid`) FROM `w_auto_ip_bans` INNER JOIN `w_attack_log` ON " \
                    "`w_attack_log`.`aeid`=`w_auto_ip_bans`.`aeid` WHERE `ieid`=? AND (SELECT `remote_ip` FROM " \
                    "`w_attack_log` WHERE `w_attack_log`.`aeid` = ?)=?; "
        check_res = MYSQL.sql_with_select(sql=sql_check, data=(ieid, aeid, ip))[0][0] == 1
        if check_res:
            # 证明该组数据真实存在，接下来准备解封
            #   1. 第一步，数据库中的简单记录表中所有该IP相关的解封时间标记为当前时间NOW()
            #   2. 第二步，数据库中该IP如果存在于黑名单中的话，则需要将黑名单进行一并清除
            #   3. 第三步，最后应当重置Lua缓存中的相应内容（调用相应接口）
            sql1 = "UPDATE `w_auto_ip_bans` SET `unlock_time`=NOW() WHERE `aeid` IN (" \
                   "SELECT `aeid` FROM `w_attack_log` WHERE `remote_ip`=?);"
            sql2 = "DELETE FROM `w_rules_info` WHERE `ptid`=(SELECT `ptid` FROM`w_rules_table` WHERE " \
                   "`nickname`='ip-black') AND `content`=?;"
            try:
                MYSQL.reconnect()
                MYSQL.cursor.execute(sql1, (ip,))
                MYSQL.cursor.execute(sql2, (ip,))
                MYSQL.connection.commit()
            except Exception as error:
                print(error)
                MYSQL.connection.rollback()
                result = {"msg": "数据库出错"}
                return Response(json.dumps(result), mimetype='application/json')
            update_lua_cache()
            del_cache_by_ip(ip=ip)
            update_lua_cache_unlock(ip=ip)
            result = {"msg": "解封成功"}
            log_waf(
                type_=7,
                detail={
                    "uid": Session.get('is_login'),
                    "del": False,
                    "attack": False,
                    "ip-bans": True,
                    "isban": False,
                    "msg": ip
                }
            )
        else:
            result = {"msg": "数据库信息缺失"}
    except KeyError as e:
        print(e)
        result = {"msg": "传参错误"}
    except IndexError as e:
        print(e)
        result = {"msg": "数据库错误"}
    return Response(json.dumps(result), mimetype='application/json')


def get_attack_logs_with_sql(sql_select_ipbans_logs: str, sql_data: tuple, redis, page: int, limit: int, count: int):
    """
    该函数的最终意义在于根据MySQL在外存中相应数据的存储，得出一个相对稳定的结果
    :param sql_select_ipbans_logs:
    :param sql_data:
    :param redis:
    :param page:
    :param limit:
    :param count:
    :return:
    """
    logs, i = [], 0
    logs_rem = MYSQL.sql_with_select(sql_select_ipbans_logs, sql_data)
    for log in logs_rem:
        import datetime
        bans = True if datetime.datetime.now() < log[7] else False
        append_log = {
            "id": log[0],
            "ip": log[1],
            "bans": bans,
            "web-id": log[3],
            "event-id": log[4],
            "time-remain": int(log[5]),
            "timestamp1": str(int(float(to_timestamp(str(log[6]))))) + "000",
            "timestamp2": str(int(float(to_timestamp(str(log[7]))))) + "000"
        }
        logs.append(append_log)
        redis.zadd("attack:logs:cache", str(append_log), count - ((page - 1) * limit + i))
        redis.expire("attack:logs:cache", 60)
        i = i + 1
    return logs


def check_data_ip_bans(ip, aeid, ieid):
    sql_check = "SELECT COUNT(`ieid`) FROM `w_auto_ip_bans` INNER JOIN `w_attack_log` ON " \
                "`w_attack_log`.`aeid`=`w_auto_ip_bans`.`aeid` WHERE `ieid`=? AND (SELECT `remote_ip` FROM " \
                "`w_attack_log` WHERE `w_attack_log`.`aeid` = ?)=?;"
    return MYSQL.sql_with_select(sql=sql_check, data=(ieid, aeid, ip))[0][0] == 1
