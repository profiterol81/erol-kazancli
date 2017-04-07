import itertools
import numpy as np
from scipy.stats.distributions import binom
import scipy.stats as sc
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.utils import shuffle

# k-nearest-neighbour cluster validation
# returns the optimal number of clusters
# data: data for the cluster analysis
# k: number of neighbours to be used
# J: number of pairs of subsamples
def cluster_validation(data, k, J):

    n_samples = np.shape(data)[0]
    original_data = np.copy(data)

    skewness_values = list()
    mean_values = list()
    percentiles90 = list()
    percentiles75 = list()


    neighbours = np.zeros((n_samples, k+1))
    neigh = NearestNeighbors(n_neighbors=k+1)
    neigh.fit(data)

    # Calculate the neighbours beforehand
    for element in range(0, n_samples):
        distances, indices = neigh.kneighbors(data[element].reshape(1, -1))
        neighbours[element, :] = indices[0][0:k+1]

    # try number of clusters from 2 to 10
    for n_clusters in range(2, 7):
        index_values = list()
        for j in range(0, J):
            # permute to get different samples for each j
            data, neighbours = shuffle(data, neighbours, random_state=0)

            # two subsamples
            sub_sample1 = data[0:n_samples / 2, :]
            sub_sample2 = data[n_samples / 2:n_samples, :]

            neighbours_sample1 = neighbours[0:n_samples / 2, :]
            neighbours_sample2 = neighbours[n_samples / 2:n_samples, :]

            fitted_sample = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
            fitted_sub_sample1 = KMeans(n_clusters=n_clusters, random_state=0).fit(sub_sample1)
            fitted_sub_sample2 = KMeans(n_clusters=n_clusters, random_state=0).fit(sub_sample2)

            # clustering in the whole sample to be used to break symmetry
            clusters = fitted_sample.labels_

            # clustering in the subsamples seperately
            clusters_sub_sample1 = fitted_sub_sample1.labels_
            clusters_sub_sample2 = fitted_sub_sample2.labels_

            clusters_main_part1 = clusters[0:n_samples / 2]
            clusters_main_part2 = clusters[n_samples / 2:n_samples]

            # solve the symmetry problem using the clustering in the whole set
            real_clusters_sub_sample1 = find_real_classes(n_clusters, clusters_sub_sample1, clusters_main_part1)
            real_clusters_sub_sample2 = find_real_classes(n_clusters, clusters_sub_sample2, clusters_main_part2)

            # the final clusters merged from subsamples
            cluster_sets = list()
            neighbours_sets = list()
            for cl in range(0, n_clusters):
                y = np.append(sub_sample1[real_clusters_sub_sample1==cl], sub_sample2[real_clusters_sub_sample2==cl], axis=0)
                cluster_sets.append(y)
                neighbours_sets.append(np.append(neighbours_sample1[real_clusters_sub_sample1==cl], neighbours_sample2[real_clusters_sub_sample2==cl], axis=0))

            sub_sample1_list = sub_sample1.tolist()
            sub_sample2_list = sub_sample2.tolist()

            worst_index = 1000

            # find the worst index value for the clustering
            for cluster_number in range(0, n_clusters):
                cluster = cluster_sets[cluster_number].tolist()
                cluster_neigbours = neighbours_sets[cluster_number]

                total_p1_index = 0
                total_p2_index = 0

                # foreach element in a cluster calculate index values p1 and p2
                for n in range(0, len(cluster)):
                    elem = cluster[n]
                    n_same_sample_membership = 0
                    # distances, indices = neigh.kneighbors(np.array(elem).reshape(1, -1))
                    element_membership = find_sample_membership(elem, sub_sample1_list, sub_sample2_list)
                    k_neighbours = cluster_neigbours[n]
                    # for the k nearest neighbours check if they are in the same subsample as the element
                    for index in k_neighbours:
                        member = original_data[index].tolist()
                        membership = find_sample_membership(member, sub_sample1_list, sub_sample2_list)
                        if membership == element_membership:
                            n_same_sample_membership = n_same_sample_membership + 1

                    p1_index = calculate_p1_index(n_same_sample_membership, k, 0.5)
                    p2_index = calculate_p2_index(n_same_sample_membership, k, 0.5)
                    total_p1_index = total_p1_index + p1_index
                    total_p2_index = total_p2_index + p2_index

                # calculate average index value for a cluster
                p1_ratio = total_p1_index / len(cluster)
                p2_ratio = total_p2_index / len(cluster)

                if p1_ratio < worst_index:
                   worst_index = p1_ratio
            #    if p2_ratio < worst_index:
            #        worst_index = p2_ratio
            # the worst index of the clusters is chosen
            index_values.append(worst_index)

        skewness = find_skewness(index_values)
        perc = np.percentile(index_values, 90)

        perc = np.percentile(index_values, 75)

        mean_values.append(np.mean(index_values))

        index_values = np.ma.array(index_values).compressed() # should be faster to not use masked arrays.
        sortedInd = np.sort(index_values)
        percentiles90.append(sortedInd[90])
        percentiles75.append(sortedInd[75])
        skewness_values.append(skewness)

    return skewness_values, percentiles75, percentiles90

# This function uses the cluster values in th main clustering to break the symmetry problem in the subsamples
# n_clusters: number of clusters
# clusters_sub: clustering of the subsample
# clusters_main_sample: clustering of the coreesponding part in the main clustering
def find_real_classes(n_clusters, clusters_sub, clusters_main_sample):

    classes = list(range(n_clusters))
    perms = list(itertools.permutations(classes, n_clusters))

    bestAccuracy = 0
    real_clusters_sub_sample = np.copy(clusters_sub)

    for i in perms:
        temp_clusters_sub_sample = np.copy(clusters_sub)
        c = 0
        for j in i:
            temp_clusters_sub_sample[clusters_sub==c] = j
            c = c + 1
        accuracy = np.sum(temp_clusters_sub_sample == clusters_main_sample)
        if accuracy > bestAccuracy:
            bestAccuracy = accuracy
            real_clusters_sub_sample = np.copy(temp_clusters_sub_sample)

    return real_clusters_sub_sample

# Finds the subsample the element belongs to
def find_sample_membership(element, sub_sample1, sub_sample2):
    if (element in sub_sample1):
        return 1
    else:
        return 2

# Calculates the P1 index
def calculate_p1_index(n_success, n_attempts, chance_of_success):
    return 1 - binom.cdf(n_success-1, n_attempts, chance_of_success)

# Calculates the P2 index
def calculate_p2_index(n_success, n_attempts, chance_of_success):
    return 2 * min(calculate_p1_index(n_success, n_attempts, chance_of_success), binom.cdf(n_success, n_attempts, chance_of_success))

# Calculates the skewness
def find_skewness(a):
    return sc.skew(a)