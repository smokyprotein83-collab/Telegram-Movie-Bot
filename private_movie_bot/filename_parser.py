import os
import re
from typing import Any

RESOLUTIONS = ["480p", "720p", "1080p", "2160p"]
RESOLUTION_RANK = {res.lower(): i for i, res in enumerate(RESOLUTIONS)}

SOURCES = ["CAM", "TELESYNC", "HDRIP", "WEB-DL", "BLU-RAY"]
SOURCE_RANK = {re.sub(r'[\s\-]', '', src): i for i, src in enumerate(SOURCES)}

LANGUAGES = {
    "malayalam": ["malayalam", "ml"],
    "tamil": ["tamil", "ta"],
    "hindi": ["hindi", "hi"],
    "english": ["english", "en"],
}


def parse_filename(name: str) -> dict[str, Any]:
    """Extract resolution, source, and languages from a filename or caption."""
    text = name.upper()
    normalized = re.sub(r'[\s\-]', '', text)

    resolution = None
    for res in RESOLUTIONS:
        if res.upper() in text:
            resolution = res
            break

    source = None
    for src in SOURCES:
        normalized_src = re.sub(r'[\s\-]', '', src)
        if normalized_src in normalized:
            source = src
            break

    detected_languages = []
    for lang, aliases in LANGUAGES.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias.upper()) + r'\b'
            if re.search(pattern, text):
                detected_languages.append(lang)
                break

    return {
        "resolution": resolution,
        "source": source,
        "languages": detected_languages,
    }


def matches_constraints(
    filename: str,
    lang: str | None,
    max_quality: str | None,
    max_res: str | None,
) -> bool:
    """Check if a filename matches the given language, quality, and resolution constraints."""
    parsed = parse_filename(filename)

    if lang:
        if lang.lower() not in [l.lower() for l in parsed["languages"]]:
            return False

    if max_res:
        max_res_lower = max_res.lower()
        if parsed["resolution"] is None:
            return False
        if RESOLUTION_RANK.get(parsed["resolution"].lower(), -1) > RESOLUTION_RANK.get(max_res_lower, -1):
            return False

    if max_quality:
        max_quality_normalized = re.sub(r'[\s\-]', '', max_quality.upper())
        max_quality_rank = SOURCE_RANK.get(max_quality_normalized, -1)
        if max_quality_rank == -1:
            return False
        if parsed["source"] is None:
            return False
        source_normalized = re.sub(r'[\s\-]', '', parsed["source"])
        source_rank = SOURCE_RANK.get(source_normalized, -1)
        if source_rank > max_quality_rank:
            return False

    return True
