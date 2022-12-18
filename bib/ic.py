#!/usr/bin/python
# coding: utf-8

from scipy import stats
import math
import numpy as np




########################### Nova funcao #############################

# for samples >= 30 
# use method z core

# for samples <= 10
# use method t student

#Function: CI_prinout, a function that outputs a number overlay expressing a sample's Confidence Interval
#Inputs: a dataframe with one column of values. Optional paramater interval for the size of the confidence interval (default is 0.95). Option parameter method that specifies whether the confidence interval will be calculating using the t distribution or a z/normal distribution.
#Outputs: a matplotlib text chart with the % confidence interval and the lower and upper bounds
def mean_confidence_interval(series, interval = 0.95, method = 'z'):
  mean_val = np.mean(series)
  n = len(series)
  stdev = np.std(series)
  
  
  if method == 't':
    test_stat = stats.t.ppf((interval + 1)/2, n)
  elif method == 'z':
    test_stat = stats.norm.ppf((interval + 1)/2)
  lower_bound = mean_val - test_stat * stdev / math.sqrt(n)
  upper_bound = mean_val + test_stat * stdev / math.sqrt(n)
  
  return mean_val, lower_bound, upper_bound, (test_stat * stdev / math.sqrt(n))
  
  

