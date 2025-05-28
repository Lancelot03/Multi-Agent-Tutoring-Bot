# AI Tutor Multi-Agent System

This project implements an AI-powered tutoring assistant based on multi-agent system principles. The "Tutor Agent" delegates questions to specialized sub-agents (Math, Physics, History, Chemistry), which can use tools (like a calculator, constants lookup, figure lookup, or periodic table) and the Gemini API to provide answers.

**Live Deployed Application:** [MAT Bot](https://multi-agent-tutoring-bot-opav.vercel.app/)

## Architecture

The system follows a multi-agent architecture:

1.  **User Interface (FastAPI Web App):** Provides a simple web page or API endpoint for users to submit natural language queries.
2.  **Tutor Agent (Main Agent):**
    *   Receives the user's query.
    *   Uses the Gemini API to classify the query's subject (Math, Physics, History, Chemistry, General).
    *   Delegates the query to the appropriate specialist sub-agent.
    *   Returns the sub-agent's response to the user.
3.  **Sub-Agents (Specialist Agents):**
    *   **Math Agent:** Handles mathematics-related questions.
        *   **Tool:** Uses a `CalculatorTool` for basic arithmetic operations.
        *   Uses the Gemini API to generate explanations or solve problems, potentially incorporating the calculator's output.
    *   **Physics Agent:** Handles physics-related questions.
        *   **Tool:** Uses a `ConstantsLookupTool` to retrieve values of physical constants from `physics_constants.json`.
        *   Uses the Gemini API to generate explanations, potentially incorporating the retrieved constant's information.
    *   **History Agent:** Handles history-related questions.
        *   **Tool:** Uses a `HistoricalFigureLookupTool` to retrieve brief descriptions of historical figures from `historical_figures.json`.
        *   Uses the Gemini API to generate explanations, potentially incorporating the retrieved figure's information.
    *   **Chemistry Agent:** Handles chemistry-related questions.
        *   **Tool:** Uses a `PeriodicTableLookupTool` to retrieve basic information about chemical elements (name, symbol, atomic number) from `periodic_table.json`.
        *   Uses the Gemini API to generate explanations, potentially incorporating the retrieved element's information.
4.  **Tools:**
    *   **`CalculatorTool`:** A Python class that performs basic arithmetic (+, -, \*, /).
    *   **`ConstantsLookupTool`:** Loads physical constants from `physics_constants.json` and allows lookup.
    *   **`HistoricalFigureLookupTool`:** Loads data on historical figures from `historical_figures.json` and allows lookup.
    *   **`PeriodicTableLookupTool`:** Loads chemical element data from `periodic_table.json` (containing common elements with details like atomic number, symbol, mass, category, etc.) and allows lookup by name, symbol, or atomic number.
5.  **Gemini API:** All agents leverage Google's Gemini API for natural language understanding (intent classification for Tutor Agent) and response generation (for all agents).

### Agent Interaction Flow Example (Chemistry)

1.  User submits a query (e.g., "Tell me about Oxygen.").
2.  The FastAPI app sends the query to the `TutorAgent`.
3.  `TutorAgent` prompts Gemini to classify the query, which returns "CHEMISTRY".
4.  `TutorAgent` forwards the query to the `ChemistryAgent`.
5.  The `ChemistryAgent` processes the query. It identifies "Oxygen" as a potential element lookup.
    *   It uses `PeriodicTableLookupTool.lookup_element("oxygen")` which consults `periodic_table.json`.
    *   The tool might return: "Element: Oxygen (O), Atomic Number: 8, Atomic Mass: 15.999, Category: diatomic nonmetal."
    *   The `ChemistryAgent` then forms a prompt for Gemini, including the original query and the tool's output: "User asked: 'Tell me about Oxygen.'. Relevant element info: 'Element: Oxygen (O), Atomic Number: 8...'. Please use this to answer."
6.  Gemini generates a comprehensive response about Oxygen, informed by the tool's data.
7.  The `ChemistryAgent` returns this response to the `TutorAgent`.
8.  The `TutorAgent` returns the response to the FastAPI app, which sends it to the user.

A similar flow occurs for other agents and their respective tools. If a specific entity isn't found by a tool, or if the query is more general (e.g., "Explain covalent bonds"), the agent will rely more heavily on Gemini's general knowledge for that subject.

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
    *   The input placeholder now suggests queries for Math, Physics, History, or Chemistry.
4.  Alternatively, you can test the API endpoint using `curl` or Postman:
    ```bash
    curl -X POST "http://127.0.0.1:8000/ask" \
         -H "Content-Type: application/json" \
         -d '{"query": "Who was Napoleon Bonaparte?"}'
    ```
    ```bash
    curl -X POST "http://127.0.0.1:8000/ask" \
         -H "Content-Type: application/json" \
         -d '{"query": "What are the properties of carbon?"}'
    ```

## Deployment

This application can be deployed to platforms like Vercel or Railway.

**For Vercel:**
1.  Ensure you have a `vercel.json` file in your project root (see example in previous instructions or project files).
2.  Connect your GitHub repository to Vercel.
3.  Configure the build command: (Usually auto-detected or handled by `vercel.json` with `@vercel/python`. Ensure `requirements.txt` is present).
4.  If overriding, the Start Command might be `uvicorn main:app --host 0.0.0.0 --port $PORT`.
5.  Add your `GEMINI_API_KEY` as an environment variable in the Vercel project settings and **redeploy**.

**For Railway:**
1.  Connect your GitHub repository to Railway.
2.  Railway will likely detect it's a Python project. You may need a `Procfile`:
    ```Procfile
    web: uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
3.  Add your `GEMINI_API_KEY` as an environment variable in the Railway project settings.

## Challenges Faced (Optional)

*   **Tool Invocation Logic:** Deciding precisely *when* and *how* a sub-agent should use its tool based on natural language required careful consideration. Simple keyword and pattern matching was used for this version, but more advanced intent recognition or function calling features from an LLM could make this more robust. For instance, the `ChemistryAgent` uses a basic word match to identify potential elements for its `PeriodicTableLookupTool`.
*   **Prompt Engineering:** Crafting effective prompts for query classification (now including History and Chemistry) and response generation with tool outputs took some iteration.
*   **Data Management for Tools:** Populating and maintaining the `.json` files for tools (like `periodic_table.json`) can be time-consuming for comprehensive coverage. For a production system, these would ideally come from more dynamic or curated data sources.
