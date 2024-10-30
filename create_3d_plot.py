import numpy as np
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from typing import List
from plot_util import create_colorscale
import json
import equation_parser_ast

def create_3d_plot(f, x_range, y_range, num_points=50):
    """
    Create a 3D surface plot of z = f(x,y)
    
    :param f: Function of two variables
    :param x_range: Tuple of (x_min, x_max)
    :param y_range: Tuple of (y_min, y_max)
    :param num_points: Number of points in each dimension
    :return: JSON representation of the plot
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    # print("Z = ", Z)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(title='3D Surface Plot: z = f(x,y)', autosize=False,
                      width=800, height=600,
                      margin=dict(l=65, r=50, b=65, t=90))

    return json.dumps(fig, cls=PlotlyJSONEncoder)

def create_3d_plot_parser(
    tokens, x_range, y_range, equation, num_points=50, locolor="#000080", hicolor="#00FF00"):
    """
    Create a 3D surface plot of z = f(x,y)
    
    :param f: Function of two variables
    :param x_range: Tuple of (x_min, x_max)
    :param y_range: Tuple of (y_min, y_max)
    :param num_points: Number of points in each dimension
    :return: JSON representation of the plot
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)
    # print("X = ", X, "\n\n")
    # print("Y = ", Y, "\n\n")
    Z = equation_parser_ast.evaluate_equation_meshgrid(tokens, x, y)

    # print("Z = ", Z, "\n\n")

    colorscale = create_colorscale(locolor, hicolor)
    fig = go.Figure(
        data=[go.Surface(z=Z, x=X, y=Y, colorscale=colorscale)])
    fig.update_layout(title=f'3D Surface Plot: z = {equation}', autosize=False,
                      width=800, height=600,
                      margin=dict(l=65, r=50, b=65, t=90))

    return json.dumps(fig, cls=PlotlyJSONEncoder)


# Example usage
def example_function(x, y):
    return np.sin(np.sqrt(x**2 + y**2))

if __name__ == "__main__":
    samples = [
        "e**(r ** .01)",
    ]
    eq = "sin(x**2 + y**2)"
    parser = equation_parser_ast.EquationParser()
    tokens = parser.tokenize(eq)
    print(f"z = {eq}, {tokens=}")
    plot_json = create_3d_plot_parser(tokens, (-6, 6), (-6, 6), eq, num_points=5)
    # print("JSON: ", plot_json)

    # plot_json = create_3d_plot(example_function, (-6, 6), (-6, 6), num_points=5)
    # In a real Flask app, you would pass this JSON to your template
    print("JSON representation of the plot created successfully.")
    print("Length of JSON string:", len(plot_json))

    # Optionally, save the JSON to a file for inspection
    # with open('plot_data.json', 'w') as f:
    #     f.write(plot_json)
    # print("Plot data saved to 'plot_data.json'")
