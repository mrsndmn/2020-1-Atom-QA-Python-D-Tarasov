
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv
load_dotenv()


Base = declarative_base()

class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(16))
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(Integer)
    active = Column(Integer)
    start_active_time = Column(Date)

    def __repr__(self):
        return f"<User(" \
                f"id='{self.id}'" \
                f"username='{self.username}'" \
                f"password='{self.password}'" \
                f"email='{self.email}'" \
                f"access='{self.access}'" \
                f"active='{self.active}'" \
                f"start_active_time='{self.start_active_time}'" \
               f")>"

class MysqlOrmConnection:

    def __init__(self):
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.db_name = os.getenv('MYSQL_DB')

        self.host = os.getenv('MYSQL_HOST', '127.0.0.1')
        self.port = os.getenv('MYSQL_PORT', 3306)
        self.connection = self.get_connection()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def get_connection(self):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=self.user,
                                                                          password=self.password,
                                                                          host=self.host,
                                                                          port=self.port,
                                                                          db=self.db_name),
            encoding='utf8'
        )

        return engine.connect()

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res.getchall()
