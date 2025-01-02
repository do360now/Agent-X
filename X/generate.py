import os
import logging
import random
from authenticate import open_ai_auth

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ai_client = open_ai_auth()


# Function to generate VR/AR-specific topics
def generate_post_topic():
    """
    Generate a random topic for a tweet from a predefined list of automatic post agent-related topics.
    """
    topics = [
        "Benefits of Automating Social Media Posts",
        "How Content Automation Saves Time for Professionals",
        
    ]
    topic = random.choice(topics)
    logger.info(f"Selected random topic: {topic}")
    return topic

def post_process_tweet(tweet):
    tweet = tweet[:250]
    if "#" not in tweet:
        tweet += " #VR #AR"  # Add default hashtags for VR and AR
    return tweet


def find_image_for_topic(topic: str):
    """
    Find an image that matches the topic from the images folder.
    """
    images_folder = "images/"
    logger.info(f"Searching for an image related to topic: {topic}")
    if not os.path.exists(images_folder):
        logger.error(f"Images folder '{images_folder}' does not exist.")
        return None

    for filename in os.listdir(images_folder):
        if topic.lower() in filename.lower():
            image_path = os.path.join(images_folder, filename)
            logger.info(f"Found image for topic '{topic}': {image_path}")
            if not os.path.isfile(image_path):
                logger.error(f"Found file '{image_path}' is not a valid image file.")
                return None
            return image_path, topic
    logger.info(f"No image found for topic: {topic}")
    return None

def gpt_generate_tweet(post_topic):
    """
    Generate a post based on the provided topic using ChatGPT API.
    """
    logger.info(
        f"Generating a post based on the following topic using ChatGPT API: {post_topic}..."
    )
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a bad ass marketing agent."},
            {
                "role": "user",
                "content": (
                    f"Create a snappy and engaging post on {post_topic}, offering help wtih automatic posting to X and Wordpress accounts. Keep it under 250 characters. "
                    "Include relevant hashtags like #post #wordpress #X."
                ),
            },
        ],
    )
    logger.info(
        f"Received response from ChatGPT API for topic '{post_topic}': {response}"
    )
    tweet = response.choices[0].message.content.strip()
    if len(tweet) > 250:
        logger.warning(
            f"Generated tweet exceeds 250 characters. Truncating tweet: {tweet}"
        )
        tweet = tweet[:247] + "..."  # Truncate to 200 characters with ellipsis
    logger.info(f"Generated tweet: {tweet}")
    return tweet


def find_ai_generated_image(topic: str):
    """
    Find an image that matches the topic from the images folder.
    """
    image_path = "images/ai_gen_image.png"
    logger.info(f"Loading image for topic: {topic}")
    if not os.path.exists(image_path):
        logger.error(f"Image file '{image_path}' does not exist.")
        return None

    if not os.path.isfile(image_path):
        logger.error(f"Found file '{image_path}' is not a valid image file.")
        return None

    logger.info(f"Found image for topic '{topic}': {image_path}")
    return image_path
