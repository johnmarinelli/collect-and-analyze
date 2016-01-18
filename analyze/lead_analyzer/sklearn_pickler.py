from sklearn.externals import joblib

from django.conf import settings

import os

PICKLE_JAR = os.path.join(settings.ROOT_DIR, 'analyze', 'sklearn_models')
TITLE_COUNT_VECTORIZER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'titlecountvectorizer.pkl')
TITLE_TFIDF_TRANSFORMER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'titletfidftransfomer.pkl')
TITLE_CLASSIFIER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'titleclf.pkl')
DESC_COUNT_VECTORIZER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'desccountvectorizer.pkl')
DESC_TFIDF_TRANSFORMER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'desctfidftransformer.pkl')
DESC_CLASSIFIER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'descclf.pkl')

class NoPicklesException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class PickleLoader:
    def pickles_exist(self):
        return (os.path.exists(PICKLE_JAR) and
          os.path.exists(TITLE_COUNT_VECTORIZER_PICKLE_PATH) and
          os.path.exists(TITLE_TFIDF_TRANSFORMER_PICKLE_PATH) and
          os.path.exists(TITLE_CLASSIFIER_PICKLE_PATH) and
          os.path.exists(DESC_COUNT_VECTORIZER_PICKLE_PATH) and
          os.path.exists(DESC_TFIDF_TRANSFORMER_PICKLE_PATH) and
          os.path.exists(DESC_CLASSIFIER_PICKLE_PATH))

    def load_pickle(self, path):
        return joblib.load(path)

class PickleSaver:
    def save_pickle(obj, path):
        return joblib.dump(obj, path)
