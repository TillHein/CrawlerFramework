from AbsDownloadState import AbsDownloadState
import requests
#import signal
#import datetime
#from urllib.request import urlopen
#from urllib.error import URLError
#from Response import Response

#def signal_handler(signum, frame):
#   with open( 'timeout.log' , 'a' )  as t:
#       t.write('TIMEOUT: ' + str(datetime.datetime.now()))
#   raise Exception ('timed out')

class DownloadState(AbsDownloadState):


    #@return Respnose Contains Downloaded Site
    def handle(self, task):
        session = requests.Session()
        #signal.signal(signal.SIGALRM, signal_handler)
        #signal.alarm(10)
        try:
            response = session.send(task, timeout = 10.0)
        #TODO: Add Logfile entries for Exception hits
        except Exception as e:
            print('Error in DownloadState.py: ' + task.url)
            return None
        return response
