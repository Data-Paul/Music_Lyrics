"""
Web Scraping Module for Lyrics Collection

This module provides functionality to scrape song lyrics from azlyrics.com.
It handles URL formatting, web requests, and HTML parsing to extract lyrics
for given artist-song combinations. The module includes:
- URL formatting for azlyrics.com
- Web scraping with proper headers and rate limiting
- HTML parsing using BeautifulSoup
- Error handling for various scraping scenarios

Note: This module implements a delay between requests to respect the
website's server and avoid being blocked.
"""
# Webscraping -> https://www.azlyrics.com/lyrics/
# Ich muss das ende der URL so designen:
# "artist/song-name.html" zb. "metallica/masterofpuppets.html"
# Das heißt ich muss aus der db/API den Artist Namen und die Song Namen nehmen
# Dann die Lyrics scrapen und alles in der Datenbank speichern

import requests
from bs4 import BeautifulSoup
import time
import re

def format_url(artist: str, song: str) -> str:
    """
    Format artist and song name into the correct URL format for azlyrics.com.
    
    Args:
        artist (str): Artist name to format
        song (str): Song name to format
        
    Returns:
        str: Formatted URL for azlyrics.com
        
    Note:
        The function handles special characters and spaces by:
        - Converting to lowercase
        - Removing special characters (except hyphens and spaces)
        - Replacing spaces with hyphens in artist names
        - Removing spaces in song names
    """
    # Konvertiere zu Kleinbuchstaben
    artist = artist.lower()
    song = song.lower()
    
    # Entferne Sonderzeichen außer Bindestrichen und Leerzeichen
    artist = re.sub(r'[^a-z0-9\s-]', '', artist)
    song = re.sub(r'[^a-z0-9\s-]', '', song)
    
    # Ersetze Leerzeichen mit Bindestrichen
    artist = artist.replace(' ', '-')
    song = song.replace(' ', '')
    
    return f"https://www.azlyrics.com/lyrics/{artist}/{song}.html"

def scrape_lyrics(artist: str, song: str) -> str:
    """
    Scrape lyrics from azlyrics.com for a given artist and song.
    
    Args:
        artist (str): Name of the artist
        song (str): Name of the song
        
    Returns:
        str: The lyrics of the song, or an error message if not found
        
    Note:
        The function includes:
        - Rate limiting (2-second delay between requests)
        - User-Agent header to avoid blocking
        - Error handling for network and parsing issues
    """
    # Formatiere die URL
    url = format_url(artist, song)
    
    # Füge eine Verzögerung hinzu, um den Server zu respektieren
    time.sleep(2)
    
    try:
        # Mache die Anfrage mit einem Browser-ähnlichen User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Wirft eine Exception bei fehlerhaften Statuscodes
        
        # Parse das HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finde den Lyrics-Div (typische Struktur auf azlyrics.com)
        lyrics_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
        if not lyrics_div:
            return "Lyrics not found"
            
        # Extrahiere die Lyrics
        lyrics = lyrics_div.find('div', class_=None).get_text(strip=True)
        return lyrics
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching lyrics: {str(e)}"
    except Exception as e:
        return f"Error processing lyrics: {str(e)}"

# Beispielverwendung
if __name__ == "__main__":
    # Test mit einem bekannten Song
    artist = "Anderson .Paak"
    song = "Make It Work"
    lyrics = scrape_lyrics(artist, song)
    print(f"Lyrics for {song} by {artist}:")
    print(lyrics)