from scipy import stats

IN_FILE = "data_biomarkers_one" 
OUT_FILE = "data_biomarkers_normalized" 

f = open(IN_FILE) 
header = f.readline() 

raw_data = []
def no_NA(row):
	for i in range(0, len(row)):
		if row[i] == "NA":
			return False
	return True

for line in f:
	row = line.strip().split()
	# if not no_NA(row): continue
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

data = [ [] for i in range(0, len(raw_data)) ] 
for i in range(3, len(raw_data[0])):
	values = [] 
	for row in raw_data:
		values.append(float(row[i]))

	normalized_values = stats.zscore(values) 

	for j in range(0, len(data)):
		foo = data[j]
		foo.append(str(normalized_values[j]))
		data[j] = foo

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
