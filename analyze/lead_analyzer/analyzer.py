from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class PostAnalyzer:
    """
    Analyzes a post given its title, body, and compensation.
    """

