"""Fetch raw ads from source storage.

This module defines an interface for KP ads raw data extraction from the various
data sources. Raw data is stored locally, ready for the next steps such as data
processing and feature transformation.

"""
import logging
import os
from typing import List, Tuple

import click
import pandas as pd
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from .. import paths


logger = logging.getLogger("analyzer.data.fetch")


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
    "posted_at",
    "thumbnail",
    "url",
]


def _init_elasticsearch_client(host: str) -> Elasticsearch:
    client = None

    try:
        client = Elasticsearch(host)
        client.info()
    except exceptions.ConnectionError:
        logger.error(f"Failed to connect to elasticsearch server at '{host}'")

    return client


def _get_latest_ad() -> Tuple[str, str]:
    ads_df = pd.read_csv(paths.RAW_ADS_PATH, usecols=["id", "posted_at"])
    ad_timestamp = ads_df.iloc[-1].posted_at
    ad_id = ads_df.iloc[-1].id
    return str(ad_id), ad_timestamp


@click.command()
@click.argument("es_host")
@click.argument("index")
@click.option(
    "--size",
    type=int,
    default=10_000,
    show_default=True,
    help="Size of the batch send at each iteration for elasticsearch scroll API",
)
def fetch(es_host: str, index: str, size: int) -> None:
    """Fetch ad documents from elasticsearch ES_HOST and INDEX.

    Documents are saved in 'data/raw/ads.csv' CSV file with rows sorted by
    'posted_at' timestamp. If some documents are previously saved, only newer
    documents will be fetched and appended to CSV file.

    """
    client = _init_elasticsearch_client(host=es_host)

    if os.path.exists(paths.RAW_ADS_PATH):
        # Fetch only ads that are newer than the most recent ad previously saved.
        ad_id, ad_timestamp = _get_latest_ad()
        search_query = {
            "query": {
                "bool": {
                    "must_not": {"term": {"id": ad_id}},
                    "filter": {"range": {"posted": {"gte": ad_timestamp}}},
                }
            }
        }
    else:
        search_query = {"query": {"match_all": {}}}

    try:
        count_response = client.count(index=index, body=search_query)
        docs_count = count_response["count"]

        if not docs_count:
            logger.info(f"No new documents found in '{index}' index")
            return

        logger.info(f"Found total {docs_count} new documents in '{index}' index")

        docs: List[dict] = [
            doc["_source"]
            for doc in scan(
                client,
                index=index,
                query=search_query,
                size=size,
                _source_excludes=["html"],
            )
        ]
    except exceptions.ElasticsearchException as e:
        logger.error(f"Elasticsearch exception: {e}", exc_info=True)
        return

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

    out_file = paths.RAW_ADS_PATH

    if os.path.exists(out_file):
        ads_df.to_csv(out_file, index=False, header=False, mode="a")
    else:
        ads_df.to_csv(out_file, index=False)

    logger.info(f"Saved {len(docs)} ad docs to '{out_file}'")


if __name__ == "__main__":
    fetch()
