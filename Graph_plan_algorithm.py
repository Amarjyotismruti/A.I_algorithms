##**Smruti Amarjyoti-AI_Assignment-2**##
##**Oct-2016**##
##**Planning graph using Astar state space search and set level heuristic**##
################################################################################
# Parameters:
#   nrow, ncol are the number of rows and columns of the grid
#   wall is the list of wall locations
#   res is the list of residence locations
#   start is the list of drone starting locations
# 
# Return Value:
#   the set level heuristic
################################################################################

def initialize_graph(nrow, ncol, wall, res, start):


  drone=[]
  occupied=[]
  wal=[]
  residence=[]
  not_residence=[]
  not_wal=[]
  not_occupied=[]
  not_drone=[]

  #initialize the graph planning state
  for i in xrange(len(start)):
    drone.append((i,start[i]))
    occupied.append(start[i])
  for i in xrange(len(res)):
    residence.append((i,res[i]))
  for i in xrange(len(wall)):
    wal.append((wall[i]))

  for i in xrange(nrow):
    for j in xrange(ncol):
      for k in xrange(len(res)):
        if (i,j) != res[k]:
          not_residence.append((k,(i,j)))
        if (i,j) != start[k]:
          not_drone.append((k,(i,j)))

  for i in xrange(nrow):
    for j in xrange(ncol):
      if (i,j) not in start:
        not_occupied.append((i,j))
      if (i,j) not in wall:
        not_wal.append((i,j))

  return drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal


def set_level_heuristic(nrow, ncol, wall, res, start):
    # construct the set of facts at level 0 (remember to add all the negative facts that are true)
    # while the planning graph has not leveled off
    #    extend by one level
    #    if all goals appear and are not mutex then return level
    
    
    drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal=initialize_graph(nrow, ncol, wall, res, start)
    ##print set_level_heuristic_astar(drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal,(nrow,ncol))
    level=1

    while not check_goal_state(not_residence,residence):
      ##print drone
      level+=1
      #postconditions buffer
      b_drone=[]
      b_occupied=[]
      b_not_residence=[]
      b_not_drone=[]
      #check preconditions for every drone operations
      for drone_iter in drone:
        
        k,pos=drone_iter
        i,j=pos[0],pos[1]
        #preconditions for up
        if i!=0 and (k,(i,j)) in drone and (i-1,j) in not_occupied and (i-1,j) in not_wal:
          if (i-1,j) not in occupied:
            b_occupied.append((i-1,j))
          if (k,(i-1,j)) not in drone:
            b_drone.append((k,(i-1,j)))
          b_not_drone.append((k,(i,j)))
          ##print k,"up"
        #preconditions for down
        if i!=nrow-1 and (k,(i,j)) in drone and (i+1,j) in not_occupied and (i+1,j) in not_wal:
          if (i+1,j) not in occupied:
            b_occupied.append((i+1,j))
          if (k,(i+1,j)) not in drone and (k,(i+1,j)) not in b_drone:
            b_drone.append((k,(i+1,j)))
          b_not_drone.append((k,(i,j)))
          ##print k,"down"
        #preconditions for left
        if j!=0 and (k,(i,j)) in drone and (i,j-1) in not_occupied and (i,j-1) in not_wal:
          if (i,j-1) not in occupied:
            b_occupied.append((i,j-1))
          if (k,(i,j-1)) not in drone and (k,(i,j-1)) not in b_drone:
            b_drone.append((k,(i,j-1)))
          b_not_drone.append((k,(i,j)))
          ##print k,"left"
        #preconditions for right
        if j!=ncol-1 and (k,(i,j)) in drone and (i,j+1) in not_occupied and (i,j+1) in not_wal:
          if (i,j+1) not in occupied:
            b_occupied.append((i,j+1))
          if (k,(i,j+1)) not in drone and (k,(i,j+1)) not in b_drone:
            b_drone.append((k,(i,j+1)))
          b_not_drone.append((k,(i,j)))
          ##print k,"right"
        #visit action
        if (k,(i,j)) in drone and (k,(i,j)) in residence:
          if (k,(i,j)) not in not_residence:
            b_not_residence.append((k,(i,j)))
          b_not_drone.append((k,(i,j)))
          ##print "RESIDENCE REACHED!!",level
      
      #add the buffer to postconditions
      drone+=b_drone
      occupied+=b_occupied
      not_residence+=b_not_residence
      not_drone+=b_not_drone
      ##print not_residence
      ##print drone
    return level

################################################################################
# Parameters:
#   nrow, ncol are the number of rows and columns of the grid
#   wall is the list of wall locations
#   res is the list of residence locations
#   start is the list of drone starting locations
# 
# Return Value:
#   a solution grid (see handout for format)
################################################################################

import copy

def set_level_heuristic_astar(state):

  state_1=copy.deepcopy(state)
  drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal,dim=state_1
  nrow,ncol=dim
    
  level=1

  while not check_goal_state(not_residence,residence):

    level+=1
    #postconditions buffer
    b_drone=[]
    b_occupied=[]
    b_not_residence=[]
    b_not_drone=[]
    #check preconditions for every drone operations
    for drone_iter in drone:
      
      k,pos=drone_iter
      i,j=pos[0],pos[1]
      #preconditions for up
      if i!=0 and (k,(i,j)) in drone and (i-1,j) in not_occupied and (i-1,j) in not_wal:
        if (i-1,j) not in occupied:
          b_occupied.append((i-1,j))
        if (k,(i-1,j)) not in drone:
          b_drone.append((k,(i-1,j)))
        b_not_drone.append((k,(i,j)))
        ##print k,"up"
      #preconditions for down
      if i!=nrow-1 and (k,(i,j)) in drone and (i+1,j) in not_occupied and (i+1,j) in not_wal:
        if (i+1,j) not in occupied:
          b_occupied.append((i+1,j))
        if (k,(i+1,j)) not in drone:
          b_drone.append((k,(i+1,j)))
        b_not_drone.append((k,(i,j)))
        ##print k,"down"
      #preconditions for left
      if j!=0 and (k,(i,j)) in drone and (i,j-1) in not_occupied and (i,j-1) in not_wal:
        if (i,j-1) not in occupied:
          b_occupied.append((i,j-1))
        if (k,(i,j-1)) not in drone:
          b_drone.append((k,(i,j-1)))
        b_not_drone.append((k,(i,j)))
        ##print k,"left"
      #preconditions for right
      if j!=ncol-1 and (k,(i,j)) in drone and (i,j+1) in not_occupied and (i,j+1) in not_wal:
        if (i,j+1) not in occupied:
          b_occupied.append((i,j+1))
        if (k,(i,j+1)) not in drone:
          b_drone.append((k,(i,j+1)))
        b_not_drone.append((k,(i,j)))
        ##print k,"right"
      #visit action
      if (k,(i,j)) in drone and (k,(i,j)) in residence:
        if (k,(i,j)) not in not_residence:
          b_not_residence.append((k,(i,j)))
        b_not_drone.append((k,(i,j)))
        ##print "RESIDENCE REACHED!!",level
  
    #add the buffer to postconditions
    drone+=b_drone
    occupied+=b_occupied
    not_residence+=b_not_residence
    not_drone+=b_not_drone
    ##print not_residence
    ##print drone
    #graph levelling off condition
    if not b_drone and not b_not_residence:
      return 100
  return level
  



def check_goal_state(not_residence,residence):
  goal_reach=True

  for i in residence:
    if i not in not_residence:
      goal_reach=goal_reach and False

  return goal_reach

import heapq


def plan(nrow, ncol, wall, res, start):
  # You can use A* with the set level heuristic, or extract solution of graphplan
  drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal=initialize_graph(nrow, ncol, wall, res, start)
  path=[]
  path.append(drone)
  g_value=0
  h_value=set_level_heuristic_astar((drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal,(nrow,ncol)))
  f_value=g_value+h_value
  explored=[]
  node=[]
  heapq.heappush(node,(f_value,g_value,drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal,path))
  
  while not check_goal_state(not_residence,residence):
  #for b in xrange(20):

    f_value,g_value,drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal,path=heapq.heappop(node)

    ##print drone,not_residence[-2],not_residence[-1],f_value
    ##print "not_residences",not_residence
    #if (drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal) not in explored:
    # explored.append((drone,occupied,residence,wal,not_drone,not_occupied,not_residence,not_wal))

    #check preconditions for every drone operations

    for drone_iter in drone:
      
      k,pos=drone_iter
      i,j=pos[0],pos[1]
      ##print drone_iter
      #preconditions for up
      if i!=0 and (k,(i,j)) in drone and (i-1,j) in not_occupied and (i-1,j) in not_wal:
        ##print "up"
        occupied_1=occupied[:]
        not_occupied_1=not_occupied[:]
        drone_1=drone[:]
        if (i-1,j) not in occupied:
          occupied_1.append((i-1,j))
          not_occupied_1.remove((i-1,j))
        if (k,(i-1,j)) not in drone:
          drone_1.append((k,(i-1,j)))
          drone_1.remove((k,(i,j)))
        path_1=path[:]
        path_1.append(drone_1)
        #print drone_1
        #print path_1
        f_value=set_level_heuristic_astar((drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,(nrow,ncol))) + g_value + 1
        heapq.heappush(node,(f_value,g_value+1,drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,path_1))
        #b_not_drone.append((k,(i,j)))
        ##print k,"up"
      #preconditions for down
      if i!=nrow-1 and (k,(i,j)) in drone and (i+1,j) in not_occupied and (i+1,j) in not_wal:
        #print "down"
        occupied_1=occupied[:]
        not_occupied_1=not_occupied[:]
        drone_1=drone[:]
        if (i+1,j) not in occupied:
          occupied_1.append((i+1,j))
          not_occupied_1.remove((i+1,j))
        if (k,(i+1,j)) not in drone:
          drone_1.append((k,(i+1,j)))
          drone_1.remove((k,(i,j)))
        path_1=path[:]
        path_1.append(drone_1) 
        #print drone_1
        f_value=set_level_heuristic_astar((drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,(nrow,ncol))) + g_value + 1
        #print path_1
        heapq.heappush(node,(f_value,g_value+1,drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,path_1))
        #b_not_drone.append((k,(i,j)))
        ##print k,"down"
      #preconditions for left
      if j!=0 and (k,(i,j)) in drone and (i,j-1) in not_occupied and (i,j-1) in not_wal:
        #print "left"
        occupied_1=occupied[:]
        not_occupied_1=not_occupied[:]
        drone_1=drone[:]
        if (i,j-1) not in occupied:
          occupied_1.append((i,j-1))
          not_occupied_1.remove((i,j-1))
        if (k,(i,j-1)) not in drone:
          drone_1.append((k,(i,j-1)))
          drone_1.remove((k,(i,j)))
        path_1=path[:]
        path_1.append(drone_1)
        #print drone_1
        #print path_1
        f_value=set_level_heuristic_astar((drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,(nrow,ncol))) + g_value + 1
        heapq.heappush(node,(f_value,g_value+1,drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,path_1))
        #not_drone.append((k,(i,j)))
        ##print k,"left"
      #preconditions for right
      if j!=ncol-1 and (k,(i,j)) in drone and (i,j+1) in not_occupied and (i,j+1) in not_wal:
        #print "right"
        occupied_1=occupied[:]
        not_occupied_1=not_occupied[:]
        drone_1=drone[:]
        if (i,j+1) not in occupied:
          occupied_1.append((i,j+1))
          not_occupied_1.remove((i,j+1))
        if (k,(i,j+1)) not in drone:
          drone_1.append((k,(i,j+1)))
          drone_1.remove((k,(i,j)))
        path_1=path[:]
        path_1.append(drone_1)
        #print drone_1
        #print path_1
        f_value=set_level_heuristic_astar((drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,(nrow,ncol))) + g_value + 1
        heapq.heappush(node,(f_value,g_value+1,drone_1,occupied_1,residence,wal,not_drone,not_occupied_1,not_residence,not_wal,path_1))
        #b_not_drone.append((k,(i,j)))
        ##print k,"right"
      #visit action
      if (k,(i,j)) in drone and (k,(i,j)) in residence and (k,(i,j)) not in not_residence:
        not_residence_1=not_residence[:]
        not_residence_1.append((k,(i,j)))
         ##print "not_residence_in_loop",not_residence_1
        f_value=set_level_heuristic_astar((drone,occupied,residence,wal,not_drone,not_occupied,not_residence_1,not_wal,(nrow,ncol))) + g_value + 1
        heapq.heappush(node,(f_value,g_value,drone,occupied,residence,wal,not_drone,not_occupied,not_residence_1,not_wal,path))
        #b_not_drone.append((k,(i,j)))
        #print "RESIDENCE REACHED!!"

  return construct_grid(path,nrow,ncol,wall)

def construct_grid(path,rows,cols,walls):
  grid=[]
  for i in xrange(rows):
    grid_r=[]
    for j in xrange(cols):
      grid_r.append(None)
    grid.append(grid_r)
  
  for wall_iter in walls:
    grid[wall_iter[0]][wall_iter[1]]=-1

  for path_1 in path:
    for path_2 in path_1:
      grid[path_2[1][0]][path_2[1][1]]=path_2[0]
      #print path_2[1][0],path_2[1][1],path_2[0]
  ##print grid
  return grid












    

