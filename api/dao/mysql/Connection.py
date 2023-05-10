from mysql import connector
from mysql.connector import Error

from config import *  # MYSQL_HOST, MYSQL_PORT, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE

# MYSQL_HOST = "192.168.99.254"
# MYSQL_PORT = "53306"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "123456"
# MYSQL_DATABASE = "waftest"


class MySQL:
    def __init__(self, host: str = MYSQL_HOST, port: int = MYSQL_PORT, user: str = MYSQL_USER,
                 passwd: str = MYSQL_PASSWORD,
                 database: str = MYSQL_DATABASE):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._database = database
        self.connection = connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._passwd,
            database=self._database
        )
        self.cursor = self.connection.cursor(prepared=True)

    def sql_no_select(self, sql: str, data: tuple):
        try:
            self.reconnect()
            self.cursor.execute(sql, data)
            self.connection.commit()
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
            return True
        except Error as error:
            self.connection.rollback()
            print(f"Error occurred : {error}")
            # 回头在这里加上对log的支持
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
            return False

    def sql_with_select(self, sql: str, data: tuple):
        try:
            self.reconnect()
            self.cursor.execute(sql, data)
            select_result = self.cursor.fetchall()
            self.connection.commit()
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
            return select_result
        except Error as error:
            self.connection.rollback()
            print(f"Error occurred : {error}")
            # 回头在这里加上对log的支持
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
            return False

    def reconnect(self):
        self.connection = connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._passwd,
            database=self._database
        )
        self.cursor = self.connection.cursor(prepared=True)


# if __name__ == '__main__':
#     MYSQL = MySQL()
#     sql_count = "SELECT COUNT(`aeid`) FROM `w_attack_log`; "
#     try:
#         aeid = 'ffa68c06-c1ae-11ed-8b2c-0242ac110002'
#         ip = '127.0.0.1'
#         atid, fid, ruid = MYSQL.sql_with_select(
#             sql="SELECT `atid`,`fid`,`ruid` FROM `w_attack_log` WHERE `aeid`=? AND `remote_ip`=?;", data=(aeid, ip))[0]
#         print(atid + "::::" + fid + "::::" + ruid)
#         target_rule = \
#             MYSQL.sql_with_select(sql="SELECT `content` FROM `w_rules_info` WHERE `ruid`=?;", data=(ruid,))[0][0]
#
#         print(target_rule)
#         target_filter = MYSQL.sql_with_select(sql="SELECT `fun_name` FROM `w_funs` WHERE `fid`=?;", data=(fid,))[0][0]
#         print(target_filter)
#         explanation = \
#             MYSQL.sql_with_select(sql="SELECT `explanation` FROM `w_attack_types` WHERE `atid`=?;", data=(atid,))[0][0]
#         print(explanation.encode())
#     except Exception as e:
#         print(e)
#         pass
