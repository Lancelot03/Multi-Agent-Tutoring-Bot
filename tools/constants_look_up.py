import json
import os

class ConstantsLookupTool:
    def __init__(self, constants_file="tools/physics_constants.json"):
        # Construct the absolute path to the JSON file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ai-tutor-project/
        self.file_path = os.path.join(base_dir, constants_file)
        try:
            with open(self.file_path, 'r') as f:
                self.constants = json.load(f)
        except FileNotFoundError:
            print(f"Error: Constants file not found at {self.file_path}")
            self.constants = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.file_path}")
            self.constants = {}


    def lookup(self, constant_name: str) -> str:
        constant_name_lower = constant_name.lower()
        if constant_name_lower in self.constants:
            data = self.constants[constant_name_lower]
            return f"{constant_name.capitalize()} ({data.get('symbol', '')}) is {data['value']} {data['unit']}."
        # Try partial match
        for key in self.constants.keys():
            if constant_name_lower in key or key in constant_name_lower:
                data = self.constants[key]
                return f"{key.capitalize()} ({data.get('symbol', '')}) is {data['value']} {data['unit']}."
        return f"Constant '{constant_name}' not found."

# Example usage (optional, for testing)
if __name__ == "__main__":
    tool = ConstantsLookupTool()
    print(tool.lookup("speed of light"))
    print(tool.lookup("gravity"))
    print(tool.lookup("h")) # Example of non-full name
    print(tool.lookup("nonexistent"))
