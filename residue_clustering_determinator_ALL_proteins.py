#!/usr/bin/env python

#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

amino_acid_to_examine_full_name = "comboKQE" # options are: 'lysine', 'glutamine', and 'glutamic_acid' for single. Or 'comboKQE'

protein_collection_name = "ALL_PROTEINS"




Window_Size = 50
step_to_move_window = 10



name_of_outputfileA = ("rankings_of_" + amino_acid_to_examine_full_name + "_raw_density_for_"+ protein_collection_name + str(Window_Size) + "_" + str(step_to_move_window )+ ".tsv")
name_of_outputfileB = ("rankings_of_" + amino_acid_to_examine_full_name + "_clustering_for_"+ protein_collection_name + "_" + str(Window_Size) + "_" + str(step_to_move_window )+ ".tsv")
name_of_outputfileC = ("rankings_of_" + amino_acid_to_examine_full_name + "_len_normalized_density_for_"+ protein_collection_name + "_" + str(Window_Size) + "_" + str(step_to_move_window )+ ".tsv")
name_of_outputfileD = ("rankings_of_" + amino_acid_to_examine_full_name + "_len_normalized_clustering_for_"+ protein_collection_name + "_" + str(Window_Size) + "_" + str(step_to_move_window )+ ".tsv")
name_of_outputfileE = ("highest_clusters_of_" + amino_acid_to_examine_full_name + "_per_gene_for_"+ protein_collection_name + "_" + str(Window_Size) + "_" + str(step_to_move_window )+ ".tsv")


adjancency_bonus_factor = 0.016999   #0.005799 from when developing but then worked out higher value while examining nuMRP proteins

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************








# options are: 'lysine', 'glutamine', and 'glutamic_acid' for single. Or 'comboKQE'
analyze_triple_amino_acid_clustering_combo = False
if amino_acid_to_examine_full_name == "lysine":
    amino_acid_to_examine = "K"
elif amino_acid_to_examine_full_name == "glutamine":
	amino_acid_to_examine = "Q"
elif amino_acid_to_examine_full_name == "glutamic_acid":
	amino_acid_to_examine = "E"
elif amino_acid_to_examine_full_name == "comboKQE":
    amino_acid_to_examine = "J"
    # from http://virology.wisc.edu/acp/Classes/DropFolders/Drop660_lectures/SingleLetterCode.html
    # references to IUPAC and IUBMB and
    # says no amino acids or ambiguity indicators assigned to single letters
    # 'J', 'O', or 'U' and so I should be safe replacing all 'K', 'Q', and 'E's
    # with one of those and counting those to assess clustering
    analyze_triple_amino_acid_clustering_combo = True

###---------------------------HELPER FUNCTIONS---------------------------------###


def density_calc (sequence_string, residue):
    '''
    takes a string representation of a protein sequence and returns the density
    of a residue
    '''
    residue_density = float(sequence_string.count(residue)) / len(sequence_string)
    return residue_density

def adjancency_bonus_calc (sequence_string, residue):
    '''
    takes a string representation of a protein sequence and test if it contains
    occurences of the residue of interest adjacent to the same residuec and then
    returns the bonus score to assign to that string based on the number of
    occurences.
    '''
    adjancency_bonus = 0.0
    for idx,amino_acid in enumerate(sequence_string):
        # Make sure there is a previous residue then only see about adding bonus
        # if current amino_acid is same as residue of interest.
        if idx > 0 and (amino_acid == residue) :
            if sequence_string[idx-1] ==  residue:
                 adjancency_bonus += adjancency_bonus_factor
            #plus if there is a residue before the previous one, add a
            # add a bonus if that is also residue of interest to compound
            # detection of chains of residue_density
            if idx > 1 and sequence_string[idx-2] ==  residue:
                 adjancency_bonus += adjancency_bonus_factor
            if idx > 2 and sequence_string[idx-3] ==  residue:
                adjancency_bonus += adjancency_bonus_factor
            if idx > 3 and sequence_string[idx-4] ==  residue:
                adjancency_bonus += adjancency_bonus_factor
            if idx > 5 and sequence_string[idx-6] ==  residue:
                adjancency_bonus += adjancency_bonus_factor
            if idx > 6 and sequence_string[idx-7] ==  residue:
                adjancency_bonus += adjancency_bonus_factor
            if idx > 7 and sequence_string[idx-8] ==  residue:
                adjancency_bonus += adjancency_bonus_factor/2
    return adjancency_bonus



def replace_KQE_with_dummy_amino_acid(text):
    '''
    Function takes text and replaces all occurences of 'K', 'Q', or 'E' with
    'J'.

    The choice of 'J' comes from fact
    http://virology.wisc.edu/acp/Classes/DropFolders/Drop660_lectures/SingleLetterCode.html
    which references to IUPAC and IUBMB says no amino acids or ambiguity
    indicators assigned to single letters 'J', 'O', or 'U' and so I should be
    safe replacing all 'K', 'Q', and 'E's
    with one of those and counting those to assess clustering

    The main portion of the function, i.e., replacing multiple characters,
    was developed using information on page
    http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
    where they report the timing of various approaches with this (ba) as one of
    fastest and most readable in Hugo's answer
    '''
    chars = "KQE"
    for char in chars:
        if char in text:
            text = text.replace(char, "J")
    return text




def generate_density_reportA (table_data):
    '''
    This function sorts the list of data contents based on density score
    and outputs a tsv table with the results with labeled headers.

    The generated outout file should be able to be opened in
    Google Spreadsheets or Excel.

    '''

    #  initialize output file stream
    output_file = open(name_of_outputfileA, "w")

    # generate the sorted lists to be used

    sorted_on_density = sorted(
        table_data, key=lambda table_data: table_data[3], reverse=True)

    # generate the output

    # for excel I find I can control the number of empty cells on left with tab,
    # but once the text starts, you'll need an extra one for putting in exmpty
    # cells because after text it just signals go to next cell

    data_text = "\t\tsorted on density\n"

    #write data row
    output_file.write(data_text + '\n')

    data_text = "ID\tsys\tpI\tdensity\tsequence of fragment analyzed"
    output_file.write(data_text + '\n')


	#write other rows of data
    for data_row in sorted_on_density:
        # CODE BEING USED TO POPULATE TABLE ROWS:
        # table_data.append([row["symbol"], current_protein_gene, row["proteins.pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])
        # Added check for `None` because I was seeing error error `TypeError:
        # unsupported operand type(s) for +: 'NoneType' and 'str'` and when I
        # set to skip those, only ended up with 1141 and not 1208 expexted
        if data_row[0] == None:
            # originally was just using the alternate, which I had as
            # the gene systematic name, when no gene)symbol present
            # but some gene_symbols/name aliases overlap and cause
            # problems if you try to go back into yeastmine, so I added
            # systematic name to all lines.
            data_text = "None\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[3]) + "\t" + str(data_row[7])
        else:
            # use the standard name, which was stored at index zero
            data_text = data_row[0] + "\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[3]) + "\t" + str(data_row[7])
        #write data row
        output_file.write(data_text + '\n')

    # close output file stream
    output_file.close()


def generate_density_with_adjancency_bonus_reportB (table_data):
    '''
    This function sorts the list of data contents based on density score + bonus
    for being adjacent another occurence of the residue of interest and outputs
    a tsv table with the results with labeled headers.

    The generated outout file should be able to be opened in
    Google Spreadsheets or Excel.

    '''

    #  initialize output file stream
    output_file = open(name_of_outputfileB, "w")

    # generate the sorted lists to be used

    sorted_on_density_with_adjancency_bonus = sorted(
        table_data, key=lambda table_data: table_data[4], reverse=True)

    # generate the output

    # for excel I find I can control the number of empty cells on left with tab,
    # but once the text starts, you'll need an extra one for putting in exmpty
    # cells because after text it just signals go to next cell

    data_text = "\t\tsorted on density + adjancency bonus\n"

    #write data row
    output_file.write(data_text + '\n')

    data_text = "ID\tsys\tpI\tdensity+adjancency bonus\tsequence of fragment analyzed"
    output_file.write(data_text + '\n')


	#write other rows of data
    for data_row in sorted_on_density_with_adjancency_bonus:
        # CODE BEING USED TO POPULATE TABLE ROWS:
        # table_data.append([row["symbol"], current_protein_gene, row["proteins.pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])
        # Added check for `None` because I was seeing error error `TypeError:
        # unsupported operand type(s) for +: 'NoneType' and 'str'` and when I
        # set to skip those, only ended up with 1141 and not 1208 expexted
        if data_row[0] == None:
            # originally was just using the alternate, which I had as
            # the gene systematic name, when no gene)symbol present
            # but some gene_symbols/name aliases overlap and cause
            # problems if you try to go back into yeastmine, so I added
            # systematic name to all lines.
            data_text = "None\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[4]) + "\t" + str(data_row[7])
        else:
            # use the standard name, which was stored at index zero
            data_text = data_row[0] + "\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[4]) + "\t" + str(data_row[7])
        #write data row
        output_file.write(data_text + '\n')

    # close output file stream
    output_file.close()


def generate_len_normalized_density_reportC (table_data):
    '''
    This function sorts the list of data contents based on length-normalized
    density and outputs a tsv table with the results with labeled headers.

    The generated outout file should be able to be opened in
    Google Spreadsheets or Excel.

    '''

    #  initialize output file stream
    output_file = open(name_of_outputfileC, "w")

    # generate the sorted lists to be used

    sorted_on_len_normalized_density = sorted(
        table_data, key=lambda table_data: table_data[5], reverse=True)

    # generate the output

    # for excel I find I can control the number of empty cells on left with tab,
    # but once the text starts, you'll need an extra one for putting in exmpty
    # cells because after text it just signals go to next cell

    data_text = "\t\tsorted on length-normalized density\n"

    #write data row
    output_file.write(data_text + '\n')

    data_text = "ID\tsys\tpI\tlength-normalized density\tsequence of fragment analyzed"
    output_file.write(data_text + '\n')


	#write other rows of data
    for data_row in sorted_on_len_normalized_density:
        # CODE BEING USED TO POPULATE TABLE ROWS:
        # table_data.append([row["symbol"], current_protein_gene, row["proteins.pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])
        # Added check for `None` because I was seeing error error `TypeError:
        # unsupported operand type(s) for +: 'NoneType' and 'str'` and when I
        # set to skip those, only ended up with 1141 and not 1208 expexted
        if data_row[0] == None:
            # originally was just using the alternate, which I had as
            # the gene systematic name, when no gene)symbol present
            # but some gene_symbols/name aliases overlap and cause
            # problems if you try to go back into yeastmine, so I added
            # systematic name to all lines.
            data_text = "None\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[5]) + "\t" + str(data_row[7])
        else:
            # use the standard name, which was stored at index zero
            data_text = data_row[0] + "\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[5]) + "\t" + str(data_row[7])
        #write data row
        output_file.write(data_text + '\n')

    # close output file stream
    output_file.close()




def generate_len_normalized_density_with_adjacency_bonus_reportD (table_data):
    '''
    This function sorts the list of data contents based on length-normalized
    density + bonus for being adjacent another occurence of the residue of
    interest and outputs a tsv table with the results with labeled headers.

    The generated outout file should be able to be opened in
    Google Spreadsheets or Excel.

    '''

    #  initialize output file stream
    output_file = open(name_of_outputfileD, "w")

    # generate the sorted lists to be used

    sorted_on_len_normalized_density_with_adjancency_bonus = sorted(
        table_data, key=lambda table_data: table_data[6], reverse=True)

    # generate the output

    # for excel I find I can control the number of empty cells on left with tab,
    # but once the text starts, you'll need an extra one for putting in exmpty
    # cells because after text it just signals go to next cell

    data_text = "\t\tsorted on length-normalized density + adjancency bonus\n"

    #write data row
    output_file.write(data_text + '\n')

    data_text = "ID\tsys\tpI\tlength-normalized density + adjancency bonus\tsequence of fragment analyzed"
    output_file.write(data_text + '\n')


	#write other rows of data
    for data_row in sorted_on_len_normalized_density_with_adjancency_bonus :
        # CODE BEING USED TO POPULATE TABLE ROWS:
        # table_data.append([row["symbol"], current_protein_gene, row["proteins.pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])
        # Added check for `None` because I was seeing error error `TypeError:
        # unsupported operand type(s) for +: 'NoneType' and 'str'` and when I
        # set to skip those, only ended up with 1141 and not 1208 expexted
        if data_row[0] == None:
            # originally was just using the alternate, which I had as
            # the gene systematic name, when no gene)symbol present
            # but some gene_symbols/name aliases overlap and cause
            # problems if you try to go back into yeastmine, so I added
            # systematic name to all lines.
            data_text = "None\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[6]) + "\t" + str(data_row[7])
        else:
            # use the standard name, which was stored at index zero
            data_text = data_row[0] + "\t" + data_row[1] + "\t" + str(data_row[2]) + "\t" + str(data_row[6]) + "\t" + str(data_row[7])
        #write data row
        output_file.write(data_text + '\n')

    # close output file stream
    output_file.close()






def generate_richest_chunks_per_gene_reportE (table_data):
    '''
    This function collects the best scoring fragment for each gene using the
    combined length-normalized density scores and adjancency bonus score
    and outputs a tsv table with the results with labeled headers.

    The generated outout file should be able to be opened in
    Google Spreadsheets or Excel.

    '''

    from collections import defaultdict
    richest_fragment_dict = defaultdict(list) # see http://ludovf.net/blog/python-collections-defaultdict/

    #  initialize output file stream
    output_file = open(name_of_outputfileE, "w")


    # generate the dictionary to be used
    # this will be a dictionary of the data lines for the highest score for
    # each gene. They keys will be the protein_gene_name.
    for i in table_data:
        #check if anything listed already and if so whether lower or better score.
        # if nothing is listed copy it in.
        if len(richest_fragment_dict[i[1]]):
            if (i[6] > richest_fragment_dict[i[1]][6]):
                richest_fragment_dict[i[1]] = i
        else:
            richest_fragment_dict[i[1]] = i


    # Convert dictionary with scores and information to a list to allow sorting the data.
    # (see Akseli Palen's answer at http://stackoverflow.com/questions/1679384/converting-python-dictionary-to-list )
    data_list = richest_fragment_dict.values()

    # sort the data - want highest to lowest combined length-normalized density
    # scores and adjancency bonus score
    from operator import itemgetter
    sorted_data_list = sorted(data_list, key=itemgetter(6), reverse=True)





    # generate the output

    # for excel I find I can control the number of empty cells on left with tab,
    # but once the text starts, you'll need an extra one for putting in empty
    # cells because after text it just signals go to next cell

    data_text = "\t\tbest combined length-normalized density + adjancency bonus score for each gene\n"

    #write data row
    output_file.write(data_text + '\n')

    data_text = "ID\tsys\tpI\tlength-normalized density + adjancency bonus\tsequence of fragment analyzed"
    output_file.write(data_text + '\n')


	#write other rows of data
    for gene in sorted_data_list:
        # CODE BEING USED TO POPULATE TABLE ROWS:
        # table_data.append([row["symbol"], current_protein_gene, row["proteins.pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])
        # Added check for `None` because I was seeing error error `TypeError:
        # unsupported operand type(s) for +: 'NoneType' and 'str'` and when I
        # set to skip those, only ended up with 1141 and not 1208 expexted
        if gene[0] == None:
            # originally was just using the alternate, which I had as
            # the gene systematic name, when no gene)symbol present
            # but some gene_symbols/name aliases overlap and cause
            # problems if you try to go back into yeastmine, so I added
            # systematic name to all lines.
            data_text = "None\t" + gene[1] + "\t" + str(gene[2]) + "\t" + str(gene[6]) + "\t" + str(gene[7])
        else:
            # use the standard name, which was stored at index zero
            data_text = gene[0] + "\t" + gene[1] + "\t" + str(gene[2]) + "\t" + str(gene[6]) + "\t" + str(gene[7])
        #write data row
        output_file.write(data_text + '\n')

    # close output file stream
    output_file.close()






###--------------------------END OF HELPER FUNCTIONS---------------------------###








###-----------------Actual Main function of script---------------------------###




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

total_gene_count = 0
table_data = []
for row in query.rows():
    total_gene_count += 1
    current_protein_gene = row["genes.secondaryIdentifier"]
    # For breaking up into chunks as a leapfrogging window, I used msw's answer on
	# http://stackoverflow.com/questions/11636079/split-very-long-character-string-into-smaller-character-blocks-with-character-ov
	# Split very long character string into smaller character blocks with character overlap
    current_sequence = row["sequence.residues"]
    for i in range(0, len(current_sequence), step_to_move_window):
        sequence_window = current_sequence[i:i+Window_Size]
        # Karlin et al 2002 cites their earlier work that says, "a 'typical' protein of 400 residues and average composition, a run of an individual amino acid is statistically significant (at the 0.1% significance level) if it is five or more residues long." So I picked one above that to be fuzzy to consider short sequences towards end of proteins. Also this allows consideration of some of sequences where the break of 10 perhaps falls arbitraily less than optimally given the step of 10 amino acids (vs one or some other low number) I used to limit computation and redundancy.
        if len(sequence_window) > 6:
            if analyze_triple_amino_acid_clustering_combo:
                unsubstituted_seq_window = sequence_window
                sequence_window = replace_KQE_with_dummy_amino_acid(sequence_window)
	        density_score = density_calc (sequence_window, amino_acid_to_examine)
	        adjancency_bonus = adjancency_bonus_calc (sequence_window, amino_acid_to_examine)
	        density_with_adjancency_bonus = density_score + adjancency_bonus
	        length_normalized_density_score = density_score * (len(sequence_window)/float(Window_Size))
	        length_normalized_adjancency_bonus =  adjancency_bonus * (len(sequence_window)/float(Window_Size))
	        length_normalized_density_and_adjancency = length_normalized_density_score + length_normalized_adjancency_bonus
            if analyze_triple_amino_acid_clustering_combo:
                table_data.append([row["symbol"], current_protein_gene, row["pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, unsubstituted_seq_window])
            else:
                table_data.append([row["symbol"], current_protein_gene, row["pI"], density_score, density_with_adjancency_bonus, length_normalized_density_score, length_normalized_density_and_adjancency, sequence_window])



# generate reports using the data
generate_density_reportA (table_data)
generate_density_with_adjancency_bonus_reportB (table_data)
generate_len_normalized_density_reportC (table_data)
generate_len_normalized_density_with_adjacency_bonus_reportD (table_data)

generate_richest_chunks_per_gene_reportE(table_data)


#give user some stats and feeback
import sys
sys.stderr.write("Concluded. \n")
sys.stderr.write(str(total_gene_count) + " protein sequences analyzed. \n")
sys.stderr.write("The report on the amino acid density been saved as \n'"
    + name_of_outputfileA +"' in same directory as the script.\n")
sys.stderr.write("The report on the amino acid clustering has been saved as \n'")
sys.stderr.write(name_of_outputfileB + ".\n")
sys.stderr.write("The report on the length-normalized amino acid density has been saved as \n'")
sys.stderr.write(name_of_outputfileC + ".\n")
sys.stderr.write("The report on the length-normalized amino acid clustering has been saved as \n'")
sys.stderr.write(name_of_outputfileD + ".\n")
sys.stderr.write("A listing of the highest scoring clusters for each gene has been saved as \n'")
sys.stderr.write(name_of_outputfileE + ".\n")
