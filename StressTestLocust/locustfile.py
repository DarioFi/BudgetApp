local_url = "http://127.0.0.1:8000/"
url = "https://filabudget.herokuapp.com"
import random
from locust import HttpUser, task, between

token = "3d09316a3b691e0d253a2c6504639074de49c22c"






class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def view_item(self):
        item_id = random.randint(1, 100)
        self.client.get(f"/budget/account_detail/{item_id}", headers={'Authorization': "token " + token})

    def on_start(self):
        # self.client.post("/users/login/", {"username": "foo", "password": "bar"})
        pass