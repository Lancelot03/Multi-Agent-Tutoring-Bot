from agents import generate_gemini_response # Assuming generate_gemini_response is in agents/__init__.py
from tools.calculator import CalculatorTool
import re

class MathAgent:
    def __init__(self):
        self.calculator = CalculatorTool()

    def process_query(self, query: str) -> str:
        # Try to identify if the query is a direct calculation request
        # e.g., "calculate 5 * 7", "what is 10 + 2", "compute 30 / 3"
        # More robust: use regex to find "number operator number" patterns within the query
        
        # Check for keywords indicating a calculation
        calculation_keywords = ["calculate", "compute", "what is", "evaluate"]
        # Regex for simple arithmetic expressions like "5 * 7", "10.5 + 3", "-2 / 4"
        # This regex looks for the pattern anywhere in the query.
        arithmetic_pattern = r"(-?\d+\.?\d*)\s*([\+\-\*\/])\s*(-?\d+\.?\d*)"
        
        # First, check for simple arithmetic expressions explicitly provided.
        # E.g., if query is "5 * 7"
        direct_calc_match = re.fullmatch(arithmetic_pattern, query.strip())

        if direct_calc_match:
            # The query itself is a calculation
            calc_expr = query.strip()
            tool_result = self.calculator.calculate(calc_expr)
            if "Error:" not in tool_result:
                # If calculation is successful, ask Gemini to present it or explain if needed
                prompt = f"The user asked to calculate: '{query}'. The result is '{tool_result}'. Please present this result to the user, perhaps with a brief confirmation or context."
            else:
                # If calculation failed, let Gemini know, or just return the error
                prompt = f"The user asked a math question: '{query}'. An attempt to use a calculator tool for part of it resulted in: '{tool_result}'. Please assist the user with their original math question, considering this tool error."
            return generate_gemini_response(prompt)

        # If not a direct calculation, check if a calculation is *embedded* or *requested*
        # Example: "Can you calculate 5 times 7 for me?"
        # Example: "What is the result of 100 / 25?"
        
        # Simpler approach for this assignment: If "calculate" or similar keyword is present
        # AND an arithmetic expression is found, use the tool.
        
        match = None
        for keyword in calculation_keywords:
            if keyword in query.lower():
                search_match = re.search(arithmetic_pattern, query)
                if search_match:
                    match = search_match
                    break
        
        if match:
            # Extracted an arithmetic expression from the larger query
            expression_to_calculate = match.group(0) # The full matched expression e.g. "5 * 7"
            tool_result = self.calculator.calculate(expression_to_calculate)
            
            if "Error:" not in tool_result:
                prompt = f"The user asked: '{query}'.\nA calculation was performed: {tool_result}.\nUse this calculation result to help answer the user's original question comprehensively. If the original query was just the calculation, confirm it."
            else:
                # Calculation failed, let Gemini handle the original query with this info
                prompt = f"The user asked: '{query}'.\nAn attempt to use a calculator tool for an embedded calculation ('{expression_to_calculate}') resulted in: '{tool_result}'.\nPlease answer the user's original math question, taking this tool error into account if relevant."
        else:
            # No specific calculation found or requested to be done by the tool, let Gemini handle the math query directly
            prompt = f"You are a helpful Math tutor. Please answer the following math question: '{query}'"
            
        return generate_gemini_response(prompt)

# Example usage (for testing)
if __name__ == "__main__":
    # Ensure agents/__init__.py loads .env by running from project root or setting PYTHONPATH
    # python -m agents.math_agent
    agent = MathAgent()
    print("Test 1 (Direct Calculation):")
    print(agent.process_query("5 * 7"))
    print("\nTest 2 (Keyword Calculation):")
    print(agent.process_query("Can you calculate 100 / 4 for me?"))
    print("\nTest 3 (General Math Question):")
    print(agent.process_query("What is Pythagoras theorem?"))
    print("\nTest 4 (Calculation with error):")
    print(agent.process_query("calculate 10 / 0"))
    print("\nTest 5 (Algebra - no tool use expected):")
    print(agent.process_query("Solve for x: 2x + 5 = 11"))
