"""
Image generation using StableDiffusion
"""

from diffusers import StableDiffusionPipeline
import torch
from config import IMAGE_GENERATION_MODEL

# Determine the appropriate device, CUDA for Nvidia GPUs, MPS for Apple M1 and CPU for others
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    IMAGE_GENERATION_MODEL, torch_dtype=torch.float32, variant="fp16"
)
pipe.to(device)
if device == "mps":
    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()


def generate_image(description, output_file):
    image = pipe(description).images[0]
    image.save(output_file)
    print(f"Image saved as {output_file}")
    return output_file
