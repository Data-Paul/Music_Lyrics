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
    Format artist and song name into the correct URL format for azlyrics.com
    
    Args:
        artist (str): Artist name
        song (str): Song name
        
    Returns:
        str: Formatted URL
    """
    # Convert to lowercase
    artist = artist.lower()
    song = song.lower()
    
    # Remove special characters except hyphens and spaces
    artist = re.sub(r'[^a-z0-9\s-]', '', artist)
    song = re.sub(r'[^a-z0-9\s-]', '', song)
    
    # Replace spaces with hyphens
    artist = artist.replace(' ', '-')
    song = song.replace(' ', '')
    
    return f"https://www.azlyrics.com/lyrics/{artist}/{song}.html"

def scrape_lyrics(artist: str, song: str) -> str:
    """
    Scrape lyrics from azlyrics.com for a given artist and song
    
    Args:
        artist (str): Artist name
        song (str): Song name
        
    Returns:
        str: The lyrics of the song, or an error message if not found
    """
    # Format the URL
    url = format_url(artist, song)
    
    # Add a delay to be respectful to the server
    time.sleep(2)
    
    try:
        # Make the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the lyrics div (this is the typical structure on azlyrics.com)
        lyrics_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
        if not lyrics_div:
            return "Lyrics not found"
            
        # Extract the lyrics
        lyrics = lyrics_div.find('div', class_=None).get_text(strip=True)
        return lyrics
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching lyrics: {str(e)}"
    except Exception as e:
        return f"Error processing lyrics: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Test with a known song
    artist = "Anderson .Paak"
    song = "Make It Work"
    lyrics = scrape_lyrics(artist, song)
    print(f"Lyrics for {song} by {artist}:")
    print(lyrics)