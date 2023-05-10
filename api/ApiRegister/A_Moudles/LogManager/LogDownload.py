import json
from flask import Blueprint, request, Response, render_template

from bean import Session
from config import TEMPLATE_FOLDER
from dao import MYSQL
from dao.LoggingApi import log_waf

API_log_download = Blueprint('LogDownload', __name__, template_folder=TEMPLATE_FOLDER)


@API_log_download.route('/waf-logging/download/', methods=['POST'])
def download_log():
    try:
        event = request.json.get('event')  # 三类事件（attack、ip或waf）
        type_ = request.json.get('type')  # 文本类型：json或html
        filename = request.json.get('filename')
    except KeyError:
        result = {"do": False, "msg": "传参错误"}
        return Response(json.dumps(result), mimetype='application/json')
    if event not in ['attack', 'ip', 'waf'] or type_ not in ['json', 'html']:
        result = {"do": False, "msg": "传参错误"}
        return Response(json.dumps(result), mimetype='application/json')
    result = []
    if event == 'attack':
        sql_select_attack_logs = "SELECT `aeid`,`remote_ip`,`level`,`webname`,`time`,`isbans`," \
                                 "`time_remain`,`atname`,`http` FROM `w_attack_log` INNER JOIN `w_attack_types`" \
                                 " on `w_attack_log`.`atid`=`w_attack_types`.`atid` INNER JOIN " \
                                 "`w_web_info` ON `w_attack_log`.`wid`=`w_web_info`.`wid` " \
                                 "ORDER BY `time` DESC;"
        datas = MYSQL.sql_with_select(sql=sql_select_attack_logs, data=())
        for data in datas:
            if data[6] == 0:
                msg = "永久"
            elif data[6] == -1:
                msg = "未封禁"
            else:
                msg = str(data[6])
            result.append({
                "id": data[0],
                "ipadddress": data[1],
                "level": data[2],
                "webname": data[3],
                "time": str(data[4]),
                "isbans": "是" if data[5] == 1 else "否",
                "time_remain": msg,
                "type": data[7],
                "http": data[8]
            })
        fields = ['事件ID', '攻击IP', '事件等级', '网站名', '时间', '是否封禁', '封禁时间', '攻击类型', 'http报文']
        title = '网站防护日志全部信息导出'
    elif event == 'ip':
        sql_select_ip_bans = "SELECT `ieid`,`remote_ip`,`time_remain`,`lock_time`,`unlock_time` FROM `w_auto_ip_bans` " \
                             "INNER JOIN `w_attack_log` ON `w_attack_log`.`aeid`=`w_auto_ip_bans`.`aeid` ORDER BY " \
                             "`lock_time` DESC;"
        datas = MYSQL.sql_with_select(sql=sql_select_ip_bans, data=())
        for data in datas:
            result.append({
                "id": data[0],
                "ipaddress": data[1],
                "time_remain": data[2],
                "lock_time": str(data[3]),
                "unlock_time": str(data[4]),
            })
        fields = ['封禁ID', '封禁IP', '封禁时间', '实际解封时间']
        title = '网站IP封禁日志全部信息导出'
    elif event == 'waf':
        sql_select_waf_logs = "SELECT `username`,`time`,`ip`,`operate`,`detail` FROM `w_waflog` INNER JOIN `w_users` " \
                              "ON `w_users`.`uid`=`w_waflog`.`uid` ORDER BY `time` DESC;"
        datas = MYSQL.sql_with_select(sql=sql_select_waf_logs, data=())
        for data in datas:
            type_ = data[3]
            if type_ == 1:
                msg = "用户登录"
            elif type_ == 2:
                msg = "防护配置修改"
            elif type_ == 3:
                msg = "文件下载动作"
            elif type_ == 4:
                msg = "系统配置修改"
            elif type_ == 5:
                msg = "用户主动退出"
            elif type_ == 6:
                msg = "用户自动退出"
            elif type_ == 7:
                msg = "日志相关修改变动"
            elif type_ == 8:
                msg = "用户信息修改(除密码)"
            elif type_ == 9:
                msg = "用户密码修改"
            else:
                msg = "Error!!!"
            result.append({
                "username": data[0],
                "time": str(data[1]),
                "ipaddress": data[2],
                "operate-type": msg,
                "detail": data[4]
            })
            fields = ['操作用户名', '操作时间','操作IP', '操作类型', '注解：请看文档解释']
            title = '网站IP封禁日志全部信息导出'
    log_waf(
        type_=3,
        detail={
            "uid": Session.get('is_login'),
            "filename": filename
        }
    )
    if type_ == 'json':
        return str(result)
    return render_template('demo-report/attack-log-report.html', title=title, data=result, fields=fields)
