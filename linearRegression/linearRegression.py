# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag

Modified: egrimson
"""

import random, pylab, numpy
# We can import r2_score from sklearn.metrics in Python to compute R_squared
from sklearn.metrics import r2_score


# GET CSV FILE
def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline() #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
    
def labelPlot():
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81  #acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured displacements')
    labelPlot()
# TESTING PLOT
# plotData('springData.txt')



# Finding a way to fit the curve and predict the value
# ¿ What´s the line such that some function of the sum of the distances from the line 
# to the measure points is minimized?

# Linear Regression
# Why to make a model? 
# # 1. Be able to expalin the phenomenon
# # 2. Make predictions
'''
pylap.polyfit (observedX, observedY, n)

pylap.polyfit finds coefficients of a polinomial of degree n that provides a best 
least squared fit for the observed data.

'''

####### Demonstration using springData
# # Plotting Data
# xVals, yVals = getData('springData.txt')
# pylab.plot(xVals, yVals, 'o', label = 'Data Points')
# pylab.title('Spring Data')


# # Try linear model
# model1 = pylab.polyfit(xVals, yVals, 1)
# pylab.plot(xVals, pylab.polyval(model1, xVals),
#           label = 'Linear Model')





###### Demonstration using mystery data
# # Plotting Data
# xVals, yVals = getData('mysteryData.txt')
# pylab.plot(xVals, yVals, 'o', label = 'Data Points')
# pylab.title('Mystery Data')

'''
Here the data does not has a linear shape but a curve shape instead.
So a linear model will not fit as much as a quadratic model will do.
Change the n degree for the quadratic model.
'''

# # Try linear model
# model1 = pylab.polyfit(xVals, yVals, 1)
# pylab.plot(xVals, pylab.polyval(model1, xVals),
#           label = 'Linear Model')

# # Try a quadratic model
# model2 = pylab.polyfit(xVals, yVals, 2)
# pylab.plot(xVals, pylab.polyval(model2, xVals),
#           'r--', label = 'Quadratic Model')
# pylab.legend()







##### ¿ How do I know what is the best solution for two models ?
# Comparing Mean Squared Error

# def aveMeanSquareError(data, predicted):
#     error = 0.0
#     for i in range(len(data)):
#         error += (data[i] - predicted[i])**2
#     return error/len(data)

# xVals, yVals = getData('mysteryData.txt')
# model1 = pylab.polyfit(xVals, yVals, 1)
# model2 = pylab.polyfit(xVals, yVals, 2)

# # code to compare fits for mystery data

# estYVals = pylab.polyval(model1, xVals)  
# print('Ave. mean square error for linear model =',
#       aveMeanSquareError(yVals, estYVals))

# estYVals = pylab.polyval(model2, xVals)
# print('Ave. mean square error for quadratic model =',
#       aveMeanSquareError(yVals, estYVals))



###### ¿ How do I know there is not a better fit out there somewhere ?
# Coefficient of determination, R ** 2

def rSquared(observed, predicted):
    return r2_score(observed, predicted)

'''
# RETURNS A VALUE BETWEEEN 0 - 1
# If returns 1 the model explains all of the variability in the data.
# If is 0 there is no relationship between the values predicted by the model and the actual data.
# As close as 1 means is better.
# During the worse cases, R2 score can even be negative.

# Example:
    r_squared = 0.68 It can be referred that 68% of the changeability of the dependent 
    output attribute can be explained by the model while the remaining 32 % of the 
    variability is still unaccounted.
'''

# generate models given a list of degrees.
def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = pylab.polyfit(xVals, yVals, d)
        models.append(model)
    return models

# run through each model and generate a fit, compute the R_squared and plot it.
def testFits(models, degrees, xVals, yVals, title):
    pylab.plot(xVals, yVals, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        pylab.plot(xVals, estYVals,
                   label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', $R^{2}=$ = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)

# # Testing goodness of fit to parabolic data

xVals, yVals = getData('mysteryData.txt')

# Compare 1 and 2 degrees

# degrees = (1, 2)
# models = genFits(xVals, yVals, degrees)
# testFits(models, degrees, xVals, yVals, 'Mystery Data')

# Compare higher-order fits

degrees = (2, 4, 8, 16)
models = genFits(xVals, yVals, degrees)
testFits(models, degrees, xVals, yVals, 'Mystery Data')

'''
The order 16th fits much better the data but that does not mean that is the best option.

If I pick an overly complexed model I have the danger of overfitting to the data, overfitting
meaning that I am not only fitting the underline process, I am fitting the noise.
'''








