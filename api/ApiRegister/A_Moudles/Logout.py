from flask import Blueprint, session

from config import TEMPLATE_FOLDER
from bean import Session
from dao.LoggingApi import log_waf

API_logout = Blueprint('logout', __name__, template_folder=TEMPLATE_FOLDER)


@API_logout.route('/logout', methods=['GET'])
def logout():
    user_id = Session.get('is_login')
    Session.del_('is_login', islogout=True)
    log_waf(type_=5, detail=user_id, user_id=user_id)
    del session['t_check']
    return "1"
