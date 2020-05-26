FROM python:3.8

RUN mkdir /tests && mkdir /allure-results
COPY requirements.txt /tests

WORKDIR /tests

RUN pip3 install -r requirements.txt

COPY pytest.ini tests/
COPY vkapi /tests/vkapi
COPY model /tests/model
COPY myapp /tests/myapp

COPY tests /tests/tests

ENTRYPOINT PYTHONPATH=. python -m pytest -v -s --alluredir=/allure-results
