import re

def clean_caption(caption: str, remove_emojis: bool = True) -> dict:
    """
    Clean caption text by:
    - Extracting hashtags
    - Removing hashtags from the main text
    - Optionally removing emojis and extra whitespace

    Returns:
        {
            "clean_text": "Wanna unlock the planche? Start here. Progressions: ...",
            "hashtags": ["#calisthenics", "#learn", "#facts"]
        }
    """
    if not caption:
        return {"clean_text": "", "hashtags": []}

    # Extract hashtags
    hashtags = re.findall(r"#\w+", caption)

    # Remove hashtags from the main text
    text_without_hashtags = re.sub(r"#\w+", "", caption)

    # Optional: Remove emojis
    if remove_emojis:
        text_without_hashtags = re.sub(
            r"[^\w\s,.!?;:()&@%$+-=/'\"]", "", text_without_hashtags
        )

    # Remove extra whitespace
    clean_text = re.sub(r"\s+", " ", text_without_hashtags).strip()

    return {
        "clean_text": clean_text,
        "hashtags": hashtags
    }
