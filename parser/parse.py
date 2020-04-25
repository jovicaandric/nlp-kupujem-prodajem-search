import json
import logging
import re
import sys
from collections import namedtuple
from typing import List, Tuple

import pandas as pd
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(name)s: %(message)s")

logger = logging.getLogger(name="parser")

Ad = namedtuple(
    "Ad",
    (
        "url",
        "name",
        "description",
        "category",
        "sub_category",
        "posted_at",
        "price",
        "currency",
        "city",
        "latitude",
        "longitude",
    ),
)


def parse_ad_description_and_city(html: str) -> Tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")

    description_element = soup.find("div", class_="oglas-description")

    if not description_element:
        description_element = soup.find("div", class_="adDescription descriptionHeight")

    description = description_element.text
    description = re.sub("\\s+", " ", description).strip()

    city_name_element = soup.find(
        "div", class_="contact-info-row", attrs={"data-element-for": "regular-ad"}
    )

    if not city_name_element:
        city_name_element = soup.find("section", class_="locationSec")

    city_name = city_name_element.text.strip()

    return description, city_name


def parse(filename: str) -> List[Ad]:
    with open(filename, "r") as fp:
        ads = json.load(fp)

    parsed_ads: List[Ad] = []

    for hit in ads["hits"]["hits"]:
        source = hit["_source"]

        if "html" not in source or source["html"] is None:
            continue

        ad_html = source["html"]
        ad_description, ad_city = parse_ad_description_and_city(html=ad_html)

        ad = Ad(
            url=source["url"],
            name=source["name"],
            description=ad_description,
            category=source["category"],
            sub_category=source["subCategory"],
            posted_at=source["posted"],
            price=source["price"],
            currency=source["currency"],
            city=ad_city,
            latitude=source["lat"],
            longitude=source["lon"],
        )
        parsed_ads.append(ad)

    return parsed_ads


if __name__ == "__main__":
    input_filename, output_filename = sys.argv[1:]

    logger.info(f"Parsing ads from '{input_filename}'")

    ads = parse(filename=input_filename)

    logger.info(f"Parsed {len(ads)} ads")

    df = pd.DataFrame(data=ads, columns=Ad._fields)
    df.to_csv(output_filename, index=False)

    logger.info(f"Parsed ads saved to '{output_filename}'")
