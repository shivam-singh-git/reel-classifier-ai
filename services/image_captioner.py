from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path: str) -> str:
    """
    Generate a descriptive caption for an image.
    """
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")

    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)

    return caption

# if __name__ == "__main__":
#     path = r"C:\Users\shiva\Desktop\images.jpeg"  # Replace with your image filename
#     caption = generate_caption(path)
#     print("🖼️ Caption:", caption)
