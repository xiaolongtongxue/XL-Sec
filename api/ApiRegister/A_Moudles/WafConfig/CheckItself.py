import json
import subprocess
from flask import Blueprint, request, Response

from config import TEMPLATE_FOLDER
from util.Filter import is_live_hosts, is_valid_url, filter_netstat

API_check_itself = Blueprint('check-itself', __name__, template_folder=TEMPLATE_FOLDER)


@API_check_itself.route('/sys/check/itself/', methods=['POST'])
def check_self():
    do_, msg = "", ""
    for key in request.json:
        if key == "check-ping":
            do_, msg = ping(request.json[key])
        elif key == "check-curl":
            do_, msg = curl(request.json[key])
        elif key == "check-tracert":
            do_, msg = tracert(request.json[key])
        elif key == "check-netstat":
            do_, msg = netstat(request.json[key])
        else:
            msg = "传参错误"
    result = {"do": do_, "msg": msg}
    return Response(json.dumps(result), mimetype='application/json')


def ping(address: str):
    if not is_live_hosts(address):
        return False, "格式出错，不是合格的host"
    if address == "": return False, "输入不能为空"
    cmd = ['ping', '-c', '4', address]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    ping_result = output.decode('utf-8')
    return True, ping_result


def tracert(address):
    if not is_live_hosts(address):
        return False, "格式出错，不是合格的host"
    if address == "": return False, "输入不能为空"
    cmd = ['traceroute', address]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    tracert_result = output.decode('utf-8')
    return True, tracert_result


def curl(url: str):
    if not is_valid_url(url):
        return False, "格式出错，不是合格的URL，请检查"
    if url == "": return False, "输入不能为空"
    cmd = ['curl', url]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    curl_result = output.decode('utf-8')
    return True, curl_result


def netstat(data):
    if not filter_netstat(data):
        return False, "格式出错，不是合格的参数【合格的比如说:\"-ntlp\"】"
    if data == "": return False, "输入不能为空"
    cmd = ['netstat', data]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    netstat_result = output.decode('utf-8')
    return True, netstat_result
