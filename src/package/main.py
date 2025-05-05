"""
Music Data Collection Application - Main Module

This module serves as the main entry point for the music data collection application.
It handles user input processing, coordinates API requests to MusicBrainz, and manages
data storage operations. The module provides functionality to:
- Collect artist names through various input methods (environment variables, stdin, interactive)
- Fetch artist information from MusicBrainz API
- Process and store music data in the database
- Handle errors and provide comprehensive logging
"""

import os
import sys
import logging
from typing import Optional
from .api_logger import MusicBrainzAPI
from .save_data import DatabaseManager

# Konfiguriere das Logging-System
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
    Retrieves the artist name through multiple input methods with fallback options.
    
    The function attempts to get the artist name in the following order:
    1. Environment variable (ARTIST_NAME)
    2. Standard input (stdin)
    3. Interactive user input
    
    Returns:
        Optional[str]: The artist name if successfully retrieved, None if no input is provided
                      and the input stream is closed (EOFError)
    
    Note:
        In interactive mode, the function will continuously prompt for input until
        a non-empty artist name is provided.
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
        while True:
            artist_name = input("Please enter an artist name: ").strip()
            if artist_name:
                logger.info(f"Using artist name from user input: {artist_name}")
                return artist_name
            else:
                logger.warning("No artist name provided. Please try again.")
    except EOFError:
        logger.error("No input provided")
        return None

def main():
    """
    Main function that orchestrates the music data collection process.
    
    This function:
    1. Retrieves the artist name
    2. Initializes the API client and database manager
    3. Fetches artist and genre information
    4. Processes and stores the data
    5. Handles any errors that occur during the process
    
    The function will exit if:
    - No artist name is provided
    - The artist is not found in MusicBrainz
    - No genres are available
    - Any other error occurs during processing
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
        
        # Hole Künstlerinformationen von der MusicBrainz API
        artist_data = api.get_artists_by_genre(artist_name)
        if not artist_data or 'artists' not in artist_data or not artist_data['artists']:
            logger.error(f"No artist found with name: {artist_name}")
            return
        
        # Hole Genre-Informationen von der API
        genres = api.get_genres()
        if not genres or 'genres' not in genres:
            logger.error("No genres found")
            return
        
        # Verarbeite und speichere die Daten in der Datenbank
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