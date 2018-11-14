import abc

class AbsResponseHandler(metaclass=abc.ABCMeta):

	def setContext(self, context):
		self._context = context

	def setSuccessor(self, successor=None):
		self._successor = successor


	#handle has to return either None, String, Response or Request
	@abc.abstractmethod
	def handle(self, response):
		pass
