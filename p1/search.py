# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from heapq import heappush, heappop, heapify
import time

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    list = []
    discovered = []
    backpointer = {}
    list.append((problem.startingState(), 'None', 1))
    backpointer[(problem.startingState(), 'None', 1)] = None

    while list:
        curr = list.pop()
        if problem.isGoal(curr[0]):
            path = []
            npath = []
            s = curr
            path.append(s)
            while s is not None:
                path.append(backpointer[s])
                s = backpointer[s]
            path.pop()
            path.pop()
            path.reverse()
            for action in path:
                npath.append(action[1])
            return npath
        if curr[0] not in discovered:
            discovered.append(curr[0])
            successors = problem.successorStates(curr[0])
            for item in successors:
                if item[0] not in discovered:
                    if item not in list and item not in backpointer:
                        list.append(item)
                        backpointer[item] = curr
    """
    Search the deepest nodes in the search tree first [p 85].
    
    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
    
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.startingState()
    print "Is the start a goal?", problem.isGoal(problem.startingState())
    print "Start's successors:", problem.successorStates(problem.startingState())
    """

def breadthFirstSearch(problem):
    list = []
    discovered = []
    path = []
    list.append((problem.startingState(), 'None', path))

    while list:
        curr = list.pop()
        if problem.isGoal(curr[0]):
            #path = []
            #npath = []
            #s = curr
            #path.append(s)
            #while s is not None:
            #    path.append(backpointer[s])
            #    s = backpointer[s]
            #path.pop()
            #path.pop()
            #path.reverse()
            #for action in path:
            #    npath.append(action[1])
            #return npath
            return curr[2]
        if curr[0] not in discovered:
            discovered.append(curr[0])
            successors = problem.successorStates(curr[0])
            for item in successors:
                if item[0] not in discovered:
                    if item not in list:
                        list.insert(0, (item[0], item[1], curr[2] + [item[1]]))
    return []
      
def uniformCostSearch(problem):
    list = []
    discovered = []
    backpointer = {}
    cost = 1
    heappush(list, (cost, (problem.startingState(), 'None')))
    backpointer[(problem.startingState(), 'None')] = None

    while list:
        cost, curr = heappop(list)
        if problem.isGoal(curr[0]):
            path = []
            npath = []
            s = curr
            path.append(s)
            while s is not None:
                path.append(backpointer[s])
                s = backpointer[s]
            path.pop()
            path.pop()
            path.reverse()
            for action in path:
                npath.append(action[1])
            print(npath)
            return npath

        if curr[0] not in discovered:
            discovered.append(curr[0])
            successors = problem.successorStates(curr[0])
            for item in successors:
                if item[0] not in discovered:
                    if item not in list and item not in backpointer:
                        heappush(list, ((cost + item[2]), item))
                        backpointer[item] = curr

def nullHeuristic(state, problem=None):

  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    list = []
    discovered = []
    backpointer = {}
    cost = 1
    heappush(list, (cost, (problem.startingState(), 'None')))
    backpointer[(problem.startingState(), 'None')] = None

    while list:
        cost, curr = heappop(list)
        cost -= heuristic(curr[0], problem)
        if problem.isGoal(curr[0]):
            path = []
            npath = []
            s = curr
            path.append(s)
            while s is not None:
                path.append(backpointer[s])
                s = backpointer[s]
            path.pop()
            path.pop()
            path.reverse()
            for action in path:
                npath.append(action[1])
            print(npath)
            return npath

        if curr[0] not in discovered:
            discovered.append(curr[0])
            successors = problem.successorStates(curr[0])
            for item in successors:
                if item[0] not in discovered:
                    if item not in list and item not in backpointer:
                        heappush(list, ((cost + item[2] + heuristic(item[0], problem)), item))
                        backpointer[item] = curr

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
