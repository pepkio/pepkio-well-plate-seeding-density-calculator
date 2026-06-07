FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README_PYPI.md ./
COPY src ./src

RUN pip install --no-cache-dir .

LABEL org.opencontainers.image.source="https://github.com/pepkio/pepkio-well-plate-seeding-density-calculator"

ENTRYPOINT ["pepkio-well-plate-seeding-density-calculator"]
