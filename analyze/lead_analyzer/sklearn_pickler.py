from sklearn.externals import joblib

from django.conf import settings

import os

class NoPicklesException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class PicklePaths:
    def __init__(self, **kwargs):
        # default parent dir is 'prod'
        parent_dir = kwargs.get('parent_dir') or 'prod'
        self.PICKLE_JAR = os.path.join(settings.ROOT_DIR, 'analyze', 'sklearn_models', parent_dir)
        self.TITLE_COUNT_VECTORIZER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'titlecountvectorizer.pkl')
        self.TITLE_TFIDF_TRANSFORMER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'titletfidftransfomer.pkl')
        self.TITLE_CLASSIFIER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'titleclf.pkl')
        self.DESC_COUNT_VECTORIZER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'desccountvectorizer.pkl')
        self.DESC_TFIDF_TRANSFORMER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'desctfidftransformer.pkl')
        self.DESC_CLASSIFIER_PICKLE_PATH = os.path.join(self.PICKLE_JAR, 'descclf.pkl')

    def pickles_exist(self):
        return (os.path.exists(self.PICKLE_JAR) and
          os.path.exists(self.TITLE_COUNT_VECTORIZER_PICKLE_PATH) and
          os.path.exists(self.TITLE_TFIDF_TRANSFORMER_PICKLE_PATH) and
          os.path.exists(self.TITLE_CLASSIFIER_PICKLE_PATH) and
          os.path.exists(self.DESC_COUNT_VECTORIZER_PICKLE_PATH) and
          os.path.exists(self.DESC_TFIDF_TRANSFORMER_PICKLE_PATH) and
          os.path.exists(self.DESC_CLASSIFIER_PICKLE_PATH))

class PickleLoader:
    def load_pickle(self, path):
        return joblib.load(path)

class PickleSaver:
    def save_pickle(self, obj, path):
        return joblib.dump(obj, path)
