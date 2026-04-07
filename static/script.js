// Global variables
let selectedMood = '';
let selectedGenre = '';
let selectedLanguage = '';
let searchTimeout;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Mood buttons
    document.querySelectorAll('.mood-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedMood = this.dataset.mood;
            showToast(`${this.dataset.mood} mood selected!`, 'info');
        });
    });
    
    // Genre buttons
    document.querySelectorAll('.genre-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.genre-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedGenre = this.dataset.genre;
            if (selectedGenre) {
                showToast(`${selectedGenre} genre selected`, 'info');
            }
        });
    });
    
    // Language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedLanguage = this.dataset.lang;
            if (selectedLanguage) {
                showToast(`${selectedLanguage.toUpperCase()} language selected`, 'info');
            }
        });
    });
});

// Get recommendations
async function getRecommendations() {
    if (!selectedMood) {
        showToast('Please select a mood first!', 'warning');
        return;
    }
    
    const resultsSection = document.getElementById('resultsSection');
    const moviesGrid = document.getElementById('moviesGrid');
    
    resultsSection.style.display = 'block';
    moviesGrid.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i><br>Finding your perfect movies...</div>';
    
    try {
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mood: selectedMood,
                genre: selectedGenre,
                language: selectedLanguage
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.movies.length > 0) {
            displayMovies(data.movies, 'moviesGrid');
            document.getElementById('resultsCount').innerHTML = `${data.movies.length} movies found`;
            showToast(`Found ${data.movies.length} movies for you! 🎬`, 'success');
        } else {
            moviesGrid.innerHTML = '<div class="loading-spinner"><i class="fas fa-sad-tear"></i><br>No movies found. Try different filters!</div>';
            showToast('No movies found. Try different preferences!', 'info');
        }
    } catch (error) {
        console.error('Error:', error);
        moviesGrid.innerHTML = '<div class="loading-spinner"><i class="fas fa-exclamation-triangle"></i><br>Error loading movies. Please try again.</div>';
        showToast('Network error. Please try again!', 'error');
    }
}

// Display movies
function displayMovies(movies, containerId) {
    const container = document.getElementById(containerId);
    const favorites = getFavorites();
    
    if (!movies || movies.length === 0) {
        container.innerHTML = '<div class="loading-spinner"><i class="fas fa-film"></i><br>No movies to display</div>';
        return;
    }
    
    container.innerHTML = movies.map(movie => {
        const isFavorite = favorites.includes(movie.id);
        const posterUrl = movie.poster_url && movie.poster_url.trim() !== '' 
            ? movie.poster_url 
            : 'https://via.placeholder.com/300x450/1a1a2e/e50914?text=' + encodeURIComponent(movie.title);
        
        return `
        <div class="movie-card" data-movie-id="${movie.id}">
            <img src="${posterUrl}" alt="${movie.title}" onerror="this.src='https://via.placeholder.com/300x450/1a1a2e/e50914?text=${encodeURIComponent(movie.title)}'">
            <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleFavorite(${movie.id}, this, '${movie.title.replace(/'/g, "\\'")}')">
                <i class="fas fa-heart"></i>
            </button>
            <div class="movie-info">
                <h3>${movie.title}</h3>
                <div class="movie-meta">
                    <span><i class="fas fa-star"></i> ${movie.rating}</span>
                    <span><i class="fas fa-calendar"></i> ${movie.year}</span>
                </div>
                <div class="movie-meta">
                    <span><i class="fas fa-language"></i> ${movie.language.toUpperCase()}</span>
                    <span><i class="fas fa-tag"></i> ${movie.genre.split(',')[0]}</span>
                </div>
                <p class="movie-overview">${movie.overview.substring(0, 100)}...</p>
            </div>
        </div>
    `}).join('');
}

// Toggle favorite
function toggleFavorite(movieId, button, movieTitle) {
    let favorites = getFavorites();
    
    if (favorites.includes(movieId)) {
        // Remove from favorites
        favorites = favorites.filter(id => id !== movieId);
        button.classList.remove('active');
        showToast(`Removed "${movieTitle}" from favorites`, 'info');
    } else {
        // Add to favorites
        favorites.push(movieId);
        button.classList.add('active');
        showToast(`Added "${movieTitle}" to favorites! ❤️`, 'success');
    }
    
    localStorage.setItem('movieFavorites', JSON.stringify(favorites));
    updateFavoritesStats();
    
    // Refresh personalized recommendations if on foryou page
    if (window.location.pathname === '/foryou') {
        loadPersonalizedRecommendations();
    }
}

// Get favorites from localStorage
function getFavorites() {
    const favorites = localStorage.getItem('movieFavorites');
    return favorites ? JSON.parse(favorites) : [];
}

// Load personalized recommendations
async function loadPersonalizedRecommendations() {
    const favorites = getFavorites();
    const grid = document.getElementById('personalizedGrid');
    
    if (!grid) return;
    
    updateFavoritesStats();
    
    if (favorites.length === 0) {
        grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-heart-broken"></i><br>No favorites yet! Go to Explore page and like some movies to get personalized recommendations.</div>';
        return;
    }
    
    grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i><br>Analyzing your taste...</div>';
    
    try {
        const response = await fetch('/api/personalized', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ favorites: favorites })
        });
        
        const data = await response.json();
        
        if (data.success && data.movies.length > 0) {
            displayMovies(data.movies, 'personalizedGrid');
            showToast(`Found ${data.movies.length} personalized recommendations for you! 🎯`, 'success');
        } else {
            grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-film"></i><br>No recommendations found. Try adding more favorites!</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-exclamation-triangle"></i><br>Error loading recommendations</div>';
        showToast('Error loading recommendations', 'error');
    }
}

// Search movies with debounce
function debouncedSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const query = document.getElementById('searchInput').value;
        if (query.length >= 2) {
            searchMovies(query);
        } else if (query.length === 0) {
            // Clear results if search is empty
            const resultsSection = document.getElementById('resultsSection');
            if (resultsSection) {
                resultsSection.style.display = 'none';
            }
        }
    }, 500);
}

async function searchMovies(query) {
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success && data.movies.length > 0) {
            const resultsSection = document.getElementById('resultsSection');
            if (resultsSection) {
                resultsSection.style.display = 'block';
                displayMovies(data.movies, 'moviesGrid');
                document.getElementById('resultsCount').innerHTML = `Search results: ${data.movies.length} movies`;
                showToast(`Found ${data.movies.length} movies matching "${query}"`, 'success');
            }
        } else {
            const resultsSection = document.getElementById('resultsSection');
            if (resultsSection) {
                resultsSection.style.display = 'block';
                document.getElementById('moviesGrid').innerHTML = '<div class="loading-spinner"><i class="fas fa-search"></i><br>No movies found matching your search</div>';
            }
        }
    } catch (error) {
        console.error('Search error:', error);
        showToast('Error searching movies', 'error');
    }
}

// Show favorites modal
async function showFavoritesModal() {
    const favorites = getFavorites();
    const modal = document.getElementById('favoritesModal');
    const favoritesList = document.getElementById('favoritesList');
    
    if (favorites.length === 0) {
        favoritesList.innerHTML = '<div class="loading-spinner"><i class="fas fa-heart-broken"></i><br>No favorites yet. Go to Explore page and click the heart icon on movies you like!</div>';
    } else {
        favoritesList.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading your favorites...</div>';
        
        // Fetch all movies to get details
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood: '', genre: '', language: '' })
        });
        
        const data = await response.json();
        const favoriteMovies = data.movies.filter(m => favorites.includes(m.id));
        
        if (favoriteMovies.length === 0) {
            favoritesList.innerHTML = '<div class="loading-spinner"><i class="fas fa-exclamation-triangle"></i><br>Could not load favorite movies details</div>';
        } else {
            favoritesList.innerHTML = favoriteMovies.map(movie => {
                const posterUrl = movie.poster_url && movie.poster_url.trim() !== '' 
                    ? movie.poster_url 
                    : 'https://via.placeholder.com/60x90/1a1a2e/e50914?text=' + encodeURIComponent(movie.title);
                
                return `
                <div class="fav-item">
                    <img src="${posterUrl}" alt="${movie.title}" style="width: 60px; height: 90px; object-fit: cover; border-radius: 8px;" onerror="this.src='https://via.placeholder.com/60x90/1a1a2e/e50914?text=${encodeURIComponent(movie.title)}'">
                    <div class="fav-item-info">
                        <h4>${movie.title}</h4>
                        <p>${movie.genre} • ${movie.language.toUpperCase()} • ⭐ ${movie.rating}</p>
                        <p style="font-size: 0.8rem; color: #888;">${movie.year}</p>
                    </div>
                    <button class="remove-fav" onclick="removeFavorite(${movie.id}, '${movie.title.replace(/'/g, "\\'")}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            `}).join('');
        }
    }
    
    modal.style.display = 'flex';
}

// Remove favorite
function removeFavorite(movieId, movieTitle) {
    let favorites = getFavorites();
    favorites = favorites.filter(id => id !== movieId);
    localStorage.setItem('movieFavorites', JSON.stringify(favorites));
    showToast(`Removed "${movieTitle}" from favorites`, 'info');
    showFavoritesModal(); // Refresh modal
    updateFavoritesStats();
    
    // Refresh recommendations if on foryou page
    if (window.location.pathname === '/foryou') {
        loadPersonalizedRecommendations();
    }
}

// Close favorites modal
function closeFavoritesModal() {
    const modal = document.getElementById('favoritesModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Update favorites stats
function updateFavoritesStats() {
    const favorites = getFavorites();
    const favCountEl = document.getElementById('favCount');
    if (favCountEl) {
        favCountEl.textContent = favorites.length;
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.style.background = type === 'success' ? 'linear-gradient(135deg, #00c853, #00e676)' : 
                            type === 'error' ? 'linear-gradient(135deg, #d50000, #ff1744)' :
                            type === 'warning' ? 'linear-gradient(135deg, #ff6d00, #ff9100)' :
                            'linear-gradient(135deg, #1a1a2e, #16213e)';
    toast.style.borderLeftColor = type === 'success' ? '#00e676' : 
                                  type === 'error' ? '#ff1744' :
                                  type === 'warning' ? '#ff9100' : '#e50914';
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('favoritesModal');
    if (event.target === modal) {
        closeFavoritesModal();
    }
}