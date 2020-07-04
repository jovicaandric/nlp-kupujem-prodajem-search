import pytest
from analyzer.price.parser import PriceRangeParser, Currency, Modifier


parser = PriceRangeParser()


@pytest.mark.parametrize(
    "query, expected_price_query, expected_currency",
    [
        (
            "samsung s10 ispod 1000eur",
            [(Modifier.LESS_OR_EQUAL, 1000.0)],
            Currency.EUR,
        ),
        (
            "samsung s10 iznad 1000eur",
            [(Modifier.GREATER_OR_EQUAL, 1000.0)],
            Currency.EUR,
        ),
        ("samsung s10 do 1000eur", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000evra", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000 EUR", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000EUR", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000€", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 do 1,000din", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.RSD,),
        ("samsung s10 do 1,000 RSD", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.RSD,),
        ("samsung s10 do 1,000RSD", [(Modifier.LESS_OR_EQUAL, 1000.0)], Currency.RSD,),
        (
            "samsung s10 do 1,000 dinara",
            [(Modifier.LESS_OR_EQUAL, 1000.0)],
            Currency.RSD,
        ),
        (
            "samsung s10 od 1000eur",
            [(Modifier.GREATER_OR_EQUAL, 1000.0)],
            Currency.EUR,
        ),
        ("samsung s10 od 1000", [(Modifier.GREATER_OR_EQUAL, 1000.0)], Currency.EUR,),
        ("samsung s10 od 1,000", [(Modifier.GREATER_OR_EQUAL, 1000.0)], Currency.EUR,),
        (
            "samsung s10 od 1,000 do 2000 rsd",
            [(Modifier.GREATER_OR_EQUAL, 1000.0), (Modifier.LESS_OR_EQUAL, 2000.0)],
            Currency.RSD,
        ),
        (
            "samsung s10 od 1,000 do 2000 dinara",
            [(Modifier.GREATER_OR_EQUAL, 1000.0), (Modifier.LESS_OR_EQUAL, 2000.0)],
            Currency.RSD,
        ),
        (
            "samsung s10 od 1,000 do 2000 din",
            [(Modifier.GREATER_OR_EQUAL, 1000.0), (Modifier.LESS_OR_EQUAL, 2000.0)],
            Currency.RSD,
        ),
        (
            "samsung s10 od 1,000din do 2000din",
            [(Modifier.GREATER_OR_EQUAL, 1000.0), (Modifier.LESS_OR_EQUAL, 2000.0)],
            Currency.RSD,
        ),
        (
            "samsung s10 do 1,000din od 2000din",
            [(Modifier.LESS_OR_EQUAL, 1000.0), (Modifier.GREATER_OR_EQUAL, 2000.0)],
            Currency.RSD,
        ),
        ("samsung s10", [], None,),
        ("eurithmycs album nov", [], None,),
        ("trazim knjigu: Planina Dinara", [], None,),
        ("hocu s10 kroz 100EUR", [], None,),
        ("hocu s10 kroz 100 na 150", [], None,),
    ],
)
def test_parse(query, expected_price_query, expected_currency):
    price_query, currency = parser.parse(query)
    assert price_query == expected_price_query
    assert currency == expected_currency
