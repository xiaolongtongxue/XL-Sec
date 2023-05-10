from flask import request


def get_ip():
    try:
        if request.headers['X-Forwarded-For'] is not None:
            return request.headers['X-Forwarded-For']
        elif request.headers['X-Real-IP'] is not None:
            return request.headers['X-Real-IP']
        else:
            return request.remote_addr
    except:
        return "0.0.0.0"


def get_ip_p():
    return ":" + get_ip() + ":"
