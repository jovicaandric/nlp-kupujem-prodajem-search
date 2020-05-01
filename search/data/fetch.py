"""Fetch raw ads from source storage.

This module defines an interface for KP ads raw data extraction from the various
data sources. Raw data is stored locally, ready for the next steps such as data
processing and feature transformation.

"""
import logging
import os

import click
import pandas as pd
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan


logger = logging.getLogger(name=__name__)


DATA_DIR = os.path.dirname(os.path.abspath(__file__))

COLUMNS = [
    "id",
    "name",
    "description",
    "category",
    "sub_category",
    "price",
    "currency",
    "location",
    "latitude",
    "longitude",
    "thumbnail",
    "posted_at",
]


def _init_elasticsearch_client(host: str) -> Elasticsearch:
    client = None

    try:
        client = Elasticsearch(host)
        info = client.info()
        logger.info(f"Connected to elasticsearch server: {info}")
    except exceptions.ConnectionError:
        logger.error(f"Failed to connect to elasticsearch server at '{host}'")

    return client


@click.command()
@click.argument("es_host")
@click.argument("index")
@click.option(
    "--size",
    type=int,
    default=10_000,
    show_default=True,
    help="Size (per shard) of the batch send at each iteration for elasticsearch scroll API",
)
def fetch(es_host: str, index: str, size: int) -> None:
    """Fetch ad documents from elasticsearch ES_HOST and INDEX.

    Documents are saved in 'data/raw/ads.csv' CSV file with rows sorted by
    'posted_at' timestamp.

    """
    client = _init_elasticsearch_client(host=es_host)

    try:
        count_response = client.count(index=index)
        docs_count = count_response["count"]
        logger.info(f"Found total {docs_count} ads in '{index}' index")

        docs = [
            doc["_source"]
            for doc in scan(client, index=index, size=size, _source_excludes=["html"])
        ]

        ads_df = pd.DataFrame(docs)
        ads_df.rename(
            columns={
                "subCategory": "sub_category",
                "lon": "longitude",
                "lat": "latitude",
                "posted": "posted_at",
            },
            inplace=True,
        )
        ads_df = ads_df[COLUMNS]  # Change column order.
        ads_df.sort_values(by=["posted_at"])

        output_file = os.path.join(DATA_DIR, "raw", "ads.csv")
        ads_df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(docs)} ad docs to '{output_file}'")
    except exceptions.ElasticsearchException as e:
        logger.error(str(e))


if __name__ == "__main__":
    fetch()
