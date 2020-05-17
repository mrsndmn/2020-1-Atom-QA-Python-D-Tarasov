FROM python:3.8

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app
RUN pip install -r requirements.txt

COPY vkapi.py app/

EXPOSE 8000

ENTRYPOINT [ "python", 'vkapi.py' ]