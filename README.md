# Music Data Collection System

A Python application that collects and stores music data from MusicBrainz API and azlyrics.com.

## Features

- Fetches artist information from MusicBrainz API
- Scrapes song lyrics from azlyrics.com
- Stores data in PostgreSQL database
- Supports multiple input methods (environment variable, stdin, interactive)
- Comprehensive logging and error handling

## Requirements

- Python 3.8+
- PostgreSQL
- Docker and Docker Compose (for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
docker-compose up -d db
```

## Usage

### Running the Application

The application can be run in several ways, with different methods to provide the artist name:

#### 1. Docker Compose (Recommended)

**Method A: Interactive Mode (Manual Input)**
```bash
# Start the database container
docker-compose up -d db

# Check running containers
docker ps  # Should only show music_db container

# Run the application container
docker-compose run --rm app

# When prompted, enter the artist name
```

**Method B: Environment Variable**
```bash
# Start the database container
docker-compose up -d db

# Run with environment variable
ARTIST_NAME="Artist Name" docker-compose run --rm app
```

**Method C: Standard Input (Pipe)**
```bash
# Start the database container
docker-compose up -d db

# Pipe artist name to the application
echo "Artist Name" | docker-compose run --rm app
```

#### 2. Direct Docker Execution

If the application container is already running:
```bash
# Check if music_app container is running
docker ps  # Look for music_app container

# If running, execute bash in the container
docker exec -it music_app bash

# Then run the application
python -m package.main
```

#### 3. Local Development

**Method A: Interactive Mode**
```bash
# Start the database
docker-compose up -d db

# Run the application
python -m src.package.main
```

**Method B: Environment Variable**
```bash
# Set environment variable
export ARTIST_NAME="Artist Name"

# Run the application
python -m src.package.main
```

**Method C: Standard Input**
```bash
# Pipe artist name to the application
echo "Artist Name" | python -m src.package.main
```

### Expected Behavior

After providing the artist name through any of the above methods:
1. The application will connect to the MusicBrainz API
2. Fetch artist information and related data
3. Scrape lyrics from azlyrics.com
4. Store all collected data in the PostgreSQL database
5. Log the progress and any errors to stdout

### Troubleshooting

If you encounter issues:
1. Ensure the database container is running (`docker ps` should show `music_db`)
2. Check container logs: `docker-compose logs`
3. Verify database connection: `docker exec -it music_db psql -U postgres -d music_db`
4. Check application logs in the container: `docker exec -it music_app cat /app/logs/app.log`

## Project Structure

```
src/
├── package/
│   ├── __init__.py
│   ├── main.py           # Main application entry point
│   ├── api_logger.py     # MusicBrainz API client
│   ├── web_logger.py     # Lyrics scraping functionality
│   └── save_data.py      # Database operations
├── requirements.txt      # Python dependencies
├── Dockerfile           # Application container definition
└── docker-compose.yml   # Multi-container setup
```

## Database Schema

The application uses the following tables:

- `Artist`: Stores artist information
- `Genre`: Stores music genres
- `Song`: Stores song information
- `Lyrics`: Stores song lyrics
- `SongGenre`: Links songs to genres

## Error Handling

The application includes comprehensive error handling for:
- API request failures
- Database connection issues
- Web scraping errors
- Input validation
- Data processing errors

## Logging

Logging is configured to output to stdout with the following format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Log levels:
- DEBUG: Detailed information for debugging
- INFO: General operational information
- ERROR: Error conditions that need attention

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


##Future AI Integration: Concept and Use Cases

While the current application focuses on collecting and storing music-related data, future versions are designed to enable powerful AI-driven analysis of lyrical content. The structured storage of artist, song, genre and lyrics data lays the foundation for multiple machine learning and NLP applications.
### 🎯 Planned AI Use Cases
1. Thematic Classification of Lyrics

Using NLP models such as TF-IDF, topic modeling (LDA), or transformer-based embeddings (e.g., BERT), lyrics can be automatically classified into thematic categories such as love, rebellion, social critique, personal struggle, etc.

    Potential outcome: Tag each song with dominant themes for further filtering, trend analysis or recommendation.

2. Artist Similarity Based on Lyrics

By embedding lyrics using sentence transformers or averaging word embeddings, each artist can be represented in a multidimensional semantic space. Cosine similarity can then be used to identify lyrical similarity between artists.

    Example: Visualize clusters of artists based on shared language patterns, recurring motifs, or sentiment profiles.

3. Trend Analysis Over Time

Using the last_updated timestamps or song release dates (extendable via MusicBrainz), lyrical themes can be analyzed over time.

    Example: How did the frequency of words like "war", "hope", or "dream" evolve across decades or musical genres?

4. Clustering and Exploratory Search

Unsupervised clustering (e.g., K-Means or HDBSCAN) on lyric embeddings can allow for discovery of hidden patterns and novel groupings of songs or artists based on language use.
5. Custom Search & Recommendation Engine

A lyric-based search and recommendation system could suggest songs with similar themes, moods, or writing styles — useful for music discovery or playlist generation.