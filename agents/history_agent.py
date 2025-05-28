from agents import generate_gemini_response
from tools.historical_figure_lookup import HistoricalFigureLookupTool

class HistoryAgent:
    def __init__(self):
        self.figure_lookup_tool = HistoricalFigureLookupTool()
        # Get a list of known figure names for simple checking
        self.known_figures = list(self.figure_lookup_tool.figures.keys()) if self.figure_lookup_tool.figures else []

    def process_query(self, query: str) -> str:
        tool_output = None
        query_lower = query.lower()

        # Simple check if a known figure is mentioned
        for figure_key in self.known_figures:
            # Check if the key (e.g., "julius caesar") is in the query
            if figure_key in query_lower:
                # More specific match if full name is present (e.g. "Julius Caesar" not just "Caesar")
                # This simple check might need refinement for robustness.
                # For instance, "Who was Caesar?" might need to map "Caesar" to "julius caesar".
                # For now, we rely on the key being present.
                tool_output = self.figure_lookup_tool.lookup(figure_key)
                break 
        
        if tool_output and "not found" not in tool_output:
            prompt = f"The user asked a history question: '{query}'.\nInformation found about a mentioned figure: '{tool_output}'.\nPlease use this information to provide a comprehensive answer to the user's question."
        else:
            prompt = f"You are a helpful History tutor. Please answer the following history question: '{query}'"
            if tool_output and "not found" in tool_output:
                 prompt += f"\n(Note: A lookup for a figure mentioned in the query resulted in: '{tool_output}')"
        
        return generate_gemini_response(prompt)

# Example usage (for testing)
if __name__ == "__main__":
    # python -m agents.history_agent
    agent = HistoryAgent()
    print("Test 1 (Figure Query):")
    print(agent.process_query("Tell me about Cleopatra."))
    print("\nTest 2 (General History Question):")
    print(agent.process_query("What were the main causes of World War I?"))
    print("\nTest 3 (Figure not in local DB):")
    print(agent.process_query("Who was Alexander the Great?")) # Not in our small JSON
