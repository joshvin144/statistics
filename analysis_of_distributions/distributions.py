# Import all modules required to execute this section of code, here
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define parent class, here
class Distribution(object):
	''' Parent class '''
	def __init__(self):
		self.mean = None
		self.standard_deviation = None
		self.equation = None
		self.sample_size = None
		self.samples = None

	def plot(self):
		if (np.ndarray != type(self.samples)):
			sys.exit("Distribution not initialized")
		sns.histplot(data = self.samples)
		plt.show()

	def __add__(self, other):
		return self.samples + other.samples

	def __sub__(self, other):
		return self.samples - other.samples

	def __repr__(self):
		return "Distribution"

# Define children classes, here
# Children classes inherit from Distribution
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

