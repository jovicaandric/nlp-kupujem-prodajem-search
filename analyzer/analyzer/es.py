from typing import Dict, Tuple

from . import paths
from .category.predictor import AdCategoryPredictor
from .location.predictor import AdLocationPredictor
from .price.parser import PriceRangeParser


class ElasticSearchQueryBuilder:
    def __init__(self):
        self._ad_category_predictor = AdCategoryPredictor.from_path(
            paths.fasttext_model_file(module="category", dim=100, extension="ftz")
        )
        self._ad_location_predictor = AdLocationPredictor.from_path(
            paths.LOCATIONS_VECTORIZER_PATH
        )
        self._price_range_parser = PriceRangeParser()

    def build(self, user_search_query: str) -> Dict:
        ad_name_filter = self._build_ad_name_filter(user_search_query)
        category_filter = self._build_category_filter(user_search_query)
        location_filter = self._build_location_filter(user_search_query)
        price_filter, currency_filter = self._build_price_filter(user_search_query)

        es_query = {
            "query": {
                "bool": {
                    "must": [
                        ad_name_filter,
                        category_filter,
                        location_filter,
                        price_filter,
                        currency_filter,
                    ]
                }
            }
        }

        return es_query

    def _build_ad_name_filter(self, user_search_query: str) -> Dict:
        return {
            "multi_match": {
                "query": user_search_query,
                "fields": ["name", "description"],
                "fuzziness": "AUTO",
            }
        }

    def _build_category_filter(self, user_search_query: str) -> Dict:
        category = self._ad_category_predictor.predict(user_search_query)

        if category is None:
            return {"match_all": {}}
        else:
            return {"match": {"category": category}}

    def _build_location_filter(self, user_search_query: str) -> Dict:
        location = self._ad_location_predictor.predict(user_search_query)

        if location is None:
            return {"match_all": {}}
        else:
            return {"match": {"location": location}}

    def _build_price_filter(self, user_search_query: str) -> Tuple[Dict, Dict]:
        price_range, currency = self._price_range_parser.parse(user_search_query)

        if not price_range:
            return {"match_all": {}}, {"match_all": {}}
        else:
            price_filter = {modifier: amount for modifier, amount in price_range}
            return (
                {"range": {"price": price_filter}},
                {"match": {"currency": currency.lower()}},
            )
