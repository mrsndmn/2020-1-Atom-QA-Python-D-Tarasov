FROM local/vkapi

RUN pip allure-pytest

COPY tests /app/tests/

ENTRYPOINT [ "python", "-m", "pytest", "-v", "--alluredir=/allure-results" ]
