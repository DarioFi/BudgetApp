# import requests
#
#
# dict = {
#     'username': 'Dario',
#     'password': 'root',
# }
#
#
# url_log = 'http://127.0.0.1:8000/users/rest_api/token_auth_login'
# url = 'http://127.0.0.1:8000/budget/api/ajax/json_insight'

# url = 'https://filabudget.herokuapp.com/budget/api/rest/transactions'
# client = requests.session()
# token = "b7a9ac8acaf5cd78d39984a4eed17a208e51ceaf"
# r = client.get(url, headers={'Authorization': "token " + token})
# r = client.post(url_log, dict)

# print(r.status_code)
# print(r.content)


def circularArrayLoop(nums) -> bool:
    lenght = len(nums)
    for starter in range(len(nums)):
        visited = []
        current = starter
        current = (current + nums[current]) % lenght
        thet = True
        while current != starter and current not in visited:
            visited.append(current)
            if nums[current] > 0:
                if nums[starter] < 0:
                    thet = False
            elif nums[starter] > 0:
                    thet = False
            current = (current + nums[current]) % lenght
            if not thet:
                break
        if not thet:
            continue
        if (nums[current] + current) % len(nums) == current:
            continue
        else:
            return True
    return False


# print(circularArrayLoop([-1,2]))
