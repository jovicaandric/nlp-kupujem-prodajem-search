import json

from flask import Flask, request, jsonify

from .es import ElasticSearchQueryBuilder
from .utils import remove_non_text_chars, remove_redundant_whitespaces


app = Flask(__name__)


es_query_builder = ElasticSearchQueryBuilder()


def _clean_search_query(query: str) -> str:
    clean_query = remove_non_text_chars(text=query.lower())
    clean_query = remove_redundant_whitespaces(text=clean_query)
    return clean_query


@app.route("/analyzer", methods=["POST"])
def analyzer():
    if not request.data:
        return "Missing request body", 400

    try:
        body = json.loads(request.data)
    except json.JSONDecodeError:
        error = "JSON parse error for input query"
        app.logger.error(f"{error}: {request.data}")
        return error, 400

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
