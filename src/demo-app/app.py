from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is an otel demo app!\n'

@app.route('/divide')
def divide():
    target_url = 'http://0.0.0.0:5002/divide'

    # Forward the request directly to the other Flask app with the original parameters
    response = requests.get(target_url, params=request.args)
    
    # Return the response from the other app
    return response.content

@app.route('/dog', methods=['GET'])
def get_dog_image():
    try:
        # Make a request to the Dog API
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200 and data['status'] == 'success':
            # Extract the JPG URL
            jpg_url = data['message']
            return jsonify({'jpg_url': jpg_url})
        else:
            return jsonify({'error': 'Failed to get dog image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)