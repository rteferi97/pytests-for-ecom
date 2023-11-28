"""
script that will use the Woocoomerce API to
get prices of all products and
create a list of products that have prices less than $X.

"""

import requests
from woocommerce import API
import os


try:
    woo_key = os.environ['WOO_KEY']
    woo_secret = os.environ['WOO_SECRET']
except KeyError:
    raise Exception(f"The environment variables 'WOO_KEY' and 'WOO_SECRET' must be set. ")



wcapi = API(
    url="http://dev.bootcamp.store.supersqa.com/",
    consumer_key=woo_key,
    consumer_secret=woo_secret,
    version="wc/v3"
)
# Set initial page to 1
page = 1
per_page = 20  # Adjust as needed

# Initialize an empty list to store all products
all_products = []

while True:

    # Query example to get products with prices <= $10
    data = wcapi.get("products", params={"per_page": per_page, "max_price": 10, "page": page})
    products = data.json()

    # If there are no more products, break out of the loop
    if not products:
        break

    # Add the current page's products to the list
    all_products.extend(products)

    # Move to the next page
    page += 1

# Create a list of products with prices <= $10
cheap_products = [
    {"name": product['name'], "price": product['regular_price']}
    for product in all_products
    if float(product['regular_price']) <= 10.0
]

