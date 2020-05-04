import os
from dotenv import load_dotenv
from mysql_client import MysqlOrmConnection
from models.nginxlogs import NginxLog, Base

load_dotenv()

mysqlclient = MysqlOrmConnection(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PASSWORD"), )

mysqlclient.reinit_db(os.getenv("MYSQL_DB"))

Base.metadata.tables['nginxlogs'].create(mysqlclient.connection.engine)