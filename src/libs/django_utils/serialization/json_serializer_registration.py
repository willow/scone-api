import json

# Encoder function
def json_flex_dumps(obj):
  # This func is called from the settings file. Nothing in this file should re-import django stuff (which
  # JSONSerializer Does)
  from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer
  return JSONSerializer().serialize(obj)


# Decoder function
def json_flex_loads(obj):
  if isinstance(obj, bytes):
    obj = obj.decode()
  return json.loads(obj)
