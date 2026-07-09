import requests


BASE_URL = "http://127.0.0.1:8000"



def get_stores():

    response = requests.get(
        f"{BASE_URL}/stores"
    )

    response.raise_for_status()

    return response.json()



def create_store(name, location):

    response = requests.post(
        f"{BASE_URL}/stores",
        json={
            "name": name,
            "location": location
        }
    )

    response.raise_for_status()

    return response.json()