import re

# Subset of BCP 47: language, optional script, optional region.
_LOCALE_PATTERN = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|\d{3}))?$")

_LOCALE_NAMES = {
    "en": "English",
    "en-US": "American English",
    "en-GB": "British English",
    "en-AU": "Australian English",
    "en-CA": "Canadian English",
    "en-IN": "Indian English",
    "de": "German",
    "de-DE": "German (Germany)",
    "de-AT": "Austrian German",
    "de-CH": "Swiss German",
    "fr": "French",
    "fr-FR": "French (France)",
    "fr-CA": "Canadian French",
    "es": "Spanish",
    "es-ES": "European Spanish",
    "es-MX": "Mexican Spanish",
    "pt": "Portuguese",
    "pt-BR": "Brazilian Portuguese",
    "pt-PT": "European Portuguese",
    "it": "Italian",
    "it-IT": "Italian (Italy)",
    "nl": "Dutch",
    "nl-NL": "Dutch (Netherlands)",
    "da": "Danish",
    "da-DK": "Danish (Denmark)",
    "sv": "Swedish",
    "sv-SE": "Swedish (Sweden)",
    "nb": "Norwegian Bokmål",
    "nb-NO": "Norwegian Bokmål (Norway)",
    "fi": "Finnish",
    "fi-FI": "Finnish (Finland)",
}


def normalize_locale(raw: str) -> str:
    """Validate a locale code and normalize its casing (e.g. "en_gb" -> "en-GB")."""
    code = raw.strip().replace("_", "-")
    if not _LOCALE_PATTERN.match(code):
        raise ValueError(
            f"Invalid language code: {raw!r}. Expected a locale code such as 'en-US', "
            f"'en-GB', or a bare language like 'de'."
        )

    parts = code.split("-")
    parts[0] = parts[0].lower()
    for index, part in enumerate(parts[1:], start=1):
        # A four-letter subtag is a script (Latn); anything else here is a region.
        parts[index] = part.title() if len(part) == 4 else part.upper()
    return "-".join(parts)


def describe_locale(code: str) -> str:
    """Human-readable name for a normalized locale, falling back to the code itself."""
    if code in _LOCALE_NAMES:
        return _LOCALE_NAMES[code]
    language = code.split("-")[0]
    return _LOCALE_NAMES.get(language, code)
