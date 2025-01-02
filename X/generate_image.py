import os
import torch
import logging
import base64
import requests
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from PIL import Image  # Import for image format conversion

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()
# Headers with encoded authorization for other requests.
# We'll update headers in the `upload_image_to_wordpress` function specifically to handle image uploads.

# Environment variables loaded as previously described
wordpress_url = os.getenv("WORDPRESS_URL")
username = os.getenv("WORDPRESS_USERNAME")
password = os.getenv("WORDPRESS_PASSWORD")

# Prepare the credentials for Basic Auth
auth_string = f"{username}:{password}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()


def main():
    topic = "Entrepreneurship"  # Choose the topic here or dynamically
    image_path = generate_image(topic)
    if image_path:
        print(f"Image generated and saved at: {image_path}")
    else:
        print("Image generation failed.")

    upload_image_to_wordpress(image_path)

def upload_image_to_wordpress(image_path):
    """ Upload an image to WordPress media library """
    url = f"{wordpress_url}/media"
    
    # Headers for the image upload, with Basic Auth and specific content type for the file
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Disposition": f"attachment; filename={os.path.basename(image_path)}"
    }

    # Open the file in binary mode
    try:
        with open(image_path, 'rb') as img_file:
            # Prepare the file for upload
            files = {
                'file': (os.path.basename(image_path), img_file, 'image/jpeg')
            }

            logger.info(f"Uploading image {os.path.basename(image_path)} to WordPress...")
            
            response = requests.post(url, headers=headers, files=files)
            
            # Check if the image was uploaded successfully
            if response.status_code == 201:
                response_json = response.json()
                image_url = response_json.get('source_url')
                image_id = response_json.get('id')  # Get the ID of the uploaded image
                logger.info(f"Image uploaded successfully: {image_url}")
                return image_url, image_id 
            else:
                logger.error(f"Failed to upload image: {response.status_code}, {response.text}")
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while uploading the image: {e}")

    return None, None


def generate_image(topic):
    print(f"Generating image for topic: {topic}")
    model_id = "stabilityai/stable-diffusion-2-1"
    print(f"Loading model: {model_id}")

    if not torch.cuda.is_available():
        print("CUDA not available. Please run on a system with CUDA support.")
        return None

    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    num_inference_steps = 50
    guidance_scale = 7.5

    # Updated prompts for each topic
    prompts = {
        "Benefits of Automating Social Media Posts": "Create an image of a futuristic lego robot managing multiple social media accounts simultaneously. The scene should convey a sense of advanced technology and global connectivity, with digital grid-like lines covering parts of the Earth. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        "How Content Automation Saves Time for Professionals": "Create an image of a futuristic AI Lego robot working on important tasks while another robot manages social media posts",
        "Maximizing Engagement with Automated Posting Schedules": "A pensil drawn image of a lego graph showing increased engagement over time due to optimized post scheduling. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        "Peak Hours for Social Media Engagement": "A 3D digital lego clock indicating peak engagement hours with social media icons. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        "ROI on Social Media Automation Tools": "A hand drawn graph of ROI growth as a result of using social media automation tools. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        "Consistency in Social Media Presence with Automation": "A 64 bit graphics of an AI robot consistently posting content on different social media platforms",
        "How Automated Posting Helps You Focus on Core Business Activities": "A 64 bit graphics style business owner focusing on core activities while automation manages social media",
        "Best Practices for Automated Content Generation": "A professional vertical infographic listing best practices, with numbered icons, headings, and short descriptions. Light minimalistic background, slight gradients, and business-like colors in blues and grays for a polished look.",
        "AI Tools for Consistent Social Media Growth": "A Lego image showing AI tools helping a plant grow, symbolizing consistent social media growth",
        "Balancing Personal Touch and Automation in Social Media": "A 64 bit image of an office like character adjusting automated posts to add a personal touch",
        "Customizing Automated Posts for Your Audience": "A marvel comics style cartoon of AI analyzing audience preferences to create customized posts",
        "Content Calendars and Automation": "A DC comics style  image of a calendar filled with scheduled posts",
        "Impact of Regular Posting on Brand Visibility": "A Marvel comics image of a growing brand visibility chart",
        "Using Automation to Post on Multiple Platforms": "An Lego AI agent managing posts on various social media platforms at once",
        "Saving Time by Automating WordPress and X Posts": "A Lego image of automatic post to X and WP sites",
        "Advantages of Scheduling Posts Ahead of Time": "A Marvel comics image of an AI agent scheduling posts in advance",
        "Automated Image Selection for Engaging Content": "Create Cyber Punk image of a futuristic robot hand choosing vibrant images for social media posts",
        "Optimizing Content Generation with AI Agents": "Create a Lego  image of a futuristic AI agent analyzing trends to optimize content generation",
        "How to Start Automating Social Media Posts": "An Lego image of beginner's guidebook on automating social media posts",
        "Choosing the Right Tool for Social Media Automation": "An 64 bit image of a social media video game"
}


    # Use the specific prompt for the topic or a fallback
    prompt = prompts.get(topic, f"An image of {topic} for a blog post")
    print(f"Generated prompt: {prompt}"
          )

    try:
        with torch.amp.autocast('cuda', dtype=torch.float16):
            image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]
        print("Image generated successfully.")
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

    # Convert image to RGB and save as JPEG
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created 'images' directory.")

    image_path = "images/ai_gen_image.png"  # Save as PNG with .jpg extension
    # image = image.convert("RGB")  # Convert to RGB for JPEG compatibility
    image.save(image_path, format="PNG")  # Save the image as PNG
    print(f"Image saved to {image_path} as PNG.")

    return image_path  # Return the path for further use

if __name__ == "__main__":
    main()
