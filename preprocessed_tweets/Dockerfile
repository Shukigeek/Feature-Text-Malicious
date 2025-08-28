FROM python:3.10-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt


ENV NLTK_DATA=/usr/local/share/nltk_data


RUN python -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon punkt wordnet stopwords


COPY . .


RUN useradd -m appuser
USER appuser

CMD ["python", "main.py"]

