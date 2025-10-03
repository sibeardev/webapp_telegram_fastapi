FROM python:3.12-slim AS runtime-python

WORKDIR /code
RUN pip install uv
COPY pyproject.toml uv.lock /code/
RUN uv sync --no-dev
COPY . .
ENV PYTHONUNBUFFERED=1