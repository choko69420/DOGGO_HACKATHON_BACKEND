import requests

endpoint = 'http://localhost:8000/api/'

json = {
    "category": "sexism",
    "reason": "a reason thats sexist",
    "website_url": "https://www.google.com",
}
headers = {
    "Authorization": "Token c04a32a7b59acfb56986f26bbf45c64c47a8590e"
}
requests.post(endpoint, json=json, headers=headers)
