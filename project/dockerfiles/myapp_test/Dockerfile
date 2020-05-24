FROM python:3.8

RUN mkdir /tests && mkdir /allure-results
COPY requirements.txt /tests

WORKDIR /tests

RUN pip3 install -r requirements.txt

COPY vkapi /tests/vkapi
COPY tests /tests/tests
COPY model /tests/model
COPY myapp /tests/myapp

ENTRYPOINT PYTHONPATH=vkapi:. python -m pytest -s --alluredir=/allure-results
