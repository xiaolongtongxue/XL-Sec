import json
from flask import Blueprint, Response
import datetime

from bean import Session
from config import TEMPLATE_FOLDER, PANEL_LUA_DB_NUM
from dao import MYSQL, REDIS

API_total_showing = Blueprint('TotalShowing', __name__, template_folder=TEMPLATE_FOLDER)


@API_total_showing.route('/total/showing/', methods=['GET'])
def total_showing():
    global tmp
    result = {}
    for errormax in range(5):
        try:
            begin_date = MYSQL.sql_with_select(sql="SELECT `begin_time` FROM `w_switch`;", data=())[0][0]
            redis = REDIS()
            redis.select(PANEL_LUA_DB_NUM)
            try:
                count = int(redis.get('attack:count'))
            except TypeError:
                count = int(MYSQL.sql_with_select(sql="SELECT COUNT(`aeid`) FROM `w_attack_log`;", data=())[0][0])
                redis.set('attack:count', str(count))
            for i in range(5):
                try:
                    count1 = int(MYSQL.sql_with_select(
                        sql="SELECT COUNT(`aeid`) FROM `w_attack_log` WHERE time>DATE_SUB(NOW(), INTERVAL 24 HOUR);",
                        data=())[0][0])
                    tmp = True
                    break
                except AttributeError:
                    tmp = False
                    continue
            attack_types = MYSQL.sql_with_select(
                sql="SELECT `atname` FROM `w_attack_types` INNER JOIN `w_attack_log` ON "
                    "`w_attack_types`.`atid`=`w_attack_log`.`atid` WHERE `w_attack_log`.`time`>DATE_SUB(NOW(), "
                    "INTERVAL 8 DAY) GROUP BY `atname`;",
                data=())
            if not tmp:
                return Response(json.dumps({"msg": "数据库出错"}), mimetype='application/json')
            eight_attack_types = []
            eight_days_info = []
            for attack_type in attack_types:
                eight_attack_types.append(attack_type[0])
                datas = []
                for i in range(8, 0, -1):
                    datas_sql_res = MYSQL.sql_with_select(
                        sql="SELECT COUNT(`aeid`) FROM `w_attack_log` WHERE `w_attack_log`.`time`>DATE_SUB(NOW(), "
                            "INTERVAL ? DAY) AND `w_attack_log`.`time`<DATE_SUB(NOW(), INTERVAL ? DAY) AND `atid`=("
                            "SELECT `atid` FROM `w_attack_types` WHERE `atname`=?);",
                        data=(i, i - 1, attack_type[0]))
                    datas.append(int(datas_sql_res[0][0]))
                eight_days_info.append(
                    {
                        "name": attack_type[0],
                        'type': 'line',
                        'data': datas
                    }
                )
            result = {
                "username": MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;",
                                                  data=(Session.get('is_login'),))[0][0],
                "save-days": (datetime.datetime.now() - begin_date).days,
                "lan-times": count1,
                "total-times": count,
                "system-status": 1,
                "for_echart": {
                    "attack-type": eight_attack_types,
                    'series': eight_days_info
                }
            }
            break
        except IndexError:
            result = {"msg": "数据出错"}
            break
        except ReferenceError or AttributeError:
            continue
    return Response(json.dumps(result), mimetype='application/json')
