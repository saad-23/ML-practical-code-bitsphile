# function to calculate area
def calculate_area(radius):
    pi = 3.14159
    area = pi * (radius ** 2)
    return area
# function to validate user input using regex
import re
def validate_input(user_input):
    pattern = r'^\d+(\.\d+)?$'  # matches positive integers and decimals
    if re.match(pattern, user_input):
        return True
    else:
        return False
    
# function to fetch data from an API
import requests
def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # check for HTTP errors
        return response.json()  # return the JSON data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
# function to save data to a filedef save_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Data successfully saved to {filename}")
