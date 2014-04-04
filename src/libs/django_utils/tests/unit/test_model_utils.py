from django.db import models
import pytest
from src.libs.django_utils.models.utils import copy_django_model_attrs


class TestModel(models.Model):
  title = models.TextField()


@pytest.fixture
def test_model():
  test_model = TestModel()
  return test_model


def test_copy_django_model_attrs_copies_correct_attribute(test_model):
  title = 'hi'
  attrs = {'title': title}
  copy_django_model_attrs(test_model, **attrs)
  assert title == test_model.title


def test_copy_django_model_attrs_copies_correct_attribute_only_if_called(test_model):
  assert bool(test_model.title) == False


def test_copy_django_model_attrs_does_not_copy_pk(test_model):
  id_field = 1
  attrs = {'pk': id_field, 'id': id_field}
  copy_django_model_attrs(test_model, **attrs)
  assert id_field != test_model.pk

