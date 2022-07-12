FROM python:3.9-slim-bullseye

# Install curl
RUN apt-get update -y && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./gunicorn_conf.py /
COPY ./app /app

RUN poetry install --no-root --no-dev

ENV PORT 8000
EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "app.main:app"]
