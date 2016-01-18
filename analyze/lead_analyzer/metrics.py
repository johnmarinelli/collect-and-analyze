from ..models import Post
from .analyzer import PostAnalyzer
from .predictor import PostPredictor
from math import floor
from sklearn import metrics

class PostMetrics:
    def get_metrics(self):
        analyzer = PostAnalyzer(saved_pickles_path = 'metrics')
        predictor = PostPredictor(saved_pickles_path = 'metrics')
        posts = Post.get_processed_posts()

        posts_len = len(posts)
        validation_size = int(floor(posts_len * 10e-2))
        training_size = posts_len - validation_size

        training = posts[:training_size]
        training_target = map(lambda p: p.passes, training)
        validation = list(reversed(posts))[:validation_size]
        validation_target = map(lambda p: p.passes, validation)

        analyzer.analyze(training)
        analyzer.save_models()
        preds = predictor.predict(validation)
        title_preds = preds['title_preds']
        desc_preds = preds['desc_preds']

        categories = ['0', '1']
        title_metrics = metrics.classification_report(validation_target, title_preds, target_names = categories)
        desc_metrics = metrics.classification_report(validation_target, desc_preds, target_names = categories)
        return { 'title': title_metrics, 'desc': desc_metrics }

