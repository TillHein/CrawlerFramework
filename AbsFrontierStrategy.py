from abc import ABC, abstractmethod, ABCMeta

class AbsFrontierStrategy(metaclass=ABCMeta):


	@abstractmethod
	def queue(self, link):
		pass 

	@abstractmethod
	def dequeue(self):
		pass 
