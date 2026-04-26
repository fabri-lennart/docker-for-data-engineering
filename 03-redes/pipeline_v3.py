# Import the necessary module
from dotenv import load_dotenv
import os
import jq
import requests
from loguru import logger
from pymongo import MongoClient


# Load environment variables from the .env file (if present)
load_dotenv()

# Acess environment variables
mongo_user = os.getenv('MONGO_USER')
mongo_pass = os.getenv('MONGO_PASS')

# expresion to filter the json data
filter_exp = jq.compile(
    ".[] | select(.id > 5) | {nombre: .name.firstname, apellido: .name.lastname, ciudad: .address.city}"
)


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def parse_data(data, compiled_filter):
    return compiled_filter.input(data).all()


def load_data(user, password, data_to_load):
    logger.info("trying the connection")
    uri = f"mongodb://{user}:{password}@localhost:27017/?authSource=admin"
    client = MongoClient(uri)
    db_client = client["ecommerce"]
    collection = db_client["users"]

    # insert the correspond document into mongo
    logger.info("inserting the data..")
    collection.insert_many(data_to_load)


url = "https://fakestoreapi.com/users"

try:
    data = fetch_data(url)
    result = parse_data(data, filter_exp)
    load_to_mongo = load_data(mongo_user, mongo_pass, result)


except Exception as e:
    print(f"Error: {e}")
