# Now lets save this information in our local computer

import datetime as datetime

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
        return df
    else:
        logger.warning("Cannot transform data: no tree")


def saving_data(df, path):
    path_with_datetime = (
        f"{path}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    )
    logger.info(f"Saving data to {path} as {path_with_datetime}")
    with open(path_with_datetime, "w") as f:
        df.to_csv(f, index=False)
        logger.info(f"Data saved to {path_with_datetime} successfully")


# testing
tree = parsing_data(fetch_data(url))
df = transform_data(tree)
saving_data(df, "output/countries.csv")
