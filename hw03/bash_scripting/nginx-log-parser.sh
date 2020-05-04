#!/usr/bin/env bash

set +ex

PATH_TO_ACCESS_LOG_DIR="."
OUTPUT_FILE="${0}.out"

while [ -n "$1" ]
do
case "$1" in
-h) echo "Help message:\n\t-d path/to/dir/with/log ";;
-d) PATH_TO_ACCESS_LOG_DIR="$2"
echo "Found the -d option, with path to access log: ${PATH_TO_ACCESS_LOG_DIR}"
shift ;;
-o) OUTPUT_FILE="$2"
echo "Found the -o option, output file: ${OUTPUT_FILE}"
shift ;;
*) echo "$1 is not an option" ;;
esac
shift
done

LOGFILE="${PATH_TO_ACCESS_LOG_DIR}/access.log"

echo "Parsing ${LOGFILE}" > "$OUTPUT_FILE"
date >> "$OUTPUT_FILE"
echo -e "=================\n" >> "$OUTPUT_FILE"

TOTAL_LOGS_QUERIES=$(wc -l "${LOGFILE}")
echo -e "TOTAL_LOGS_QUERIES:\n${TOTAL_LOGS_QUERIES}\n" >> "$OUTPUT_FILE"

QUERIES_COUN_BY_REQUEST_METHOD=$(perl -lne '/\]\s"(\S+)/; print $1' "$LOGFILE" | sort | uniq -c)
echo -e "QUERIES_COUN_BY_REQUEST_METHOD:\n${QUERIES_COUN_BY_REQUEST_METHOD}\n"  >> "$OUTPUT_FILE"

TOP_BIG_QUERIES=$(perl -lnE ' /\]\s"(\S+)\s(\S+) HTTP\/1\.1"\s(\d{3})\s(\d+)/; print join("\t", $1, $2, $3, $4) ' "$LOGFILE" | sort -k4 -nr | uniq | head -10)
echo -e "TOP_BIG_QUERIES: \nmethod\tpath\tcode\tsize\n${TOP_BIG_QUERIES}\n"  >> "$OUTPUT_FILE"

TOP_CLIENT_ERROR_QUERIES=$(perl -lnE ' /(\S+).+\]\s"(\S+)\s(\S+) HTTP\/1\.1"\s(4\d{2})/ or next; print join("\t", $1, $2, $3, $4) ' "$LOGFILE" | sort | uniq --skip-fields=1 -c | sort -rnk1 | head -n10)
echo -e "TOP_CLIENT_ERROR_QUERIES: \ncount\tip\tmethod\tpath\tcode\n${TOP_CLIENT_ERROR_QUERIES}\n"  >> "$OUTPUT_FILE"

TOP_CLIENT_ERROR_QUERIES_BY_SIZE=$(perl -lnE ' /(\S+).+\]\s"(\S+)\s(\S+) HTTP\/1\.1"\s(4\d{2})\s(\d+)/ or next; print join("\t", $1, $2, $3, $4, $5) ' "$LOGFILE" | sort -rk5 | uniq --skip-fields=1 | head -n10 | cut -f 1-4)
echo -e "TOP_CLIENT_ERROR_QUERIES_BY_SIZE: ip\tmethod\tpath\tcode\n${TOP_CLIENT_ERROR_QUERIES_BY_SIZE}\n"  >> "$OUTPUT_FILE"



