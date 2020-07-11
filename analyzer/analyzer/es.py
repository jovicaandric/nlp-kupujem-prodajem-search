from typing import Dict, Tuple, Optional

from .pipeline import Pipeline
from .price.parser import PriceLabel, PriceQuery


class ElasticSearchQueryBuilder:
    def __init__(self):
        self._pipeline = Pipeline()

    def build(self, user_search_query: str) -> Dict:
        analysis_results = self._pipeline.run(user_search_query)

        ad_name_filter = self._build_ad_name_filter(analysis_results.query)
        category_filter = self._build_category_filter(analysis_results.category)
        location_filter = self._build_location_filter(analysis_results.location)
        price_filter, currency_filter = self._build_price_filter(
            analysis_results.price_query, analysis_results.currency
        )
        ads_exceptions_filters = self._build_ads_exceptions_filter()

        filters = [
            ad_name_filter,
            category_filter,
            location_filter,
            price_filter,
            currency_filter,
        ]

        non_empty_filters = [
            query_filter
            for query_filter in filters
            if query_filter != {"match_all": {}}
        ]

        es_query = {
            "query": {
                "bool": {"must": non_empty_filters, "must_not": ads_exceptions_filters}
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

    def _build_category_filter(self, category: Optional[str]) -> Dict:
        if category is None:
            return {"match_all": {}}
        else:
            return {"match": {"category": category}}

    def _build_location_filter(self, location: Optional[str]) -> Dict:
        if location is None:
            return {"match_all": {}}
        else:
            return {"match": {"location": location}}

    def _build_price_filter(
        self, price_query: PriceQuery, currency: Optional[str]
    ) -> Tuple[Dict, Dict]:
        if not price_query:
            return {"match_all": {}}, {"match_all": {}}
        else:
            price_filter = {modifier: amount for modifier, amount in price_query}
            return (
                {"range": {"price": price_filter}},
                {"match": {"currency": currency}},
            )

    def _build_ads_exceptions_filter(self) -> Dict:
        return {
            "terms": {
                "price": [
                    PriceLabel.BUYING,
                    PriceLabel.LOOKING,
                    PriceLabel.AGREEMENT,
                    PriceLabel.CONTACT,
                    PriceLabel.CALL,
                ],
            }
        }
