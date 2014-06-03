import nltk

def find_stem(token):
  snowball =  nltk.SnowballStemmer('english')
  
  token = token.lower()
  
  stem = snowball.stem(token)
  return stem
