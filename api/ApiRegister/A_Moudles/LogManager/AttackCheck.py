import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER, PANEL_LUA_DB_NUM, PANEL_DB_NUM
from dao import MYSQL
from dao import REDIS
from dao.LoggingApi import log_waf
from util.TimeToStamp import to_timestamp

API_attack_check = Blueprint('AttackCheck', __name__, template_folder=TEMPLATE_FOLDER)


@API_attack_check.route('/attack/logs', methods=['GET', 'POST'])
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
        sql_select_attack_logs = "SELECT `aeid`,`remote_ip`,`level`,`wid`,`time`,`isbans`,`time_remain`,`atname` FROM " \
                                 "`w_attack_log` INNER JOIN `w_attack_types` on " \
                                 "`w_attack_log`.`atid`=`w_attack_types`.`atid` ORDER BY `time` DESC LIMIT ?,?; "
        sql_data = (str((page - 1) * limit), str(limit))
        # 查询到的数据总数（先从redis里边拉(本次需要调用的redis数据库需要和lua那边进行联动，需要一个string和一个zset)）
        redis.select(PANEL_LUA_DB_NUM)
        try:
            count = int(redis.get('attack:count'))
        except TypeError:
            count = None
        logs, i = [], 0
        if count is None:
            # 第一次redis没查出来，说明已经出问题了，这一次全部跟着MySQL走
            count = int(MYSQL.sql_with_select(sql="SELECT COUNT(`aeid`) FROM `w_attack_log`;", data=())[0][0])
            redis.set('attack:count', str(count))
            redis.select(PANEL_DB_NUM)
            logs = get_attack_logs_with_sql(sql_select_attack_logs=sql_select_attack_logs, sql_data=sql_data,
                                            redis=redis, page=page, limit=limit, count=count)
        else:
            # 第一次redis查询没问题，说明还好，先跟着redis走，不行就扒拉MySQL
            redis.select(PANEL_DB_NUM)
            logs_rem = redis.zrange("attack:logs:cache", count - count % page - page * limit,
                                    count - count % page - (page * limit + limit))
            # 这边的REDIS调用的时候，使用的数量有问题，我暂时先给他噶了，后续再说
            if len(logs_rem) == 0 or 1 == 1:
                # redis里边键值出了问题
                logs = get_attack_logs_with_sql(sql_select_attack_logs=sql_select_attack_logs, sql_data=sql_data,
                                                redis=redis, page=page, limit=limit, count=count)
            else:
                # redis没出问题
                for log in logs_rem:
                    append_log = json.loads(log)
                    logs.append(append_log)
                    # redis.zadd("attack:logs:cache", append_log, count - ((page - 1) * limit + i))
                    redis.expire("attack:logs:cache", 60)
                    i = i + 1

        result = {
            "code": 0,
            "count": count,
            "data": logs
        }
    except Exception as e:
        result = {"msg": "接口出错"}
    return Response(json.dumps(result), mimetype='application/json')


@API_attack_check.route('/web-info/logs/get/', methods=['GET', 'POST'])
def web_log_info():
    if request.method == 'GET':
        # 获取详细信息
        aeid = request.args.get('aeid')
        ip = request.args.get('ip')
        atid, fid, ruid = MYSQL.sql_with_select(
            sql="SELECT `atid`,`fid`,`ruid` FROM `w_attack_log` WHERE `aeid`=? AND `remote_ip`=?;", data=(aeid, ip))[0]
        try:
            target_rule = \
                MYSQL.sql_with_select(sql="SELECT `content` FROM `w_rules_info` WHERE `ruid`=?;", data=(ruid,))[0][0]
        except IndexError:
            target_rule = ""
        try:
            target_filter = MYSQL.sql_with_select(sql="SELECT `fun_name` FROM `w_funs` WHERE `fid`=?;", data=(fid,))[0][
                0]
        except IndexError:
            target_filter = ""
        try:
            explanation = \
                MYSQL.sql_with_select(sql="SELECT `explanation` FROM `w_attack_types` WHERE `atid`=?;", data=(atid,))[
                    0][0]
        except IndexError:
            explanation = ""
        try:
            http = MYSQL.sql_with_select(sql="SELECT `http` FROM `w_attack_log` WHERE `aeid`=?;", data=(aeid,))[0][0]
        except IndexError:
            http = ""
        result = {
            "tag-rules": target_rule,
            "tag-func": target_filter,
            "tag-dang": get_dang_line(http, target_rule),
            "fact-sheet": explanation
        }
        if result['tag-func'] == 'cc()':
            result["tag-rules"] = "寄"
            result['tag-dang'] = "命中CC规则，访问过快"
        return Response(json.dumps(result), mimetype='application/json')
    elif request.method == 'POST':
        # 获取详细的HTTP信息
        aeid = request.json.get('aeid')
        ip = request.json.get('ip')
        if aeid is None or ip is None:
            result = {"msg": "传入参数错误"}
            return Response(json.dumps(result), mimetype='application/json')
        try:
            result = {
                "http": MYSQL.sql_with_select(sql="SELECT `http` FROM `w_attack_log` WHERE `aeid`=?;", data=(aeid,))
                [0][0]}
        except IndexError:
            result = {"msg": "数据库数据缺失"}
        return Response(json.dumps(result), mimetype='application/json')


@API_attack_check.route('/web-info/logs/del/', methods=['POST'])
def web_log_del():
    redis = REDIS()
    nums = request.json.get('nums')
    if nums is None:
        aeid = request.json.get('aeid')
        ip = request.json.get('ip')
        if aeid is None or ip is None:
            result = {"msg": "传入参数错误"}
            return Response(json.dumps(result), mimetype='application/json')
        res = MYSQL.sql_no_select(sql="DELETE FROM `w_attack_log` WHERE `aeid`=? AND `remote_ip`=?;", data=(aeid, ip))
        if res:
            redis.select(PANEL_LUA_DB_NUM)
            redis.redis.decr('attack:count')
            result = {"res": True, "msg_": "删除成功"}
            log_waf(
                type_=7,
                detail={
                    "uid": Session.get('is_login'),
                    "del": True,
                    "attack": True,
                    "ip-bans": False,
                    "msg": ip
                }
            )
        else:
            result = {"res": False, "msg_": "删除失败"}
        return Response(json.dumps(result), mimetype='application/json')
    else:
        data = request.json.get('data')
        try:
            if len(data) == 0:
                result = {"res": False, "msg_": "选择项目为空"}
            else:
                sql_dels = "DELETE FROM `w_attack_log` WHERE"
                data_ = ()
                for i in range(len(data)):
                    sql_dels += " `aeid`=? AND `remote_ip`=? OR"
                    data_ += (data[i]['aeid'], data[i]['ip'])
                sql_dels += " 1=2;"
                res = MYSQL.sql_no_select(sql=sql_dels,
                                          data=data_)
                if res:
                    redis.select(PANEL_LUA_DB_NUM)
                    for i in range(len(data)):
                        redis.redis.decr('attack:count')
                    result = {"res": True, "msg_": "删除成功"}
                    log_waf(
                        type_=7,
                        detail={
                            "uid": Session.get('is_login'),
                            "del": True,
                            "attack": True,
                            "ip-bans": False,
                            "msg": '、'.join(set([d['ip'] for d in data]))
                        }
                    )
                else:
                    result = {"res": False, "msg_": "删除失败"}
        except IndexError:
            result = {"res": False, "msg_": "删除失败"}
        return Response(json.dumps(result), mimetype='application/json')


def get_attack_logs_with_sql(sql_select_attack_logs: str, sql_data: tuple, redis, page: int, limit: int, count: int):
    """
    该函数的最终意义在于根据MySQL在外存中相应数据的存储，得出一个相对稳定的结果
    :param sql_select_attack_logs:
    :param sql_data:
    :param redis:
    :param page:
    :param limit:
    :param count:
    :return:
    """
    logs, i = [], 0
    logs_rem = MYSQL.sql_with_select(sql_select_attack_logs, sql_data)
    for log in logs_rem:
        import datetime
        bans = False if datetime.datetime.now() > log[4] + datetime.timedelta(seconds=int(log[6])) else True
        unlock_search = MYSQL.sql_with_select(sql="SELECT `unlock_time` FROM `w_auto_ip_bans` WHERE `aeid`=?;",
                                              data=(log[0],))
        if len(unlock_search) == 0:
            pass
        else:
            unlock_time = unlock_search[0][0]
            bans = False if unlock_time < datetime.datetime.now() else True
        if not bans:
            try:
                bans = MYSQL.sql_with_select(
                    sql="SELECT `unlock_time` FROM `w_auto_ip_bans` WHERE `ipaddress`=? LIMIT 0,1;",
                    data=(log[1],))[0][0] > datetime.datetime.now()
            except IndexError:
                pass
        append_log = {
            "timestamp": str(int(float(to_timestamp(str(log[4]))))) + "000",
            "eid": log[0],
            "ip": log[1],
            "ret": True if log[5] == 1 else False,
            "level": int(log[2]),
            "web-id": log[3],
            'bans': bans,
            "time-remain": int(log[6]),
            'attack-type': log[7]
        }
        logs.append(append_log)
        redis.zadd("attack:logs:cache", str(append_log), count - ((page - 1) * limit + i))
        redis.expire("attack:logs:cache", 60)
        i = i + 1
    return logs


def get_dang_line(string: str, re_s: str):
    """
    在前端了解详情的时候，需要后端提供一下正则检测到的主要行号。
    该函数的意义就在于从HTTP中根据正则再把之前有问题的那一行给拉出来
    :param string: 
    :param re_s: 
    :return: 
    """
    import re
    for word in string.split("\n"):
        res = re.findall(re_s, word)
        if len(res) != 0:
            return word
    return ""
