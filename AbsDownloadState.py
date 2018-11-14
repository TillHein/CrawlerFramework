from abc import ABC, abstractmethod, ABCMeta

class AbsDownloadState(metaclass=ABCMeta):

	def setContext(self, context):
		self.__context = context

	@abstractmethod
	def handle(self, task):
		pass 


