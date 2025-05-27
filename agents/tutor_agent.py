from agents import generate_gemini_response
from agents.math_agent import MathAgent
from agents.physics_agent import PhysicsAgent

class TutorAgent:
    def __init__(self):
        self.math_agent = MathAgent()
        self.physics_agent = PhysicsAgent()

    def _classify_query(self, query: str) -> str:
        # Simple keyword-based classification (can be improved with Gemini)
        # query_lower = query.lower()
        # if any(kw in query_lower for kw in ["math", "solve", "calculate", "equation", "number", "algebra", "geometry"]):
        #     # Check for physics keywords to avoid misclassification if both are present
        #     if not any(kw in query_lower for kw in ["physics", "force", "energy", "light", "gravity", "newton", "einstein"]):
        #         return "MATH"
        # if any(kw in query_lower for kw in ["physics", "force", "energy", "light", "gravity", "newton", "einstein", "wave", "particle"]):
        #     return "PHYSICS"
        # return "GENERAL" # Default or if unsure

        # Using Gemini for classification
        prompt = f"""You are an expert query classifier for a tutoring system.
Classify the following student's question into one of these categories: 'MATH', 'PHYSICS', or 'GENERAL'.
Respond with only the category name in uppercase (e.g., MATH). Do not add any other text.

Student's question: "{query}"
Category:"""
        
        classification = generate_gemini_response(prompt).strip().upper()
        
        # Validate classification
        if classification in ["MATH", "PHYSICS", "GENERAL"]:
            return classification
        else:
            # Fallback or re-attempt if classification is unexpected
            print(f"Warning: Unexpected classification '{classification}'. Defaulting to GENERAL.")
            return "GENERAL"


    def handle_query(self, query: str) -> str:
        subject = self._classify_query(query)
        print(f"DEBUG: Classified query '{query}' as {subject}") # For debugging

        if subject == "MATH":
            return self.math_agent.process_query(query)
        elif subject == "PHYSICS":
            return self.physics_agent.process_query(query)
        elif subject == "GENERAL":
            # Handle general queries directly or have a GeneralAgent
            prompt = f"You are a helpful general tutor. Please answer the following question: '{query}'"
            return generate_gemini_response(prompt)
        else:
            # Should not happen with current classification logic but good for robustness
            return "I'm not sure how to categorize your question. Can you please rephrase it or specify the subject?"

# Example usage (for testing)
if __name__ == "__main__":
    # python -m agents.tutor_agent
    tutor = TutorAgent()
    
    # Test with environment variable for API key set
    print("--- MATH QUERY ---")
    print(tutor.handle_query("Can you help me solve 2x + 5 = 11?"))
    print("\n--- MATH CALCULATION QUERY ---")
    print(tutor.handle_query("calculate 15 * 3"))
    
    print("\n--- PHYSICS QUERY ---")
    print(tutor.handle_query("What is Newton's second law?"))
    print("\n--- PHYSICS CONSTANT QUERY ---")
    print(tutor.handle_query("Tell me about the speed of light."))
    
    print("\n--- GENERAL QUERY ---")
    print(tutor.handle_query("Who was Albert Einstein?")) # Could be physics or general
    
    print("\n--- AMBIGUOUS QUERY ---")
    print(tutor.handle_query("What is the energy of a photon given its wavelength using planck constant?"))
