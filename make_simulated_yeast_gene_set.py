#!/usr/bin/env python
# make_simulated_yeast_gene_set.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# USES Python 2.7 but should be convertable via 2to3, see https://docs.python.org/3.0/library/2to3.html
#
# PURPOSE: Makes a simulated yeast gene set of user-determined size and saves
# a file of the gene list using the SGD systematic IDs each on individual lines.
#
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# none
#
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version
#

#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# make_simulated_yeast_gene_set.py 135
#-----------------------------------
# Replace `135` with the number of genes you want in your list.
#
#*******************************************************************************
#


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
#
output_file_name = "simulated_yeast_gene_list.txt"

stored_gene_data_file_prefix = "yeastmine_gene_ids_for_creating_random_set" #
# prefix for file name for data to save for subsequent use or to use from
# previous runs.

progress_bar_use = False # `False` to disable by default because relies on
# an uncommon module. Fancier progressbar if set to `True`. If you get an error
# concerning `import tqdm`, set this to `False`. Or the necessary
# module can be installed on most machines with `pip install tqdm`. On
# PythonAnywhere.com, it is `pip install --user tqdm` .

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************
























#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
import argparse
import random


###---------------------------HELPER FUNCTIONS---------------------------------###


def generate_stored_data_file_name(file_name_prefix):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function in June 2016 with
        ("yeastmine_gene_data_for_creating_random_set")
    returns
        "yeastmine_gene_data_for_creating_random_setJune2016.py"

    It also returns month and year to use in the data file text.
    '''
    # prepare to timestamp the name of file to save
    import datetime
    now = datetime.datetime.now()
    # see http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
    # for formatting options simplified
    return file_name_prefix + now.strftime("%B%Y") +".py", now.strftime(
        "%B"), now.strftime("%Y")

def generate_output_file(provided_text):
    '''
    function text and saves it as a text file
    '''
    name_of_file_to_save = output_file_name
    data_file_stream = open(name_of_file_to_save , "w")
    data_file_stream.write(provided_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    data_file_stream.close()
    sys.stderr.write(
        "\nGene set composed of {1} genes selected randomly from the {2} genes in the genome saved as '{0}'.\n".format(
        name_of_file_to_save, number_of_genes_for_list, str(
        genes_in_genome)))

def list2text(a_list):
    '''
    a function that takes a lists and makes a string where each item in list
    is on a new line
    '''
    return "\n".join(a_list)


def check_one_or_greater(value):
    ivalue = int(value)
    if ivalue < 1:
         raise argparse.ArgumentTypeError(
            "{0} is an invalid value for the number of genes to put in the simulated set; provide an integer that is one or greater.".format(value))
    return ivalue


def header_text_note_maker(month, year):
    '''
    function generates text that puts description(header) for list entries in
    gene_data_list

    month and year are provided from the calling function to make header better
    '''
    header_text = "# These were the identifiers for all the " + str(
        genes_in_genome) +" yeast genes in YeastMine "+ month + " " + year +".\n# The  YeastMine `secondaryIdentifier` (equivalent to SGD's `Systematic Name` identifier) for each gene are as follows:\n"
    return header_text

def generate_data_file(the_data_list):
    '''
    function takes gene data list from YeastMine and saves it as script-like file
    '''

    stored_gene_data_file, month, year  = generate_stored_data_file_name(
        stored_gene_data_file_prefix) # see next line for info on month & year.
    # Month and year are first used in the function just called and so instead
    # of calling that import and commands again, just passing back.


    data_file_stream = open(stored_gene_data_file , "w")
    data_file_stream.write(header_text_note_maker(month, year))
    data_file_stream.write('gene_data_list = ' + repr(gene_data_list ) + "\n")
    data_file_stream.close()
    sys.stderr.write( "\b \nGene ids for the " + str(
    genes_in_genome) +" yeast genes stored for posible future use.\n") # `\b ` in the
    # deletes the spinner, if was there; it is important that some text be
    # after the backspace because backspace and new line alone doesn't write
    # over the spinner otherwise.



###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###














#*******************************************************************************
###-----------------for parsing command line arguments-----------------------###
parser = argparse.ArgumentParser(prog='make_simulated_yeast_gene_set.py ',description="make_simulated_yeast_gene_set.py  \
    Makes a simulated yeast gene set of user-determined size and saves a file \
    of the gene list using the SGD's systematic IDs, each on individual lines.\
    **** Script by Wayne Decatur (fomightez @ github) ***")
parser.add_argument("Number", help="Number of genes to have in the produced \
    gene set.", type=check_one_or_greater)
#I would also like trigger help to display if no arguments provided because need at least one input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
number_of_genes_for_list = args.Number




###-----------------Actual Main portion of script---------------------------###

# Use previously saved list of yeast genes, or if none exists contact YeastMine
# and get a list of the genes

# To check for a file that begins with the prefix make a list of the files in
# the folder with the script and check if one of them begins with the prefix text.
# Then use that to get name if any match by taking first one because there never
# will be more than one unless debugging. Set to something that couldn't
# possibly match anything in folder otherwise so can use
# `os.path.isfile(stored_gene_data_file)` without having to first check if `stored_gene_data_file` id defined.
# Line below based on Marc L's answer at http://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
stored_gene_data_file_possible_list = [filename for filename in os.listdir('.') if (filename.startswith(stored_gene_data_file_prefix)) and (not filename.endswith('.pyc'))] # the `not filename.endswith('pyc')` is to exclude getting name of compiled version
if stored_gene_data_file_possible_list:
    stored_gene_data_file = stored_gene_data_file_possible_list[0]
else:
    stored_gene_data_file = "DOESN'T EXIST and this is an impossible name to never match a file"

if os.path.isfile(stored_gene_data_file) :
    # If data for conversion table already saved, used that to make dictionary.
    # The reason the dictionary wasn't saved is because it drops a lot of the
    # gene data information and the additional details saved in the gene data
    # list may later help in  sorting if gene is the same or different, etc..
    #
    #import the saved data list
    import importlib
    imported_data = importlib.import_module(stored_gene_data_file[:-3], package=None) # `[:-3]` part is because don't want `.py` part of file name when calling module
    # instead of using `imported_data.gene_data_list` assign variable shorter name.
    gene_data_list_text = imported_data.gene_data_list

    # Now almost ready to make the list
    # set up list
    syst_id_list = []

    # Make the list
    sys.stderr.write("Using stored genes data previously acquired from YeastMine, stored as `" + stored_gene_data_file +"`, to make a list of yeast genes.\n(Rename or delete that file if you prefer the script try to retrieve the pertinent information from YeastMine at this time.)..." )
    genes_processed = 0
    for each_gene_id in gene_data_list_text:
        syst_id_list.append(each_gene_id)
        genes_processed += 1
        # no point having progress bar because so fast with data already saved in a file so no call to YeastMine needed.
        if (genes_processed  % 1000 == 0):
                sys.stderr.write(".")

else:

    # To run your query
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
    query = service.new_query("SequenceFeature")
    query.add_view(
        "primaryIdentifier", "featureType", "secondaryIdentifier", "description",
        "sgdAlias", "symbol"
    )
    query.add_constraint("featureType", "=", "telomerase_RNA_gene", code = "Z")
    query.add_constraint("qualifier", "IS NULL", code = "W")
    query.add_constraint("qualifier", "!=", "Dubious", code = "V")
    query.add_constraint("status", "=", "Active", code = "U")
    query.add_constraint("featureType", "=", "transposable_element_gene", code = "S")
    query.add_constraint("featureType", "=", "telomeric_repeat", code = "R")
    query.add_constraint("featureType", "=", "telomere", code = "Q")
    query.add_constraint("featureType", "=", "tRNA_gene", code = "P")
    query.add_constraint("featureType", "=", "snoRNA_gene", code = "O")
    query.add_constraint("featureType", "=", "snRNA_gene", code = "N")
    query.add_constraint("featureType", "=", "LTR_retrotransposon", code = "M")
    query.add_constraint("featureType", "=", "rRNA_gene", code = "L")
    query.add_constraint("featureType", "=", "pseudogene", code = "K")
    query.add_constraint("featureType", "=", "not physically mapped", code = "J")
    #query.add_constraint("featureType", "=", "not in systematic sequence of S288C", code = "I")
    query.add_constraint("featureType", "=", "ncRNA_gene", code = "H")
    query.add_constraint("featureType", "=", "long_terminal_repeat", code = "G")
    #query.add_constraint("featureType", "=", "centromere", code = "F")
    query.add_constraint("featureType", "=", "Y_prime_element", code = "E")
    query.add_constraint("featureType", "=", "X_element", code = "D")
    query.add_constraint("featureType", "=", "X_element_combinatorial_repeat", code = "C")
    #query.add_constraint("featureType", "=", "ARS", code = "B")
    query.add_constraint("featureType", "=", "ORF", code = "A")
    query.add_constraint("featureType", "=", "blocked_reading_frame", code = "X")
    query.add_constraint("featureType", "=", "intein_encoding_region", code = "Y")
    query.add_constraint("organism.name", "=", "Saccharomyces cerevisiae", code = "T")
    #query.set_logic("(A or B or C or D or E or F or G or H or I or J or K or L or M or N or O or P or Q or R or S or X or Y or Z) and T and U and (V or W)")
    query.set_logic("(A or C or D or E or G or H or J or K or L or M or N or O or P or Q or R or S or X or Y or Z) and T and U and (V or W)")


    # Now almost ready to make the list.
    # set up the list
    syst_id_list = []

    # prepare a list to store the information for each gene to ultimately save as a file
    gene_data_list = []


    # Make the list
    sys.stderr.write("Please wait. Acquiring id information on every gene reported at YeastMine to ultimately make a subset containing the user-requested number...")
    if progress_bar_use:
        from tqdm import * #see about this module at https://github.com/tqdm/tqdm and https://github.com/noamraph/tqdm
        genes_processed = 0
        none_instances = 0
        sys.stderr.write("\n") #go to next line so progress bar doesn't delete earlier text
        for row in tqdm(query.rows()):
            if row["secondaryIdentifier"] == None:
                none_instances += 1
                #print row["primaryIdentifier"], row["sgdAlias"],row["symbol"], row["description"], row["featureType"]
                # Using that print statement on above line to look into this I found 111 give `None` for row["secondaryIdentifier"]
                # and so just used that method here to filter out and not add to lists instead of toying with above since maybe
                # some have identifers since when I had filtered more I was down to ~6532 genes ??
                '''
                S000029636 None None None intein_encoding_region
                S000028938 None None None telomeric_repeat
                S000028864 None None None telomeric_repeat
                S000028941 None None None telomeric_repeat
                S000028945 None None None telomeric_repeat
                S000028872 None None None telomeric_repeat
                S000028949 None None None telomeric_repeat
                S000028876 None None None telomeric_repeat
                S000028958 None None None telomeric_repeat
                S000028883 None None None telomeric_repeat
                S000028888 None None None telomeric_repeat
                S000028965 None None None telomeric_repeat
                S000028966 None None None telomeric_repeat
                S000028892 None None None telomeric_repeat
                S000028897 None None None telomeric_repeat
                S000028971 None None None telomeric_repeat
                S000028975 None None None telomeric_repeat
                S000028902 None None None telomeric_repeat
                S000028979 None None None telomeric_repeat
                S000028907 None None None telomeric_repeat
                S000028983 None None None telomeric_repeat
                S000028984 None None None telomeric_repeat
                S000028911 None None None telomeric_repeat
                S000028912 None None None telomeric_repeat
                S000028913 None None None telomeric_repeat
                S000028990 None None None telomeric_repeat
                S000028919 None None None telomeric_repeat
                S000028920 None None None telomeric_repeat
                S000028994 None None None telomeric_repeat
                S000028925 None None None telomeric_repeat
                S000028998 None None None telomeric_repeat
                S000028930 None None None telomeric_repeat
                S000028939 None None None X_element
                S000028865 None None None X_element
                S000028942 None None None X_element
                S000028868 None None None X_element
                S000028946 None None None X_element
                S000028873 None None None X_element
                S000028950 None None None X_element
                S000028877 None None None X_element
                S000028954 None None None X_element
                S000028880 None None None X_element
                S000028959 None None None X_element
                S000028884 None None None X_element
                S000028961 None None None X_element
                S000028889 None None None X_element
                S000028967 None None None X_element
                S000028893 None None None X_element
                S000028898 None None None X_element
                S000028972 None None None X_element
                S000028976 None None None X_element
                S000028903 None None None X_element
                S000028980 None None None X_element
                S000028908 None None None X_element
                S000028985 None None None X_element
                S000028914 None None None X_element
                S000028991 None None None X_element
                S000028921 None None None X_element
                S000028995 None None None X_element
                S000028926 None None None X_element
                S000028999 None None None X_element
                S000028931 None None None X_element
                S000028934 None None None X_element
                S000029003 None None None X_element
                S000028866 None None None X_element_combinatorial_repeat
                S000028943 None None None X_element_combinatorial_repeat
                S000028869 None None None X_element_combinatorial_repeat
                S000028947 None None None X_element_combinatorial_repeat
                S000028874 None None None X_element_combinatorial_repeat
                S000028951 None None None X_element_combinatorial_repeat
                S000028878 None None None X_element_combinatorial_repeat
                S000028955 None None None X_element_combinatorial_repeat
                S000028885 None None None X_element_combinatorial_repeat
                S000028962 None None None X_element_combinatorial_repeat
                S000028890 None None None X_element_combinatorial_repeat
                S000028968 None None None X_element_combinatorial_repeat
                S000028894 None None None X_element_combinatorial_repeat
                S000028899 None None None X_element_combinatorial_repeat
                S000028973 None None None X_element_combinatorial_repeat
                S000028977 None None None X_element_combinatorial_repeat
                S000028904 None None None X_element_combinatorial_repeat
                S000028981 None None None X_element_combinatorial_repeat
                S000028909 None None None X_element_combinatorial_repeat
                S000028986 None None None X_element_combinatorial_repeat
                S000028915 None None None X_element_combinatorial_repeat
                S000028992 None None None X_element_combinatorial_repeat
                S000028922 None None None X_element_combinatorial_repeat
                S000028996 None None None X_element_combinatorial_repeat
                S000028927 None None None X_element_combinatorial_repeat
                S000029000 None None None X_element_combinatorial_repeat
                S000028932 None None None X_element_combinatorial_repeat
                S000028935 None None None X_element_combinatorial_repeat
                S000028870 None None None Y_prime_element
                S000028952 None None None Y_prime_element
                S000028956 None None None Y_prime_element
                S000028881 None None None Y_prime_element
                S000028886 None None None Y_prime_element
                S000028963 None None None Y_prime_element
                S000028969 None None None Y_prime_element
                S000028895 None None None Y_prime_element
                S000028900 None None None Y_prime_element
                S000028905 None None None Y_prime_element
                S000028988 None None None Y_prime_element
                S000028987 None None None Y_prime_element
                S000028916 None None None Y_prime_element
                S000028917 None None None Y_prime_element
                S000028923 None None None Y_prime_element
                S000028928 None None None Y_prime_element
                S000029001 None None None Y_prime_element
                S000028936 None None None Y_prime_element
                S000029004 None None None Y_prime_element
                '''
            else:
                genes_processed += 1
                syst_id_list.append(row["secondaryIdentifier"])
                # Collect the data as a list of lists for possible future use and/or speeding up runs
                gene_data_list.append(row["secondaryIdentifier"])

    else:
        genes_processed = 0
        for row in query.rows():
            if row["secondaryIdentifier"] == None:
                none_instances += 1
                #print row["primaryIdentifier"], row["sgdAlias"],row["symbol"], row["description"], row["featureType"]
                # SEE ABOVE ABOUT DEBUGGING WITH THAT LINE
            else:
                genes_processed += 1
                syst_id_list.append(row["secondaryIdentifier"])
                # Collect the data as a list of lists for possible future use and/or speeding up runs
                gene_data_list.append(row["secondaryIdentifier"])
            #every 200 lines print
            if (genes_processed % 200 == 0):
                sys.stderr.write(".")

    # assign `genes_processed` to something more meaningful
    genes_in_genome = genes_processed

    #print none_instances # FOR DEBUGGING GENE LIST

    # Save the data in gene_data_list for possibe future use or for saving time.
    # This will allow storage of the uds. This will serve two
    # two purposes:
    # 1) This will store the version of YeastMine gene list ids at the time. And
    # therefore as gene designations change perhaps in later YeastMine/SGD
    # releases, this will have served to capture the data for when the input
    # data was originally created. At that time the version of YeastMine/SGD
    # should match the generated data.
    # 2) This will make the script run faster by eliminating the need to access
    #  YeastMine and make on subsequent runs.
    # The file will be stored as a ".py" file for ease but any tecxt editor will
    # be able to read it. It may need some manipulation to convery it to a form
    # that is easy to read for a human but the data will be there in almost
    # readable form.
    generate_data_file(gene_data_list)



# assign `genes_processed` to something more meaningful
genes_in_genome = genes_processed


# Now use user-provided number to make a subset from the list of yeast genes
subset_of_genes = random.sample(syst_id_list, number_of_genes_for_list)



# handle the generating the output list text
# Make the list easily made into an output file by separating each with a new line
text_to_save = list2text(subset_of_genes)


# Save results and signal that to user
generate_output_file(text_to_save)






#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
