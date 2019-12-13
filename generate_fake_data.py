import random

#OUT_FILE = "fake_data_biomarkers_normalized"
OUT_FILE = "fake_data_biomarkers_normalized_by_age_v2"

participants = []
for i in range(10):
	p = ""
	#for i in range(34):
	for i in range(34*3):
		num = random.uniform(-3, 3)
		p += str(num) + " "
	p += str(random.choice([0, 1]))
	participants.append(p)

o = open(OUT_FILE, "w+")
for p in participants:
	o.write(p)
	o.write("\n")

o.close()
