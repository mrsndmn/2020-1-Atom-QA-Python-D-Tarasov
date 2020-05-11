import os
from dotenv import load_dotenv
from db.mysql_client import MysqlOrmConnection
import argparse

from bash_scripting.nginxlogline import LogLine
from db.models.nginxlogs import NginxLog

load_dotenv()

mysqlclient = MysqlOrmConnection(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PASSWORD"), db_name=os.getenv("MYSQL_DB"))

parser = argparse.ArgumentParser(description='nginx logs parser')

# todo find all logs in directory
parser.add_argument('--dir', metavar='d', nargs='+', default=".",
                    help='dir which contains access.log file')

args = parser.parse_args()

access_log = os.path.join(args.dir, "access.log")

logfile = open(access_log, "r")


for line in logfile:
    parsed_line = LogLine(line)
    dbLog = NginxLog(
        ip = parsed_line.ip,
        method = parsed_line.method,
        path = parsed_line.path,
        status = parsed_line.status,
        size = parsed_line.size,
    )

    mysqlclient.session.add(dbLog)

mysqlclient.session.commit()

res = mysqlclient.session.execute('select count(*) from nginxlogs;')

print('Общее количество запросов: ')
for r in res:
    print(r[0])

print("\n\nКоличество запросов по типу:")
res = mysqlclient.session.execute('select method, count(*) from nginxlogs group by method;')
for r in res:
    print(r)

print("\n\nТоп 10 самых больших по размеру запросов: ")
res = mysqlclient.session.execute('select method, path, status, count(*) from nginxlogs group by method, path, status, size order by size desc limit 10;')
for r in res:
    print(r)

print("\n\nТоп 10 запросов по количеству, которые завершились клиентской ошибкой:")
res = mysqlclient.session.execute('select method, path, status, ip, count(*) as count from nginxlogs where status >= 400 and status < 500 group by method, path, status, ip order by count desc limit 10;')
for r in res:
    print(r)

print("\n\nТоп 10 запросов клиентских ошибок по размеру запроса:")
res = mysqlclient.session.execute('select method, path, status, ip as count from nginxlogs where status >= 400 and status < 500 group by method, path, status, ip, size order by size desc limit 10;')
for r in res:
    print(r)

