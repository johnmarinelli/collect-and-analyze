from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

from .sklearn_pickler import *

class PostPredictor:
    """
    Predicts a post given its title, body, and compensation.
    Requires there to be a saved classifier model.
    """
    def __init__(self):
        if pickle_loader.pickles_exist():
            self.title_count_vectorizer = pickle_loader.load_pickle(TITLE_COUNT_VECTORIZER_PICKLE_PATH)
            self.title_tfidf_transformer = pickle_loader.load_pickle(TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.title_classifier = pickle_loader.load_pickle(TITLE_CLASSIFIER_PICKLE_PATH)
        else:
            raise NoPicklesException("No pickles loaded for Predictor.")

    def predict(self, post):
        new_post = [post]
        new_post_counts = self.title_count_vectorizer.transform(new_post)
        new_post_tfidf = self.title_tfidf_transformer.transform(new_post_counts)

        predicted = self.title_classifier.predict(new_post_tfidf)

        return predicted[0]

