# Elasticsearch Docker Cluster

Before running `docker-compose` increase max virtual memory on the host machine

```
$ sudo sysctl -w vm.max_map_count=262144
```

Start Elasticsearch cluster with 3 nodes with

```
$ docker-compose up
```

Create the new ad index

```bash
curl -X PUT localhost:9200/ad \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "url": {"type": "keyword"},
      "thumbnail": {"type": "keyword"},
      "name": {"type": "text"},
      "description": {"type": "text"},
      "price": {"type": "double"},
      "currency": {"type": "keyword"},
      "location": {"type": "keyword"},
      "lat": {"type": "double"},
      "lon": {"type": "double"},
      "category": {"type": "keyword"},
      "subCategory": {"type": "keyword"},
      "posted": {"type": "date"}
    }
  }
}
EOF
```
