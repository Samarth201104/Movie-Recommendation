from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from typing import List, Dict

app = Flask(__name__)
CORS(app)

# ==================== COMPREHENSIVE MOVIE DATASET ====================
# You can add poster URLs from Google Images later

MOVIES_DATASET = [
    # Hindi Movies
    {"id": 1, "title": "3 Idiots", "genre": "Comedy,Drama,Family", "language": "hindi", "rating": 8.4, "year": 2009, "overview": "Two friends search for their lost college buddy while reminiscing about their college days. A heartwarming tale of friendship and following your passion.", "poster_url": "https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssoloscw79z8Tew.jpg"},
    {"id": 2, "title": "Dangal", "genre": "Drama,Action,Biography", "language": "hindi", "rating": 8.8, "year": 2016, "overview": "A former wrestler trains his daughters to become world-class wrestlers, defying societal norms.", "poster_url": ""},
    {"id": 3, "title": "Zindagi Na Milegi Dobara", "genre": "Comedy,Drama,Romance", "language": "hindi", "rating": 8.2, "year": 2011, "overview": "Three friends take a road trip in Spain that changes their lives forever.", "poster_url": ""},
    {"id": 4, "title": "Andhadhun", "genre": "Thriller,Crime,Mystery", "language": "hindi", "rating": 8.5, "year": 2018, "overview": "A blind pianist witnesses a murder and gets entangled in a web of lies and deception.", "poster_url": ""},
    {"id": 5, "title": "Hera Pheri", "genre": "Comedy,Crime", "language": "hindi", "rating": 8.2, "year": 2000, "overview": "Three tenants try to make quick money but get caught in hilarious situations.", "poster_url": ""},
    {"id": 6, "title": "Gully Boy", "genre": "Drama,Music", "language": "hindi", "rating": 8.0, "year": 2019, "overview": "A young street rapper from Mumbai's slums rises to fame against all odds.", "poster_url": ""},
    {"id": 7, "title": "Drishyam", "genre": "Thriller,Mystery,Drama", "language": "hindi", "rating": 8.4, "year": 2015, "overview": "A simple family man uses his wits to protect his family from a police investigation.", "poster_url": ""},
    {"id": 8, "title": "Yeh Jawaani Hai Deewani", "genre": "Romance,Drama,Comedy", "language": "hindi", "rating": 7.7, "year": 2013, "overview": "A free-spirited girl reconnects with old friends on a life-changing trek.", "poster_url": ""},
    {"id": 9, "title": "Queen", "genre": "Comedy,Drama", "language": "hindi", "rating": 8.2, "year": 2014, "overview": "A woman goes on her honeymoon alone after her wedding is called off.", "poster_url": ""},
    {"id": 10, "title": "Tumbbad", "genre": "Horror,Fantasy,Thriller", "language": "hindi", "rating": 8.4, "year": 2018, "overview": "A man seeks a hidden treasure in a cursed village, facing ancient evil.", "poster_url": ""},
    {"id": 11, "title": "Kabir Singh", "genre": "Drama,Romance", "language": "hindi", "rating": 7.1, "year": 2019, "overview": "A brilliant but self-destructive surgeon spirals after his girlfriend marries someone else.", "poster_url": ""},
    {"id": 12, "title": "Stree", "genre": "Horror,Comedy", "language": "hindi", "rating": 7.8, "year": 2018, "overview": "A small town is haunted by a female ghost who abducts men at night.", "poster_url": ""},
    
    # English Movies
    {"id": 13, "title": "The Dark Knight", "genre": "Action,Thriller,Crime", "language": "english", "rating": 9.0, "year": 2008, "overview": "Batman faces his greatest enemy, the Joker, who wants to plunge Gotham into chaos.", "poster_url": ""},
    {"id": 14, "title": "Inception", "genre": "Action,Sci-Fi,Thriller", "language": "english", "rating": 8.8, "year": 2010, "overview": "A thief who steals corporate secrets through dream-sharing technology.", "poster_url": ""},
    {"id": 15, "title": "Joker", "genre": "Drama,Thriller", "language": "english", "rating": 8.8, "year": 2019, "overview": "A mentally troubled comedian descends into anarchy in Gotham City.", "poster_url": ""},
    {"id": 16, "title": "Interstellar", "genre": "Adventure,Drama,Sci-Fi", "language": "english", "rating": 8.6, "year": 2014, "overview": "A team of explorers travel through a wormhole in space to save humanity.", "poster_url": ""},
    {"id": 17, "title": "La La Land", "genre": "Romance,Drama,Music", "language": "english", "rating": 8.0, "year": 2016, "overview": "A jazz pianist and an aspiring actress fall in love while chasing their dreams.", "poster_url": ""},
    {"id": 18, "title": "The Pursuit of Happyness", "genre": "Drama,Biography", "language": "english", "rating": 8.0, "year": 2006, "overview": "A struggling salesman takes custody of his son as he pursues a stockbroker career.", "poster_url": ""},
    {"id": 19, "title": "Avengers: Endgame", "genre": "Action,Adventure,Sci-Fi", "language": "english", "rating": 8.4, "year": 2019, "overview": "The Avengers assemble for one final battle against Thanos.", "poster_url": ""},
    {"id": 20, "title": "The Shawshank Redemption", "genre": "Drama", "language": "english", "rating": 9.3, "year": 1994, "overview": "Two imprisoned men bond over several years, finding solace and eventual redemption.", "poster_url": ""},
    {"id": 21, "title": "Titanic", "genre": "Romance,Drama", "language": "english", "rating": 7.9, "year": 1997, "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "poster_url": ""},
    
    # Tamil Movies
    {"id": 22, "title": "Baahubali 2", "genre": "Action,Drama,Fantasy", "language": "tamil", "rating": 8.2, "year": 2017, "overview": "An epic tale of power, revenge, and a kingdom's destiny.", "poster_url": ""},
    {"id": 23, "title": "Vikram Vedha", "genre": "Action,Thriller,Crime", "language": "tamil", "rating": 8.4, "year": 2017, "overview": "A police officer hunts a gangster, blurring lines between good and evil.", "poster_url": ""},
    {"id": 24, "title": "Jai Bhim", "genre": "Drama,Crime", "language": "tamil", "rating": 8.9, "year": 2021, "overview": "A tribal man is falsely accused, and a lawyer fights for justice.", "poster_url": ""},
    {"id": 25, "title": "Soorarai Pottru", "genre": "Drama,Biography", "language": "tamil", "rating": 8.7, "year": 2020, "overview": "A common man dreams to make affordable airlines for the poor.", "poster_url": ""},
    {"id": 26, "title": "Master", "genre": "Action,Drama", "language": "tamil", "rating": 7.8, "year": 2021, "overview": "An alcoholic professor takes on a dangerous juvenile school.", "poster_url": ""},
    
    # Telugu Movies
    {"id": 27, "title": "RRR", "genre": "Action,Drama", "language": "telugu", "rating": 7.9, "year": 2022, "overview": "A fearless warrior faces his ultimate test in colonial India.", "poster_url": ""},
    {"id": 28, "title": "Pushpa: The Rise", "genre": "Action,Thriller", "language": "telugu", "rating": 7.6, "year": 2021, "overview": "A laborer rises in the red sandalwood smuggling world.", "poster_url": ""},
    {"id": 29, "title": "Arjun Reddy", "genre": "Drama,Romance", "language": "telugu", "rating": 8.0, "year": 2017, "overview": "A talented surgeon's life spirals after his girlfriend leaves him.", "poster_url": ""},
    {"id": 30, "title": "Ala Vaikunthapurramuloo", "genre": "Action,Comedy,Drama", "language": "telugu", "rating": 7.5, "year": 2020, "overview": "A young man discovers his true identity and fights for his place.", "poster_url": ""},
    
    # Marathi Movies
    {"id": 31, "title": "Sairat", "genre": "Drama,Romance", "language": "marathi", "rating": 8.3, "year": 2016, "overview": "A young couple from different castes fight for their love.", "poster_url": ""},
    {"id": 32, "title": "Natsamrat", "genre": "Drama,Family", "language": "marathi", "rating": 8.9, "year": 2016, "overview": "A legendary stage actor faces struggles in his old age.", "poster_url": ""},
    {"id": 33, "title": "Katyar Kaljat Ghusali", "genre": "Drama,Musical", "language": "marathi", "rating": 8.1, "year": 2015, "overview": "Two rival musicians compete for the throne of a kingdom.", "poster_url": ""},
    {"id": 34, "title": "Mumbai-Pune-Mumbai", "genre": "Romance,Comedy", "language": "marathi", "rating": 7.6, "year": 2010, "overview": "A chance meeting on a train leads to an unexpected romance.", "poster_url": ""},
    {"id": 35, "title": "Timepass", "genre": "Comedy,Romance", "language": "marathi", "rating": 7.4, "year": 2014, "overview": "A young man's journey through love and self-discovery.", "poster_url": ""},
    
    # Kannada Movies
    {"id": 36, "title": "KGF Chapter 2", "genre": "Action,Thriller", "language": "kannada", "rating": 8.3, "year": 2022, "overview": "The rise of a powerful gangster who rules the gold mines.", "poster_url": ""},
    {"id": 37, "title": "Kantara", "genre": "Action,Drama,Thriller", "language": "kannada", "rating": 8.6, "year": 2022, "overview": "A clash between man and nature reveals ancient secrets.", "poster_url": ""},
    {"id": 38, "title": "777 Charlie", "genre": "Adventure,Drama,Comedy", "language": "kannada", "rating": 8.7, "year": 2022, "overview": "A lonely factory worker bonds with a stray dog.", "poster_url": ""},
    
    # Malayalam Movies
    {"id": 39, "title": "Drishyam 2", "genre": "Thriller,Drama,Mystery", "language": "malayalam", "rating": 8.6, "year": 2021, "overview": "Six years later, Georgekutty faces new challenges.", "poster_url": ""},
    {"id": 40, "title": "Kumbalangi Nights", "genre": "Drama,Comedy,Family", "language": "malayalam", "rating": 8.5, "year": 2019, "overview": "Four brothers confront their differences and bond.", "poster_url": ""},
    {"id": 41, "title": "Premam", "genre": "Romance,Comedy,Drama", "language": "malayalam", "rating": 8.3, "year": 2015, "overview": "A man's journey through three stages of love.", "poster_url": ""},
    {"id": 42, "title": "Jana Gana Mana", "genre": "Thriller,Drama", "language": "malayalam", "rating": 8.4, "year": 2021, "overview": "A murder investigation unravels deep political conspiracies.", "poster_url": ""},
]

# ==================== MOOD TO GENRE MAPPING ====================
MOOD_GENRE_MAP = {
    "happy": ["comedy", "family", "music", "adventure"],
    "sad": ["drama", "romance", "biography"],
    "energetic": ["action", "thriller", "crime", "fantasy"],
    "romantic": ["romance", "drama", "family"],
    "thriller": ["thriller", "crime", "mystery", "horror"]
}

def filter_movies_by_criteria(mood: str = "", genre: str = "", language: str = "", exclude_ids: list = None) -> List[Dict]:
    """Filter movies based on mood, genre, language, and exclude favorites"""
    if exclude_ids is None:
        exclude_ids = []
        
    filtered_movies = MOVIES_DATASET.copy()
    
    # Exclude favorite movies
    if exclude_ids:
        filtered_movies = [m for m in filtered_movies if m["id"] not in exclude_ids]
    
    # Apply mood filter
    if mood:
        mood_key = mood.lower()
        allowed_genres = MOOD_GENRE_MAP.get(mood_key, ["comedy", "drama"])
        filtered_movies = [
            m for m in filtered_movies 
            if any(g.strip().lower() in allowed_genres for g in m["genre"].split(","))
        ]
    
    # Apply specific genre filter
    if genre:
        genre_lower = genre.lower()
        filtered_movies = [
            m for m in filtered_movies 
            if any(g.strip().lower() == genre_lower for g in m["genre"].split(","))
        ]
    
    # Apply language filter
    if language:
        filtered_movies = [m for m in filtered_movies if m["language"].lower() == language.lower()]
    
    # Sort by rating
    filtered_movies.sort(key=lambda x: float(x["rating"]), reverse=True)
    return filtered_movies[:12]

def get_personalized_recommendations(favorites: list) -> List[Dict]:
    """Generate personalized recommendations based on favorite movies"""
    if not favorites:
        return filter_movies_by_criteria(mood="happy")[:8]
    
    # Analyze favorite genres and languages
    fav_genres = []
    fav_languages = []
    
    for fav_id in favorites:
        movie = next((m for m in MOVIES_DATASET if m["id"] == fav_id), None)
        if movie:
            fav_genres.extend([g.strip().lower() for g in movie["genre"].split(",")])
            fav_languages.append(movie["language"])
    
    # Find most common genre and language
    from collections import Counter
    common_genre = Counter(fav_genres).most_common(1)[0][0] if fav_genres else "drama"
    common_language = Counter(fav_languages).most_common(1)[0][0] if fav_languages else "english"
    
    # Get recommendations based on favorite patterns
    recommendations = []
    
    # First, try to match the common genre
    genre_matches = [
        m for m in MOVIES_DATASET 
        if m["id"] not in favorites and 
        any(g.strip().lower() == common_genre for g in m["genre"].split(","))
    ]
    recommendations.extend(genre_matches[:6])
    
    # Then, try to match the common language
    if len(recommendations) < 8:
        lang_matches = [
            m for m in MOVIES_DATASET 
            if m["id"] not in favorites and 
            m["language"] == common_language and
            m not in recommendations
        ]
        recommendations.extend(lang_matches[:8 - len(recommendations)])
    
    # Finally, add top-rated movies
    if len(recommendations) < 8:
        top_rated = [
            m for m in MOVIES_DATASET 
            if m["id"] not in favorites and 
            m not in recommendations
        ]
        recommendations.extend(top_rated[:8 - len(recommendations)])
    
    return recommendations[:8]

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend_page():
    return render_template('recommend.html')

@app.route('/foryou')
def foryou_page():
    return render_template('foryou.html')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get movie recommendations based on filters"""
    try:
        data = request.get_json()
        mood = data.get('mood', '')
        genre = data.get('genre', '')
        language = data.get('language', '')
        
        movies = filter_movies_by_criteria(mood, genre, language)
        
        return jsonify({
            "success": True,
            "movies": movies,
            "count": len(movies)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/personalized', methods=['POST'])
def get_personalized():
    """Get personalized recommendations based on favorites"""
    try:
        data = request.get_json()
        favorites = data.get('favorites', [])
        
        recommendations = get_personalized_recommendations(favorites)
        
        return jsonify({
            "success": True,
            "movies": recommendations,
            "count": len(recommendations)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_movies():
    """Search movies by title"""
    try:
        data = request.get_json()
        query = data.get('query', '').lower().strip()
        
        if len(query) < 2:
            return jsonify({"success": True, "movies": []})
        
        results = [m for m in MOVIES_DATASET if query in m["title"].lower()]
        results.sort(key=lambda x: x["rating"], reverse=True)
        
        return jsonify({
            "success": True,
            "movies": results[:10]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎬 CineMood - Movie Recommendation System")
    print(f"📊 Loaded {len(MOVIES_DATASET)} movies")
    print("📝 Poster URLs are empty - Add them from Google Images")
    print("💡 To add poster URLs, edit the 'poster_url' field in MOVIES_DATASET")
    print("🌐 Server running at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)