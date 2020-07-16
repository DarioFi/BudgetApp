import requests

dict = {
    'username': 'Dario',
    'password': 'root',
}

url_log = 'http://127.0.0.1:8000/users/rest_api/token_auth_login'
url = 'http://127.0.0.1:8000/budget/api/rest/account_list'
#
client = requests.session()
token = "3d09316a3b691e0d253a2c6504639074de49c22c"
r = client.get(url, headers={'Authorization': "token " + token})

print(r.status_code)
print(r.content)

url = 'http://127.0.0.1:8000/budget/api/rest/category_list'

r = client.get(url, headers={'Authorization': "token " + token})

print(r.status_code)
print(r.content)
