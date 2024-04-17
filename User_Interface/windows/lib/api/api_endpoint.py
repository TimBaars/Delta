from flask import Flask, jsonify, request, abort
from os import abort
import os

app = Flask(__name__) 

API_KEY = os.getenv('APIKEY', '')

@app.before_request 
def verify_api_key():
    if API_KEY == '':
        abort(500, description="Internal Server Error - API Key not set") 

    api_key = request.headers.get('X-API-KEY') 
    if api_key != API_KEY:
        abort(401, description="Unauthorized - Invalid API Key") 

@app.route('/api/start', methods=['GET']) 
def start_delta(): 
    # ToDo: Run the program 
    data = {'message': 'Started the Delta robot!'} 
    return jsonify(data) 

@app.route('/api/stop', methods=['GET']) 
def stop_delta(): 
    # ToDo: Stop the program 
    data = {'message': 'Stopped the Delta robot!'} 
    return jsonify(data) 

@app.route('/api/location', methods=['GET']) 
def location_delta(): 
    # ToDo: Get live location the program 
    data = {'message': 'Location for the Delta robot!', 'location': {'x': 0, 'y': 0, 'z': 0} } # ToDo fill with correct values 
    return jsonify(data) 

if __name__ == '__main__': 
    app.run(debug=True) 