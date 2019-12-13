from sklearn.cluster import KMeans
import numpy as np
import pprint 

IN_FILE = "/home/users/benson97/data_BIO_one_instance" 
PATIENT_FILE = "/home/users/benson97/ICD_defined_depression"
N_CLUSTERS = 15

# create a set of relevant patients
patients = set()
f = open(PATIENT_FILE)

for line in f:
	patients.add(line.strip())

f.close()

f = open(IN_FILE)
f.readline() # want to ignore the header...

yes_depression = []
no_depression = []

for line in f: 
	current = line.strip().split()
	
	if current[0] in patients:
		current.pop(0)
		yes_depression.append(current)
	else:
		current.pop(0)
		no_depression.append(current)

# lol, is this imputation? help!
for i in range(len(yes_depression)):
	for j in range(len(yes_depression[i])):
		if yes_depression[i][j] == "NA":
			yes_depression[i][j] = 0

for i in range(len(no_depression)):
	for j in range(len(no_depression[i])):
		if no_depression[i][j] == "NA":
			no_depression[i][j] = 0

# need to make every value a float
convert = []
for i in range(len(yes_depression)):
	current = []
	for j in range(len(yes_depression[i])):
		current.append(float(yes_depression[i][j]))

	convert.append(current)

yes_depression = convert

convert = []
for i in range(len(no_depression)):
	current = []
	for j in range(len(no_depression[i])):
		current.append(float(no_depression[i][j]))

	convert.append(current)

no_depression = convert

eighth = int(len(yes_depression) * .8)
yes_train = yes_depression[:eighth]
yes_test = yes_depression[eighth:]

# 13850 is the number of people diagnosed with Depression
no_test = no_depression[eighth: 13850]

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0).fit(yes_train) 

print(kmeans.score(yes_test))
print(kmeans.score(no_test))

yes_results = kmeans.predict(yes_test)
no_results = kmeans.predict(no_test)

yes_clusters = {}
for result in yes_results: 
	yes_clusters[result] = yes_clusters.get(result, 0) + 1

no_clusters = {}
for result in no_results:
	no_clusters[result] = no_clusters.get(result, 0) + 1

pprint.pprint(yes_clusters)
pprint.pprint(no_clusters)
