import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER, TOTAL_TYPES
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache
from util.Filter import is_live_hosts
from util.Filter import def_xss as dxss

API_webs_switch = Blueprint('WebsSwitch', __name__, template_folder=TEMPLATE_FOLDER)


@API_webs_switch.route('/switches/webs/', methods=['GET', 'POST'])
def webs_switches():
    result = {}
    if request.method == 'GET':
        web_names = MYSQL.sql_with_select(
            sql="SELECT `wid`,`webname`,`total_switch`,`switchs` FROM `w_web_info` ORDER BY `webname`;",
            data=())
        for web_name_tmp in web_names:
            try:
                web_id = web_name_tmp[0]
                web_name = dxss(web_name_tmp[1])
                w_total_switch = True if int(web_name_tmp[2]) == 1 else False
                switches_strs = web_name_tmp[3].split(" ")
                cc_switch = True if int(switches_strs[0]) == 1 else False
                inject_switch = True if int(switches_strs[1]) == 1 else False
                formdata_switch = True if int(switches_strs[2]) == 1 else False
                result[web_name] = {
                    "id": web_id,
                    "total": w_total_switch,
                    "cc": cc_switch,
                    "injection": inject_switch,
                    "form-data": formdata_switch
                }
            except IndexError or TypeError:
                result = {"msg": "数据库出错"}
    elif request.method == 'POST':
        wid = request.json['wid']
        event = request.json['event']
        end = request.json['e']
        if wid is None or event is None or end is None or (event > 2 or event < -1) or not isinstance(end, bool):
            result = {"do": False, "msg": "传参错误！！"}
            return Response(json.dumps(result), mimetype='application/json')
        end_s = 1 if end else 0
        if event == -1:
            sql_check_res = MYSQL.sql_no_select(sql="UPDATE `w_web_info` SET `total_switch`=? WHERE `wid`=?;",
                                                data=(end_s, wid))
            if sql_check_res:
                result = {"do": True}
                update_lua_cache()
                log_waf(
                    type_=2,
                    detail={
                        "uid": Session.get('is_login'),
                        "type": "switch",
                        "wid": wid,
                        "tid": 0,
                        "size": TOTAL_TYPES[-1],
                        "isOpen": end
                    }
                )
            else:
                result = {"do": False, "msg": "数据库错误！！"}
                return Response(json.dumps(result), mimetype='application/json')
        else:
            try:
                ago_res = \
                    MYSQL.sql_with_select(sql="SELECT `switchs` FROM `w_web_info` WHERE `wid`=?;", data=(wid,))[0][
                        0].split(" ")
                ago_res[event] = '1' if end else '0'
                res = ""
                for i in ago_res: res = res + i + " "
            except IndexError:
                result = {"do": False, "msg": "传入ID错误，别乱搞事儿哈！！"}
                return Response(json.dumps(result), mimetype='application/json')
            sql_check_res = MYSQL.sql_no_select(sql="UPDATE `w_web_info` SET `switchs`=? WHERE `wid`=?;;",
                                                data=(res, wid))
            if sql_check_res:
                result = {"do": True}
                update_lua_cache()
                log_waf(
                    type_=2,
                    detail={
                        "uid": Session.get('is_login'),
                        "type": "switch",
                        "wid": wid,
                        "tid": 0,
                        "size": TOTAL_TYPES[event],
                        "isOpen": end
                    }
                )
            else:
                result = {"do": False, "msg": "数据库错误！！"}
                return Response(json.dumps(result), mimetype='application/json')
    else:
        result = {"code": 405}
    return Response(json.dumps(result), mimetype='application/json')


@API_webs_switch.route('/switches/webs/info', methods=['GET', 'POST'])
def webs_info():
    if request.method == 'GET':
        wid = request.args.get('wid')
        if wid is None:
            result = {"msg": "传参错误！！"}
            return Response(json.dumps(result), mimetype='application/json')
        if wid != "new":
            try:
                webname, host, iscdn = MYSQL.sql_with_select(
                    sql="SELECT `webname`,`host`,`iscdn` FROM `w_web_info` WHERE `wid`=?;", data=(wid,))[0]
            except IndexError:
                result = {"msg": "数据库出错！"}
                return Response(json.dumps(result), mimetype='application/json')
            cdn = True if iscdn == 1 else False
            result = {
                "name": dxss(webname),
                "id": wid,
                "host": dxss(host),
                "cdn": cdn
            }
        else:
            return Response(json.dumps({}), mimetype='application/json')
    elif request.method == 'POST':
        webname = request.json['name']
        hosts = request.json['host']
        iscdn = request.json['cdn']
        wid = request.json['wid']
        if webname is None or hosts is None or iscdn is None or wid is None or not isinstance(iscdn, bool) \
                or not is_live_hosts(hosts):
            result = {"msg": "传参错误！！"}
            return Response(json.dumps(result), mimetype='application/json')
        if wid == "new":
            sql_res = MYSQL.sql_no_select(
                sql="INSERT INTO `w_web_info` (`webname`,`host`,`iscdn`) VALUES(?,?,?);",
                data=(webname, hosts, 1 if iscdn else 0))
        else:
            sql_res = MYSQL.sql_no_select(
                sql="UPDATE `w_web_info` SET `webname`=?,`host`=?,`iscdn`=? WHERE `wid`=?;",
                data=(webname, hosts, 1 if iscdn else 0, wid))
        if sql_res:
            result = {"do": True}
            update_lua_cache()
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "web-update",
                    "wid": wid,
                    "webname": webname,
                    "hosts": hosts,
                    "iscdn": iscdn
                }
            )
        else:
            result = {"do": False, "msg": "数据库出错"}
    else:
        result = {"code": 405}
    return Response(json.dumps(result), mimetype='application/json')
