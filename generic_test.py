import requests


dict = {
    'username': 'Dario',
    'password': 'root',
}

url_log = 'http://127.0.0.1:8000/users/rest_api/token_auth_login'

url = 'http://127.0.0.1:8000/budget/api/rest/transactions'
client = requests.session()
r = client.get(url, headers={'Authorization': "token b7a9ac8acaf5cd78d39984a4eed17a208e51ceaf"})

print(r.status_code)
print(r.text)
print(r.content)