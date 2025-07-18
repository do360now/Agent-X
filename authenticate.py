import tweepy
import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
logger.info("Loading environment variables from .env file...")
load_dotenv()

# Get API credentials from environment variables with error handling
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

logger.info("Checking if all Twitter API credentials are available...")
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    raise ValueError(
        "One or more Twitter API credentials are missing. Please check your environment variables."
    )

def authenticate_v1() -> tweepy.API:
    """
    Authenticate with Twitter API v1.1 using OAuth 1.0a User Context and return the API object.
    """
    logger.info("Authenticating with Twitter API v1.1 using OAuth 1.0a User Context...")
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    logger.info("Successfully authenticated with Twitter API v1.1.")
    return api

def authenticate_v2() -> tweepy.Client:
    """
    Authenticate with Twitter API v2 using OAuth 1.0a User Context and return the Client object.
    """
    logger.info("Authenticating with Twitter API v2 using OAuth 1.0a User Context...")
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
    )
    logger.info("Successfully authenticated with Twitter API v2.")
    return client