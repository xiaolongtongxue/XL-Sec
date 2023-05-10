from config import LUA_SET_DATA_URL, LUA_SET_DATA_URL_HEADERS, LUA_UNLOCK_DATA_URL
import urllib.request


def update_lua_cache():
    opener = urllib.request.build_opener()
    opener.addheaders = [LUA_SET_DATA_URL_HEADERS]
    opener.open(LUA_SET_DATA_URL)


def update_lua_cache_unlock(ip: str):
    opener = urllib.request.build_opener()
    opener.addheaders = [LUA_SET_DATA_URL_HEADERS]
    opener.open(LUA_UNLOCK_DATA_URL + ip)
