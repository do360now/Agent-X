import unittest
from unittest.mock import patch, MagicMock
import os
from authenticate import authenticate_v1, authenticate_v2, open_ai_auth

class TestAuthenticate(unittest.TestCase):

    @patch("authenticate.tweepy.OAuth1UserHandler")
    @patch("authenticate.tweepy.API")
    def test_authenticate_v1(self, mock_tweepy_api, mock_oauth1_handler):
        """Test authenticate_v1 successfully authenticates and returns API object."""
        mock_api_instance = MagicMock()
        mock_tweepy_api.return_value = mock_api_instance
        mock_oauth1_handler.return_value = MagicMock()

        api = authenticate_v1()

        mock_oauth1_handler.assert_called_once_with(
            os.getenv("API_KEY"),
            os.getenv("API_SECRET"),
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_SECRET"),
        )
        mock_tweepy_api.assert_called_once_with(mock_oauth1_handler.return_value)
        self.assertEqual(api, mock_api_instance)

    @patch("authenticate.tweepy.Client")
    def test_authenticate_v2(self, mock_tweepy_client):
        """Test authenticate_v2 successfully authenticates and returns Client object."""
        mock_client_instance = MagicMock()
        mock_tweepy_client.return_value = mock_client_instance

        client = authenticate_v2()

        mock_tweepy_client.assert_called_once_with(
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_SECRET"),
        )
        self.assertEqual(client, mock_client_instance)

    @patch("authenticate.openai.OpenAI")
    def test_open_ai_auth(self, mock_openai):
        """Test open_ai_auth successfully authenticates with OpenAI API."""
        mock_openai_instance = MagicMock()
        mock_openai.return_value = mock_openai_instance

        ai_client = open_ai_auth()

        mock_openai.assert_called_once_with(api_key=os.getenv("OPENAI_API_KEY"))
        self.assertEqual(ai_client, mock_openai_instance)
    

    @patch("authenticate.API_KEY", None)
    @patch("authenticate.API_SECRET", None)
    @patch("authenticate.ACCESS_TOKEN", "mock_access_token")
    @patch("authenticate.ACCESS_SECRET", "mock_access_secret")
    def test_missing_environment_variables(self):
        """Test that missing environment variables raise appropriate errors."""
        with self.assertRaises(ValueError) as v1_error:
            authenticate_v1()
        self.assertIn("One or more X API credentials are missing", str(v1_error.exception))


if __name__ == "__main__":
    unittest.main()
