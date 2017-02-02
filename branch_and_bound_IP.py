## samarjyo@andrew.cmu.edu##
##Nov 5 2016##
##Branch and Bound Integer Programming solution using LP relaxation pruning##
import numpy as np
from copy import deepcopy
from cvxopt import matrix, solvers

# Solve the binary integer program using branch and bound
# Minimize Cx given Ax <= b and all xs are binary
# Note that A does not restrict the varibles to integer values
#
# A: mxn 2d list specifying constraints
# B: m 1d list specifying constraints
# C: n 1d list specifying the optimization function
#
# returns (val, var, expandlist)
# val is the value of the objective (None if no feasible assignment)
# var is a variable assignment list (None if no feasible assignment)
# expandlist: list of expanded nodes specified by assigned variables

def children(action,node):
	cur_node=deepcopy(node)
	if action=='left':
		cur_node.append(0)
	else:
		cur_node.append(1)

	return cur_node

def preproces(A,B,C):
	#matrix preprocessing
	for j in xrange(len(C)):
		con_bfr_1,con_bfr_2=[],[]
		for i in xrange(len(C)):
			con_bfr_1.append(0)
			con_bfr_2.append(0)
		con_bfr_1[j]=-1
		con_bfr_2[j]=1	
		A.append(con_bfr_1)
		A.append(con_bfr_2)
		B.append(0)
		B.append(1)

	A,B,C=np.array(A).astype(float),np.array(B).astype(float),np.array(C).astype(float)
	A,B,C=matrix(A),matrix(B),matrix(C)

	return A,B,C

def modify_matrices(A,B,C,node):
	var=len(node)
	C1=deepcopy(np.array(C))
	B1=deepcopy(np.array(B))
	A1=deepcopy(np.array(A))

	C1=C1[var:].astype(float)
	A_1=A1[:,0:var]
	B1=B1.T-A_1.dot(np.array(node))
	B1=B1.astype(float)
	A1=A1[:,var:].astype(float)


	return A1,B1.T,C1

def check_binary(x):
	x=np.array(x)
	# print 'x', x
	b=np.logical_or(x<=0.000001,x>=0.999999)
	return np.all(b)

def check_optimal(sol):
	return sol['status']=='optimal'

def process_solution(sol):
	sol1=deepcopy(sol)
	for i,val in enumerate(sol):
		if val>=0.999999:
			sol1[i]=1.0
		if val<=0.000001:
			sol1[i]=0.0
	return sol1



def solve(A, B, C):

	solvers.options['show_progress'] = False
	node=[]
	best_value=[]
	frontier,explored=[],[]


	#solve the LP without assignments.
	explored.append(node)
	A,B,C=preproces(A,B,C)
	solution = solvers.lp(C, A, B)
	if check_binary(solution['x']) and check_optimal(solution):
		return (solution['primal objective'],list(solution['x']),explored)
	#Expand the root node
	frontier.append(children('right',node))
	frontier.append(children('left',node))
	# print solution['x']
	# print np.array(list(solution['x'])).astype(int)

	
	while frontier:

		node=frontier.pop()
		explored.append(node)


		if len(node)!=len(C):
			a,b,c=modify_matrices(A,B,C,node)
			a,b,c=matrix(a),matrix(b),matrix(c)
			solution=solvers.lp(c,a,b)

			#print list(solution['x']), check_binary(solution['x'])


			if check_optimal(solution):
				value=solution['primal objective'] + float(np.array(node).dot(np.array(C[0:len(node)])))

				if best_value:
					if value<=best_value[0]:
						if check_binary(solution['x']):
							best_value=(value, node + list(solution['x']))
							continue
						frontier.append(children('right',node))
						frontier.append(children('left',node))
					else:
						continue
				else:
					if check_binary(solution['x']):
						best_value=(value,node + list(solution['x']))
						continue
					frontier.append(children('right',node))
					frontier.append(children('left',node))
			else:
				continue
		else:
			A,B,C,node=np.array(A),np.array(B),np.array(C),np.array(node)

			if best_value:
				if np.all(A.dot(node)<=B.T) and np.all(C.T.dot(node)<best_value[0]):
					best_value=(C.T.dot(node),node)
			else:
				if np.all(A.dot(node)<=B.T):
					best_value=(C.T.dot(node),node)

	if best_value:
		sol1=process_solution(list(best_value[1]))
		return (float(best_value[0]), sol1, explored)
	else:
		return (None,None,[[]])











if __name__=='__main__':

	print solve([[-2, -1, -8, 10], [5, -6, 3, 8], [6, -7, -7, 9]], [6, 5, 2], [-10, 12, -5, -4])







    	
