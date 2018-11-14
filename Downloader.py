from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class Downloader:

	def __fetchPage(self, req):
		try:
			response = urlopen(req)
		
		#TODO: Add Logfile entries for Exception hits

		except URLError as e:
			if hasattr(e, 'reason'):
				print("Error reaching the server.")
				#print("Reason: " + e.reason)
				return None
			elif hassattr(e, 'code'):
				print("Server couldn\'t fulfill the request.")
				#print("Error code: ", e.code)
				return None
		else:
			return response


	#TODO: Define a different output for when res equals None 
	def __checkForMedia(self, url):
		req = Request(url, method='HEAD')
		res = self.__fetchPage(req)
		if res != None:
			contentType = res.getheader('content-type')
			if 'text' in contentType.lower():
				return False
			if 'html' in contentType.lower():
				return False
		return True


	#Check url for any accurances of filetypes via regex
	#Returns True if url may contain a file ending
	#Returns False if url does not contain a file ending
	#By only checking for an occurence of "." there are more False Positives but no need for a lis of filetypes to check against
	def __checkFileEnding(self, url):
		path = urlparse(url).path
		if ("." not in path):
			return False
		return True
		
	def __buildRobotsPath(self, url):
		parsedUrl = urlparse(url)
		return "http://" +  parsedUrl.netloc + "/robots.txt"


	def __checkRobots(self, url):
		self.robotParser.set_url(self.__buildRobotsPath(url))
		self.robotParser.read()
		return self.robotParser.can_fetch("*", url)

	def fetch(self, url):
		if not self.__checkRobots(url):
			print("Obey the Robots - " + str(url))
			return None
		if(self.__checkFileEnding(url)):
			if(self.__checkForMedia(url)):
				return None
		else:
			self.count = self.count +1
			req = Request(url)
			return self.__fetchPage(req)

	def __init__(self):
		self.robotParser = RobotFileParser()
		self.count = 0


