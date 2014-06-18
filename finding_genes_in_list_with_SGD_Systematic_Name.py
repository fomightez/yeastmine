#!/usr/bin/env python

# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://www.intermine.org/wiki/PythonClient



list_to_get_info_for = ["YAL030W", "YAL003W", "YAL001C", "YBL111C", "YBL092W", "YBL087C", "YBL072C", "YBL059C-A", "YBL050W", "YBL040C", "YBL027W", "YBL026W", "YBL018C", "YBR048W", "YBR062C", "YBR078W", "YBR082C", "YBR084C-A", "YBR089C-A", "YBR111W-A", "YBR119W", "YBR181C", "YBR189W", "YBR191W", "YBR215W", "YBR255C-A", "YCL012C", "YCL002C", "YCR031C", "YCR097W", "YDL191W", "YDL136W", "YDL130W", "YDL115C", "YDL108W", "YDL083C", "YDL075W", "YDL061C", "YDL029W", "YDL012C", "YDR005C", "YDR025W", "YDR064W", "YDR092W", "YDR129C", "YDR139C", "YDR397C", "YDR424C", "YDR424C", "YDR447C", "YDR450W", "YDR471W", "YDR500C", "YEL076C-A", "YEL012W", "YEL003W", "YER056C-A", "YER074W", "YER074W-A", "YER093C-A", "YER102W", "YER117W", "YER133W", "YFL034C-A", "YFR024C-A", "YFR031C-A", "YFR032C-A", "YGL232W", "YGL226C-A", "YGL189C", "YGL178W", "YGL137W", "YGL103W", "YGL087C", "YGL076C", "YGL076C", "YGL031C", "YGL030W", "YGR001C", "YGR001C", "YGR027C", "YGR034W", "YGR118W", "YGR148C", "YGR214W", "YHL050C", "YHL001W", "YHR001W-A", "YHR010W", "YHR016C", "YHR021C", "YHR076W", "YHR077C", "YHR097C", "YHR101C", "YHR199C-A", "YHR203C", "YIL177C", "YIL156W-B", "YIL133C", "YIL123W", "YIL106W", "YIL069C", "YIL052C", "YIL018W", "YJL225C", "YJL205C", "YJL191W", "YJL177W", "YJL136C", "YJL130C", "YJL001W", "YJR021C", "YJR145C", "YKL190W", "YKL186C", "YKL180W", "YKL157W", "YKL156W", "YKL150W", "YKL081W", "YKL006W", "YKL002W", "YKR004C", "YKR057W", "YKR094C", "YKR095W-A", "YLL067C", "YLL066C", "YLR048W", "YLR061W", "YLR093C", "YLR185W", "YLR287C-A", "YLR306W", "YLR316C", "YLR316C", "YLR329W", "YLR344W", "YLR367W", "YLR367W", "YLR388W", "YLR406C", "YLR426W", "YLR448W", "YLR464W", "YML133C", "YML124C", "YML094W", "YML073C", "YML056C", "YML034W", "YML026C", "YMR033W", "YMR079W", "YMR116C", "YMR125W", "YMR133W", "YMR142C", "YMR143W", "YMR194W", "YMR201C", "YMR225C", "YMR230W", "YNL302C", "YNL301C", "YNL265C", "YNL246W", "YNL162W", "YNL147W", "YNL112W", "YNL096C", "YNL069C", "YNL038W", "YNL012W", "YNL004W", "YOL127W", "YOL121C", "YOL120C", "YOL048C", "YOR096W", "YOR122C", "YOR182C", "YOR234C", "YOR293W", "YOR312C", "YPL249C-A", "YPL218W", "YPL198W", "YPL175W", "YPL143W", "YPL129W", "YPL109C", "YPL090C", "YPL081W", "YPL079W", "YPL075W", "YPL031C", "YPR028W", "YPR043W", "YPR063C", "YPR098C", "YPR132W", "YPR170W-B", "YPR187W", "YPR202W"]

#OPTIONAL - SEE BELOW
#my_favorite_genes = ["NMD2", "MUD1", "TAN1"]

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view(
    "primaryIdentifier", "secondaryIdentifier", "symbol", "name",
    "organism.shortName", "proteins.symbol",  "sgdAlias", "featureType", "description"
)

# This query's custom sort order is specified below:
query.add_sort_order("Gene.secondaryIdentifier", "ASC")


print "primaryIdentifier\tsecondaryIdentifier\tsymbol\tname\torganism.shortName\tproteins.symbol\tsgdAlias\tfeatureType\tdescription"


for row in query.rows():
	if row["secondaryIdentifier"] in list_to_get_info_for:
	#LIST OF FAVORITE GENES AND ADD AN 'AND' CONDITION TO ABOVE LINE TO LIMIT TO YOUR FAV GENES
	#if (row["secondaryIdentifier"] in list_to_get_info_for) & (row["symbol"] in my_favorite_genes):
	    print row["primaryIdentifier"], row["secondaryIdentifier"], row["symbol"], row["name"], \
	        row["organism.shortName"], row["proteins.symbol"], row["sgdAlias"], row["featureType"], \
	         row["description"]
