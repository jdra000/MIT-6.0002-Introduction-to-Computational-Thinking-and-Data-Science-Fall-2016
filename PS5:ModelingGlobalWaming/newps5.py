#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 17:20:51 2024

@author: juanrey
"""

# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy 
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import random

import warnings
warnings.simplefilter('ignore', numpy.exceptions.RankWarning)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for d in degs:
        model = pylab.polyfit(x, y, d)
        models.append(model)
    return models
    # return pylab.array([pylab.polyfit(x, y, deg) for deg in degs])

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    return r2_score(y, estimated)

def evaluate_models_on_training(x, y, models, degrees, slope = True, yLabel = False):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """

    # 1. Plot values
    pylab.plot(x, y, 'bo', label = 'Data')
    # 2. Test models
    for i in range(len(models)):
        
        estYVals = pylab.polyval(models[i], x)
        error = r_squared(y, estYVals)
        if slope:
            se = se_over_slope(x, y, estYVals, models[i])

        pylab.plot(x, estYVals, label = 'Fit of degree ' + str(degrees[i]) \
                   + ', $R^{2}=$ = ' + str(round(error, 5)))
            
    pylab.legend(loc = 'best')
    pylab.xlabel('Year')
    pylab.ylabel('$Temperature\ (C\degree)$')
    if slope:
        pylab.title('Temperature vs. Time\n' + ('se_over_slope: '+ str(round(se, 2))))
    else:
        pylab.title('Temperature vs. Time')
        
    if yLabel:
        pylab.ylabel('STD')


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # new = []
    # avg = 0
    # for year in years:
    #     for city in multi_cities:
    #         avg += sum(climate.get_yearly_temp(city, year)) / len(climate.get_yearly_temp(city, year))
    #     new.append(avg / len(years))
    
    # cities_averages = [pylab.array( [climate.get_yearly_temp(city, year)
    #     for city in multi_cities]).mean(axis=0).mean() for year in years]
    
    cities_avg = []
    for year in years:
        cities_avg_local = []
        for city in multi_cities:
            cities_avg_local.append(climate.get_yearly_temp(city, year).mean())
        cities_avg.append(numpy.mean(cities_avg_local))
        
    return pylab.array(cities_avg)
    

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

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """    
    return mean_squared_error(y, estimated)

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    cities_std = []
    for year in years:
        cities_avg = []
        for city in multi_cities:
            cities_avg.append(numpy.std(climate.get_yearly_temp(city, year)).mean())
        cities_std.append(numpy.mean(cities_avg))
        
    return pylab.array(cities_std)

## HOT TEMPERATURES
def gen_hot_temp(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    cities_std = []
    for year in years:
        cities_hot_temp = []
        for city in multi_cities:
            for temp in climate.get_yearly_temp(city, year):
                if temp >= 35:
                    cities_hot_temp.append(temp)
        cities_std.append(numpy.mean(cities_hot_temp))
        
    return pylab.array(cities_std)



def random_dist(xVals, yVals):
    
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
    dimensions = (1, 2, 3, 4, 20, 30)
    rSquares = {}
    for d in dimensions:
        rSquares[d] = []
    
    
    for f in range(numSubsets):
        trainX, trainY, testX, testY = splitData(xVals, yVals)
        for d in dimensions:
            model = pylab.polyfit(trainX, trainY, d)
    
            # How well polyval predict the test set instead of the training one.
            estYVals = pylab.polyval(model, testX)
            rSquares[d].append(r_squared(testY, estYVals))
            
    print('Mean R-squares for test data')
    for d in dimensions:
        mean = round(sum(rSquares[d])/len(rSquares[d]), 4)
        sd = round(numpy.std(rSquares[d]), 4)
        print('For dimensionality', d, 'mean =', mean,
              'Std =', sd)  
        
    
    
###### IMPLEMENTATION

if __name__ == '__main__': 
    climate = Climate("./data.csv")
    
    TRAINING_INTERVAL = pylab.array(range(1961, 2010))
    TESTING_INTERVAL = range(2010, 2016)
    NEW_INTERVAL = range(1961, 2016)
    
    # cities in our weather data
    CITIES = [
        'BOSTON',
        'SEATTLE',
        'SAN DIEGO',
        'PHILADELPHIA',
        'PHOENIX',
        'LAS VEGAS',
        'CHARLOTTE',
        'DALLAS',
        'BALTIMORE',
        'SAN JUAN',
        'LOS ANGELES',
        'MIAMI',
        'NEW ORLEANS',
        'ALBUQUERQUE',
        'PORTLAND',
        'SAN FRANCISCO',
        'TAMPA',
        'NEW YORK',
        'DETROIT',
        'ST LOUIS',
        'CHICAGO'
    ]
    

    ###### Part A.4.I
    # # 1. Generate Data
    # sample = pylab.array([climate.get_daily_temp('NEW YORK', 1, 10, year)
    #         for year in TRAINING_INTERVAL])
   
    # # 2. Fitting data to a degree-one polynomial
    # models = generate_models(training_interval, sample, [1])
    # # 3. Evalute linear model
    # evaluate_models_on_training(training_interval, sample, models, [1])


    ###### Part A.4.II
    # # 1. Generate Data
    # sample = pylab.array([pylab.average(climate.get_yearly_temp('NEW YORK', year))
    #                         for year in TRAINING_INTERVAL])
    
    # # 2. Fitting data to a degree-one polynomial
    # models = generate_models(TRAINING_INTERVAL, sample, [1])
    # # 3. Evalute linear model
    # evaluate_models_on_training(TRAINING_INTERVAL, sample, models, [1])


    ###### Part B
    # # 1. Generate Data
    # national_yearly_temp = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    
    # # 2. Fitting Data to a degree-one polynomial
    # models = generate_models(TRAINING_INTERVAL, national_yearly_temp, [1])
    # # 3. Evaluate linear model
    # evaluate_models_on_training(TRAINING_INTERVAL, national_yearly_temp, models, [1])
   
   
   
    ##### Part C
    # # 1. Generate Data
    # national_yearly_temp = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    # sample = moving_average(national_yearly_temp, 5)
    # # 2. Fitting Data to a degree-one polynomial
    # models = generate_models(TRAINING_INTERVAL, sample, [1])
    # # 3. Evaluate linear model
    # evaluate_models_on_training(TRAINING_INTERVAL, sample, models, [1])



    # ##### Part D.1
    # # 1. Generate Data
    # national_yearly_temp = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    # sample = moving_average(national_yearly_temp, 5)
    # # 2. Fitting Data to 1, 2 and 20 degree polynomial
    # models = generate_models(TRAINING_INTERVAL, sample, [1,2,20])
    # # 3. Evaluate Models
    # evaluate_models_on_training(TRAINING_INTERVAL, sample, models, [1,2,20], False)
    
    ###### Part D.2
    # # Evaluating Models
    new_interval = range(1961, 2016)
    national_yearly_temp = gen_cities_avg(climate, CITIES, new_interval)
    random_dist(new_interval, national_yearly_temp)

    
    #### Part E.1
    # 1. Generate Data
    national_yearly_temp_std = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    sample = moving_average(national_yearly_temp_std, 5)
    # 2. Fitting data
    models = generate_models(TRAINING_INTERVAL, sample, [1])
    # 3. Evaluate Models
    evaluate_models_on_training(TRAINING_INTERVAL, sample, models, [1], yLabel=True)
    
    
    
    # ##### Part E.2
    # # 1. Generate Data
    # national_yearly_temp_std = gen_hot_temp(climate, CITIES, NEW_INTERVAL)
    # sample = moving_average(national_yearly_temp_std, 5)
    # # 2. Fitting data
    # models = generate_models(NEW_INTERVAL, sample, [1,2])
    # # 3. Evaluate Models
    # evaluate_models_on_training(NEW_INTERVAL, sample, models, [1,2], False)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    