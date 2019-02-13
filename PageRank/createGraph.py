import networkx as nx
import os
import threading
import json
from HTMLExtractor import HTMLExtractor

##Pagerank Algorithm taken from https://www.geeksforgeeks.org/page-rank-algorithm-implementation/

# :%s/ \{6}/\t/g
# path = '/Volumes/INTENSO/Dt'
path = '/media/mumm/INTENSO/Dt'

class PageRank:

    def setPath(self,path):
        self.path = path

    # returns directet NetworkX Graph with nodes equal to domains and edges equal to Links between those
    def createGraph(self):
        G = nx.DiGraph()
        nodes = self._createNodeList()
        for node in nodes:
            G.add_node(node)
        G = self._createEdges(G)
        return G

    # returns List of Domainnames
    def _createNodeList(self):
        nodes = os.listdir(self.path)
        return nodes

    # adds Edges to the Graph G and returns it
    def _createEdges(self,G):
        count = 0
        threads = []
        for root, dirs, files in os.walk(self.path):
            for name in files:
                filepath = os.path.join(root, name)
                domain = root.split('/')[7]
                current = CheckFiles(filepath, domain)
                threads.append(current)
                current.start()
        for t in threads:
            count = count +1
            t.join()
            print(str(count))
            for link in t.links:
                print('add Edge: '+ t.domain + link)
                G.add_edge(t.domain, link)
        return G

#      #returns list with all outlinks from sourcefile
#      def _addLinksFrom(self,filepath, G, domain):
#          print('collecting links from' + filepath)
#          f = open(filepath, 'r')
#          links = self.HTMLE.extract(f)
#          f.close()
#          for link in links:
#              lock.acquire()
#              G.add_edge(domain, link)
#              lock.release()
#          return


    def getPageRank(self,D, d=0.85, max_iter=60, tol=1.0e-6, weight='weight'):
        print('BEGINN PAGE RANK CALCULATION')
        if len(D) == 0:
            return {}
        G = nx.stochastic_graph(D, weight=weight)
        N = G.number_of_nodes()
        print('Number of nodes: ' + str(N))
        x = dict.fromkeys(G,1.0 / N)
        p = dict.fromkeys(G,1.0 / N)
        dangling_weights = x
        dangling_nodes = [n for n in G if G.out_degree(n, weight=weight) == 0.0]
        for _ in range(max_iter):
            print('Enter iteration ' + str(_))
            xlast = x 
            x = dict.fromkeys(xlast.keys(), 0) 
            danglesum = d * sum(xlast[n] for n in dangling_nodes) 
            for n in x: 

                # this matrix multiply looks odd because it is 
                # doing a left multiply x^T=xlast^T*W 
                for nbr in G[n]: 
                    x[nbr] += d * xlast[n] * G[n][nbr][weight]
                    x[n] += danglesum * dangling_weights[n] + (1.0 - d) * p[n] 

            # check convergence, l1 norm 
            err = sum([abs(x[n] - xlast[n]) for n in x]) 
            if err < N*tol: 
                print("pagerank: power iteration failed to converge in" + str(iterations))    
            return x 
        #raise nx.NetworkXError('pagerank: power iteration failed to converge ''in %d iterations.' % max_iter)

#    def __init__(self):
#       lock = thread.allocate_lock()
#       numlock = thread.allocate_lock()
#       numberOfThreads = 0
#       threadStarted = False
#          G = createGraph()
#          print(G.adj)

    def saveGraph(self, d, name):
        data = nx.convert.to_dict_of_dicts(d, nodelist=None,edge_data=None)
        with open(name, 'w') as fp:
            json.dump(data, fp, sort_keys=False, ensure_ascii=False, indent=4)
        return True

class CheckFiles(threading.Thread):
    def __init__(self, filepath, domain):
        threading.Thread.__init__(self)
        self.HTMLE = HTMLExtractor()
        self.links = []
        self.filepath = filepath
        self.domain = domain

    def run(self):
        print('collecting links from' + self.filepath)
        try:
            f = open(self.filepath, 'r')
        except:
            print("Error: failed to open " + str (self.filepath))
            f.close()
            return
        try:
            self.links = self.HTMLE.regextractAuthority(f)
        except:
            print("Error: failed to extract Links")
        f.close()


if __name__ == "__main__":
    PR = PageRank()
    PR.setPath('/Users/webcrawler/Projects/Bachelor/CrawlerDataZip/crawler/')
    G = PR.createGraph()
    print('graph complete')
    print('saving graph')
    if (PR.saveGraph(G, 'data.json') == True):
        print('Graph saved')
    else:
        print('saving graph failed')
    print()
    pr = PR.getPageRank(G)
    print('pagerank complete')
    print('saving pagrerank')
    jpr = json.dumps(pr, ensure_ascii=False)
    try:
        s = open('pagerank.txt', 'w')
        s.write(jpr)
    except Exception as ERR:
        print("wirte to pagerank.txt failed")
    #if (PR.saveGraph(pr, 'pagerank.json') == True):
    #    print('pagerank saved')
    #else:
    #    print('saving pagerank failed')
    print(pr)
