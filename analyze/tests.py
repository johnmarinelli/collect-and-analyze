from django.test import TestCase
from django.core.urlresolvers import reverse

class IndexViewTests(TestCase):

  def test_index_view_with_no_posts(self):
      res = self.client.get(reverse('analyze:index'))
      self.assertEqual(res.status_code, 200)
      self.assertQuerysetEqual(res.context['posts_list'], [])
