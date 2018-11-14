from createGraph import Graph


class PageRank:

	def getPageRank(G, d=0.85, max_iter=60, tol=1.0e-6):
		if len(G) == 0:
			return {}
		
		N = G.number_of_nodes()
		x = dict.fromkeys(G,1.0 / N)
		p = dict.fromkeys(G,1.0 / N)
		dangling_weights = x

		for _ in range(max_iter): 
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
