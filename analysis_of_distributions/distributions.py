# Import all modules required to execute this section of code, here
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Debugging
from icecream import ic

NUM_INTENSITY_VALUES = 256

# Define parent class, here
class Distribution(object):
	''' Parent class '''
	def __init__(self):
		self.mean = None
		self.standard_deviation = None
		self.equation = None

		self.sample_size = None
		self.samples = None

		self.hist = None
		self.pmf = None
		self.cdf = None

	def histplot(self, num_bins = 0):
		if (np.ndarray != type(self.samples)):
			sys.exit("Distribution not initialized")
		sns.histplot(data = self.samples, bins = num_bins)
		plt.show()

	def dotplot(self):
		if (np.ndarray != type(self.pmf)):
			sys.exit("PMF not initialized")
		fig, axs = plt.subplots(1, 2)
		horizontal_axis = np.arange(self.pmf.shape[0])
		axs[0].plot(horizontal_axis, self.pmf, 'bo')
		axs[1].plot(horizontal_axis, self.cdf, 'bo')
		plt.show()

	def __add__(self, other):
		return self.samples + other.samples

	def __sub__(self, other):
		return self.samples - other.samples

	def __repr__(self):
		return "Distribution"

#### Define children classes, here ####
# Children classes inherit from Distribution

#### Discrete Distributions ####

class Binomial_Distribution(Distribution):
	def __init__(self, num_trials = 1, probability_of_success_on_each_trial = 0.5, num_experiments = 1000):
		super(Binomial_Distribution, self).__init__()
		self.sample_size = num_experiments
		self.samples = np.random.binomial(num_trials, probability_of_success_on_each_trial, num_experiments)
		# Each index represents the number of successful trials out of the total number of trials from 0 to the number of trials
		# Each value represents the number of experiments where said number of successful trials were observed
		# The maximum number of successful trials is the number of Bernoulli trials
		
		sorted_samples = np.sort(self.samples)
		hist = np.zeros(num_trials)
		for experiment in range(num_experiments):
			hist[int(sorted_samples[experiment])] += 1
		self.pmf = sorted_samples/(np.sum(sorted_samples)) # The probability is the number of successful trials divided by the total number of successes
		self.cdf = np.cumsum(self.pmf)

	def __repr__(self):
		return "Binomial Distribution"

#### Continuous Distributions ####

class Normal_Distribution(Distribution):
	def __init__(self, mean = 0, standard_deviation = 1, sample_size = 1000):
		super(Normal_Distribution, self).__init__()

		# Set instance variables, here
		self.mean = mean
		self.standard_deviation = standard_deviation
		self.equation = lambda x : 1/(self.standard_deviation * np.sqrt(2 * np.pi)) * np.exp( - (x - self.mean)**2 / (2 * self.standard_deviation**2))
		self.sample_size = sample_size
		self.samples = np.random.normal(self.mean, self.standard_deviation, self.sample_size)

		def __repr__(self):
			return "Normal Distribution"

class Uniform_Distribution(Distribution):
	def __init__(self, sample_size = 1000):
		super(Uniform_Distribution, self).__init__()

		self.sample_size = sample_size
		self.samples = np.random.uniform(size = sample_size)

		def __repr__(self):
			return "Uniform Distribution"

