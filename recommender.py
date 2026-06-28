import time
import faiss
from movie_data import movies
from google import genai
import numpy as np
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set."
    )

client = genai.Client(api_key=api_key)

def keyword_search(query):

    tokenized_corpus = []

    for movie in movies:
        text = (
            movie["title"] + " " +
            movie["plot"]            
        ).lower()

        tokenized_corpus.append(
            text.split()
        )

    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    
    results = []
    for i, score in enumerate(scores):
        if score>0:
            results.append({
                "title": movies[i]["title"],
                "score": score
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    return results
            

def recommend_movies(
        genre,
        pace,
        runtime,
        query,
        top_k
):

    keyword_results = keyword_search(query)

    bm25_scores = {}
    for movie in keyword_results:
        bm25_scores[movie["title"]] = movie["score"]

    print("\nKeyword Results:\n")

    for movie in keyword_results[:5]:
        print(movie)

    print("Movies considered:", len(movies))

    # --------------------
    # Load FAISS index
    # --------------------
    index = faiss.read_index(
        "movie_index.faiss"
    )

    # --------------------
    # Query Embedding
    # --------------------
    if not query or not query.strip():
        return[], "No query provided"
    query_response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=query
    )

    query_embedding = np.array(
        [query_response.embeddings[0].values],
        dtype=np.float32
    )

    faiss.normalize_L2(query_embedding)

    # --------------------
    # FAISS Search
    # --------------------
    scores, indices = index.search(
        query_embedding,
        len(movies)
    )

    print("\nFAISS Results:\n")

    for i in range(10):
        movie_index = indices[0][i]

        print(
            movies[movie_index]["title"],
            f"{scores[0][i]:.4f}"
        )

    results = []

    # --------------------
    # Metadata Boosting
    # --------------------
    for i in range(len(indices[0])):

        movie_index = indices[0][i]

        movie = movies[movie_index]

        score = float(scores[0][i])

        bm25_score = bm25_scores.get(
            movie["title"],
            0
        )
        score += bm25_score * 0.02      

        if movie["genre"].lower() == genre:
            score += 0.05

        if movie["pace"].lower() == pace:
            score += 0.05

        if movie["runtime"] <= runtime:
            score += 0.05

        results.append({
            "title": movie["title"],
            "director": movie["director"],
            "runtime": movie["runtime"],
            "imdb": movie["imdb"],
            "plot": movie["plot"],
            "score": score
        })

    # --------------------
    # Sort Results
    # --------------------
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top_movies = results[:top_k]

    print("\nTop Recommendations:\n")

    for movie in top_movies:
        print(
            f"{movie['title']} : {movie['score']:.4f}"
        )

    # --------------------
    # Build Context
    # --------------------
    context = ""

    for movie in top_movies:
        context += (
            f"Title: {movie['title']}\n"
            f"Plot: {movie['plot']}\n\n"
        )

    # --------------------
    # Gemini Explanation
    # --------------------
    prompt = f"""
You are a movie recommendation expert.

Based on the user's query and the retrieved movies,
recommend the single best movie.

User Query:
{query}

Movies:
{context}

Explain why you chose the movie.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return top_movies, response.text

    except Exception as e:

        print(e)

        time.sleep(60)

        return(
            top_movies,
            "AI explanation disabled during development."
        )
    

