import os
import torch
import logging
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from PIL import Image  # Import for image format conversion

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

def main():
    topic = "Entrepreneurship"  # Choose the topic here or generate it dynamically
    image_path = generate_image(topic)
    if image_path:
        logger.info(f"Image generated and saved at: {image_path}")
    else:
        logger.error("Image generation failed.")

def generate_image(topic):
    """
    Generate an AI-generated image based on the given topic using the Stable Diffusion model.
    Save the generated image as a PNG file in the 'images' directory.
    Return the path to the saved image file.
    """
    logger.info(f"Generating image for topic: {topic}")

    model_id = "stabilityai/stable-diffusion-2-1"
    logger.info(f"Loading model: {model_id}")

    if not torch.cuda.is_available():
        logger.error("CUDA not available. Please run on a system with CUDA support.")
        return None

    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        logger.info(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

    num_inference_steps = 30
    guidance_scale = 6

    # Updated prompts for each topic
    prompts = {
        "Benefits of Automating Social Media Posts": "Create an image of a futuristic lego robot managing multiple social media accounts simultaneously. The scene should convey a sense of advanced technology and global connectivity, with digital grid-like lines covering parts of the Earth. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        "How Content Automation Saves Time for Professionals": "Create an image of a futuristic AI Lego robot working on important tasks while another robot manages social media posts",
        "Maximizing Engagement with Automated Posting Schedules": "A pensil drawn image of a lego graph showing increased engagement over time due to optimized post scheduling. Use a color palette with dark blues, silvery grays, and bright whites, with electric glows highlighting key features to give a sci-fi, high-tech aesthetic.",
        
}


    # Use the specific prompt for the topic or a fallback
    prompt = prompts.get(topic, f"An image of {topic} for a blog post")
    logger.info(f"Generated prompt: {prompt}")

    try:
        with torch.amp.autocast('cuda', dtype=torch.float16):
            image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]
        logger.info("Image generated successfully.")    
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None

    # Convert image to RGB and save as JPEG
    if not os.path.exists("images"):
        os.makedirs("images")
        logger.info("Created 'images' directory.")

    image_path = "images/ai_gen_image.png"  # Save as PNG with .jpg extension
    # image = image.convert("RGB")  # Convert to RGB for JPEG compatibility
    image.save(image_path, format="PNG")  # Save the image as PNG
    logger.info(f"Image saved to {image_path} as PNG.")

    return image_path  # Return the path for further use

if __name__ == "__main__":
    main()
