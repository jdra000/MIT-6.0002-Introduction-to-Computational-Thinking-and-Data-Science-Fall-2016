import random, pylab, numpy

# #set line width
# pylab.rcParams['lines.linewidth'] = 4
# #set font size for titles 
# pylab.rcParams['axes.titlesize'] = 20
# #set font size for labels on axes
# pylab.rcParams['axes.labelsize'] = 20
# #set size of numbers on x-axis
# pylab.rcParams['xtick.labelsize'] = 16
# #set size of numbers on y-axis
# pylab.rcParams['ytick.labelsize'] = 16
# #set size of ticks on x-axis
# pylab.rcParams['xtick.major.size'] = 7
# #set size of ticks on y-axis
# pylab.rcParams['ytick.major.size'] = 7
# #set size of markers, e.g., circles representing points
# #set numpoints for legend
# pylab.rcParams['legend.numpoints'] = 1

class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1
    def spin(self):
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else: return -amt
    def __str__(self):
        return 'Fair Roulette'

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        totPocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=',\
              str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins) # returns the mean amt after playing
        
def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std




#######

# ## GENERATING AND PLOTTING NORMALLY DISTRIBUTED DATA
# random.seed(1)
# dist, numSamples = [], 1000000

# # gauss receives the mean as first argument and std as second argument.
# # returns a number with gaussian distribution.
# for i in range(numSamples):
#     dist.append(random.gauss(0, 100))
# # Plotting
# v = pylab.hist(dist, bins = 100,
#               weights = [1/numSamples]*len(dist))
# pylab.xlabel('x')
# pylab.ylabel('Relative Frequency')

# # This gives us 0.9571469999999963 (two stds from the mean)
# print('Fraction within ~200 of mean =',
#       sum(v[0][30:70]))


#######

## Probability Density Function (PDF) for Normal Distribution
'''
More precisely, the PDF is used to specify the probability of the random 
variable falling within a particular range of values.

This probability is given by the integral of this variable's PDF over 
that range—that is, it is given by the area under the density function 
but above the horizontal axis and between the lowest and greatest values 
of the range. 
'''
def gaussian(x, mu, sigma): # mu = media, sigma = standard deviation
  '''
  Builds each factor of the PDF formula and returns the result. 
  '''
  factor1 = (1.0/(sigma*((2*pylab.pi)**0.5)))
  factor2 = pylab.e**-(((x-mu)**2)/(2*sigma**2))
  return factor1*factor2

#Plotting
# for a set of x's get the set of y's corresponding
xVals, yVals = [], []
# Standard Normal Distribution Values
mu, sigma = 0, 1
x = -4
while x <= 4: # Look at the distribution from -4 to 4
    xVals.append(x)
    yVals.append(gaussian(x, mu, sigma))
    x += 0.05
# pylab.plot(xVals, yVals)
# pylab.title('Normal Distribution, mu = ' + str(mu)\
#             + ', sigma = ' + str(sigma))



#######

## Using Scipy to check Emprical Rule
## By getting the area under the curve between each
## empirical rule values from the mean.
'''
# scipy.integrate.quad has up to four arguments:
    # a function or method to be integrated
    # a number representing the lower limit
    # a number representing the upper limit
    # optional tuple supplying values for all arguments, except the function to be integrated.

# scipy.integrate.quad returns a tuple:
    # (approximation to result, estimate of absolute error)
'''
# import scipy.integrate

# def checkEmpirical(numTrials):
#   for t in range(numTrials):
#       mu = random.randint(-10, 10) # random mean
#       sigma = random.randint(1, 10) # random sigma
#       print('For mu =', mu, 'and sigma =', sigma)
#       for numStd in (1, 1.96, 3):
#         area = scipy.integrate.quad(gaussian, mu-numStd*sigma, mu+numStd*sigma, (mu, sigma))[0] # getting the approximation
#         print(' Fraction within', numStd,
#               'std =', round(area, 4))
        
# checkEmpirical(3)




#######
# Central Limit Theorem

'''
As soon as we end up reasoning not about a single event but about 
the mean of something, we can apply the Central Limit Theorem

# Given a sufficiently large sample:
    # The means of the samples in a set of samples will be approximately
    normally distributed.
    # This normal distribution will have a mean close to the mean 
    of the population
    # The variance of the sample means will be close to the variance of the 
    population divided by the sample size.
'''


# Checking CLT for a Continuos Die (values from 0.0 to 5.0)
# numDice = sample size
# numRolls // numDice = num of samples (Population)

# def plotMeans(numDice, numRolls, numBins, legend, color, style):
#     means = []
#     for i in range(numRolls//numDice):
#         vals = 0
#         for j in range(numDice):
#             vals += 5*random.random()  # returns nums between 0.0 - 1.0
#         means.append(vals/float(numDice)) # sum of values / numDice
#     pylab.hist(means, numBins, color = color, label = legend,
#               weights = [1/len(means)]*len(means),
#               hatch = style)
#     return getMeanAndStd(means)

# mean, std = plotMeans(1, 1000000, 19, '1 die', 'b', '*')
# print('Mean of rolling 1 die =', str(mean) + ',', 'Std =', std)
# mean, std = plotMeans(50, 1000000, 19, 'Mean of 50 dice', 'r', '//')
# print('Mean of rolling 50 dice =', str(mean) + ',', 'Std =', std)
# pylab.title('Rolling Continuous Dice')
# pylab.xlabel('Value')
# pylab.ylabel('Probability')
# pylab.legend()
'''
# RESULTS:
#     Mean of rolling 1 die = 2.4998674611414646, Std = 1.4441014587861611
#     Mean of rolling 50 dice = 2.497221691006734, Std = 0.2043493684221549
# CONCLUSSION:
# The mean of 50 gives me a normal distribution
# Standard deviation of the sampling distribution decreases as the size 
of the samples that were used to calculate the means for the sampling 
distribution increases.
'''
    
    

    
# # # Checking CLT for Fair Roulette
# numTrials = 1000000
# numSpins = 200
# game = FairRoulette()

# means = []
# for i in range(numTrials):
#     means.append(findPocketReturn(game, 1, numSpins,
#                                   False)[0])

# pylab.hist(means, bins = 19,
#           weights = [1/len(means)]*len(means))
# pylab.xlabel('Mean Return')
# pylab.ylabel('Probability')
# pylab.title('Expected Return Betting a Pocket 200 Times')




# Simulating Buffon-Laplace Method to find PI
def throwNeedles(numNeedles):
    inCircle = 0
    for Needles in range(1, numNeedles + 1, 1):
        x = random.random()
        y = random.random()
        if (x*x + y*y)**0.5 <= 1.0:
            inCircle += 1
    return 4*(inCircle/float(numNeedles))
    
def getEst(numNeedles, numTrials):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = numpy.std(estimates)
    curEst = sum(estimates)/len(estimates)
    print('Est. = ' + str(curEst) +\
          ', Std. dev. = ' + str(round(sDev, 6))\
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)

def estPi(precision, numTrials):
    numNeedles = 1000
    sDev = precision
    while sDev >= precision/2:
        curEst, sDev = getEst(numNeedles,
                              numTrials)
        numNeedles *= 2
    return curEst

random.seed(0)
estPi(0.005, 100)





