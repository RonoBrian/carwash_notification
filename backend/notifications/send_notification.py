import requests

url = "http://127.0.0.1:8000/api/notifications/send/"

payload = {
    "service": "full Body Wash",
    "recipient": "flutterwavekeny29@gmail.com"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())
