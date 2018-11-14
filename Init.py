import Downloader
import BreadthFirst
import HTMLExtractor

frontier = BreadthFirst.BreadthFirst()
dl = Downloader.Downloader()
extractor = HTMLExtractor.HTMLExtractor()
enquedHashList = {}

print (dl.count)

frontier.queue('https://de.wikipedia.org/wiki/Jython')
frontier.queue('https://de.wikipedia.org/wiki/CPython')
link = frontier.dequeue()
while(link):
	#print(link)
	#Creating a new Extractor object leads to a clear link attribute
	#extractor = HTMLExtractor.HTMLExtractor()
	#extractor.setStartUrl(link)
	res = dl.fetch(link)
	if res != None:
		links = extractor.extract(res)
		for newLink in links:
			if newLink not in enquedHashList:
				frontier.queue(newLink)
				print(str(frontier.size()))
				enquedHashList[newLink] = 1
				print("Found new Link: - " + str(newLink))
			else:
				enquedHashList[newLink] = enquedHashList[newLink] +1
				#print(link + "Anzahl:" + str(enquedHashList[newLink]))
		print ("Total: " + str(dl.count))
	link = frontier.dequeue()
