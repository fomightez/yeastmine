#!/usr/bin/env python
# get_gene_genomic_seq_as_FASTA.py 
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# get_gene_genomic_seq_as_FASTA.py  by 
# Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.6; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a systematic name, standard name, or alias as defined 
# at gene page at yeastgenome.org, rerieves the related information from 
# YeastMine, and saves or returns the genomic sequence of the gene in FASTA 
# format.
#
# Saves file if called from the command line. Can be used to send the FASTA file
# record to IPython or Jupyter if main function called.
#
# Note search is only as good as the supplied gene identifier, and so it is best
# to match the systematic name standard name seen on the corresponding gene page
# at Saccharomyces Genome Database (SGD) (yeastgenome.org). If it is more 
# convenient, you can test queries via web form at 
# https://yeastmine.yeastgenome.org/yeastmine/template.do?name=Gene_GenomicDNA&scope=all.
# The first result there and what this script returns should be the same.
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
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python get_gene_genomic_seq_as_FASTA.py gene_id
#-----------------------------------
#
# Issue `get_gene_genomic_seq_as_FASTA.py  -h` for details.
# 
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the results file (or results as a string) in the 
# call to the main function similar to below:
# get_gene_genomic_seq_as_FASTA("rpa12")
# -OR- 
# To get the output returned as a string instead of outputing a file:
# s = get_gene_genomic_seq_as_FASTA("VPH1", return_text = True)
# 
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
s = get_gene_genomic_seq_as_FASTA("VPH1", return_text = True)
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


def generate_output_file_name(gene_nom_info,extension_for_saving):
    '''
    Takes a dictionay of gene name information and and extension string and 
    returns string for the name of the output file. The generated name is made 
    to mirror what you'd get using  the 'Download Sequence (.fsa)' button from 
    under the 'Sequence' tab for each gene at yeastgenome.org.


    Specific example
    =================
    Calling function with
        ({'sys_nom':'YOR270C','std_nom': 'VPH1', 'alias':'????'},"fsa")
    returns
        "S288C_YOR270C_VPH1_genomic.fsa"
    '''
    return "S288C_{}_{}_genomic.{}".format(
        gene_nom_info['sys_nom'],gene_nom_info['std_nom'],extension_for_saving)



###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###






#*******************************************************************************
###------------------------'main' function of script--------------------------##

def get_gene_genomic_seq_as_FASTA(gene_id, 
    extension_for_saving = extension_for_saving, return_text = False):
    '''
    Main function of script. 
    Takes a gene's systematic name, standard name, or alias as defined at gene 
    page at yeastgenome.org, retrieves the associated information from 
    YeastMine, and saves or returns the genomic sequence of the gene in FASTA 
    format.

    Use `return_text` if calling from IPython or a Jupyter notebook and you want
    the FASTA record returned as text,
    '''
    # Get gene information from YeastMine
    #---------------------------------------------------------------------------
    # Based on the template Gene_Genomic DNA available under 
    # 'Gene --> Genomic DNA' when under 'Templates' on navigation bar 
    # in middle of page at YeastMine. Direct link:
    # https://yeastmine.yeastgenome.org/yeastmine/template.do?name=Gene_GenomicDNA&scope=all
    
    service = Service("https://yeastmine.yeastgenome.org:443/yeastmine/service")

    # Retrieve genomic DNA (DNA sequence with introns) for the specified gene. 

    template =  service.get_template('Gene_GenomicDNA')

    # You can edit the constraint values below
    # E    Gene

    rows = template.rows(
        E = {"op": "LOOKUP", "value": gene_id, "extra_value": "S. cerevisiae"}
    )
    results = []
    for row in rows:
        results.append(row)
    
    # store corresponding gene genomic sequence
    genomic_seq = results[0]["sequence.residues"]
    
    # format gene_nom_info for making output file name or anything else needing 
    # that information
    gene_nom_info = {}
    gene_nom_info['sys_nom'] = results[0]["secondaryIdentifier"]
    gene_nom_info['std_nom'] = results[0]["symbol"]
    gene_nom_info['aliases'] = results[0]["sgdAlias"]
    #print (gene_nom_info['aliases'] ) # FOR DEBUGGING ONLY
    #print (gene_nom_info['std_nom'] ) # FOR DEBUGGING ONLY
    #print (gene_nom_info['sys_nom'] ) # FOR DEBUGGING ONLY


    # feedback
    sys.stderr.write("looking up the gene associated with "
        "{}...".format(gene_id))


    # Make output FASTA record
    #---------------------------------------------------------------------------
    # based handling worked out in 
    # `delete_seq_following_pattern_within_multiFASTA.py`
    record_description = '{}'.format(gene_nom_info['sys_nom'])
    record = SeqRecord(Seq(prot_seq, generic_dna), 
            id=gene_nom_info['std_nom'], description=record_description)#based
        # on https://www.biostars.org/p/48797/ and `.ungap()` method, see
        # https://github.com/biopython/biopython/issues/1511 , and `description`
        # from what I've seen for `id` plus https://biopython.org/wiki/SeqIO
        #print (records[indx]) # ONLY FOR DEBUGGING
    sys.stderr.write("getting genomic sequence for the gene...")

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
            gene_nom_info,extension_for_saving)
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
    kwargs['extension_for_saving'] = extension_for_saving
    get_gene_genomic_seq_as_FASTA(gene_id,**kwargs)
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
        'get_gene_genomic_seq_as_FASTA.py ',
        description="get_gene_genomic_seq_as_FASTA.py  \
        takes a gene's systematic name, standard name, or alias as defined at \
        gene page at yeastgenome.org, retieves the associated information from \
        YeastMine, and saves the coding sequence in FASTA format.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("gene_id", help="gene's systematic name, standard \
        name, or symbol (see gene page at yeastgenome.org). REQUIRED. \
        ", metavar="GENE_ID")

    parser.add_argument('-oe', '--output_extension', action='store', type=str, 
    default= extension_for_saving, help="OPTIONAL: Set an extension for the file \
    name of output. \
    If none provided, '{}' will be used.".format(extension_for_saving))



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    gene_id = args.gene_id
    extension_for_saving = args.output_extension


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************