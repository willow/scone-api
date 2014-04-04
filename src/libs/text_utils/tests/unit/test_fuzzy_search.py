import pytest
from src.libs.text_utils.search import fuzzy_search


@pytest.mark.parametrize(('target', 'sources', 'expected'), [
  ('organ', ['organize', 'organization'], 'organize')
])
def test_fuzzy_parser_gets_closest_source(target, sources, expected):
  actual = fuzzy_search.get_closest_word(target, sources)
  assert expected == actual
