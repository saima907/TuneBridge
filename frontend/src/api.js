const API_BASE = "http://127.0.0.1:8000";

export async function getSpotifyLoginUrl() {
  const res = await fetch(`${API_BASE}/auth/spotify/login`);
  const data = await res.json();
  return data.auth_url;
}

export async function convertPlaylist(youtubeUrl, spotifyToken, playlistName) {
  const res = await fetch(`${API_BASE}/convert`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      spotify_token: spotifyToken,
      playlist_name: playlistName,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Something went wrong during conversion.");
  }

  return data;
}
