FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]