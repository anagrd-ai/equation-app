import numpy as np
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from plotly.subplots import make_subplots
from typing import List
from plot_util import create_colorscale
import json
import equation_parser_ast
import nn_equation_solve

def generate_data(tokens, x_range, y_range, num_points=50):
    X = np.random.uniform(x_range[0], x_range[1], num_points)
    Y = np.random.uniform(y_range[0], y_range[1], num_points)
    z = equation_parser_ast.evaluate_equation_meshgrid(tokens, X, Y)
    Z = np.array(z, float)
    return X, Y, Z

def create_3d_plot(
        tokens, equation, x_range, y_range, num_points=50, locolor="#000080", hicolor="#00FF00"):
    x_train, y_train, z_train = generate_data(tokens, x_range, y_range, num_points=int(0.8 * num_points))
    x_test, y_test, z_test = generate_data(tokens, x_range, y_range, num_points=int(0.2 * num_points))

    # Create and train the model
    model = nn_equation_solve.create_model()
    history = nn_equation_solve.train_model(model, x_train, y_train, z_train)

    # Make predictions
    z_pred = model.predict(np.column_stack((x_test, y_test)))

    X_test, Y_test = np.meshgrid(x_test, y_test)
    colorscale = create_colorscale(locolor, hicolor)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('True Data', 'Model Prediction'),
        specs=[[{'type': 'surface'}, {'type': 'surface'}]]
    )
    fig.add_trace(
        go.Surface(z=z_test, x=X_test, y=Y_test, colorscale=colorscale),
        row=1, col=1
    )
    fig.add_trace(
        go.Surface(z=z_pred, x=X_test, y=Y_test, colorscale=colorscale),
        row=1, col=2
    )

    fig.update_layout(
        title=f'3D Surface Plots: z = {equation}',
        autosize=False,
        width=1600,  # Doubled the width to accommodate two plots
        height=600,
        margin=dict(l=65, r=50, b=65, t=90),
        showlegend=False
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)


if __name__ == "__main__":
    eq = "sin(x**2 + y**2)"
    parser = equation_parser_ast.EquationParser()
    tokens = parser.tokenize(eq)
    print(f"z = {eq}, {tokens=}")
    plot_json = create_3d_plot(tokens, eq, (-6, 6), (-6, 6), num_points=10)
    # print("JSON: ", plot_json)

    # plot_json = create_3d_plot(example_function, (-6, 6), (-6, 6), num_points=5)
    # In a real Flask app, you would pass this JSON to your template
    print("JSON representation of the plot created successfully.")
    print("Length of JSON string:", len(plot_json))

    # Optionally, save the JSON to a file for inspection
    with open('plot_data.json', 'w') as f:
        f.write(plot_json)
    print("Plot data saved to 'plot_data.json'")
