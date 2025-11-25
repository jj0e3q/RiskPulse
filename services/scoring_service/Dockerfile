FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY services/scoring_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared ./shared
COPY services/scoring_service/app ./app
COPY services/scoring_service/alembic.ini .
COPY services/scoring_service/alembic ./alembic

ENV DATABASE_URL=postgresql+psycopg2://riskpulse:riskpulse@postgres:5432/riskpulse

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]