FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

# Setup config to not create virtualenvs in docker
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi --no-root

COPY . /app

EXPOSE 8000

# Using bash script or inline command to run migrations before uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
