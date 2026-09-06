from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import spotipy

import spotify_service
import youtube_service
from matcher import clean_title, find_best_match
from config import FRONTEND_URL

app = FastAPI(title="Tunebridge API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "Tunebridge backend is running"}


@app.get("/auth/spotify/login")
def spotify_login():
    """Frontend calls this to get the URL it should send the browser to."""
    return {"auth_url": spotify_service.get_login_url()}


@app.get("/auth/spotify/callback")
def spotify_callback(code: str):
    """
    Spotify redirects the browser here after the user logs in and approves access.
    We exchange the code for a token, then bounce the browser back to the
    frontend with that token attached so the frontend can store it.
    """
    access_token = spotify_service.exchange_code_for_token(code)
    return RedirectResponse(url=f"{FRONTEND_URL}?spotify_token={access_token}")


class ConvertRequest(BaseModel):
    youtube_url: str
    spotify_token: str
    playlist_name: str


@app.post("/convert")
def convert_playlist(payload: ConvertRequest):
    """
    The core pipeline: fetch YouTube videos -> clean titles -> search Spotify
    -> match -> create playlist -> add matched tracks.
    """
    try:
        videos = youtube_service.fetch_playlist_videos(payload.youtube_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not videos:
        raise HTTPException(status_code=400, detail="No videos found in that playlist.")

    spotify_client = spotipy.Spotify(auth=payload.spotify_token)

    matched_uris = []
    matched_titles = []
    unmatched_titles = []

    for video in videos:
        cleaned = clean_title(video["title"])
        candidates = spotify_service.search_track(spotify_client, cleaned)
        best_match = find_best_match(cleaned, candidates)

        if best_match:
            matched_uris.append(best_match["uri"])
            matched_titles.append(f"{best_match['artist']} - {best_match['name']}")
        else:
            unmatched_titles.append(video["title"])

    if not matched_uris:
        raise HTTPException(status_code=400, detail="Couldn't match any songs to Spotify tracks.")

    result = spotify_service.create_or_update_playlist(
        payload.spotify_token, payload.playlist_name, matched_uris
    )

    return {
        "playlist_url": result["playlist_url"],
        "created_new": result["created_new"],
        "newly_added_count": result["newly_added_count"],
        "skipped_duplicate_count": result["skipped_duplicate_count"],
        "total_videos": len(videos),
        "matched_count": len(matched_uris),
        "matched_titles": matched_titles,
        "unmatched_titles": unmatched_titles,
    }
