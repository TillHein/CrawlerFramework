from http.client import HTTPResponse
from AbsDownloadState import AbsDownloadState
from urllib.request import Request

class ResponseState(AbsDownloadState):

	def handle(self, task):
		#if( isinstance(task, HTTPResponse) ):
		#	self._response = task
		#else:
		#	return None #Set Return type to catch Errors (maybe add Exception Handling)
		#	
		return self.__firstHandler.handle(task)

	def setFirstHandler(self, firstHandler):
		self.__firstHandler = firstHandler
