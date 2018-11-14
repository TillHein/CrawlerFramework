from AbsDownloadState import AbsDownloadState
from requests import Request

#from urllib.request import Request, urlopen


class RequestState(AbsDownloadState):
	
	def setFirstHandler(self, firstHandler):
		self.__firstHandler = firstHandler

	def handle(self, task):
		if( isinstance(task, str) ):
			req = Request('GET', task)
			request = req.prepare()
		elif( isinstance(task, Request) ):
			request = task.prepare()
			#print('Call First Requests Handler: ' + task.url)
		return self.__firstHandler.handle(request)
			
