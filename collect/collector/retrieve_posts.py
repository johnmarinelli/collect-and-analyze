import urllib2, subprocess, json, os, time
import feedparser
from bs4 import BeautifulSoup
from random import shuffle
from django.conf import settings
from ..models import Post

class InvalidPageException(Exception):
    pass

class PostRetriever:
    def create_post_from_rss_entry(self, rss_entry):
        link = rss_entry['dc_source']
        cl_id = Post.get_cl_id(link)

        # if post doesn't already exist in our db
        if not Post.objects.filter(cl_id__exact = cl_id):
            attrs = {
                'link': link,
                'title': rss_entry['title'],
                'description': rss_entry['summary_detail']['value'],
                'cl_id': cl_id
            }
            return Post.objects.create(**attrs)
        else:
            print "Post %s already in database" % link
            return None

    def get_posts_from_rss(self, rss_feed_link):
        feed = feedparser.parse(rss_feed_link)
        return map(self.create_post_from_rss_entry, feed['entries'])

    def get_information_from_post(self, post):
        print post.link

        process = subprocess.Popen(
            [
                os.getenv('PATH_TO_PHANTOMJS', 'phantomjs'), 
                os.path.join(settings.ROOT_DIR, 'collect', 'collector', 'get_email.js'), 
                post.link
            ], 
            stdout = subprocess.PIPE
        )

        output, err = process.communicate()

        if not err:
            data = json.loads(output.strip())
            if data['errorCode'] == 0:
                email = data['email']
                phone_number = data['phone_number']

                html = urllib2.urlopen(post.link).read()
                soup = BeautifulSoup(html, 'html.parser')

                compensation = soup.select('p.attrgroup span')[0].get_text()
                description = soup.select('section#postingbody')[0].get_text()

                print email

                return {
                    'email': email,
                    'phone_number': phone_number,
                    'compensation': compensation,
                    'description': description
                }
            else:
                raise InvalidPageException("Retrieval failed: %s" % data['errorMsg'])
        else:
            raise SystemError(err)

    def get_posts(self):
        areas = ['orangecounty', 'phoenix', 'losangeles', 'sfbay', 'inlandempire']
        shuffle(areas)

        for area in areas:
            print "Scanning %s.craigslist..." % area
            rss_feed_link = "https://%s.craigslist.org/search/cpg?format=rss&is_paid=all&query=wordpress&search_distance_type=mi" % area
            posts = filter(lambda p: p != None, self.get_posts_from_rss(rss_feed_link))

            for post in posts:
                try:
                    attrs = self.get_information_from_post(post)
                    post.email = attrs['email']
                    post.phone_number = attrs['phone_number']
                    post.compensation = attrs['compensation']
                    post.description = attrs['description']
                    post.save()
                except (InvalidPageException, SystemError) as e:
                    print e

                time.sleep(10)

