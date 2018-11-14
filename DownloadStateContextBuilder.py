from DownloadStateContext import DownloadStateContext
from RequestState import RequestState 
from DownloadState import  DownloadState
from ResponseState import  ResponseState
import config as cfg
import operator

class DownloadStateContextBuilder:

	def __init__(self):
		self.downloadStateContext = DownloadStateContext()


	def construct(self):
		requestState = self.buildRequestState()
		self.downloadStateContext.defineRequestState(requestState)
		downloadState = self.buildDownloadState()
		self.downloadStateContext.defineDownloadState(downloadState)
		responseState = self.buildResponseState()
		self.downloadStateContext.defineResponseState(responseState)


	def buildRequestState(self):
		module = __import__("RequestHandler")
		requestState = RequestState()
		#sort RequestHandler by their Priority (lowest first)
		sortedRequestHandler = sorted(cfg.requestHandler.items(), key=operator.itemgetter(1))
		setFirst = True
		base = requestState
		for handler in sortedRequestHandler:
			nextHandlerClass = getattr(module, handler[0])
			nextHandler = nextHandlerClass()
			nextHandler.setContext(self.downloadStateContext)
			if setFirst:
				base.setFirstHandler(nextHandler)
				setFirst = False
			else:
				base.setSuccessor(nextHandler)
			base = nextHandler
			base.setSuccessor(None)
		return requestState	


	def buildDownloadState(self):
		downloadState = DownloadState()
		return downloadState


	def buildResponseState(self):
		module = __import__("ResponseHandler")
		responseState = ResponseState()
		#sort ResponseHandler by their Priority (lowest first)
		sortedResponseHandler = sorted(cfg.responseHandler.items(), key=operator.itemgetter(1))
		setFirst = True
		base = responseState
		for handler in sortedResponseHandler:
			nextHandlerClass = getattr(module, handler[0])
			nextHandler = nextHandlerClass()
			nextHandler.setContext(self.downloadStateContext)
			if setFirst:
				base.setFirstHandler(nextHandler)
				setFirst = False
			else:
				base.setSuccessor(nextHandler)
			base = nextHandler
			base.setSuccessor(None)
		return responseState

