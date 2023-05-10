# -*- coding:utf-8 -*-
import datetime
import json

from flask import Flask, request, Response, session
from gevent import pywsgi

from ApiRegister import get_api_list as apis
from bean import Session
from bean.DemoMenu import Get_Menu
from config import *

app = Flask(
    __name__,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER
)
app.secret_key = SECERT_KEY
[app.register_blueprint(api) for api in apis()]
app.permanent_session_lifetime = datetime.timedelta(seconds=LOGIN_LIMIT)


@app.before_request
def check_login():
    is_login = Session.get('is_login', t_check=session.get('t_check') if session.get('t_check') else "")
    if is_login is None:
        # 没登陆的给爷登录去
        if request.path[0: 23] != "/login/get-verify-code/" and request.path[0: 6] != "/login":
            result = {"login": False, "lo": is_login}
            return Response(json.dumps(result), mimetype='application/json')
    else:
        # 已经登陆了就别来捣乱了
        if request.path[0: 6] == "/login":
            return "/"
        # 给key续命
        Session.live('is_login')


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = CHILD_PROTOCOL + "://" + CHILD_HOST
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/')
def menu_api():
    return Response(json.dumps(Get_Menu()), mimetype='application/json')


@app.errorhandler(500)
def panel_server_error():
    result = {"do": False, "res": False, "msg": "系统出现500错误，请检查接口状态"}
    return Response(json.dumps(result), mimetype='application/json')


# server = pywsgi.WSGIServer((HOSTS,PORT),app)
# server.serve_forever()

if __name__ == '__main__':
    app.run(
        host=HOSTS,
        port=PORT,
        debug=True
    )
