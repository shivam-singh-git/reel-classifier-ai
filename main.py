from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.reel_fetcher import fetch_reel_data
from services.classifier import classify_caption_with_mistral
from utils.clean_text import clean_caption
from services.reel_fusion_classifier import classify_reel_multimodal  # ✅ Updated import
from utils.download_video import download_video_from_url
import os
import traceback

app = FastAPI(title="Reel Classification API")

class ReelRequest(BaseModel):
    reel_url: str

class ClassificationResponse(BaseModel):
    category: str
    sub_category: str
    sub_sub_category: str

@app.get("/")
def root():
    return {"message": "Reel Classification API is up and running 🚀"}

@app.post("/classify-reel", response_model=ClassificationResponse)
def classify_reel(request: ReelRequest):
    try:
        # Step 1: Fetch metadata
        reel_data = fetch_reel_data(request.reel_url)

        if reel_data is None:
            raise HTTPException(status_code=500, detail="Failed to fetch reel data — result is None. Check your API key and quota.")

        caption = reel_data.get("caption", {}).get("text", "").strip()

        # Step 2: Always download video — it's needed for fusion
        video_url = reel_data["video_versions"][0]["url"]
        os.makedirs("temp", exist_ok=True)
        video_path = download_video_from_url(video_url, "temp/reel.mp4")

        # Step 3: Run fusion classification using all inputs
        classification_result = classify_reel_multimodal(video_path, original_caption=caption)

        # Step 4: Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)

        # Step 5: Return only the final category breakdown (as per response model)
        return classification_result["classification"]

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Run this file directly: `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
