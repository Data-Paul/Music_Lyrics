"""
Module for API data logging and request handling.
This module provides functions to fetch and process MusicBrainz API data.
"""

import requests
import time
from typing import Dict, List, Optional

class MusicBrainzAPI:
    # Basis-URL für alle API-Anfragen
    BASE_URL = "https://musicbrainz.org/ws/2/"
    # Header-Informationen für die API-Anfragen
    HEADERS = {
        "User-Agent": "MusicBrainz API Wrapper/0.0.1 ( paulharasek@yahoo.de )",
        "Accept": "application/json"
    }

    def __init__(self):
        # Erstellt eine Session für bessere Performance bei mehreren Anfragen
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Sends a request to the MusicBrainz API with rate limiting.
        This method is used internally by all other methods.
        
        Args:
            endpoint (str): The API endpoint to call
            params (Optional[Dict]): Optional parameters for the request
            
        Returns:
            Optional[Dict]: JSON response if successful, None otherwise
        """
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            
            # Erfolgreiche Anfrage
            if response.status_code == 200:
                return response.json()
            # Rate-Limit überschritten, warte und versuche es erneut
            elif response.status_code == 503:
                print(f"Rate limit exceeded. Waiting before retry...")
                time.sleep(1)
                return self._make_request(endpoint, params)
            # Andere Fehler
            else:
                print(f"Error: Status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_artists_by_genre(self, genre: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieves artists by genre with basic information needed for database storage.
        
        Args:
            genre (str): Genre to search for
            limit (int): Maximum number of results
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of artists with ID, name, and genre information
        """
        return self._make_request("artist", {
            "query": f"genre:{genre}",
            "limit": limit,
            "offset": offset
        })

    def get_artist_recordings(self, artist_id: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieves all recordings by an artist with minimal required information.
        
        Args:
            artist_id (str): MusicBrainz ID of the artist
            limit (int): Maximum number of results
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of recordings with ID, title, and artist information
        """
        return self._make_request("recording", {
            "artist": artist_id,
            "limit": limit,
            "offset": offset
        })

    def get_genres(self, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """
        Retrieves a list of all available genres.
        
        Args:
            limit (int): Maximum number of results
            offset (int): Starting position for pagination
            
        Returns:
            Optional[List[Dict]]: List of genres with ID and name
        """
        return self._make_request("genre/all", {"limit": limit, "offset": offset}) 