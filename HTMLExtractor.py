from html.parser import HTMLParser
from urllib.parse import urlparse

class HTMLExtractor(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []
		self.startUrl = ""

	def extract(self, res):
		self.links = []
		self.setStartUrl(res.url)
		self.feed(res.read().decode('utf-8'))
		return self.links

	def setStartUrl(self, url):
		self.startUrl = url
		self.parsedStartUrl = urlparse(url)

	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for name, value in attrs:
				if name == "href":
					canonicalizedLink = self.__cannoicalizeLinks(value)
					if canonicalizedLink != False:
						self.links.append(canonicalizedLink)
					

	#Function to equalize link formats
	#No Link validation should happen here
	def __cannoicalizeLinks(self, link):
		parsedLink = urlparse(link)
		if parsedLink.scheme == "http" or parsedLink.scheme == "https":
			return link
		elif link.startswith("//"):
			return self.parsedStartUrl.scheme + ":" + link
		elif link.startswith("/"):
			return self.parsedStartUrl.scheme + "://" + self.parsedStartUrl.netloc + link
		else:
			return False
