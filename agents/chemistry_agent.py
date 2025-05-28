from agents import generate_gemini_response
from tools.periodic_table_lookup import PeriodicTableLookupTool

class ChemistryAgent:
    def __init__(self):
        self.periodic_table_tool = PeriodicTableLookupTool()
        self.element_names = list(self.periodic_table_tool.elements.keys())
        self.element_symbols = [data['symbol'] for data in self.periodic_table_tool.elements.values()]

    def process_query(self, query: str) -> str:
        tool_output = None
        query_lower = query.lower()
        words_in_query = query_lower.replace('?', '').replace('.', '').split() # Simple tokenization

        # Try to find an element name, symbol, or atomic number to look up
        # This is a basic approach. More robust would be regex or specific keyword extraction.
        potential_identifiers = []
        for word in words_in_query:
            if word in self.element_names:
                potential_identifiers.append(word)
            elif word.capitalize() in self.element_symbols: # Symbols are often capitalized
                 potential_identifiers.append(word.capitalize())
            elif word.isdigit() and 1 <= int(word) <= 118: # Max known atomic number
                 potential_identifiers.append(word)
        
        if potential_identifiers:
            # For simplicity, use the first identified potential element
            # A more complex agent might try to disambiguate or ask for clarification
            identifier_to_lookup = potential_identifiers[0]
            tool_output = self.periodic_table_tool.lookup_element(identifier_to_lookup)
            
        if tool_output and "not found" not in tool_output:
            prompt = f"The user asked a chemistry question: '{query}'.\nRelevant information from the periodic table tool: '{tool_output}'.\nPlease use this information to provide a comprehensive answer to the user's question."
        else:
            prompt = f"You are a helpful Chemistry tutor. Please answer the following chemistry question: '{query}'"
            if tool_output and "not found" in tool_output:
                 prompt += f"\n(Note: A lookup for an element mentioned in the query resulted in: '{tool_output}')"

        return generate_gemini_response(prompt)

# Example usage (for testing)
if __name__ == "__main__":
    # python -m agents.chemistry_agent
    agent = ChemistryAgent()
    print("Test 1 (Element Query by name):")
    print(agent.process_query("What is carbon?"))
    print("\nTest 2 (Element Query by symbol):")
    print(agent.process_query("Tell me about O."))
    print("\nTest 3 (General Chemistry Question):")
    print(agent.process_query("What is a covalent bond?"))
    print("\nTest 4 (Element not in local DB):")
    print(agent.process_query("What is unobtainium?"))
