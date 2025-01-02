from diffusers import StableDiffusionPipeline
from torch import autocast
from authenticate import open_ai_auth
import logging
import torch
import os
import requests

# Configure logger with timestamp and log level
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

ai_client = open_ai_auth()

def main(topic):
    print("Starting the main function...")
    generate_image(topic)
    print("Main function finished.")

def validate_topic(topic):
    if not topic or not isinstance(topic, str):
        raise ValueError("The topic must be a non-empty string.")
    return topic.strip()

def generate_image(topic):
    print(f"Generating image for topic: {topic}")
    model_id = "runwayml/stable-diffusion-v1-5"
    print(f"Loading model: {model_id}")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

    pipe.enable_attention_slicing()
    print("Model loaded successfully.")

    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
        print(f"CUDA available. Using {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA is not available. Using CPU instead.")

    # Define VR/AR-specific prompts for each topic
    prompts = {
        
        "Benefits of Automating Social Media Posts": "An illustration of automation software managing multiple social media accounts simultaneously",
        "How Content Automation Saves Time for Professionals": "A professional working on important tasks while a robot manages social media posts",
        "Maximizing Engagement with Automated Posting Schedules": "A graph showing increased engagement over time due to optimized post scheduling",
        "Peak Hours for Social Media Engagement": "A digital clock indicating peak engagement hours with social media icons",
        "ROI on Social Media Automation Tools": "A visual representation of ROI growth as a result of using social media automation tools",
        "Consistency in Social Media Presence with Automation": "An AI robot consistently posting content on different social media platforms",
        "How Automated Posting Helps You Focus on Core Business Activities": "A relaxed business owner focusing on core activities while automation manages social media",
        "Best Practices for Automated Content Generation": "A checklist of best practices for using automation tools for social media",
        "AI Tools for Consistent Social Media Growth": "A concept image showing AI tools helping a plant grow, symbolizing consistent social media growth",
        "Balancing Personal Touch and Automation in Social Media": "A professional adjusting automated posts to add a personal touch",
        "Customizing Automated Posts for Your Audience": "An image of AI analyzing audience preferences to create customized posts",
        "Content Calendars and Automation": "A content calendar filled with scheduled posts managed by an automation tool",
        "Impact of Regular Posting on Brand Visibility": "A growing brand visibility chart due to regular social media posts",
        "Using Automation to Post on Multiple Platforms": "A concept of an AI managing posts on various social media platforms at once",
        "Saving Time by Automating WordPress and X Posts": "A digital clock with arrows pointing towards WordPress and X logos",
        "Advantages of Scheduling Posts Ahead of Time": "A calendar with scheduled posts marked in advance",
        "Automated Image Selection for Engaging Content": "A robot hand choosing vibrant images for social media posts",
        "Optimizing Content Generation with AI Agents": "An AI agent analyzing trends to optimize content generation",
        "How to Start Automating Social Media Posts": "A beginner's guidebook on automating social media posts",
        "Choosing the Right Tool for Social Media Automation": "A comparison chart of different social media automation tools"
}


    # Use the specific prompt for the topic or a fallback
    prompt = prompts.get(topic, f"A futuristic and immersive VR/AR scene focused on {topic}, with realistic holograms, high-tech environments, and user interaction.")
    print(f"Generated prompt: {prompt}")

    try:
        with autocast("cuda"):
            image = pipe(prompt).images[0]
        print("Image generated successfully.")
    except Exception as e:
        print(f"Error generating image: {e}")
        return

    # Save the generated image
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created 'images' directory.")

    image_path = "images/ai_gen_image.png"
    image.save(image_path)
    print(f"Image saved to {image_path}")

def gpt_generate_image(post_topic: str):
    """
    Generate an image related to the VR/AR topic using OpenAI's API.
    """
    logger.info(f"Generating an image related to topic: {post_topic}")
    
    # Map VR/AR topics to prompts
    prompt_map = {
        "Latest VR Headset Releases": "A sleek, modern VR headset with cutting-edge design, shown in a futuristic setting with digital lights and reflections.",
        "AR in Healthcare": "A doctor wearing AR glasses to assist in diagnosing a patient, with holographic displays of medical data around the doctor.",
        "VR Training Programs": "An immersive virtual reality training room, where participants are engaged in a VR simulation with controllers and headsets.",
        "Future of the Metaverse": "A colorful and interactive metaverse environment with avatars, digital buildings, and holographic displays showing virtual events.",
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
    topic = "Latest VR Headset Releases"  # Replace with desired topic or use input()
    main(topic)
