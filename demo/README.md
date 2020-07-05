# Demo

## Getting Started

Install `elasticsearch-loader`

```bash
$ pip install elasticsearch-loader
```

## Optional

Transform already downloaded ads into format supported by ads elasticsearch index

```bash
$ python transform_ads.py <input-csv-file> <output-jsonl-file>
```

Load transformed ads into index with

```bash
$ elasticsearch_loader --id-field id --index ad --bulk-size 10000 json --json-lines <jsonl-file>
`````
