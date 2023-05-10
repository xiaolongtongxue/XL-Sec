import json
from flask import Blueprint, Response

from config import TEMPLATE_FOLDER
from dao import MYSQL

API_total_counting = Blueprint('TotalCounting', __name__, template_folder=TEMPLATE_FOLDER)


@API_total_counting.route('/total/counting/', methods=['GET'])
def total_counting():
    result = {"numdata": {}}
    attack_types = MYSQL.sql_with_select(
        sql="SELECT `w_attack_types`.`atid`,`atname` FROM `w_attack_types` INNER JOIN `w_attack_log` ON "
            "`w_attack_types`.`atid`=`w_attack_log`.`atid` GROUP BY `atid`,`atname`;",
        data=())
    if not isinstance(attack_types, list):
        result = {"numdata": {"数据库出错": 0}}
        return Response(json.dumps(result), mimetype='application/json')
    if len(attack_types) <= 0:
        result = {"numdata": {"暂无数据": 0}}
        return Response(json.dumps(result), mimetype='application/json')
    for attack_type in attack_types:
        sql = "SELECT COUNT(`aeid`) FROM `w_attack_log` WHERE `atid`=?;"
        try:
            num = MYSQL.sql_with_select(sql=sql, data=(attack_type[0],))
            result['numdata'][attack_type[1]] = int(num[0][0])
        except IndexError:
            result['numdata'][attack_type[1]] = 0
    return Response(json.dumps(result), mimetype='application/json')
