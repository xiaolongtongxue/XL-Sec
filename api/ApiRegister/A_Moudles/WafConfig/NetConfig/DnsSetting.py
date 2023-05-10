import json
import subprocess
import platform
import shutil
from flask import Blueprint, request, Response

from config import TEMPLATE_FOLDER
from util.Filter import is_right_ip

API_check_dns = Blueprint('dns-setting', __name__, template_folder=TEMPLATE_FOLDER)


@API_check_dns.route('/sys/dns/setting/get/', methods=['GET'])
def dns_setting_get():
    dns_config = subprocess.check_output(['cat', '/etc/resolv.conf']).decode('utf-8')
    dns_lines = dns_config.split('\n')
    dns1 = None
    dns2 = None
    for line in dns_lines:
        if line.startswith('nameserver'):
            dns_addr = line.split(' ')[1]
            if dns1 is None:
                dns1 = dns_addr
            else:
                dns2 = dns_addr
                break
    if dns1 is None:
        result = {"do": False}
    else:
        result = {
            "do": True,
            "dns1": dns1,
            "dns2": dns2
        }
    return Response(json.dumps(result), mimetype='application/json')


@API_check_dns.route('/sys/dns/setting/set/', methods=['POST'])
def dns_setting_set():
    try:
        dns1 = request.json['dns1']
        dns2 = request.json['dns2']
        if dns1 == "" or dns1 is None:
            do = False
            msg = "第一dns不能为空"
        else:
            if not is_right_ip(dns1) or (not is_right_ip(str(dns2)) and dns2 != "" and dns2 is not None):
                do = False
                msg = "请输入正确的IP地址"
                return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
            global cmd1, cmd2
            dist_name, dist_version, _ = platform.linux_distribution()
            if dist_name.lower() in ['centos', 'redhat', 'fedora', 'centos linux']:
                cmd1 = f"echo 'nameserver {dns1}' > /etc/resolv.conf"
                cmd2 = f"echo 'nameserver {dns2}' >> /etc/resolv.conf"
            elif dist_name.lower() in ['ubuntu', 'debian']:
                shutil.copy('/etc/resolv.conf', '/tmp/resolv.conf.tmp')
                # 修改临时文件中的内容
                with open('/tmp/resolv.conf.tmp', 'r') as f:
                    lines = f.readlines()
                if lines:
                    lines[0] = f"nameserver {dns1}\n"
                    if dns2 and dns2.strip():
                        lines.append(f"nameserver {dns2}\n")
                with open('/tmp/resolv.conf.tmp', 'w') as f:
                    f.writelines(lines)
                cmd1 = f"cp -f /tmp/resolv.conf.tmp /etc/resolv.conf"
                cmd2 = ""
            else:
                do = False
                msg = "您使用的Linux操作系统为：{" + dist_name.lower() + "}，不支持该操作"
                return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
            try:
                subprocess.run(cmd1, shell=True, check=True)
                print('cmd1 is ok')
                if dns2 and dns2.strip():
                    print('cmd2 is running')
                    subprocess.run(cmd2, shell=True, check=True)
                    print('cmd2 is ok')
                do = True,
                msg = "DNS地址修改成功"
            except subprocess.CalledProcessError:
                # import traceback
                # traceback.print_exc()
                do = False
                msg = "命令运行出错"
    except KeyError:
        do = False
        msg = "传参出错"
    return Response(json.dumps({"do": do, "msg": msg}), mimetype='application/json')
