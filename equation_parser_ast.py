"""
Equation Parser
"""
import ast
import operator
import math
from enum import Enum, auto

class NodeType(Enum):
    NUMBER = auto()
    VARIABLE = auto()
    OPERATOR = auto()
    FUNCTION = auto()

class EquationParser:
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        self.functions = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'acos': math.acos,
            'asin': math.asin,
            'atan': math.atan,
            'cosh': math.cosh,
            'sinh': math.sinh,
            'tanh': math.tanh,
            'exp': math.exp,
            'log': math.log,
            'abs': math.fabs,
            'fabs': math.fabs,
            'sqrt': math.sqrt,
            'trunc': math.trunc,
        }

    def parse_equation(self, equation_string):
        try:
            return ast.parse(equation_string, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Invalid equation syntax: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid equation syntax: {e}")

    def tokenize(self, equation_string):
        parsed_eq = self.parse_equation(equation_string)
        return self._tokenize_node(parsed_eq.body)

    def _tokenize_node(self, node):
        if isinstance(node, ast.Num):
            return (NodeType.NUMBER, node.n)
        elif isinstance(node, ast.Name):
            return (NodeType.VARIABLE, node.id)
        elif isinstance(node, ast.BinOp):
            return (NodeType.OPERATOR, type(node.op),
                    self._tokenize_node(node.left),
                    self._tokenize_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return (NodeType.OPERATOR, type(node.op),
                    self._tokenize_node(node.operand))
        elif isinstance(node, ast.Call):
            return (NodeType.FUNCTION, node.func.id,
                    [self._tokenize_node(arg) for arg in node.args])
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    def evaluate(self, tokenized_eq, x, y):
        r = math.sqrt(x*x + y*y)  # Slight optimization: x*x instead of x**2
        return self._evaluate_node(
            tokenized_eq, {'x': x, 'y': y, 'r': r, 'pi': math.pi, 'e': math.e})

    def _evaluate_node(self, node, variables):
        node_type = node[0]
        if node_type is NodeType.NUMBER:
            return node[1]
        elif node_type is NodeType.VARIABLE:
            return variables[node[1]]
        elif node_type is NodeType.OPERATOR:
            op = self.operators[node[1]]
            if len(node) == 3:
                return op(self._evaluate_node(node[2], variables))
            else:
                return op(self._evaluate_node(node[2], variables),
                          self._evaluate_node(node[3], variables))
        elif node_type is NodeType.FUNCTION:
            func = self.functions[node[1]]
            args = [self._evaluate_node(arg, variables) for arg in node[2]]
            return func(*args)
        else:
            raise ValueError(f"Unsupported node type: {node_type}")

def evaluate_equation_meshgrid(tokens, X: list[float], Y: list[float]) -> list[list[float]]:
    parser = EquationParser()
    Z = []
    for y in Y:
        row = []
        for x in X:
            row.append(float(parser.evaluate(tokens, x, y)))
        Z.append(row)
    return Z


# Test the functions
if __name__ == "__main__":
    import timeit

    parser = EquationParser()

    x, y = 3, 4

    equations = [
        "3. + .3 + x - y -.3",
        "x + y*.5 -2.",
        "pi - (.5 * e ** 2)",
        "2 * x + sin(y) - 3 * sqrt(x**2 + y**2)",
        "r * sin(y/x)",
        "x * cos(r) + y * sin(r)"
    ]

    for eq_string in equations:
        tokenized = parser.tokenize(eq_string)
        result = parser.evaluate(tokenized, x, y)
        print(f"z(x, y) = {eq_string}\nz({x}, {y}) = {result}")

        # Measure performance
        time = timeit.timeit(lambda: parser.evaluate(tokenized, x, y), number=100000)
        print(f"Evaluation time for 100,000 iterations: {time:.4f} seconds")
        result = parser.evaluate(tokenized, x, y)

