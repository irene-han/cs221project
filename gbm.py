from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import plot_partial_dependence
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy

IN_FILE = "data_biomarkers_double_plus_normalized"
f = open(IN_FILE)

data = []
for line in f:
    row = line.strip().split()
    row_numerical = [ float(val) for val in row ]
    data.append(row_numerical)
print(data[0])
SPLIT_INDEX = int(0.9 * len(data)) 
def gradient_boosting(train):
    # generate feature sets (X)
    X_train = train[0:SPLIT_INDEX]
    X_test = train[SPLIT_INDEX:]

    Y_train = [ row.pop() for row in X_train ]
    Y_test = [ row.pop() for row in X_test ]

    # split training feature and target sets into training and validation subsets
    X_train_sub, X_validation_sub, Y_train_sub, Y_validation_sub = train_test_split(X_train, Y_train, random_state=0)

    # train with Gradient Boosting algorithm
    # compute the accuracy scores on train and validation sets when training with different learning rates
    learning_rates = [0.5] # [0.05, 0.1, 0.25, 0.5, 0.75, 1]
   
    feature_importances = [] 
    for learning_rate in learning_rates:
        gb = GradientBoostingClassifier(n_estimators=100, learning_rate=learning_rate, min_samples_leaf=10, max_features=2, max_depth=3, random_state = 0)
        gb.fit(X_train_sub, Y_train_sub)
        feature_importances = gb.feature_importances_
        print("Learning rate: ", learning_rate)
        print("Accuracy score (training): {0:.3f}".format(gb.score(X_train_sub, Y_train_sub)))
        print("Accuracy score (validation): {0:.3f}".format(gb.score(X_validation_sub, Y_validation_sub)))
        print("Accuracy score (testing): {0:.3f}".format(gb.score(X_test, Y_test)))
        print()

        features = [30, 31, 32]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("pd_direct_bilirubin.png")

        features = [9, 10, 11]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("pd_sodium_in_urine.png")
 
        features = [39, 40, 41]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("pd_cholesterol.png")

        features = [21, 22, 23]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("pd_apoliprotein_a.png")
 
        features = [24, 25, 26]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("pd_apoliprotein_b.png")
  
        features = [18, 19, 20]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("bd_alanine_aminotransferase.png")

        features = [3, 4, 5]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("bd_creatinine_enzymatic.png")

        features = [27, 28, 29]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("bd_aspartate_amino.png")

        features = [57, 58, 59]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("bd_hba1c.png")

        features = [42, 43, 44]
        plot_partial_dependence(gb, X_train_sub, features)
        plt.gcf().savefig("bd_creatinine.png")
 
    return feature_importances

lol  = copy.deepcopy(data)
feature_importances = gradient_boosting(lol)
print(feature_importances)
picked = []

while len(picked) < 10:
    total = 0
    to_add = -1 
    for i in range(0, len(feature_importances)):
        if i in picked: continue

        if feature_importances[i] > total:
            total = feature_importances[i]
            to_add = i

    picked.append(to_add)

print("Features", picked)
print(data[0])
reduced_data = []
count = 0
for row in data:
    if int(row[-1]) == 0: continue 
    new_row = [ row[i] for i in picked ] 
    reduced_data.append(new_row)
    count += 1

print(count)

reduced_data = reduced_data[0:30000]

def dbscan(data, dist):
    # Compute DBSCAN
    db = DBSCAN(eps=dist, min_samples=10).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    counts = {}
    for val in labels:
        counts[val] = counts.get(val, 0) + 1

    print(counts)

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
	
    print('Eps: %f' % dist)
    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    print()

    # Plotting...
    for i in range(1, 10): 
        plot(data, labels, 0, i, i)

def plot(data, labels, x, y, no):
    colors = [(.1372, .43, .588), (.95, .529, .1843), (1, .35, .56), (0.08, .698, .827), (0, 0, 1), 
        (0, .2, 0), (0, .4, 0), (0, .6, 0), (0, .8, 0), (0, 1, 0), (.2, 0, 0), (.4, 0, 0),
        (.6, 0, 0), (.8, 0, 0), (1, 0, 0), (0, 0, 0)]
    fig, ax = plt.subplots()

    for i in range(0, len(labels), 10):
        index = labels[i]
        if index == -1:
            index = 15

        ax.scatter(data[i][x], data[i][y], c=[colors[index]])          

    fig.savefig("please_work_" + str(no) +".png")

distances = [2.75] #[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
for dist in distances:
	dbscan(reduced_data, dist)
