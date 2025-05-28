import os
from utils.frame_extractor import extract_first_frame
from services.image_captioner import generate_caption
from services.audio_transcriber import transcribe_audio
from services.classifier import classify_caption_with_mistral
import traceback

def score_caption(text: str) -> float:
    words = text.strip().split()
    if len(words) < 20:
        return 0  # ✅ Ignore if < 20 words
    elif any(word in text.lower() for word in ["dm", "offer", "sale", "follow", "link in bio"]):
        return 0  # ✅ Ignore if promotional
    return 1.0  # ✅ Use only if long + useful


def score_audio(text: str) -> float:
    words = text.strip().split()
    if len(words) < 3:
        return 0
    elif len(words) < 10:
        return 0.5
    return 1.0

def score_image_caption(text: str) -> float:
    return 1.0 if len(text.strip().split()) > 3 else 0.5

def classify_reel_multimodal(video_path: str, original_caption: str = "") -> dict:
    os.makedirs("temp", exist_ok=True)
    temp_frame = "temp/frame.jpg"

    try:
        # Extract image frame and get image caption
        extract_first_frame(video_path, temp_frame)
        image_caption = generate_caption(temp_frame)

        # Transcribe audio
        audio_transcript = transcribe_audio(video_path)

        # Score inputs
        caption_score = score_caption(original_caption)
        image_score = score_image_caption(image_caption)
        audio_score = score_audio(audio_transcript)

        # Build smart prompt
        prompt = f"""You are a helpful AI that classifies Instagram reels into general 3-level categories for human browsing.

Use the inputs below and weigh them based on usefulness. Ignore any promotional or irrelevant content, especially from the caption.

Guidelines:
- Do NOT make classifications overly specific.
- Classify in a way that a regular human would — general, practical, and intuitive.
- For example, if a reel even *resembles* a gym video, classify it as:
  Category: Fitness
  Subcategory: Weightlifting
  Sub-sub-category: [relevant body part or routine]

Scores:
- Caption: {caption_score}
- Image: {image_score}
- Audio: {audio_score}

Inputs:
Caption: "{original_caption if caption_score else 'DISREGARDED (short/promotional)'}"
Image Description: "{image_caption}"
Audio Transcript: "{audio_transcript}"

Now classify the reel into the following format:
{{
  "category": "...",
  "sub_category": "...",
  "sub_sub_category": "..."
}}
"""

        print("📤 LLM Prompt:\n", prompt)


        # ❗ Call Mistral classification
        result = classify_caption_with_mistral(prompt)

        return {
            "classification": result,
            "weights": {
                "caption": caption_score,
                "image": image_score,
                "audio": audio_score
            },
            "context_used": {
                "caption": original_caption.strip(),
                "image_caption": image_caption,
                "audio_transcript": audio_transcript
            },
            "llm_prompt": prompt
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "classification": {
                "category": "Uncategorized",
                "sub_category": "Unknown",
                "sub_sub_category": "Fallback"
            },
            "error": str(e)
        }

    finally:
        if os.path.exists(temp_frame):
            os.remove(temp_frame)
