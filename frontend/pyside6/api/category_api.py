import requests

BASE_URL = "http://127.0.0.1:8000"

def get_categories_by_store(store_id: int):
    """/categories/store/{store_id}"""
    
    response = requests.get(
        f"{BASE_URL}/categories/store/{store_id}"
    )
    response.raise_for_status()
    return response.json()

def create_category(store_id: int, name: str):
    response = requests.post(
        f"{BASE_URL}/categories",
        json={
            "store_id": store_id,
            "name": name
        }
    )
    response.raise_for_status()
    return response.json()