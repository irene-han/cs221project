from scipy import stats
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

IN_FILE = "data_biomarkers_plus_one"
OUT_FILE = "data_biomarkers_normalized_by_age_v2"

f = open(IN_FILE)
header = f.readline()

#extract raw data
raw_data = []
for line in f:
	row = line.strip().split()
	raw_data.append(row)

for i in range(0, len(raw_data)):
	for j in range(0, len(raw_data[i])):
		if raw_data[i][j] == "NA":
			raw_data[i][j] = 0

for i in range(0, len(raw_data[0])):
	total = 0.0
	count = 0
	for j in range(0, len(raw_data)):
		if raw_data[j][i] != "NA":
			total += float(raw_data[j][i])
			count += 1

	average = total / count

	for j in range(0, len(raw_data)):
		if raw_data[j][i] == "NA":
			raw_data[j][i] = average

#extract sex and age vector
sex = [float(row[1]) for row in raw_data]
age = [float(row[4]) for row in raw_data]
sex_age = [[float(row[1]), float(row[4])] for row in raw_data]

print_count = 5
#extract biomarker data
data = [ [] for i in range(0, len(raw_data)) ]
for i in range(5, len(raw_data[0])):
	values = []
	values_raw = []
	values_age = []
	values_sex = []
	for j, row in enumerate(raw_data):
		coeff = 1 if sex[j] == 1 else -1
		values_raw.append(float(row[i]))
		values_age.append(float(row[i]) * age[j])
		values_sex.append(float(row[i]) * coeff)
		# values.append(float(row[i])*age[j]*coeff)
	
	normalized_regular = stats.zscore(values_raw)
	normalized_age = stats.zscore(values_age)
	normalized_sex = stats.zscore(values_sex)
	# normalized_values = stats.zscore(values)

	for j in range(0, len(data)):
		foo = data[j]
		foo.append(str(normalized_regular[j]))
		foo.append(str(normalized_age[j]))
		foo.append(str(normalized_sex[j]))
		data[j] = foo
	'''
	for j in range(0, len(data)):
		coeff = 1 if sex[j] == 1 else -1
		participant = data[j]
		participant.append(values[j]*age[j]*coeff)
		data[j] = participant
	'''

'''
#linear regression
	model = LinearRegression()
	model.fit(np.array(sex_age), np.array(values).reshape(-1, 1))
	predict = model.predict(np.array(sex_age))

	for j in range(0, len(data)):
		participant = data[j]
		val = values[j]
		participant.append((val - predict[j][0]) ** 2)
		data[j] = participant
		if i == 6 and print_count != 0:
			print("val: ", val)
			print("predict: ", predict[j])
			print(data[j][i-5])
			print_count -= 1
	if i == 6:
		plt.scatter(age, values,  color='black')
		plt.plot(values, predict, color='blue', linewidth=3)

		plt.xticks(())
		plt.yticks(())

		plt.show()	
	print("finished biomarker ", i)
print("done")
'''

for i in range(0, len(raw_data)):
	if (raw_data[i][1] == "1") or (raw_data[i][2] == "1"):
		foo = data[i]
		foo.append("1")
		data[i] = foo
	else:
		foo = data[i]
		foo.append("0")
		data[i] = foo

o = open(OUT_FILE, "w+")

for row in data:
	for val in row:
		o.write(str(val))
		o.write("\t")

	o.write("\n")

f.close()
o.close()
