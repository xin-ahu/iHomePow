"""

"""


import clickhouse_connect
import pymysql

from config import C1ickhouse_config, mysql_config


def ConnectClickHouse():
    try:
        client = clickhouse_connect.get_client(**C1ickhouse_config)
        print("Connected successfully!")
        return client
    except Exception as e:
        print(f"Failed to connect: {e}")
        raise


class ConnectMySql:
    def __init__(self):
        self.config = mysql_config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.config)
        except pymysql.MySQLError as e:
            print(f"数据库连接失败{e}")

    def query(self, query):
        if not self.connection:
            print("尚未建立数据库连接, 调用connect")
            return None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"查询执行失败: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("数据库连接关闭")



