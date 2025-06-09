import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

#API_KEY = os.getenv("SERPAPI_API_KEY")
API_KEY = 'LvqFXqiMAPdQmrUrZqRvNuay'

def search_serpapi(query: str, num_results: int = 5) -> str:
    if not API_KEY:
        return "❌ Missing SERPAPI_API_KEY in environment."

    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": API_KEY,
            "num": num_results
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" not in results or not results["organic_results"]:
            return f"🔍 No results found for '{query}'."

        output = f"🌐 **Top Web Results for '{query}':**\n\n"
        for result in results["organic_results"]:
            title = result.get("title", "No Title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description available.")
            output += f"- [{title}]({link})\n  - {snippet}\n\n"

        return output

    except Exception as e:
        return f"❌ Web search failed: {e}"
