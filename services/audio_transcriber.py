from utils.language_quality import is_valid_transcript

def transcribe_audio(video_path: str) -> str:
    import shutil
    from whisper import load_model

    if not shutil.which("ffmpeg"):
        raise Exception("FFmpeg is not installed or not in PATH.")

    try:
        model = load_model("base")
        result = model.transcribe(video_path)
        transcript = result["text"].strip()

        if not transcript:
            print("🔇 No speech detected.")
            return ""

        if not is_valid_transcript(transcript):
            print("🛑 Disregarded audio — likely song, gibberish, or non-English.")
            return ""

        return transcript

    except RuntimeError as e:
        if "Output file does not contain any stream" in str(e):
            print("⚠️ No audio stream found. Skipping.")
            return ""
        else:
            raise Exception(f"Whisper transcription failed: {str(e)}")
