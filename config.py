import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")  
GITHUB_ORG = os.getenv("GITHUB_ORG", "default-org")
GITHUB_PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER", "10"))  


if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in the environment.")
