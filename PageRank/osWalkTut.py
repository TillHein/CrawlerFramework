import os

path = '/var/tmp/crawler'

for root, dirs, files in os.walk(path):
	for name in files:
		print(os.path.join(root, name))
		#print(name + '--Verzeichnis: ' + root.split('/')[4])
#	for name in dirs:
#		print(name + '--Verzeichnis: ' + root)

