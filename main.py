import tweepy
import logging
import random
import time
import os

from authenticate import authenticate_v2, authenticate_v1
from generate import generate_topic, generate_post, find_image_for_topic

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to authenticate and post tweets on X at random intervals."""
    # Authenticate for Twitter API v2 and v1
    logger.info("Starting authentication for Twitter API v2...")
    client = authenticate_v2()
    api_v1 = authenticate_v1()

    if not client or not api_v1:
        logger.error("Authentication failed. Cannot proceed with posting.")
        return

    # Configurable frequency for posting (random between 1 to 3 hours)
    while True:
        topic = generate_topic()
        logger.info(f"The selected topic for the post is: {topic}")

        # Generate post content
        post_content = generate_post(topic)
        if not post_content:
            logger.error(f"Failed to generate post content for topic: {topic}. Skipping post.")
            time.sleep(60)  # Short wait before retry
            continue

        # Optionally generate or find image (uncomment to enable)
        # image_path = find_image_for_topic(topic)
        image_path = None

        # Upload the post
        upload_post(post_content, client, api_v1, image_path)

        # Wait for a random interval (1 to 3 hours) before the next post
        post_interval = random.randint(3600, 10800)  # 1 to 3 hours in seconds
        logger.info(f"Waiting for {post_interval / 60:.1f} minutes before the next post...")
        time.sleep(post_interval)

def upload_post(content: str, client: tweepy.Client, api_v1: tweepy.API, image_path: str | None = None) -> None:
    """
    Upload a tweet with optional image on X.

    Args:
        content (str): The tweet content.
        client (tweepy.Client): Twitter API v2 client for posting.
        api_v1 (tweepy.API): Twitter API v1 client for media upload.
        image_path (str | None): Path to the image file (optional).

    Raises:
        tweepy.TweepyException: If posting or uploading fails.
    """
    try:
        media_ids = None
        if image_path:
            if not os.path.exists(image_path):
                logger.warning(f"Image file not found at {image_path}. Posting without image.")
            else:
                media = api_v1.media_upload(filename=image_path)
                logger.info(f"Image uploaded successfully: media_id = {media.media_id}")
                media_ids = [media.media_id]

        # Post the tweet
        response = client.create_tweet(text=content, media_ids=media_ids)
        logger.info(f"Posted successfully: {response.data['id']}")
    except tweepy.TweepyException as e:
        logger.error(f"Failed to post tweet: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during tweet upload: {e}")

if __name__ == "__main__":
    main()