from retrieve_posts import PostRetriever
import pprint

pr = PostRetriever()

link = 'http://losangeles.craigslist.org/wst/cpg/5395529366.html'

rss_link = 'https://losangeles.craigslist.org/search/cpg?format=rss&is_paid=all&query=wordpress&search_distance_type=mi'

printer = pprint.PrettyPrinter(indent = 4)

#printer.pprint(pr.get_posts_from_rss(rss_link))

#printer.pprint(pr.get_information_from_post({ 'link': link }))

pr.get_posts()
