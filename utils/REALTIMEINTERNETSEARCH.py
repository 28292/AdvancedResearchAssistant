from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_API_KEY")

def search_serpapi(query: str, num_results: int = 5) -> str:
    if not api_key:
        return "❌ Missing SERPAPI_API_KEY in environment."
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": '4edfe3b58f4c65cf3f918255006dc37810abbc5c7fe973156b5ee1e01d5bb2cf',
            "num": num_results
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            return f"❌ API error: {results['error']}"

        if "organic_results" not in results or not results["organic_results"]:
            return f"🔍 No results found for '{query}'."

        output = f"🌐 **Top Web Results for '{query}':**\\n\\n"
        for result in results["organic_results"]:
            title = result.get("title", "No Title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description available.")
            output += f"- [{title}]({link})\n  - {snippet}\n\n"


        return output

    except Exception as e:
        return f"❌ Web search failed: {e}"
