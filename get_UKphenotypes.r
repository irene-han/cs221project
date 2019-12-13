# Input:
# 1. base_UKBphenotype=NULL: Phenotype file UK Biobank
# 2. outputfile: name outputfile
# 3. codefile: file containing names of phenotypes and UKB ID
#	e.g		Sex	31
#			Age	21022

# Script returns:
# 1. A file with the phenotypes asked for.
# 2. A housekeeping file containing:
# 	Column 1 = Phenotype name
# 	Column 2 = UKB Data-Field ID
# 	Column 3 = UKB Data-Field ID as in official file (also takes waves into account)
# 	Column 4 = Column number in file for extraction

getPhenotypesUKB = function(base_UKBphenotype=NULL, outputfile=NULL, codefile=NULL)
{
	# give a file with 2 columns: column 1 = Phenotype name (for user; not needed for this to work) and column 2 = UKB Data-Field ID (e.g.6145)
	codes = read.table(codefile,sep="\t")
	# Remove duplicate codes
	codes = codes[!duplicated(codes[,2]),]

	# get column names UKB datafile
	cols = read.table(base_UKBphenotype, header=T, nrows=1, sep="\t")

	# create UKB phenotype file ID coding from UKB Data-Field ID e.g.6145--> f.6145.
	x = paste("f.", codes[,2], ".",sep="")

	# Create empty vectors
	colnr = c()
	colname = c()
	codeshort = c()

	# Loop through UKB Data-Field IDs to extract
	for(i in 1:nrow(codes))
	{
		# Match names if not there report
		if(length(grep(x[i], colnames(cols),fixed=T)) == 0)
		{
			cat(as.character(codes[i,1]), "UK Biobank ID", as.character(codes[i,2]), "not present", "\n")
		}
		
		# Get column number in file for extract
		colnr = c(colnr, grep(x[i], colnames(cols),fixed=T))
		# Get column name UKB file
		colname = c(colname, colnames(cols)[grep(x[i], colnames(cols),fixed=T)])
		# Get UKB ID codes
		codeshort = c(codeshort, rep(codes[i,2], length(grep(x[i], colnames(cols),fixed=T))))
	}
	# Combine together
	t1 = cbind(colname,codeshort, colnr)

	# Creation housekeeping file
	fin = merge(codes, t1, by.x="V2", by.y="codeshort")
	# Change order
	fin = fin[,c(2,1,3,4)]
	# Give column names
	colnames(fin) = c("Phenotype", "UKB ID", "UKB ID full", "Location in dataset")
	# Write housekeeping file
	write.table(fin, paste(outputfile, ".housekeeping", sep=""), col.names=T, row.names=F, quote=T)

	# Create bash code to extract phenotypes outside of R
	line_of_code = paste(paste("cut -d$'\t' -f",paste(c(1,as.character(fin[,4])), collapse=","),sep=""), base_UKBphenotype, ">", outputfile)  
	
	# Pipe column numbers to Bash to quickly extract the data using 'cut'
	system(command=line_of_code)
}

# running function
getPhenotypesUKB(
base_UKBphenotype="/home/groups/laramied/data/UKBiobank/ORIGINALS/UKB_prep/Phenotype_data/ukb52498_phenotypes",
outputfile= "~/CS221/data_biomarkers_double_plus",
codefile="~/CS221/variables"
)


