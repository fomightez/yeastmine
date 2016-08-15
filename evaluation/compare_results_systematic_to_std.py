#!/usr/bin/env python
# compare_results_systematic_to_std.py by Wayne Decatur
# ver 0.01
#
#*******************************************************************************
# USES Python 2.7 but should be convertable via 2to3, see https://docs.python.org/3.0/library/2to3.html
#
# PURPOSE: Takes two output files where a gene list was converted to standard
# (common) gene names, each by a different method. It is being written with the
# idea it would compare results of using YeastMine as the source of gene data to
# results of using a gtf file as the source.
# As written, by default the comparison is case-insensitive.
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# None
#
#
#
# VERSION HISTORY:
# v.0.01. basic working version
#
#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# compare_results_systematic_to_std.py list1.txt list2.txt
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
# ?
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


def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("file1.txt")
    when `list_files_to_analyze_list` contains 3 file names
    returns
        "file1_and_3others_shared_items.txt"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if len(list_files_to_analyze_list) == 2:
        base_name_without_extension_second_file = os.path.splitext(
            os.path.basename(list_files_to_analyze_list[1]))[0]
        if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
            return main_part_of_name + "_and_"+ base_name_without_extension_second_file +"_shared_items" + file_extension
        else:
            return file_name + "_and_"+ base_name_without_extension_second_file +"_shared_items"
    else:
        if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
            return main_part_of_name + "_and_"+ str(len(
                list_files_to_analyze_list) - 1) +"others_shared_items" + file_extension
        else:
            return file_name + "_and_"+ str(len(
                list_files_to_analyze_list) - 1) +"others_shared_items"

def generate_output_file(provided_text):
    '''
    function text and saves it as a text file
    '''
    name_of_file_to_save = generate_output_file_name(input_file_stream1.name)
    data_file_stream = open(name_of_file_to_save , "w")
    data_file_stream.write(provided_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    data_file_stream.close()
    #sys.stderr.write( "\nOverlap identified! Shared items list saved as '{0}'.\n".format(name_of_file_to_save))

def list2text(a_list):
    '''
    a function that takes a lists and makes a string where each item in list
    is on a new line
    '''
    return "\n".join(a_list)

###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###














#*******************************************************************************
###-----------------for parsing command line arguments-----------------------###
parser = argparse.ArgumentParser(prog='compare_results_systematic_to_std.py',description="compare_results_systematic_to_std.py \
    takes two output files where a gene list was converted to standard \
    (common) gene names, each by a different method. It is being written with \
    the idea it would compare results of using YeastMine as the source of gene \
    data to results of using a gtf file as the source. **** Script by Wayne Decatur   \
    (fomightez @ github) ***")
parser.add_argument("List1", help="Name of file containing converted gene list. REQUIRED.", type=argparse.FileType('r'), metavar="FILE")
parser.add_argument("List2", help="Name of the other file containing converted gene list. REQUIRED.", type=argparse.FileType('r'), metavar="FILE")

#I would also like trigger help to display if no arguments or only two provided because need at least two input files
if (len(sys.argv)==1) or (len(sys.argv)==2):    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    sys.stderr.write("********************************** \n")
    sys.stderr.write("Error: too few arguments provided \n")
    sys.stderr.write("********************************** \n")
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
input_file_stream1 = args.List1
input_file_stream2 = args.List2



###-----------------Actual Main portion of script---------------------------###


print "Differences in the files\nFile1\tFile2\tline#"

# read each line and compare
from itertools import izip
#with open(file1) as f1,open(fil2) as f2: # Don't need separate open when use `type=argparse.FileType`. It sets everything up automatically and you will actually cause errors if try to open when already open.
line_count = 1
comparison_result_text = ""
for line_of_file1, line_of_file2 in izip(input_file_stream1, input_file_stream2):
    line_of_file1 = line_of_file1.strip().upper() #don't want spaces or line
    # endings confusing, and want converted to uppercase so case insensitive
    line_of_file2 = line_of_file2.strip().upper()
    # only are concerned with those that differ some
    if line_of_file1 != line_of_file2:
        # plus don't care if one of them is "None", which will be "NONE" since uppercased!
        if line_of_file1 != "NONE" and line_of_file2 != "NONE":
            comparison_result_text += (line_of_file1  + "\t" + line_of_file2  +
             "\t" + str(line_count) + "\n")
    line_count += 1

print comparison_result_text #this way doesn't add extra space between lines due
# to use of both `print` and `+ "\n"` at end. I wanted the `+ "\n"` to set up
# for other output options down the road.


#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
