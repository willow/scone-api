import json

import pytest
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer
from src.libs.django_utils.tests import FakeTestClass


@pytest.mark.django_db_with_migrations
def test_serializer_serializes_queryset_correctly():
  serializer = JSONSerializer()
  test_class = FakeTestClass(name='Some Name', id=1, url='http://www.test.com', trusted_geo_data=False)
  test_class.save()
  test_class = FakeTestClass(name='Some Name 2', id=2, url='http://www2.test.com', trusted_geo_data=True)
  test_class.save()
  dict_data = {'test_models': FakeTestClass.objects.all()}

  serialized_data = serializer.serialize(dict_data)
  deserialized_data = json.loads(serialized_data)
  assert deserialized_data["test_models"][0]["model"] == 'django_utils.faketestclass'
