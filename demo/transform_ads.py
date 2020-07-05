import sys

import pandas as pd


_PRICE_LABEL_MAP = {
    "Kontakt": -1,
    "Dogovor": -2,
    "Pozvati": -3,
    "Besplatno": -4,
    "Kupujem": -5,
    "Tražim": -6,
}


def transform_price(raw_price: str) -> float:
    raw_price = raw_price.replace(".", "").replace(",", ".")

    if raw_price in _PRICE_LABEL_MAP:
        return _PRICE_LABEL_MAP[raw_price]

    price = pd.to_numeric(raw_price, errors="coerce")
    return price


def transform_ads(input_file: str) -> str:
    df = pd.read_csv(input_file)
    df = df.drop_duplicates("id")
    df["id"] = df["id"].astype(str)
    df["price"] = df["price"].apply(transform_price)
    df["currency"] = df["currency"].str.upper()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.rename(
        columns={
            "sub_category": "subCategory",
            "latitude": "lat",
            "longitude": "lon",
            "posted_at": "posted",
        }
    )
    return df.to_json(orient="records", lines=True)


if __name__ == "__main__":
    input_file = sys.argv[1]
    ads_jsonl = transform_ads(input_file)

    output_file = sys.argv[2]
    with open(output_file, "w") as fp:
        fp.write(ads_jsonl)
