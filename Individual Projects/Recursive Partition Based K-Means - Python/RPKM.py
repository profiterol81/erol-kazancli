import numpy as np
import random
import math

# finds clustering of the given data according to rpkm algorithm
# data: data to be partitioned
# m_min: minimum partition degree
# m_max: maximum partition degree
# k: number of clusters
def find_RPKM_clustering(data, m_min, m_max, k):

    n_samples = np.shape(data)[0]
    n_dimensions = np.shape(data)[1]

    # find all the partitions from m_min to m_max
    partitions, partitions_metadata = find_initial_partitions(data, m_min, m_max)

    best_error = n_samples * 10
    best_partition_number = 0
    new_clusters = list()

    # starting from the coarsest partition to the finest apply weighted lloyd and find the best error
    for partitioning_number in range(0, m_max-m_min + 1):
        cores = list()

        metadata = partitions_metadata[partitioning_number]
        # choose randomly cores
        indices_cores = random.sample(range(0, len(metadata)), k)

        for cluster in range(0, k):
            core_meta = metadata[indices_cores[cluster]]
            core = core_meta[0]
            cores.append(core)

        previous_error = n_samples * 10
        error_difference = n_samples * 10
        i = 0

        # apply weighted lloyd 1000 times or until the error does not change
        while i < 100 and error_difference > 0.1:
            new_clusters = update_clusters(cores, metadata)
            new_cores, error = update_cores(new_clusters, metadata, k, n_dimensions)
            cores = new_cores
            error_difference = abs(previous_error - error)
            previous_error = error
            i = i + 1
        # Choose the best error through mMin to mMax partitions and store it
        if error < best_error:
            best_error = error
            best_partition_number = partitioning_number
            best_clusters = np.array(new_clusters)

    chosen_partition = partitions[:, best_partition_number]

    result_clustering = np.copy(chosen_partition)
    # find the resulting clustering according to the best error through all the partitions
    for i in range(0, k):
        indices = np.where(best_clusters == i)[0]
        for j in range(0, np.shape(indices)[0]):
            result_clustering[chosen_partition == indices[j]] = i

    return result_clustering

# finds initial partitions by dividing each dimension into equal-sized intervals
# data: data to be partitioned
# m_min: minimum partition degree
# m_max: maximum partition degree
def find_initial_partitions(data, m_min, m_max):

    n_samples = np.shape(data)[0]
    n_dimensions = np.shape(data)[1]

    partitions = np.zeros((n_samples, m_max-m_min+1)).astype(int)

    features_min_max = list()

    # find min max values for each feature
    for d in range(0, n_dimensions):
        min_value = np.min(data[:, d])
        max_value = np.max(data[:, d])
        features_min_max.append([min_value, max_value])

    partitions_metadata = list()

    # calculate all the partitions by dividing by two each dimensions for the first dimension and for each subsequent
    # partitions dividing by further two
    for partitioning_number in range(0, m_max-m_min + 1):

        partition = np.zeros((n_samples))
        division = (2 ** partitioning_number) * m_min
        initial_groups = list()
        for n in range(0,n_samples):
            element = data[n]
            real_group = 0
            for d in range(0, n_dimensions):
                feature_info = features_min_max[d]
                min_value = feature_info[0]
                max_value = feature_info[1]
                difference = float(max_value - min_value)
                interval = difference / division
                interim_group = math.floor((element[d] - min_value) / interval)
                if interim_group == division:
                    interim_group = interim_group - 1
                real_group = int((real_group * division) + interim_group)
            partition[n] = real_group
            if real_group not in initial_groups:
                initial_groups.append(real_group)

        # make partition numbers sequential(eliminate partitions that do not have any elements)
        interim = np.copy(partition)
        n_partition = 0
        for i in initial_groups:
            partition[interim == i] = n_partition
            n_partition = n_partition + 1

        meta_info = list()
        # form the partitions with metadata - avg and weight.
        for m in range(0, n_partition):
            group = data[partition == m]
            info = list()
            # Calculate the meta data such as average and the weight
            if len(group) > 0:
                avg = sum(group) / float(len(group))
                info.append(list(avg))
                info.append(len(group))
                meta_info.append(info)
        partitions[:, partitioning_number] = partition
        partitions_metadata.append(meta_info)

    return  partitions, partitions_metadata

# weighted lloyd update clusters step
# cores: the chosen cores
# partitions_meta: the average and weight which represent each partition
# return clusters: the resulting clusters
def update_clusters(cores, partitions_meta):
    clusters = list()

    for i in range(0, len(partitions_meta)):
        metadata = partitions_meta[i]
        avg = metadata[0]
        difference = 100000
        core_index = -1
        for j in range(0, len(cores)):
            # new_difference = math.sqrt(find_difference(cores[j], avg))
            new_difference = find_difference(cores[j], avg)
            if new_difference < difference:
                difference = new_difference
                core_index = j
        clusters.append(core_index)
    return clusters

# calculate the new cores according to the previous clusters found
# clusters: the clusters found in the previous step
# partition_meta:the average and weight which represent each partition
# the number of clusters
# n_dimensions: the number of dimensions
# return core: new cores
# return error: resulting error
def update_cores(clusters, partition_meta, k, n_dimensions):
    length = len(partition_meta)
    clusters = np.array(clusters)
    partition_meta_array = np.array(partition_meta)
    avgs = partition_meta_array[:, 0]
    weights = partition_meta_array[:, 1]
    weighted_averages = np.empty([length, n_dimensions])
    for i in range(0, length):
        weighted_averages[i] = np.multiply(avgs[i], weights[i])
    cores = list()
    for i in range(0, k):
        core = np.sum(weighted_averages[clusters == i], axis=0) / np.sum(weights[clusters==i])
        cores.append(list(core))

    diff = 0
    for i in range(0, length):
        diff = diff + find_difference(cores[clusters[i]], avgs[i]) * weights[i]

    error = diff

    return cores, error

# find difference between two points
def find_difference(point1, point2):
    dim = len(point1)
    diff = 0
    for i in range(0, dim):
        diff = diff + (point1[i] - point2[i]) ** 2
    return diff

# finds error in clustering
def find_error_clustering(clustering, X, k):
    error = 0
    for i in range (0, k):
        cluster = X[clustering==i]
        mean = np.mean(X[clustering==i], axis=0)
        for j in range (0, cluster.shape[0]):
            error = error + find_difference(mean, cluster[j])


    return error