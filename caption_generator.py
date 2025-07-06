from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

def generate_caption(image_path, style="default"):
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")

        if style == "funny":
            generation_args = {
                "do_sample": True,
                "top_p": 0.9,
                "temperature": 1.2,
                "max_new_tokens": 40
            }
        elif style == "poetic":
            generation_args = {
                "do_sample": True,
                "top_k": 50,
                "temperature": 1.0,
                "max_new_tokens": 60
            }
        elif style == "detailed":
            generation_args = {
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.85,
                "max_new_tokens": 70
            }
        else:
            generation_args = {
                "do_sample": False,
                "max_new_tokens": 40
            }

        with torch.no_grad():
            output = model.generate(**inputs, **generation_args)

        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption

    except Exception as e:
        return f"Captioning Error: {str(e)}"
