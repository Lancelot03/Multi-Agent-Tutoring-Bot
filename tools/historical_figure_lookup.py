import json
import os

class HistoricalFigureLookupTool:
    def __init__(self, figures_file="tools/historical_figures.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ai-tutor-project/
        self.file_path = os.path.join(base_dir, figures_file)
        try:
            with open(self.file_path, 'r') as f:
                self.figures = json.load(f)
        except FileNotFoundError:
            print(f"Error: Historical figures file not found at {self.file_path}")
            self.figures = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.file_path}")
            self.figures = {}

    def lookup(self, figure_name: str) -> str:
        figure_name_lower = figure_name.lower()
        if figure_name_lower in self.figures:
            data = self.figures[figure_name_lower]
            return f"{data['full_name']} ({data['period']}): {data['description']}"
        
        # Try partial match in full names (more complex, could be added if needed)
        # For simplicity, we'll stick to direct key match for now.
        
        return f"Information about '{figure_name}' not found in the local database."

# Example usage
if __name__ == "__main__":
    tool = HistoricalFigureLookupTool()
    print(tool.lookup("cleopatra"))
    print(tool.lookup("Julius Caesar"))
    print(tool.lookup("alexander the great"))
