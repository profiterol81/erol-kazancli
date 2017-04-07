from sklearn.cluster import KMeans
import sklearn.preprocessing as pp
import numpy as np
import RPKM as rpkm
import sklearn.datasets as sc

# flea beetles data
X = np.array([[150,15],[147,13],[144,14],[144,16],[153,13],[140,15],[151,14],[143,14],[144,14],[142,15],[141,13],[150,15],[148,13],
[154,15],[147,14],[137,14],[134,15],[157,14],[149,13],[147,13],[148,14],[120,14],[123,16],[130,14],[131,16],[116,16],[122,15],
[127,15],[132,16],[125,14],[119,13],[122,13],[120,15],[119,14],[123,15],[125,15],[125,14],[129,14],[130,13],[129,13],[122,12],
[129,15],[124,15],[120,13],[119,16],[119,14],[133,13],[121,15],[128,14],[129,14],[124,13],[129,14],[145,8],[140,11],[140,11],
[131,10],[139,11],[139,10],[136,12],[129,11],[140,10],[137,9],[141,11],[138,9],[143,9],[142,11],[144,10],[138,10],[140,10],[130,9],
[137,11],[137,10],[136,9],[140,10]])

# generated data
# generated_data = sc.make_classification(n_samples=1000, n_features=3, n_classes=3, n_clusters_per_class=2, n_informative=3, n_redundant=0)
# X = np.array(generated_data[0])

X = pp.scale(X)

mMax = 5
mMin = 2
k = 3

clustering = rpkm.find_RPKM_clustering(X, mMin, mMax, k)

kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
clustersKmeans = kmeans.labels_

error_rpkm = rpkm.find_error_clustering(clustering, X, k)
error_kmeans = rpkm.find_error_clustering(clustersKmeans, X, k)

print "error with rpkm algorithm:" + str(error_rpkm)
print "error with k-means algorithm:" + str(error_kmeans)
