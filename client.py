import requests

endpoint = 'http://localhost:8000/api/friends'

json = {
    "username": "admin"
}
headers = {
    "Authorization": "Token b68a97a1f486a2d4f40c31ed8979a056d8ab0174"
}
print(requests.get(endpoint, json=json, headers=headers).json())
