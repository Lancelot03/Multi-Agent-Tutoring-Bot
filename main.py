# main.py
from fastapi import FastAPI, Request, HTTPException # Add HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# ... (existing imports and TutorAgent instantiation) ...
from agents.tutor_agent import TutorAgent

# Import tool classes
from tools.calculator import CalculatorTool
from tools.constants_look_up import ConstantsLookupTool
from tools.historical_figure_lookup import HistoricalFigureLookupTool
from tools.periodic_table_lookup import PeriodicTableLookupTool

app = FastAPI()

# Mount static files (for index.html)
current_dir = os.path.dirname(os.path.abspath(__file__))
static_files_dir = os.path.join(current_dir, "static")

if os.path.exists(static_files_dir):
    app.mount("/static", StaticFiles(directory=static_files_dir), name="static")
else:
    print(f"Warning: Static directory not found at {static_files_dir}. HTML frontend may not work.")

tutor_agent_instance = TutorAgent()

# Instantiate tools for direct access
calculator_tool = CalculatorTool()
constants_tool = ConstantsLookupTool()
figure_tool = HistoricalFigureLookupTool()
periodic_table_tool = PeriodicTableLookupTool()

class QueryRequest(BaseModel):
    query: str

class ToolInput(BaseModel):
    input_string: str

# --- Existing Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    index_html_path = os.path.join(static_files_dir, "index.html")
    if os.path.exists(index_html_path):
        with open(index_html_path, "r") as f:
            html_content = f.read()
        # Replace a placeholder in HTML with tool names for dynamic listing (optional)
        tool_names = ["Calculator", "Physics Constants", "Historical Figures", "Periodic Table"]
        # A simple way to pass data, more complex templating engines exist
        # For this example, we'll keep the tool list static in HTML or handle via JS fetch
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
        print(f"Error handling query '{user_query}': {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": "An internal server error occurred."}, status_code=500)

# --- New Tool Endpoints ---

@app.post("/tools/calculator")
async def use_calculator_tool(payload: ToolInput):
    try:
        result = calculator_tool.calculate(payload.input_string)
        return {"tool": "Calculator", "input": payload.input_string, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/constants")
async def use_constants_tool(payload: ToolInput):
    try:
        result = constants_tool.lookup(payload.input_string)
        return {"tool": "Physics Constants", "input": payload.input_string, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/historical_figures")
async def use_figure_tool(payload: ToolInput):
    try:
        result = figure_tool.lookup(payload.input_string)
        return {"tool": "Historical Figures", "input": payload.input_string, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/periodic_table")
async def use_periodic_table_tool(payload: ToolInput):
    try:
        result = periodic_table_tool.lookup_element(payload.input_string)
        return {"tool": "Periodic Table", "input": payload.input_string, "output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to list available tools (optional, for dynamic UI generation)
@app.get("/tools/list")
async def list_tools():
    return {
        "tools": [
            {"id": "calculator", "name": "Calculator", "description": "Performs basic arithmetic (e.g., '5 * 7')."},
            {"id": "constants", "name": "Physics Constants", "description": "Looks up physical constants (e.g., 'speed of light')."},
            {"id": "historical_figures", "name": "Historical Figures", "description": "Looks up brief info on figures (e.g., 'cleopatra')."},
            {"id": "periodic_table", "name": "Periodic Table", "description": "Looks up element info (e.g., 'carbon', 'O', or '6')."}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
