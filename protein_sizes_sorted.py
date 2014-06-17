#!/usr/bin/env python

# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://www.intermine.org/wiki/PythonClient

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

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
