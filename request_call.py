import requests

response = requests.get("http://localhost:5000/employee/1")

print(response.json())
