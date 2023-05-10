import re
import html


def is_live_hosts(hosts):
    if hosts is None:
        return False
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    for host in hosts.split(" "):
        if not pattern.match(host):
            # 考虑到录入IP的情况
            if not is_right_ip(host):
                return False
    return True


def def_xss(string: str):
    return html.escape(string)


def is_right_ip(ip_str):
    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(ip_str):
        return True
    else:
        pattern_ipv6 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^(([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4})?::(([' \
                       r'0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4})?$ '
        if re.match(pattern_ipv6, ip_str):
            return True
        return False


def is_valid_url(url_str):
    pattern = r'^https?://(?:(?:[\w\-]+\.)*[\w\-]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:\/[^\/?#]*)*(?:\?[' \
              r'^#]*)?(?:#.*)?$'
    if re.match(pattern, url_str):
        return True
    else:
        return False


def filter_netstat(str_: str):
    pattern = r'^-[a-zA-Z]+$'
    if re.match(pattern, str_):
        return True
    return False


def is_valid_phone(phone_str):
    pattern = r'^1[3-9]\d{9}$'
    if re.match(pattern, phone_str):
        return True
    else:
        return False


def is_valid_email(email_str):
    pattern = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,4}$'
    if re.match(pattern, email_str):
        return True
    else:
        return False


def is_valid_hosts(hosts):
    pattern = re.compile(r'^\s*(?:(?:\d{1,3}\.){3}\d{1,3}|(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})\s+[\w\-\.]+\s*$')
    lines = hosts.split('\n')
    print(hosts)
    for line in lines:
        print(line.strip())
        print(type(line.strip()))
        if line.strip().startswith('#') or not line.strip():
            continue
        if not pattern.match(line):
            return False
    return True


def filter_strings(str_list, pattern):
    """
    Filter out strings in a list that match a specific pattern.

    Args:
        str_list: A list of strings to be filtered.
        pattern: A regular expression pattern to match the strings.

    Returns:
        A list of strings that match the pattern.
    """
    filtered_list = []
    for s in str_list:
        if re.match(pattern, s):
            filtered_list.append(s)
    return filtered_list
