import tweepy
import logging
import time
import random
import datetime
import pytz
from authenticate import authenticate_v2, authenticate_v1
from generate import find_ai_generated_image, generate_post_topic, gpt_generate_tweet
from generate_image import generate_image

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define optimal posting hours (e.g., 9 a.m. to 3 p.m. EST)
optimal_start_hour = 9
optimal_end_hour = 15

# Set timezone for target audience (Eastern Time)
target_timezone = pytz.timezone('US/Eastern')

def main():
    # Authenticate only once
    logger.info("Starting authentication for Twitter API v2...")
    client = authenticate_v2()
    api_v1 = authenticate_v1() if client else None

    # Posting loop
    while True:
        # Get the current time in the target timezone (e.g., EST)
        now = datetime.datetime.now(target_timezone)

        # Calculate next posting time
        if optimal_start_hour <= now.hour < optimal_end_hour:
            next_post_time = now
        else:
            # Schedule next post at the start of the optimal window (next day if outside of hours)
            next_post_time = now.replace(hour=optimal_start_hour, minute=0, second=0, microsecond=0)
            if now.hour >= optimal_end_hour:
                next_post_time += datetime.timedelta(days=1)

        # Add a small random delay to avoid looking like a bot (e.g., between 10 to 45 minutes)
        random_minutes = random.randint(10, 45)
        next_post_time += datetime.timedelta(minutes=random_minutes)

        # Log and calculate sleep duration
        logger.info(f"Next post scheduled at: {next_post_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        time_to_sleep = (next_post_time - now).total_seconds()

        # Wait until the next scheduled time
        if time_to_sleep > 0:
            logger.info(f"Sleeping for {time_to_sleep / 3600:.2f} hours...")
            time.sleep(time_to_sleep)

        # Generate post topic and image
        topic = generate_post_topic()
        logger.info(f"Generated topic for the post: {topic}")
        generate_image(topic)

        # Start the tweet generation process
        post_tweet(topic, client, api_v1)

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
