import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This needs to be called early, e.g., when the module is imported
# or at the start of your main application script.
# If FastAPI runs this, it might be loaded there.
# For individual agent testing, this is useful here.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(_project_root, '.env'))


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # This check is important. If the key isn't found,
    # the application shouldn't proceed or should warn loudly.
    print("Warning: GEMINI_API_KEY not found. AI features will not work.")
    # raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Using 1.5 flash as it's generally good and fast
        # You might need to adjust based on availability or preference.
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        gemini_model = None


def generate_gemini_response(prompt: str) -> str:
    if not gemini_model:
        return "Gemini model not initialized. Check API key and configuration."
    try:
        response = gemini_model.generate_content(prompt)
        # Accessing response.text directly is common for simple text generation
        # However, checking parts and feedback is more robust
        if response.parts:
            # Concatenate text from all parts if multiple exist
            return "".join(part.text for part in response.parts if hasattr(part, 'text'))
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
            return f"Response blocked: {response.prompt_feedback.block_reason_message or response.prompt_feedback.block_reason}"
        return "Sorry, I couldn't generate a response. The response was empty or unexpected."
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error communicating with Gemini API: {e}\n{traceback.format_exc()}")
        return "Sorry, I encountered an error trying to process your request with the AI model."

# This makes the function directly available when importing from agents
# e.g., from agents import generate_gemini_response
