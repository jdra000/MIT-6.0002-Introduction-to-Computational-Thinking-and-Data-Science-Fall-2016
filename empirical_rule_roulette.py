import random, pylab

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers, e.g., circles representing points
#set numpoints for legend
pylab.rcParams['legend.numpoints'] = 1

## FairRoulette Simulation

class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1
    def spin(self): # returns random pocket
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds # win amt*36
        else: return -amt # lose the amt
    def __str__(self):
        return 'Fair Roulette'

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        # keep count for earnings and loses
        totPocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=',\
              str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins) # returns the mean amt after playing

# TESTING
# random.seed(0)
# game = FairRoulette()
# for numSpins in (100, 1000000):
#     for i in range(3):
#         playRoulette(game, numSpins, 2, 1, True)
        
        

class EuRoulette(FairRoulette): # 1 MORE POCKET
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'

class AmRoulette(EuRoulette): # 1 MORE POCKET
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'

# Function to return a list of amt means for numTrials
def findPocketReturn(game, numTrials, numSpins, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, numSpins, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns
             
# receives a list and returns the mean and the standard deviation
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

random.seed(0)
numTrials = 20
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)

## Applying Emprirical Rule
# 95 % within 1.96 standard deviations from the mean
resultDict = {}
for G in games:
    resultDict[G().__str__()] = []
for numSpins in (1000, 10000, 100000, 1000000):
    print('\nSimulate betting a pocket for', numTrials, 'trials of',
          numSpins, 'spins each')
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials,
                                          numSpins, False)
        # gets the mean of the means and the std of the means
        mean, std = getMeanAndStd(pocketReturns)
        resultDict[G().__str__()].append((numSpins, 100*mean, 100*std))
        # expReturn = 100*sum(pocketReturns)/len(pocketReturns)
        print('Exp. return for', G(), '=',
              str(round(100*mean, 3))
              + '%', '+/- ' + str(round(100*1.96*std, 3))
              + '% with 95% confidence')
'''
This means that 95 % of the cases will fall between +- those range of 
values from the mean.

Confidence interval is smaller so I have good reason to believe that
the mean I am computing is close to the true mean.
'''






