import requests
import spotipy
from typing import Optional
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPE,
)


def get_oauth_manager() -> SpotifyOAuth:
    """
    Creates the OAuth helper. cache_path=None means we don't rely on
    spotipy writing token files to disk -- we pass tokens around explicitly instead.
    """
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        cache_handler=MemoryCacheHandler(),
        show_dialog=True,
    )


def get_login_url() -> str:
    """Returns the URL to send the user to for Spotify login/consent."""
    return get_oauth_manager().get_authorize_url()


def exchange_code_for_token(code: str) -> str:
    """Swaps the OAuth 'code' Spotify sends back for a usable access token."""
    token_info = get_oauth_manager().get_access_token(code, as_dict=True)
    return token_info["access_token"]


def search_track(client: spotipy.Spotify, query: str, limit: int = 5) -> list[dict]:
    """Searches Spotify and returns simplified candidate track info."""
    results = client.search(q=query, type="track", limit=limit)
    candidates = []
    for track in results["tracks"]["items"]:
        candidates.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "uri": track["uri"],
        })
    return candidates


def find_playlist_by_name(access_token: str, playlist_name: str) -> Optional[dict]:
    """
    Looks through the user's own Spotify playlists for one whose name matches
    (case-insensitively). Returns its {id, url} if found, otherwise None.
    Paginates through all of the user's playlists since there could be many.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.spotify.com/v1/me/playlists?limit=50"

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for playlist in data["items"]:
            if playlist["name"].strip().lower() == playlist_name.strip().lower():
                return {
                    "id": playlist["id"],
                    "url": playlist["external_urls"]["spotify"],
                }

        url = data.get("next")  # Spotify gives us the next page's URL directly, or None

    return None


def get_existing_track_uris(access_token: str, playlist_id: str) -> set:
    """
    Returns the set of track URIs already in a playlist, so we know which
    ones to skip when adding -- avoids adding the same song twice on re-runs.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items?fields=items(item(uri)),next&limit=100"
    existing_uris = set()

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for entry in data["items"]:
                if entry.get("item"):  # guards against removed/unavailable tracks
                    existing_uris.add(entry["item"]["uri"])

        url = data.get("next")

    return existing_uris


def create_new_playlist(access_token: str, playlist_name: str) -> dict:
    """Creates a fresh, empty playlist and returns its {id, url}."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://api.spotify.com/v1/me/playlists",
        headers=headers,
        json={"name": playlist_name, "public": False},
    )
    response.raise_for_status()
    playlist = response.json()
    return {"id": playlist["id"], "url": playlist["external_urls"]["spotify"]}


def add_tracks_to_playlist(access_token: str, playlist_id: str, track_uris: list) -> None:
    """Adds tracks to a playlist, 100 at a time (Spotify's per-call limit)."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i + 100]
        response = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/items",
            headers=headers,
            json={"uris": batch},
        )
        response.raise_for_status()


def create_or_update_playlist(access_token: str, playlist_name: str, track_uris: list) -> dict:
    """
    Finds an existing playlist with this name, or creates a new one.
    Either way, only adds tracks that aren't already in it.

    Returns {playlist_url, newly_added_count, skipped_duplicate_count, created_new}.
    """
    existing = find_playlist_by_name(access_token, playlist_name)

    if existing:
        playlist_id = existing["id"]
        playlist_url = existing["url"]
        created_new = False
        already_in_playlist = get_existing_track_uris(access_token, playlist_id)
    else:
        new_playlist = create_new_playlist(access_token, playlist_name)
        playlist_id = new_playlist["id"]
        playlist_url = new_playlist["url"]
        created_new = True
        already_in_playlist = set()

    tracks_to_add = [uri for uri in track_uris if uri not in already_in_playlist]

    if tracks_to_add:
        add_tracks_to_playlist(access_token, playlist_id, tracks_to_add)

    return {
        "playlist_url": playlist_url,
        "created_new": created_new,
        "newly_added_count": len(tracks_to_add),
        "skipped_duplicate_count": len(track_uris) - len(tracks_to_add),
    }