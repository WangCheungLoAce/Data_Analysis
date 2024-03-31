from flask import Flask, request, render_template, send_file
from csv_converter import convert_to_csv
from healthgrade import scrape_health_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_py_script', methods=['POST'])
def run_py_script():
    # Get data from the form
    specialty = request.form.get('specialty')
    location = request.form.get('location')

    # Call the function with input data and convert to csv
    output = scrape_health_data(specialty, location)
    csv_data = convert_to_csv(output)

    # Return the output and CSV data to the template
    return render_template('index.html', output=output, csv_data=csv_data)

@app.route('/download_csv')
def download_csv():
    try:
        # Serve the 'data.csv' file as a downloadable file
        return send_file('data.csv', as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
