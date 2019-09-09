#!/usr/bin/env python

## USAGE: LIST ALL YEAST PROTEIN GENES IN ORDER OF SIZE.
## SINCE EACH GENE IS ON A SINGLE LINE, WHEN VIEWING IN A TEXT EDITOR
## YOU CAN JUST USE LINE NUMBER [MINUS ONE TO ACCOUNT FOR COLUMN NAMES LINE]
## TO GET THE RANK.

# See the README.txt for this script at the link below for more information:
# https://github.com/fomightez/yeastmine

## IMPETUS FOR THIS SCRIPT:
## CURIOSITY ABOUT WHERE SOME GENE LIE IN THE SIZE SPECTRUM WITHIN YEAST.

from intermine.webservice import Service
service = Service("https://yeastmine.yeastgenome.org:443/yeastmine/service")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view(
    "primaryIdentifier", "secondaryIdentifier", "symbol", "name",
    "organism.shortName", "proteins.symbol", "proteins.molecularWeight",
    "proteins.pI", "featureType", "description"
)

# This query's custom sort order is specified below:
query.add_sort_order("Gene.proteins.molecularWeight", "DESC")

# You can edit the constraint values below
query.add_constraint("featureType", "!=", "pseudogene", code = "G")
query.add_constraint("featureType", "=", "ORF", code = "C")
query.add_constraint("featureType", "=", "transposable_element_gene", code = "H")
query.add_constraint("status", "=", "Active", code = "D")
query.add_constraint("qualifier", "!=", "Dubious", code = "E")
query.add_constraint("qualifier", "IS NULL", code = "F")
query.add_constraint("proteins.molecularWeight", ">=", "1", code = "A")

# Your custom constraint logic is specified with the code below:
query.set_logic("A and (C or H) and G and D and (E or F)")


print "primaryIdentifier\tsecondaryIdentifier\tsymbol\tname\torganism.shortName\tproteins.symbol\tproteins.molecularWeight\tproteins.pI\tfeatureType\tdescription"


for row in query.rows():
    print row["primaryIdentifier"], row["secondaryIdentifier"], row["symbol"], row["name"], \
        row["organism.shortName"], row["proteins.symbol"], row["proteins.molecularWeight"], \
        row["proteins.pI"], row["featureType"], row["description"]
# NOTE WHEN I TRIED TO REDIRECT THIS TO FILE I RAN INTO AN ASCII ENCODING ERROR. SINCE PRINTED WELL IN TEMRINAL, I COPIED FROM THERE. (MY TRY AT WHAT ALLOWED ME TO FIX ENCODING TO UTF-8 BEFORE DIN'T WORK HERE.)
