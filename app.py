# Flask application code
from flask import Flask, jsonify, request
from flask_cors import CORS
from model import adira 
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_data():
    try:
        result = subprocess.Popen(['python', 'model.py'], stdout=subprocess.PIPE)
        output = ""
        for line in iter(result.stdout.readline, b''):
            try:
                output += line.decode("utf-8")
            except UnicodeDecodeError:
                pass  # Ignore decoding errors
        result.wait()
        json_data = {'message': output}
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"})

@app.route('/', methods=['POST'])
def run_model():
    try:
        request_data = request.get_json()
        
        # Check if "query" key exists in the request data
        if 'query' not in request_data:
            return jsonify({'error': 'No "query" key found in the request data'})

        # Extract the string value associated with the "query" key
        query_value = request_data['query']

        # Convert the query value to string
        query_string = str(query_value)

        # Call the adira function from model.py with the query string
        output = adira(query_string)
        
        # Format the response
        response = {'message': output}
        
        # Return the response
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
