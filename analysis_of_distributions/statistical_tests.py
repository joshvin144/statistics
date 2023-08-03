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

# Analisys of Variance (ANOVA) Class
class ANOVA(object):
    def __init__(self):
        pass

    # Concatenate distributions that you want to compare
    def run(self, distribution):
        is_significant_difference = False
        p_val = 0

        # Calculate the Grand Mean
        grand_mean = np.mean(distribution.samples)
        ic(grand_mean)
        
        # Extract the number of groups
        number_of_groups = np.max(distribution.group)
        number_of_groups = int(number_of_groups)
        
        # Calculate the group mean for each group
        group_mean = np.zeros(number_of_groups)
        for group_idx in range(number_of_groups):
            group_mean[group_idx] += np.mean(distribution.samples[np.equal(group_idx + 1, distribution.group)])
        ic(group_mean)
        
        # Calculate the Sum of Squares Between Groups
        ssbetween = 0.0
        for group_idx in range(number_of_groups):
            ssbetween += np.sum(np.power((group_mean[group_idx] - grand_mean), 2))
        
        # Calculate the Sum of Squares Within Groups
        sswithin_group = np.zeros(number_of_groups)
        num_samples_in_group = np.zeros(number_of_groups, dtype = np.int)
        num_samples_processed = 0
        for group_idx in range(number_of_groups):
            num_samples_in_group[group_idx] = np.sum(np.equal(group_idx + 1, distribution.group))
            for sample_idx in range(num_samples_in_group[group_idx]):
                sswithin_group[group_idx] += np.power((distribution.samples[num_samples_processed + sample_idx] - group_mean[group_idx]), 2)
            num_samples_processed += num_samples_in_group[group_idx]
        ic(sswithin_group)
        ic(num_samples_in_group)

        # Calculate the Total Sum of Squares Within Groups
        sswithin = np.sum(sswithin_group)

        # Calculate ratio of SSBetween to SSWithin
        f_stat = ssbetween/sswithin
        ic(f_stat)

        # Sample from the f-distribution
        dfn = number_of_groups
        dfd = num_samples_processed - number_of_groups
        p_val = 1 - f.cdf(f_stat, dfn, dfd)

        if (SIGNIFICANCE_LEVEL >= p_val):
            is_significant_difference = True
        return is_significant_difference

