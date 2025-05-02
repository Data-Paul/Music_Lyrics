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

# Anwendungscode in den Container kopieren
COPY src /app/src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Umgebungsvariablen setzen
ENV PYTHONPATH=/app/src
# Standard-Datenbankverbindungs-URL
ENV DATABASE_URL=postgresql://postgres:postgres@db:8880/music_db

# Run the Python application
CMD ["python", "-m", "package.main"]