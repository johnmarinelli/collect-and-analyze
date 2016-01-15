from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

from django.conf import settings

from .sklearn_pickler import *

import os

class PostAnalyzer:
    """
    Analyzes a set of posts.
    features: title, description, compensation
    target: passes
    """
    def __init__(self):
        pickle_loader = PickleLoader()

        # transform data for processing by scikit-learn
        self.posts = Post.get_processed_posts()
        self.title_training_content = map(lambda p: p.title, self.posts)
        self.description_training_content = map(lambda p: p.description, self.posts)
        self.training_target = map(lambda p: p.passes, self.posts)

        if pickle_loader.pickles_exist():
            self.title_count_vectorizer = pickle_loader.load_pickle(TITLE_COUNT_VECTORIZER_PICKLE_PATH)
            self.title_tfidf_transformer = pickle_loader.load_pickle(TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.title_classifier = pickle_loader.load_pickle(TITLE_CLASSIFIER_PICKLE_PATH)
        else:
            # todo: don't forget lemmatization
            self.title_count_vectorizer = CountVectorizer()
            self.title_tfidf_transformer = TfidfTransformer()
            self.title_classifier = None

    def analyze(self):
        """
        Call this when a new training example is added
        """
        x_title_train_counts = self.title_count_vectorizer.fit_transform(self.title_training_content)
        x_title_train_tfidf = self.title_tfidf_transformer.fit_transform(x_title_train_counts)

        # fit the model to our targets
        self.title_classifier = self.title_classifier or MultinomialNB().fit(x_title_train_tfidf, self.title_training_target)

        # save models
        pickle_saver = PickleSaver()
        pickle_saver.save_pickle(self.title_count_vectorizer, TITLE_COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_tfidf_transformer, TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_clf, TITLE_CLASSIFIER_PICKLE_PATH)
