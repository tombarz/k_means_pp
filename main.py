import mykmeanssp
import numpy as np

# To use this run in the terminal: python setup.py build_ext --inplace
# And on Nova: python3.8.5 setup.py build_ext --inplace
# os.system("python setup.py build_ext --inplace")

def test_3_caes():

    data=[0]*3
    data[0] = (3,"input_1.txt")
    data[1] = (7,"input_2.txt")
    data[2] = (15,"input_3.txt")
    for row in data:
        print(row)
        test_hw1_data(row)


def test_hw1_data( test_data):
    k =test_data[0]
    filename = test_data[1]

    np.set_printoptions(suppress=True, linewidth=15*k)
    dots = []
    clusters = []
    indexs = []

    with open(filename, "r") as txt_file:
      txt =  txt_file.readlines()

    txt_file.close()
    for line in txt:
        line = line[:-1].split(",")
        line = [float(i) for i in line]
        dots.append(line)

    for j,dot in enumerate(dots):
        clusters.append(dot)
        indexs.append(j)
        if j+1==k:
            break

    max_iter= 200
    #print(dots)

    clusters = np.array(mykmeanssp.fit(max_iter, dots, clusters, indexs))
    clusters = np.round(clusters,4)
    print(clusters)
##print("got clusters back:")
##for dot in clusters:
##    for val in dot:
 ##       print('%.4f' %val,end=",")
  ##  print(" ")


test_3_caes()