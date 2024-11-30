from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Library.Common.Utils.SingletonTypeUtil import SingletonType
from sqlalchemy import text
from Library.Common.Utils.Contexts import ms_context
from Library.Common.Utils.YamlUtil import YamlUtil
from copy import deepcopy


class MysqlBase(metaclass=SingletonType):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.engine_dic = {}
        self.session_dic = {}
        self.cursor_dic = {}
        server_info = YamlUtil().load_common_config('mysql')
        for database in server_info['database'].split(","):
            server_info_tmp = deepcopy(server_info)
            server_info_tmp['database'] = database
            # 创建引擎
            engine = create_engine(
                self.construct_db_url(server_info_tmp),
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600,
                echo=True,
                isolation_level="AUTOCOMMIT"
            )
            # 创建会话,用于链式查询
            self.session_dic[database] = sessionmaker(bind=engine)()
            self.engine_dic[database] = engine
            self.cursor_dic[database] = engine.connect()
        self.session = self.session_dic[server_info['database'].split(",")[0]]
        self.cursor = self.cursor_dic[server_info['database'].split(",")[0]]
        ms_context.set(self)

    def change_database(self, db_name):
        if db_name not in self.session_dic:
            raise AssertionError(f"{db_name} 不存在，请检查")
        self.session = self.session_dic[db_name]
        self.cursor = self.cursor_dic[db_name]

    @staticmethod
    def construct_db_url(server):
        return "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(server["username"], server["password"], server["ip"],
                                                                  server["port"], server["database"], 'utf8')

    def query(self, sql):
        """
        数据查询，用于原始sql查询
        :param sql:
        :return:
        """
        print(f"sql: {sql}")
        # return self.cursor.execute(text(sql)).fetchall()._rows
        return list(self.cursor.execute(text(sql)))

    def update(self, sql):
        print(f"sql: {sql}")
        return self.cursor.execute(text(sql))


# ms = SqlAlchemyBase('sit')
