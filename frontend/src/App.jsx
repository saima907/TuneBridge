import { useState, useEffect } from "react";
import PlaylistForm from "./components/PlaylistForm.jsx";
import ResultCard from "./components/ResultCard.jsx";
import { getSpotifyLoginUrl, convertPlaylist } from "./api.js";

export default function App() {
    const [youtubeUrl, setYoutubeUrl] = useState("");
  const [playlistName, setPlaylistName] = useState("");
  const [spotifyToken, setSpotifyToken] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // After Spotify login, the backend redirects back here with
  // ?spotify_token=... in the URL. Pick it up once, then clean the URL.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("spotify_token");
    if (token) {
      setSpotifyToken(token);
      window.history.replaceState({}, "", window.location.pathname);
    }
  }, []);

  async function handleConnectSpotify() {
    try {
      const url = await getSpotifyLoginUrl();
      window.location.href = url;
    } catch (err) {
      setError("Couldn't reach the server to start Spotify login.");
    }
  }

  async function handleConvert() {
    setError(null);
    setResult(null);
    setIsLoading(true);
    try {
      const data = await convertPlaylist(youtubeUrl, spotifyToken, playlistName);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

    return (
    <div className="page">
      <div className="header">
        <p className="title">Tunebridge</p>
        <p className="subtitle">Move a YouTube playlist to Spotify in one click</p>
      </div>

        <PlaylistForm
            youtubeUrl={youtubeUrl}
            setYoutubeUrl={setYoutubeUrl}
            playlistName={playlistName}
            setPlaylistName={setPlaylistName}
            onConvert={handleConvert}
            isConnected={!!spotifyToken}
            onConnectSpotify={handleConnectSpotify}
            isLoading={isLoading}
        />

      {error && <p className="error-text">{error}</p>}

      <ResultCard result={result} />
    </div>
  );
}
