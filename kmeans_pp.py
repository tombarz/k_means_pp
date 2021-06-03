import numpy as np
import pandas as pd
import argparse
#import mykmeanssp
import time
import math
#python3 kmeans_pp.py 3 100 input_1_db_1.txt input_1_db_2.txt
def get_dots_from_file(file_name1, file_name2):
    t0 = time.process_time()

    file1 = pd.read_csv(file_name1, prefix="col", header=None)
    file2 = pd.read_csv(file_name2, prefix="col",header=None)
    t1 = time.process_time()
    print(f"time to load files {t1-t0}")
    joined = file1.merge(file2, how="inner", on=["col0"]) # join the two file togther to create array of arrays
    joined = joined.sort_values(by="col0")
    joined = joined.drop(columns=["col0"])
    print(f"time to sort {time.process_time() - t1}")
    return joined.to_numpy()



def find_index_nearest_cluster(w):# returns a random index by the chances provided by w
    return int(np.random.choice(range(len(w)), 1, replace=False, p=w))



def get_cluster_distance(dot, cluster):
    a = np.array(cluster)
    b = np.array(dot)
    d = np.linalg.norm(a-b)
    d = math.pow(d,2)
    return d


def find_initial_clusters(n_dots, k):
    n = len(n_dots)
    random_index = np.random.randint(n-1)
    first_cluster = n_dots[random_index]
    clusters_list = [first_cluster]
    indices = [random_index]
    z = 1
    distances_list = [float("inf")] * n
    while z < k:
        sum_d = 0
        for j, dot in enumerate(n_dots):
            d = get_cluster_distance(dot, clusters_list[z-1])
            if d < distances_list[j]:
                distances_list[j] = d
            sum_d += distances_list[j]

        weights = [0]*n
        for i in range(n):
            weights[i] = distances_list[i]/sum_d

        index = find_index_nearest_cluster(weights)
        indices.append(index)
        clusters_list.append(n_dots[index])
        z += 1
    return indices

def get_cluster_list (dot_list, indices):
    clusters = []
    for ind in indices:
        clusters.append(dot_list[ind])
    return clusters

def check_param(k, max_iter,file_name1,file_name2):
    assert type(k) is int, "k must be an integer"
    assert k > 0, "k must be positive"
    assert type(max_iter) is int, "max_iter must be an integer"
    assert max_iter > 0, "max_iter must be positive"
    assert type(file_name1) is str, "file path must be a string"
    assert type(file_name2) is str, "file path must be a string"

def parse():
    np.set_printoptions(suppress=True,linewidth=1000)
    parser = argparse.ArgumentParser()
    ##TODO make a default option for max iteration
    parser.add_argument("k_num", help="k", type=int)
    parser.add_argument("max_iter", help="max iteration", type=int, default=200, nargs='?')
    parser.add_argument("file_name1", help="file name 1", type=str, nargs='?')
    parser.add_argument("file_name2", help="file name 2", type=str, nargs='?')
    return parser.parse_args()
def main():
    t0= time.process_time()
    np.random.seed(0)
    args = parse()
    k = args.k_num
    max_iter = args.max_iter
    file_name1 = args.file_name1
    file_name2 = args.file_name2
    check_param(k, max_iter, file_name1, file_name2)
    dot_list = get_dots_from_file(file_name1, file_name2)
    assert len(dot_list) > k, "k must be smaller than number of input vectors"
    T1 = time.process_time()
    indices = find_initial_clusters(dot_list, k)
    T2 = time.process_time()
    print("time to find indices:", T2-T1)
    dot_list = dot_list.tolist()
    clusters = get_cluster_list(dot_list, indices)
    #print(dot_list)
    t1 = time.process_time()
    print("time to read files:", time.process_time()-t0)
 #   clusters = np.array(mykmeanssp.fit(max_iter, dot_list, clusters, indices))
  #  clusters = np.round(clusters, 4)
    print("time to kmean files:", time.process_time() - t1)
    print("-----RESULTS:------")
    print(indices)
   # print(clusters)

main()