import os
import argparse

from bash_scripting.nginxlogline import LogLine

parser = argparse.ArgumentParser(description='nginx logs parser')

# todo find all logs in directory
parser.add_argument('--dir', metavar='d', nargs='+', default=".",
                    help='dir which contains access.log file')
parser.add_argument('--out', metavar='o', nargs='+', default="pytohn-nginx-log-parser.out",
                    help='file for output')

args = parser.parse_args()

access_log = os.path.join(args.dir, "access.log")

logfile = open(access_log, "r")

result = {
    "total_lines": 0,
    "queries_by_type": {
        # Количество запросов по типу, например: GET - 20, POST - 10 и т.д. (0,5 балла)
    },
    # Топ 10 самых больших по размеру запросов, должно быть видно url, код, число запросов (1 балл)
    "top_by_size": [],
    # Топ 10 запросов по количеству, которые завершились клиентской ошибкой, должно быть видно url, статус код, ip адрес (1 балл)
    "top_client_error": [],
    # Топ 10 запросов клиентских ошибок по размеру запроса, должно быть видно url, статус код, ip адрес (1 балл)
    "top_by_size_client_error": [],
}

all_parsed = []

for line in logfile:
    parsed_line = LogLine(line)

    result["total_lines"] += 1

    if parsed_line.method not in result["queries_by_type"]:
        result["queries_by_type"][parsed_line.method] = 0
    result["queries_by_type"][parsed_line.method] += 1

    all_parsed.append(parsed_line)

by_size = sorted(all_parsed, key=lambda l: l.size, reverse=True)

result["top_by_size"] = by_size[:10]

by_size_client_err = [l for l in by_size if l.status >= 400 and l.status < 500]
result["top_by_size_client_error"] = by_size_client_err[:10]

# учитываем только уникальные запросы
req_with_error_set = dict()
for l in by_size_client_err:
    key = " ".join((l.ip, l.method, l.path, str(l.status)))
    if key not in req_with_error_set:
        req_with_error_set[key] = 0
    req_with_error_set[key] += 1


count_client_err = sorted(req_with_error_set.keys(), key=lambda k: req_with_error_set[k], reverse=True)
result["top_client_error"] = count_client_err[:10]

out = open(args.out, 'w')
print(result, file=out)

