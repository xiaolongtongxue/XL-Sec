import json
from flask import Blueprint, request, Response

from config import TEMPLATE_FOLDER
from dao import MYSQL
from util.TimeToStamp import to_timestamp

API_waf_log_bak = Blueprint('WafLogBak', __name__, template_folder=TEMPLATE_FOLDER)


@API_waf_log_bak.route('/waf-operate/logs/get/', methods=['GET'])
def get_waf_log():
    try:
        try:
            # 前端发来的页数和每页限制的行数
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
        except TypeError:
            page = 1
            limit = 10
        sql_waf_log = "SELECT `username`,`time`,`ip`,`operate`,`detail` FROM `w_waflog` INNER JOIN `w_users` ON " \
                      "`w_users`.`uid`=`w_waflog`.`uid` ORDER BY `time` DESC LIMIT ?,?;"
        log_data = MYSQL.sql_with_select(sql=sql_waf_log, data=(page, limit))
        logs, index = [], (page - 1) * limit
        for log in log_data:
            index += 1
            logs.append({
                "index": index,
                "timestamp": str(int(float(to_timestamp(str(log[1]))))) + "000",
                "ip": log[2],
                "operating": log[3],
                "detail": log[4]
            })
        result = {
            "code": 0,
            "count": int(MYSQL.sql_with_select(sql="SELECT COUNT(`oeid`) FROM `w_waflog`;", data=())[0][0]),
            "data": logs
        }
    except Exception:
        import traceback
        traceback.print_exc()
        result = {"msg": "接口出错"}
    return Response(json.dumps(result), mimetype='application/json')


@API_waf_log_bak.route('/waf-operate/logs/del/', methods=['GET'])
def del_waf_log():
    sql = "DELETE FROM `w_waflog`;"
    res = MYSQL.sql_no_select(sql=sql, data=())
    if res:
        result = {"do": True}
    else:
        result = {"do": False, "msg": "删除失败"}
    return Response(json.dumps(result), mimetype='application/json')
