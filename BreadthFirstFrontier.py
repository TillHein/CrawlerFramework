from AbsFrontierStrategy import AbsFrontierStrategy
class BreadthFirstFrontier(AbsFrontierStrategy):

	def queue(self, link):
		self.frontier.insert(0,link)
		return True

	def dequeue(self):
		if len(self.frontier)>0:
			return self.frontier.pop()
		else:
			return None

	def size(self):
		return len(self.frontier)


	def __init__(self):
		self.frontier = list()
