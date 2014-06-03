from src import celery_app
import nltk

# http://stackoverflow.com/questions/13965823/resource-corpora-wordnet-not-found-on-heroku
nltk.data.path.append('./src/nltk_data')
