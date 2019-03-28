#!/usr/bin/env python
# get_chromosomal_coordinates_as_FASTA.py 
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# get_chromosomal_coordinates_as_FASTA.py  by 
# Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.7; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a chromosome designation and coordinates and gets from 
# YeastMine the sequence of that region of the chromsome as FASTA format.
# Saves or returns the genomic sequence of the gene in FASTA format. Enter 
# coordinates in ascending order for the Watson strand and descending order for 
# the Crick strand as you'd do at https://www.yeastgenome.org/seqTools under
# 'Search a specified chromosomal region of S288C genome'.
#
# Saves file if called from the command line. Can be used to send the FASTA file
# record to IPython or Jupyter if main function called.
#
#
#
# Written to run from command line or imported into/pasted/loaded inside a 
# Jupyter notebook cell.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# biopython, intermine
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version

#
# to do:
# - ?
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python get_chromosomal_coordinates_as_FASTA.py IV 200000-2200000
#-----------------------------------
#
# Issue `get_chromosomal_coordinates_as_FASTA.py  -h` for details.
# 
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the results file (or results as a string) in the 
# call to the main function similar to below:
# get_chromosomal_coordinates_as_FASTA("IV",region_str="200000-2200000")
# -OR- 
# To get the output returned as a string instead of outputing a file:
# s = get_chromosomal_coordinates_as_FASTA("I", region_str="100-999", return_text = True)
# 
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
s = get_chromosomal_coordinates_as_FASTA("I", region_str="100-999", return_text = True)
%store s > gene_sequence.fa # to save it to a file in jupyter environment, too
'''
#
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#


extension_for_saving = "fsa" #to be used for naming the output

coordinates_delimiter_default = "-" #change to ":" to use a colon to specify the 
# positions range to span. Mainly meant for advanced/power users because for
# the command line you can just use the `--use_colon` (or `-uc`) flag. And if
# using Jupyter cell you can specify `use_colon = True` when calling the main 
# function.

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************













#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
from intermine.webservice import Service
from Bio import SeqIO
from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord 
from Bio.Alphabet import generic_dna




###---------------------------HELPER FUNCTIONS-------------------------------###


def generate_output_file_name(chr_info,ext_for_saving):
    '''
    Takes a dictionay of chromosome information and and extension string and 
    returns string for the name of the output file.
    Name of file loosely based on output from 
    https://www.yeastgenome.org/seqTools under 'Search a specified chromosomal 
    region of S288C genome'.


    Specific example
    =================
    Calling function with
        ({'chr_nom':'IV','start': 2000, 'end':3000},"fsa")
    returns
        "S288C_chrIV_2000-3000_genomic.fsa"
    '''
    return "S288C_{}_{}-{}_genomic.{}".format(
        chr_info['chr_nom'],chr_info['start'],chr_info['end'],ext_for_saving)



###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###






#*******************************************************************************
###------------------------'main' function of script--------------------------##

def get_chromosomal_coordinates_as_FASTA(chr_id, region_str, use_colon = False,
    extension_for_saving = extension_for_saving, return_text = False):
    '''
    Main function of script. 
    Takes a chromosome designation and coordinates and gets from
    YeastMine the sequence of that region of the chromsome as FASTA format.
    Saves or returns the genomic sequence of the gene in FASTA format.

    The coordinate order is used to signal which strand to get. Coordinates in 
    ascending order for the Watson strand and descending order for the Crick 
    strand as is the convention at https://www.yeastgenome.org/seqTools under
    'Search a specified chromosomal region of S288C genome'.

    Use `return_text` if calling from IPython or a Jupyter notebook and you want
    the FASTA record returned as text,
    '''

    # Parse the region_str to get the start and end positions of the reference 
    # sequence to specify what corresponding segment to extract from each of 
    # the aligned sequences. Handle strand to get be provided via order.
    #---------------------------------------------------------------------------
    if use_colon:
        coordinates_delimiter= ":"
    else:
        coordinates_delimiter = coordinates_delimiter_default
    region_str_parts = region_str.split(coordinates_delimiter)
    start, end = int(region_str_parts[0]), int(region_str_parts[1])
    # just fix if user was knowledgeable about Python and used zero to get to 
    # start because below I try to account for users using common numbering and 
    # it will substract and woould give negative numbers.
    if start == 0:
        start = 1
    if end == 0:
        end = 1
    
    # sanity checks
    assert start != end, (
    "The user-supplied 'start' ({}) and 'end' ({}) cannot be same value"
    ".".format(start,end))

    '''CANNOT USE HERE BECAUSE START CAN BE LARGER TO SIGNAL STRAND
    assert start < end, (
    "The user-supplied 'start' ({}) must be less than "
    "'end' ({}).".format(start,end))
    '''

    # overly explicit strand handling
    if start < end:
        get_watson_strand = True
        get_crick_strand = False
    else:
        get_watson_strand= False
        get_crick_strand= True
    # translate the strand info to YeastMine specifications
    if get_watson_strand:
        strand = 1
        strand_text = "Watson(1)"
        sys.stderr.write("Sequence on Watson strand specified...")
    elif get_crick_strand:
        strand = -1
        strand_text = "Crick(-1)"
        sys.stderr.write("Sequence on Crick strand specified...")
    else:
        sys.stderr.write("\n\nWhich strand?\n")
        sys.exit(1)

    # Get chromosome information from YeastMine
    #---------------------------------------------------------------------------
    # Based on the query I built at YeastMine to get sequence of chromosome and 
    # then can limit to coordinates needed after have entire sequence.
    
    service = Service("https://yeastmine.yeastgenome.org:443/yeastmine/service")

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("Chromosome")

    # The view specifies the output columns
    query.add_view("sequence.residues")
    # constraint values
    chr_designation = "chr"+chr_id
    query.add_constraint("primaryIdentifier", "=", chr_designation, code = "A")


    rows = query.rows()
    results = []
    for row in rows:
        results.append(row)
    
    # store corresponding genomic sequence
    genomic_seq = (
        results[0]["sequence.residues"][min(start,end)-1: max(start,end)]) # the 
    #minus one is so user can provide coordinates in common terms but this
    #  adjusts for zero-indexing.
    # Make reverse complement if want crick strand BELOW after convert to
    # a biopython seq object so can use biopython `.reverse_complement` method


    
    # format chr_info for making output file name or anything else needing 
    # that information
    chr_info = {}
    chr_info['chr_nom'] = chr_designation
    chr_info['start'] = start
    chr_info['end'] = end
    #print (gene_nom_info['aliases'] ) # FOR DEBUGGING ONLY
    #print (gene_nom_info['std_nom'] ) # FOR DEBUGGING ONLY
    #print (gene_nom_info['sys_nom'] ) # FOR DEBUGGING ONLY


    # feedback
    sys.stderr.write("retrieving sequence from chromosome "
        "{}...".format(chr_id))


    # Make output FASTA record
    #---------------------------------------------------------------------------
    # based on handling worked out in 
    # `delete_seq_following_pattern_within_multiFASTA.py`
    # Description line loosely based on output from 
    # https://www.yeastgenome.org/seqTools under 'Search a specified chromosomal 
    # region of S288C genome'.
    record_description = 'coordinates {} to {}; strand is {}'.format(
        start, end, strand_text)
    record = SeqRecord(Seq(genomic_seq, generic_dna), 
            id=chr_designation, description=record_description)#based
        # on https://www.biostars.org/p/48797/ and `.ungap()` method, see
        # https://github.com/biopython/biopython/issues/1511 , and `description`
        # from what I've seen for `id` plus https://biopython.org/wiki/SeqIO
        #print (records[indx]) # ONLY FOR DEBUGGING
    # Make reverse complement if want crick strand after convert to
    # a biopython seq object so can use biopython `.reverse_complement` method
    if get_crick_strand:
        record = record.reverse_complement(id=True,description=True)
    sys.stderr.write("making FASTA formatted entry with retrieved sequence...")

    # Return text if called with `return_text = True`. Otherwise, consider 
    # called from command line & save file.
    #---------------------------------------------------------------------------
    if return_text == True:
        # based on section 4.6 at 
        #http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec:SeqRecord-format
        # Feedback
        sys.stderr.write("\nReturning genomic sequence in FASTA format.")
        return record.format("fasta") 
    else:
        output_file_name = generate_output_file_name(
            chr_info,extension_for_saving)
        SeqIO.write(record,output_file_name, "fasta");
        # Feedback
        sys.stderr.write("\n\nFile of genomic sequence "
            "saved as '{}'.".format(output_file_name))
        sys.stderr.write("\nFinished.\n")




###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###










#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main():
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    kwargs['region_str'] = region_str
    kwargs['use_colon'] = use_colon
    kwargs['extension_for_saving'] = extension_for_saving
    get_chromosomal_coordinates_as_FASTA(chr_id,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__" and '__file__' in globals():
    """ This is executed when run from the command line """
    # Code with just `if __name__ == "__main__":` alone will be run if pasted
    # into a notebook. The addition of ` and '__file__' in globals()` is based
    # on https://stackoverflow.com/a/22923872/8508004
    # See also https://stackoverflow.com/a/22424821/8508004 for an option to 
    # provide arguments when prototyping a full script in the notebook.
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog=
        'get_chromosomal_coordinates_as_FASTA.py ',
        description="get_chromosomal_coordinates_as_FASTA.py  \
        Takes a chromosome designation and coordinates and gets from YeastMine \
        the sequence of that region of the chromsome as FASTA format. Saves \
        or returns the genomic sequence of the gene in FASTA format. \
        Coordinate order is used to specify the strand to return as you'd do \
        at https://www.yeastgenome.org/seqTools under 'Search a specified \
        chromosomal region of S288C genome'.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("chr_id", help="Roman numeral I through XVI, or 'mt' \
        without quotes, of S. cerevisiae S288C chromosome containing the region \
        to retrieve. REQUIRED. \
        ", metavar="CHR_ID")
    parser.add_argument("region", help="Coordinates of region of specified \
        chromomsome to retrieve. Provide \
        start position and end position coordinates separated by the region \
        delimiter which is '{}' by default. You can use `--use_colon` flag to \
        change to a colon, for using something like, `201:405` instead of \
        `201{}405`. Provide coordinates in ascending order for the Watson \
        strand and descending order for the Crick strand. (Coordinates are \
        meant to refer to 'common' numbering scheme where first residue is \
        numbered one, etc.)\
        ".format(coordinates_delimiter_default,coordinates_delimiter_default), 
        metavar="REGION_START-REGION_END")
    parser.add_argument("-uc", "--use_colon",help=
    "Add this flag to be able to specify that you want to use a colon in for \
    specifying the region to extact the corresponding aligned sequences.",
    action="store_true")
    parser.add_argument('-oe', '--output_extension', action='store', type=str, 
    default= extension_for_saving, help="OPTIONAL: Set an extension for the file \
    name of output. \
    If none provided, '{}' will be used.".format(extension_for_saving))

    '''
    parser.add_argument('-oe', '--output_extension', action='store', type=str, 
    default= extension_for_saving, help="OPTIONAL: Set an extension for the file \
    name of output. \
    If none provided, '{}' will be used.".format(extension_for_saving))
    '''



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    chr_id = args.chr_id
    region_str = args.region
    use_colon = args.use_colon
    extension_for_saving = args.output_extension


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
