# enum implementation http://stackoverflow.com/a/1695250/173957
def enum(**enums):
  return type('Enum', (), enums)
