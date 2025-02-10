'''
Image generation using StableDiffusion
'''

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
from config import STABLE_DIFFUSION_MODEL

#Function to generate the character image based on description 
def generate_character_image(description, output_file="assets/character.png"):
    pipe = StableDiffusionPipeline.from_pretrained(STABLE_DIFFUSION_MODEL)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    image = pipe(description).images[0]
    image.save(output_file)
    print(f"Character image saved as {output_file}")
    return output_file  # Return the image path

#Function to generate the map image based on description
def generate_map(description, output_file="assets/map.png"):
    pipe = StableDiffusionPipeline.from_pretrained(STABLE_DIFFUSION_MODEL)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    image = pipe(description).images[0]
    image.save(output_file)
    
    print(f"Map generated and saved at {output_file}")
    return output_file  # Return the image path