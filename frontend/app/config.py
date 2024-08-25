import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve environment variables
# backend_url = os.environ.get("BACKEND_URL")
# backend_url = os.environ.get("BACKEND_URL")

backend_url = "http://localhost:8000"
domain = os.environ.get("DOMAIN")
posthog_key = os.environ.get("POSTHOG_API_KEY")

# Print the values to verify they are loaded correctly
# print(f"BACKEND_URL: {backend_url}")
# print(f"DOMAIN: {domain}")
# print(f"POSTHOG_API_KEY: {posthog_key}")