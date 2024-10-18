from flask import Flask, render_template, request, redirect, url_for
import create_3d_plot
import equation_parser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        color = request.form.get('color')
        subscribe = request.form.get('subscribe')

        # Redirect to the result page
        return redirect(url_for('result', name=name, email=email, age=age, color=color, subscribe=subscribe))
    return render_template('form.html')

@app.route('/result')
def result():
    # Get data from query parameters
    name = request.args.get('name')
    email = request.args.get('email')
    age = request.args.get('age')
    color = request.args.get('color')
    subscribe = request.args.get('subscribe')
    
    return render_template('result.html', name=name, email=email, age=age, color=color, subscribe=subscribe)

@app.route('/3dplot')
def threed_plot():
    plot_json = create_3d_plot.create_3d_plot(create_3d_plot.example_function, (-6, 6), (-6, 6))
    return render_template('plot_3d.html', plot_json=plot_json)

@app.route('/3dplot_parse')
def threed_plot_parse():
    eq = "sin(x^2 + y^2)"
    tokens = equation_parser.tokenize_equation(eq)
    plot_json = create_3d_plot.create_3d_plot_parser(tokens, (-3, 3), (-3, 3), eq, num_points=40)
    return render_template('plot_3d.html', plot_json=plot_json)


if __name__ == '__main__':
    app.run(debug=True)
