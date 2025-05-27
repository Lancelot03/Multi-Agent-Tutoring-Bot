import re

class CalculatorTool:
    def calculate(self, expression: str) -> str:
        # Basic safety: allow only numbers, +, -, *, / and spaces
        # This is a simplified calculator for explicit expressions like "5 * 10" or "100 / 2"
        # It does NOT handle complex algebra like "2x + 5 = 10" directly
        
        expression = expression.strip()
        # Regex to find simple arithmetic: number operator number
        match = re.fullmatch(r"^\s*(-?\d+\.?\d*)\s*([\+\-\*\/])\s*(-?\d+\.?\d*)\s*$", expression)
        
        if not match:
            return "Error: Invalid expression format. Use 'number operator number', e.g., '5 * 7' or '10 / 2'."

        num1_str, operator, num2_str = match.groups()

        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
        except ValueError:
            return "Error: Invalid numbers in expression."

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error: Division by zero."
            result = num1 / num2
        else:
            # This case should not be reached due to regex, but as a safeguard
            return "Error: Unsupported operator."
        
        # Return result as int if it's a whole number, else float
        if result.is_integer():
            return f"{expression} = {int(result)}"
        else:
            return f"{expression} = {result:.4f}" # Format float to 4 decimal places

# Example usage (optional, for testing)
if __name__ == "__main__":
    calc = CalculatorTool()
    print(calc.calculate("10 + 5"))
    print(calc.calculate(" 100.5 * 2 "))
    print(calc.calculate("50 / 0"))
    print(calc.calculate("10 / 3"))
    print(calc.calculate("10 / 2"))
    print(calc.calculate("solve 2x+5=10")) # Example of what it won't do
    print(calc.calculate("5 *"))
