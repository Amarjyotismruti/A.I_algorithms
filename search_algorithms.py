################################################################################
# Input:
# grid is a 2D grid of the neighborhood
#     free spaces are 0
#     walls are -1
#     residences are 1
# start is a tuple (row, column) of the starting position
# 
# Output:
# An ordered list of expanded nodes represented as a list of tuples (row, column)
################################################################################
def dfs(grid, start):
    
    frontier_nodes,explored_nodes=[],[]
    residence_no,total_res=0,0
    start=list(start)
    breadth=len(grid[0])
    depth=len(grid)
    res_pos=[]
    ##Preprocess the grid
    for i in xrange(depth):
        for j in xrange(breadth):
            if grid[i][j]==1:
                total_res+=1
                res_pos.append([i,j])

    frontier_nodes.append(start)
    node=frontier_nodes[0]

    output=[]

    while len(node)<total_res+2:
       
        ##Get the current node
        node=frontier_nodes.pop()

        ##Compare the node with explored nodes
        if node not in explored_nodes:
            #print "loop"
            explored_nodes.append(node)
            ##Cycle detection-checking for goal
            if grid[node[0]][node[1]]==1 and [node[0], node[1]] not in node:
                node.append([node[0],node[1]])

            #print node

            ##DFS strategy
            if node[1]-1>=0:
                node_1=node[:]
                node_1[1]=node[1]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_1"
                    frontier_nodes.append(node_1)
            if node[0]+1<depth:
                node_1=node[:]
                node_1[0]=node[0]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_2"
                    frontier_nodes.append(node_1)
            if node[1]+1<breadth:
                node_1=node[:]
                node_1[1]=node[1]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_3"
                    frontier_nodes.append(node_1)
            if node[0]-1>=0:
                node_1=node[:]
                node_1[0]=node[0]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_4"
                    frontier_nodes.append(node_1)

    for i in xrange(len(explored_nodes)):
        output.append((explored_nodes[i][0],explored_nodes[i][1]))

    return output
            
################################################################################
# Input:
# grid is a 2D grid of the neighborhood
#     free spaces are 0
#     walls are -1
#     residences are 1
# start is a tuple (row, column) of the starting position
# 
# Output:
# An ordered list of expanded nodes represented as a list of tuples (row, column)
################################################################################
def bfs(grid, start):

    frontier_nodes,explored_nodes=[],[]
    residence_no,total_res=0,0
    start=list(start)
    breadth=len(grid[0])
    depth=len(grid)
    res_pos=[]
    ##Preprocess the grid
    for i in xrange(depth):
        for j in xrange(breadth):
            if grid[i][j]==1:
                total_res+=1
                res_pos.append([i,j])

    frontier_nodes.append(start)
    node=frontier_nodes[0]

    output=[]

    while len(node)<total_res+2:
        
        ##Get the current node
        node=frontier_nodes[0]
        del frontier_nodes[0]

        ##Compare the node with explored nodes
        if node not in explored_nodes:
            #print "loop"
            
            ##Cycle detection-checking for goal
            if grid[node[0]][node[1]]==1 and [node[0], node[1]] not in node:
                node.append([node[0],node[1]])
                
            #print node

            explored_nodes.append(node)
            ##DFS strategy
            if node[0]-1>=0:
                node_1=node[:]
                node_1[0]=node[0]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_1"
                    frontier_nodes.append(node_1)
            if node[1]+1<breadth:
                node_1=node[:]
                node_1[1]=node[1]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_2"
                    frontier_nodes.append(node_1)
            if node[0]+1<depth:
                node_1=node[:]
                node_1[0]=node[0]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_3"
                    frontier_nodes.append(node_1)
            if node[1]-1>=0:
                node_1=node[:]
                node_1[1]=node[1]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_4"
                    frontier_nodes.append(node_1)
    
    for i in xrange(len(explored_nodes)):
        output.append((explored_nodes[i][0],explored_nodes[i][1]))
            

    return output


# Default h-function that always returns 0
def admissible(data):
    return 0

################################################################################
# Input:
# grid is a 2D grid of the neighborhood
#     free spaces are 0
#     walls are -1
#     residences are 1
# start is a tuple (row, column) of the starting position
# hfunc is a function for computing the h-value of a search node that you will define
#     hfunc should take in one parameter and return a number
# 
# Output:
# An ordered list of expanded nodes represented as a list of tuples (row, column)
################################################################################
import heapq
import collections

def astar(grid, start, hfunc):
    # You need to decide on a node structure e.g. (pos, residences visited, f-value, parent node, ...)
    frontier_nodes,explored_nodes=[],[]
    start=list(start)
    breadth=len(grid[0])
    depth=len(grid)
    cost,priority=0,0
    total_res=0
    res_pos=[]
    ##Preprocess the grid
    for i in xrange(depth):
        for j in xrange(breadth):
            if grid[i][j]==1:
                total_res+=1
                res_pos.append([i,j])

    heapq.heappush(frontier_nodes,(cost,priority,start))
    node=frontier_nodes[0][2]

    output=[]

    while len(node)<total_res+2:
        
        ##Get the current node
        cost,_,node=heapq.heappop(frontier_nodes)

        ##Compare the node with explored nodes
        if node not in explored_nodes:
            #print "loop"
            
            ##Cycle detection-checking for goal
            if grid[node[0]][node[1]]==1 and [node[0],node[1]] not in node:
                node.append([node[0],node[1]])
                
            #print node
            
            explored_nodes.append(node)

            ##A* strategy
            if node[0]-1>=0:
                node_1=node[:]
                node_1[0]=node[0]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_1"
                    new_cost=hfunc([node_1,res_pos])
                    priority+=1
                    heapq.heappush(frontier_nodes,(new_cost,priority,node_1))
            if node[1]+1<breadth:
                node_1=node[:]
                node_1[1]=node[1]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_2"
                    new_cost=hfunc([node_1,res_pos])
                    priority+=1
                    heapq.heappush(frontier_nodes,(new_cost,priority,node_1))
            if node[0]+1<depth:
                node_1=node[:]
                node_1[0]=node[0]+1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_3"
                    new_cost=hfunc([node_1,res_pos])
                    priority+=1
                    heapq.heappush(frontier_nodes,(new_cost,priority,node_1))
            if node[1]-1>=0:
                node_1=node[:]
                node_1[1]=node[1]-1
                if grid[node_1[0]][node_1[1]]!=-1:
                    #print "append_4"
                    new_cost=hfunc([node_1,res_pos])
                    priority+=1
                    heapq.heappush(frontier_nodes,(new_cost,priority,node_1))
            #print frontier_nodes
            
            
            
            
            
    
    for i in xrange(len(explored_nodes)):
        output.append((explored_nodes[i][0],explored_nodes[i][1]))
            

    return output
    # You need a priority queue (e.g. heapq)
    # q = priority q
    
    # The central loop
    # while q is not empty, expand the top node, check if it's a goal, if not then push successors
    

################################################################################
# Input:
# data is up to you and your astar function, but should be related to a search node
# 
# Your simple heuristic should return the number of residences that haven't been visited
# 
# Output:
# the h-value for the related search node
################################################################################
def simple(data):
    node=data[0]
    res_pos=data[1]
    if [node[0],node[1]] in res_pos:
        return len(res_pos)+1-len(node)
    else:
        return len(res_pos)-len(node)+2

################################################################################
# Input:
# grid is a 2D grid of the neighborhood
# start is a tuple (row, column) of the starting position
# hfunc is a function for computing the h-value of a search node that you will define
#     hfunc should take in one parameter and return a number
# threshold is the cutoff for the h-value
# 
# Output:
# An ordered list of expanded nodes represented as a list of tuples (row, column)
################################################################################
def idastar(grid, start, hfunc):
    frontier_nodes,explored_nodes=[],[]
    start=list(start)
    breadth=len(grid[0])
    depth=len(grid)
    cost=0
    total_res=0
    res_pos=[]
    f_value,f_min=[],0
    ##Preprocess the grid
    for i in xrange(depth):
        for j in xrange(breadth):
            if grid[i][j]==1:
                total_res+=1
                res_pos.append([i,j])

    frontier_nodes.append((start,cost))
    node=frontier_nodes[0][0]

    pre_output=[]
    output=[]

    while len(node)<total_res+2:
        
        ##Get the current node
        node,cost=frontier_nodes.pop()

        ##Compare the node with explored nodes
        
        ##Cycle detection-checking for goal
        if grid[node[0]][node[1]]==1 and [node[0],node[1]] not in node:
            node.append([node[0],node[1]])
            
        explored_nodes.append(node)

        ##IDA* strategy
        if node[1]-1>=0:
            node_1=node[:]
            node_1[1]=node[1]-1
            if grid[node_1[0]][node_1[1]]!=-1:
                if node_1 not in explored_nodes:
                    new_cost=hfunc([node_1,res_pos])
                    cost_1=cost+1
                    f_v=cost_1+new_cost
                    if f_v<=f_min:
                        frontier_nodes.append((node_1,cost_1))
                    else:
                        heapq.heappush(f_value,f_v)
                
        if node[0]+1<depth:
            node_1=node[:]
            node_1[0]=node[0]+1
            if grid[node_1[0]][node_1[1]]!=-1:
                if node_1 not in explored_nodes:
                    new_cost=hfunc([node_1,res_pos])
                    cost_1=cost+1
                    f_v=cost_1+new_cost
                    if f_v<=f_min:
                        frontier_nodes.append((node_1,cost_1))
                    else:
                        heapq.heappush(f_value,f_v)

        if node[1]+1<breadth:
            node_1=node[:]
            node_1[1]=node[1]+1
            if grid[node_1[0]][node_1[1]]!=-1:
                if node_1 not in explored_nodes:
                    new_cost=hfunc([node_1,res_pos])
                    cost_1=cost+1
                    f_v=cost_1+new_cost
                    if f_v<=f_min:
                        frontier_nodes.append((node_1,cost_1))
                    else:
                        heapq.heappush(f_value,f_v)

        if node[0]-1>=0:
            node_1=node[:]
            node_1[0]=node[0]-1
            if grid[node_1[0]][node_1[1]]!=-1:
                if node_1 not in explored_nodes:
                    new_cost=hfunc([node_1,res_pos])
                    cost_1=cost+1
                    f_v=cost_1+new_cost
                    if f_v<=f_min:
                        frontier_nodes.append((node_1,cost_1))
                    else:
                        heapq.heappush(f_value,f_v)
                
        if not frontier_nodes:
            pre_output+=explored_nodes
            frontier_nodes,explored_nodes=[],[]
            frontier_nodes.append((start,0))
            node=frontier_nodes[0][0]
            f_min=heapq.heappop(f_value)
            f_value=[]
        
    pre_output+=explored_nodes
            
            
            
            
    
    for i in xrange(len(pre_output)):
        output.append((pre_output[i][0],pre_output[i][1]))
            

    return output
    

################################################################################
# Input:
# data is up to you and your astar function, but should be related to a search node
# 
# Output:
# the h-value for the related search node
################################################################################
def custom(data):
    node=data[0]
    res_pos=data[1]
    if [node[0],node[1]] in res_pos:
        return 3-len(node)
    else:
        return len(res_pos)-len(node)+2

