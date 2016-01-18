from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

from .sklearn_pickler import *

class PostPredictor:
    """
    Predicts a post given its title, body, and compensation.
    Requires there to be a saved classifier model.
    """
    def __init__(self, **kwargs):
        saved_pickles_path = kwargs.get('saved_pickles_path')
        self.pickle_paths = PicklePaths(parent_dir = saved_pickles_path)

    def load_pickles(self):
        pickle_loader = PickleLoader()
        if self.pickle_paths.pickles_exist():
            self.title_count_vectorizer = pickle_loader.load_pickle(self.pickle_paths.TITLE_COUNT_VECTORIZER_PICKLE_PATH)
            self.title_tfidf_transformer = pickle_loader.load_pickle(self.pickle_paths.TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.title_classifier = pickle_loader.load_pickle(self.pickle_paths.TITLE_CLASSIFIER_PICKLE_PATH)
            self.desc_count_vectorizer = pickle_loader.load_pickle(self.pickle_paths.DESC_COUNT_VECTORIZER_PICKLE_PATH)
            self.desc_tfidf_transformer = pickle_loader.load_pickle(self.pickle_paths.DESC_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.desc_classifier = pickle_loader.load_pickle(self.pickle_paths.DESC_CLASSIFIER_PICKLE_PATH)
        else:
            raise NoPicklesException("No pickles loaded for Predictor.")

        self.desc_preds = None
        self.title_preds = None

    def predict(self, posts):
        self.load_pickles()
        title_new_content = map(lambda p: p.title, posts)
        desc_new_content = map(lambda p: p.description, posts)
        training_target = map(lambda p: p.passes, posts)

        x_title_new_counts = self.title_count_vectorizer.transform(title_new_content)
        x_title_new_tfidf = self.title_tfidf_transformer.transform(x_title_new_counts)
        self.title_preds = self.title_classifier.predict(x_title_new_tfidf)

        x_desc_new_counts = self.desc_count_vectorizer.transform(desc_new_content)
        x_desc_new_tfidf = self.desc_tfidf_transformer.transform(x_desc_new_counts)
        self.desc_preds = self.desc_classifier.predict(x_desc_new_tfidf)

        return { 'title_preds': self.title_preds, 'desc_preds': self.desc_preds }

