import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")


client = genai.Client(api_key=API_KEY)


MODEL_NAME = "gemini-2.0-flash"
MAX_CHARS = 6000         
RETRY_DELAY = 30          


def analyze_text(text: str) -> str:
    """
    Analyze long text safely using Gemini with chunking and quota handling.
    """

    if not text.strip():
        return "No text found in document."

    # Split text into chunks
    chunks = [
        text[i:i + MAX_CHARS]
        for i in range(0, len(text), MAX_CHARS)
    ]

    responses = []

    for idx, chunk in enumerate(chunks, start=1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=(
                    "Analyze the following document content and provide a clear summary:\n\n"
                    + chunk
                )
            )

            if response.text:
                responses.append(response.text)

        except ClientError as e:
            error_str = str(e)

            # Handle quota exceeded
            if "RESOURCE_EXHAUSTED" in error_str:
                print("Gemini quota exceeded. Waiting before retrying...")
                time.sleep(RETRY_DELAY)
                return (
                    "Gemini quota exceeded. "
                    "Please try again later or enable billing in Google Cloud."
                )

            
            elif "NOT_FOUND" in error_str:
                return (
                    "Gemini model not available. "
                    "Please verify model name or API access."
                )

            
            else:
                print("Gemini API error:", error_str)
                return "Error analyzing document. Please try again."

    
    return "\n\n".join(responses)

    
  















