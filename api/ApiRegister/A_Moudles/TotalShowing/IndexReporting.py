import json
from flask import Blueprint, Response, request, render_template
import datetime

from bean import Session
from config import TEMPLATE_FOLDER
from dao import MYSQL
from dao.LoggingApi import log_waf

API_total_reporting = Blueprint('TotalReporting', __name__, template_folder=TEMPLATE_FOLDER)


@API_total_reporting.route('/total/reporting/', methods=['POST'])
def total_reporting():
    try:
        time1 = datetime.datetime.fromtimestamp((request.json['time'][0]) / 1000)
        time2 = datetime.datetime.fromtimestamp((request.json['time'][1]) / 1000)
        filename = request.json['filename']
        if time1 > time2:
            time1, time2 = time2, time1
        if not (request.json['type'] == "html" or request.json['type'] == "json"):
            return Response(json.dumps({}), mimetype='application/json')
        sql = "SELECT `aeid`,`remote_ip`,`level`,`wid`,`time`,`isbans`,`time_remain`,`atname`,`http` FROM " \
              "`w_attack_log` INNER JOIN `w_attack_types` on " \
              "`w_attack_log`.`atid`=`w_attack_types`.`atid` WHERE `time` BETWEEN ? AND ? ORDER BY `time`;"
        res = MYSQL.sql_with_select(sql=sql, data=(time1, time2))
        result = []
        for r in res:
            wid = r[3]
            sql = "SELECT `webname`,`host` FROM `w_web_info` WHERE `wid`=?;"
            web_info = MYSQL.sql_with_select(sql=sql, data=(wid,))
            try:
                web_name = web_info[0][0]
                web_hosts = web_info[0][1]
            except IndexError:
                web_name = "无名站点"
                web_hosts = "None Host"
            result.append({
                "id": r[0],
                "time": r[4],
                "remote_ip": r[1],
                "level": r[2],
                "webname": web_name,
                "host": web_hosts,
                "time_remain": r[6],
                "Attack_Type": r[7],
                "http": r[8]
            })
    except KeyError or IndexError:
        return Response(json.dumps({}), mimetype='application/json')
    log_waf(
        type_=3,
        detail={
            "uid": Session.get('is_login'),
            "filename": filename
        }
    )
    if request.json['type'] == "json":
        return str(result)
    else:
        return render_template("demo-report/total-report.html", items=result)
