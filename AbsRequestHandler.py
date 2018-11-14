import abc

class AbsRequestHandler(metaclass=abc.ABCMeta):

	def setContext(self, context):
		self._context = context

	def setSuccessor(self, successor=None):
		#print('set successor absrequestHandler')
		self._successor = successor
#handle has to return either None, String, or Request
#it is technacally possible to return a Response but it's not advised
	@abc.abstractmethod
	def handle(self, response):
		pass
