import tweepy
import logging
import time
import random
from authenticate import authenticate_v2, authenticate_v1
from generate import find_ai_generated_image, generate_post_topic, gpt_generate_tweet
from generate_image import generate_image


# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Authenticate only once
    logger.info("Starting authentication for Twitter API v2...")
    client = authenticate_v2()
    api_v1 = authenticate_v1() if client else None


    # Temporarlily disable the posting loop
    # Configurable frequency for posting (random between 1 to 2 hours)
    while True:
        topic = generate_post_topic()
        logger.info(f"Generated topic for the post: {topic}")
        generate_image(topic)

        POST_INTERVAL = random.randint(0.5 * 3600, 1 * 3600)
        logger.info(f"Configured posting interval: {POST_INTERVAL} seconds")

        # Start the tweet generation process
        post_tweet(topic, client, api_v1)

        # Wait for the configured interval before posting the next tweet
        logger.info(f"Waiting for {POST_INTERVAL} seconds before the next tweet...")
        time.sleep(POST_INTERVAL)


def post_tweet(topic, client, api_v1):
    try:
        # Generate the tweet content
        tweet_content = gpt_generate_tweet(topic)
        if not tweet_content:
            logger.error("Tweet generation failed. Stopping the app.")
            return  # Stop the function if tweet generation fails

        image_path = find_ai_generated_image(topic)
        if image_path:
            logger.info(f"Attempting to upload image at {image_path}...")
            media = api_v1.media_upload(filename=image_path)
            logger.info(f"Image uploaded successfully: media_id = {media.media_id}")
            response = client.create_tweet(
                text=tweet_content, media_ids=[media.media_id]
            )
            logger.info(f"Tweeted successfully with image: {response.data['id']}")
        else:
            response = client.create_tweet(text=tweet_content)
            logger.info(f"Tweeted successfully without image: {response.data['id']}")
    except tweepy.TweepyException as e:
        logger.error(f"Failed to post tweet: {e}")


if __name__ == "__main__":
    main()
