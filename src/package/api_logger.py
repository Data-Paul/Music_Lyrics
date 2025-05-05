"""
MusicBrainz API Client Module

This module provides a client interface for interacting with the MusicBrainz API.
It handles all API requests, including rate limiting, error handling, and response processing.
The module supports fetching:
- Artist information by genre
- Artist recordings
- Genre information
- Detailed artist data

The client implements proper rate limiting and retry mechanisms to ensure reliable
API communication while respecting MusicBrainz's usage policies.
"""

import requests
import time
import logging
from typing import Dict, List, Optional

# Konfiguriere das Logging-System
logger = logging.getLogger(__name__)

class MusicBrainzAPI:
    """
    Client for interacting with the MusicBrainz API.
    
    This class provides methods to fetch various types of music-related data
    from the MusicBrainz API. It handles authentication, rate limiting, and
    error handling automatically.
    
    Attributes:
        BASE_URL (str): Base URL for all API requests
        HEADERS (dict): Default headers for API requests
    """
    
    # Basis-URL für alle API-Anfragen
    BASE_URL = "https://musicbrainz.org/ws/2/"
    # Header-Informationen für die API-Anfragen
    HEADERS = {
        "User-Agent": "MusicBrainz API Wrapper/0.0.1 ( paulharasek@yahoo.de )",
        "Accept": "application/json"
    }

    def __init__(self):
        """
        Initialize the MusicBrainz API client.
        
        Creates a session for better performance with multiple requests and
        sets up the default headers for API communication.
        """
        # Erstellt eine Session für bessere Performance bei mehreren Anfragen
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Make a request to the MusicBrainz API with retry logic.
        
        Args:
            endpoint (str): API endpoint to call
            params (Dict): Query parameters for the request
            
        Returns:
            Optional[Dict]: JSON response from the API if successful, None otherwise
            
        Note:
            Implements retry logic for rate limiting (503 responses) and
            handles other common error cases.
        """
        max_retries = 3
        retry_delay = 1  # Sekunden
        
        for attempt in range(max_retries):
            try:
                # Führe die API-Anfrage aus
                response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
                
                # Prüfe auf Rate-Limit
                if response.status_code == 503:
                    if attempt < max_retries - 1:
                        logger.warning("Rate limit reached, retrying...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error("Max retries reached for rate limit")
                        return None
                
                # Prüfe auf andere Fehler
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed: {e}")
                return None

    def get_artists_by_genre(self, genre: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieve artists by genre with basic information needed for database storage.
        
        Args:
            genre (str): Genre to search for
            limit (int): Maximum number of results to return
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of artists with ID, name, and genre information
        """
        logger.debug(f"Fetching artists for genre: {genre}")
        return self._make_request("artist", {
            "query": f"genre:{genre}",
            "limit": limit,
            "offset": offset
        })

    def get_artist_recordings(self, artist_id: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieve all recordings by an artist with minimal required information.
        
        Args:
            artist_id (str): MusicBrainz ID of the artist
            limit (int): Maximum number of results to return
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of recordings with ID, title, and artist information
        """
        logger.debug(f"Fetching recordings for artist: {artist_id}")
        return self._make_request("recording", {
            "artist": artist_id,
            "limit": limit,
            "offset": offset
        })

    def get_genres(self, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieve a list of all available genres.
        
        Args:
            limit (int): Maximum number of results to return
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of genres with ID and name
        """
        logger.debug("Fetching all available genres")
        return self._make_request("genre/all", {"limit": limit, "offset": offset}) 