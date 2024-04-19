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
