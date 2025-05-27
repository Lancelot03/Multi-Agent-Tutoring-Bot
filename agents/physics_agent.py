from agents import generate_gemini_response
from tools.constants_look_up import ConstantsLookupTool

class PhysicsAgent:
    def __init__(self):
        self.constants_tool = ConstantsLookupTool()
        # Pre-load constant names for easier matching
        self.known_constant_names = list(self.constants_tool.constants.keys()) if self.constants_tool.constants else []


    def process_query(self, query: str) -> str:
        tool_output = None
        
        # Try to find if a known constant is mentioned
        # This is a simple keyword match. More advanced would be NER.
        for const_name in self.known_constant_names:
            if const_name.lower() in query.lower():
                tool_output = self.constants_tool.lookup(const_name)
                break # Use the first one found for simplicity

        if tool_output and "not found" not in tool_output:
            prompt = f"The user asked a physics question: '{query}'.\nRelevant physical constant information found: '{tool_output}'.\nPlease use this information to provide a comprehensive answer to the user's question."
        else:
            prompt = f"You are a helpful Physics tutor. Please answer the following physics question: '{query}'"
            if tool_output and "not found" in tool_output: # e.g. user asked for "my favorite constant"
                prompt += f"\n(Note: A lookup for a constant mentioned in the query resulted in: '{tool_output}')"
                
        return generate_gemini_response(prompt)

# Example usage (for testing)
if __name__ == "__main__":
    # python -m agents.physics_agent
    agent = PhysicsAgent()
    print("Test 1 (Constant Query):")
    print(agent.process_query("What is the speed of light?"))
    print("\nTest 2 (General Physics Question):")
    print(agent.process_query("Explain Newton's second law."))
    print("\nTest 3 (Question mentioning a constant implicitly):")
    print(agent.process_query("How does earth gravity affect falling objects?"))
    print("\nTest 4 (Query for non-existent constant):")
    print(agent.process_query("What is the value of the flibbertigibbet constant?"))
