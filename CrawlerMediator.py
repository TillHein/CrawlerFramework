import signal
import datetime
import config

def timeout_handler(signum, frame):
    with open( 'timeout.log' , 'a' )  as t:
        t.write('TIMEOUT: ' + str(datetime.datetime.now()))
    raise Exception ('timed out')

class CrawlerMediator:
    
    def __init__(self):
        self._secondsUntilTimeout = config.timeout
        self._nextUrl = ""

    """Call this function to start the crawl process"""
    def crawl(self):
        while(self._getNextUrl()):
            self._download()
        return

    def _getNextUrl(self):
        try:
            self._nextUrl = self._frontier.dequeue()
        except Exception as e:
            self._nextUrl = None
            print('MEDIATPOR: Dequeue Error' + str(e))
            return False
        return True if self._hasNextUrl() else False

    def _hasNextUrl(self):
        return True if self._nextUrl is not None else False

    def _download(self):
        self._configureTimeoutHandler()
        try:
            self._downloader.download(self._nextUrl)
        except Exception as e:
            print('MEDIATOR: Unknown error in download' + str(e))

    def _configureTimeoutHandler(self):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self._secondsUntilTimeout)

    """Function used by DownloadStateContext to Store new URLs"""
    def queue(self, url):
        try:
            self._frontier.queue(url)
        except Exception as e:
            print('MEDIATOR: Unknown error in queue: ' + str(e))
        return

    """Function used by DownloadStateContext to Store Crawled Information
     Implementation unclear"""
    def store(self, data):
        try:
            self._store.store(data)
        except Exception as e:
            print('MEDIATOR: Unknown error in store' + str(e))
        return
    
    """set Functions to connect the different contexts"""
    def setFrontierContext(self, frontier):
        self._frontier = frontier
        return

    def setStoreContext(self, store):
        self._store = store
        return

    def setDownloadStateContext(self, downloader):
        self._downloader = downloader
        return