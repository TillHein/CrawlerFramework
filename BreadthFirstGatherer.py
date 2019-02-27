from AbsFrontierStrategy import AbsFrontierStrategy
import urllib
import datetime
class BreadthFirstGatherer(AbsFrontierStrategy):
    def queue(self, link):
        try:
            link = self.__canonicalizeLinks(link)
        except Exception as e:
            print('Frontier: Error canonicalizing link' + str(e))
            return True
        try:
            hashUrl = self.__parseUrl(link)
        except Exception:
            print('Frontier: Error stripping URL')
            return True
        try:
            if str(hashUrl) not in self.visited:
                self.frontier.insert(0, link)
                self.visited[hashUrl] = 1
                #print('Frontier: ' + link + ' added')
        except Exception:
            print('Frontier: Error ')
        return True

    def dequeue(self):
        if self.max > 0:
            self.max = self.max - 1
            return self.frontier.pop()
        else:
            print("Frontier: Reached Crawl Limit")
            return None

    def size(self):
        return len(self.frontier)

    def __parseUrl(self, url):
        parsedUrl = urllib.parse.urlparse(url)
        return parsedUrl.netloc + parsedUrl.path

    def __init__(self):
        self.frontier = list()
        #{link: layer}
        self.visited = {}
        self.layer = 0
        self.count = 0
        self.max = 20


    def __canonicalizeLinks(self, link):
    # Remove Port
    # Add trailing slash (root and guessed directorys)
    # remove Fragments and options
    # resolve Path (http://cs.india.edu/a/./../b/ -> http://cs.india.edu/b/
    # Remove default filenames (index.html)
    # decode needlessly encoded characters like '%7' -> '~'
    # encode forbidden characters like ' ' -> '%20'
        link = link.replace('///', '//')
        parsedLink = urllib.parse.urlparse(link)
        scheme = parsedLink.scheme
        netloc = parsedLink.hostname
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        netloc = 'localhost/crawler/' + netloc
        path = parsedLink.path
        steps = [str(f) for f in path.split('/') if f.strip()]
        steplen = len(steps)
        #only netloc -> create index.html
        if (steplen == 0):
            if path.endswith('/'):
                path = path[:-1]
            path = path + '/' + 'index.html'
        elif '.' not in steps[steplen-1]:
            if path.endswith('/'):
                path = path[:-1]
            path = path + '.html'

        """
        if (len(path) == 0):
            path = 'index.html'
        elif (path.endswith('/')):
            path = path[:-1] + '.html'
        elif not ((path.endswith('.html')) or (path.endswith('.htm'))):
            path = path + '.html'
        """            
        qs = parsedLink.query
        #scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(link)
        path = urllib.parse.quote(path, '/%')
        qs = urllib.parse.quote_plus(qs, ':&=')
        anchor = ''
        scheme = 'http'
        return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))
