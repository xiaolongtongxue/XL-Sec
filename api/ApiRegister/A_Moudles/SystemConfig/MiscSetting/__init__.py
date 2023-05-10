import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER, INJECTIONS, WHITE_LIST, TYPES_LIST
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache
from util.Filter import is_right_ip
from util.DeleteBlackCacheByIP import del_cache_by_ip

API_misc_settings = Blueprint('MiscSetting', __name__, template_folder=TEMPLATE_FOLDER)


@API_misc_settings.route('/rules/table/cc/', methods=['GET', 'POST'])
def cc_settings():
    if request.method == 'GET':
        try:
            cc_setting = MYSQL.sql_with_select(
                sql="SELECT `content` FROM `w_rules_info` WHERE `ptid`=(SELECT `ptid` FROM `w_rules_table` WHERE "
                    "`nickname`='cc')",
                data=())[0][0]
            result = json.loads(cc_setting.replace("'", '"'))
        except IndexError or json.decoder.JSONDecodeError:
            result = {"msg": "数据库出错"}
    elif request.method == 'POST':
        new_json_data = request.json
        if new_json_data['cycle'] is not None and new_json_data['rate'] is not None and new_json_data['lock-time'] \
                is not None and new_json_data['tolerate-times'] is not None and len(new_json_data) == 4:
            try:
                for key in new_json_data:
                    new_json_data[key] = str(new_json_data[key])
                res = MYSQL.sql_no_select(
                    sql="UPDATE `w_rules_info` SET `content`=? WHERE `ptid`=(SELECT `ptid` FROM `w_rules_table` WHERE "
                        "`nickname`='cc');",
                    data=(str(new_json_data).replace("'", '"'),))
                if res:
                    result = {"do": True}
                    update_lua_cache()
                    log_waf(
                        type_=2,
                        detail={
                            "uid": Session.get('is_login'),
                            "type": "rule-update",
                            "nickname": "cc",
                            "msg": "新的CC内容四个数据分别为：" + '、'.join(new_json_data.values())
                        }
                    )
                else:
                    result = {"msg": "数据库错误"}
            except ValueError:
                result = {"msg": "传参错误"}
        else:
            result = {"msg": "传参错误"}
    else:
        result = {"code": 405, "msg": "405 Method Not Allowed"}
    return Response(json.dumps(result), mimetype='application/json')


@API_misc_settings.route('/rules/table/<string:tabletype>/gets/<string:nickname>/', methods=['GET'])
def others_gets_setting(tabletype, nickname):
    result = {"code": 0, "data": []}
    if tabletype not in TYPES_LIST:
        result = {"msg": "传参出错！type::" + tabletype}
        return Response(json.dumps(result), mimetype='application/json')
    is_alive = request.args.get('use')
    right_names = INJECTIONS if tabletype == "others" else WHITE_LIST
    if (str(is_alive) != "1" and str(is_alive) != "0") or nickname not in right_names:
        result = {"msg": "传参出错！"}
        return Response(json.dumps(result), mimetype='application/json')
    sql_rules = MYSQL.sql_with_select(
        sql="SELECT `ruid`,`content`,`explanation` FROM `w_rules_info` WHERE `isalive`=? AND `ptid`=(SELECT `ptid` "
            "FROM `w_rules_table` WHERE `nickname`=?);", data=(str(is_alive), nickname))
    for ruid, rule_content, expl in sql_rules:
        result["data"].append({
            "id": ruid,
            "re-rules": rule_content,
            "expl": expl
        })
    return Response(json.dumps(result), mimetype='application/json')


@API_misc_settings.route('/rules/table/<string:tabletype>/news/<string:nickname>/', methods=['POST'])
def others_news_setting(tabletype, nickname):
    if tabletype not in TYPES_LIST:
        result = {"msg": "传参出错！type::" + tabletype}
        return Response(json.dumps(result), mimetype='application/json')
    right_names = INJECTIONS if tabletype == "others" else WHITE_LIST
    new_re = request.json['new-re']
    new_expl = request.json['expl']
    if new_re is None or new_expl is None or nickname not in right_names or len(new_re) == 0:
        result = {"do": False, "msg": "传参出错！"}
        return Response(json.dumps(result), mimetype='application/json')
    if tabletype == "iplist" and nickname != "url-white":
        for ip in new_re.split(" "):
            if not is_right_ip(ip):
                result = {"do": False, "msg": "请检查IP地址的输入格式！"}
                return Response(json.dumps(result), mimetype='application/json')
    sql_res = MYSQL.sql_no_select(
        sql="INSERT INTO `w_rules_info`(`ptid`,`fid`,`atid`,`isalive`,`content`,`explanation`) VALUES ((SELECT `ptid` "
            "FROM `w_rules_table` WHERE `nickname`=?),(SELECT `fid` FROM `w_funs` WHERE `ptid`=(SELECT `ptid` FROM "
            "`w_rules_table` WHERE `nickname`=?)),(SELECT `atid` FROM `w_attack_types` WHERE `diy`=1),0,?,?);",
        data=(nickname, nickname, new_re, new_expl)
    )
    if sql_res:
        result = {"do": True}
        update_lua_cache()
        log_waf(
            type_=2,
            detail={
                "uid": Session.get('is_login'),
                "type": "rule-update",
                "nickname": nickname,
                "msg": "新的规则【未开启】为：" + new_re
            }
        )
    else:
        result = {"do": False, "msg": "数据库出错！插入失败"}
    return Response(json.dumps(result), mimetype='application/json')


@API_misc_settings.route('/rules/table/<string:tabletype>/sets/<string:nickname>/', methods=['GET', 'POST'])
def others_sets_setting(tabletype, nickname):
    if tabletype not in TYPES_LIST:
        result = {"msg": "传参出错！type::" + tabletype}
        return Response(json.dumps(result), mimetype='application/json')
    right_names = INJECTIONS if tabletype == "others" else WHITE_LIST
    if nickname not in right_names:
        result = {"do": False, "msg": "传参出错！"}
        return Response(json.dumps(result), mimetype='application/json')
    if request.method == 'GET':
        # 更新开启关闭
        ruid = request.args.get('ruid')
        if ruid is None:
            result = {"do": False, "msg": "传参出错！"}
            return Response(json.dumps(result), mimetype='application/json')
        res = MYSQL.sql_no_select(sql="UPDATE `w_rules_info` SET `isalive`=ABS(`isalive`-1) WHERE `ruid`=?;",
                                  data=(ruid,))
    elif request.method == 'POST':
        # 更新最终结果
        ruid = request.json['ruid']
        new_re = request.json['new-re']
        expl = request.json['expl']
        if tabletype == "iplist" and nickname != "url-white":
            for ip in new_re.split(" "):
                if not is_right_ip(ip):
                    result = {"do": False, "msg": "请检查IP地址的输入格式！"}
                    return Response(json.dumps(result), mimetype='application/json')
        if ruid is None or new_re is None or expl is None or new_re == "" or expl == "":
            result = {"do": False, "msg": "传参出错！"}
            return Response(json.dumps(result), mimetype='application/json')
        res = MYSQL.sql_no_select(sql="UPDATE `w_rules_info` SET `content`=?,`explanation`=? WHERE `ruid`=?;",
                                  data=(new_re, expl, ruid))
    else:
        result = {"code": 405}
        return Response(json.dumps(result), mimetype='application/json')
    if res:
        result = {"do": True}
        update_lua_cache()
        if request.method == 'GET':
            # 更新规则开启 or 关闭
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "rule-update",
                    "nickname": nickname,
                    "msg": "以下ID的开关状态切换（请对应数据库查看）：" + ruid
                }
            )
        else:
            # 更新规则内容
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "rule-update",
                    "nickname": nickname,
                    "msg": "修改了规则，新的为：" + new_re + "；规则ID为：" + ruid
                }
            )
    else:
        result = {"do": False, "msg": "数据库出错！"}
    return Response(json.dumps(result), mimetype='application/json')


@API_misc_settings.route('/rules/table/<string:tabletype>/dels/<string:nickname>/', methods=['POST'])
def others_dels_setting(tabletype, nickname):
    if tabletype not in TYPES_LIST:
        result = {"msg": "传参出错！type::" + tabletype}
        return Response(json.dumps(result), mimetype='application/json')
    right_names = INJECTIONS if tabletype == "others" else WHITE_LIST
    ruid = request.json['ruid']
    rule = request.json['rule']
    if ruid is None or rule is None or nickname not in right_names:
        result = {"do": False, "msg": "传参出错！"}
        return Response(json.dumps(result), mimetype='application/json')
    sql_res = len(MYSQL.sql_with_select(sql="SELECT 1 FROM `w_rules_info` WHERE `ruid`=? AND `content`=?;",
                                        data=(ruid, rule))) > 0
    if sql_res:
        if nickname == "ip-black":
            sql1 = "UPDATE `w_auto_ip_bans` SET `unlock_time`=NOW() WHERE `ipaddress`=?;"
            sql2 = "DELETE FROM `w_rules_info` WHERE `ruid`=? AND `content`=?;"
            try:
                MYSQL.reconnect()
                MYSQL.cursor.execute(sql1, (rule,))
                MYSQL.cursor.execute(sql2, (ruid, rule))
                MYSQL.connection.commit()
                sql_res = True
                del_cache_by_ip(rule)
            except Exception as e:
                print(e)
                sql_res = False
        else:
            sql_res = MYSQL.sql_no_select(sql="DELETE FROM `w_rules_info` WHERE `ruid`=? AND `content`=?;",
                                          data=(ruid, rule))
        if sql_res:
            result = {"do": True}
            update_lua_cache()
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "rule-update",
                    "nickname": nickname,
                    "msg": "以下规则被删除：" + rule
                }
            )
        else:
            result = {"do": False, "msg": "数据库出错！"}
        return Response(json.dumps(result), mimetype='application/json')
    else:
        result = {"do": False, "msg": "数据不存在！"}
        return Response(json.dumps(result), mimetype='application/json')
