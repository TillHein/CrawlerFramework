from requests import Request, Response, PreparedRequest
# from http.client import HTTPResponse

class DownloadStateContext:

	def setMediator(self,mediator):
		self.__mediator = mediator
		return

	def changeState(self, state):
		self.__state = state
		return

	def defineRequestState(self, state):
		self.REQUEST = state
		return

	def defineDownloadState(self, state):
		self.DOWNLOAD = state
		return
	
	def defineResponseState(self, state):
		self.RESPONSE = state
		return

	#Add handling for Request Changes based on return types
	#request -> DOWNLOAD
	#response -> RESPONSE
	#String -> REQUEST
	#None -> Return
	def download(self, url):
		while(url != None):
			if isinstance(url, PreparedRequest):
				self.changeState(self.DOWNLOAD)
			elif isinstance(url, Response):
				self.changeState(self.RESPONSE)
			elif isinstance(url, str):
				print('Handle: ' + url)
				self.changeState(self.REQUEST)
			url = self.__state.handle(url)
		return

	def queue(self, url):
		self.__mediator.queue(url)

	def store(self, obj):
		self.__mediator.store(obj)
