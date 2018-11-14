from AbsResponseHandler import AbsResponseHandler
from html.parser import HTMLParser
#import urllib.parse
#from urllib.parse import urlparse
import urllib
#import urlparse
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
					self._context.queue([l, self.startUrl])

		# By usage of Response.text the encoding should be detacted automaticly
		#try:
		#	encoding = response.headers.get_content_charset()
		#except Exception as err:
		#	print("HTML Head Encoding Error: ")
		#	logging.exception(err, exc_info = True)
		#	f = open('Error.log', 'a')
		#	f.write("####################################################")
		#	f.close()
		#	encoding = 'utf-8'

		#Handle edgecases None and Binary
		#if encoding == None or encoding == 'binary':
		#	encoding = 'utf-8'
			#return None

		# To Handle UniCodeDecodeError
		#try:
		#	self.feed(response.text)
		#	#self.feed(response.read().decode(encoding))
		#except Exception as err:
		#	logging.exception(err, exc_info = True)
		#	f = open('Error.log', 'a')
		#	f.write("####################################################")
		#	f.close()
		#	return None
		#print('HANDLE SHIT')
		if self._successor != None:
			return self._successor.handle(response)
		else:
			return None

	def __setStartUrl(self, url):
		self.startUrl = self.__completeLinks(url)


	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for name, value in attrs:
				if name == "href":
					canonicalizedLink = self.__completeLinks(value)
					if canonicalizedLink != False:
						# Changed for usage with BreadthFirstGatherer
						self._context.queue([canonicalizedLink, self.startUrl])
						self.len = self.len + 1
	# Function to equalize link formats
	# No Link validation should happen here



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
					canonicalizedLink = self.__completeLinks(value)
					if canonicalizedLink != False:
						self.links.append(canonicalizedLink)


	def __canonicalizeLinks(self, link):
	# Remove Port
	# Add trailing slash (root and guessed directorys)
	# remove Fragments and options
	# resolve Path (http://cs.india.edu/a/./../b/ -> http://cs.india.edu/b/
	# Remove default filenames (index.html)
	# decode needlessly encoded characters like '%7' -> '~'
	# encode forbidden characters like ' ' -> '%20'
		

		link = str(link)
		scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(link)
		path = urllib.parse.quote(path, '/%')
		qs = urllib.parse.quote_plus(qs, ':&=')
		anchor = ''
		return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))

	def __completeLinks(self, link):
		parsedLink = urllib.parse.urlparse(link)
		# cut the parameter so no page will be crawled multiple times with different parameters.
		# This cuts search querrys. May be to restrict.
		link = parsedLink.scheme + '://' + parsedLink.netloc + parsedLink.path
		if parsedLink.scheme == "http" or parsedLink.scheme == "https":
			return self.__canonicalizeLinks(link)
		elif link.startswith("//"):
			return self.__canonicalizeLinks(self.parsedStartUrl.scheme + ":" + link)
		elif link.startswith("/"):
			return self.__canonicalizeLinks(self.parsedStartUrl.scheme + "://" + self.parsedStartUrl.netloc + link)
		else:
			return False
