import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movies(query: str, language: str | None = None):
    """Search TMDB for movies matching the query."""
    params = {"api_key": TMDB_API_KEY, "query": query}
    if language:
        params["language"] = language

    resp = requests.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])


def get_movie_details(movie_id: int, language: str | None = None):
    """Get detailed information for a specific TMDB movie."""
    params = {"api_key": TMDB_API_KEY}
    if language:
        params["language"] = language

    resp = requests.get(f"{BASE_URL}/movie/{movie_id}", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
