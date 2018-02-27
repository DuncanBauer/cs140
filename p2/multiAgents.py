# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (food) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    childGameState = currentGameState.generatePacmanSuccessor(action)
    pacPos = childGameState.getPacmanPosition()
    food = currentGameState.getFood()
    newGhostStates = childGameState.getGhostStates()

    score =  childGameState.getScore()
    # Subtracts from score if ghosts are nearby
    distFromGhost = manhattanDistance(pacPos, newGhostStates[0].getPosition())
    if distFromGhost > 0:
      score -= 10 / distFromGhost

    # distance to ghosts
    ghostScore = 0
    for ghost in newGhostStates:
      dist = manhattanDistance(pacPos, newGhostStates[0].getPosition())
      if dist > 0:
        if ghost.scaredTimer > 0:  # if ghost is scared, go for him
          ghostScore += 500 / dist
        else:  # otherwise run!
          ghostScore -= 50 / dist
    score += ghostScore

    # Adds to score if ghosts are nearby
    distFromFood = [manhattanDistance(pacPos, pos) for pos in food.asList()]
    if distFromFood > 0:
      score += 10 / (min(distFromFood) + 1)
    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

  def isTerminal(self, state, depth, agent):
      return depth == self.depth or \
             state.isWin() or \
             state.isLose() or \
             state.getLegalActions(agent) == 0

  def isPacman(self, state, agent):
      return agent == state.getNumAgents()

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    def minimax(state, depth, agent):
      # Maximizes score and resets agent
      if self.isPacman(state, agent):
        return minimax(state, depth+1, 0)

      # evaluates the score of the node if it is terminal
      if self.isTerminal(state, depth, agent):
        return self.evaluationFunction(state)

      # Generates a list of successors to the current state
      successors = (minimax(state.generateSuccessor(agent, action), depth, agent+1) for action in state.getLegalActions(agent))

      # Returns max score if pacmans turn and min score otherwise
      if self.isPacman(state, agent):
        return max(successors)
      else:
        return min(successors)

    # Begins the min max search and returns the best action
    return max(gameState.getLegalActions(0),
               key=lambda action: minimax(gameState.generateSuccessor(0, action), 0, 1))

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """

    def beginPruning(state, depth, agent, a=float("-inf"), b=float("inf")):
      if self.isPacman(state,agent):  # next depth
        depth += 1
        agent = 0

      # evaluate the node if it is terminal
      if self.isTerminal(state, depth, agent):  # dead end
        return self.evaluationFunction(state), None

      # If it is pacmans turn, maximize options, else minimize options
      # Ends searching branch if not within bounds
      if self.isPacman(state, agent):
        return getScore(state, depth, agent, a, b, float('-inf'), max)
      else:
        return getScore(state, depth, agent, a, b, float('inf'), min)

    # Returns the best action for the tree, whether minimizing or maximizing
    def getScore(state, depth, agent, a, b, _bestScore, minMaxFunction):
      bestScore = _bestScore
      bestAction = None

      # Look at the actions and score of every action and choose which is best based on minimizing or maximizing
      for action in state.getLegalActions(agent):
        successor = state.generateSuccessor(agent, action)
        score, _action = beginPruning(successor, depth, agent + 1, a, b)
        bestScore, bestAction = minMaxFunction((bestScore, bestAction), (score, action))

        # Sets new bounds for pruning
        # If it is pacmans turn, maximize the score and set the new max value
        if self.isPacman(state, agent):
          if bestScore > b:
            return bestScore, bestAction
          a = minMaxFunction(a, bestScore)
        else:
        # Else minimize the score and set the new min value
          if bestScore < a:
            return bestScore, bestAction
          b = minMaxFunction(b, bestScore)

      return bestScore, bestAction

    # Begins pruning and returns the best action
    score, action = beginPruning(gameState, 0, 0)
    return action

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    def expectimax(state, depth, agent):
        if self.isPacman(state, agent):  # is pacman
            return expectimax(state, depth + 1, 0)  # start next depth

        if self.isTerminal(state, depth, agent):
            return self.evaluationFunction(state)  # return evaluation for bottom states

        successors = [expectimax(state.generateSuccessor(agent, action), depth, agent + 1) for action in state.getLegalActions(agent)]

        # Return the best move for pacman
        if self.isPacman(state, agent):
            return max(successors)
        # take average score for ghosts actions
        else:
            return sum(successors)/len(successors)

    # return the best of pacman's possible moves
    return max(gameState.getLegalActions(0), key = lambda action: expectimax(gameState.generateSuccessor(0, action), 0, 1))


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  pacPos = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  ghostStates = currentGameState.getGhostStates()
  score = currentGameState.getScore()

  # distance to ghosts
  ghostScore = 0
  for ghost in ghostStates:
      dist = manhattanDistance(pacPos, ghostStates[0].getPosition())
      if dist > 0:
          if ghost.scaredTimer > 0:  # if ghost is scared, go for him
              ghostScore += 500 / dist
          else:  # otherwise run!
              ghostScore -= 50 / dist
  score += ghostScore

  # distance to closest food
  distancesToFood = [manhattanDistance(pacPos, pos) for pos in food.asList()]
  if len(distancesToFood):
    score += 10 / min(distancesToFood)

  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

