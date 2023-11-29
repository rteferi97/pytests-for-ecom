"""
script that will use the Woocoomerce API to
get prices of all products and
create a list of products that have prices less than $X.
X is command line argument

Example : python3 get_products_under_x.py 24 

"""

import sys
import csv
from woocommerce import API
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


try:
    woo_key = os.environ['WOO_KEY']
    woo_secret = os.environ['WOO_SECRET']
except KeyError:
    raise Exception(f"The environment variables 'WOO_KEY' and 'WOO_SECRET' must be set. ")

try:
    url = os.environ['URL']
except KeyError:
    raise Exception(f"The environment variables 'URL' must be set")

# Check if a command line argument for target price is provided
if len(sys.argv) != 2 or len(sys.argv[1]) > 3:
    raise Exception("Usage: python script.py [where is <= 3 characters long]")

try:
    user_price = float(sys.argv[1]) - .01
except ValueError:
    raise ValueError("Error: Invalid price. Please provide a whole number.")

wcapi = API(
    url=url,
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
]

        # try:
        #     workspace = os.environ['WORKSPACE']
        # except KeyError:
        #     raise Exception(f"The environment variable 'WORKSPACE' must be set. ")

        # Check if the directory exists, and if not, use the current directory
        # try:
        #     workspace = os.environ['WORKSPACE']
        # except KeyError:
        #     pass
        # #     raise Exception(f"The environment variables 'WORKSPACE' must be set. ")
        #
        #
        # directory_path = workspace if workspace and os.path.exists(workspace) else os.getcwd()
        #
        # # Specify the filename you want to create in the chosen directory
        # filename = "products_output.csv"
        #
        # # Full path to the file
        # csv_file_path = os.path.join(workspace, filename)

        # Construct the file path relative to the Jenkins workspace or to the directory this script is located in
        # if workspace:
        #     csv_file_path = os.path.join(os.environ['WORKSPACE'], "products_output.csv")
        # else:
        #     csv_file_path = "products_output.csv"  # f"your_products_under_{str(user_price)}.csv"

# Construct the file path relative to the directory script is located in
csv_file_path = "products_output.csv" #f"your_products_under_{str(user_price)}.csv"

# Create a CSV file with the list of products
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(["Product Name", " Price"])

    # Write data
    for product in all_products:
        csv_writer.writerow([product['name'], f"  {product['price']}"])

print(f"CSV file created: {csv_file_path}")


if os.path.exists(csv_file_path):
    # Email configuration
    try:
        sender_email = os.environ['SENDER_EMAIL']
        receiver_email = os.environ['RECIPIENT_EMAIL']
    except KeyError:
        raise Exception(f"The environment variables 'SENDER_EMAIL' and 'RECIPIENT_EMAIL' must be set. ")

    subject = 'CSV File Report'
    body = 'Please find attached the CSV file report.'

    # Email server configuration (for Gmail in this example)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    try:
        smtp_username = os.environ['EMAIL_USER']
        smtp_password = os.environ['EMAIL_PASSWORD']
    except KeyError:
        raise Exception(f"The environment variables 'EMAIL_USER' and 'EMAIL_PASSWORD' must be set. ")

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach the CSV file to the email
    with open(csv_file_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(csv_file_path))
        part['Content-Disposition'] = f'attachment; filename={os.path.basename(csv_file_path)}'
        message.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print(f"Email with CSV attachment sent to {receiver_email}")
else:
    print(f"CSV file does not exist at {csv_file_path}. Email not sent.")