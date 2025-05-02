"""
Modul zum Speichern von Daten aus API und Web-Scraping in der Datenbank.
Dieses Modul stellt Funktionen zum Speichern und Verwalten von Musikdaten in PostgreSQL bereit.
"""

import psycopg2
from psycopg2.extras import Json
import logging
from typing import Dict, List, Optional, Tuple
from src.package.api_logger import MusicBrainzAPI
from src.package.web_logger import scrape_lyrics
import sys
import json

# Logging-Konfiguration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, dbname: str = "music_db", user: str = "postgres", 
                 password: str = "postgres", host: str = "localhost", port: str = "8880"):
        """
        Initialize database connection.
        
        Args:
            dbname (str): Database name
            user (str): Database user
            password (str): Database password
            host (str): Database host
            port (str): Database port
        """
        # Verbindungsparameter für die Datenbank
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "client_encoding": "UTF8"  # UTF8-Kodierung für die Verbindung
        }
        self.api = MusicBrainzAPI()
        logger.info(f"DatabaseManager initialisiert mit Parametern: {self.conn_params}")

    def connect(self):
        """Establish database connection."""
        try:
            logger.info("Versuche Verbindung zur Datenbank herzustellen...")

            # UTF-8-Test für alle Verbindungsparameter
            for key, value in self.conn_params.items():
                try:
                    str(value).encode('utf-8')
                    logger.debug(f"Verbindungsparameter '{key}' ist UTF-8-kompatibel")
                except UnicodeDecodeError as ue:
                    logger.error(f"❌ Problem im Verbindungsparameter '{key}': {ue}")
                    raise

            # Datenbankverbindung aufbauen
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
            
            # Testabfrage zur Überprüfung der Verbindung
            self.cur.execute("SELECT 1;")
            self.cur.fetchone()
            
            logger.info("✅ Datenbankverbindung erfolgreich hergestellt")
            
        except psycopg2.Error as e:
            logger.error(f"❌ PostgreSQL-Fehler: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unerwarteter Fehler bei der Datenbankverbindung: {e}")
            raise

    def close(self):
        """Close database connection."""
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()
            logger.info("Datenbankverbindung geschlossen")

    def save_artist(self, artist_data: Dict) -> Optional[int]:
        """
        Speichert Künstlerdaten in der Datenbank.
        
        Args:
            artist_data (Dict): Künstlerinformationen von der MusicBrainz API
            
        Returns:
            Optional[int]: Künstler-ID bei Erfolg, None sonst
        """
        try:
            # UTF-8-Kompatibilität der Künstlerdaten prüfen
            try:
                json.dumps(artist_data)
            except UnicodeDecodeError as ue:
                logger.error(f"❌ UnicodeDecodeError in artist_data: {ue}")
                raise
            
            # Künstler in die Datenbank einfügen
            self.cur.execute("""
                INSERT INTO Artist (artist_name, artist_url, additional_info)
                VALUES (%s, %s, %s)
                RETURNING artist_id
            """, (
                artist_data.get('name'),
                f"https://musicbrainz.org/artist/{artist_data.get('id')}",
                Json(artist_data)  # JSON-Objekt für zusätzliche Informationen
            ))
            artist_id = self.cur.fetchone()[0]
            self.conn.commit()
            logger.info(f"Künstler gespeichert: {artist_data.get('name')}")
            return artist_id
        except Exception as e:
            logger.error(f"Fehler beim Speichern des Künstlers: {e}")
            self.conn.rollback()
            return None

    def save_genre(self, genre_name: str) -> Optional[int]:
        """
        Save genre to database.
        
        Args:
            genre_name (str): Name of the genre
            
        Returns:
            Optional[int]: Genre ID if successful, None otherwise
        """
        try:
            self.cur.execute("""
                INSERT INTO Genre (genre_name)
                VALUES (%s)
                ON CONFLICT (genre_name) DO UPDATE
                SET genre_name = EXCLUDED.genre_name
                RETURNING genre_id
            """, (genre_name,))
            genre_id = self.cur.fetchone()[0]
            self.conn.commit()
            logger.info(f"Saved genre: {genre_name}")
            return genre_id
        except Exception as e:
            logger.error(f"Error saving genre: {e}")
            self.conn.rollback()
            return None

    def save_song(self, song_data: Dict, artist_id: int) -> Optional[int]:
        """
        Save song data to database.
        
        Args:
            song_data (Dict): Song information from MusicBrainz API
            artist_id (int): ID of the associated artist
            
        Returns:
            Optional[int]: Song ID if successful, None otherwise
        """
        try:
            self.cur.execute("""
                INSERT INTO Song (artist_id, song_name, song_url, additional_info)
                VALUES (%s, %s, %s, %s)
                RETURNING song_id
            """, (
                artist_id,
                song_data.get('title'),
                f"https://musicbrainz.org/recording/{song_data.get('id')}",
                Json(song_data)
            ))
            song_id = self.cur.fetchone()[0]
            self.conn.commit()
            logger.info(f"Saved song: {song_data.get('title')}")
            return song_id
        except Exception as e:
            logger.error(f"Error saving song: {e}")
            self.conn.rollback()
            return None

    def save_lyrics(self, song_id: int, artist_name: str, song_name: str) -> Optional[int]:
        """
        Save lyrics to database.
        
        Args:
            song_id (int): ID of the associated song
            artist_name (str): Name of the artist
            song_name (str): Name of the song
            
        Returns:
            Optional[int]: Lyrics ID if successful, None otherwise
        """
        try:
            lyrics = scrape_lyrics(artist_name, song_name)
            self.cur.execute("""
                INSERT INTO Lyrics (song_id, lyrics_text)
                VALUES (%s, %s)
                RETURNING lyrics_id
            """, (song_id, lyrics))
            lyrics_id = self.cur.fetchone()[0]
            self.conn.commit()
            logger.info(f"Saved lyrics for song ID: {song_id}")
            return lyrics_id
        except Exception as e:
            logger.error(f"Error saving lyrics: {e}")
            self.conn.rollback()
            return None

    def link_song_genre(self, song_id: int, genre_id: int) -> bool:
        """
        Link a song to a genre.
        
        Args:
            song_id (int): ID of the song
            genre_id (int): ID of the genre
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cur.execute("""
                INSERT INTO SongGenre (song_id, genre_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (song_id, genre_id))
            self.conn.commit()
            logger.info(f"Linked song {song_id} to genre {genre_id}")
            return True
        except Exception as e:
            logger.error(f"Error linking song to genre: {e}")
            self.conn.rollback()
            return False

    def process_artist_data(self, artist_data: Dict, genres: List[str]) -> bool:
        """
        Process and save complete artist data including songs and lyrics.
        
        Args:
            artist_data (Dict): Artist information from MusicBrainz API
            genres (List[str]): List of genres associated with the artist
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.connect()
            
            # Save artist
            artist_id = self.save_artist(artist_data)
            if not artist_id:
                return False
            
            # Save genres and create links
            for genre_name in genres:
                genre_id = self.save_genre(genre_name)
                if genre_id:
                    self.link_song_genre(artist_id, genre_id)
            
            # Get and save songs
            songs = self.api.get_artist_recordings(artist_data.get('id'))
            if songs and 'recordings' in songs:
                for song in songs['recordings']:
                    song_id = self.save_song(song, artist_id)
                    if song_id:
                        self.save_lyrics(song_id, artist_data.get('name'), song.get('title'))
            
            return True
        except Exception as e:
            logger.error(f"Error processing artist data: {e}")
            return False
        finally:
            self.close()

# Example usage
if __name__ == "__main__":
    # Initialize database manager with Docker container settings
    db_manager = DatabaseManager(
        dbname="music_db",
        user="postgres",
        password="postgres",
        host="db", # service name from docker-compose.yml
        port="8880"
    )
    
    # Test with a simple artist
    test_artist = {
        "id": "123",
        "name": "SimpleArtist",
        "type": "Person",
        "country": "US"
    }
    test_genres = ["Rock", "Alternative"]
    
    # Process and save the data
    logger.info("Starting test data processing...")
    success = db_manager.process_artist_data(test_artist, test_genres)
    logger.info(f"Data processing {'successful' if success else 'failed'}")