export default function ResultCard({ result }) {
  if (!result) return null;

  const statusText = result.created_new
    ? `Created new playlist · ${result.newly_added_count} tracks added`
    : `Updated existing playlist · ${result.newly_added_count} new tracks added`;

  return (
    <div className="result-card">
      <div>
        <div className="result-text">{statusText}</div>
        {result.skipped_duplicate_count > 0 && (
          <div className="result-subtext">
            {result.skipped_duplicate_count} already in the playlist, skipped
          </div>
        )}
      </div>
      <a
        className="result-link"
        href={result.playlist_url}
        target="_blank"
        rel="noreferrer"
      >
        Open playlist ↗
      </a>
    </div>
  );
}