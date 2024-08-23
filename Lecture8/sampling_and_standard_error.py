import random, pylab, numpy

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
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1

'''
Data Information:
    # From U.S National Centers for Enviromental Information (NCEI)
    # Daily high and low temperatures for 21 different US cities
    # 1961 - 2015
    
Simple random sampling: each member has an equal chance of being chosen.

numpy.std : 
    is the function in the numpy module that returns the std.
    
random.sample (population, sampleSize) :
    returns a list containing sampleSize randomly chosen distinct 
    elements of population.
'''
### UNDERSTANDING CSV

def makeHist(data, title, xlabel, ylabel, bins = 20):
    pylab.hist(data, bins = bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1]) # gets temperature from csv
            population.append(tempC)
        except:
            continue
    return population

def getMeansAndSDs(population, sample, verbose = False):
    popMean = sum(population)/len(population)
    sampleMean = sum(sample)/len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' +\
                 '(mean = '  + str(round(popMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        pylab.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' +\
                 '(mean = ' + str(round(sampleMean, 2)) + ')',
                 'Degrees C', 'Number Days')   
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean, numpy.std(population), numpy.std(sample)

# random.seed(0)         
# population = getHighs() # all the temp data from csv
# sample = random.sample(population, 100) # choosing sample
# getMeansAndSDs(population, sample, True)
'''
# RESULTS:
    The graph do not seem like a normal distribution.
    
    Population mean = 16.298769461986048
    Standard deviation of population = 9.437558544803602
    Sample mean = 17.0685
    Standard deviation of sample = 10.390314372048614

Sometimes we should expect that the mean and std from the population are similar
with the ones in the sample and sometimes not.

Let's test this with 1000 samples of 100 values each.
'''

    
# random.seed(0) 
# population = getHighs()
# sampleSize = 100
# numSamples = 1000
# sampleMeans = []
# for i in range(numSamples):
#     sample = random.sample(population, sampleSize)
#     popMean, sampleMean, popSD, sampleSD = getMeansAndSDs(population, sample, verbose = False)
#     sampleMeans.append(sampleMean)
# print('Mean of sample Means =',
#       round(sum(sampleMeans)/len(sampleMeans), 3))
# print('Standard deviation of sample means =',
#       round(numpy.std(sampleMeans), 3))
# makeHist(sampleMeans, 'Means of Samples', 'Mean', 'Frequency')
# pylab.axvline(x = popMean, color = 'r')
'''
# RESULTS:
    The graph is a normal distribution beacuse of the CLT.
    We are plotting the mean of more samples this case.
    
    Mean of sample Means = 16.294
    Standard deviation of sample means = 0.943
'''


## Error Bars for Temperatures
'''
We use this bars to see how as the sample size gets bigger, the error bars
get smaller.
The standard deviations get smaller each time.
The mean keeps being similar for all cases.

'''
# def showErrorBars(population, sizes, numSamples):
#     xVals = []
#     sizeMeans, sizeSDs = [], []
#     for sampleSize in sizes:
#         xVals.append(sampleSize)
#         samplesMeans = []
#         for t in range(numSamples):
#             sample = random.sample(population, sampleSize)
#             popMean, sampleMean, popSD, sampleSD = getMeansAndSDs(population, sample)
#             samplesMeans.append(sampleMean)
#         sizeMeans.append(sum(samplesMeans)/len(samplesMeans))
#         sizeSDs.append(numpy.std(samplesMeans))
#     print(sizeSDs)
#     pylab.errorbar(xVals, sizeMeans,
#                     yerr = 1.96*pylab.array(sizeSDs), fmt = 'o',
#                     label = '95% Confidence Interval')
#     pylab.title('Mean Temperature ('
#                 + str(numSamples) + ' trials)')
#     pylab.xlabel('Sample Size')
#     pylab.ylabel('Mean')
#     pylab.axhline(y = popMean, color ='r', label = 'Population Mean')
#     pylab.xlim(0, sizes[-1] + 10)
#     pylab.legend()

# random.seed(0)
# population = getHighs()   
# showErrorBars(population,
#               (50, 100, 200, 300, 400, 500, 600), 100)





## STANDARD ERROR OF THE MEAN (SEM)
'''
Here we calculate the SEM with 1 sample of each size and
the STD with the means of more samples.

The result is that they are very similar and I can anticipate what the 
STD will be by computing the SEM with just 1 sample and not 50.

If I chose the correct size for my sample depending on the distribution,
I can get an ESTIMATE of the SEM by changing the population STD by the
sample STD.
'''

def sem(popSD, sampleSize):
    return popSD/sampleSize**0.5

sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600)
numSamples = 50
population = getHighs()
popSD = numpy.std(population)
sems = []
sampleSDs = []
# In this first loop we calculate the SEM for each sample
for size in sampleSizes:
    sems.append(sem(popSD, size))
    means = []
    # Here we calculate the STD for each sample
    for t in range(numSamples):
        sample = random.sample(population, size)
        means.append(sum(sample)/len(sample))
    sampleSDs.append(numpy.std(means))
pylab.plot(sampleSizes, sampleSDs,
          label = 'Std of ' + str(numSamples) + ' means')
pylab.plot(sampleSizes, sems, 'r--', label = 'SEM')
pylab.xlabel('Sample Size')
pylab.ylabel('Std and SEM')
pylab.title('SD for ' + str(numSamples) + ' Means and SEM')
pylab.legend()

'''
Example of this:
    If I chose the correct size for my sample depending on the distribution,
    I can get an ESTIMATE of the SEM by changing the population STD by the
    sample STD.
'''


temps = getHighs()
popMean = sum(temps)/len(temps)
sampleSize = 200
numTrials = 10000


# Example
random.seed(0)      
numBad = 0
for t in range(numTrials):
    sample = random.sample(temps, sampleSize)
    sampleMean = sum(sample)/sampleSize
    se = numpy.std(sample)/sampleSize**0.5
    if abs(popMean - sampleMean) > 1.96*se:
        numBad += 1
print('Fraction outside 95% confidence interval =',
      numBad/numTrials)


## DISTRIBUTIONS

# # Exploring some of the most common Distributions
# def plotDistributions():
#     uniform, normal, exp = [], [], []
#     for i in range(100000):
#         uniform.append(random.random())
#         normal.append(random.gauss(0, 1))
#         exp.append(random.expovariate(0.5))
#     makeHist(uniform, 'Uniform', 'Value', 'Frequency')
#     pylab.figure()
#     makeHist(normal, 'Gaussian', 'Value', 'Frequency')
#     pylab.figure()
#     makeHist(exp, 'Exponential', 'Value', 'Frequency')

# plotDistributions()

'''
Notes about distributions:
    # If the population is very asymetric in the distribution you will need
    a lot of samples for more accuracy.
    
    # If is very uniform, you will need many fewer samples.
'''












