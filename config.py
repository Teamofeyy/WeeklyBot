import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
MY_GITHUB_API_URL = os.getenv("MY_GITHUB_API_URL", "https://api.github.com")
MY_GITHUB_ORG = os.getenv("MY_GITHUB_ORG", "default-org")
MY_GITHUB_PROJECT_NUMBER = int(os.getenv("MY_GITHUB_PROJECT_NUMBER", "10"))


if not MY_GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in the environment.")
