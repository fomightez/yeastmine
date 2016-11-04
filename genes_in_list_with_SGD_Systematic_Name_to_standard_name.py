#!/usr/bin/env python


# genes_in_list_with_SGD_Systematic_Name_to_standard_name.py by Wayne Decatur



#*******************************************************************************
# USES Python 2.7 but should be convertable via
# 2to3, see https://docs.python.org/3.0/library/2to3.html
#
# PURPOSE: Using YeastMine as a source of yeast gene data, this script converts
# a list of systematic yeast gene ids to standard (common names), where they
# exist. It just adds the yeast systematic identifier on a line in the new list
# for those that don't have a standard (common) gene name.
# Importantly, the produced output file will have the systematic identifiers
# replaced with the standard (common) gene name in the same order as the input
# list.
# The input list should be gene ids each on a separate line of the file.
# The input list has to have to have the yeast gene systematic identifiers at
# the start of each line. There can be other text on the line as long as the
# additional text is separated by space or tabs from the other data on the same
# line. (It would be a simple edit from
# line_list = line.split() to line_list = line.split(',') in order to convert
# this script to work for comma-separated values on each line.) The produced
# output will place the additional content on any line after the identifier
# after a tab. (Change the "\t" on line 255 to read ", " to change the output to also be csv.)
#
# While the default is to only send the standard (common) gene name to the
# output, the addition of the optional flag `--details` to the command call will expand the information sent to the output list beyond the standard name to a full list of details about the yeast gene. This will quickly allow one an overview of the gene information for many genes without use of SGD in a browser. The details printed on each line follow this order: primaryIdentifier, secondaryIdentifier, symbol, name, organism.shortName, proteins.symbol?!?!??!, sgdAlias, featureType, and description. <-- I don't think it will have `proteins.symbol` so fix when know.
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version.
#
#
# to do:
# -
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python genes_in_list_with_SGD_Systematic_Name_to_standard_name.py list.txt
#-----------------------------------
#
#
#*******************************************************************************
#


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
stored_gene_data_file_prefix = "yeastmine_data_for_sys_to_std" #
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


def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("file1.txt")
    returns
        "file1_converted_to_std_id.txt"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name + "_converted_to_std_id" + file_extension
    else:
        return file_name + "_converted_to_std_id"

def generate_output_file(provided_text):
    '''
    function text and saves it as a text file
    '''
    name_of_file_to_save = generate_output_file_name(list_files_to_analyze_list[0])
    data_file_stream = open(name_of_file_to_save , "w")
    data_file_stream.write(provided_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    data_file_stream.close()
    sys.stderr.write( "\nOverlap identified! Shared items list saved as '{0}'.\n".format(name_of_file_to_save))

def list2text(a_list):
    '''
    a function that takes a lists and makes a string where each item in list
    is on a new line
    '''
    return "\n".join(a_list)



def header_text_note_maker(month, year):
    '''
    function generates text that puts description(header) for list entries in
    gene_data_list

    month and year are provided from the calling function to make header better
    '''
    header_text = "# These were the identifiers for all the " + str(
        features_in_genome) +" yeast genes in YeastMine "+ month + " " + year +".\n# The values in the list for each gene are as follows:\n"
    # Recall the values in the list for each gene are as follows:
    # primaryIdentifier, secondaryIdentifier, symbol, name,  sgdAlias, featureType, description
    header_text += "# primaryIdentifier, secondaryIdentifier, symbol, name,  sgdAlias, featureType, description\n"

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
    features_in_genome) +" yeast genes stored for posible future use.\n") # `\b ` in the
    # deletes the spinner, if was there; it is important that some text be
    # after the backspace because backspace and new line alone doesn't write
    # over the spinner otherwise.




###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###














#*******************************************************************************
###-----------------for parsing command line arguments-----------------------###
parser=argparse.ArgumentParser(prog="genes_in_list_with_SGD_Systematic_Name_to_standard_name",
    description="genes_in_list_with_SGD_Systematic_Name_to_standard_name.py uses\
    data from YeastMine to convert a list of systematic gene ids in a \
    file to standard (common) gene names, where they exist. The list should be \
    gene ids each on a separate line of the file. \
    **** Script by Wayne Decatur   \
    (fomightez @ github) ***")

parser.add_argument("List", help="Name of file containing `systematic ids` list to convert. REQUIRED.", type=argparse.FileType('r'), metavar="FILE")
parser.add_argument("-d", "--details",help=
    "add this flag to have the output file have an expanded set of information \
    about the gene in place of the systematic id. The information will include \
    a description in addition to the standard name.",
    action="store_true")

#I would also like trigger help to display if no arguments provided because need at least one input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
input_file_stream = args.List
include_expanded_gene_details = args.details












###-----------------Actual Main portion of script---------------------------###


# Use previously saved list of yeast gene info, or if none exists contact YeastMine
# and get a list of the genes

# To check for a file that begins with the prefix make a list of the files in
# the folder with the script and check if one of them begins with the prefix text.
# Then use that to get name if any match by taking first one because there never
# will be more than one unless debugging. Set to something that couldn't
# possibly match anything in folder otherwise so can use
# `os.path.isfile(stored_gene_data_file)` without having to first check if `stored_gene_data_file` id defined.
# Line below based on Marc L's answer at http://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
stored_gene_data_file_possible_list = [filename for filename in os.listdir('.') if (filename.startswith(stored_gene_data_file_prefix )) and (not filename.endswith('.pyc'))] # the `not filename.endswith('pyc')` is to exclude getting name of compiled version
if stored_gene_data_file_possible_list:
    stored_conversion_data_file = stored_gene_data_file_possible_list[0]
else:
    stored_conversion_data_file = "DOESN'T EXIST and this is an impossible name to never match a file"

if os.path.isfile(stored_conversion_data_file) :
    # If data for conversion table already saved, used that to make dictionary.
    # The reason the dictionary wasn't saved is because it drops a lot of the
    # gene data information and the additional details saved in the gene data
    # list may later help in  sorting if gene is the same or different, etc..
    #
    #import the saved data list
    import importlib
    imported_data = importlib.import_module(stored_conversion_data_file[:-3], package=None) # `[:-3]` part is because don't want `.py` part of file name when calling module
    # instead of using `imported_data.gene_data_list` assign variable shorter name.
    gene_data_list = imported_data.gene_data_list

    # Now almost ready to make the dictionary
    # set up defaultdict
    from collections import defaultdict
    # just need a string as dictionary value since even if `include_expanded_gene_details`
    # is true the value of the dictionary will just a string of text
    # just need a string as dictionary value since even if `include_expanded_gene_details`
    conversion_resolving_dictionary = defaultdict(str) # see http://ludovf.net/blog/python-collections-defaultdict/


    # Make the dictionary
    sys.stderr.write("Using stored genes data previously acquired from YeastMine, stored as `" + stored_conversion_data_file +"`,to make a dictionary for conversion.\n(Rename that file if you prefer the script try to retrieve the pertinent information from YeastMine at this time.)..." )
    genes_processed = 0
    for gene_info in gene_data_list:
        # Recall the values in the list for each gene are as follows:
        # primaryIdentifier, secondaryIdentifier, symbol, name,  sgdAlias, featureType, description


        # Depending on state of of details flag,
        # `include_expanded_gene_details` adjust what will get put in the conversion
        # dictionary at this time. All the information will be stored if not already.
        if include_expanded_gene_details:
            # all details will be used to replace the systematic id
            conversion_resolving_dictionary[gene_info[1]] = ' '.join(gene_info) # put \t between single quotes, instead of the space, to make tab separated
        else:
            # just the standard (common) name will be used to replace the
            # systematic id
            conversion_resolving_dictionary[gene_info[1]] = gene_info[2]

        # collect data to use to provide some feedack it is running
        genes_processed += 1
        # no point having progress bar because so fast with data already saved in a file so no call to YeastMine needed.
        if (genes_processed  % 1000 == 0):
            sys.stderr.write(".")

else:
    # No saved file and so we need to contact YeastMine to get the data and
    # process it.

    # Contacting YeastMinr with query
    from intermine.webservice import Service
    service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")
    query = service.new_query("SequenceFeature")
    # The view specifies the output columns
    query.add_view(
        "primaryIdentifier", "secondaryIdentifier", "symbol", "name",
        "sgdAlias", "featureType", "description"
    )

    query.add_constraint("featureType", "=", "telomerase_RNA_gene", code = "Z")
    #query.add_constraint("qualifier", "IS NULL", code = "W") # W and V need to be commented out so they can be left out of logic so it is more open
    #query.add_constraint("qualifier", "!=", "Dubious", code = "V")   # when it was "!=" vs "=", it wasn't getting the dubious ones that happened to be in gene list. Conversion based on gtf was able to handle them so I changed to "=" so that it could handle them too!!
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
    query.add_constraint("featureType", "=", "not in systematic sequence of S288C", code = "I")
    query.add_constraint("featureType", "=", "ncRNA_gene", code = "H")
    query.add_constraint("featureType", "=", "long_terminal_repeat", code = "G")
    query.add_constraint("featureType", "=", "centromere", code = "F")
    query.add_constraint("featureType", "=", "Y_prime_element", code = "E")
    query.add_constraint("featureType", "=", "X_element", code = "D")
    query.add_constraint("featureType", "=", "X_element_combinatorial_repeat", code = "C")
    query.add_constraint("featureType", "=", "ARS", code = "B")
    query.add_constraint("featureType", "=", "ORF", code = "A")
    query.add_constraint("featureType", "=", "blocked_reading_frame", code = "X")
    query.add_constraint("featureType", "=", "intein_encoding_region", code = "Y")
    query.add_constraint("organism.name", "=", "Saccharomyces cerevisiae", code = "T")
    # query.set_logic("(A or B or C or D or E or F or G or H or I or J or K or L or M or N or O or P or Q or R or S or X or Y or Z) and T and U and (V or W)")
    query.set_logic("(A or B or C or D or E or F or G or H or I or J or K or L or M or N or O or P or Q or R or S or X or Y or Z) and T and U") #conditions concerning V and W were eliminated to try and get a fuller set of possibilities since several dubious ones had standard names from the literature the previous logic wasn't allowing
    # note for logic to get closer to a real set of yeast genes see `make simulated_yeast_gene_set.py` and also see the filter added on line 331 of that script


    # Now almost ready to make the dictionary
    # set up defaultdict
    from collections import defaultdict
    conversion_resolving_dictionary = defaultdict(str) # see http://ludovf.net/blog/python-collections-defaultdict/
    # Just need a string as dictionary value since even if `include_expanded_gene_details`
    # is true the value of the dictionary will just a string of text

    # prepare a list to store the information for each gene to ultimately save as a file
    gene_data_list = []

    # Make the dictionary
    sys.stderr.write("Please wait. Acquiring information on every gene reported at YeastMine for mapping to genes in input file...")
    if progress_bar_use:
        from tqdm import * #see about this module at https://github.com/tqdm/tqdm and https://github.com/noamraph/tqdm
        rows_processed = 0
        sys.stderr.write("\n") #go to next line so progress bar doesn't delete earlier text
        for row in tqdm(query.rows()):
            # Depending on state of of details flag,
            # `include_expanded_gene_details` adjust what will get put in the conversion
            # dictionary at this time.
            # All the information will be stored if not already.
            if include_expanded_gene_details:
                # All details will be used to replace the systematic id.
                #
                # The typecast to string is to avoid problem of
                # concatenating NoneType objects to strings, since some of the
                # values have a `None` where `None` is Python NoneType.
                # Otherwise get error `TypeError: cannot concatenate 'str'
                # and 'NoneType' objects`
                conversion_resolving_dictionary[row["secondaryIdentifier"]] = (
                    str(row["primaryIdentifier"]) + " " +  str(
                        row["secondaryIdentifier"]) +
                    " " + str(row["symbol"]) + " " +  str(row["name"]) + " " +
                    str(row["sgdAlias"]) + " " +  str(row["featureType"]) + " " +
                    str(row["description"]))

            else:
                # just the standard (common) name will be used to replace the
                # systematic id.
                # The typecast to string is to avoid problem of
                # concatenating NoneType objects to strings, since some of them
                # have a `None` standard name where `None` is Python NoneType.
                # Otherwise get error `TypeError: cannot concatenate 'str'
                # and 'NoneType' objects`
                conversion_resolving_dictionary[row["secondaryIdentifier"]] = (
                    str(row["symbol"]))
            #
            #provide some feedack it is running
            rows_processed += 1
            # Collect the data as a list of lists for possible future use and/or
            # speeding up runs.
            # (The typecast to string is to avoid later problems of concatenating
            # NoneType objects to strings, since some of the values are defined
            # as `None`, where `None` is Python NoneType.)
            gene_data_list.append([str(row["primaryIdentifier"]),
                str(row["secondaryIdentifier"]), str(row["symbol"]),
                str(row["name"]), str(row["sgdAlias"]), str(row["featureType"]),
                str(row["description"])])

    else:
        rows_processed = 0
        for row in query.rows():
            # Depending on state of of details flag,
            # `include_expanded_gene_details` adjust what will get put in the conversion
            # dictionary at this time.
            # All the information will be stored if not already.
            if include_expanded_gene_details:
                # all details will be used to replace the systematic id
                #
                # The typecast to string is to avoid problem of
                # concatenating NoneType objects to strings, since some of the
                # values have a `None` where `None` is Python NoneType.
                # Otherwise get error `TypeError: cannot concatenate 'str'
                # and 'NoneType' objects`
                conversion_resolving_dictionary[row["secondaryIdentifier"]] = (
                    str(row["primaryIdentifier"]) + " " +  str(
                        row["secondaryIdentifier"]) +
                    " " + str(row["symbol"]) + " " +  str(row["name"]) + " " +
                    str(row["sgdAlias"]) + " " +  str(row["featureType"]) + " "
                    + str(row["description"]))
            else:
                # just the standard (common) name will be used to replace the
                # systematic id.
                # The typecast to string is to avoid problem of
                # concatenating NoneType objects to strings, since some of them
                # have a `None` standard name where `None` is Python NoneType.
                # Otherwise get error `TypeError: cannot concatenate 'str'
                # and 'NoneType' objects`
                conversion_resolving_dictionary[row["secondaryIdentifier"]] = (
                    str(row["symbol"]))
            #
            #
            #provide some feedack it is running
            rows_processed += 1
            # Collect the data as a list of lists for possible future use and/or
            # speeding up runs.
            # (The typecast to string is to avoid later problems of concatenating
            # NoneType objects to strings, since some of the values are defined
            # as `None`, where `None` is Python NoneType.)
            gene_data_list.append([str(row["primaryIdentifier"]),
                str(row["secondaryIdentifier"]), str(row["symbol"]),
                str(row["name"]), str(row["sgdAlias"]), str(row["featureType"]),
                str(row["description"])])
            #every 200 lines print
            if (rows_processed % 200 == 0):
                sys.stderr.write(".")

    # assign `rows_processed` to something more meaningful
    features_in_genome = rows_processed

    # Save the data in gene_data_list for possibe future use or for saving time.
    # This will allow storage if the conversion data. This will serve two
    # two purposes:
    # 1) This will store the version of YeastMine gene list at the time. And
    # therefore as gene designations change perhaps in later YeastMine/SGD
    # releases, this will have served to capture the data for when the input
    # data was originally created. At that time the version of YeastMine/SGD
    # should match the generated data.
    # 2) This will make the script run faster by eliminating the need to access
    # YeastMine and make on subsequent runs.
    # The file will be stored as a ".py" file for ease but any text editor will
    # be able to read it. It may need some manipulation to convery it to a form
    # that is easy to read for a human but the data will be there in almost
    # readable form.
    generate_data_file(gene_data_list)











# CONVERT
# Now it is time to go through the list in the file provided when command called
# and convert from systematic ids to standard (common) gene name based on the
# conversion_resolving_dictionary

new_file_text = ""
lines_processed = 0

# open input file and start reading
sys.stderr.write("\nReading input file and converting...")
#input_file_stream = open(sys_ids_list_file, "r")  # Don't need separate open when use `type=argparse.FileType`. It sets everything up automatically and you will actually cause errors if try to open when already open.


for line in input_file_stream :
    lines_processed += 1
    # split on space or tab
    '''
    line_list = line.split(maxsplit=1) # Only want one split so anything after gets
    # added to produced text. By not specifying delimiter, it splies on ANY whitespace, includint tabs, see http://stackoverflow.com/questions/4309684/how-in-python-to-split-a-string-with-unknown-number-of-spaces-as-separator and
    # https://docs.python.org/3/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange
    gene_id = line_list[0]
    rest_of_line = line_list[1]
    # ACK THAT SOLUTION ONLY WORKS WITH PYTHON 3!! Cannot specify `maxsplit` in 2.7

    '''
    # Since using Python 2, I'll split default way with no separator argument and then grab everything after as separate item. Cannot ust argument for calling split because want it to split on both space and tabs as it does when called without an argumnet in Python 2. see -> http://stackoverflow.com/questions/4309684/how-in-python-to-split-a-string-with-unknown-number-of-spaces-as-separator
    # gene_id = first in split
    line_list = line.split()
    id_to_convert = line_list[0]
    rest_of_line = line[line.find(id_to_convert)+len(id_to_convert):] #find gets first occurence
    # END OF PYTHON 2 SPECIFIC APPROACH


    # if the id is a key in the dictionay, do the conversion to the text that it
    # has as a value, otherwise just copy the line text over to the text being
    # collected for the output
    if id_to_convert in conversion_resolving_dictionary:
        new_file_text = new_file_text + conversion_resolving_dictionary[id_to_convert] + " " + rest_of_line.strip() + '\n'
    else:
        new_file_text = new_file_text + line.strip() + '\n'




# Completed scan of input file and therefore close file, alert user as to any
# issues, and write new file.
sys.stderr.write( "\n"+ str(lines_processed) + " lines read from '" + input_file_stream.name + "'.")
input_file_stream.close()

output_file_name = generate_output_file_name(input_file_stream.name)
output_file = open(output_file_name, "w")
output_file.write(new_file_text.rstrip('\r\n')) #rstrip to remove trailing newline
# from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
output_file.close()
sys.stderr.write("\n\nOutput file named '" + output_file_name +"' created.\n")




#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
