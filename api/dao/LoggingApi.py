from bean import Session
from util.Get_IP import get_ip

from dao import MYSQL


def log_waf(type_: int, detail, user_id: str = None):
    """
    将waf中的一些行为记录进日志的函数，在这边会对各种各样的参数进行规定声明，type_的不同内容代表了不同的含义

    type_内容   表示的相应的类型
    1           用户登录行为
    2           修改了网站防护配置【包括了开关、规则、响应等】
    3           有文件下载动作【配置下载或日志下载】
    4           修改了系统的配置【比如部署配置之类的】
    5           用户主动退出登录
    6           自动退出登录【Session过期（弃用）、修改密码等】
    7           日志相关
    8           更新除了密码以外的用户信息
    9           修改了登录用户的密码

    :param type_:
    :param detail:
    :param user_id:
    :return:
    """
    if type_ > 9:
        return False
    ip = get_ip()
    if user_id is None: user_id = Session.get('is_login')
    detail = get_detail(type_=type_, inf=detail)
    if detail is None: return False
    res = MYSQL.sql_no_select(
        sql="INSERT INTO `w_waflog` (`uid`,`ip`,`operate`,`detail`) VALUES ('" + user_id + "',?,'" + str(
            type_) + "',?);",
        data=(ip, detail)
    )
    if res:
        return True
    else:
        return False


def get_detail(type_: int, inf):
    """
    该函数的主要意义在于对detail字段的生成
    :param type_:
    :param inf:
    :return:
    """
    # if isinstance(inf, str):
    #     return inf
    if type_ == 1 or type_ == 5:
        # 登录登出行为
        username = MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;", data=(inf,))[0][0]
        return username
    elif type_ == 2:
        # 规则变动
        if not isinstance(inf, dict): return str(inf)
        detail = ""
        try:
            username = \
                MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;", data=(inf['uid'],))[0][0]
            if inf['type'] == 'switch':
                # 开关相关的
                if isinstance(inf['size'], int):
                    size = '0'
                elif isinstance(inf['size'], str):
                    if isinstance(inf['wid'], str):
                        webname = MYSQL.sql_with_select(sql="SELECT `webname` FROM `w_web_info` WHERE `wid`=?;",
                                                        data=(inf['wid'],))[0][0]
                        size = "网站<span style='color:green'>" + webname + "</span> 的<span style='color:green'>" + \
                               inf['size'] + "开关</span>"
                    elif isinstance(inf['tid'], str):
                        size = "<span style='color:green'>" + inf['tid'] + "</span>类型 的总开关"
                    else:
                        size = "Error"
                else:
                    size = "Error"
                is_open = "on" if inf['isOpen'] else "off"
                detail = username + ":" + size + ":" + is_open
            elif inf['type'] == 'web-update':
                if inf['wid'] == "new":
                    content = "新增网站"
                    webname = "New"
                else:
                    content = "修改网站"
                    webname = MYSQL.sql_with_select(sql="SELECT `webname` FROM `w_web_info` WHERE `wid`=?;",
                                                    data=(inf['wid'],))[0][0]
                list_ = [webname, inf['hosts'], "开启" if inf['iscdn'] else "关闭"]
                detail = username + ":" + inf['type'] + ":" + content + ":" + str(list_)
            elif inf['type'] == "web-delete":
                detail = username + ":" + inf['type'] + ":" + inf['webname'] + ":" + inf['wid']
            elif inf['type'] == 'rule-update':
                ptname = MYSQL.sql_with_select(sql="SELECT `ptname` FROM `w_rules_table` WHERE `nickname`=?;",
                                               data=(inf['nickname'],))[0][0]
                detail = username + ":" + inf['type'] + ":" + ptname + ":" + inf['msg']
            elif inf['type'] == 'resp-update':
                ptname = MYSQL.sql_with_select(sql="SELECT `ptname` FROM `w_rules_table` WHERE `nickname`=?;",
                                               data=(inf['nickname'],))[0][0]
                detail = username + ":" + inf['type'] + ":" + ptname
            elif inf['type'] == 'upload':
                # 待补充
                pass
            else:
                detail = "日志模块出错"
        except KeyError or TypeError:
            # import traceback
            # traceback.print_exc()
            detail = "日志模块出错"
        return detail
    elif type_ == 3:
        # 文件下载行为
        if not isinstance(inf, dict): return None
        detail = MYSQL.sql_with_select(
            sql="SELECT `username` FROM `w_users` WHERE `uid`=?;", data=(inf['uid'],))[0][0] + ":" + inf['filename']
        return detail
    elif type_ == 4:
        # 修改了系统的部署、配置等
        return str(inf)
    elif type_ == 6:
        # 自动退出登录【Session过期（弃用）、修改密码等】
        return str(inf)
    elif type_ == 7:
        # 日志相关编辑
        username = \
            MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;", data=(inf['uid'],))[0][0]
        if inf['attack'] and not inf['ip-bans']:
            detail = "攻击记录检测表中的 " + inf['msg'] + "相关记录被删除"
        else:
            detail = "通过IP封禁记录表，IP地址" + inf['msg']
            if inf['isban']:
                detail = detail + " 被封禁，拉入黑名单"
            else:
                detail = detail + " 被解封"
        return username + ":" + detail
    elif type_ == 8:
        # 更新除了密码以外的用户信息
        return str(inf)
    elif type_ == 9:
        # 修改了登录用户的密码
        return str(inf)
    else:
        return str(inf)
