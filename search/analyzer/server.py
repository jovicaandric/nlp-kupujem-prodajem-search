import json
import re

from flask import Flask, request, jsonify

from es import ElasticSearchQueryBuilder


app = Flask(__name__)


es_query_builder = ElasticSearchQueryBuilder()


def _clean_search_query(query: str) -> str:
    clean_query = re.sub("\\W", " ", query.lower())
    clean_query = re.sub("\\s+", " ", clean_query)
    clean_query = clean_query.strip()
    return clean_query


@app.route("/analyzer", methods=["POST"])
def analyzer():
    if not request.data:
        return "Missing request body", 400

    body = json.loads(request.data)

    if "query" not in body:
        return "Request body missing 'query' field", 400

    query = body["query"].strip()
    query = _clean_search_query(query)

    if not query:
        return "Search query is empty", 400

    app.logger.info(f"User submitted search query: {query}")

    es_query = es_query_builder.build(user_search_query=query)

    app.logger.info(f"Compiled elasticsearch query: {es_query}")

    return jsonify(es_query)


if __name__ == "__main__":
    app.run()
