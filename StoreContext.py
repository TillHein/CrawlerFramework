class StoreContext:
	"""
	Defines interface of interest for store requests
	""" 

	def setStrategy(self, strategy):
		self._strategy = strategy

	def store(self, obj):
		self._strategy.store(obj)

