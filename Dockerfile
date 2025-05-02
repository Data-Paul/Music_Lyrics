# Basis-Image mit Python 3.9 (schlanke Version)
FROM python:3.9-slim

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update \
    # libpq-dev wird für PostgreSQL-Client-Bibliotheken benötigt
    && apt-get -y install libpq-dev gcc \
    # pip auf die neueste Version aktualisieren
    && pip install --upgrade pip \
    # PostgreSQL-Adapter für Python installieren
    && pip install psycopg2-binary

# Paketverzeichnis erstellen
RUN mkdir -p /app/package

# Anwendungscode in den Container kopieren
COPY src/package/*.py /app/package/
COPY src/package/database /app/package/database
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Umgebungsvariablen setzen
ENV PYTHONPATH=/app
# Standard-Datenbankverbindungs-URL
ENV DATABASE_URL=postgresql://postgres:postgres@db:8880/music_db

# Container am Laufen halten (für Entwicklung)
CMD ["tail", "-f", "/dev/null"] 