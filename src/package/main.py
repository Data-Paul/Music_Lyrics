"""
Main script for the MusicBrainz data collection system.
This script provides a simple CLI interface to search for artists and save their data.
"""

import logging
from src.package.api_logger import MusicBrainzAPI
from src.package.save_data import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Initialize API client and database manager
    api = MusicBrainzAPI()
    db = DatabaseManager()
    
    try:
        # Get artist name from user
        artist_name = input("Enter artist name to search: ").strip()
        if not artist_name:
            logger.error("Artist name cannot be empty")
            return
            
        # Search for artist
        logger.info(f"Searching for artist: {artist_name}")
        artist_data = api._make_request("artist", {
            "query": artist_name,
            "limit": 1
        })
        
        if not artist_data or 'artists' not in artist_data or not artist_data['artists']:
            logger.error(f"No artist found for: {artist_name}")
            return
            
        # Get the first matching artist
        artist = artist_data['artists'][0]
        logger.info(f"Found artist: {artist['name']} (ID: {artist['id']})")
        
        # Process and save the artist data
        # Note: We're using an empty list for genres since we don't have genre data from the search
        success = db.process_artist_data(artist, [])
        
        if success:
            logger.info("Successfully saved artist data")
        else:
            logger.error("Failed to save artist data")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Clean up
        db.close()

if __name__ == "__main__":
    main()