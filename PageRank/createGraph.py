import networkx as nx
import os
from HTMLExtractor import HTMLExtractor

path = '/Volumes/INTENSO/Dt'

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
		for root, dirs, files in os.walk(self.path):
			for name in files:
				links = self._getLinksFrom(os.path.join(root, name))
				domain = root.split('/')[4]
				for link in links:
					G.add_edge(domain, link)
		return G

	#returns list with all outlinks from sourcefile
	def _getLinksFrom(self,filepath):
		print('collecting links from' + filepath)
		f = open(filepath, 'r')
		links = self.HTMLE.extract(f)
		f.close()
		return links


	def getPageRank(self,G, d=0.85, max_iter=60, tol=1.0e-6):
		print('BEGINN PAGE RANK CALCULATION')
		if len(G) == 0:
			return {}
		
		N = G.number_of_nodes()
		print('Number of nodes: ' + str(N))
		x = dict.fromkeys(G,1.0 / N)
		p = dict.fromkeys(G,1.0 / N)
		dangling_weights = x

		for _ in range(max_iter):
			print('Enter iteration ' + str(_))
			xlast = x 
			x = dict.fromkeys(xlast.keys(), 0) 
			danglesum = d * sum(xlast[n] for n in dangling_nodes) 
			for n in x: 
 
				# this matrix multiply looks odd because it is 
				# doing a left multiply x^T=xlast^T*W 
				for nbr in W[n]: 
					x[nbr] += d * xlast[n] * W[n][nbr][weight] 
					x[n] += danglesum * dangling_weights[n] + (1.0 - d) * p[n] 
  
			# check convergence, l1 norm 
			err = sum([abs(x[n] - xlast[n]) for n in x]) 
			if err < N*tol: 
				return x 
		raise NetworkXError('pagerank: power iteration failed to converge ''in %d iterations.' % max_iter) 
	def __init__(self):
		self.HTMLE = HTMLExtractor()
#		G = createGraph()
#		print(G.adj)
	
if __name__ == "__main__":
	PR = PageRank()
	PR.setPath('/Volumes/INTENSO/Dt')
	G = PR.createGraph()
	pr = PR.getPageRank(G)
	print(pr)
