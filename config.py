import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG= os.getenv("GITHUB_ORG")
GITHUB_PROJECT_NUMBER= int(os.getenv("GITHUB_PROJECT_NUMBER"))
GITHUB_API_URL = os.getenv("GITHUB_API_URL")