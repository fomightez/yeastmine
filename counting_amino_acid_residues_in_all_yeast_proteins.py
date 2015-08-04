#!/usr/bin/env python

#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

name_of_outputfile = "amino_acid_counts_for_all_yeast_proteins.tsv"
#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************




###---------------------------HELPER FUNCTIONS---------------------------------###

###--------------------------END OF HELPER FUNCTIONS---------------------------###





###-----------------Actual Main function of script---------------------------###

from collections import defaultdict
amino_acid_frequencies_dict = defaultdict(int) # see http://ludovf.net/blog/python-collections-defaultdict/
total_amino_acid_count = 0
total_gene_count = 0

##################################################################
#############START OF CODE FROM YEASTMINE########################

#!/usr/bin/env python

# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Protein")

# The view specifies the output columns
query.add_view(
    "genes.primaryIdentifier", "genes.secondaryIdentifier", "symbol", "length",
    "molecularWeight", "pI", "genes.featureType", "genes.sgdAlias",
    "genes.description", "sequence.residues"
)

# You can edit the constraint values below
query.add_constraint("genes.featureType", "=", "intein_encoding_region", code = "H")
query.add_constraint("genes.featureType", "=", "blocked_reading_frame", code = "E")
query.add_constraint("genes.qualifier", "!=", "Dubious", code = "B")
query.add_constraint("genes.qualifier", "IS NULL", code = "C")
query.add_constraint("genes.status", "=", "Active", code = "D")
query.add_constraint("genes.featureType", "=", "ORF", code = "F")
query.add_constraint("genes.featureType", "=", "transposable_element_gene", code = "G")
query.add_constraint("organism.name", "=", "Saccharomyces cerevisiae", code = "A")



# Your custom constraint logic is specified with the code below:
query.set_logic("A and (B or C) and D and (F or G or E or H)")


#############END OF CODE FROM YEASTMINE########################
##################################################################



table_data = []
for row in query.rows():
    total_gene_count += 1
    count_of_stars = 0
    for residue in row["sequence.residues"]:
        amino_acid_frequencies_dict[residue] += 1

        total_amino_acid_count += 1
        if residue == "*":
            count_of_stars +=1
    # I noticed number of stop codons was off from number of ORFs. This code
    # with the two lines above showed it's due to blocked_reading_frames in SGD.
    if count_of_stars > 1:
        print row["genes.secondaryIdentifier"] + " contains " + str(
            count_of_stars) +  " stop codons. Sequence of protein at SGD:"
        print row["sequence.residues"]
    # is it worth leaving out the blocked_reading_frames?

# Convert dictionary with counts to a list at the same time adding the percent.
# This conversion will allow sorting the data.
data_list = []
for residue in amino_acid_frequencies_dict:
    # append a list of residue, frequency, and total percent
    data_list.append([residue, amino_acid_frequencies_dict[residue], (
        (amino_acid_frequencies_dict[residue]/float(total_amino_acid_count))*100
        )])

# sort the data - want highest to lowest frequency
from operator import itemgetter
sorted_data_list = sorted(data_list, key=itemgetter(1), reverse=True)

# report residue, total count, and percent of total SORTED
#  initialize output file stream
output_file_handler = open(name_of_outputfile, "w")
# generate column/header labels for output
labels_text = ("\t\tamino acid\tcount\tpercent")
output_file_handler.write(labels_text + '\n')
# generate data rows output
for data in sorted_data_list:
    # Fill data_text with residue, frequency, and total percent from the list
    # seprated by tabs to produce tab separated values.
    data_text = ("\t\t" + data[0] + "\t" +
        str(data[1]) + "\t" + str(data[2]) )
    output_file_handler.write(data_text + '\n')

gene_total_text = ("\n\t\tProteins encoded by " + str(total_gene_count)
    + " genes examined.")
output_file_handler.write(gene_total_text + '\n')

# close output file stream
output_file_handler.close()




#give user some stats and feeback
import sys
sys.stderr.write("Concluded. \n")
sys.stderr.write("The counts and percents of the amino acids has been saved as \n'"
    + name_of_outputfile +"' in same directory as the script.\n")
