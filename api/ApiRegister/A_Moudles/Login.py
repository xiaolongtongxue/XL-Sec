import json

from flask import Blueprint, session, request, Response

from config import TEMPLATE_FOLDER, CHILD_PROTOCOL, CHILD_HOST
from bean import Session
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.VerifyCode import generate_verification_code_image

API_login = Blueprint('login', __name__, template_folder=TEMPLATE_FOLDER)


@API_login.route('/login/get-verify-code/<string:size>/<int:len_>', methods=['GET'])
def verify_code(size, len_):
    size = (int(size.split(',')[0]), int(size.split(',')[1]))
    code, image_base = generate_verification_code_image(size=size, length=len_)
    if Session.get('v_code') is None:
        fst = True
    else:
        fst = False
    Session.set('v_code', code, islogin=fst)
    return image_base


@API_login.route('/login/get-salt/<string:username>/<verify_code_>', methods=['GET'])
def salt_with_user(username, verify_code_):
    try:
        if Session.get('v_code') is None:
            return "ee"
        if verify_code_.lower() != Session.get('v_code').lower():
            return "ee"
        sql = "SELECT `salt` FROM `w_users` WHERE `username`=?;"
        salt = MYSQL.sql_with_select(sql=sql, data=(username,))[0][0]
        Session.set('is_v_code', True)
        return salt
    except Exception as e:
        print(e)
        return "e"


@API_login.route('/login', methods=['POST'])
def login():
    if Session.get('is_v_code') is None:
        access = True if Session.get('is_v_code') == "1" else "0"
        if not access:
            return Response(json.dumps({"login": False}), mimetype='application/json')
    Session.del_('is_v_code')
    try:
        username = request.json['username']
        password = request.json['password']
        sql = "SELECT `uid` FROM `w_users` WHERE `username` = ? and `password` = ?;"
        sql_res = MYSQL.sql_with_select(sql=sql, data=(username, password))
        if len(sql_res) > 0:
            # Login Successfully
            uid = sql_res[0][0]
            Session.set('is_login', uid)
            Session.live('is_login')
            Session.del_('v_code')
            session['t_check'] = Session.get_token()[0:9]
            log_waf(type_=1, detail=uid, user_id=uid)
            try:
                referer = request.json['referer']
                if CHILD_PROTOCOL + "://" + CHILD_HOST not in referer: referer = "/"
            except Exception:
                referer = "/"
            result = {"login": True, "href": referer}
        else:
            result = {"login": False}
        return Response(json.dumps(result), mimetype='application/json')
    except Exception as e:
        print(e)
        return ""
