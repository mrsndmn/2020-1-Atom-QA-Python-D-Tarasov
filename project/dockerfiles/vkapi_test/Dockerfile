FROM vkapi

RUN pip install allure-pytest

COPY tests /app/tests/

ENTRYPOINT [ "python", "-m", "pytest", "-v", "--alluredir=/allure-results" ]
