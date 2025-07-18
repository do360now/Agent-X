# Automated Twitter Post Bot

This project is an automated bot that generates and posts content to Twitter, using AI-generated topics and images. It uses various technologies, including Stable Diffusion for image creation, Tweepy for Twitter API interaction, and Ollama for generating tweets.

## Features
- **Automated Tweet Posting**: Uses Tweepy to post tweets with a configurable frequency.
- **AI-Generated Content**: Generates tweet topics and content using Ollama and GPT models.
- **Image Creation**: Generates accompanying images using Stable Diffusion for selected topics.

## Prerequisites
- Python 3.8 or higher.
- Twitter Developer account for API credentials.
- CUDA-compatible GPU (optional for faster image generation).
- Docker (for containerized deployment).
- Poetry (for managing dependencies).

## Installation
1. **Clone the repository**
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Use Poetry to install dependencies:
   ```sh
   poetry install
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   API_KEY=your_api_key
   API_SECRET=your_api_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_SECRET=your_access_secret
   ```

5. **Run the Application**
   To start the bot:
   ```sh
   python agent_x.py
   ```

## Usage
- The bot will automatically generate a new topic, tweet content, and image, and post it to your Twitter account at random intervals (between 1-2 hours).
- Logs are generated to help monitor the bot's activity.

## Docker Deployment
1. **Build Docker Image**
   ```sh
   docker build -t do360now/agent-x:1.0.0 .
   ```

2. **Run the Docker Container**
   ```sh
   docker run -d --env-file .env do360now/agent-x:1.0.0
   ```

## File Structure
- `agent_x.py`: Main script that handles authentication, tweet generation, and posting.
- `authenticate.py`: Contains functions for authenticating with Twitter APIs.
- `generate.py`: Generates topics and tweets using AI models.
- `image_generator.py`: Uses Stable Diffusion to generate images for the selected topics.

## Dependencies
- **Tweepy**: Twitter API integration.
- **Ollama**: Used for generating tweet content.
- **Stable Diffusion**: For generating images (via `diffusers`).
- **dotenv**: To manage environment variables.

## Notes
- Ensure you have the necessary permissions on your Twitter account to post content.
- The model used for image generation (`StableDiffusionPipeline`) may require a GPU for optimal performance.

## Contributing
Feel free to open issues or submit pull requests. Contributions are always welcome.

## License
MIT License. See `LICENSE` file for details.

