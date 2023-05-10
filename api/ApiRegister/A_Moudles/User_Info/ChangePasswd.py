import datetime
import json
from flask import Blueprint, request, Response, session, render_template

from config import TEMPLATE_FOLDER, MAX_CHANGE_PASSWD_TIME, PANEL_TITLE, EMAIL_SEND_CYCLE
from bean import Session
from dao import MYSQL
from dao.LoggingApi import log_waf
from util.Check_Send import send_email
from util.Filter import is_valid_email
from util.Get_IP import get_ip
from util.VerifyCode import random_string

API_change_passwd = Blueprint('change_passwd', __name__, template_folder=TEMPLATE_FOLDER)


@API_change_passwd.route('/user-info/change-passwd/', methods=['GET'])
def change_passwd():
    """
    获取基本的状态要求，为GET请求
    :return:
    """
    try:
        uid = Session.get('is_login')
        username = MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;", data=(uid,))[0][0]
        is_phone = MYSQL.sql_with_select(sql="SELECT `phone_check` FROM `w_users` WHERE `uid`=?;", data=(uid,))[0][0]
        is_email = MYSQL.sql_with_select(sql="SELECT `email_check` FROM `w_users` WHERE `uid`=?;", data=(uid,))[0][0]
    except KeyError or IndexError:
        result = {"do": False, "msg": "后台出现错误"}
        return Response(json.dumps(result), mimetype='application/json')
    result = {"inphone": is_phone == 1, "inemail": is_email == 1, "info": {
        "change": True,
        "username": username
    }, 'stepitems': [{"title": "请输入旧密码和新密码"}, ]}
    if result['inphone'] and not result['inemail']:
        result['stepitems'].append({"title": "请进行短信验证码校验"}, )
    elif not result['inphone'] and result['inemail']:
        result['stepitems'].append({"title": "请进行邮箱验证码校验"}, )
    elif result['inphone'] and result['inemail']:
        result['stepitems'].append({"title": "请进行邮箱验证码和短信验证码校验"}, )
    result['stepitems'].append({"title": "完成"}, )
    return Response(json.dumps(result), mimetype='application/json')


@API_change_passwd.route('/user-info/change-passwd/get/salt/', methods=['POST'])
def get_salt_by_user():
    """
    修改密码时根据用户输入的旧密码获取用户的盐，方便前端加密
    :return:
    """
    try:
        username = request.json['username']
    except KeyError:
        result = {"do": False, "msg": "传参出错"}
        return Response(json.dumps(result), mimetype='application/json')
    salt = MYSQL.sql_with_select(sql="SELECT `salt` FROM `w_users` WHERE `username`=?;", data=(username,))
    if len(salt) > 0:
        return {"do": True, "data": salt[0][0]}
    else:
        return {"do": False, "msg": "用户名" + username + "不存在"}


@API_change_passwd.route('/user-info/change-passwd/check/old/', methods=['POST'])
def check_old_passed():
    """
    检查旧密码是否正确
    :return:
    """
    try:
        username = request.json['username']
        passwd_sha = request.json['passwd_sha']
    except KeyError:
        result = {"do": False, "msg": "传参出错"}
        return Response(json.dumps(result), mimetype='application/json')
    res = len(MYSQL.sql_with_select(sql="SELECT `uid` FROM `w_users` WHERE `username`=? AND `password`=?;",
                                    data=(username, passwd_sha))) > 0
    if res:
        phone_check, email_check = MYSQL.sql_with_select(
            sql="SELECT `phone_check`,`email_check` FROM `w_users` WHERE `username`=? AND `password`=?;",
            data=(username, passwd_sha))[0]
        Session.set(key="change_passwd_Token1", value="1", time=MAX_CHANGE_PASSWD_TIME)
        if phone_check == 0 and email_check == 0:
            # 如果都没有限制多重校验的话，就可以放行了
            Session.set(key="change_passwd_Token2", value="1", time=MAX_CHANGE_PASSWD_TIME)
        result = {"do": True}
    else:
        result = {"do": False, "msg": "旧密码错误"}
    return Response(json.dumps(result), mimetype='application/json')


@API_change_passwd.route('/user-info/change-passwd/end/update/', methods=['POST'])
def update_passwd():
    """
    更新密码
    :return:
    """
    if Session.get("change_passwd_Token1") is None or Session.get("change_passwd_Token2") is None:
        result = {"do": False, "msg": "操作超时", "tip": "您的操作已超时，请重新操作；如有渗透测试行为请立即停止。"}
        return Response(json.dumps(result), mimetype='application/json')
    try:
        username = request.json['username']
        sha_passwd = request.json['sha_passwd']
        salt = request.json['salt']
        print(sha_passwd)
        res = MYSQL.sql_no_select(sql="UPDATE `w_users` SET `password`=? WHERE `username`=? AND `salt`=?;",
                                  data=(sha_passwd, username, salt))
        if res:
            result = {"do": True, "msg": "密码更新成功", "tip": "当前账户Session已被清除，请点击下方按钮重新登陆"}
            log_waf(type_=9, detail=username)
            Session.del_('is_login', islogout=True)
            del session['t_check']
            Session.del_("change_passwd_Token1")
            Session.del_("change_passwd_Token2")
        else:
            result = {"do": False, "msg": "更新密码失败", "tip": "如无法登录，可考虑使用官方脚本重刷密码。"}
    except KeyError or IndexError:
        result = {"do": False, "msg": "Error", "tip": "传参错误或数据库错误，密码未修改"}
    return Response(json.dumps(result), mimetype='application/json')


@API_change_passwd.route('/user-info/change-passwd/email/send/', methods=['POST'])
def email_send():
    """
    确认邮箱地址没有问题并发送邮件
    :return:
    """
    if Session.get("change_passwd_Token1") is None:
        result = {"do": False, "msg": "操作超时，请刷新界面重新操作", "refresh": 5}
        return Response(json.dumps(result), mimetype='application/json')

    try:
        email_address = request.json['email']
        if Session.get("No-Sending:" + email_address) is not None:
            result = {"do": False, "msg": "发送太快，请稍后再试"}
            return Response(json.dumps(result), mimetype='application/json')
        if not is_valid_email(email_address):
            result = {"do": False, "msg": "Email地址格式出错"}
            return Response(json.dumps(result), mimetype='application/json')
        if email_address != MYSQL.sql_with_select(sql="SELECT `email` FROM `w_users` WHERE `uid`=?;",
                                                  data=(Session.get('is_login'),))[0][0]:
            result = {"do": False, "msg": "Email和预留的不同"}
            return Response(json.dumps(result), mimetype='application/json')
    except KeyError or IndexError:
        result = {"do": False, "msg": "传参出错"}
        return Response(json.dumps(result), mimetype='application/json')
    random_key = str.upper(random_string(length=7))
    ip = get_ip()
    res = send_email(receiver=email_address, send_title="一份来自--" + PANEL_TITLE + "--的验证码",
                     send_data=render_template('send-check/email.html', title=PANEL_TITLE, event="密码重置事件",
                                               code=random_key, ip=ip, url="https://www.txk123.top",
                                               time=datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')),
                     uid=Session.get('is_login'), ip=get_ip())
    if res:
        result = {"do": True}
        Session.set(key="Email-Key", value=random_key, time=MAX_CHANGE_PASSWD_TIME)
        Session.set(key="No-Sending:" + email_address, value=1, time=EMAIL_SEND_CYCLE)
    else:
        result = {"do": False, "msg": "邮箱发送失败"}
    return Response(json.dumps(result), mimetype='application/json')


@API_change_passwd.route('/user-info/change-passwd/email/check/', methods=['POST'])
def check_email_code():
    if Session.get("change_passwd_Token1") is None:
        result = {"do": False, "msg": "操作超时，请刷新界面重新操作，五秒后将自动刷新", "refresh": 5}
        return Response(json.dumps(result), mimetype='application/json')
    try:
        code = request.json['email-code']
        if code != Session.get("Email-Key"):
            result = {"do": False, "msg": "验证码错误"}
        else:
            result = {"do": True}
            if Session.get("change_passwd_Token_phone") is not None:
                Session.set(key="change_passwd_Token2", value="1", time=MAX_CHANGE_PASSWD_TIME)
                result['msg'] = '已完成全部验证'
            else:
                if MYSQL.sql_with_select(sql="SELECT `email_check` FROM `w_users` WHERE `uid`=?;",
                                         data=(Session.get('is_login'),))[0][0] != 1:
                    Session.set(key="change_passwd_Token_email", value="1", time=MAX_CHANGE_PASSWD_TIME)
                    result['msg'] = '还需手机验证'
                else:
                    Session.set(key="change_passwd_Token2", value="1", time=MAX_CHANGE_PASSWD_TIME)
                    result['msg'] = '已完成全部验证'
    except KeyError or IndexError:
        result = {"do": False, "msg": "传参出错"}
        return Response(json.dumps(result), mimetype='application/json')
    return Response(json.dumps(result), mimetype='application/json')
