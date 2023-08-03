# Import all modules required to execute this section of code, here
import argparse
import numpy as np
from distributions import Binomial_Distribution
from distributions import Normal_Distribution
from distributions import Uniform_Distribution
from distributions import detect_outliers_IQR
from statistical_tests import Tester
from statistical_tests import Normality_Test
from statistical_tests import T_Test
from unpaired_versus_paired_t_test import Independent_T_Test
from unpaired_versus_paired_t_test import Dependent_T_Test
from statistical_tests import ANOVA

# Debugging
from icecream import ic

# Add command line arguments, here
def create_argument_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-p", "--plot", action = "store_true")
    return argument_parser

# Define the execution, here
def main():
    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    # Create two sample distributions to compare
    sample_distribution_1 = Normal_Distribution(0,1, group_number = 1)
    sample_distribution_2 = Normal_Distribution(2,1, group_number = 2)
    
    # Concatenate the distributions
    sample_distribution_concatenated = sample_distribution_1 + sample_distribution_2

    # Initialize the tester function
    normality_test = Normality_Test()
    # Initialize the tester
    tester = Tester(normality_test)

    # Run the tester
    is_normal = tester.run(sample_distribution_1)
    print("There is evidence to suggest that the distribution is normal if the test results are False.\nThere is evidence to suggest that the distribution is not normal if the test results are True.\nTest results:\t{:b}\n".format(is_normal))

    # Initialize and run a T-Test
    # t_test = T_Test()
    # is_significant_difference = t_test.run(sample_distribution_1, sample_distribution_2)
    # print("There is evidence to suggest that there is a significant difference between the two distributions if the test results are True.\nTest results: {:b}\n".format(is_significant_difference))

    # Initialize and run an ANOVA
    anova_test = ANOVA()
    # Initialize the tester
    tester = Tester(anova_test)

    # Run the tester
    is_significant_difference = tester.run(sample_distribution_concatenated)
    print("There is evidence to suggest that the groups are not significantly different if the results are False.\nTest results:\t{:b}\n".format(is_significant_difference))

    if (args.plot):
        sample_distribution_1.dotplot()

    return 0

# There should be no need to touch this
if (__name__ == "__main__"):
    _ = main()

