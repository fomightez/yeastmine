#!/usr/bin/env python

# see `Trying to convert Shafi's list to something that works in T-profiler.md` for info about this script

# To do: make so input file name isn't hard coded into script, and the output
# file name is based on the input.


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
input_file_name = "culled_extracted_geneIDs_and_log2change.txt"

output_file_name = "systematicIDs_and_log2change.txt"

stored_conversion_data_file_prefix = "yeastmine_conversion_data" #
# prefix for file name to save data for subsequent use or to use  from previous
# runs. Approach like this first worked out in `make simulated_yeast_gene_set.py`

discarding_non_orfs = False   # Only keep ORFs? Disarding non-ORFS will mean those
# like NME1 that don't have a standard name beginnning in `Y`, like YDR190C or
# YPL235W, won't be moved over to the output file. I suspect that they need to
# be discarded because the T-profiler directions at
# http://www.t-profiler.org/Saccharomyces/add_info/howtoupload.html
# only refer those that begin
# with Y, like YDR190C or YPL235W.


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

    This was originally developed in `make simulated_yeast_gene_set.py`


    '''
    # prepare to timestamp the name of file to save
    import datetime
    now = datetime.datetime.now()
    # see http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
    # for formatting options simplified
    return file_name_prefix + now.strftime("%B%Y") +".py", now.strftime(
        "%B"), now.strftime("%Y")

def header_text_note_maker(month, year):
    '''
    function generates text that puts description(header) for list entries in
    gene_data_list

    month and year are provided from the calling function to make header better
    '''
    header_text = "# These were the identifiers for all the " + str(
        features_in_genome ) +" yeast sequenceFeatures in YeastMine "+ month + " " + year +".\n# The values in the list for each are as follows:\n"
    header_text += "# primaryIdentifier, secondaryIdentifier, symbol, name, sgdAlias, featureType, description\n"
    return header_text

def generate_data_file(the_data_list):
    '''
    function takes gene data list from YeastMine and saves it as script-like file
    '''
    stored_gene_data_file, month, year  = generate_stored_data_file_name(
        stored_conversion_data_file_prefix) # see next line for info on month & year.
    # Month and year are first used in the function just called and so instead
    # of calling that import and commands again, just passing back.


    data_file_stream = open(stored_gene_data_file , "w")
    data_file_stream.write(header_text_note_maker(month, year))
    data_file_stream.write('gene_data_list = ' + repr(gene_data_list ) + "\n")
    data_file_stream.close()
    sys.stderr.write( "\b \nGene data stored for future use.\n") # `\b ` in the
    # deletes the spinner; it is important that some text be after the backspace
    # because backspace and new line alone doesn't write over the spinner otherwise.

###--------------------------END OF HELPER FUNCTIONS---------------------------###


# Use previously saved list of yeast gene info, or if none exists contact YeastMine
# and get a list of the genes

# To check for a file that begins with the prefix make a list of the files in
# the folder with the script and check if one of them begins with the prefix text.
# Then use that to get name if any match by taking first one because there never
# will be more than one unless debugging. Set to something that couldn't
# possibly match anything in folder otherwise so can use
# `os.path.isfile(stored_gene_data_file)` without having to first check if `stored_gene_data_file` id defined.
# Line below based on Marc L's answer at http://stackoverflow.com/questions/15312953/choose-a-file-starting-with-a-given-string
stored_gene_data_file_possible_list = [filename for filename in os.listdir('.') if (filename.startswith(stored_conversion_data_file_prefix )) and (not filename.endswith('.pyc'))] # the `not filename.endswith('pyc')` is to exclude getting name of compiled version
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
    gene_id_to_syst_id_dict = defaultdict(str) # see http://ludovf.net/blog/python-collections-defaultdict/

    # Make the dictionary
    sys.stderr.write("Using stored genes data previously acquired from YeastMine, stored as `" + stored_conversion_data_file +"`,to make a dictionary for conversion.\n(Rename that file if you prefer the script try to retrieve the pertinent information from YeastMine at this time.)..." )
    genes_processed = 0
    for gene_info in gene_data_list:
        # Recall the values in the list for each gene are as follows:
        # primaryIdentifier, secondaryIdentifier, symbol, name, proteins.symbol, sgdAlias, featureType, description
        gene_id_to_syst_id_dict[gene_info[2]] = gene_info[1] # This will make a
        # dictionary entry for the "symbol" key with the gene's systematic_id as the value
        #
        # collect data to use to provide some feedack it is running
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
    query.set_logic("(A or B or C or D or E or F or G or H or I or J or K or L or M or N or O or P or Q or R or S or X or Y or Z) and T and U and (V or W)")
    # note for logic to get closer to a real set of yeast genes see `make simulated_yeast_gene_set.py` and also see the filer added on line 331 of that script


    # Now almost ready to make the dictionary
    # set up defaultdict
    from collections import defaultdict
    gene_id_to_syst_id_dict = defaultdict(str) # see http://ludovf.net/blog/python-collections-defaultdict/

    # prepare a list to store the information for each gene to ultimately save as a file
    gene_data_list = []

    # Make the dictionary
    sys.stderr.write("Please wait. Acquiring information on every gene reported at YeastMine for mapping to genes in input file...")
    if progress_bar_use:
        from tqdm import * #see about this module at https://github.com/tqdm/tqdm and https://github.com/noamraph/tqdm
        rows_processed = 0
        sys.stderr.write("\n") #go to next line so progress bar doesn't delete earlier text
        for row in tqdm(query.rows()):
            gene_id_to_syst_id_dict[row["symbol"]] = row["secondaryIdentifier"]
            # This will make a dictionary entry for the "symbol" key with the gene's systematic_id as the value
            #
            #provide some feedack it is running
            rows_processed += 1
            # Collect the data as a list of lists for possible future use and/or speeding up runs
            gene_data_list.append([row["primaryIdentifier"],
                row["secondaryIdentifier"], row["symbol"], row["name"],
                row["sgdAlias"], row["featureType"],
                row["description"]])

    else:
        rows_processed = 0
        for row in query.rows():
            gene_id_to_syst_id_dict[row["symbol"]] = row["secondaryIdentifier"]
            # This will make a dictionary entry for the "symbol" key with the gene's systematic_id as the value
            #
            #provide some feedack it is running
            rows_processed += 1
            # Collect the data as a list of lists for possible future use and/or speeding up runs
            gene_data_list.append([row["primaryIdentifier"],
                row["secondaryIdentifier"], row["symbol"], row["name"],
                row["sgdAlias"], row["featureType"],
                row["description"]])
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




#Now go through the file and make the new file with the names replaced
#initialize holder for text that will be output
new_file_text = ""
lines_processed = 0
# open input file and start reading
sys.stderr.write("\nReading input file and converting...") #backspace at start to delete the spinner
input_file_stream = open(input_file_name , "r")
for line in input_file_stream:
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
    gene_id = line_list[0]
    rest_of_line = line [line.find(gene_id)+len(gene_id):] #find gets first occurence
    # END OF PYTHON 2 SPECIFIC APPROACH

    # log2value = second in split (not defining as variable since it doesn't get used). (AND TRYING TO MAKE GENERAL SOLUTION.) IT ALSO HAS LINE END AT END OF STRING.
    # if that gene_id is in the conversion dictionary, use to convert to systematic
    # name. If not, then leave line as it was.
    if gene_id in gene_id_to_syst_id_dict:
    	new_file_text = new_file_text + gene_id_to_syst_id_dict[gene_id]+ "\t" + rest_of_line.strip() + "\n"  #stripping the line ending and then adding one back so that it won't rely on there being text besides the indentifier on the line. If there is no text after the identifier, it will still get line ending there.
    elif not discarding_non_orfs:
    	new_file_text = new_file_text + line

#Completed scan of input file and therefore close file, write new file.
sys.stderr.write( "\n"+ str(lines_processed) + " lines read from '" + input_file_name + "'.")
input_file_stream.close()
output_file = open(output_file_name, "w")
output_file.write(new_file_text.rstrip('\r\n')) #rstrip to remove trailing newline
# from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
output_file.close()
sys.stderr.write("\n\nOutput file named '" + output_file_name +"' created.\n") # This file should work at T-profiler --> http://www.t-profiler.org/

