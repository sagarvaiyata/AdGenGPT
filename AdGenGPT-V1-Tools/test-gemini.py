import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Generate ima
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Vast cosmic nebula in deep space. Swirling purple and blue gas clouds with bright star clusters. Ethereal glow. Epic space photography. 16:9 cinematic composition. No planets visible.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"
        ),
    )
)

# Save the image
for part in response.parts:
    if image := part.as_image():
        image.save("cosmic_base.png")
        print("Image saved!")