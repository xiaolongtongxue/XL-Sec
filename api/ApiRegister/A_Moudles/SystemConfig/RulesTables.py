import json
from flask import Blueprint, request, Response, render_template

from bean import Session
from config import TEMPLATE_FOLDER, INJECTIONS, WHITE_LIST
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache

API_rules_tables = Blueprint('RulesTables', __name__, template_folder=TEMPLATE_FOLDER)


@API_rules_tables.route('/rules/table/list/', methods=['GET'])
def rules_table():
    """
    获得相应的规则列表结构
    :return:
    """
    data_s = []
    try:
        data_s_table = MYSQL.sql_with_select(
            sql="SELECT `tip`,`explanation`,`nickname`,`ptname`,`code`,`isrule`,`isresp` FROM `w_rules_table` ORDER "
                "BY `num`;", data=())
        for line in data_s_table:
            istip = True if line[0] == 1 else False
            explanation = line[1]
            if istip:
                append_data = {"print": False, "description": explanation}
            else:
                id_ = line[2]
                save_types = line[3]
                return_code = line[4]
                isrule = True if line[5] else False
                isresp = True if line[6] else False
                append_data = {
                    "id": id_,
                    "save-types": save_types,
                    "description": explanation,
                    "return-code": return_code,
                    "rule": isrule,
                    "resp": isresp
                }
            data_s.append(append_data)
    except IndexError:
        result = {"msg": "数据库信息缺失"}
        return Response(json.dumps(result), mimetype='application/json')
    result = {
        "code": 0,
        "data": data_s
    }
    return Response(json.dumps(result), mimetype='application/json')


@API_rules_tables.route('/rules/table/info/getsize/', methods=['GET'])
def rules_info_size():
    """
    获得相应的界面尺寸
    :return:
    """
    layevents = request.args.get("layevents")
    events = request.args.get("events")
    if layevents is None or events is None:
        result = {"msg": "传参出错"}
        return Response(json.dumps(result), mimetype='application/json')
    if layevents == "get-rules":
        try:
            width, height = \
                MYSQL.sql_with_select(sql="SELECT `width`,`height` FROM `w_rules_table` WHERE `nickname`=?;",
                                      data=(events,))[0]
            result = {
                "width": int(width),
                "height": int(height)
            }
        except IndexError:
            result = {
                "width": 800,
                "height": 500
            }
    elif layevents == "get-resps":
        result = {"width": "90%", "height": "87%"}
    else:
        result = {"msg": "传参出错"}
    return Response(json.dumps(result), mimetype='application/json')


@API_rules_tables.route('/rules/table/info/html/', methods=['GET'])
def rules_info_html():
    """
    获得相应的规则或响应的对应列表
    :return:
    """
    layevents = request.args.get("layevents")
    events = request.args.get("events")
    if layevents == "get-rules":
        if events == "cc":
            return Response(json.dumps({"html": render_template("rules/" + events + ".html")}),
                            mimetype='application/json')
        elif events in INJECTIONS:
            return Response(json.dumps({"html": render_template("rules/injections.html")}),
                            mimetype='application/json')
        elif events in WHITE_LIST:
            return Response(json.dumps({"html": render_template("rules/iplist.html")}),
                            mimetype='application/json')
        else:
            return Response(json.dumps({"html": "<h1>传参错了草，你要不要看看你GET发的events是个啥？</h1>"}),
                            mimetype='application/json')
    else:
        try:
            html = MYSQL.sql_with_select(
                sql="SELECT `return_html` FROM `w_resps_info` INNER JOIN `w_rules_table` ON "
                    "`w_rules_table`.`ptid`=`w_resps_info`.`ptid` WHERE `nickname`=?;",
                data=(events,))[0][0]
            return Response(json.dumps({"html": html}), mimetype='application/json')
        except IndexError:
            return Response(json.dumps({"html": "<h1>数据库没数据呀啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊</h1>"}), mimetype='application/json')


@API_rules_tables.route('/resps/table/html/<string:nickname>', methods=['POST'])
def resps_set(nickname):
    from config import INJECTIONS
    new_html = request.json['new-html']
    if nickname not in INJECTIONS or new_html is None:
        result = {"do": False, "msg": "传参错误"}
    else:
        update_res = MYSQL.sql_no_select(
            sql="UPDATE `w_resps_info` SET `return_html`=? WHERE `ptid`=(SELECT `ptid` FROM `w_rules_table` WHERE "
                "`nickname`=?);",
            data=(new_html, nickname))
        if update_res:
            result = {"do": True}
            update_lua_cache()
            log_waf(
                type_=2,
                detail={
                    "uid": Session.get('is_login'),
                    "type": "resp-update",
                    "nickname": nickname
                }
            )
        else:
            result = {"do": False, "msg": "数据库错误"}
    return Response(json.dumps(result), mimetype='application/json')
