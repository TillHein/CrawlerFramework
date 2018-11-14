from AbsFrontierStrategy import AbsFrontierStrategy
import urllib
import datetime
class BreadthFirstGatherer(AbsFrontierStrategy):


	#link[link, source]
	def queue(self, link):
		#Edgecase first entries from seed list
		if type(link) is not list:
			link = self.__canonicalizeLinks(link)
			self.frontier.insert(0,link)
			print(link + ' seeded')
			self.visited[self.__parseUrl(link)] = 0
			self.lenght = self.lenght + 1
		elif type(link) is list:
			try:
				link[0] = self.__canonicalizeLinks(link[0])
				link[1] = self.__canonicalizeLinks(link[1])
			except Exception:
				print('GATHERER: Error canonicalizing')
				return True
			try:
				hashUrl = self.__parseUrl(link[0])
			except Exception:
				print('GATHERER Error in parsing')
				return True
			
			try:
				if str(hashUrl) not in self.visited:
					self.frontier.insert(0,link[0])
					self.visited[hashUrl] = 0
					self.lenght = self.lenght + 1
			except Exception:
				print('GATHERER: Error in adding to frontier')
				return True

		else:
			print('GATHER: WRONG TYPE')
			return True


		#	if 'portal.dnb.de' in hashUrl:
		#		print ('Add ' + hashUrl + 'to Frontier')
		#	try:
		#		if self.visited[self.__parseUrl(link[1])] < 1:
		#			#print('add to Frontier: ' + link[0])
		#			self.frontier.insert(0,link[0])
		#			self.visited[hashUrl] = self.visited[self.__parseUrl(link[1])] + 1
		#			
		#			if 'portal.dnb.de/opec.htm' in hashUrl:
		#				print ('Add ' + hashUrl + 'to Frontier')
		#			self.lenght = self.lenght + 1
		#	
		#	except Exception as err:
		#		print('Key Error: ' + self.__parseUrl(link[1]))
				
			#	for key, value in self.viseted.iteritems():
			#		print (key, value)






		print(str(datetime.datetime.now()) + ': GATHER LEN: ' + str(self.lenght))
		return True

	def dequeue(self):
		if self.lenght > 0:
			self.count = self.count + 1
			self.lenght = self.lenght - 1
			return self.frontier.pop()
		else:
			print("Frontier is empty")
			return None

	def size(self):
		return len(self.frontier)

	def __parseUrl(self, url):
		parsedUrl = urllib.parse.urlparse(url)
		return parsedUrl.netloc + parsedUrl.path

	def __init__(self):
		self.frontier = list()
		#{link: layer}
		self.visited = {}
		self.layer = 0
		self.count = 0
		self.lenght = 0


	def __canonicalizeLinks(self, link):
	# Remove Port
	# Add trailing slash (root and guessed directorys)
	# remove Fragments and options
	# resolve Path (http://cs.india.edu/a/./../b/ -> http://cs.india.edu/b/
	# Remove default filenames (index.html)
	# decode needlessly encoded characters like '%7' -> '~'
	# encode forbidden characters like ' ' -> '%20'
		

		link = link.replace('///', '//')
		parsedLink = urllib.parse.urlparse(link)
		scheme = parsedLink.scheme
		netloc = parsedLink.hostname
		if ':' in netloc:
			netloc = netloc.split(':')[0]
		path = parsedLink.path
		qs = parsedLink.query
		#scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(link)
		path = urllib.parse.quote(path, '/%')
		qs = urllib.parse.quote_plus(qs, ':&=')
		anchor = ''
		if scheme == 'http':
			scheme = 'https'
		return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))
