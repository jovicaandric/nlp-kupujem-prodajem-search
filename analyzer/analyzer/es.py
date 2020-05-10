from typing import Dict

from .category.model import AdCategoryClassifier
from .location.model import AdLocationClassificator


class ElasticSearchQueryBuilder:
    def __init__(self):
        self._ad_category_classifier = AdCategoryClassifier()
        self._ad_location_classifier = AdLocationClassificator()

    def build(self, user_search_query: str) -> Dict:
        ad_name_filter = self._build_ad_name_filter(user_search_query)
        category_filter = self._build_category_filter(user_search_query)
        location_filter = self._build_location_filter(user_search_query)
        price_filter = self._build_price_filter(user_search_query)

        es_query = {
            "query": {
                "bool": {
                    "must": [
                        ad_name_filter,
                        category_filter,
                        location_filter,
                        price_filter,
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
        category = self._ad_category_classifier.predict(user_search_query)

        if category is None:
            return {"match_all": {}}
        else:
            return {"match": {"category": category}}

    def _build_location_filter(self, user_search_query: str) -> Dict:
        location = self._ad_location_classifier.predict(user_search_query)

        if location is None:
            return {"match_all": {}}
        else:
            return {"match": {"location": location}}

    def _build_price_filter(self, user_search_query: str) -> Dict:
        # TODO(nemanja) Implement when price analyzer is done.
        return {"match_all": {}}
