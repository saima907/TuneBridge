# Tunebridge

Converts a YouTube playlist into a Spotify playlist on your own account.

## How it works
1. Paste a YouTube playlist link.
2. Connect your Spotify account (one-time login).
3. Click Convert — the backend fetches the YouTube video titles, cleans them up,
   searches Spotify for the closest match, and creates a new playlist in your
   Spotify account with the matched tracks.

## Tech stack
- Backend: Python, FastAPI, YouTube Data API, Spotify Web API (Spotipy), rapidfuzz
- Frontend: React (Vite), plain CSS

## Project structure
```
tunebridge/
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── youtube_service.py   # Fetches playlist videos
│   ├── spotify_service.py   # OAuth, search, playlist creation
│   ├── matcher.py           # Title cleaning + fuzzy matching
│   ├── config.py            # Loads API keys from .env
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   ├── api.js
    │   └── components/
    ├── index.html
    ├── package.json
    └── vite.config.js
```

See SETUP.md for step-by-step run instructions.
