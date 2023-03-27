# Import all modules required to execute this section of code, here
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# RMS
def root_mean_square(samples):
	rms = np.power(samples, 2)
	rms = np.sum(rms)
	rms /= samples.shape[0]
	rms = np.sqrt(rms)
	return rms