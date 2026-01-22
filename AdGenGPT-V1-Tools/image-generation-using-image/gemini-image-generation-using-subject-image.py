import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """
            
                    {
                        "prompt": "Create a modern Ayurvedic product advertisement for 'Shivam Ayurveda – Shuddha Shilajit Capsule' with an energy-focused theme. Use a clean white background with a split layout. On the right side, display a high-resolution amber glass bottle with a black ribbed lid. The full orange and cream label is clearly readable, including the Shivam Ayurveda logo, 'Shuddha Shilajit', '30 Capsule', and a Sanskrit verse.\n\nOn the left side, add a strong typographic hierarchy. A small heading at the top reads 'Shuddha Shilajit Capsule'. Below it, place a bold orange headline reading 'Pure Strength for Energy, Vitality & Stamina.' Beneath the headline, include a short paragraph explaining that Shilajit is traditionally valued in Ayurveda for supporting natural energy, strength, and daily vitality.\n\nBehind the text, add subtle outline graphics such as a lightning bolt and plus symbols in soft orange to symbolize energy and activation. Place the Shivam Ayurveda logo at the bottom left. The design is clean, dynamic, and motivating while remaining professional and compliant.",
                        "negative_prompt": "dark background, cluttered design, unreadable text, blurred label, incorrect branding, medical claims, aggressive visuals, neon colors, watermark",
                        "style": "clean D2C wellness advertisement",
                        "lighting": "soft studio lighting",
                        "composition": "text left, product right, ample white space",
                        "aspect_ratio": "1:1"
                    }

         """

aspect_ratio = "5:4" # "1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"
resolution = "2K" # "1K", "2K", "4K"


response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        prompt,
        Image.open('logo.png'),
        Image.open('product.png'),
        Image.open('sample.png')
        ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("office.png")