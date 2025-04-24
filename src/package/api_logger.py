"""
Module for API data logging and request handling.
This module provides functions to fetch and process API data using the requests module.
""" 

import requests

# The API root URL is https://musicbrainz.org/ws/2/. 

def get_musicbrainz():
    """Sendet eine GET-Anfrage an die Google Books API, um Bücher zu suchen."""
    url = "https://musicbrainz.org/ws/2/artist" # Maybe get a artist list from the api genre divided
    artist = []
    try:
        response = requests.get(url)

        # Überprüfe, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            return response.json()  # Gibt die JSON-Antwort zurück
        elif response.status_code == 503:
            print(f"Fehler: Too many requests. Please try again later. {response.status_code}.")
            return None
        else:
            print(f"Fehler: Unzulässiger Statuscode {response.status_code}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None