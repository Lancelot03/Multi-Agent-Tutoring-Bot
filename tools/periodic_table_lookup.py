
import json
import os

class PeriodicTableLookupTool:
    def __init__(self, elements_file="tools/periodic_table.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ai-tutor-project/
        self.file_path = os.path.join(base_dir, elements_file)
        try:
            with open(self.file_path, 'r') as f:
                self.elements = json.load(f) # Stored by element name (lowercase)
        except FileNotFoundError:
            print(f"Error: Periodic table file not found at {self.file_path}")
            self.elements = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.file_path}")
            self.elements = {}

    def lookup_element(self, identifier: str) -> str:
        identifier_lower = identifier.lower()
        
        # Check if identifier is an element name
        if identifier_lower in self.elements:
            data = self.elements[identifier_lower]
            return f"Element: {data['name']}, Symbol: {data['symbol']}, Atomic Number: {data['atomic_number']}."

        # Check if identifier is a symbol
        for name, data in self.elements.items():
            if data['symbol'].lower() == identifier_lower:
                return f"Element: {data['name']}, Symbol: {data['symbol']}, Atomic Number: {data['atomic_number']}."
        
        # Check if identifier is an atomic number (as string)
        for name, data in self.elements.items():
            if str(data['atomic_number']) == identifier:
               return (f"Element: {data['name']} ({data['symbol']}), " 
                       f"Atomic Number: {data['atomic_number']}, "
                       f"Atomic Mass: {data.get('atomic_mass', 'N/A')}, " # Use .get for optional fields
                       f"Category: {data.get('category', 'N/A')}.")

        return f"Element '{identifier}' not found in the simplified periodic table."

# Example usage
if __name__ == "__main__":
    tool = PeriodicTableLookupTool()
    print(tool.lookup_element("carbon"))
    print(tool.lookup_element("O"))
    print(tool.lookup_element("11"))
    print(tool.lookup_element("Unobtainium"))
