import requests

url = "http://127.0.0.1:8000/product/recommend"
headers = {"Content-Type": "application/json"}
data = {"candidate_id": "AlisonGaines78"}

response = requests.post(url, headers=headers, json=data)

# Print the response
print(response.status_code)
print(response.json())  # If the response is in JSON format
print(response.json().get('recommendation'))
