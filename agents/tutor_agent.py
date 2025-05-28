from agents import generate_gemini_response
from agents.math_agent import MathAgent
from agents.physics_agent import PhysicsAgent
from agents.history_agent import HistoryAgent # New import
from agents.chemistry_agent import ChemistryAgent # New import

class TutorAgent:
    def __init__(self):
        self.math_agent = MathAgent()
        self.physics_agent = PhysicsAgent()
        self.history_agent = HistoryAgent()       # New instance
        self.chemistry_agent = ChemistryAgent()   # New instance

    def _classify_query(self, query: str) -> str:
        # Using Gemini for classification
        prompt = f"""You are an expert query classifier for a tutoring system.
Classify the following student's question into one of these categories: 'MATH', 'PHYSICS', 'HISTORY', 'CHEMISTRY', or 'GENERAL'.
Respond with only the category name in uppercase (e.g., MATH). Do not add any other text.

Student's question: "{query}"
Category:"""
        
        classification = generate_gemini_response(prompt).strip().upper()
        
        # Validate classification
        if classification in ["MATH", "PHYSICS", "HISTORY", "CHEMISTRY", "GENERAL"]: # Added new categories
            return classification
        else:
            # Fallback or re-attempt if classification is unexpected
            print(f"Warning: Unexpected classification '{classification}' for query '{query}'. Defaulting to GENERAL.")
            # Attempt to find keywords as a simpler fallback
            query_lower = query.lower()
            if any(kw in query_lower for kw in ["math", "solve", "calculate", "equation", "number", "algebra", "geometry", "count", "sum", "integral", "derivative"]):
                return "MATH"
            if any(kw in query_lower for kw in ["physics", "force", "energy", "light", "gravity", "newton", "einstein", "wave", "particle", "motion", "thermodynamics"]):
                return "PHYSICS"
            if any(kw in query_lower for kw in ["history", "historical", "past", "event", "war", "king", "queen", "ancient", "when did", "who was"]):
                return "HISTORY"
            if any(kw in query_lower for kw in ["chemistry", "chemical", "element", "molecule", "reaction", "bond", "acid", "base", "periodic table"]):
                return "CHEMISTRY"
            return "GENERAL"


    def handle_query(self, query: str) -> str:
        subject = self._classify_query(query)
        print(f"DEBUG: Classified query '{query}' as {subject}") # For debugging

        if subject == "MATH":
            return self.math_agent.process_query(query)
        elif subject == "PHYSICS":
            return self.physics_agent.process_query(query)
        elif subject == "HISTORY":                       # New block
            return self.history_agent.process_query(query)
        elif subject == "CHEMISTRY":                     # New block
            return self.chemistry_agent.process_query(query)
        elif subject == "GENERAL":
            prompt = f"You are a helpful general tutor. Please answer the following question: '{query}'"
            return generate_gemini_response(prompt)
        else: # Should ideally not be reached if classification is one of the above
            print(f"Warning: Unhandled subject category '{subject}'. Defaulting to GENERAL for query: {query}")
            prompt = f"You are a helpful general tutor. Please answer the following question: '{query}'"
            return generate_gemini_response(prompt)

# Example usage (for testing)
if __name__ == "__main__":
    # python -m agents.tutor_agent
    tutor = TutorAgent()
    
    print("--- MATH QUERY ---")
    print(tutor.handle_query("calculate 15 * 3"))
    
    print("\n--- PHYSICS QUERY ---")
    print(tutor.handle_query("What is Newton's second law?"))

    print("\n--- HISTORY QUERY ---")
    print(tutor.handle_query("Tell me about Napoleon Bonaparte."))
    print("\n--- HISTORY QUERY (General) ---")
    print(tutor.handle_query("What was the Renaissance?"))
    
    print("\n--- CHEMISTRY QUERY ---")
    print(tutor.handle_query("What are the properties of Oxygen?"))
    print("\n--- CHEMISTRY QUERY (General) ---")
    print(tutor.handle_query("Explain what an ionic bond is."))

    print("\n--- GENERAL QUERY ---")
    print(tutor.handle_query("What's the weather like today?")) # Example of a truly general query
