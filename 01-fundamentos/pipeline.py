# This file just do a simple hhtp  request to a page, then extract a table

import pandas as pd
import requests as rq
from loguru import logger
from selectolax.parser import HTMLParser

url = "https://www.scrapethissite.com/pages/simple/"


def fetch_data(url):
    """
    this is going to check if it is a valid url
    and return the response if it is.
    """
    try:
        logger.info(f"Fetching data from {url}")
        response = rq.get(url)
        response.raise_for_status()
        return response.text
    except rq.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None


def parsing_data(response):
    if response:
        logger.info("Parsing data")
        tree = HTMLParser(response)
        return tree
    else:
        logger.warning("Cannot parse data: no response")


def transform_data(tree):
    if tree:
        nodes = tree.css("h3.country-name")
        # create and empty list
        list = []
        logger.info("addig each country to the list")
        for node in nodes:
            # here we add the text of each node to the list
            list.append(node.text().strip())
        # create a df based on the list
        df = pd.DataFrame(list, columns=["country_name"])
        print(df.head())
    else:
        logger.warning("Cannot transform data: no tree")


# testing
tree = parsing_data(fetch_data(url))
transform_data(tree)
