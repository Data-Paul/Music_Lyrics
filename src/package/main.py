"""
Main module for the music data collection application.
This module handles user input, API requests, and data storage.
"""

import os
import sys
import logging
from typing import Optional
from .api_logger import MusicBrainzAPI
from .save_data import DatabaseManager

# Logging-Konfiguration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_artist_name() -> Optional[str]:
    """
    Get artist name from environment variable, stdin, or user input.
    
    Returns:
        Optional[str]: Artist name if found, None otherwise
    """
    # Prüfe zuerst die Umgebungsvariable
    artist_name = os.environ.get('ARTIST_NAME')
    if artist_name:
        logger.info(f"Using artist name from environment variable: {artist_name}")
        return artist_name
    
    # Prüfe, ob stdin nicht leer ist (für nicht-interaktive Verwendung)
    if not sys.stdin.isatty():
        artist_name = sys.stdin.read().strip()
        if artist_name:
            logger.info(f"Using artist name from stdin: {artist_name}")
            return artist_name
    
    # Interaktive Eingabeaufforderung
    try:
        artist_name = input("Please enter an artist name: ").strip()
        if artist_name:
            logger.info(f"Using artist name from user input: {artist_name}")
            return artist_name
        else:
            logger.error("No artist name provided")
            return None
    except EOFError:
        logger.error("No input provided")
        return None

def main():
    """
    Main function to collect and store music data.
    """
    try:
        # Hole den Künstlernamen
        artist_name = get_artist_name()
        if not artist_name:
            logger.error("No artist name provided. Exiting.")
            return
        
        # Initialisiere API und Datenbankmanager
        api = MusicBrainzAPI()
        db_manager = DatabaseManager()
        
        # Hole Künstlerinformationen
        artist_data = api.get_artists_by_genre(artist_name)
        if not artist_data or 'artists' not in artist_data or not artist_data['artists']:
            logger.error(f"No artist found with name: {artist_name}")
            return
        
        # Hole Genre-Informationen
        genres = api.get_genres()
        if not genres or 'genres' not in genres:
            logger.error("No genres found")
            return
        
        # Verarbeite und speichere die Daten
        success = db_manager.process_artist_data(artist_data['artists'][0], genres['genres'])
        if success:
            logger.info(f"Successfully processed data for artist: {artist_name}")
        else:
            logger.error(f"Failed to process data for artist: {artist_name}")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    main()