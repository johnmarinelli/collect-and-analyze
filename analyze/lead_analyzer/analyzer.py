from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
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
    def __init__(self, **kwargs):
        pickle_loader = PickleLoader()
        saved_pickles_path = kwargs.get('saved_pickles_path')
        self.pickle_paths = PicklePaths(parent_dir = saved_pickles_path)

        if self.pickle_paths.pickles_exist():
            self.title_count_vectorizer = pickle_loader.load_pickle(self.pickle_paths.TITLE_COUNT_VECTORIZER_PICKLE_PATH)
            self.title_tfidf_transformer = pickle_loader.load_pickle(self.pickle_paths.TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.title_classifier = pickle_loader.load_pickle(self.pickle_paths.TITLE_CLASSIFIER_PICKLE_PATH)
            self.desc_count_vectorizer = pickle_loader.load_pickle(self.pickle_paths.DESC_COUNT_VECTORIZER_PICKLE_PATH)
            self.desc_tfidf_transformer = pickle_loader.load_pickle(self.pickle_paths.DESC_TFIDF_TRANSFORMER_PICKLE_PATH)
            self.desc_classifier = pickle_loader.load_pickle(self.pickle_paths.DESC_CLASSIFIER_PICKLE_PATH)
        else:
            # todo: don't forget lemmatization, stopwords. etc
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

        # fit the models to our targets
        self.title_classifier = self.title_classifier or self.__create_classifier().fit(x_title_train_tfidf, training_target)
        self.desc_classifier = self.desc_classifier or self.__create_classifier().fit(x_desc_train_tfidf, training_target)

    def save_models(self):
        """
        Let's pickle some classifiers and transformers
        """
        pickle_saver = PickleSaver()
        pickle_saver.save_pickle(self.title_count_vectorizer, self.pickle_paths.TITLE_COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_tfidf_transformer, self.pickle_paths.TITLE_TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.title_classifier, self.pickle_paths.TITLE_CLASSIFIER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_count_vectorizer, self.pickle_paths.DESC_COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_tfidf_transformer, self.pickle_paths.DESC_TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.desc_classifier, self.pickle_paths.DESC_CLASSIFIER_PICKLE_PATH)

    def __create_classifier(self):
        return SGDClassifier(loss = 'hinge', penalty = 'l2', alpha = 1e-9, n_iter = 10, random_state = 42)

