import tweepy
import os
import logging
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables from the .env file
logger.info("Loading environment variables from .env file...")
load_dotenv()

# Get Twitter API credentials from environment variables with error handling
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")


logger.info("Checking if all Twitter API credentials are available...")
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    raise ValueError(
        "One or more Twitter API credentials are missing. Please check your environment variables."
    )

if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable."
    )


def authenticate_v1():
    """
    Authenticate with Twitter API v1.1 using OAuth 1.0a User Context and return the API object.
    """
    logger.info("Authenticating with Twitter API v1.1 using OAuth 1.0a User Context...")
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    logger.info("Successfully authenticated with Twitter API v1.1.")
    return api


def authenticate_v2():
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


def open_ai_auth():
    """
    Authenticate with OpenAI API using the provided API key.
    """
    logger.info("Authenticating with OpenAI API...")

    ai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    logger.info("Successfully authenticated with OpenAI API.")
    return ai_client


def grok_ai_auth():
    """
    Authenticate with X.AI API using the provided API key.
    """
    logger.info("Authenticating with X.AI API...")
    
    client = OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )
    logger.info("Successfully authenticated with X.AI API.")

    return client
