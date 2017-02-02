################################################################################
# Parameters:
#   rewards is a 2d array that contains the rewards for each state (None for walls)
#   ware is the list of warehouse locations
#   nofly is the list of no-fly-zone locations
# 
# Return Value:
#   a tuple (value_hist, policy)
#   value_hist is a list of 2d arrays corresponding to the value of each 
#       state after each iteration (Start after the first iteration when values = rewards) 
#   policy is a 2d array corresponding to the optimal policy for each state with
#       values of None for walls, warehouses, and no-fly-zones. All others have a 
#        value from ('N','S','W','E')
################################################################################
def delta(iter_0, iter_1,states):
  maxim=0
  for (i,j) in states:
    diff=abs(iter_0[i][j]-iter_1[i][j])
    if maxim<diff:
      maxim=diff
  return maxim

import copy

def value_iteration(rewards, ware, nofly):
  value_function=[]

  depth,breadth=len(rewards),len(rewards[0])

  #Set up admissible states
  states=[]
  for i in xrange(depth):
    for j in xrange(breadth):
      if not ((i,j) in ware or (i,j) in nofly or rewards[i][j]==None):
        states.append((i,j))

  value_function=copy.deepcopy(rewards)
  value_function_1=copy.deepcopy(value_function)
  policy=copy.deepcopy(value_function)
  max_norm=1
  itera=0
  output=[]
  output.append(rewards)
  #set up the iteration
  while max_norm>0.00009:
  #for i in xrange(15):
    for (i,j) in states:

      next_state_utilities=[]

      #up action utility
      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.8*value_function[i][j]
      else:
        exp_util_up=0.8*value_function[i-1][j]

      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.1*value_function[i][j]
      else:
        exp_util_left=0.1*value_function[i][j-1]

      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.1*value_function[i][j]
      else:
        exp_util_right=0.1*value_function[i][j+1]

      next_state_utilities.append(exp_util_up+exp_util_left+exp_util_right)

      #down action utility
      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.8*value_function[i][j]
      else:
        exp_util_dwn=0.8*value_function[i+1][j]

      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.1*value_function[i][j]
      else:
        exp_util_left=0.1*value_function[i][j-1]

      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.1*value_function[i][j]
      else:
        exp_util_right=0.1*value_function[i][j+1]

      next_state_utilities.append(exp_util_dwn+exp_util_left+exp_util_right)

      #left action utility
      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.8*value_function[i][j]
      else:
        exp_util_left=0.8*value_function[i][j-1]

      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.1*value_function[i][j]
      else:
        exp_util_up=0.1*value_function[i-1][j]

      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.1*value_function[i][j]
      else:
        exp_util_dwn=0.1*value_function[i+1][j]

      next_state_utilities.append(exp_util_left+exp_util_up+exp_util_dwn)

      #right action utility
      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.8*value_function[i][j]
      else:
        exp_util_right=0.8*value_function[i][j+1]

      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.1*value_function[i][j]
      else:
        exp_util_up=0.1*value_function[i-1][j]

      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.1*value_function[i][j]
      else:
        exp_util_dwn=0.1*value_function[i+1][j]

      next_state_utilities.append(exp_util_right+exp_util_up+exp_util_dwn)

      max_utility=max(next_state_utilities)
      value_function_1[i][j]=rewards[i][j] + (max_utility)*0.9
      max_arg=next_state_utilities.index(max_utility)
      policy[i][j]=max_arg

    
    max_norm=delta(value_function,value_function_1,states)
    value_function=copy.deepcopy(value_function_1)
    output.append(value_function)
    

  #Extract optimal policy from value function
  for i in xrange(depth):
    for j in xrange(breadth):
      if (i,j) in states:
        if policy[i][j]==0:
          policy[i][j]='N'
        elif policy[i][j]==1:
          policy[i][j]='S'
        elif policy[i][j]==2:
          policy[i][j]='W'
        elif policy[i][j]==3:
          policy[i][j]='E'
      else:
        policy[i][j]=None
  




  return (output,policy)




################################################################################
# Parameters:
#   rewards is a 2d array that contains the rewards for each state (None for walls)
#   ware is the list of warehouse locations
#   nofly is the list of no-fly-zone locations
# 
# Return Value:
#   a tuple (policy_hist, policy)
#   policy_hist is a list of 2d arrays corresponding to the policy following each iteration 
#   policy is a 2d array corresponding to the optimal policy for each state with
#       values of None for walls, warehouses, and no-fly-zones. All others have a 
#        value from ('N','S','W','E')
################################################################################
def policy_evaluation(policy,utility,rewards,states):

  breadth=len(policy[0])
  depth=len(policy)

  utility_1=copy.deepcopy(utility)
  utility_2=copy.deepcopy(utility)
  max_norm=1

  while max_norm>=0.00009:

    for (i,j) in states:

      if policy[i][j]=='N':
        if i==0 or utility_1[i-1][j]==None:
          exp_util_up=0.8*utility_1[i][j]
        else:
          exp_util_up=0.8*utility_1[i-1][j]

        if j==0 or utility[i][j-1]==None:
          exp_util_left=0.1*utility_1[i][j]
        else:
          exp_util_left=0.1*utility_1[i][j-1]

        if j==breadth-1 or utility_1[i][j+1]==None:
          exp_util_right=0.1*utility_1[i][j]
        else:
          exp_util_right=0.1*utility_1[i][j+1]

        utility_2[i][j]= rewards[i][j] + 0.9*(exp_util_up+exp_util_left+exp_util_right)

      if policy[i][j]=='S':
        if i==depth-1 or utility_1[i+1][j]==None:
          exp_util_dwn=0.8*utility_1[i][j]
        else:
          exp_util_dwn=0.8*utility_1[i+1][j]

        if j==0 or utility_1[i][j-1]==None:
          exp_util_left=0.1*utility_1[i][j]
        else:
          exp_util_left=0.1*utility_1[i][j-1]

        if j==breadth-1 or utility_1[i][j+1]==None:
          exp_util_right=0.1*utility_1[i][j]
        else:
          exp_util_right=0.1*utility_1[i][j+1]

        utility_2[i][j]= rewards[i][j] + 0.9*(exp_util_dwn+exp_util_left+exp_util_right)

      if policy[i][j]=='W':
        if j==0 or utility_1[i][j-1]==None:
          exp_util_left=0.8*utility_1[i][j]
        else:
          exp_util_left=0.8*utility_1[i][j-1]

        if i==0 or utility_1[i-1][j]==None:
          exp_util_up=0.1*utility_1[i][j]
        else:
          exp_util_up=0.1*utility_1[i-1][j]

        if i==depth-1 or utility_1[i+1][j]==None:
          exp_util_dwn=0.1*utility_1[i][j]
        else:
          exp_util_dwn=0.1*utility_1[i+1][j]

        utility_2[i][j]= rewards[i][j] + 0.9*(exp_util_left+exp_util_up+exp_util_dwn)

      if policy[i][j]=='E':
        if j==breadth-1 or utility_1[i][j+1]==None:
          exp_util_right=0.8*utility_1[i][j]
        else:
          exp_util_right=0.8*utility_1[i][j+1]

        if i==0 or utility_1[i-1][j]==None:
          exp_util_up=0.1*utility_1[i][j]
        else:
          exp_util_up=0.1*utility_1[i-1][j]

        if i==depth-1 or utility_1[i+1][j]==None:
          exp_util_dwn=0.1*utility_1[i][j]
        else:
          exp_util_dwn=0.1*utility_1[i+1][j]

        utility_2[i][j]= rewards[i][j] + 0.9*(exp_util_right+exp_util_up+exp_util_dwn)

    max_norm=delta(utility_1,utility_2,states)
    utility_1=copy.deepcopy(utility_2)

  #print utility_2
  return utility_2




def policy_iteration(rewards, ware, nofly):

  value_function=[]

  depth,breadth=len(rewards),len(rewards[0])

  #Set up admissible states
  states=[]
  for i in xrange(depth):
    for j in xrange(breadth):
      if not ((i,j) in ware or (i,j) in nofly or rewards[i][j]==None):
        states.append((i,j))

  #value_function=copy.deepcopy(rewards)
  policy=copy.deepcopy(rewards)
  policy_1=copy.deepcopy(rewards)
  max_norm=1
  itera=0
  output=[]
  
  #initialize the starting policy with all North
  for i in xrange(depth):
    for j in xrange(breadth):
      if (i,j) in states:
        policy[i][j]='N'
      else:
        policy[i][j]=None

  #set up the iteration
  while True:
  #for i in xrange(15):
    #Evaluate the utility from policy
    value_function=policy_evaluation(policy,rewards,rewards,states)

    #policy improvement
    for (i,j) in states:

      next_state_utilities=[]

      #up action utility
      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.8*value_function[i][j]
      else:
        exp_util_up=0.8*value_function[i-1][j]

      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.1*value_function[i][j]
      else:
        exp_util_left=0.1*value_function[i][j-1]

      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.1*value_function[i][j]
      else:
        exp_util_right=0.1*value_function[i][j+1]

      next_state_utilities.append(exp_util_up+exp_util_left+exp_util_right)

      #down action utility
      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.8*value_function[i][j]
      else:
        exp_util_dwn=0.8*value_function[i+1][j]

      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.1*value_function[i][j]
      else:
        exp_util_left=0.1*value_function[i][j-1]

      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.1*value_function[i][j]
      else:
        exp_util_right=0.1*value_function[i][j+1]

      next_state_utilities.append(exp_util_dwn+exp_util_left+exp_util_right)

      #left action utility
      if j==0 or rewards[i][j-1]==None:
        exp_util_left=0.8*value_function[i][j]
      else:
        exp_util_left=0.8*value_function[i][j-1]

      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.1*value_function[i][j]
      else:
        exp_util_up=0.1*value_function[i-1][j]

      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.1*value_function[i][j]
      else:
        exp_util_dwn=0.1*value_function[i+1][j]

      next_state_utilities.append(exp_util_left+exp_util_up+exp_util_dwn)

      #right action utility
      if j==breadth-1 or rewards[i][j+1]==None:
        exp_util_right=0.8*value_function[i][j]
      else:
        exp_util_right=0.8*value_function[i][j+1]

      if i==0 or rewards[i-1][j]==None:
        exp_util_up=0.1*value_function[i][j]
      else:
        exp_util_up=0.1*value_function[i-1][j]

      if i==depth-1 or rewards[i+1][j]==None:
        exp_util_dwn=0.1*value_function[i][j]
      else:
        exp_util_dwn=0.1*value_function[i+1][j]

      next_state_utilities.append(exp_util_right+exp_util_up+exp_util_dwn)

      max_utility=max(next_state_utilities)
      max_arg=next_state_utilities.index(max_utility)
      policy_1[i][j]=max_arg

      for i in xrange(depth):
        for j in xrange(breadth):
          if (i,j) in states:
            if policy_1[i][j]==0:
              policy_1[i][j]='N'
            elif policy_1[i][j]==1:
              policy_1[i][j]='S'
            elif policy_1[i][j]==2:
              policy_1[i][j]='W'
            elif policy_1[i][j]==3:
              policy_1[i][j]='E'
          else:
            policy_1[i][j]=None

    output.append(policy)
    if policy==policy_1:
      break
    policy=copy.deepcopy(policy_1)
    
  output.append(policy)
  return output,policy_1
    

if __name__=='__main__':
  print policy_iteration([[-0.04,-0.04,-0.04,1],[-0.04,None,-0.04,-1],[-0.04,-0.04,-0.04,-0.04]],[(0,3)],[(1,3)])
  #print policy_iteration([[0, -1], [0, 1]], [(1, 1)], [(0, 1)])