FROM node:20 AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build


FROM python:3.12-slim AS backend
WORKDIR /code/backend
RUN pip install uv
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --no-dev
COPY backend/ ./
COPY --from=frontend-builder /app/build ./frontend/build
ENV PYTHONUNBUFFERED=1