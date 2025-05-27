# Multi-Agent-Tutoring-Bot

This project implements an AI-powered tutoring assistant based on multi-agent system principles. The "Tutor Agent" delegates questions to specialized sub-agents (Math Agent, Physics Agent), which can use tools (like a calculator or a constants lookup) and the Gemini API to provide answers.

**Live Deployed Application:** [Link to be added after deployment]

## Architecture

The system follows a multi-agent architecture:

1.  **User Interface (FastAPI Web App):** Provides a simple web page or API endpoint for users to submit natural language queries.
2.  **Tutor Agent (Main Agent):**
    *   Receives the user's query.
    *   Uses the Gemini API to classify the query's subject (Math, Physics, General).
    *   Delegates the query to the appropriate specialist sub-agent.
    *   Returns the sub-agent's response to the user.
3.  **Sub-Agents (Specialist Agents):**
    *   **Math Agent:** Handles mathematics-related questions.
        *   **Tool:** Uses a `CalculatorTool` for basic arithmetic operations (e.g., if the query is "calculate 5 * 7" or "What is the sum of 10 and 20?").
        *   Uses the Gemini API to generate explanations or solve problems, potentially incorporating the calculator's output.
    *   **Physics Agent:** Handles physics-related questions.
        *   **Tool:** Uses a `ConstantsLookupTool` to retrieve values of physical constants (e.g., speed of light, gravitational constant) from a `physics_constants.json` file.
        *   Uses the Gemini API to generate explanations, potentially incorporating the retrieved constant's information.
4.  **Tools:**
    *   **CalculatorTool:** A Python class that performs basic arithmetic (+, -, \*, /) on explicit expressions.
    *   **ConstantsLookupTool:** A Python class that loads physical constants from a JSON file and allows lookup by name.
5.  **Gemini API:** All agents leverage Google's Gemini API for natural language understanding (intent classification for Tutor Agent) and response generation (for all agents).

### Agent Interaction Flow

1.  User submits a query (e.g., "What is the value for the speed of light?" or "Can you calculate 12 + 5?").
2.  The FastAPI app sends the query to the `TutorAgent`.
3.  `TutorAgent` prompts Gemini to classify the query (e.g., as "PHYSICS" or "MATH").
4.  Based on the classification, `TutorAgent` forwards the query to the corresponding sub-agent (e.g., `PhysicsAgent`).
5.  The `PhysicsAgent` processes the query. It checks if any known physical constant names (from `physics_constants.json`) are mentioned.
    *   If "speed of light" is found, it uses `ConstantsLookupTool.lookup("speed of light")` to get: "Speed of light (c) is 299792458 m/s."
    *   The `PhysicsAgent` then forms a prompt for Gemini, including the original query and the tool's output: "User asked: 'What is the value for the speed of light?'. Relevant constant info: 'Speed of light (c) is 299792458 m/s.'. Please use this to answer."
6.  Gemini generates a response.
7.  The `PhysicsAgent` returns this response to the `TutorAgent`.
8.  The `TutorAgent` returns the response to the FastAPI app, which sends it to the user.

A similar flow occurs for the `MathAgent` and its `CalculatorTool`. If the query is "calculate 12 + 5", the `MathAgent` uses the `CalculatorTool` to get "12 + 5 = 17" and then asks Gemini to present this.

## Local Setup & Running

### Prerequisites

*   Python 3.8+
*   Git

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ai-tutor-project
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the project root (`ai-tutor-project/.env`):
    ```env
    GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
    ```
    Replace `"YOUR_GOOGLE_GEMINI_API_KEY"` with your actual API key obtained from [ai.google.dev](https://ai.google.dev).

### Running Locally

1.  Ensure your virtual environment is activated and the `.env` file is correctly set up.
2.  Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    (Or `python main.py` if uvicorn.run is configured in main.py)
3.  Open your web browser and navigate to `http://127.0.0.1:8000`. You should see the AI Tutor interface.
4.  Alternatively, you can test the API endpoint using `curl` or Postman:
    ```bash
    curl -X POST "http://127.0.0.1:8000/ask" \
         -H "Content-Type: application/json" \
         -d '{"query": "What is the speed of light?"}'
    ```

## Deployment

This application can be deployed to platforms like Vercel or Railway.

**For Vercel:**
1. Connect your GitHub repository to Vercel.
2. Configure the build command: (Often auto-detected for Python/FastAPI, but might be `pip install -r requirements.txt`)
3. Configure the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT` (Vercel sets the `$PORT` environment variable).
4. Add your `GEMINI_API_KEY` as an environment variable in the Vercel project settings.

**For Railway:**
1. Connect your GitHub repository to Railway.
2. Railway will likely detect it's a Python project using a `Procfile` or try to run `main.py`. Add a `Procfile`:
   ```Procfile
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
