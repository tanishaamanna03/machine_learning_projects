from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Datasets used: https://files.grouplens.org/datasets/movielens/ml-25m.zip

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


movies["clean_title"] = movies["title"].apply(clean_title)

vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf = vectorizer.fit_transform(movies["clean_title"])

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    return results

def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_movies():
    query = request.args.get('query', '')
    if len(query) < 3:
        return jsonify([])
    
    results = search(query)
    return jsonify(results[["movieId", "title", "genres"]].to_dict('records'))

@app.route('/recommend')
def recommend():
    movie_id = int(request.args.get('movieId'))
    recommendations = find_similar_movies(movie_id)
    return jsonify(recommendations.to_dict('records'))

import os
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Movie Recommendation Engine</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        .search-container { margin: 20px 0; }
        input { padding: 10px; width: 300px; font-size: 16px; }
        button { padding: 10px 15px; background: #4285f4; color: white; border: none; cursor: pointer; }
        .results { margin-top: 20px; }
        .movie-item { padding: 10px; margin: 5px 0; background: #f5f5f5; cursor: pointer; }
        .movie-item:hover { background: #e0e0e0; }
        .recommendations { margin-top: 30px; }
        .selected-movie { font-weight: bold; margin: 10px 0; padding: 10px; background: #e1f5fe; }
        .recommendation { padding: 8px; margin: 5px 0; background: #f9f9f9; }
        .score { color: #4285f4; font-weight: bold; }
    </style>
</head>
<body style="background: radial-gradient(circle, #ffc1e3, #ffe4f0);">
    <h1>Movie Recommendation Engine</h1>
    
    <div class="search-container">
        <input type="text" id="searchInput" placeholder="Enter movie title...">
        <button onclick="searchMovies()">Search</button>
    </div>
    
    <div class="results" id="searchResults"></div>
    
    <div class="selected-movie" id="selectedMovie" style="display: none;"></div>
    
    <div class="recommendations" id="recommendations"></div>

    <script>
        // Search for movies
        function searchMovies() {
            const query = document.getElementById('searchInput').value;
            if (query.length < 3) return;
            
            fetch(`/search?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('searchResults');
                    resultsDiv.innerHTML = '<h2>Search Results:</h2>';
                    
                    if (data.length === 0) {
                        resultsDiv.innerHTML += '<p>No results found</p>';
                        return;
                    }
                    
                    data.forEach(movie => {
                        const movieDiv = document.createElement('div');
                        movieDiv.className = 'movie-item';
                        movieDiv.innerHTML = `<strong>${movie.title}</strong> - ${movie.genres}`;
                        movieDiv.onclick = () => getRecommendations(movie.movieId, movie.title);
                        resultsDiv.appendChild(movieDiv);
                    });
                });
        }
        
        // Get recommendations for a movie
        function getRecommendations(movieId, title) {
            const selectedMovieDiv = document.getElementById('selectedMovie');
            selectedMovieDiv.style.display = 'block';
            selectedMovieDiv.innerHTML = `<h2>Selected Movie:</h2> ${title}`;
            
            fetch(`/recommend?movieId=${movieId}`)
                .then(response => response.json())
                .then(data => {
                    const recommendationsDiv = document.getElementById('recommendations');
                    recommendationsDiv.innerHTML = '<h2>Recommendations:</h2>';
                    
                    if (data.length === 0) {
                        recommendationsDiv.innerHTML += '<p>No recommendations found</p>';
                        return;
                    }
                    
                    data.forEach(movie => {
                        const recDiv = document.createElement('div');
                        recDiv.className = 'recommendation';
                        recDiv.innerHTML = `
                            <strong>${movie.title}</strong> - 
                            <span class="score">Score: ${movie.score.toFixed(2)}</span>
                            <br>${movie.genres}
                        `;
                        recommendationsDiv.appendChild(recDiv);
                    });
                });
        }
        
        // Add event listener for Enter key
        document.getElementById('searchInput').addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                searchMovies();
            }
        });
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("Movie Recommendation App is running at http://127.0.0.1:5000")
    app.run(debug=True)