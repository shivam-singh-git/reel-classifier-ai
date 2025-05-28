import re
from spellchecker import SpellChecker

spell = SpellChecker()

def is_valid_transcript(text: str) -> bool:
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)  # Only 3+ letter words

    if not words or len(words) < 5:
        return False  # Too few usable words

    misspelled = spell.unknown(words)
    error_rate = len(misspelled) / len(words)

    # 🟡 Thresholds — tune as needed
    if error_rate > 0.5:
        return False  # Likely gibberish / non-English
    if len(" ".join(words)) / len(words) < 3.5:
        return False  # Word avg too short (e.g., "la la ya da boom")
    
    return True
