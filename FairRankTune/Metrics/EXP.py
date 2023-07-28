import numpy as np
from FairRankTune.Metrics.ComboUtil import *
# Script to calculate Exposure-based metrics
# References: Singh, A., & Joachims, T. (2018, July). Fairness of exposure in rankings.
# In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2219-2228).
def EXP(ranking, group_ids, combo):
    """
    Calculate EXP score (Singh et. al)
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param combo: String aggregation metric for calculating meta metric
    :return: EXP value, numpy array of group average exposure
    """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    vals = grp_exposures / grp_count_items
    if combo == 'MinMaxRatio':
        return MinMaxRatio(vals), vals
    if combo == 'MaxMinRatio':
        return MaxMinRatio(vals), vals
    if combo == 'MaxMinDiff':
        return MaxMinDiff(vals), vals
    if combo == 'MaxAbsDiff':
        return MaxAbsDiff(vals), vals
    if combo == 'MeanAbsDev':
        return MeanAbsDev(vals), vals
    if combo == 'LTwo':
        return LTwo(vals), vals
    if combo == 'Variance':
        return Variance(vals), vals

def EXPU(ranking, group_ids, relevance, combo):
    """
    Calculate EXPU (Exposure-Utility) score (Singh et. al)
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param relvance: Numpy array of relevance values for items
    :param combo: String aggregation metric for calculating meta metric
    :return: EXPU value, numpy array of group ratios of average exposure and average utility
    """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    grp_relevances = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        rel_of_item = relevance[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item
        grp_relevances[grp_of_item] += rel_of_item

    avg_exp = grp_exposures / grp_count_items
    avg_utility = grp_relevances /grp_count_items
    vals = avg_exp/avg_utility
    if combo == 'MinMaxRatio':
        return MinMaxRatio(vals), vals
    if combo == 'MaxMinRatio':
        return MaxMinRatio(vals), vals
    if combo == 'MaxMinDiff':
        return MaxMinDiff(vals), vals
    if combo == 'MaxAbsDiff':
        return MaxAbsDiff(vals), vals
    if combo == 'MeanAbsDev':
        return MeanAbsDev(vals), vals
    if combo == 'LTwo':
        return LTwo(vals), vals
    if combo == 'Variance':
        return Variance(vals), vals

def EXPRU(ranking, group_ids, relevance, ctr, combo):
    """
    Calculate EXPRU (Exposure Realized Utility) score (Singh et. al)
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param relvance: Numpy array of relevance values for items
    :param ctr: Numpy array of click through rates for items (could be 0,1 values or floats)
    :param combo: String aggregation metric for calculating meta metric
    :return: EXPRU value, numpy array of group ratios of average click-through-rate and average utility
    """

    if np.any((relevance < 0) | (relevance > 1)):
        assert("Exposure (RBP) requires that relevance score be either 0 (not relevant) or 1 (relevant). ")

    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    grp_ctr= np.zeros_like(unique_grps, dtype=np.float64)
    grp_relevances = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        ctr_of_item = ctr[i]
        rel_of_item = relevance[i]
        #update total group exp
        grp_ctr[grp_of_item] += ctr_of_item
        grp_relevances[grp_of_item] += rel_of_item

    avg_ctr = grp_ctr / grp_count_items
    avg_utility = grp_relevances /grp_count_items
    vals = avg_ctr/avg_utility
    if combo == 'MinMaxRatio':
        return MinMaxRatio(vals), vals
    if combo == 'MaxMinRatio':
        return MaxMinRatio(vals), vals
    if combo == 'MaxMinDiff':
        return MaxMinDiff(vals), vals
    if combo == 'MaxAbsDiff':
        return MaxAbsDiff(vals), vals
    if combo == 'MeanAbsDev':
        return MeanAbsDev(vals), vals
    if combo == 'LTwo':
        return LTwo(vals), vals
    if combo == 'Variance':
        return Variance(vals), vals

def exp_at_position_array(num_items):
    return np.array([(1/(np.log2(i+1))) for i in range(1,num_items+1)])