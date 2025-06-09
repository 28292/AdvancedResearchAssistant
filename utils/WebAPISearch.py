import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")

def search_regulations(topic: str, agency_id: Optional[str] = None) -> str:
    """
    Search recent federal regulations by topic and optional agency (e.g., 'EPA').
    Returns formatted markdown string.
    """
    if not API_KEY:
        return "Missing REGULATIONS_GOV_API_KEY in environment."

    url = "https://api.regulations.gov/v4/documents"
    params = {
        "api_key": API_KEY,
        "filter[searchTerm]": topic,
        "sort": "-lastModifiedDate",
        "page[size]": 5
    }
    if agency_id:
        params["filter[agencyId]"] = agency_id

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            return f"🔍 No regulations found for topic: '{topic}'"

        output = f"📄 **Top Regulations for '{topic}':**\n\n"
        for doc in data["data"]:
            attr = doc["attributes"]
            output += f"- **Title**: {attr.get('title', 'No title')}\n"
            output += f"  - Type: {attr.get('documentType')}\n"
            output += f"  - Agency: {attr.get('agencyAcronym')}\n"
            output += f"  - Last Modified: {attr.get('lastModifiedDate')}\n"
            output += f"  - Comments: {attr.get('commentCount', 0)}\n"
            output += f"  - [View Document](https://www.regulations.gov/document/{doc['id']})\n\n"

        return output

    except Exception as e:
        return f"Error fetching regulations: {e}"
