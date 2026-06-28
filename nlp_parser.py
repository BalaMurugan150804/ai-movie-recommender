from google import genai
import json
import re
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def get_genre(text):

    text = text.lower()

    genres = {
        "sci-fi": "Sci-Fi",
        "science fiction": "Sci-Fi",
        "thriller": "Thriller",
        "drama": "Drama",
        "action": "Action",
        "horror": "Horror",
        "fantasy": "Fantasy",
        "crime": "Crime",
        "comedy": "Comedy",
        "romance": "Romance",
        "war": "War",
        "sports": "Sports",
        "animation": "Animation"
    }

    for key, value in genres.items():

        if key in text:
            return value

    return "Sci-Fi"

def get_pace(text):

    text = text.lower()

    if "slow" in text:
        return "Slow"

    if "medium" in text:
        return "Medium"

    if "fast" in text:
        return "Fast"

    return "Medium"

def get_runtime(text):
    
    text = text.lower()

    match = re.search(r"under\s+(\d+)\s*hours?",text)

    if match:
        return int(match.group(1))*60
    
    match = re.search(r"under\s+(\d+)\s*minutes?", text)

    if match:
        return int(match.group(1))
    
    return 180

def clean_query(text):

    text = text.lower()

    stop_words = [
        "i",
        "want",
        "a",
        "an",
        "the",
        "movie",
        "film",
        "about",
        "under",
        "hours",
        "hour",
        "minutes",
        "minute",
        "fast",
        "slow",
        "medium",
        "sci-fi",
        "science",
        "fiction"
    ]
    words = text.split()
    cleaned_words = []

    for word in words:
        cleaned_words.append(word)

    clean_query = []
    for word in cleaned_words:
        word = re.sub(r"[^a-z]","",word)
    if word:
        clean_query.append(word)

    return " ".join(clean_query)

def extract_preferences(user_text):

    if not user_text or not user_text.strip() or not any(c.isalpha() for c in user_text):
        st.warning("Please describe the movie you want.")
        
    return {
        "genre": get_genre(user_text),
        "pace": get_pace(user_text),
        "runtime": get_runtime(user_text),
        "query": clean_query(user_text)
    }


    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text

        text = text.replace("```json","")
        text = text.replace("```","")
        text = text.strip()

        return json.loads(text)
    
    except Exception:

        return{
        "genre": get_genre(user_text),
        "pace": get_pace(user_text),
        "runtime": get_runtime(user_text),
        "query": clean_query(user_text)
    }

    