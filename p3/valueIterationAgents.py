# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    Determine utility values using value iteraction
    """
    states = self.mdp.getStates()
    values = self.values.copy()
    for i in range(self.iters):
      for state in states[1:]:
        actions = self.mdp.getPossibleActions(state)
        # Calculate max values for each current state
        values[state] = max([sum([transState[1] * (self.mdp.getReward(state, action, transState[0]) + self.discountRate*self.values[transState[0]]) for transState in self.mdp.getTransitionStatesAndProbs(state, action)]) for action in actions])
      # Sets values
      self.values = values.copy()

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    """Description:
        No changes made
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    Calculate qvalue using bellman equation 
    """
    transStates = self.mdp.getTransitionStatesAndProbs(state, action)
    qvalue = sum([transition[1] * (self.mdp.getReward(state, action, transition[0]) + self.discountRate * self.values[transition[0]]) for transition in transStates])
    return qvalue

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    import random

    """Description:
    Calculates the best qvalue and action among the possible actions and returns a random action with the highest qvalue
    """
    # End if terminal state
    if self.mdp.isTerminal(state):
        return None
    # Get possible actions
    actions = self.mdp.getPossibleActions(state)
    # Calculate qvalues for the actions and choose best value
    qvalues = [sum([transition[1] * (self.mdp.getReward(state, action, transition[0]) + self.discountRate * self.values[transition[0]]) for transition in self.mdp.getTransitionStatesAndProbs(state, action)]) for action in actions]
    maxq = max(qvalues)
    # Find index of the best value
    maxIndex = [index for index in range(len(qvalues)) if qvalues[index] == maxq]
    # Return a random action matching with the best qvalue
    return actions[random.choice(maxIndex)]

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
