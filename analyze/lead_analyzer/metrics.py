from ..models import Post
from .analyzer import PostAnalyzer
from .predictor import PostPredictor
from math import floor
from sklearn import metrics

class PostMetrics:
    def get_metrics(self):
        analyzer = PostAnalyzer()
        predictor = PostPredictor()
        posts = Post.get_processed_posts()
        training_target = map(lambda p: p.passes, posts)

        posts_len = len(posts)
        training_size = int(floor(posts_len * 10e-2))
        training = posts[training_size:]
        validation_size = posts_len - training_size
        validation = posts[:validation_size]

        # todo: create a separate pickle jar for metrics
        analzyer.analyze(training)
        predictor.predict(validation)
        title_preds = predictor.title_preds
        desc_preds = predictor.title_preds

        return { 'title': metrics.classification_report(training_target, title_preds, ['0', '1']), 'desc': metrics.classification_report(training_target, desc_preds, ['0', '1']) }


