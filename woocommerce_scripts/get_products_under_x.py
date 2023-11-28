"""
script that will use the Woocoomerce API to
get prices of all products and
create a list of products that have prices less than $X.

"""

import sys
import csv
from woocommerce import API
import os


try:
    woo_key = os.environ['WOO_KEY']
    woo_secret = os.environ['WOO_SECRET']
except KeyError:
    raise Exception(f"The environment variables 'WOO_KEY' and 'WOO_SECRET' must be set. ")

# Check if a command line argument for target price is provided
if len(sys.argv) != 2 or len(sys.argv[1]) > 3:
    print("Usage: python script.py <price> [where <price> is <= 6 characters long]")
    sys.exit(1)

try:
    user_price = float(sys.argv[1])
except ValueError:
    print("Error: Invalid price. Please provide a whole number.")
    sys.exit(1)


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

    # Query example to get products with price user chose
    data = wcapi.get("products", params={"per_page": per_page, "max_price": user_price, "page": page})
    products = data.json()

    # If there are no more products, break out of the loop
    if not products:
        break

    # Add the current page's products to the list
    all_products.extend(products)

    # Move to the next page
    page += 1

# Create a list of products with prices < user_price

cheap_products = [
    {"name": product['name'], "price": product['price']}
    for product in all_products
    if float(product['price']) < user_price
]

# Create a CSV file with the list of products
csv_file_path = f"your_products_under_{str(user_price)}.csv"
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(["Product Name", " Price"])

    # Write data
    for product in all_products:
        csv_writer.writerow([product['name'], f"  {product['price']}"])

print(f"CSV file created: {csv_file_path}")