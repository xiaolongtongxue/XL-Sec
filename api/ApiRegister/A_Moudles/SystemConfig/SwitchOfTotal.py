import json
from flask import Blueprint, request, Response

from bean import Session
from config import TEMPLATE_FOLDER
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache

API_total_switch = Blueprint('TotalSwitch', __name__, template_folder=TEMPLATE_FOLDER)


@API_total_switch.route('/switches/', methods=['GET', 'POST'])
def total_switch():
    if request.method == 'GET':
        for i in range(5):
            try:
                switch_check = MYSQL.sql_with_select(sql="SELECT `switch` FROM `w_switch`;", data=())[0][0]
                result = {"check": True if switch_check == 1 else False}
                break
            except IndexError:
                result = {"check": False, "msg": "数据库出错"}
                break
            except ReferenceError or AttributeError:
                continue
    elif request.method == 'POST':
        try:
            end = 1 if request.json['e'] else 0
            res = MYSQL.sql_no_select(sql="UPDATE `w_switch` SET `switch`=?;", data=(end,))
            result = {
                "s": res
            }
            if not res:
                result['msg'] = '数据库出错'
            else:
                update_lua_cache()
                log_waf(
                    type_=2,
                    detail={
                        "uid": Session.get('is_login'),
                        "type": "switch",
                        "size": 0,
                        "isOpen": request.json['e']
                    }
                )
        except KeyError:
            result = {"s": False, "msg": "传入参数出错"}
    else:
        result = {'code': 405}
    return Response(json.dumps(result), mimetype='application/json')
