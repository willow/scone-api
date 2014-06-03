from django.utils.text import slugify


def create_slug(token):
  return slugify(token)
