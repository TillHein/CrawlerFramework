from html.parser import HTMLParser
import urllib
import re

class HTMLExtractor(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []

        def regextract(self, res):
            self.links = []
            try:
                #regex raw string with href= maybe link in " or ' ends with >
                urls = re.findall(r'href=[\'"]?([^\'" >]+)', res.read())
            except Exception as Err:
                return self.links
            return self.links


	def extract(self, res):
		self.links = []
		try:
			self.feed(res.read())
			#self.feed(response.read().decode(encoding))
		except Exception as err:
			if len(self.links) > 0:
				return self.links
			return []
		return self.links


	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for name, value in attrs:
				if name == "href":
					canonicalizedLink = self.__completeLinks(value)
					if canonicalizedLink != False and canonicalizedLink not in self.links:
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
		return netloc

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
