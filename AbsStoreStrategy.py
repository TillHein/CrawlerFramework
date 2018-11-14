from abc import ABC, abstractmethod, ABCMeta

class AbsStoreStrategy(metaclass=ABCMeta):

	@abstractmethod
	def store(self, obj):
		pass 

