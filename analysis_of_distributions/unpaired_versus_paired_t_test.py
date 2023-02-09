# Import all modules required to execute this section of code, here
import sys
import numpy as np
from scipy.stats import t
import seaborn as sns
import matplotlib.pyplot as plt

# Debugging
from icecream import ic

SIGNIFICANCE_LEVEL = 0.05

class Independent_T_Test(object):
	def __init__(self):
		pass

	def run(self, distribution_1 = None, distribution_2 = None):
		is_significant_difference = False
		
		sample_size_1 = distribution_1.sample_size
		sample_size_2 = distribution_2.sample_size

		# Calculate the pooled variance
		var_1 = distribution_1.standard_deviation**2
		var_2 = distribution_2.standard_deviation**2
		if (sample_size_1 == sample_size_2):
			pooled_var = (var_1 + var_2)/2
		else:
			pooled_var = ((sample_size_1*var_1) + (sample_size_1*var_2))/(sample_size_1 + sample_size_2 - 2)
		# Calculate the T-Stat
		mean_1 = distribution_1.mean
		mean_2 = distribution_2.mean
		standard_err = np.sqrt(pooled_var*((1/sample_size_1) + (1/sample_size_2)))
		t_stat = np.abs(mean_1 - mean_2)/standard_err

		degrees_of_freedom = sample_size_1 + sample_size_2 - 2
		p = 1 - t.cdf(t_stat, degrees_of_freedom)

		# Debugging
		ic(t_stat, p)

		if (SIGNIFICANCE_LEVEL >= p):
			is_significant_difference = True

		return is_significant_difference

	def __repr__(self):
		return "Independent T-Test"

class Dependent_T_Test(object):
	def __init__(self):
		pass

	def run(self, distribution_1 = None, distribution_2 = None):
		diff = distribution_2 - distribution_1
		
		sample_size = distribution_1.sample_size
		mean_diff = np.mean(diff)
		var_diff = np.var(diff)
		standard_err = np.sqrt(var_diff/sample_size)
		t_stat = (mean_diff - 0)/standard_err
		
		degrees_of_freedom = sample_size - 1
		p = 1 - t.cdf(t_stat, degrees_of_freedom)

		# Debugging
		ic(t_stat, p)
		
		if (SIGNIFICANCE_LEVEL >= p):
			is_significant_difference = True

		return is_significant_difference

	def __repr__(self):
		return "Dependent T-Test"

