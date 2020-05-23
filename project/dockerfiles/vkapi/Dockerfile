FROM python:3.8

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app

# todo тесты, теоретически нужно было бы унести в отдельный докерфайл
RUN pip3 install -r requirements.txt

COPY vkapi.py /app/

EXPOSE 8000

ENTRYPOINT [ "/usr/local/bin/python3", "vkapi.py" ]
