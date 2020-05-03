from analyzer.category.model import AdCategoryClassifier


class ElasticSearchQueryBuilder:
    def __init__(self):
        self._ad_category_classifier = AdCategoryClassifier()

    def build(self, user_search_query: str) -> str:
        ad_name_filter = self._build_ad_name_filter(user_search_query)
        category_filter = self._build_category_filter(user_search_query)
        es_query = {"bool": {"must": [ad_name_filter, category_filter]}}
        return es_query

    def _build_ad_name_filter(self, user_search_query: str) -> dict:
        return {
            "multi_match": {
                "query": user_search_query,
                "fields": ["name", "description"],
            }
        }

    def _build_category_filter(self, user_search_query: str) -> dict:
        category, confidence = self._ad_category_classifier.predict(user_search_query)

        if confidence > self._ad_category_classifier.confidence_threshold:
            return {"match": {"category": category}}
        else:
            return {"match_all": {}}
