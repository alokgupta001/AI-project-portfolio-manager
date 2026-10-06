ARG PYTHON_IMAGE=python:3.12-slim-bookworm@sha256:54c85f3c47607a77f32adec749d3c81d1348bf25833671f512b26a9b6d778cb3
FROM ${PYTHON_IMAGE}
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 UV_COMPILE_BYTECODE=1
WORKDIR /app
RUN pip install --no-cache-dir uv==0.11.15
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-managed-python
COPY services ./services
COPY scripts ./scripts
COPY tests ./tests
COPY alembic.ini ./
RUN useradd --uid 10001 --create-home ppm && mkdir -p /var/ppm/objects && chown -R ppm:ppm /var/ppm && chown ppm:ppm /app
USER ppm
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app/services/api:/app/services/worker"
CMD ["uvicorn", "ppm_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
