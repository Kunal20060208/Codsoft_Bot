import requests
import os
from imdb import IMDb
from dotenv import load_dotenv

load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

ia = IMDb()

def fetch_imdb_movies(query, min_rating=0):
    try:
        results = ia.search_movie(query)
        filtered = []
        for movie in results[:10]:
            ia.update(movie)
            title = movie.get('title', 'Unknown Title')
            rating = movie.get('rating', 0)
            if rating and rating >= float(min_rating):
                year = movie.get('year', '')
                filtered.append(f"{title} ({year}) — Rating: {rating}")
            if len(filtered) >= 5:
                break
        return filtered if filtered else ["No IMDb movies matched the rating."]
    except Exception as e:
        return ["IMDb fetch error or unreachable."]

def fetch_books(query, min_rating=0):
    try:
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": query,
            "key": GOOGLE_BOOKS_API_KEY
        }
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        items = res.json().get("items", [])
        filtered = []
        for item in items:
            info = item.get("volumeInfo", {})
            title = info.get("title", "Unknown Title")
            authors = ", ".join(info.get("authors", [])) if "authors" in info else "Unknown Author"
            rating = info.get("averageRating", 0)
            if rating >= float(min_rating):
                filtered.append(f"{title} by {authors} — Rating: {rating}")
            if len(filtered) >= 5:
                break
        return filtered if filtered else ["No books matched the rating."]
    except Exception as e:
        return ["Google Books API error or unreachable."]

def fetch_products(query):
    try:
        url = "https://fakestoreapi.com/products"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        results = res.json()
        matches = [p["title"] for p in results if query.lower() in p["title"].lower()]
        return matches[:5] if matches else ["No products matched."]
    except Exception as e:
        return ["Product API error or unreachable."]

def recommend(query, category="movie", min_rating=0):
    if not query.strip():
        return ["Please enter something to search."]

    if category == "movie":
        return fetch_imdb_movies(query, min_rating)
    elif category == "book":
        return fetch_books(query, min_rating)
    elif category == "product":
        return fetch_products(query)
    else:
        return ["Invalid category."]
