from AbsStoreStrategy import AbsStoreStrategy
from urllib.parse import urlparse, unquote, unquote_plus, urlunsplit
import os
import shutil
from requests import Response
# from http.client import HTTPResponse

class StoreToFilesystem:


	def __init__(self):
		self.path = '/var/tmp/crawler'
		if os.path.exists(self.path):
			shutil.rmtree(self.path)
		os.makedirs(self.path)

	def store(self, obj):
		if not isinstance(obj, Response):
                    print('Wrong type: exit Store')
                    return
		try:
			link = self.__decanonicalizeLinks(obj.url)
			parsedLink = urlparse(link)
		except Exception:
			print('STORE: Error in parsing')
			return
		localPath = self.path + '/' + parsedLink.netloc
		try:
			if not os.path.exists(localPath):
				#print('path created' + localPath)
				os.makedirs(localPath, exist_ok=True)
		except Exception:
			print('STORE: Error creating path')
			return
		urlpath = parsedLink.path
		folders = [str(f) for f in urlpath.split('/') if f.strip()]
		folderLen = len(folders)
		#only netloc -> create index.html
		if (folderLen == 0):
			filename = localPath + '/' + 'index.html'
			#os.makedirs(os.path.dirname(filename), exist_ok=True)
			try:
				with open(filename, 'wb') as f:
					#print('WRITE TO: ' + filename)
					f.write(obj.content)
			except Exception:
				print('STORE: Error wrinting to file')
				return 
		else:
			i = 0
			while (i < (len(folders) -1)):
				localPath = localPath + '/' + folders[i]
				i = i + 1
			#for f in folders:
			#	localPath = localPath + '/' + f
			try:
				os.makedirs(localPath, exist_ok=True)
			except Exception as e:
				print('STORE: Error creating path')
				return 
			localPath = localPath + '/' + folders[i]
			if '.' not in folders[i]:
				localPath = localPath + '.html'
			try:
				with open(localPath, 'wb') as f:
					#print('WRITE TO: ' + localPath)
					#print(obj.content)
					f.write(obj.content)
			except Exception:
				print('STORE: Error writing to file')
				return
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
		if scheme == 'http':
			scheme = 'https'
		return urlunsplit((scheme, netloc, path, qs, anchor))
