# 🎬 AI Movie Recommender

An AI-powered movie recommendation system that understands natural language and recommends movies using **Hybrid Retrieval (FAISS + BM25)**. The application combines semantic search, keyword search, AI-powered explanations, and live movie metadata to help users quickly discover movies that match their preferences.

---

## 📌 Problem Statement

Finding the perfect movie can often take longer than actually watching one. Users usually browse through hundreds of titles before finding something that matches their mood.

This project solves that problem by allowing users to describe the kind of movie they want in natural language, such as:

> *"I want a fast sci-fi movie under 2 hours about robots."*

The system understands the request and returns the most relevant recommendations with an AI-generated explanation.

---

## ✨ Features

* Natural Language Movie Search
* Hybrid Retrieval using **FAISS + BM25**
* AI-powered explanation for recommendations
* Live movie posters and metadata using **OMDb API**
* IMDb rating, runtime, genres, cast and director
* Clean and responsive Streamlit interface
* Input validation and error handling
* Cached API responses for better performance

---

## 🛠 Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Google Gemini
* Natural Language Processing

### Search & Retrieval

* FAISS
* BM25 Hybrid Search

### External APIs

* Gemini API
* OMDb API

### Development Tools

* Git
* GitHub
* VS Code

---

## 🏗 Architecture

```text
                    User
                      │
                      ▼
           Natural Language Query
                      │
                      ▼
          NLP Preference Extraction
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     BM25 Retrieval        FAISS Retrieval
          │                       │
          └───────────┬───────────┘
                      ▼
             Hybrid Re-ranking
                      ▼
         Top Movie Recommendations
                      ▼
          OMDb Metadata Enrichment
                      ▼
        Gemini AI Recommendation
                      ▼
           Streamlit User Interface
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_gemini_api_key
OMDB_API_KEY=your_omdb_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## 📷 Screenshots

> Add screenshots of the application here.

* Home Page
* Recommendation Cards
* AI Explanation
* Movie Posters

---

## 🔮 Future Improvements

* User authentication
* Search history
* Movie trailers
* Favorites and watchlist
* Voice-based movie search
* Multi-language support
* Community platform for cinephiles to share reviews, recommendations, ratings, and discussions

---

## 👨‍💻 Author

**Bala Murugan**

Built as a portfolio project to explore modern AI-powered recommendation systems using NLP, Hybrid Retrieval, and Generative AI.
