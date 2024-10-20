import numpy as np
import re

def tokenize_equation(equation):
    # Define regex pattern for operators, functions, variables, and numbers
    pattern = r'(\+|-|\*|/|\^|\(|\)|sin|cos|tan|sqrt|x|y|\d+(\.\d*)?)'
    tokens = re.findall(pattern, equation)
    return [token[0] for token in tokens]

def evaluate_equation(tokens, x, y):
    # Define operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left / right)
        elif operator == '^':
            values.append(left ** right)

    def apply_function(function, values):
        arg = values.pop()
        if function == 'sin':
            values.append(np.sin(arg))
        elif function == 'cos':
            values.append(np.cos(arg))
        elif function == 'tan':
            values.append(np.tan(arg))
        elif function == 'sqrt':
            values.append(np.sqrt(arg))

    operators = []
    values = []
    
    for token in tokens:
        if token == 'x':
            values.append(x)
        elif token == 'y':
            values.append(y)
        elif token == 'r':
            values.append(np.sqrt(y*y + x*x))
        elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            values.append(float(token))
        elif token in ('sin', 'cos', 'tan', 'sqrt'):
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                if operators[-1] in ('sin', 'cos', 'tan', 'sqrt'):
                    apply_function(operators.pop(), values)
                else:
                    apply_operator(operators, values)
            operators.pop()  # Remove the '('
            if operators and operators[-1] in ('sin', 'cos', 'tan', 'sqrt'):
                apply_function(operators.pop(), values)
        elif token in precedence:
            while operators and operators[-1] != '(' and precedence.get(operators[-1], 0) >= precedence[token]:
                apply_operator(operators, values)
            operators.append(token)

    while operators:
        apply_operator(operators, values)

    return values[0]


def test_equation_parser():
	# Example usage
	equation = "cos(x + y) * sqrt(x^2 + y^2)"
	tokens = tokenize_equation(equation)
	print("Tokenized equation:", tokens)

	# Test with scalar values
	x, y = 1.0, 2.0
	result = evaluate_equation(tokens, x, y)
	print(f"Result for x={x}, y={y}: {result}")

	# Test with vector values
	x = np.array([1.0, 2.0, 3.0])
	y = np.array([2.0, 3.0, 4.0])
	result = evaluate_equation(tokens, x, y)
	print(f"Result for vector inputs:\n{result}")

if __name__ == "__main__":
	test_equation_parser()

