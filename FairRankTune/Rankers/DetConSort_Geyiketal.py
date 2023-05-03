import numpy as np
import math
from collections import defaultdict as ddict

def DETCONSORT(current_ranking, current_group_ids, current_ranking_scores, distribution, k):
    """
    DetConSort reranking algorithm.
    :param current_ranking: Numpy array of items to rerank.
    :param current_group_ids: Numpy array of group ids corresponding to the current_ranking.
    :param current_ranking_scores: Numpy array of scores corresponding to the current_ranking.
    :param distribution: Numpy array of the target distribution "p" in the paper. Ex. [.5, .5] is a fifty-fifty split.
    :param k: How long the returned ranking should be.
    :return: reranking, Numpy array of item, reranking_ids, Numpy array of group ids for reranking, Numpy array of scores for reranking,
    """

    #score_list is <group id>  <score> and <rank> <startrank> <id>
    score_list = [(current_group_ids[i], current_ranking_scores[i], i+1, i+1, current_ranking[i]) for i in range(len(current_ranking))]

    unique_group_ids = list(np.unique(current_group_ids))
    AttrScores = {}
    num_items_per_group = {}
    min_grp_count = {}
    GlobalAttrCounts = {}
    constructed_ranking_group_ids = {}  # []
    rankedScoreList = {}  # []
    maxIndices = {}  # []
    last_empty_indx = 0
    k_iter = 0

    for grp_id in unique_group_ids:
        num_items_per_group[grp_id] = 0
        min_grp_count[grp_id] = 0
        GlobalAttrCounts[grp_id] = sum([1 for elem in score_list if elem[0] == grp_id])
        AttrScores[grp_id] = [(item[1], item[0], item[2], item[3], item[4]) for item in score_list if
                            item[0] == grp_id]  # to be initialized

    while last_empty_indx <= k:

        if last_empty_indx == len(score_list):
            break

        k_iter += 1
        temp_min_attr_count_for_curr_prefix = ddict(int)
        changedMins = {}
        for grp_id in unique_group_ids:
            temp_min_attr_count_for_curr_prefix[grp_id] = math.floor(k_iter * distribution[grp_id])
            if min_grp_count[grp_id] < temp_min_attr_count_for_curr_prefix[grp_id] and min_grp_count[grp_id] < GlobalAttrCounts[grp_id]:
                changedMins[grp_id] = AttrScores[grp_id][num_items_per_group[grp_id]]

        if len(changedMins) != 0:
            ordChangedMins = sorted(changedMins.items(), key=lambda x: x[1][0], reverse=True)
            for item in ordChangedMins:
                constructed_ranking_group_ids[last_empty_indx] = item[0]
                rankedScoreList[last_empty_indx] = item[1]
                maxIndices[last_empty_indx] = k_iter
                start = last_empty_indx
                while start > 0 and maxIndices[start - 1] >= start and rankedScoreList[start - 1][0] < \
                        rankedScoreList[start][0]:
                    swap(rankedScoreList, start - 1, start)
                    swap(maxIndices, start - 1, start)
                    swap(constructed_ranking_group_ids, start - 1, start)
                    start -= 1
                num_items_per_group[item[0]] += 1
                last_empty_indx += 1
            min_grp_count = dict(temp_min_attr_count_for_curr_prefix)

    K_items = []
    K_scores = []

    for i in range(0,k):
        item = rankedScoreList[i]
        K_items.append(int(item[4]))
        K_scores.append(item[0])

    reranking = np.asarray(K_items)
    reranking_scores = np.asarray(K_scores)
    current_rank = list(current_ranking)
    reranking_ids = np.asarray([current_group_ids[current_rank.index(item)] for item in reranking])
    return reranking, reranking_ids, reranking_scores


def getdist(p):
    # Given a list, return the true protected attr dist as a dictionary
    d = {}
    for person in p:
        if person['real_attr'] not in d:
            d[person['real_attr']]=1
        else:
            d[person['real_attr']]+=1
    for attr in d:
        d[attr] = d[attr]/len(p)
    return d

def swap(temp_list, pos_i, pos_j):
    temp = temp_list[pos_i]
    temp_list[pos_i] = temp_list[pos_j]
    temp_list[pos_j] = temp
