import json

from flask import Blueprint, Response

from bean import Session
from config import TEMPLATE_FOLDER
from dao import MYSQL

API_User_Name = Blueprint('GetUserName', __name__, template_folder=TEMPLATE_FOLDER)


@API_User_Name.route('/info/get/username/', methods=['GET'])
def get_user_name():
    result = {"username": MYSQL.sql_with_select(sql="SELECT `username` FROM `w_users` WHERE `uid`=?;",
                                                data=(Session.get('is_login'),))[0][0], }
    return Response(json.dumps(result), mimetype='application/json')
