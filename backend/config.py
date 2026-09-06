import os
from dotenv import load_dotenv

load_dotenv()

# YouTube Data API
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Spotify API
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")

SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8000/auth/spotify/callback")

# Where to send the browser back to after Spotify login completes
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")

# Spotify permissions our app needs
SPOTIFY_SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private"
