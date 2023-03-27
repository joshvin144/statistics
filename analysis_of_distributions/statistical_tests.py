# Import all modules required to execute this section of code, here
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from scipy.stats import ttest_ind
from scipy.stats import ttest_rel
from scipy.stats import f
from scipy.stats import f_oneway

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

# Define a statistical T-Test class
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

# Analisys of Variance (ANOVA) class
class ANOVA(object):
    def __init__(self):
        pass

    def run(self, distribution):
        is_significant_difference = False

        # Custom ANOVA
        num_samples = distribution.samples.shape[0]
        num_groups = int(np.amax(distribution.group))
        mean_within_group = np.zeros(num_groups)
        var_within_group = np.zeros(num_groups)
        std_within_group = np.zeros(num_groups)
        num_samples_within_group = np.zeros(num_groups)
        degrees_of_freedom_within_group = np.zeros(num_groups)
        sum_of_squares_within_group = np.zeros(num_groups)
        mean_between_groups = np.mean(distribution.samples)
        degrees_of_freedom_between = 0
        sum_of_squares_between = 0

        for i in range(num_groups):
            mean_within_group[i] = np.mean(distribution.samples[np.equal(i + 1, distribution.group)])
            var_within_group[i] = np.var(distribution.samples[np.equal(i + 1, distribution.group)])
            std_within_group[i] = np.sqrt(var_within_group[i])
            num_samples_within_group[i] = np.sum(np.equal(i + 1, distribution.group))
            degrees_of_freedom_within_group[i] = num_samples_within_group[i] - 1
            sum_of_squares_within_group[i] = var_within_group[i]*degrees_of_freedom_within_group[i]
            sum_of_squares_between += num_samples_within_group[i]*np.power((mean_within_group[i] - mean_between_groups), 2)

        degrees_of_freedom_between = np.sum(degrees_of_freedom_within_group)
        sum_of_squares_within = np.sum(sum_of_squares_within_group)
        f_stat = sum_of_squares_between/sum_of_squares_within
        p_val = 1 - f.cdf(f_stat, num_groups, degrees_of_freedom_between)
        ic(f_stat, p_val)

        # ANOVA from Scipy
        group_1 = distribution.samples[np.equal(1, distribution.group)]
        group_2 = distribution.samples[np.equal(2, distribution.group)]
        stat, pvalue = f_oneway(group_1, group_2)
        ic(stat, pvalue)

        if (SIGNIFICANCE_LEVEL >= p_val):
            is_significant_difference = True
        return is_significant_difference

