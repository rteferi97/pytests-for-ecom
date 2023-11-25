"""
Script to create X number of random products.
X is a command line argument.
The products will be created with random name and random price between 3 and 50.

Example command:
    $ python create_dummy_products.py --number-of-products=10
"""

from woocommerce import API
import random
import os
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process the number of products.")

# Add the '--number-of-products' argument
parser.add_argument('--number-of-products', required=True, type=int, help='Number of products to process')

# Parse the arguments
args = parser.parse_args()

number_of_products = args.number_of_products

try:
    woo_key = os.environ['WOO_KEY']
    woo_secret = os.environ['WOO_SECRET']
except KeyError:
    raise Exception(f"The environment variables 'WOO_KEY' and 'WOO_SECRET' must be set. ")

wcapi = API(
    url="http://localhost:8888/ecomtester",
    consumer_key=woo_key,
    consumer_secret=woo_secret,
    version="wc/v3"
)

counter = 0
for i in range(int(number_of_products)):
    # counter = counter + 1
    counter += 1
    print(f"Creating product number: {counter}")
    payload = dict()
    payload['name'] = f"rand product {random.randint(1, 1000)}"
    payload['regular_price'] = str(random.randint(3, 50))

    rs = wcapi.post("products", data=payload)
    assert rs.status_code == 201, f"failed to create product. Response: {rs.json()}"

