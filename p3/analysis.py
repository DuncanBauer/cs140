# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.016
  """Description:
  Reduced noise to allow the agent to traverse more freely
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.3
  answerNoise = 0.001
  answerLivingReward = -1.0
  """Description:
  Reduced noise to allow the agent to traverse more freely
  Decreased living reward to make the agent take more risks
  Decreased discount to make closer tiles more appealing
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.3
  answerNoise = 0.3
  answerLivingReward = -1.0
  """Description:
  Reduced noise to allow the agent to traverse more freely
  Reduced living reward to make the agent take more risks
  Reduced discount to make closer tiles more appealing
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.7
  answerNoise = 0.001
  answerLivingReward = -1.0
  """Description:
  Reduced noise to allow the agent to traverse more freely
  Decreased living reward to make the agent take more risks
  Decreased discount to give further tiles less appeal
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.3
  answerNoise = 0.3
  answerLivingReward = 1.0
  """Description:
  Reduced noise to allow the agent to traverse more freely
  Increased living reward to prevent the agent from nearing the cliff and to stay alive in general
  Decreased discount to give further tiles less appeal
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 1
  answerNoise = 1
  answerLivingReward = 100
  """Description:
  Increased noise to restrict the agent
  Increased living reward to prevent the agent from nearing the cliff and to stay alive in general
  Increased discount to give alternate tiles more appeal
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = 0.5
  answerLearningRate = 0.8
  """Description:
  """
  """ YOUR CODE HERE """
  # No code, only value changes
  """ END CODE """
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
