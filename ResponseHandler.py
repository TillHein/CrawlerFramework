from AbsResponseHandler import AbsResponseHandler
from html.parser import HTMLParser
import urllib
import logging

# This File contains all classes that inherit from AbsResponseHandler.py
# all classes mus implement def handle(self, response): and either return:
# None -> dismiss the Request
# a String Object -> Resets the Download State to Request has to contain a url
# a Response Object -> restarts the Response Handler Chain 
# a Request Object -> Starts a Download (not advised)
# Multiple inheritance is possible there is no super __init__ that needs to be called

class LinkExtractor(AbsResponseHandler):

	def __init__(self):
		#self.links = []
		self.startUrl = ""
		self.f = open('Error.log', 'w')
		LOG_FILENAME = 'Error.log'
		logging.basicConfig(filename = LOG_FILENAME, level=logging.DEBUG)
		self.len = 0
	
	def __del__(self):
		self.f.close()

	def handle(self, response):
		self.startUrl = response.url
		Extractor = HTMLExtractor()
		links = Extractor.extract(response)
		if links != None:
			for l in links:
				if l != None:
					self._context.queue(l)
		if self._successor != None:
			return self._successor.handle(response)
		else:
			return None


class StorePage(AbsResponseHandler):

	def handle(self, response):
		self._context.store(response)
		if self._successor != None:
			return self._successor.handle(response)
		else:
			return None


class HTMLExtractor(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []

	def extract(self, res):
		self.links = []
		try:
			self.feed(res.text)
			#self.feed(response.read().decode(encoding))
		except Exception as err:
			if len(self.links) > 0:
				return self.links
			return None
		return self.links

	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for name, value in attrs:
				if name == "href":
					completedLink = self.__completeLinks(value)
					if completedLink != False:
						self.links.append(completedLink)


	def __completeLinks(self, link):
		parsedLink = urllib.parse.urlparse(link)
		# This cuts search querrys. May be to restrict.
		link = parsedLink.scheme + '://' + parsedLink.netloc + parsedLink.path
		if parsedLink.scheme == "http" or parsedLink.scheme == "https":
			return self.link
		elif link.startswith("//"):
			return self.self.parsedStartUrl.scheme + ":" + link
		elif link.startswith("/"):
			return self.self.parsedStartUrl.scheme + "://" + self.parsedStartUrl.netloc + link
		else:
			return False
