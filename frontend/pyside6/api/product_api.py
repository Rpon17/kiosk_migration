import requests

BASE_URL = "http://127.0.0.1:8000"

def get_products_by_category(category_id: int):
    response = requests.get(
        f"{BASE_URL}/products/category/{category_id}"
    )
    response.raise_for_status()
    return response.json()

def create_product(category_id: int, name: str, price: int, image_url: str = ""):
    response = requests.post(
        f"{BASE_URL}/products",
        json={
            "category_id": category_id,
            "name": name,
            "price": price,
            "image_url": image_url
        }
    )
    response.raise_for_status()
    return response.json()