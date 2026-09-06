export default function ConnectSpotify({ isConnected, onConnect }) {
  return (
    <div className="connect-row">
      <div className="connect-label">
        <span className="spotify-dot" />
        <span>Spotify account</span>
      </div>
      {isConnected ? (
        <span className="connected-badge">Connected</span>
      ) : (
        <button className="connect-btn" onClick={onConnect}>
          Connect
        </button>
      )}
    </div>
  );
}
