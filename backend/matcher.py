import re
from typing import Optional
from rapidfuzz import fuzz

# Common junk that shows up in YouTube video titles but isn't part of the song name
NOISE_PATTERNS = [
    r"\(official.*?\)",
    r"\[official.*?\]",
    r"\(lyrics?.*?\)",
    r"\[lyrics?.*?\]",
    r"\(audio.*?\)",
    r"\[audio.*?\]",
    r"\(visualizer.*?\)",
    r"\(4k.*?\)",
    r"\[4k.*?\]",
    r"\(hd.*?\)",
    r"official music video",
    r"official video",
    r"official audio",
    r"lyric video",
    r"music video",
    r"ft\..*",
    r"feat\..*",
    r"\|.*",
]


def clean_title(raw_title: str) -> str:
    """
    Strips common noise from a YouTube title so it's closer to
    a clean "artist - song" string before searching Spotify.
    """
    title = raw_title.lower()
    for pattern in NOISE_PATTERNS:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE)

    # Remove leftover brackets/parens and extra whitespace
    title = re.sub(r"[\(\)\[\]]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def find_best_match(cleaned_title: str, spotify_candidates: list) -> Optional[dict]:
    """
    Given a cleaned YouTube title and a list of Spotify track candidates
    (each with 'name', 'artist', 'uri'), returns the best match if it's
    confident enough, otherwise None.
    """
    best_score = 0
    best_candidate = None

    for candidate in spotify_candidates:
        candidate_string = f"{candidate['artist']} {candidate['name']}"
        score = fuzz.token_set_ratio(cleaned_title, candidate_string)
        if score > best_score:
            best_score = score
            best_candidate = candidate

    # Below this threshold, the match is too unreliable to trust
    CONFIDENCE_THRESHOLD = 60
    if best_score >= CONFIDENCE_THRESHOLD:
        return best_candidate
    return None
