from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv
import os
import logging
from typing import Literal
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Campus Communication AI",
    description="API for generating professional academic communications",
    version="1.0.0"
)

# Configure CORS more securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load API key securely
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

client = genai.Client(api_key=api_key)

# Define valid options as enums
class CommunicationType(str):
    EMAIL = "Email"
    LEAVE_LETTER = "Leave Letter"
    PERMISSION_LETTER = "Permission Letter"
    NOTICE = "Notice"
    COMPLAINT_LETTER = "Complaint Letter"
    EVENT_ANNOUNCEMENT = "Event Announcement"
    WHATSAPP_MESSAGE = "WhatsApp Message"

class Tone(str):
    FORMAL = "Formal"
    PROFESSIONAL = "Professional"
    FRIENDLY = "Friendly"
    POLITE = "Polite"

class Length(str):
    SHORT = "Short"
    MEDIUM = "Medium"
    DETAILED = "Detailed"

class RequestData(BaseModel):
    type: str = Field(..., description="Type of communication")
    message: str = Field(..., min_length=5, max_length=1000, description="Situation description")
    tone: str = Field(..., description="Desired tone")
    length: str = Field(..., description="Desired length")

    class Config:
        schema_extra = {
            "example": {
                "type": "Email",
                "message": "I need permission to miss class tomorrow for a medical appointment",
                "tone": "Professional",
                "length": "Medium"
            }
        }

@app.get("/")
async def root():
    return {
        "message": "Campus Communication AI API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate (POST)"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/generate")
async def generate_text(data: RequestData):
    """
    Generate professional academic communication based on user input.
    """
    try:
        logger.info(f"Generating {data.type} with {data.tone} tone")
        
        # Enhanced prompt with better structure
        prompt = f"""
You are an expert campus communication assistant specializing in academic and professional writing.

Task: Generate a {data.type}

Context:
{data.message}

Requirements:
- Tone: {data.tone}
- Length: {data.length}
- Format: {get_format_instructions(data.type)}
- Purpose: Clear, professional, and appropriate for academic setting

Guidelines:
1. Use appropriate salutations and closings
2. Maintain consistent tone throughout
3. Include all necessary details from the context
4. Follow standard academic communication conventions
5. Ensure clarity and professionalism

Generate the communication:
"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if not response or not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")
        
        logger.info("Successfully generated communication")
        return {
            "output": response.text,
            "type": data.type,
            "tone": data.tone,
            "length": data.length,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error generating communication: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

def get_format_instructions(comm_type: str) -> str:
    """Get specific format instructions for different communication types"""
    formats = {
        "Email": "Include subject line, proper salutation, body, and signature",
        "Leave Letter": "Include date, recipient address, subject, reason, dates, and closing",
        "Permission Letter": "Include date, recipient, subject, clear request, reason, and closing",
        "Notice": "Include title, date, clear message, and issuing authority",
        "Complaint Letter": "Include date, recipient, subject, clear description of issue, and desired resolution",
        "Event Announcement": "Include event name, date, time, venue, and call to action",
        "WhatsApp Message": "Brief, conversational format suitable for instant messaging"
    }
    return formats.get(comm_type, "Standard professional format")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)