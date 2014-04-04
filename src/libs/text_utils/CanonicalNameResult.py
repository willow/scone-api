from collections import namedtuple

#is_available is a bool
#False = it is found in the text but negated. Ex: ("No dogs allowed"). Dogs is found but negated.
#True = it is found in the text and positively truthy.
CanonicalNameResult = namedtuple('CanonicalNameResult', 'keyword_id is_available')
