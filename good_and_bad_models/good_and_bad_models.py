# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag
"""

import random, pylab, numpy
from sklearn.metrics import r2_score


def rSquared(observed, predicted):
    return r2_score(observed, predicted)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    i = 1
    moving_averages = []
    # returns the array of the cumulative sum of elements of the given array
    cum_sum = numpy.cumsum(y)
    
    while i <= len(y):
        
        window_average = round(cum_sum[i-1] / i, 2)
        
        moving_averages.append(window_average)
        
        i += 1
        
    return pylab.array(moving_averages)
###### Validate a Model
# # Task: Model how the mean daily high temperature in the U.S. varied from 1961 through 2015
# # Get means for each year and plot them
# # Randomly divide data in half n times
# # Report r_squared for each dimensionality


class tempDatum(object):
    def __init__(self, s):
        info = s.split(',')
        self.high = float(info[1])
        self.year = int(info[2][0:4])
    def getHigh(self):
        return self.high
    def getYear(self):
        return self.year
    
def getTempData():
    inFile = open('temperatures.csv')
    data = []
    for l in inFile:
        data.append(tempDatum(l))
    return data
    
def getYearlyMeans(data):
    years = {}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
        except:
            years[d.getYear()] = [d.getHigh()]
    for y in years:
        years[y] = sum(years[y])/len(years[y])
    return years

data = getTempData()
years = getYearlyMeans(data)
xVals, yVals = [], []
for e in years:
    xVals.append(e)
    yVals.append(years[e])
pylab.plot(xVals, yVals)
pylab.xlabel('Year')
pylab.ylabel('Mean Daily High (C)')
pylab.title('Select U.S. Cities')

def splitData(xVals, yVals):
    # list of random samples (half of real data)
    toTrain = random.sample(range(len(xVals)), len(xVals)//2)
    
    trainX, trainY, testX, testY = [],[],[],[]
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX, trainY, testX, testY

# # 10 random distributions of the sample 
numSubsets = 10
dimensions = (1, 2, 3, 4, 20)
rSquares = {}
for d in dimensions:
    rSquares[d] = []


for f in range(numSubsets):
    trainX, trainY, testX, testY = splitData(xVals, yVals)
    for d in dimensions:
        model = pylab.polyfit(trainX, trainY, d)

        # How well polyval predict the test set instead of the training one.
        estYVals = pylab.polyval(model, testX)
        rSquares[d].append(rSquared(testY, estYVals))
        
print('Mean R-squares for test data')
for d in dimensions:
    mean = round(sum(rSquares[d])/len(rSquares[d]), 4)
    sd = round(numpy.std(rSquares[d]), 4)
    print('For dimensionality', d, 'mean =', mean,
          'Std =', sd)
 ## RESULTS:
'''
Mean R-squares for test data
For dimensionality 1 mean = 0.7293 Std = 0.0563
For dimensionality 2 mean = 0.7067 Std = 0.0624
For dimensionality 3 mean = 0.6714 Std = 0.1067
For dimensionality 4 mean = 0.6827 Std = 0.0964
     '''
# Line seems to be the winner :
    # Highest average r_squared
    # Smallest deviation across trials
    # Simplest model

















