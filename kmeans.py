import argparse
import numpy as np
class Cluster:
    def __init__(self, dot):
        self.center = dot
        self.N = 1

    def get_center(self):
        return self.center

    def update_center(self, dot, sign=1):
        """ center =  (center *N + dot) / N+1 """
        if self.N + sign == 0:
            print("remove the only dot - Error !!")

        f = lambda arr, num : [ele * num for ele in arr]
        tmp = f(self.center,self.N)
        dot = f(dot, sign)
        self.center = [sum(x) for x in zip(tmp,dot)]
        self.N += sign
        self.center = f(self.center, 1/self.N)


    def get_distance(self, dot, sum = 0):
        for axis in range(len(dot)):
            sum += (self.center[axis] - dot[axis]) ** 2
        return sum ** 0.5


def get_dots_from_file(file_name1, file_name2):
    file1 = np.loadtxt(file_name1, delimiter=",")
    file2 = np.loadtxt(file_name2, delimiter=",")
    joined = np.concatenate((file1, file2),axis=1) # join the two file togther to create array of arrays
    return joined


def find_index_nearest_cluster(w):
    # returns a random index by the chances provided by w
    return int(np.random.choice(len(w), 1, replace=False, p=w))


def get_nearest_cluster_distance(dot, cluster_list):
    min_distance = float("inf")
    for j, cluster in enumerate(cluster_list):
        a = np.array(cluster)
        b = np.array(dot)
        d = np.linalg.norm(a-b)
        if d <= min_distance:
            min_distance = d
    return min_distance


def find_initial_clusters(n_dots, k):
    n = len(n_dots)
    first_cluster = n_dots[np.random.randint(n-1)]
    clusters_list = [first_cluster]
    indices = []
    z = 0

    while z < k:
        sum_d = 0
        distances_list = [0]*n
        for j, dot in enumerate(n_dots):
            d = get_nearest_cluster_distance(dot, clusters_list)
            sum_d += d
            distances_list[j] = d

        for i in range(n):
            distances_list[i] = distances_list[i]/sum_d

        index = find_index_nearest_cluster(distances_list)
        indices.append(index)
        clusters_list.append(n_dots[index])
        z += 1
    return indices


def find_index_nearest_cluster(w):

    return int(np.random.choice(len(w), 1 , replace=False , p=w))


def get_nearest_cluster_distance(dot, cluster_list):
    min_distance = float("inf")
    for j, cluster in enumerate(cluster_list):
        d = cluster.get_distance(dot)
        if d <= min_distance:
            min_distance = d
    return min_distance


def find_initial_clusters(n_dots, k):
    n = len(n_dots)
    dot_list = np.array(n_dots)
    np.random.seed(0)
    indices = [0]*k
    first_cluster = Cluster(dot_list[np.random.randint(n-1)])
    clusters_list = [first_cluster]
    z = 1

    while z < k:
        sum_d = 0
        distances_list = [0]*n
        for j, dot in enumerate(n_dots):
            d = get_nearest_cluster_distance(dot, clusters_list)
            sum_d += d
            distances_list[j] = d

        for i in range(n):
            distances_list[i] = distances_list[i]/sum_d

        index = find_index_nearest_cluster(distances_list)
        indices.append(index)
        clusters_list.append(Cluster(n_dots[index]))
        z += 1
    return indices


def load_data_to_dots(file_name1, file_name2):
    file1 = np.loadtxt(file_name1)
    file2 = np.loadtxt(file_name2)
    joined = np.concatenate(file1, file2)
    dots_list = []
    Lines = []
    while (True):
        try:
            line = input()
            Lines.append(line)
        except EOFError:
            break



    for line in Lines:
        dot = [float(word) for word in line.split(sep=",")]
        dots_list.append(dot)
    return dots_list


def get_nearest_cluster_index(dot, cluster_list):
    index_of_min_distance = 0
    min_distance = float("inf")
    for j, cluster in enumerate(cluster_list):
        d = cluster.get_distance(dot)
        if d <= min_distance:
            min_distance = d
            index_of_min_distance = j
    return index_of_min_distance


def print_outputs(dot_list):
    print("expected:")
    for dot in dot_list:
        for num in dot:
            print(num, end=",")
        print("")


def print_results(clusters,):
    for cluster in clusters:
        d=  len(cluster.get_center())
        for i,num in enumerate( cluster.get_center()):
            end_char = "" if i+1==d else ","
            print("%.4f" % num, end=end_char)
        print("")


def kmean():
    parser = argparse.ArgumentParser()
    parser.add_argument("k_num", help="k", type=int)
    parser.add_argument("max_iter", help="max iteration", type=int, default=300, nargs='?')
    parser.add_argument("file_name1", help="file name 1", type=str, nargs='?')
    parser.add_argument("file_name2", help="file name 2", type=str, nargs='?')
    args = parser.parse_args()
    k = args.k_num
    max_iter = args.max_iter
    file_name1 = args.file_name1
    file_name2 = args.file_name2
    assert type(k) is int,"k must be an integer"
    assert k > 0, "k must be positive"
    assert type(max_iter) is int, "max_iter must be an integer"
    assert max_iter > 0, "max_iter must be positive"
    assert type(file_name1) is str, "file path must be a string"
    assert type(file_name2) is str, "file path must be a string"
    dot_list = get_dots_from_file(file_name1, file_name2)
    assert len(dot_list) > k, "k must be smaller than number of input vectors"
    dot_in_cluster = [-1] * len(dot_list)
    dot_should_be_at = [-1] * len(dot_list)
    clusters = []
    indices = find_initial_clusters(dot_list, k)

    for i in indices:  # create K clusters
        clusters.append(Cluster(dot_list[i]))
        dot_in_cluster[i] = i

    iter_num = 0
    is_clsuters_changed = True
    while iter_num < max_iter and is_clsuters_changed:
        is_clsuters_changed = False

        for i, dot in enumerate(dot_list):
            dot_should_be_at[i] = get_nearest_cluster_index(dot, clusters)

        for i, dot in enumerate(dot_list):
            j = dot_should_be_at[i]
            if dot_in_cluster[i] == -1:  ## dot not in any cluster
                clusters[j].update_center(dot)
                dot_in_cluster[i] = j  # set dot i to cluster j
                is_clsuters_changed = True

            elif dot_in_cluster[i] != j:
                clusters[dot_in_cluster[i]].update_center(dot, -1)  ## remove dot from old cluster
                clusters[j].update_center(dot)
                dot_in_cluster[i] = j
                is_clsuters_changed = True

        iter_num += 1



    print_results(clusters)


kmean()