import json
from flask import Blueprint, request, Response

from config import TEMPLATE_FOLDER
from bean import Session
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.DataCheck import check_phone_num, check_email

API_getinfo = Blueprint('getinfo', __name__, template_folder=TEMPLATE_FOLDER)


@API_getinfo.route('/user-info/getinfo', methods=['GET', 'POST'])
def get_user_info():
    user_id = Session.get('is_login')
    result = {}
    if request.method == 'GET':
        sql_get_info = "SELECT `username`,`phone`,`email`,`remark`,`phone_check`,`email_check` FROM `w_users` WHERE " \
                       "`uid` = ? "
        user_info = MYSQL.sql_with_select(sql=sql_get_info, data=(user_id,))
        try:
            username, phone, email, remark, inphone, inemail = user_info[0]
        except Exception as e:
            print(e)
            username, phone, email, remark, inphone, inemail = None, None, None, None, False, False
        result = {
            "info": {
                "username_": username,
                "phone": phone,
                "email": email,
                "remark": remark
            },
            "inphone": inphone == 1,
            "inemail": inemail == 1
        }
        return Response(json.dumps(result), mimetype='application/json')
    elif request.method == 'POST':
        sql_update = "UPDATE `w_users` SET `username`=?,`phone`=?,`email`=?,`remark`=? WHERE `uid`=?"
        if not check_phone_num(request.json['phone']):
            result['msg'] = "手机号格式出错"
        elif not check_email(request.json['email']):
            result['msg'] = "邮箱格式出错"
        else:
            status = {"res": MYSQL.sql_no_select(sql=sql_update, data=(
                request.json['username'], request.json['phone'], request.json['email'], request.json['remark'],
                user_id))}
            result = {"res": status, "msg": ""}
            if not status:
                result['msg'] = "后台出错了"
            else:
                log_waf(type_=8, detail=str((
                    request.json['username'], request.json['phone'], request.json['email'], request.json['remark'],
                    user_id)))
        return Response(json.dumps(result), mimetype='application/json')
    else:
        return Response(json.dumps(result), mimetype='application/json')
