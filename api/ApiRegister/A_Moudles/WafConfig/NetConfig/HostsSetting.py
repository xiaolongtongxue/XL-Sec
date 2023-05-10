import json
import shutil
import time
from flask import Blueprint, request, Response

from config import TEMPLATE_FOLDER
from util.Filter import is_valid_hosts

API_check_hosts = Blueprint('hosts-setting', __name__, template_folder=TEMPLATE_FOLDER)


@API_check_hosts.route('/sys/hosts/setting/get/', methods=['GET'])
def hosts_setting_get():
    try:
        with open('/etc/hosts', 'r') as f:
            hosts = f.read()
    except FileNotFoundError:
        do = False
        msg = "当前设备的/etc/hosts文件不存在，请手动排查"
        return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
    do = True
    return Response(json.dumps({"do": do, "host-setting-msg": hosts}), mimetype='application/json')


@API_check_hosts.route('/sys/hosts/setting/set/', methods=['POST'])
def hosts_setting_set():
    try:
        hosts = request.json['host-setting-msg']
    except KeyError:
        do = False
        msg = "传入参数错误"
        return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
    # check input
    if not is_valid_hosts(hosts):
        do = False
        msg = "hosts格式错误"
        return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
    # backup file
    now = time.strftime('%Y-%m-%d-%H:%M', time.localtime())
    backup_file = f'/etc/hosts.bak.{now}'
    shutil.copy('/etc/hosts', backup_file)
    # update file
    try:
        with open('/etc/hosts', 'w') as f:
            f.write(hosts)
        do = True
        msg = "hosts修改成功"
    except PermissionError:
        do = False
        msg = "权限不足，修改失败"
    return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
