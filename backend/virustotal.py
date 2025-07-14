import httpx
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')  # Replace with your actual key

async def scan_url_virustotal(url: str) -> dict:
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }

    scan_url = "https://www.virustotal.com/api/v3/urls"

    try:
        async with httpx.AsyncClient() as client:
            # 1. Submit the URL for scanning
            response = await client.post(scan_url, headers=headers, data={"url": url})
            if response.status_code != 200:
                return {"error": f"Submit failed", "url": url}

            scan_data = response.json()
            analysis_id = scan_data["data"]["id"]

            # 2. Fetch the analysis result
            analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            result = await client.get(analysis_url, headers=headers)

            if result.status_code != 200:
                return {"error": "Analysis fetch failed", "url": url}


            return result.json()

    except Exception as e:
        return {"error": str(e), "url": url}

    
   