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
            self.count_vectorizer = pickle_loader.load_pickle(COUNT_VECTORIZER_PICKLE_PATH)
            self.tfidf_transformer = pickle_loader.load_pickle(TFIDF_TRANSFORMER_PICKLE_PATH)
            self.classifier = pickle_loader.load_pickle(CLASSIFIER_PICKLE_PATH)
        else:
            # todo: don't forget lemmatization
            self.count_vectorizer = CountVectorizer()
            self.tfidf_transformer = TfidfTransformer()
            self.classifier = None

    def initial_analyze(self):
        """
        Call this when a new training example is added, or it's the first time analyzing data.
        """
        x_title_train_counts = self.count_vectorizer.fit_transform(self.title_training_content)
        x_title_train_tfidf = self.tfidf_transformer.fit_transform(x_title_train_counts)

        # fit the model to our targets
        title_clf = MultinomialNB().fit(x_title_train_tfidf, self.training_target)

        # save models
        pickle_saver = PickleSaver()
        pickle_saver.save_pickle(self.count_vectorizer, COUNT_VECTORIZER_PICKLE_PATH)
        pickle_saver.save_pickle(self.tfidf_transformer, TFIDF_TRANSFORMER_PICKLE_PATH)
        pickle_saver.save_pickle(self.tfidf_transformer, CLASSIFIER_PICKLE_PATH)
