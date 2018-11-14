import signal
import datetime

def signal_handler(signum, frame):
	with open( 'timeout.log' , 'a' )  as t:
		t.write('TIMEOUT: ' + str(datetime.datetime.now()))
	raise Exception ('timed out')

class CrawlerMediator:

	"""Call this function to start the crawl process"""
	def crawl(self):
		nextUrl = self._frontier.dequeue()
		while(nextUrl != None):
			try:
				signal.signal(signal.SIGALRM, signal_handler)
				signal.alarm(10)
				self._download.download(nextUrl)
			except Exception:
				print('MEDIATOR: Unknown error in download')
			try:
				nextUrl = self._frontier.dequeue()
			except Exception:
				print('MEDIATPOR: Dequeue Error')
		return

	"""Function used by DownloadStateContext to Store new URLs"""
	def queue(self, url):
		try:
			self._frontier.queue(url)
		except Exception:
			print('MEDIATOR: Unknown error in queue')
		return

	"""Function used by DownloadStateContext to Store Crawled Information
	 Implementation unclear"""
	def store(self, data):
		try:
			self._store.store(data)
		except Exception:
			print('MEDIATOR: Unknown error in queue')
		return
	
	"""set Functions to connect the different contexts"""
	def setFrontierContext(self, frontier):
		self._frontier = frontier
		return

	def setStoreContext(self, store):
		self._store = store
		return
	
	def setDownloadStateContext(self, download):
		self._download = download
		return


