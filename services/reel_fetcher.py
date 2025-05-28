from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()  # ✅ This must be called before using os.getenv


# load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

print(RAPIDAPI_KEY)
def extract_reel_code(reel_url: str) -> str:
    """
    Extract reel shortcode from a full Instagram URL.
    Example: https://www.instagram.com/reel/DIbdzBcT0lf/ => DIbdzBcT0lf
    """
    match = re.search(r"reel/([^/?]+)", reel_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Instagram Reel URL")

def fetch_reel_data(reel_url: str) -> dict:
    """
    Fetch Instagram reel metadata using the RapidAPI service.
    Accepts a full reel URL and extracts shortcode internally.
    """
    reel_code = extract_reel_code(reel_url)

    url = "https://instagram-scraper-stable-api.p.rapidapi.com/get_media_data.php"
    querystring = {
        "reel_post_code_or_url": f"https://www.instagram.com/reel/{reel_code}/?utm_source=ig_web_copy_link",
        "type": "reel"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch reel data: {response.status_code}, {response.text}")

