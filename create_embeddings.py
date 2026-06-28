import faiss
from movie_data import movies
from google import genai
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

embeddings = []

for movie in movies:

    text = (
        movie["title"]+
        ". "+
        movie["plot"]
    )

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    embeddings.append(
        response.embeddings[0].values
    )

embeddings_array = np.array(
    embeddings,
    dtype=np.float32
)

np.save(
    "movie_embeddings.npy",
    embeddings_array
)

dimension = embeddings_array.shape[1]
faiss.normalize_L2(embeddings_array)
index = faiss.IndexFlatIP(dimension)
index.add(embeddings_array)
faiss.write_index(
    index,
    "movie_index.faiss"
)

print("Embeddings saved!")
print("FAISS index saved!")

