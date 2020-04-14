import requests


dict = {
    'username': 'Dario',
    'password': 'root',
}


# url_log = 'http://127.0.0.1:8000/users/rest_api/token_auth_login'
url = 'http://127.0.0.1:8000/budget/api/rest/transactions'

# url = 'https://filabudget.herokuapp.com/budget/api/rest/transactions'
client = requests.session()
# token = "0fd78870cfad95ee54b1d400297a4c030556b6fb"
token = "87ec1370ebab5905f6b64b7952460cc16ff2d3b6"
r = client.get(url, headers={'Authorization': "token " + token})

print(r.status_code)
print(r.content)