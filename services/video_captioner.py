from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import torch

# Load BLIP-2 model once
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_video_summary(frame_paths):
    images = [Image.open(f).convert("RGB") for f in frame_paths]
    prompt = "Describe this video in a short caption."

    inputs = processor(images=images, text=prompt, return_tensors="pt").to(device)
    generated_ids = model.generate(**inputs, max_new_tokens=50)
    caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    return caption
