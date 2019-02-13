from HTMLExtractor import HTMLExtractor

f = open('/Users/webcrawler/Projects/Bachelor/CrawlerDataZip/crawler/aoh.com/index.html','r')
htmle = HTMLExtractor()

htmle.regextractAuthority(f)
f.close()
