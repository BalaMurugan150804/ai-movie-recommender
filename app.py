import streamlit as st
from recommender import recommend_movies
from nlp_parser import extract_preferences
from omdb import get_movie_details

st.set_page_config(
  page_title="AI Movie Recommender",
  page_icon="🎞️",
  layout="wide"
)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align:center; margin-bottom:0;'>
        AI Movie Recommender
    </h1>

    <p style='text-align:center; color:gray; font-size:18px;'>
        Describe the movie you're looking for in natural language.
    </p>
    """,
    unsafe_allow_html=True
)

with st.sidebar:

    st.header("About")

    st.markdown("---")

    st.write(
        """
        Powered by

        • Natural Language Processing

        • Hybrid Search (FAISS + BM25)

        • Gemini AI

        • OMDb API
        """
    )

left, center, right = st.columns([1,6,1])
with center:
  
  user_request = st.text_area(
      "Describe the movie you want",
      height=140,
      placeholder="Example: A fast sci-fi movie under 2 hours about robots.",
      
)

top_k = st.slider(
  "Number of Recommendations",
  min_value=1,
  max_value=10,
  value=3
)
recommend = st.button(
  "Recommend",
  use_container_width=True
)



if recommend:
   
   if not user_request or not user_request.strip() or not any(c.isalpha() for c in user_request):
    st.warning("Please describe the movie you want.\n\n"
               "Example: I want a fast sci-fi movie about robots.")
    st.stop()
   else:    
    status = st.status(
      "Understanding your request...",
      expanded=True
    )
    preferences = extract_preferences(user_request)

    status.update(
      label="Searching movie database...",
      state="running"
    )

    top_movies, explanation = recommend_movies(
      preferences["genre"].lower(),
      preferences["pace"].lower(),
      preferences["runtime"],
      preferences["query"],
      top_k
    )
    status.update(
      label="Generating AI explanation...",
      state="running"
    )
    status.update(
        label="Done!",
        state="complete"
    )
    
    st.subheader("Top Recommendations")

    for movie in top_movies:
      with st.container(border=True):
        left,right = st.columns([1,3])
        with left:
          details = get_movie_details(
            movie["title"]
          )
          if details:
            st.image(
              details["Poster"],
              use_container_width=True
            )
          with right:
            year = details.get("Year","")
            st.markdown(
              f"### {movie['title']} ({year})"
            )
            genre = details.get("Genre","")
            st.caption(genre.replace(","," •"))
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
              st.caption("IMDb")
              st.markdown(f"**{movie['imdb']}**")

              st.caption(f"Director")
              st.markdown(f"**{movie['director']}**")

              actors = details.get("Actors","")
              st.caption("Cast")
              st.markdown(f"**{actors}**")

            with col2:
              st.caption("Runtime")
              st.markdown(f"**{movie['runtime']} min**")

              match = min(movie["score"] *100,100)

              st.caption("Match")
              st.progress(match / 100)
              st.markdown(f"**{match:.1f}% Match**")        
    
    st.markdown("---")

    st.caption(
        "Built with Python • Streamlit • Gemini • FAISS • BM25 • OMDb"
    )

    with st.expander(
      "Why these recommendations?",
      expanded=True
    ):
      st.write(explanation)