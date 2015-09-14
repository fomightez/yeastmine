#!/usr/bin/env python

#****CAVEAT: For those few with introns in their genes, the plots in gbrowse
# won't be in sync with the the gene entirely. They will instead be contiguous
# with the start of the protein gene. This choice was made for simplicity to
# eliminate the need to work out code calculating positioning relative to intron
# sequences.   ****

#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#



name_of_outputfile_prefix = "residue_density_gbrowse_custom_track"

number_of_genes_per_custom_track_file = 4000


Window_Size = 30
step_to_move_window = 10





fragment_size_cutoff = 6 # see note below about why 6 at branch where 'fragment_size_cutoff' used to decide if fragment worth analysis

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************




amino_acids_to_examine_full_names = ["lysine", "glutamine","glutamic_acid", "comboKQE"] # options are: 'lysine', 'glutamine', and 'glutamic_acid' for single. Or 'comboKQE'

amino_acid_name_to_letter_dict = {
    "lysine": "K",
    "glutamine": "Q",
    "glutamic_acid":"E",
    "comboKQE": "J"
}
# from http://virology.wisc.edu/acp/Classes/DropFolders/Drop660_lectures/SingleLetterCode.html
# references to IUPAC and IUBMB and
# says no amino acids or ambiguity indicators assigned to single letters
# 'J', 'O', or 'U' and so I should be safe replacing all 'K', 'Q', and 'E's
# with one of those and counting those to assess clustering





###---------------------------HELPER FUNCTIONS---------------------------------###

def normalize_fragment_count_list(fragment_number_list):
    '''
    takes a list of fragments numbered one through to the last, and returns a new
    list where fragments numbered by percent contribution of total adding to 1
    '''
    total_fragments =  float(len(fragment_number_list))
    new_list = []
    for fragment_number in fragment_number_list:
        new_list.append (fragment_number/total_fragments)
    return new_list


# def total_number_fragment_calc(protein_len, step, fragment_size_cutoff):
#     '''
#     takes a the length of a protein sequence and the step of the sliding window
#     and the cutoff for considering fragments and returns the number
#     of fragments
#
#     see http://stackoverflow.com/questions/5584586/find-the-division-remainder-of-a-number
#     (tzot's answer) for divmod() description
#     '''
#     total_fragments, remainder = divmod(protein_len,step)
#     if remainder > fragment_size_cutoff:
#         total_fragments += 1
#     return total_fragments


def density_calc (sequence_string, residue):
    '''
    takes a string representation of a protein sequence and returns the density
    of a residue
    '''
    residue_density = float(sequence_string.count(residue)) / len(sequence_string)
    return residue_density



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

def chunker(seq, size):
    '''
    function takes a sequence and breaks it up based on the size input

    see nosklo's answer at http://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    '''
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))



def generate_configuration_header_text_string ():
    '''
    builds and returns a text string with the settings for the track I had
    worked out testing in gbrowse.

    Generates output in the FFF format as described at
    http://browse.yeastgenome.org/gbrowse2/annotation_help.html
    '''
    text_string = "[level]\n"
    text_string += "glyph = xyplot\n"
    text_string += "graph_type=boxes\n"
    text_string += "fgcolor = mediumorchid\n"
    text_string += "bgcolor = cornflowerblue\n"
    text_string += "height=100  #use as percent because 1 as height and max score looked poor\n"
    text_string += "min_score=0\n"
    text_string += "max_score=100\n"
    text_string += "label=1\n"
    text_string += "key=Density\n"
    return text_string





def generate_custom_tracks_file (output_file_name_prefix, plotting_data):
    '''
    Generates a file containing output in the FFF format as described at
    http://browse.yeastgenome.org/gbrowse2/annotation_help.html

    GUIDE TO PLOTTING_DATA LIST ELEMENTS:
    plotting_data.append([amino_acid_full_name, current_fragment_chr_location_start,  current_fragment_chr_location_end, density_score * 100])
    '''

    # detail what text gets used in place of amino acids for
    # Column 2 (the feature name) of the custom track
    amino_acid_text_for_track_label_dict = {
        "lysine": "Lys",
        "glutamine": "Gln",
        "glutamic_acid":"Glu",
        "comboKQE": "combo"
    }


    # turns out everything in one file is too much to upload to SGD, even if
    # gzip file.
    # so perhaps break up into several files and upload them?
    # I devised a general method that allows me to break up into any amount of
    # subsets needed, but it seemed splitting in roughly half was sufficient after I
    # tested several smaller subsets that succeeded.
    # Roughly half because I did 4000 in first set since last set of genes seems
    # to have more data.
    # This approach allowed me to upload the two files to the yeast genome gbrowse
    # site with each protein having a plot for the three residues and one for
    # the combo. But you had to scroll to find which of the two tracks the data
    # was in. After realizing this, it would just make more sense to have
    # density for each residue, or combination, as a separate track. It will
    # be easier to follow for each gene this way. So next version of the program worked that way.
    plot_subset_number = 1
    genes_in_subset = 0
    for data_line in plotting_data:


        if data_line[0].startswith("reference"):
            #reset for next set if already enough genes
            if genes_in_subset >= number_of_genes_per_custom_track_file:
                genes_in_subset = 0
                plot_subset_number +=1
                # close current output file stream to ready for new one
                output_file.close()
            if genes_in_subset == 0:
                #  initialize output file stream with a different file name
                output_file = open(output_file_name_prefix + str(plot_subset_number) + ".txt", "w")

                #write configuration header for track
                data_text = generate_configuration_header_text_string ()
                output_file.write(data_text)
            data_text = "\n" + data_line[0] +"\n"
            # write that line to the output text because it has reference chromosome
            # for next protein coding sequence
            genes_in_subset += 1

            #write data row
            output_file.write(data_text)
        else:
            # construct line to write for gene
            data_text = ("level\t" +
                amino_acid_text_for_track_label_dict[data_line[0]]+ "\t" +
                str(data_line[1]) + ".." + str(data_line[2]) +
                "\tscore="+ str(data_line[-1]) + "\n"
                )
            #write data row
            output_file.write(data_text)
    return plot_subset_number










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
# NOTE THAT 4 of the 5917 protein/genes disappear when you add "genes.chromosome.primaryIdentifier" to view to leave 5913
# Explanation is that four genes off 2-micron get dropped!!!
# THOSE DROPPED SECONDARY IDENTIFIERS (LIKE YDR190C format)---> set(['R0020C', 'R0030W', 'R0010W', 'R0040C'])
query.add_view(
    "genes.primaryIdentifier", "genes.secondaryIdentifier", "symbol", "length",
    "molecularWeight", "pI", "genes.featureType", "genes.sgdAlias",
    "genes.description", "sequence.residues","genes.chromosome.primaryIdentifier",
    "genes.chromosomeLocation.start", "genes.chromosomeLocation.end",
    "genes.chromosomeLocation.strand"
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
plotting_data = []
for row in query.rows():
    total_gene_count += 1
    ##if total_gene_count > 10:
    ##    break  # for debugging just want to to first 10. When breaks, number reported in stderror will be one more than actually analyzed because just added one on line above.
    current_protein_gene = row["genes.secondaryIdentifier"]
    current_sequence = row["sequence.residues"]
    protein_length = len(current_sequence)
    current_chr = row["genes.chromosome.primaryIdentifier"]
    strand_indicator = int(row["genes.chromosomeLocation.strand"]) # .strand is "1" for Watson and "-1" for Crick and more useful for calculations later if it was an integer
    if strand_indicator == 1:
        gene_start = row["genes.chromosomeLocation.start"]
    else:
        # on crick strand so start is highest value in .start/.end data
        gene_start = row["genes.chromosomeLocation.end"]
    plotting_data.append(["reference="+current_chr]) #append it as a list so can simply use first elment to sort if reference or other data
    for amino_acid_full_name in amino_acids_to_examine_full_names:
        #reset the combo boolean so can test and make true if needed
        analyze_triple_amino_acid_clustering_combo = False
        amino_acid_to_examine = amino_acid_name_to_letter_dict[amino_acid_full_name]
        if amino_acid_full_name == "comboKQE":
            analyze_triple_amino_acid_clustering_combo = True
        fragment_count = 0
        # For breaking up into chunks as a leapfrogging window, I used msw's answer on
        # http://stackoverflow.com/questions/11636079/split-very-long-character-string-into-smaller-character-blocks-with-character-ov
        # Split very long character string into smaller character blocks with character overlap
        for i in range(0, len(current_sequence), step_to_move_window):
            fragment_count += 1
            sequence_window = current_sequence[i:i+Window_Size]
            # Karlin et al 2002 cites their earlier work that says, "a 'typical' protein of 400 residues and average composition, a run of an individual amino acid is statistically significant (at the 0.1% significance level) if it is five or more residues long." So I picked one above that to be fuzzy to consider short sequences towards end of proteins. Also this allows consideration of some of sequences where the break of 10 perhaps falls arbitraily less than optimally given the step of 10 amino acids (vs one or some other low number) I used to limit computation and redundancy.
            if len(sequence_window) > fragment_size_cutoff:
                if analyze_triple_amino_acid_clustering_combo:
                    unsubstituted_seq_window = sequence_window
                    sequence_window = replace_KQE_with_dummy_amino_acid(sequence_window)
                density_score = density_calc (sequence_window, amino_acid_to_examine)
                if analyze_triple_amino_acid_clustering_combo:
                    table_data.append([row["symbol"], current_protein_gene, row["pI"], density_score, unsubstituted_seq_window])
                else:
                    table_data.append([row["symbol"], current_protein_gene, row["pI"], density_score, sequence_window])

                # now update data that will get used for plotting
                current_fragment_chr_location_start = gene_start + (((step_to_move_window * 3) * (fragment_count - 1) * strand_indicator ) )
                current_fragment_chr_location_end = gene_start + (((step_to_move_window * 3) * (fragment_count) * strand_indicator ) )
                if strand_indicator == 1:
                    assert (current_fragment_chr_location_start + (step_to_move_window * 3)) == current_fragment_chr_location_end, "Error: the distance between the fragment start and end site doesn't match the window step"
                else:
                    assert (current_fragment_chr_location_start - (step_to_move_window * 3)) == current_fragment_chr_location_end, "Error: the distance between fragment start and end site doen't match the window step"
                plotting_data.append([amino_acid_full_name, current_fragment_chr_location_start,  current_fragment_chr_location_end, density_score * 100.00]) # `* 100` to convert decimal to percent since 0-100 range looks better in gbrowse than 0 - 1



# generate a file that is custom tracks for gbrowse in FFF format (see http://browse.yeastgenome.org/gbrowse2/annotation_help.html)
subset_records = generate_custom_tracks_file (name_of_outputfile_prefix, plotting_data)
# FOR DEBUGGING print plotting_data



#give user some stats and feeback
import sys
sys.stderr.write("Concluded. \n")


sys.stderr.write(str(total_gene_count) + " protein sequences analyzed. \n")
sys.stderr.write("The "+ str(subset_records) + " file(s) with the gbrowse custom track (FFF format) saved as \n'"
    + name_of_outputfile_prefix +"1.txt', ..2.txt, etc. in same directory as the script.\n")

