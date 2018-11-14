class FrontierContext:
	"""
	Defines interface of interest for frontier requests
	""" 

	def setStrategy(self, strategy):
		self._strategy = strategy

	def queue(self, link):
		self._strategy.queue(link)
	
	def dequeue(self):
		return self._strategy.dequeue()
