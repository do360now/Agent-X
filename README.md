# Automated X (Twitter) Poster with AI-Generated Content
This project is a Python script that automates posting tweets on X (formerly Twitter) at random intervals. It generates topics either from static lists or by scraping trending topics from trends24.in, creates engaging post content using a locally running Ollama model (gemma3:4b), and posts them using the Tweepy library. Images can optionally be attached if found in the images/ folder.

# Features
* Authenticates with X API v1.1 and v2 using OAuth 1.0a.
* Generates topics from trends (via web scraping) or a fallback static list.
* Uses Ollama with the gemma3:4b model to generate concise, engaging posts.
* Posts tweets with optional images.
* Runs in a loop with random delays between 1-3 hours.

# Prerequisites
* Python 3.8 or higher.
* A Twitter/X Developer Account with API keys (API Key, API Secret, Access Token, Access Secret). You need Elevated or higher access for posting.
* Ollama installed and running locally.
* An images/ folder (optional) for topic-related images.

# Installation
1. Clone the Repository
- `git clone https://github.com/yourusername/your-repo-name.git`
- `cd your-repo-name`

2. Set Up a Virtual Environment (recommended)
- `python -m venv .venv`
- `source .venv/bin/activate  # On Windows: .venv\Scripts\activate`

3. Install Python Dependencies
- Create a `requirements.txt` file with the following content:
- `tweepy==4.14.0  # Or latest version`
- `python-dotenv==1.0.0`
- `ollama==0.1.0  # Adjust based on actual package; if using ollama-python library`
- `requests==2.31.0`
- `beautifulsoup4==4.12.2`

Then install:
- `pip install -r requirements.txt`
-  Note: The `ollama` package might refer to the Python client for Ollama. If not installed via pip, ensure you have the Ollama API running.