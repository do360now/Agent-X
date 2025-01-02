import tweepy
import os
import logging
import time
import random
from dotenv import load_dotenv
from authenticate import authenticate_v2, authenticate_v1, open_ai_auth
import requests


# Configure logger with timestamp and log level
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
logger.info("Loading environment variables from .env file...")
load_dotenv()

ai_client = open_ai_auth()

# Main function to run the tweet generation process
def main():
    """
    Main function to run the tweet generation process
    """
    try:
        # Authenticate with Twitter API v2
        logger.info("Starting authentication for Twitter API v2...")
        client = authenticate_v2()

        # Configurable frequency for posting (from environment variable or default to random between 1 to 2 hours)
        POST_INTERVAL = int(os.getenv("POST_INTERVAL", random.randint(600, 7200)))
        logger.info(f"Configured posting interval: {POST_INTERVAL} seconds")

        while True:
            try:
                logger.info("Starting tweet generation process...")
                post_topic = generate_post_topic()  # Generate the topic once

                # Generate both image and tweet based on the same topic
                image_path = gpt_generate_image(post_topic)
                tweet_v2 = gpt_generate_tweet(post_topic)
                logger.info(f"Attempting to post tweet using v2 API: '{tweet_v2}'")

                if image_path:
                    # Authenticate with Twitter API v1.1 to upload media
                    api_v1 = authenticate_v1()
                    media = api_v1.media_upload(filename=image_path)
                    # Post the tweet with the image
                    response = client.create_tweet(
                        text=tweet_v2, media_ids=[media.media_id]
                    )
                    logger.info(
                        f"Tweeted successfully with image using v2 API: {response.data['id']}"
                    )
                else:
                    logger.info("No image found, posting tweet without image.")
                    # Post the tweet without an image
                    response = client.create_tweet(text=tweet_v2)
                    logger.info(
                        f"Tweeted successfully without image using v2 API: {response.data['id']}"
                    )

                logger.info(
                    f"Waiting for {POST_INTERVAL} seconds before the next tweet..."
                )
                time.sleep(POST_INTERVAL)

            except tweepy.TweepyException as e:
                logger.error(f"Failed to post tweet using v2 API: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

    except KeyboardInterrupt:
        logger.info("Tweet posting process interrupted by user.")
    finally:
        logger.info("Exiting the tweet posting process.")

def generate_post_topic():
    """
    Generate a random topic for a tweet from a predefined list of VR/AR-related topics.
    """
    topics = [
        "Latest VR Headset Releases",
        "AR in Healthcare",
        "VR Training Programs",
        "Augmented Reality in Retail",
        "VR & AR in Education",
        "Future of the Metaverse",
        "Immersive VR Gaming",
        "AR-Powered Navigation",
        "Using VR for Mental Health",
        "Innovations in Mixed Reality",
        "AR in Interior Design",
        "VR for Remote Work",
        "Extended Reality Trends",
        "Interactive AR Experiences",
        "VR Hardware Comparisons",
        "Real-World AR Use Cases",
        "Impact of VR in Therapy",
        "Metaverse Development Updates",
        "Tips for VR Beginners",
        "How to Get Started with AR",
        "VenezArt",
    ]
    topic = random.choice(topics)
    logger.info(f"Selected random topic: {topic}")
    return topic

def post_process_tweet(tweet):
    tweet = tweet[:250]
    if "#" not in tweet:
        tweet += " #VR #AR"  # Add default hashtags for VR and AR
    return tweet

def gpt_generate_tweet(post_topic):
    """
    Generate a post based on the provided VR/AR topic using ChatGPT API.
    """
    logger.info(
        f"Generating a post based on the following topic using ChatGPT API: {post_topic}..."
    )
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": (
                    f"Create a snappy and engaging post on {post_topic}, offering VR or AR tips or news under 250 characters. "
                    "Include relevant hashtags like #VR #AR."
                ),
            },
        ],
    )
    logger.info(
        f"Received response from ChatGPT API for topic '{post_topic}': {response}"
    )
    tweet = response.choices[0].message.content.strip()
    if len(tweet) > 200:
        logger.warning(
            f"Generated tweet exceeds 250 characters. Truncating tweet: {tweet}"
        )
        tweet = tweet[:197] + "..."  # Truncate to 200 characters with ellipsis
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


def gpt_generate_image(post_topic: str):
    """
    Generate an image related to the VR/AR topic using OpenAI's API.
    """
    logger.info(f"Generating an image related to topic: {post_topic}")
    
    # Map VR/AR topics to prompts
    prompt_map = {
        "Latest VR Headset Releases": "A close-up of a modern, sleek VR headset with a minimalistic design, showcased on a clean, well-lit futuristic platform with soft digital reflections.",
        "AR in Healthcare": "A doctor in a brightly lit, modern hospital wearing AR glasses, viewing a holographic medical display that surrounds the patient in a clear and realistic manner.",
        "VR Training Programs": "A realistic virtual reality training room where participants are focused, wearing VR headsets and holding simple controllers, with a clean, organized layout.",
        "Augmented Reality in Retail": "A shopper in a well-lit retail store using an AR app on a tablet, with realistic holograms displaying furniture overlaid in the room for easy visualization.",
        "VR & AR in Education": "Students in a brightly lit classroom using VR and AR devices, interacting with clear educational holograms and virtual environments around them.",
        "Future of the Metaverse": "A vibrant and well-organized metaverse scene with avatars walking around digital structures, colorful holographic signs, and clear virtual event displays in a high-resolution environment.",
        "Immersive VR Gaming": "A gamer in a dark room with soft neon lights, wearing a VR headset and gloves, surrounded by simple holographic game elements for an immersive experience.",
        "AR-Powered Navigation": "A person walking through a city street using AR glasses with simple digital navigation markers overlaid on buildings and street signs in clear view.",
        "Using VR for Mental Health": "A peaceful virtual reality scene, like a calm forest or beach, created to provide relaxation for mental health therapy in a realistic, calming environment.",
        "Innovations in Mixed Reality": "A modern workspace where people use mixed reality glasses to interact with clear holographic screens and physical objects in a well-lit setting.",
        "AR in Interior Design": "An interior designer in a naturally lit room using an AR tablet, visualizing realistic furniture and decor changes with subtle digital overlays.",
        "VR for Remote Work": "A virtual office space where remote workers connect via VR headsets, collaborating in a clean, organized virtual workspace with clear holographic screens.",
        "Extended Reality Trends": "A tech showcase with a variety of XR devices on display, each with subtle holographic labels describing their features in a well-lit, minimalistic environment.",
        "Interactive AR Experiences": "People in a park setting, interacting with digital animals and objects through AR on their mobile devices, in a realistic outdoor environment.",
        "VR Hardware Comparisons": "A lineup of various VR headsets on a sleek display table, each with digital tags explaining their features, set in a modern tech showroom.",
        "Real-World AR Use Cases": "A split scene showcasing AR in healthcare, retail, and navigation, each with subtle, transparent holographic overlays displaying real-time information.",
        "Impact of VR in Therapy": "A therapist using VR with a patient in a calm, minimalist therapy room, showcasing a relaxing virtual environment on the VR headset display.",
        "Metaverse Development Updates": "Developers in a high-tech lab working on metaverse projects, with clear holographic screens displaying code and digital assets for virtual worlds.",
        "Tips for VR Beginners": "A simple, beginner-friendly VR setup guide with icons for setup, safety, and recommended apps, displayed in a clean and organized layout.",
        "How to Get Started with AR": "A person holding a tablet with an AR app, with digital instructions on the screen in a well-lit room, perfect for first-time AR users.",
        "VenezArt": "A virtual art gallery featuring digital art by VenezArt, with immersive, interactive exhibits and multimedia experiences in a clean, professional gallery space.",
}



    prompt = prompt_map.get(post_topic, f"A high-tech VR or AR scene illustrating {post_topic}, with immersive and interactive elements.")
    
    try:
        response = ai_client.images.generate(
            prompt=prompt,
            n=1,
            size="512x512",
        )

        image_url = response.data[0].url
        logger.info(f"Generated image for topic '{post_topic}': {image_url}")

        # Download the image to a local file
        image_path = f"images/{post_topic.replace(' ', '_').lower()}_image.png"
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(image_path, "wb") as file:
                file.write(image_response.content)
            logger.info(f"Image downloaded successfully to {image_path}")
        else:
            logger.error(
                f"Failed to download image, status code: {image_response.status_code}"
            )
            return None
        return image_path
    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        return None

if __name__ == "__main__":
    main()
