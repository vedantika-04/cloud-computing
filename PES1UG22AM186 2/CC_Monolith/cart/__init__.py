import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    # Fetch cart details for the user
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []
    
    # Use JSON to parse contents safely instead of eval
    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Parse JSON safely
            items.extend(contents)  # Add all items to the list
        except json.JSONDecodeError:
            continue  # Skip invalid entries
    
    # Fetch product details in bulk for better performance
    product_details = products.get_products_bulk(items)  # Assume this is a bulk fetch method
    return product_details


    


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)