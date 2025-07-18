import os
import logging
import random
import ollama
from typing import Optional, List
import requests
from bs4 import BeautifulSoup

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = "gemma3:4b"

STATIC_TOPICS = [
    "DevOps", "DevSecOps", "GitOps", "Infrastructure as Code", "Pipeline as Code",
    "CI/CD Pipeline", "Software Release Automation", "Continuous Integration",
    "Continuous Deployment", "joke of the day", "Azure DevOps", "Docker",
    "Bitbucket", "Jenkins", "Ansible", "Terraform", "HelmCharts", "MongoDB",
    "Artifactory repository", "Python code", "FastAPI", "Restful APIs", "Bitcoins",
    "Bitcoin portfolio", "Bitcoin price", "Bitcoin trading automation", "Behave test automation",
    "BDD Gherkin syntax", "TDD Test Driven Development", "Bitcoin Slots",
]

PROMPTS_MAP = {
    "Artificial Intelligence (AI)": "Share insights into the future of AI and how it is transforming industries. Include this link https://amzn.to/3NXPho7. Keep it under 280 characters with hashtags like #FutureTech and #AI.",
    "Machine Learning (ML)": "Include this link https://amzn.to/3NXPho7. Generate a tweet on the latest ML trends and best practices. Keep it concise with hashtags #ML and #DataScience.",
    "Cybersecurity": "Promote tips on enhancing cybersecurity for everyday users under 280 characters. Use hashtags like #Cybersecurity and #StaySafeOnline.",
    "Cloud Computing": "Discuss benefits of cloud adoption for businesses. Keep it under 280 characters, including hashtags #CloudTech and #Innovation.",
    "Blockchain & Cryptocurrency": "Create an engaging post on blockchain impact on finance. Keep it within 280 characters and add hashtags like #Blockchain and #CryptoNews.",
    "DevOps & CI/CD": "Share tips for seamless CI/CD in DevOps. Keep it brief with hashtags #DevOps and #CICD.",
    "Artificial Neural Networks (ANN) & Deep Learning": "Promote the benefits of ANNs and deep learning advancements. Limit to 280 characters with hashtags #DeepLearning and #AIResearch.",
    "Data Science & Data Analytics": "Discuss the importance of data-driven decisions. Keep it under 280 characters and add hashtags #DataScience and #Analytics.",
    "Python (Programming Language)": "Generate a post on Python tips for beginners under 280 characters. Use hashtags #PythonTips and #CodeNewbie. Mention this link for best python books: https://amzn.to/4f11fJC",
    "Tech Trends (2024)": "Share predictions for tech trends in 2024. Limit to 280 characters and include #TechTrends2024 and #Innovation.",
    "Robots & Automation": "Discuss the role of robotics in modern industries. Keep it under 280 characters with hashtags #Automation and #Robotics.",
    "Natural Language Processing (NLP)": "Promote NLP role in enhancing customer experience. Keep it brief with hashtags #NLP and #AI.",
    "HelloAI": "Create a snappy and engaging post promoting https://helloai.com, keep it under 280 characters. Highlight benefits of Automatic Post Generation using AI Agents. Use hashtags like #AIAutomation and #SmartPosting.",
    "VenezArt": "Generate a tweet on VenezArt Multimedia Corp services. Keep it under 280 characters, using hashtags like #Innovation, #Multimedia, and #VenezArt.",
    "Cutting-Edge Gadgets": "Share a captivating tweet promoting the latest tech gadget. Mention this link https://amzn.to/3Ahx4i9 as a top pick for tech enthusiasts. Use hashtags like #TechGadget and #AmazonFinds.",
    "joke of the day": "Share a light-hearted joke to brighten someone day. Keep it under 280 characters with hashtags #JokeOfTheDay and #LaughOutLoud.",
    "SemiConductors": "Generate a tweet on the latest SemiConductors trends and best practices. Keep it concise with hashtags #SemiConductors and #DataScience.",
    "Quantum Computing": "Promote the benefits of Quantum Computing advancements. Limit to 280 characters with hashtags #QuantumComputing and #AIResearch.",
    "Kubernetes": "Discuss the importance of Kubernetes in modern industries. Keep it under 280 characters with hashtags #Kubernetes and #DevOps.",
    "Docker": "Promote Docker role in enhancing software development. Keep it brief with hashtags #Docker and #DevOps.",
    "Behave test automation": "Generate a post explaining how to using BDD Gherkin syntax used in a TPS can also be used for creating test automation in CI/CD. Keep it concise.",
    "Bitcoin Slots": "Share a captivating tweet promoting the latest Bitcoin Slots version. Mention this link https://bitcoins.do360now.com/ as a top pick for Bitcoin enthusiasts.",
}

def get_trending_topics() -> List[str]:
    """
    Fetch trending topics from trends24.in using web scraping.

    Returns:
        List[str]: List of trending topic names.
    """
    url = "https://trends24.in/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        trends = []
        for ul in soup.find_all('ul', class_='trend-list'):
            for li in ul.find_all('li', class_='trend-item'):
                trend = li.text.strip().split(' ')[0]  # Get the topic name
                if trend not in trends:
                    trends.append(trend)
        logger.info(f"Fetched {len(trends)} trending topics.")
        return trends[:20]
    except Exception as e:
        logger.error(f"Error fetching trending topics from trends24.in: {e}")
        return []

def generate_topic() -> str:
    """
    Generate a topic by selecting from trending topics or fallback to static list.

    Returns:
        str: A selected topic.
    """
    trends = get_trending_topics()
    if trends:
        topic = random.choice(trends)
    else:
        if not STATIC_TOPICS:
            logger.error("Static topic list is empty. Cannot generate a topic.")
            raise ValueError("No topics available.")
        topic = random.choice(STATIC_TOPICS)
    logger.info(f"Selected topic: {topic}")
    return topic

def generate_post(topic: str) -> Optional[str]:
    """
    Generate a post based on the topic using local Ollama with gemma3:4b model.

    Returns:
        Optional[str]: The generated post content, or None if generation fails.
    """
    logger.info(f"Generating a post for topic: {topic}")

    # Check for specific prompt in map (case-insensitive match)
    prompt_key = next((k for k in PROMPTS_MAP if k.lower() == topic.lower()), None)
    if prompt_key:
        user_prompt = PROMPTS_MAP[prompt_key]
    else:
        user_prompt = (
            f"Generate exactly one snappy and engaging post on {topic}, offering tips or insights. "
            "Output only the post content itself, nothing else like introductions, options, or explanations. "
            "Keep the post under 250 characters. Add relevant hashtags. "
            "End with a call to action and ask users to like and repost."
        )

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI designed to create engaging X posts. Respond with only the post text."},
                {"role": "user", "content": user_prompt},
            ],
        )
        post_content = response['message']['content'].strip()

        # Post-process
        post_content = post_process(post_content)

        logger.info(f"Generated post: {post_content}")
        return post_content
    except Exception as e:
        logger.error(f"Error generating post with Ollama: {e}")
        return None

def post_process(post: str) -> str:
    """
    Post-process the generated tweet to ensure length and hashtags.

    Args:
        post (str): The generated post.

    Returns:
        str: Processed post.
    """
    # Remove any unwanted prefixes or multiple options if present
    lines = post.split('\n')
    if len(lines) > 1:
        # Take the first meaningful line
        post = next((line for line in lines if line.strip() and not line.startswith('**')), post)

    # Ensure within 280 characters
    if len(post) > 280:
        post = post[:277] + "..."

    # Ensure at least one hashtag
    if "#" not in post:
        post += " #News"

    return post

def find_image_for_topic(topic: str) -> Optional[str]:
    """
    Find an image that matches the topic from the images folder.

    Returns:
        Optional[str]: Path to the image if found, else None.
    """
    images_folder = "images/"
    logger.info(f"Searching for an image related to topic: {topic}")
    if not os.path.exists(images_folder):
        logger.error(f"Images folder '{images_folder}' does not exist.")
        return None

    for filename in os.listdir(images_folder):
        if topic.lower() in filename.lower():
            image_path = os.path.join(images_folder, filename)
            if os.path.isfile(image_path):
                logger.info(f"Found image for topic '{topic}': {image_path}")
                return image_path
    logger.info(f"No image found for topic: {topic}")
    return None

if __name__ == "__main__":
    # For testing
    pass