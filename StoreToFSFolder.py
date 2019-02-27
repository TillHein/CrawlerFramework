from AbsStoreStrategy import AbsStoreStrategy
from urllib.parse import urlparse, unquote, unquote_plus, urlunsplit
import os
import shutil
from requests import Response
import random
import string
# from http.client import HTTPResponse

class StoreToFSFolder:

    def __init__(self):
        folder = ''.join([random.choice(string.ascii_letters) for n in range (16)])
        self.path = '/Users/webcrawler/Projects/Bachelor/Testdaten/found/' + folder + '/'
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        os.makedirs(self.path)

    def store(self, obj):
        if not isinstance(obj, Response):
            print('Wrong type: exit Store')
            return
        try:
            link = self.__decanonicalizeLinks(obj.url)
        except Exception as e:
            print('STORE: Error in parsing: ' + str(e))
            link = obj.url
        if (obj.status_code != 200):
            #write textdocName equals errorcode + url
            filename = self.path + str(obj.status_code) + '_' + link.replace('/', '')
            self.__write(filename, b'')
        else:
            ressourcename = self.path.split('/')
            filename = self.path + link.replace('/', '')
            if ('.' not in ressourcename[-1]) and (len(ressourcename[-1]) > 0):
                filename = filename + '.html'
            self.__write(filename, obj.content)
        return  

    def __write(self, path, content):
        try:
            with open(path, 'wb') as f:
                f.write(content)
        except Exception as e:
            print('STORE: Error wrinting to file' + str(e))
            return 

    def __decanonicalizeLinks(self, link):
    # Remove Port
    # Add trailing slash (root and guessed directorys)
    # remove Fragments and options
    # resolve Path (http://cs.india.edu/a/./../b/ -> http://cs.india.edu/b/
    # Remove default filenames (index.html)
    # decode needlessly encoded characters like '%7' -> '~'
    # encode forbidden characters like ' ' -> '%20'
        link = str(link)
        parsedLink = urlparse(link)
        scheme = parsedLink.scheme
        netloc = parsedLink.hostname
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        path = parsedLink.path
        qs = parsedLink.query
        #scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(link)
        path = unquote(path)
        qs = unquote_plus(qs)
        anchor = ''
        return urlunsplit((scheme, netloc, path, qs, anchor))
