# Import all modules required to execute this section of code, here
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from scipy.stats import ttest_ind
from scipy.stats import ttest_rel

# Debugging
from icecream import ic

# Define "constants," here
SIGNIFICANCE_LEVEL = 0.05

# Define a generic tester class to test ONE distribution at a time
class Tester(object):
	def __init__(self, test_func = None):
		self.test_func = test_func

	def run(self, distribution = None):
		test_passed = False
		test_passed = self.test_func.run(distribution)
		return test_passed

	def __repr__(self):
		"Tester"

#### Statistical tests to pass to the tester ####

# Normality test
class Normality_Test(object):
	def __init__(self):
		pass

	def run(self, distribution = None):
		''' There is evidence to suggest that the distribution is not normal
		if the return value is True'''
		test_passed = False
		stat, p = shapiro(distribution.samples)
		if (SIGNIFICANCE_LEVEL >= p):
			test_passed = True
		return test_passed

	def __repr__(self):
		return "Normality_Test"

#### Statistical tests that are not compatible with the tester, yet ####

# Define a statistical test class
class T_Test(object):
	def __init__(self, is_independent = True):
		self.is_independent = is_independent

	def run(self, distribution_1 = None, distribution_2 = None):
		is_significant_difference = False
		if (self.is_independent):
			stat, p = ttest_ind(distribution_1.samples, distribution_2.samples)
		else:
			stat, p, df = ttest_rel(distribution_1.samples, distribution_2.samples)

		# Debugging
		ic(stat, p)
		
		if (SIGNIFICANCE_LEVEL >= p):
			is_significant_difference = True
		return is_significant_difference

	def plot(self, distribution_1 = None, distribution_2 = None):
		sns.histplot(data = distribution_1.samples)
		sns.histplot(data = distribution_2.samples)
		plt.show()

	def __repr__(self):
		return "T_Test"

