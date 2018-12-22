import numpy as np
import pandas as pd


def init(data,k):
	n = np.shape(data)[1]
    
    # The centroids
	centroids = np.mat(np.zeros((k,n)))

    # Create random centroids (get min, max attribute values, randomize in that range)
	for j in range(n):
		min_j = min(data[:,j])
		range_j = float(max(data[:,j]) - min_j)
		centroids[:,j] = min_j + range_j*np.random.rand(k, 1)

def euclidean_distance(data_point1, data_point2):
		if len(data_point1) != len(data_point2) :
			raise ValueError('feature length not matching')
		else:
			distance = 0
			for x in range(len(data_point1)):
				distance += pow((data_point1[x] - data_point2[x]), 2)
			return math.sqrt(distance)

def cluster(data, k):
	# Number of rows in dataset
	print(np.shape(data)[0])
	m = np.shape(data)[0]

	# Hold the instance cluster assignments
	cluster_assignments = np.mat(np.zeros((m, 2)))

	# Initialize centroids
	centroids = init(data, k)
    
	# Preserve original centroids
	cents_orig = centroids.copy()
    
	changed = True
	num_iter = 0

	# Loop until no changes to cluster assignments
	while changed:

		changed = False

		# For every instance (row in dataset)
		for i in range(m):

			# Track minimum distance, and vector index of associated cluster
			min_dist = np.inf
			min_index = -1

			# Calculate distances
			for j in range(k):

				dist_ji = euclidean_distance(cents[j,:], data[i,:])
				if dist_ji < min_dist:
					min_dist = dist_ji
					min_index = j

			# Check if cluster assignment of instance has changed
			if cluster_assignments[i, 0] != min_index: 
				changed = True

			# Assign instance to appropriate cluster
			cluster_assignments[i, :] = min_index, min_dist**2

		# Update centroid location
		for cent in range(k):
			points = data[np.nonzero(cluster_assignments[:,0].A==cent)[0]]
			cents[cent,:] = np.mean(points, axis=0)

		# Count iterations
		num_iter += 1

	# Return important stuff when done
	return cents, cluster_assignments, num_iter, cents_orig	

def main():
	#load the csv_file as a pandas dataframe. 
	iris_csv_file = './iris.csv'
	names = ['SepalLength_cm', 'SepalWidth_cm', 'PetalLength_cm','PetalWidth_cm','label']
	data = pd.read_csv(iris_csv_file,names=names)
	#print(data)
	feature_columns = ['SepalLength_cm', 'SepalWidth_cm', 'PetalLength_cm','PetalWidth_cm']
	X = data[feature_columns].as_matrix
	#Drop the labels as it is an unsupervised learning problem.
	data.drop(['label'],axis=1,inplace=True) 
	#print(data.shape)
	centroids, cluster_assignments, iters, orig_centroids = cluster(X, 3)
	print('Number of iterations:', iters)
	print('\nFinal centroids:\n', centroids)
	print('\nCluster membership and error of first 10 instances:\n', cluster_assignments[:10])
	print('\nOriginal centroids:\n', orig_centroids)

if __name__=='__main__':
	main()	
			