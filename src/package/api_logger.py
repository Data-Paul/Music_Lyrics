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


# _make_request ist eine private Methode, die verwendet wird, um Anfragen an die MusicBrainz API zu stellen.
# endpoint ist der letzte Teil der URL, der für die Anfrage verwendet wird.
# params ist ein optionales Dictionary mit Parametern, die in der Anfrage übergeben werden.
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Sendet eine Anfrage an die MusicBrainz API mit Rate-Limiting.
        Diese Methode wird intern von allen anderen Methoden verwendet.
        """
        try:
            # Führt die GET-Anfrage aus
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            
            # Erfolgreiche Anfrage
            if response.status_code == 200:
                return response.json()
            # Rate-Limit überschritten, warte und versuche es erneut
            elif response.status_code == 503:
                print(f"Rate limit exceeded. Waiting before retry...")
                time.sleep(1)  # Wait 1 second before retry
                return self._make_request(endpoint, params)
            # Andere Fehler
            else:
                print(f"Error: Status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_genres(self, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """Get a list of all genres."""
        return self._make_request("genre/all", {"limit": limit, "offset": offset})

    def get_artists_by_genre(self, genre: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """Sucht Künstler nach Genre."""
        return self._make_request("artist", {
            "query": f"genre:{genre}",  # Sucht Künstler mit diesem Genre
            "limit": limit,             # Maximale Anzahl der Ergebnisse
            "offset": offset            # Startposition für Paginierung
        })

    def get_release_groups(self, artist_id: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """Holt alle Veröffentlichungsgruppen eines Künstlers."""
        return self._make_request("release-group", {
            "artist": artist_id,  # MusicBrainz ID des Künstlers
            "limit": limit,
            "offset": offset
        })

    def get_recordings(self, release_id: str, limit: int = 100, offset: int = 0) -> Optional[List[Dict]]:
        """Holt alle Aufnahmen einer Veröffentlichung."""
        return self._make_request("recording", {
            "release": release_id,  # MusicBrainz ID der Veröffentlichung
            "limit": limit,
            "offset": offset
        })

    def get_artist_details(self, artist_id: str) -> Optional[Dict]:
        """Holt detaillierte Informationen über einen Künstler."""
        return self._make_request(f"artist/{artist_id}", {"inc": "releases"}) 