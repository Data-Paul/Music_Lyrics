# Project Name

## Project Structure
```
project-root/
│
├── src/
│   └── package/               # Main package with modules & logic
│       ├── main.py            # Application entry point
│       ├── playground.ipynb   # Jupyter notebook for analysis & tests
│       ├── api_logger.py      # MusicBrainz API integration
│       └── test/              # Unit tests for modules
│
├── data/                      # Raw data, cached JSONs, or scrape results
├── database/                  # DDL scripts, database dumps, init.sql for Docker DB
├── results/                   # Visualizations, evaluations, topic model results
│
├── Dockerfile                 # Container for Python application
├── docker-compose.yml         # Orchestrates application + database
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## MusicBrainz API Integration

The project uses the MusicBrainz API to collect music metadata. Here's how to use the API integration:

### Setup
1. Set your application's User-Agent in `api_logger.py`:
```python
HEADERS = {
    "User-Agent": "YourApp/1.0.0 ( your-email@example.com )",
    "Accept": "application/json"
}
```

### Data Collection Flow
1. **Genres**: Get all available genres
```python
api = MusicBrainzAPI()
genres = api.get_genres()
```

2. **Artists by Genre**: Get artists for each genre
```python
artists = api.get_artists_by_genre("rock")
```

3. **Release Groups**: Get release groups for each artist
```python
release_groups = api.get_release_groups(artist_id)
```

4. **Recordings**: Get recordings for each release
```python
recordings = api.get_recordings(release_id)
```

### Rate Limiting
- The API has a rate limit of 1 request per second
- The implementation includes automatic retry with delay
- Use pagination (limit/offset) for large datasets

### Data Structure
The API returns JSON data with the following main entities:
- Genres
- Artists
- Release Groups
- Recordings

Note: Lyrics are not available through the MusicBrainz API. Consider integrating with additional APIs (e.g., Genius, Musixmatch) for lyrics data.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

- Run the application:
  ```bash
  python src/package/main.py
  ```

- Run tests:
  ```bash
  pytest src/package/test/
  ```

## Docker

Build and run the application with Docker:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Database

The project uses PostgreSQL. The database is automatically set up when running with Docker Compose.

- Host: localhost
- Port: 5432
- Database: mydb
- User: postgres
- Password: postgres

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request