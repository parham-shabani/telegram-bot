import requests

api_url = "http://127.0.0.1:8000/all-items/?format=json"

response = requests.get(api_url)

if response.status_code == 200 :
    data = response.json()

def get_data():
    return data

