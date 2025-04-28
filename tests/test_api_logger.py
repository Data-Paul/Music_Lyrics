import unittest
from unittest.mock import patch, MagicMock
import logging
import requests
from src.package.api_logger import MusicBrainzAPI

#Erklärung: Mocking
# In diesem Testfile wird Mocking eingesetzt, um externe Abhängigkeiten zu simulieren.
# Konkret werden die Methoden 'requests.Session.get' und 'time.sleep' gemockt:
# - 'requests.Session.get' wird ersetzt, um API-Aufrufe zu kontrollieren und keine echten HTTP-Requests zu senden.
# - 'time.sleep' wird ersetzt, damit Rate-Limit-Simulationen den Test nicht künstlich verzögern.
# Dadurch können API-Methoden isoliert, schnell und reproduzierbar getestet werden – inklusive Fehlerbehandlung (z. B. Netzwerkfehler, Rate-Limit-Überschreitungen).

# Konfiguriere Logging für bessere Fehlermeldungen
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestMusicBrainzAPI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = MusicBrainzAPI()
        # Erstelle ein Mock-Response-Objekt für erfolgreiche API-Aufrufe
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {
            "artists": [
                {"id": "1", "name": "Test Artist", "type": "Person"}
            ]
        }

    @patch('time.sleep')
    @patch('requests.Session.get')
    def test_get_artists_by_genre(self, mock_get, mock_sleep):
        """Test retrieving artists by genre."""
        logger.debug("Starting test_get_artists_by_genre")
        # Konfiguriere den Mock für einen erfolgreichen API-Aufruf
        mock_get.return_value = self.mock_response
        
        # Teste erfolgreichen API-Aufruf
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNotNone(result, "API call should return a result")
        self.assertEqual(result["artists"][0]["name"], "Test Artist", 
                        "Artist name should match expected value")
        
        # Teste Rate-Limit-Handling
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 503
        # Simuliere einen Rate-Limit-Fehler gefolgt von einem erfolgreichen Aufruf
        mock_get.side_effect = [rate_limit_response, self.mock_response]
        
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNotNone(result, "API call should succeed after rate limit retry")
        self.assertEqual(result["artists"][0]["name"], "Test Artist",
                        "Artist name should match after rate limit retry")

    @patch('time.sleep')
    @patch('requests.Session.get')
    def test_get_artist_recordings(self, mock_get, mock_sleep):
        """Test retrieving artist recordings."""
        logger.debug("Starting test_get_artist_recordings")
        mock_get.return_value = self.mock_response
        
        result = self.api.get_artist_recordings("test-id")
        self.assertIsNotNone(result, "API call should return a result")
        self.assertEqual(result["artists"][0]["name"], "Test Artist",
                        "Artist name should match expected value")

    @patch('time.sleep')
    @patch('requests.Session.get')
    def test_get_genres(self, mock_get, mock_sleep):
        """Test retrieving genres."""
        logger.debug("Starting test_get_genres")
        mock_get.return_value = self.mock_response
        
        result = self.api.get_genres()
        self.assertIsNotNone(result, "API call should return a result")
        self.assertEqual(result["artists"][0]["name"], "Test Artist",
                        "Artist name should match expected value")

    @patch('time.sleep')
    @patch('requests.Session.get')
    def test_error_handling(self, mock_get, mock_sleep):
        """Test error handling in API requests."""
        logger.debug("Starting test_error_handling")
        
        # Teste Netzwerkfehler
        logger.debug("Testing network error scenario")
        # Simuliere einen Netzwerkfehler
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        # Teste, ob die API None zurückgibt bei einem Netzwerkfehler
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNone(result, "API call should return None for network errors")
        
        # Setze den Mock zurück für den nächsten Test
        mock_get.reset_mock()
        
        # Teste nicht-200 Statuscode
        logger.debug("Testing 404 error scenario")
        error_response = MagicMock()
        error_response.status_code = 404
        mock_get.return_value = error_response
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNone(result, "API call should return None for 404 errors")
        
        # Setze den Mock zurück für den nächsten Test
        mock_get.reset_mock()
        
        # Teste Rate-Limit mit mehreren Wiederholungsversuchen
        logger.debug("Testing rate limit retry scenario")
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 503
        mock_get.side_effect = [rate_limit_response, rate_limit_response, self.mock_response]
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNotNone(result, "API call should succeed after rate limit retries")
        self.assertEqual(result["artists"][0]["name"], "Test Artist",
                        "Artist name should match after rate limit retries")

    @patch('time.sleep')
    @patch('requests.Session.get')
    def test_rate_limit_retry(self, mock_get, mock_sleep):
        """Test rate limit retry mechanism."""
        logger.debug("Starting test_rate_limit_retry")
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 503
        mock_get.side_effect = [rate_limit_response, self.mock_response]
        
        result = self.api.get_artists_by_genre("rock")
        self.assertIsNotNone(result, "API call should succeed after rate limit retry")
        self.assertEqual(result["artists"][0]["name"], "Test Artist",
                        "Artist name should match after rate limit retry")
        mock_sleep.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main() 