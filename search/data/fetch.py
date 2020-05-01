"""Fetch raw ads from source storage.

This module defines an interface for KP ads raw data extraction from the various
data sources. Raw data is stored locally, ready for the next steps such as data
processing and feature transformation.

"""
import json
import logging
import os

import click
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan


logger = logging.getLogger(name=__name__)


DATA_DIR = os.path.dirname(os.path.abspath(__file__))


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
def fetch(es_host: str, index: str, size: int):
    """Fetch ad documents from elasticsearch ES_HOST and INDEX."""
    client = _init_elasticsearch_client(host=es_host)

    try:
        count_response = client.count(index=index)
        docs_count = count_response["count"]
        logger.info(f"Found total {docs_count} ads in '{index}' index")

        docs = [
            doc["_source"]
            for doc in scan(client, index=index, size=size, _source_excludes=["html"])
        ]

        output_file = os.path.join(DATA_DIR, "raw", "ads.json")
        with open(output_file, "w") as fp:
            json.dump(docs, fp, indent=2)
            logger.info(f"Saved {len(docs)} ad docs to '{output_file}'")
    except exceptions.ElasticsearchException as e:
        logger.error(str(e))


if __name__ == "__main__":
    fetch()
