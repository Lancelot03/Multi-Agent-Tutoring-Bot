from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# Ensure .env is loaded. agents/__init__.py should handle this if it's imported early.
# If not, uncomment and adjust:
# from dotenv import load_dotenv
# load_dotenv()

from agents.tutor_agent import TutorAgent # This import should trigger .env loading via agents/__init__.py

app = FastAPI()

# Mount static files (for index.html)
# Ensure the 'static' directory exists at the same level as main.py
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
static_files_dir = os.path.join(current_dir, "static")

if os.path.exists(static_files_dir):
    app.mount("/static", StaticFiles(directory=static_files_dir), name="static")
else:
    print(f"Warning: Static directory not found at {static_files_dir}. HTML frontend may not work.")


tutor_agent_instance = TutorAgent()

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    # Serve the index.html file
    # Ensure index.html is in a 'static' directory next to main.py
    index_html_path = os.path.join(static_files_dir, "index.html")
    if os.path.exists(index_html_path):
        with open(index_html_path, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>AI Tutor Agent</h1><p>Static file 'index.html' not found.</p>")


@app.post("/ask")
async def ask_tutor(request: QueryRequest):
    user_query = request.query
    if not user_query:
        return JSONResponse(content={"error": "Query cannot be empty"}, status_code=400)
    
    try:
        response = tutor_agent_instance.handle_query(user_query)
        return JSONResponse(content={"query": user_query, "answer": response})
    except Exception as e:
        # Log the error for server-side debugging
        print(f"Error handling query '{user_query}': {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": "An internal server error occurred."}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    # To run: uvicorn main:app --reload
    # Or from this script: python main.py (will use port 8000 by default with uvicorn.run)
    uvicorn.run(app, host="0.0.0.0", port=8000)
