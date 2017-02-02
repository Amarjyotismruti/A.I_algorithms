"""|samarjyo@andrew.cmu.edu|27 November 2016|"""
"""|Game Theory|Stackleberg stratergy using multiple LPs|"""

import numpy as np
from cvxopt import matrix, solvers
from copy import deepcopy



def preprocess(U):

    A,B=[],[]
    z1=list(np.zeros(len(U)))
    o1=np.ones(len(U))
    no1=np.negative(o1)
    A.append(list(o1))
    A.append(list(no1))
    B+=[1,-1]

    for i in xrange(len(U)):
        z2=deepcopy(z1)
        z3=deepcopy(z1)
        z2[i],z3[i]=1,-1
        A+=[z2,z3]
        B+=[1,0]

    A,B=matrix(np.array(A).astype(float)),matrix(np.array(B).astype(float))
    return A,B

def modify_ABC(A,B,s2,u2,u1):

    C=np.negative(u1[:,s2].astype(float))
    A1,B1=np.array(deepcopy(A)),np.array(deepcopy(B))
    for i in xrange(len(u2)):
        buf=u2[:,i]-u2[:,s2]
        A1=np.append(A1,[buf],axis=0)
        B1=np.append(B1,[0])
    
    return matrix(A1),matrix(B1),matrix(C)




def stackelberg(u1, u2):
    '''
    Compute the optimal Stackelberg strategy for the given 2-player normal form game.
        
    Arguments:
        u1: a list of lists representing the utility function for player 1
        u2: a list of lists representing the utility function for player 2
        
    Return:
        (u,x1,s2) where
            u is the expected utility for player 1 of mixed strategy x1 and s2
            x1 is a list of probabilities representing the mixed strategy of player 1
            s2 is the index (0-based) of the pure strategy for player 2
    '''
    solvers.options['show_progress'] = False
    #initialize the LP matrices
    A,B=preprocess(u1)
    u1=np.array(u1)
    u2=np.array(u2)
    stratergies={}

    #loop over the true follower stratergies
    for i in xrange(u1.shape[0]):
        a,b,c=modify_ABC(A,B,i,u2,u1)
        sol=solvers.lp(c,a,b)
        #save all the stratergies that give optimal solution
        if sol['status']=='optimal':
            stratergies[-sol['primal objective']]=(i,list(sol['x']))
    ans=max(stratergies)
    output=(ans, stratergies[ans][1], stratergies[ans][0] )

    return output







if __name__=='__main__':
    # u1 = [[-1, -9], [0, -6]]
    # u2 = [[-1, 0], [-9, -6]]
    u1 = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    u2 = [[0, 1, -1], [-1, 0, 1], [1, -1, 0]]
    print stackelberg(u1, u2)