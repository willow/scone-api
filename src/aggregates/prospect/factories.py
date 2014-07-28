from src.aggregates.prospect.models import Prospect


def construct_prospect_from_attrs(prospect_attrs):
  prospect = Prospect._from_attrs(prospect_attrs)
  return prospect
