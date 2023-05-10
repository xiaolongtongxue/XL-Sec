import json
from flask import Blueprint, Response

from bean import Session
from config import TEMPLATE_FOLDER, PANEL_DB_NUM
from dao import MYSQL
from dao import REDIS
from dao.LoggingApi import log_waf
from util.UpdateLuaCache import update_lua_cache

API_web_info = Blueprint('WebInfo', __name__, template_folder=TEMPLATE_FOLDER)


@API_web_info.route('/web-info/name/get/<string:web_id>', methods=['GET'])
def get_web_info(web_id):
    redis = REDIS()
    redis.select(PANEL_DB_NUM)
    web_name = redis.get("web:name:" + web_id)
    if web_name is not None:
        redis.expire("web:name:" + web_id, 3600)
        result = {"name": web_name}
        return Response(json.dumps(result), mimetype='application/json')
    sql = "SELECT `webname` FROM `w_web_info` WHERE `wid`=?;"
    web_names = MYSQL.sql_with_select(sql=sql, data=(web_id,))
    try:
        web_name = web_names[0][0]
    except IndexError:
        web_name = "无名站点"
    result = {"name": web_name}
    redis.set("web:name:" + web_id, web_name)
    redis.expire("web:name:" + web_id, 3600)
    return Response(json.dumps(result), mimetype='application/json')


@API_web_info.route('/web-del/wid/del/<string:web_id>', methods=['GET'])
def del_web_info(web_id):
    webname = MYSQL.sql_with_select(sql="SELECT `webname` FROM `w_web_info` WHERE `wid`=?;",
                                    data=(web_id,))[0][0]
    sql = "DELETE FROM `w_web_info` WHERE wid=?;"
    res = MYSQL.sql_no_select(sql=sql, data=(web_id,))
    if res:
        result = {"do": True}
        update_lua_cache()
        log_waf(
            type_=2,
            detail={
                "uid": Session.get('is_login'),
                "type": "web-delete",
                "webname": webname,
                "wid": web_id,
            }
        )
    else:
        result = {"do": True, "msg": "数据库出错"}
    return Response(json.dumps(result), mimetype='application/json')
