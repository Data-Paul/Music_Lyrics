# MusicLyricsAnalyzer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A comprehensive tool for analyzing and comparing musical artists through their lyrics and metadata.

## Overview

The project combines structured metadata from the MusicBrainz API with unstructured text data from AZLyrics.com webscraping. Through a combination of data integration, NLP analysis, and machine learning approaches, artists are made comparable and themes in lyrics are explored.

### Key Features
- Artist metadata collection from MusicBrainz API
- Lyrics scraping from AZLyrics.com
- Thematic analysis of song lyrics
- Artist comparison based on lyrical content
- PostgreSQL database integration
- Docker containerization
- Power BI visualization support

## Technologies and Data Sources

### MusicBrainz API Integration
- Artist information (name, ID, genre)
- Song information (title, ID, associated artist)
- Genre information

### AZLyrics.com (Webscraping)
- Complete song lyrics based on artist and song names

### Data Collection Details

| Source | Data | Purpose |
|--------|------|---------|
| MusicBrainz API | Artist name, Artist ID, Genre | Genre classification of artists |
| MusicBrainz API | Song title, Song ID, Artist ID | Foundation for webscraping and database integration |
| AZLyrics Webscraping | Song title, Lyrics | Content analysis of song lyrics |

Data is stored in a relational database (PostgreSQL) in 3rd normal form to avoid redundancy and facilitate analysis.

## AI and Analysis Features

### Thematic Analysis
- NLP techniques: tokenization, stopword removal, TF-IDF vectorization
- Topic Modeling (e.g., Latent Dirichlet Allocation, LDA) to identify common themes
- Semantic pattern recognition in lyrics

### Artist Comparison
- Vector space representations (e.g., based on TF-IDF matrices)
- Similarity calculations between artists using Cosine Similarity
- Artist clustering based on lyrical theme proximity (e.g., K-Means)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- PostgreSQL (optional, included in Docker setup)
- Power BI (for visualization)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MusicLyricsAnalyzer.git
   cd MusicLyricsAnalyzer
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Running the Application

#### Local Development
```bash
python src/package/main.py
```

#### Docker
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Database Setup

The project uses PostgreSQL. The database is automatically set up when running with Docker Compose.

- Host: localhost
- Port: 8880
- Database: mydb
- User: postgres
- Password: postgres

## 🎵 API Integration

### MusicBrainz API Setup
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

## Testing

Run the test suite:
```bash
pytest src/package/test/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- MusicBrainz for providing the API
- AZLyrics for song lyrics
- All contributors who have helped shape this project

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Implement Genius API integration for additional lyrics
- [ ] Add sentiment analysis for lyrics
- [ ] Develop genre prediction model
- [ ] Create interactive visualization dashboard
- [ ] Add multilingual support