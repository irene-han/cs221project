import numpy as np
from sklearn.linear_model import LogisticRegression

IN_FILE = "/home/users/benson97/data_BIO_one_instance" 
PATIENT_FILE = "/home/users/benson97/ICD_defined_depression"

# create a set of relevant patients
patients = set()
f = open(PATIENT_FILE)

for line in f:
	patients.add(line.strip())

f.close()

f = open(IN_FILE)
f.readline() # want to ignore the header...

# 13850 patients have a primary or secondary diagnosis of depression
# need to balance the data.....
no_depression_diagnosis_count = 0

samples = []
labels = []
for line in f: 
	current = line.strip().split()
	
	if current[0] in patients:
		current.pop(0)
		samples.append(current)
		labels.append(1)
	elif no_depression_diagnosis_count < 13850:
		current.pop(0)
		samples.append(current)
		labels.append(0)
		no_depression_diagnosis_count += 1

# lol, is this imputation? help!
for i in range(len(samples)):
	for j in range(len(samples[i])):
		if samples[i][j] == "NA":
			samples[i][j] = 0

# need to make every value a float
convert = []
for i in range(len(samples)):
	current = []
	for j in range(len(samples[i])):
		current.append(float(samples[i][j]))

	convert.append(current)

samples = convert

eighth = int(len(samples) * .8)
train_X = samples[:eighth]
test_X = samples[eighth:]
train_Y = labels[:eighth]
test_Y = labels[eighth:]

logreg = LogisticRegression(random_state=0)
logreg.fit(train_X, train_Y)
print(logreg.score(test_X, test_Y))
