import feedparser


def print_feed():
	firenews = feedparser.parse('http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/')
	for item in firenews.feed:
		print type(item)


print_feed()