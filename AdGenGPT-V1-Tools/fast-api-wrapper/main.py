from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from openai import OpenAI
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import base64
import os
import io
import tempfile

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# FastAPI app
app = FastAPI(title="Image Generation API")


# Request model for text-to-image
class PromptRequest(BaseModel):
    prompt: str


# -----------------------------------------
# Endpoint 1: Generate Image with OpenAI
# -----------------------------------------
@app.post("/generate-image-openai")
async def generate_image_openai(request: PromptRequest):
    try:
        response = openai_client.images.generate(
            model="gpt-image-1",
            prompt=request.prompt,
            background="auto",
            n=1,
            quality="high",
            size="1536x1024",
            output_format="png",
            moderation="auto",
        )
        
        image_bytes = base64.b64decode(response.data[0].b64_json)
        
        return Response(
            content=image_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=generated_openai.png"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# Endpoint 2: Generate Image with Gemini
# -----------------------------------------
@app.post("/generate-image-gemini")
async def generate_image_gemini(request: PromptRequest):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=request.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="4K"
                ),
            )
        )
        
        text_response = None
        
        for part in response.parts:
            if part.text is not None:
                text_response = part.text
            elif image := part.as_image():
                # Save to temp file and read back
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    temp_path = tmp.name
                
                image.save(temp_path)
                
                with open(temp_path, 'rb') as f:
                    image_data = f.read()
                
                os.unlink(temp_path)
                
                return Response(
                    content=image_data,
                    media_type="image/png",
                    headers={"Content-Disposition": "attachment; filename=generated_gemini.png"}
                )
        
        if text_response:
            raise HTTPException(
                status_code=400, 
                detail=f"Gemini did not generate an image. Response: {text_response}"
            )
        
        raise HTTPException(status_code=500, detail="No response from Gemini")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# Endpoint 3: Generate with Subject Images (OpenAI)
# -----------------------------------------
@app.post("/generate-image-using-subject-image-openai")
async def generate_image_subject_openai(
    prompt: str = Form(...),
    images: list[UploadFile] = File(...)
):
    try:
        image_files = []
        for img in images:
            content = await img.read()
            # Create BytesIO and give it a name attribute for mimetype detection
            file_obj = io.BytesIO(content)
            file_obj.name = img.filename
            image_files.append(file_obj)
        
        response = openai_client.images.edit(
            model="gpt-image-1",
            image=image_files,
            prompt=prompt,
            input_fidelity="high"
        )
        
        image_bytes = base64.b64decode(response.data[0].b64_json)
        
        return Response(
            content=image_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=generated_openai_subject.png"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# Endpoint 4: Generate with Subject Images (Gemini)
# -----------------------------------------
@app.post("/generate-image-using-subject-image-gemini")
async def generate_image_subject_gemini(
    prompt: str = Form(...),
    aspect_ratio: str = Form(default="1:1"),
    resolution: str = Form(default="2K"),
    images: list[UploadFile] = File(...)
):
    try:
        # Build content list with prompt and images
        contents = [prompt]
        
        for img in images:
            content = await img.read()
            pil_image = Image.open(io.BytesIO(content))
            contents.append(pil_image)
        
        response = gemini_client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=resolution
                ),
            )
        )
        
        text_response = None
        
        for part in response.parts:
            if part.text is not None:
                text_response = part.text
            elif image := part.as_image():
                # Save to temp file and read back
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    temp_path = tmp.name
                
                image.save(temp_path)
                
                with open(temp_path, 'rb') as f:
                    image_data = f.read()
                
                os.unlink(temp_path)
                
                return Response(
                    content=image_data,
                    media_type="image/png",
                    headers={"Content-Disposition": "attachment; filename=generated_gemini_subject.png"}
                )
        
        if text_response:
            raise HTTPException(
                status_code=400, 
                detail=f"Gemini did not generate an image. Response: {text_response}"
            )
        
        raise HTTPException(status_code=500, detail="No response from Gemini")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------
# Health check
# -----------------------------------------
@app.get("/")
async def root():
    return {"status": "running", "message": "Image Generation API"}
