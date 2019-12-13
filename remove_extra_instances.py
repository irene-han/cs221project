"""After the initial BioBank assessment, two later assessments were 
performed. However, this data is not that helpful to us, as 
the two later assessments were completed by a fraction of the original cohort.

This script takes in a BioBank file, and removes the extra  instances.
"""

# BELOW: constants that often need to be altered
IN_FILE = "/home/users/benson97/CS221/data_biomarkers_double_plus"
OUT_FILE = "/home/users/benson97/CS221/data_biomarkers_double_plus_one"

def get_instance(string):
    """Finds the instance number in a column header.

    Args:
        string: Should be in the form f.#.#.#
    """
    row = string.split(".")

    # handles "f.eid" case
    if len(row) < 4:
        return "0"

    # the number is somewhat arbitrary... 
    # it is determined by Joeri's UK Phenotypes script.
    # (which is "get_UKphenotypes.r" --- thanks Joeri!)
    return row[2]

infile = open(IN_FILE)
outfile = open(OUT_FILE, "w+")

header = infile.readline().split()
outfile_header = ""
to_add = set()

index = 0
for column in header:
    if get_instance(column) == "0":
        outfile_header = outfile_header + column + "\t"
        to_add.add(index)

    index += 1

# remove extra \t, add \n
outfile_header = outfile_header[:-1]
outfile_header = outfile_header + "\n"

outfile.write(outfile_header)

current = infile.readline().strip()
future = infile.readline().strip()

while True:
    row = current.split()
    outfile_row = []

    index = 0 
    for column in row:
        if index in to_add:
            outfile_row.append(column)

        index += 1

    outfile_line = ""
    for column in outfile_row:
        outfile_line = outfile_line + column + "\t"
    outfile_line = outfile_line[:-1]

    if future != "":
        outfile_line = outfile_line + "\n"

    outfile.write(outfile_line)

    current = future
    if current == "":
        break
    future = infile.readline().strip()

infile.close()
outfile.close()
