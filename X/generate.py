import os
import logging
import random
# import ollama
from authenticate import open_ai_auth, grok_ai_auth

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ai_client = open_ai_auth()
grok_client = grok_ai_auth()

# Function to generate VR/AR-specific topics
def generate_post_topic():
    """
    Generate a random topic for a tweet from a predefined list of automatic post agent-related topics.
    """
    topics = [
        "Benefits of Automating Social Media Posts",
        "How Content Automation Saves Time for Professionals",
        "Maximizing Engagement with Automated Posting Schedules",
        "Peak Hours for Social Media Engagement",
        "ROI on Social Media Automation Tools",
        "Consistency in Social Media Presence with Automation",
        "How Automated Posting Helps You Focus on Core Business Activities",
        "Best Practices for Automated Content Generation",
        "AI Tools for Consistent Social Media Growth",
        "Balancing Personal Touch and Automation in Social Media",
        "Customizing Automated Posts for Your Audience",
        "Content Calendars and Automation",
        "Impact of Regular Posting on Brand Visibility",
        "Using Automation to Post on Multiple Platforms",
        "Saving Time by Automating WordPress and X Posts",
        "Advantages of Scheduling Posts Ahead of Time",
        "Automated Image Selection for Engaging Content",
        "Optimizing Content Generation with AI Agents",
        "How to Start Automating Social Media Posts",
        "Choosing the Right Tool for Social Media Automation",
    ]
    topic = random.choice(topics)
    logger.info(f"Selected random topic: {topic}")
    return topic

def post_process_tweet(tweet):
    tweet = tweet[:250]
    if "#" not in tweet:
        tweet += " #VR #AR"  # Add default hashtags for VR and AR
    return tweet

def generate_tweet(topic):
    """
    Generate a post based on a dynamically generated VR/AR topic using Ollama.
    """
    logger.info(f"Generating a post based on the following topic: {topic}...")

    # Mapping topics to tweet prompts with VR/AR content
    prompts = {
        "Latest VR Headset Releases": "Create a post about the latest VR headset releases and include this link https://amzn.to/3Ahx4i9 focusing on new features, under 250 characters. Use hashtags like #VRHeadsets #TechTrends.",
        "AR in Healthcare": "Generate a tweet about how AR is transforming healthcare, under 250 characters. Include hashtags like #ARHealthcare #TechForGood.",
        "VR Training Programs": "Create a post on the use of VR in training programs for various industries, under 250 characters. Use hashtags like #VRTraining #FutureOfWork.",
        "Augmented Reality in Retail": "Write a post about how AR is being used to enhance the retail experience, include this link https://amzn.to/3Ahx4i9, under 250 characters. Use hashtags like #ARRetail #ShoppingTech.",
        "VR & AR in Education": "Describe how VR and AR are transforming the educational experience, under 250 characters. Include hashtags like #EdTech #FutureOfLearning.",
        "Future of the Metaverse": "Share a tweet on the potential future of the metaverse and its impact, under 250 characters. Include hashtags like #Metaverse #VirtualWorlds.",
        "Immersive VR Gaming": "Generate a tweet on the latest immersive VR gaming experiences, under 250 characters. Use hashtags like #VRGaming #Immersion.",
        "AR-Powered Navigation": "Describe how AR is revolutionizing navigation, with digital overlays and real-time directions. Include hashtags like #ARNavigation #TechInnovation.",
        "Using VR for Mental Health": "Create a tweet on the benefits of VR for mental health therapy, providing immersive relaxation and healing experiences. Include hashtags like #VRTherapy #MentalHealth.",
        "Innovations in Mixed Reality": "Share insights on recent innovations in mixed reality, merging the real and virtual worlds. Include hashtags like #MixedReality #Innovation.",
        "AR in Interior Design": "Talk about how AR is changing interior design, allowing users to visualize furniture and decor in real-time. Use hashtags like #ARInterior #HomeDesign.",
        "VR for Remote Work": "Describe how VR is enabling remote work collaboration with virtual workspaces, include this link https://amzn.to/3Ahx4i9, under 250 characters. Use hashtags like #RemoteWork #VRSpaces.",
        "Extended Reality Trends": "Provide a quick overview of the latest trends in Extended Reality (XR), combining AR, VR, and MR. Include hashtags like #XRTrends #FutureOfTech.",
        "Interactive AR Experiences": "Create a post on interactive AR experiences for entertainment and learning, under 250 characters. Use hashtags like #InteractiveAR #Tech.",
        "VR Hardware Comparisons": "Generate a tweet comparing different VR hardware options, focusing on features and performance. Use hashtags like #VRHardware #TechComparison.",
        "Real-World AR Use Cases": "Describe real-world applications of AR, such as navigation, retail, and healthcare, under 250 characters. Use hashtags like #ARApplications #FutureTech.",
        "Impact of VR in Therapy": "Generate a tweet on how VR is being used in therapy, from exposure therapy to virtual relaxation environments. Use hashtags like #VRTherapy #HealthTech.",
        "Metaverse Development Updates": "Share recent developments in the metaverse, including platform updates and new features, under 250 characters. Use hashtags like #MetaverseUpdates #VirtualWorld.",
        "Tips for VR Beginners": "Provide helpful tips for VR beginners, such as setup advice and must-try experiences. Use hashtags like #VRTips #GettingStarted. Include this link https://amzn.to/3Ahx4i9.",
        "How to Get Started with AR": "Offer guidance for beginners interested in AR, including app suggestions and basic setup tips. Use hashtags like #ARBasics #GettingStarted.",
        "VenezArt": "Generate a tweet on different variations of this introduction, Explore the boundless creativity of VenezArt Multimedia Corp. From animations to immersive gaming, graphic design, and custom apparel, we bring your vision to life. Include @venezart and keep it under 250 characters.",
    }

    content = prompts.get(topic, f"Create a short and engaging tweet on {topic}, related to VR or AR, under 250 characters. Include relevant hashtags like #VR or #AR.")
    
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": content}],
        )
        
        tweet = response["message"]["content"]
        tweet = post_process_tweet(tweet)
        logger.info(f"Generated tweet: {tweet}")
        return tweet

    except Exception as e:
        logger.error(f"Error generating tweet for topic '{topic}': {e}")
        return f"Could not generate tweet due to an error. Topic: {topic}"


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

def grok_generate_topic():
    """
    Generate a topic for a post based on what is currently trending with Bitcoin and has high engagement on X regarding venezuela.
    """
    logger.info("Generating a trending Bitcoin topic for a post using Grok AI...")

    # Prompt to generate a topic based on X trends
    topic_prompt = """
    Please identify a topic about Bitcoin that is currently trending on the X platform with high engagement. 
    The topic should be relevant for creating engaging posts. 
    Return just the topic name or a short phrase, without any additional context or hashtags.
    """

    try:
        completion = grok_client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "You are Grok, an AI designed to analyze trends on X."},
                {"role": "user", "content": topic_prompt},
            ],
        )

        # Extract the generated topic
        generated_topic = completion.choices[0].message
        if hasattr(generated_topic, 'content'):
            # Strip any leading/trailing whitespace and return just the topic
            topic = generated_topic.content.strip()
            logger.info(f"Topic generated successfully: {topic}")
            return topic
        else:
            logger.error("Failed to extract topic from the generated message.")
            return None

    except Exception as e:
        logger.error(f"An error occurred while generating the topic: {e}")
        return None
    
def grok_generate_post(post_topic):
    """
    Generate a post based on a dynamically generated topic using Grok AI, tailored to engaging with VenezArt posts.
    This version only returns the post content without any prefatory remarks.
    """
    logger.info(f"Generating a post about '{post_topic}' using Grok AI...")

    # Enhanced prompt to leverage current trends and popular engagement patterns
    prompt = f"""
    Based on the trending topic '{post_topic}' on X with high engagement:
    Generate a post related to it that:
    - Reflects these trends in style or content.
    - Is concise, eye-catching, and under 290 characters.
    - Includes relevant hashtags based on current trends.
    - Tag and engage relevant accounts to get them active in the discussion.
    - Asks the readers to Like and Repost.
    - Include my bitcoing address for donations. 17QxAMKK3tXeWCFukze9gDDGgHhGp4aG3j

    Keep the total post length of 300 characters. Do not include any introduction to the post.
    """
    post_topic = post_topic[:50]  # Limit the topic to 50 characters for the prompt
    try:
        completion = grok_client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "You are Grok, an AI designed to engage users with insightful and timely content."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract the generated content
        generated_message = completion.choices[0].message
        if hasattr(generated_message, 'content'):
            # Directly return the post content without any additional text
            logger.info("Post generated successfully.")
            return generated_message.content
        else:
            logger.error("Failed to extract content from the generated message.")
            return None

    except Exception as e:
        logger.error(f"An error occurred while generating the post: {e}")
        return None