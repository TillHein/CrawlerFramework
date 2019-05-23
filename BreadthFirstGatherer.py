from AbsFrontierStrategy import AbsFrontierStrategy
import urllib
import datetime
class BreadthFirstGatherer(AbsFrontierStrategy):

    def queue(self, link):
        try:
           self. __addToFrontier(link)
        except Exception as e:
            print("Failed to queue link" + str(link) + str(e))
        return True

    def __addToFrontier(self, link):
        try:
            canonicalizedLink = self.__canonicalizeLinks(link)
        except Exception as e:
            raise Exception("Error canonicalizing Link: " + str(link) + " " + str(e))
        stripedLink = self.__stripUrl(canonicalizedLink)
        if not self.__linkAlreadyInRepository(stripedLink):
            self.frontier.insert(0, canonicalizedLink)
            self.lenght = self.lenght + 1
            print(canonicalizedLink)
            self.__addLinkToRepository(stripedLink)

    def __linkAlreadyInRepository(self, link):
        if link in self.visited:
            return True
        return False

    def __addLinkToRepository(self, link):
        self.visited[link] = 0

    def dequeue(self):
        print(self.frontier)
        if self.lenght > 0:
            self.count = self.count + 1
            self.lenght = self.lenght - 1
            return self.frontier.pop()
        else:
            print("Frontier is empty")
            return None

    def size(self):
        return len(self.frontier)

    def __stripUrl(self, url):
        parsedUrl = urllib.parse.urlparse(url)
        return parsedUrl.netloc + parsedUrl.path

    def __init__(self):
        self.frontier = list()
        self.visited = {}
        self.layer = 0
        self.count = 0
        self.lenght = 0


    def __canonicalizeLinks(self, link):
    # Remove Port
    # Add trailing slash (root and guessed directorys)
    # remove Fragments and options
    # resolve Path (http://cs.india.edu/a/./../b/ -> http://cs.india.edu/b/
    # Remove default filenames (index.html)
    # decode needlessly encoded characters like '%7' -> '~'
    # encode forbidden characters like ' ' -> '%20'
        if not type(link) is str:
            raise Exception("Link is not in string Format")
        if link == "":
            raise Exception("Link contains empty string")
        link = link.replace('///', '//')
        parsedLink = urllib.parse.urlparse(link)
        scheme = parsedLink.scheme
        netloc = parsedLink.hostname
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        path = parsedLink.path
        qs = parsedLink.query
        path = urllib.parse.quote(path, '/%')
        qs = urllib.parse.quote_plus(qs, ':&=')
        anchor = ''
        if scheme == 'http':
            scheme = 'https'
        return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))
