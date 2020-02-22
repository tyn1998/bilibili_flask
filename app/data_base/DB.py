import pymysql
import sqlparse
import os


class DB:
    def __init__(self, host='localhost', port=3306, user='root', passwd='', db='', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    def __enter__(self):
        # 建立连接
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset=self.charset
        )
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 返回游标
        return self.cur

    def __exit__(self):
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def execute(self, sql, params):
        cur = self.__enter__()
        if sql.split(' ', 1)[0] != 'select':
            try:
                cur.execute(sql, params)
                result = cur.fetchall()
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
        else:   # 除了select语句，其他需要"事务"
            try:
                cur.execute(sql, params)
                result = cur.fetchall()
            except Exception as e:
                print(e)
        self.__exit__()
        return result


    """
        下面这个类函数一点都不类函数，
        想不好放哪里，还是放在类里吧，
        该函数读取指定sql文件并执行，
        代替了原来在workbench里手动
        执行sql文件的方式。
    """
    @classmethod
    def reset(cls):
        root_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        file_path = root_path + '/db_init.sql'
        with open(file_path, 'r', encoding='utf8') as sql_file:
            file_parse = sqlparse.parse(sql_file.read().strip())
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='TYn13646825688'
            )
            cur = conn.cursor()
            for sql in file_parse:
                cur.execute(sql.value)
            cur.close()
            conn.close()


