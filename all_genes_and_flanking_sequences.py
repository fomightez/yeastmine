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
    "secondaryIdentifier", "symbol", "length", "flankingRegions.direction",
    "flankingRegions.sequence.length", "flankingRegions.sequence.residues"
)

# Uncomment and edit the line below (the default) to select a custom sort order:
# query.add_sort_order("Gene.secondaryIdentifier", "ASC")

# You can edit the constraint values below
query.add_constraint("flankingRegions.direction", "=", "both", code = "C")
query.add_constraint("Gene", "LOOKUP", "*", "S. cerevisiae", code = "B")
query.add_constraint("flankingRegions.distance", "=", "1.0kb", code = "A")

# Uncomment and edit the code below to specify your own custom logic:
# query.set_logic("A and B and C")

for row in query.rows():
    print row["secondaryIdentifier"], row["symbol"], row["length"], \
        row["flankingRegions.direction"], row["flankingRegions.sequence.length"], \
        row["flankingRegions.sequence.residues"]
