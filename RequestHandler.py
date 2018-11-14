from AbsRequestHandler import AbsRequestHandler
import requests
#from urllib.request import Request, urlopen
#from urllib.error import URLError
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import sys
# This File contains all classes that inherit from AbsRequestHandler
# All classes must implement the def handle(self, response): method
# after the method is handled the handle function must either call the successor if not None
# or return a Request Object to change State to Download,
# a String Object containing an url that cycles the Request State from the beginning
# or a None Object to cancel the current workflow and get the next item from the frontier 


class CheckFiles(AbsRequestHandler):

	def handle(self, request):
		url = request.url
		if(self.__checkFileEnding(url)):
			if(self.__checkHeader(url)):
				return None
		if (self._successor != None):
			return self._successor.handle(request)
		else:
			return request
		

	def __checkHeader(self, url):
		req = requests.Request('HEAD', url)
		res = self.__fetchPage(req)
		# Hacky Solution, find a proper way to exit handler Chain on faulty Download
		# Also check if HEAD Only Request can be blocked by the Server on a otherwise 
		# downloadable website
		if res == None:
			return True
		
		encoding = res.encoding
		if encoding == 'binary':
			return True
		
		contentType = res.headers.get('Content-Type')
		if contentType == None:
			return False
		if 'binary' in contentType:
			return True
		if 'text' in contentType.lower():
			return False
		if 'html' in contentType.lower():
			return False

		return True

	#Very Basic Version, maybe try blacklisting or proper regex
	def __checkFileEnding(self, url):
		path = urlparse(url).path
		if ("." not in path):
			return False
		return True


	def __fetchPage(self, req):
		req = req.prepare()
		session = requests.Session()
		try:
			response = session.send(req, timeout=10.0)
		
		#TODO: Add Logfile entries for Exception hits

		except Exception as e:
			print('Error in checkfiles Fetchpage' + str(e))
			return None
		else:
			return response

# Add persistent list of already requested robot rules to limit Network traffic
# Also find a way to persist RobotFileParse
class CheckRobots(AbsRequestHandler):

	def handle(self, request):
		url = request.url
		if not self.__checkRobots(url):
			print("Obey the Robots - " + str(url))
			return None
		elif (self._successor != None):
			return self._successor.handle(request)
		else:
			return request
			

	def __buildRobotsPath(self, url):
		parsedUrl = urlparse(url)
		return "http://" +  parsedUrl.netloc + "/robots.txt"


	def __checkRobots(self, url):
		self.robotParser = RobotFileParser()
		self.robotParser.set_url(self.__buildRobotsPath(url))
		try:
			self.robotParser.read()
		except Exception as e:
			print(e)
			print('robots URL: ' + self.__buildRobotsPath(url))
			return False
		return self.robotParser.can_fetch("*", url)
