from AbsStoreStrategy import AbsStoreStrategy

class printStore:
	def __init__(self):
		self.count = 0	
	def store(self, obj):
		self.count = self.count + 1
		print("Store#: " + str(self.count))
		print(obj.content)
		return
