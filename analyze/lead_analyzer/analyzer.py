from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

from django.conf import settings

from .sklearn_pickler import *

from ..models import Post

import os

class PostAnalyzer:
    """
    Analyzes a set of posts.
    features: title, description, compensation
    target: passes
    """
    def __init__(self):
        pickle_loader = PickleLoader()

        if pickle_loader.pickles_exist():
            self.title_count_vectorizer = pickle_loader.load_pickle(TITLE_COUNT_VECTORIZER_PICKLE_PATH)
            self.title_tfidf_transformer = pickle_loader.load_pickle(TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.title_classifier = pickle_loader.load_pickle(TITLE_CLASSIFIER_PICKLE_PATH)
            self.desc_count_vectorizer = pickle_loader.load_pickle(DESC_COUNT_VECTORIZER_PICKLE_PATH)
            self.desc_tfidf_transformer = pickle_loader.load_pickle(DESC_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.desc_classifier = pickle_loader.load_pickle(DESC_CLASSIFIER_PICKLE_PATH)
        else:
            # todo: don't forget lemmatization
            self.title_count_vectorizer = CountVectorizer()
            self.title_tfidf_transformer = TfidfTransformer()
            self.desc_count_vectorizer = CountVectorizer()
            self.desc_tfidf_transformer = TfidfTransformer()
            self.title_classifier = None
            self.desc_classifier = None

    def analyze(self, posts = None):
        """
        Call this when a new training example is added
        """

        # transform data for processing by scikit-learn
        posts = posts or Post.get_processed_posts()
        title_training_content = map(lambda p: p.title, posts)
        desc_training_content = map(lambda p: p.description, posts)
        training_target = map(lambda p: p.passes, posts)

        x_title_train_counts = self.title_count_vectorizer.fit_transform(title_training_content)
        x_title_train_tfidf = self.title_tfidf_transformer.fit_transform(x_title_train_counts)

        x_desc_train_counts = self.desc_count_vectorizer.fit_transform(desc_training_content)
        x_desc_train_tfidf = self.desc_tfidf_transformer.fit_transform(x_desc_train_counts)

        # fit the title model to our targets
        #self.title_classifier = self.title_classifier or MultinomialNB().fit(x_title_train_tfidf, self.title_training_target)
        self.title_classifier = self.title_classifier or SGDClassifier(loss = 'hinge', penalty = 'l2', alpha = 1e-9, n_iter = 10, random_state = 42).fit(x_title_train_tfidf, training_target)

        self.desc_classifier = self.desc_classifier or SGDClassifier(loss = 'hinge', penalty = 'l2', alpha = 1e-9, n_iter = 10, random_state = 42).fit(x_desc_train_tfidf, training_target)

    def save_models(self):
        """
        Let's pickle some classifiers and transformers
        """
        pickle_saver = PickleSaver()
        pickle_saver.save_pickle(self.title_count_vectorizer, TITLE_COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_tfidf_transformer, TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_clf, TITLE_CLASSIFIER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_count_vectorizer, DESC_COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_tfidf_transformer, DESC_TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_clf, DESC_CLASSIFIER_PICKLE_PATH)

