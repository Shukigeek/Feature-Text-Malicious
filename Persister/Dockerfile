FROM python:3.10-slim

WORKDIR /app

COPY Persister/requirements.txt .


RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt


COPY . .
COPY utiles /app/utiles

CMD ["python", "main.py"]
