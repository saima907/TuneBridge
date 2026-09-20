# Tunebridge

Converts a YouTube playlist into a Spotify playlist on your own account.

## How it works
1. Connect your Spotify account (one-time login).
2. Paste a YouTube playlist link.
3. Click Convert — the backend fetches the YouTube video titles, cleans them up,
   searches Spotify for the closest match, and creates a new playlist in your
   Spotify account with the matched tracks.

## ⚠️ Access Note: Spotify Developer Mode

TuneBridge uses the Spotify Web API in **development mode**. Under Spotify's current developer policy, this means:

- **Limited users:** Only **5 users** can connect their Spotify account to the app.
- **Approval required:** Each user must be **manually approved by the app owner**. Their Spotify account email has to be added to the app's User Management list before they can log in.
- **Owner needs Premium:** Spotify requires the app owner's account to have an active **Spotify Premium** subscription to keep the app working in development mode.

If you try to log in without being approved, Spotify's authorization will fail. This is a Spotify platform restriction, not a bug in the app.

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
