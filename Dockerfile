# Pokemon Draft League Bot — Multi-stage Dockerfile
# Works on Windows/macOS/Linux via Docker Desktop
# Stage selection: docker build --target bot or --target api

FROM python:3.11-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY data/ ./data/
COPY scripts/ ./scripts/
RUN mkdir -p logs

FROM base AS bot
CMD ["python", "-m", "src.bot.main"]

FROM base AS api
EXPOSE 8000
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
