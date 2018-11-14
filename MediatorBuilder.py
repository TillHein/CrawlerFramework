from DownloadStateContextBuilder import DownloadStateContextBuilder
from CrawlerMediator import CrawlerMediator
from FrontierContext import FrontierContext
from StoreContext import StoreContext
import config as cfg

class MediatorBuilder:

	def __init__(self):
		self.mediator = CrawlerMediator()


	def construct(self):
		downloadStateContext = self.buildDownloadState()
		downloadStateContext.setMediator(self.mediator)
		self.mediator.setDownloadStateContext(downloadStateContext)
		
		frontierContext = self.buildFrontier()
		self.mediator.setFrontierContext(frontierContext)

		storeContext = self.buildStore()
		self.mediator.setStoreContext(storeContext)

	def buildFrontier(self):
		frontierContext = FrontierContext()

		module = __import__(cfg.frontier)
		frontierClass = getattr(module, cfg.frontier)
		frontierContext.setStrategy(frontierClass())

		for l in cfg.initialList:
			frontierContext.queue(l)
		
		return frontierContext
		


	def buildStore(self):
		storeContext = StoreContext()
		
		module = __import__(cfg.store)
		storeClass = getattr(module, cfg.store)

		storeContext.setStrategy(storeClass())
		return storeContext


	def buildDownloadState(self):
		downloadStateContextBuilder = DownloadStateContextBuilder()
		downloadStateContextBuilder.construct()
		return downloadStateContextBuilder.downloadStateContext
		
