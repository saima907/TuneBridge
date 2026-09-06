import re
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def extract_playlist_id(url: str) -> str:
    """Pulls the playlist ID out of a full YouTube playlist URL."""
    match = re.search(r"[?&]list=([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("That doesn't look like a valid YouTube playlist link.")
    return match.group(1)


def fetch_playlist_videos(playlist_url: str) -> list[dict]:
    """
    Returns a list of {title, video_id} for every video in the playlist.
    Handles pagination since a playlist can have more than 50 videos.
    """
    playlist_id = extract_playlist_id(playlist_url)
    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        ).execute()

        for item in response.get("items", []):
            snippet = item["snippet"]
            # Skip deleted/private videos, which show up with this placeholder title
            if snippet["title"] in ("Deleted video", "Private video"):
                continue
            videos.append({
                "title": snippet["title"],
                "video_id": snippet["resourceId"]["videoId"],
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos
