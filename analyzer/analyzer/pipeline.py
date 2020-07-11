import re
from typing import Optional

from dataclasses import dataclass

from . import paths
from .category.predictor import AdCategoryPredictor
from .location.predictor import AdLocationPredictor
from .price.parser import PriceRangeParser, PriceQuery


@dataclass(frozen=True)
class QueryAnalysisResult:
    query: str
    category: Optional[str] = None
    location: Optional[str] = None
    price_query: Optional[PriceQuery] = None
    currency: Optional[str] = None

    def update(self, **kwargs) -> "QueryAnalysisResult":
        query = kwargs.get("query", self.query)
        category = kwargs.get("category", self.category)
        location = kwargs.get("location", self.location)
        price_query = kwargs.get("price_query", self.price_query)
        currency = kwargs.get("currency", self.currency)
        return QueryAnalysisResult(query, category, location, price_query, currency)


class Pipeline:
    def __init__(self) -> None:
        self._ad_category_predictor = AdCategoryPredictor.from_path(
            paths.fasttext_model_file(module="category", dim=100, extension="ftz")
        )
        self._ad_location_predictor = AdLocationPredictor.from_path(
            paths.LOCATIONS_VECTORIZER_PATH
        )
        self._price_range_parser = PriceRangeParser()

    def run(self, query: str) -> QueryAnalysisResult:
        step_input = QueryAnalysisResult(query=query)
        category_step = self._run_category_step(step_input)
        location_step = self._run_location_step(category_step)
        output = self._run_price_step(location_step)
        return output

    def _run_category_step(
        self, step_input: QueryAnalysisResult
    ) -> QueryAnalysisResult:
        query = step_input.query
        category = self._ad_category_predictor.predict(query)
        output = step_input.update(query=query, category=category)
        return output

    def _run_location_step(
        self, step_input: QueryAnalysisResult
    ) -> QueryAnalysisResult:
        query = step_input.query
        location, new_query = self._ad_location_predictor.predict(query)
        output = step_input.update(query=new_query, location=location)
        return output

    def _run_price_step(self, step_input: QueryAnalysisResult) -> QueryAnalysisResult:
        query = step_input.query
        price_query, currency, new_query = self._price_range_parser.parse(query)
        new_query = re.sub("\\s+", " ", new_query).strip()
        output = step_input.update(
            query=new_query, price_query=price_query, currency=currency
        )
        return output
