# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.qValues = util.Counter()               # a counter to Q-value of (state, action)
    self.vitCount = util.Counter()              # record how many times an action get visited


  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    Returns the qvalue for the given state and action
    """
    return self.qValues[(state, action)]



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    Returns the best value among the possible actions of the state
    """
    # Get all legal actions and end if there are none
    actions = self.getLegalActions(state)
    if not actions: return 0.0
    # Find and return the best value among the actions
    maxValue = max([self.getQValue(state, action) for action in actions])
    return maxValue

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    Returns the best action of the state
    """
    # Get all legal actions and set a counter
    # return None if there are no actions
    actions = self.getLegalActions(state)
    policy = util.Counter()
    if not actions:
        return None

    # Get the policy for all actions in the state
    for action in actions:
        policy[action] = self.getQValue(state, action)
    bestAction = policy.argMax()
    return bestAction

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    """Description:
    Flips a coin to determine whether to pick a random action or use the policy
    """
    # Get all legal actions
    # return None if there are no actions
    actions = self.getLegalActions(state)
    action = None
    if not actions:
        return action

    # Flip a coin based on the epsilon to either make a random choice or use the policy to pick an action
    if util.flipCoin(self.epsilon):
        action = random.choice(actions)
    else:
        action = self.getPolicy(state)
    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    Use q-learning to improve the agent
    """
    #Get the value of the next state
    nextq = self.getValue(nextState)
    if nextq == None:
      nextq = 0
    # Get q value of current state
    currq = self.getQValue(state, action)
    # Find the difference in values with respect to the reward and discount rate
    difference  = (reward + self.discountRate * nextq) - currq
    # Update qvalues and vitcount
    self.qValues[(state, action)] += self.alpha * difference
    self.vitCount[(state, action)] += 1

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    self.weight = util.Counter()

    # You might want to initialize weights here.

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    Calculate qvalue dependant on weight and features
    """
    # If weight is empty, extract the feature from the given state and action and initialize all weight keys given by the feature
    if len(self.weight) == 0:
        features = self.featExtractor.getFeatures(state, action)
        self.weight.incrementAll(features.keys(), 1)
    # Calculate and return qvalue
    qValue = self.weight * self.featExtractor.getFeatures(state,action)
    return qValue

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    Use q-learning to improve the agent
    updating weights based on transitions
    """
    # Extract features from state, action pair
    features = self.featExtractor.getFeatures(state, action)
    # If weight is empty, initialize all keys from the feature
    if len(self.weight) == 0:
        features = self.featExtractor.getFeatures(state, action)
        self.weight.incrementAll(features.keys(), 1)

    # Get the values of the next state
    nextq = self.getValue(nextState)
    # If there is none, set it to 0
    if nextq == None:
      nextq = 0
    # Get the qvalue of the current state
    currq = self.getQValue(state, action)
    # Find the difference in values with respect to the reward and discount rate
    difference = (reward + self.discountRate * nextq) - currq

    # Update weights for all keys using the alpha, different, and feature value
    for key in self.weight.keys():
        self.weight[key] += (self.alpha * difference * features[key])

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      print "Currrent weights: ", self.weight
