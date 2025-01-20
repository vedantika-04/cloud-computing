from products import dao

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> 'Product':
        """
        Safely create a Product object from a dictionary.
        """
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if qty is missing
        )

def list_products() -> list[Product]:
    """
    Retrieve a list of all products from the database, loading them as Product objects.
    """
    products = dao.list_products()  # Fetch raw product data
    # Use a list comprehension to create Product objects more efficiently
    return [Product.load(product) for product in products]

def get_product(product_id: int) -> Product:
    """
    Retrieve a single product by ID.
    """
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)

def add_product(product: dict):
    """
    Add a new product to the database.
    """
    # Validate required keys before passing to the DAO
    required_keys = {'id', 'name', 'description', 'cost'}
    if not required_keys.issubset(product.keys()):
        raise ValueError(f"Missing keys in product data: {required_keys - product.keys()}")
    dao.add_product(product)

def update_qty(product_id: int, qty: int):
    """
    Update the quantity of a product by ID.
    """
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    # Ensure the product exists before updating
    product = dao.get_product(product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")
    dao.update_qty(product_id, qty)
