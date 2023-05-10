import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache

API_types_switch = Blueprint('TypesSwitch', __name__, template_folder=TEMPLATE_FOLDER)


@API_types_switch.route('/switches/type/get/', methods=['GET'])
def type_switch_get():
    try:
        sql_data = MYSQL.sql_with_select(sql="SELECT `t_switchs` FROM `w_switch`;", data=())[0][0]
        cc_s = True if sql_data.split(" ")[0] == '1' else False
        inject_s = True if sql_data.split(" ")[1] == '1' else False
        formdata_s = True if sql_data.split(" ")[2] == '1' else False
        result = {
            "cc": cc_s,
            "injection": inject_s,
            "form-data": formdata_s
        }
    except IndexError:
        result = {"msg": "数据库出错"}
    return Response(json.dumps(result), mimetype='application/json')


@API_types_switch.route('/switches/type/set/', methods=['POST'])
def type_switch_set():
    try:
        event = request.json['event']
        status = request.json['e']
        e_num = int(request.json['e_num'])
        # 白名单机制，严防死守
        if event is None or status is None or e_num is None or (e_num == 0 and event != 'cc') or (
                e_num == 1 and event != "injection") or (e_num == 2 and event != "form-data") or \
                not isinstance(status, bool):
            result = {"do": False, "msg": "传参错误！！"}
            return Response(json.dumps(result), mimetype='application/json')
        sql_back_data = MYSQL.sql_with_select(sql="SELECT `t_switchs` FROM `w_switch`;", data=())[0][0].split(" ")
        sql_back_data[e_num] = "1" if status else "0"
        res = ""
        for i in sql_back_data: res += i + " "
        sql_update_res = MYSQL.sql_no_select(sql="UPDATE `w_switch` SET `t_switchs`=?", data=(res[0:-1],))
        if sql_update_res:
            result = {
                "do": True
            }
            update_lua_cache()
            print(request.json)
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "switch",
                    "wid": 0,
                    "tid": event,
                    "size": event,
                    "isOpen": status
                }
            )
        else:
            result = {"do": False, "msg": "数据库出错，更新失败"}
    except IndexError:
        result = {"do": False, "msg": "数据库出错"}
    except TypeError:
        result = {"do": False, "msg": "传参出错"}
    return Response(json.dumps(result), mimetype='application/json')
