import ConnectSpotify from "./ConnectSpotify.jsx";

export default function PlaylistForm({
  youtubeUrl,
  setYoutubeUrl,
  playlistName,
  setPlaylistName,
  onConvert,
  isConnected,
  onConnectSpotify,
  isLoading,
}) {
  return (
    <div className="glass-card">
      <label className="field-label">YouTube playlist link</label>
      <input
        type="text"
        className="text-input"
        placeholder="https://youtube.com/playlist?list=..."
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
      />

      <label className="field-label">Spotify playlist name</label>
      <input
        type="text"
        className="text-input"
        placeholder="e.g. My YouTube Playlist"
        value={playlistName}
        onChange={(e) => setPlaylistName(e.target.value)}
      />

      <ConnectSpotify isConnected={isConnected} onConnect={onConnectSpotify} />

      <button
        className="convert-btn"
        onClick={onConvert}
        disabled={!isConnected || !youtubeUrl || !playlistName || isLoading}
      >
        {isLoading ? "Converting..." : "Convert playlist"}
      </button>
    </div>
  );
}