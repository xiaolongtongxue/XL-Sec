import json
from flask import Blueprint, Response

from config import TEMPLATE_FOLDER
from dao import MYSQL

API_funs_interceptor = Blueprint('FunInterceptor', __name__, template_folder=TEMPLATE_FOLDER)


@API_funs_interceptor.route('/nearly/info/interceptor/', methods=['GET'])
def funs_interceptor():
    try:
        sql_res = MYSQL.sql_with_select(sql="SELECT `fun_name` FROM `w_funs`;", data=())
        res = []
        for data in sql_res:
            res.append(data[0])
        res.append("其他")
        result = {"result": res}
    except IndexError:
        result = {"msg": "数据库错误"}
    return Response(json.dumps(result), mimetype='application/json')
