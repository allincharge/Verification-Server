# Verification-Server
This repository contains the server component of the Vehicle Data Management System, a Flask-based API designed to manage vehicle data such as VINs and plate numbers. It is optimized to run on Raspberry Pi and provides endpoints for adding and verifying vehicle data.

## API Endpoints

#### Add Data
```http
  POST /add-data
```
#### Description
Adds a new vehicle to the database.
- **Method**: POST
- **URL**: /add-data
- **Headers**:
  - Content-Type: application/json
- **Request Body**:
  ```json
  {
    "VINnumber": "VIN12345678901234",
    "plateNumber": "PLATE1234"
  }
#### Response
- **Status 200 OK: Successfully added the vehicle.
- **Status 500 Internal Server Error: Failed to add the vehicle.
- **Response Body**:
  ```json
  {
    "status": "true"
  }

#### Verify Data
```http
  POST /verify-vin
```
#### Description
Verifies if a VIN is present in the database.
- **Method**: POST
- **URL**: /verify-vin
- **Headers**:
  - Content-Type: application/json
- **Request Body**:
  ```json
  {
    "VINnumber": "VIN12345678901234"
  }
#### Response
- **Status 200 OK: VIN exists or does not exist.
- **Response Body**:
  ```json
  {
    "status": "true"
  }

## Example Usage

### Python (Client):
```python
import requests
import json

# Server URLs
VERIFY_URL = 'http://192.168.1.106:5000/verify-vin'
DATA_URL = 'http://192.168.1.106:5000/add-data'

def check_vin(VIN_number):
    """
    Check if the provided VIN number exists in the database.
    Returns True if the VIN number exists, False otherwise.
    """
    data = {
        'VINnumber': VIN_number
    }

    try:
        response = requests.post(VERIFY_URL, json=data)
        response.raise_for_status()
        return response.json()['status']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

def insert_data(VIN_number, plate_number):
    """
    Insert the provided VIN number and plate number into the database.
    Returns True on success, False on failure.
    """
    data = {
        'VINnumber': VIN_number,
        'plateNumber': plate_number
    }

    try:
        response = requests.post(DATA_URL, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    VIN_number = '9234587890abcde5'
    plate_number = 'CBA123'

    result = check_vin(VIN_number)
    print(f"Server response: {result}")
```

### Python (Server):
```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = 'vehicle.db'

def create_database():
    """
    Create the SQLite3 database if it doesn't already exist.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles
                 (VINnumber TEXT, plateNumber TEXT)''')
    conn.commit()
    conn.close()

def insert_data(VINnumber, plateNumber):
    """
    Insert the provided VIN number and plate number into the database.
    Returns True on success, False on failure.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO vehicles (VINnumber, plateNumber) VALUES (?, ?)", (VINnumber, plateNumber))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        conn.close()
        return False
    
def check_vin(VINnumber):
    """
    Check if the provided VIN number exists in the database.
    Returns True if the VIN number exists, False otherwise.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles WHERE VINnumber = ?", (VINnumber,))
    result = c.fetchone()
    conn.close()
    return bool(result)

@app.route('/add-data', methods=['POST'])
def add_data():
    """
    Endpoint to add the provided VIN number and plate number to the database.
    Returns a JSON response with the 'status' field set to True or False.
    """
    data = request.get_json()
    VINnumber = data['VINnumber']
    plateNumber = data['plateNumber']

    if insert_data(VINnumber, plateNumber):
        return jsonify({'status': True})
    else:
        return jsonify({'status': False}), 500
    
@app.route('/verify-vin', methods=['POST'])
def verify_vin():
    """
    Endpoint to verify the provided VIN number only.
    Returns a JSON response with the 'status' field set to True or False.
    """
    data = request.get_json()
    VINnumber = data['VINnumber']

    if check_vin(VINnumber):
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})

if __name__ == '__main__':
    create_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
```
