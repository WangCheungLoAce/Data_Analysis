from flask import Flask, request, render_template
from healthgrade import scrape_health_data  # Importing the function from healthgrade.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_py_script', methods=['POST'])
def run_py_script():
    # Get data from the form
    specialty = request.form.get('specialty')
    location = request.form.get('location')

    # Call the function with input data
    output = scrape_health_data(specialty, location)

    # Return the output to the template
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
