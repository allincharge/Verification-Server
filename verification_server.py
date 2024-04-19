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
