from openai import OpenAI
import base64
from dotenv import load_dotenv
import os

# Load the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

result = client.images.edit(
    model="gpt-image-1",
    image=[open("logo.png", "rb"), open("product.png", "rb")],
    prompt="""       
            {
                "prompt": "Create a premium, minimal Ayurvedic product advertisement in the style of a modern D2C wellness brand. Use a soft warm beige or off-white background with subtle natural gradients. The layout follows a clean split composition: informational content on the left and the product bottle on the right.\n\nOn the right side, place a high-resolution amber glass bottle with a black ribbed cap. The bottle label must be sharp, readable, and accurate, featuring the Shivam Ayurveda logo, product name, dosage or quantity, and a Sanskrit verse at the bottom. The label color palette uses warm orange and cream tones with subtle botanical patterns. The bottle should appear realistic, well-lit, and slightly elevated from the background using a soft shadow.\n\nOn the left side, create a strong text hierarchy. At the top, place a small muted heading with the product category name. Below it, add a large elegant serif headline in warm orange that communicates the core benefit of the product. Beneath the headline, include a short descriptive paragraph in dark gray explaining the traditional Ayurvedic value and wellness support of the product in a compliant, non-medical tone.\n\nAdd a single, minimal line-art icon or abstract graphic behind or beside the text that visually represents the product benefit, such as energy, digestion, or joint wellness. The graphic should be outlined, soft orange, subtle, and non-distracting. Avoid clutter. Leave generous whitespace.\n\nPlace the Shivam Ayurveda logo at the bottom left corner. The overall aesthetic is calm, authentic, premium, and trustworthy, blending ancient Ayurvedic heritage with modern wellness design. The design must feel suitable for Instagram ads, website banners, and product landing pages.",

                "negative_prompt": "dark backgrounds, busy textures, cluttered layout, harsh shadows, unreadable text, incorrect branding, neon colors, plastic bottles, medical symbols, exaggerated health claims, watermarks, stock-photo look",

                "style": "premium modern Ayurvedic D2C advertisement",
                "lighting": "soft diffused studio lighting with warm tones",
                "composition": "text left, product right, high whitespace, balanced layout",
                "quality": "ultra high resolution, crisp typography, commercial-ready",
                "aspect_ratio": "1:1"
            }

            """,
    input_fidelity="high"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("woman_with_logo.png", "wb") as f:
    f.write(image_bytes)