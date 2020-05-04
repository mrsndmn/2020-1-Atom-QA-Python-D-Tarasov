import pymysql

import sqlalchemy
from sqlalchemy.orm import sessionmaker

class MysqlOrmConnection:

    def __init__(self, user, password, db_name=None, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.connection = self.get_connection()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def get_connection(self):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                db=self.db_name if self.db_name is not None else ''),
            encoding='utf8'
        )

        return engine.connect()

    def reinit_db(self, db_name):
        self.db_name = db_name

        self.connection.execute(f'DROP DATABASE if exists {self.db_name}')
        self.connection.execute(f'CREATE DATABASE {self.db_name}')

        # по-хорошему, кажется, можно выставить базу прямо в рантайме для коннекта, но
        # решил, что для этой задачи оно того не стоит и прооще переоткрыть коннект
        self.connection.close()

        self.connection = self.get_connection()

        return

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res

    def __del__(self):
        if self.connection:
            self.connection.close()
        return
