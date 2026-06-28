import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OMDB_API_KEY environment variable is not set."
    )

@st.cache_data
def get_movie_details(title):
    url = f"http://www.omdbapi.com/?apikey=ca4af7db&t={title}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()

    if data["Response"] == "False":
        return None
    return data

