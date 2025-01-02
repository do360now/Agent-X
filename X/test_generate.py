import unittest
from unittest.mock import patch, MagicMock
import os
import random
import logging
from authenticate import open_ai_auth, grok_ai_auth
from generate import (
    generate_post_topic,
    post_process_tweet,
    generate_tweet,
    find_image_for_topic,
    gpt_generate_tweet,
    find_ai_generated_image,
    grok_generate_topic,
    grok_generate_post,
)

class TestFunctions(unittest.TestCase):
    
    @patch('random.choice')
    def test_generate_post_topic(self, mock_choice):
        mock_choice.return_value = "Benefits of Automating Social Media Posts"
        result = generate_post_topic()
        self.assertEqual(result, "Benefits of Automating Social Media Posts")

    def test_post_process_tweet(self):
        tweet = "This is a tweet without hashtags."
        result = post_process_tweet(tweet)
        self.assertIn("#VR", result)
        self.assertIn("#AR", result)

        tweet_with_hashtags = "This is a tweet with #VR hashtag."
        result = post_process_tweet(tweet_with_hashtags)
        self.assertEqual(result, tweet_with_hashtags[:250])

    @unittest.skip("Skipping test_generate_tweet")
    @patch('ollama.chat')
    def test_generate_tweet(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "This is a test tweet."}}
        topic = "Latest VR Headset Releases"
        result = generate_tweet(topic)
        self.assertEqual(result, "This is a test tweet. #VR #AR")

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.listdir')
    def test_find_image_for_topic(self, mock_listdir, mock_isfile, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["vr_image.png", "ar_image.jpg"]
        mock_isfile.return_value = True

        result = find_image_for_topic("vr")
        self.assertEqual(result, ("images/vr_image.png", "vr"))

    @unittest.skip("Skipping test_gpt_generate_tweet")
    @patch('open_ai_auth.chat.completions.create')
    def test_gpt_generate_tweet(self, mock_ai_client):
        mock_ai_client.return_value = {
            "choices": [{"message": {"content": "This is a GPT-generated tweet."}}]
        }

        result = gpt_generate_tweet("Test topic")
        self.assertEqual(result, "This is a GPT-generated tweet.")

    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_find_ai_generated_image(self, mock_isfile, mock_exists):
        mock_exists.return_value = True
        mock_isfile.return_value = True

        result = find_ai_generated_image("topic")
        self.assertEqual(result, "images/ai_gen_image.png")

    @unittest.skip("Skipping test_grok_generate_topic")
    @patch('grok_ai_auth.chat.completions.create')
    def test_grok_generate_topic(self, mock_grok_client):
        mock_grok_client.return_value = {
            "choices": [{"message": {"content": "Trending Bitcoin Topic"}}]
        }

        result = grok_generate_topic()
        self.assertEqual(result, "Trending Bitcoin Topic")

    @unittest.skip("Skipping test_grok_generate_post")
    @patch('grok_ai_auth.chat.completions.create')
    def test_grok_generate_post(self, mock_grok_client):
        mock_grok_client.return_value = {
            "choices": [{"message": {"content": "Engaging Bitcoin Post"}}]
        }

        result = grok_generate_post("Bitcoin Topic")
        self.assertEqual(result, "Engaging Bitcoin Post")

if __name__ == "__main__":
    unittest.main()
