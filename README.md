YeastMine
=========

* Scripts using [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) (populated by [SGD](www.yeastgenome.org/) and powered by [InterMine](http://intermine.github.io/intermine.org/)) to collect [Saccharomyces Genome Database](www.yeastgenome.org/) data.

* Running these scripts does require InterMine Python Web Service Client module be installed on the system. See notes on installing the InterMine Python Web Service Client Module.

* These scripts will work on free [PythonAnywhere](https://www.pythonanywhere.com/) accounts because InterMine and YeastMine were graciously added to the [Whitelisted sites for free users](https://www.pythonanywhere.com/whitelist/) when I requested. THANKS, PythonAnywhere! See nothes on installing the InterMine Python Web Service Client Module on PythonAnywhere below.

* Of course, they will also work on your computer, server, or cloud instance or wherever you run Python programs that can access the internet. (On [SourceLair](https://www.sourcelair.com) `easy_install intermine  ` didn't work for adding the InterMine module, `pip install intermine` did work to install the InterMine module though; however, the company has now switched their business model to not include free accounts.)





Installation of InterMine Python Web Service Client Module
----------------------------------------------------------

As described at [here](http://yeastmine.yeastgenome.org/yeastmine/api.do?subtab=python) you intstall the module on your system by

    $ easy_install intermine

(Dollar sign is used to indicate prompt. Don’t include that in your command.)  
You may need to do that as a superuser, i.e. include `sudo` at the start of that command, depending on how your system is set up.


If you are choosing to use a [PythonAnywhere](https://www.pythonanywhere.com/) account, you still need to install the InterMine Python Web Service Client Module to your individual account. It is done very similarly. You just need to additionally pass the user flag ‘--user ', as described [here](https://www.pythonanywhere.com/wiki/InstallingNewModules).
 
    $ easy_install --user intermine


On [SourceLair](https://www.sourcelair.com) that while `easy_install intermine  ` didn't work, `pip install intermine` did work to install the InterMine module.


Running the scripts
------------------
Add the script to your current directory and issue a command to tell python to run it.
Typically,

    python scriptname.py


For example,

    python protein_sizes_sorted.py

You'll probably want to direct the output to a file.

    python scriptname.py > output_filename.txt


Find more information on general installing and running InterMine [here](http://yeastmine.yeastgenome.org/yeastmine/api.do?subtab=python). 

Descriptions of the Scripts
---------------------------

- counting_amino_acid_residues_in_all_yeast_proteins.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces a file containing a sorted table of the counts and percent of occurences of amino acid residues in all the yeast proteins. The table is sorted in decreasing order with the most abundant amino acids at the top. The table can easily be pasted into or opened in Excel or Google Spreadsheets as it is tab-separated values (`tsv`) document. The way the code is arranged you can easily substitute the part that accesses YeastMine to specify your own subset list of proteins to analyze for amino acid content.

---

- residue_clustering_determinator_ALL_proteins.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces a file containing a sorted table of the density and clustering of certain amino acids.  The tables are sorted in decreasing order with the best scores for density/clustering at the top. The tables produced can easily be pasted into or opened in Excel or Google Spreadsheets as it is tab-separated values (`tsv`) document. The way the code is arranged you can easily substitute the part that accesses YeastMine to specify your own subset list of proteins to analyze for amino acid clustering.

---

- residue_density_plotting_to_gbrowse_custom_track.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces two files that can be uploaded to SGD's Gbrowse to produces tracks with residue density plotted. Combining all into one seems to bee to many points along the chromosomes for the format being used to handle, and so there are two file made and both need to be uploaded. If you alter code to handle your own subset and have less than 4000 genes/loci, you will only get one file to upload.

---

- finding_genes_in_list_with_SGD_Systematic_Name.py

> Takes a list of genes provided in the long SGD systematic name form and collects more user friendly version of name and information for each gene from YeastMine. It is suggested on the command line you redirect the output to a file yourself. Or adapt it to meet your needs.

---

- all_genes_and_flanking_sequences.py

> Uses YeastMine to fetch genomic regions (gene + 1kb upstream and downstream) for all yeast genes. This script doesn't produce a named file. It is suggested on the command line you direct the output to a file yourself. For example when running, `python all_genes_and_flanking_sequences.py > all_genomic_regions.txt'. Or adapt it to meet your needs.

---

- gene_with_flanking_sequences.py

> Uses YeastMine to fetch genomic region (gene + 1kb upstream and downstream) for a yeast genes. This script doesn't produce a named file. It is suggested on the command line you direct the output to a file yourself. For example when running, `python gene_with_flanking_sequences.py > POP1_genomic_region.txt'. Or adapt it to meet your needs. The example is written to use POP1 but you can edit it to your gene.

---

- geneID_list_to_systematic_names.py

> Standard Name --> Systematic Name  
The script takes a list of yeast gene identifiers and changes them to be systematic names if it recognizes the standard name. It just adds the name to the new list if it doesn't match a systematic name.  
Originally designed to adjust a gene list generated as output by Tophat to be useful for [T-profiler](http://www.t-profiler.org/index.html). As described [here](http://www.t-profiler.org/Saccharomyces/add_info/howtoupload.html), [T-profiler](http://www.t-profiler.org/index.html) wants the systematic ORF names at T-profiler.  
Note that T-profiler seemed to not accept data uploads May 2016, and [g:Profiler](http://biit.cs.ut.ee/gprofiler/), that is listed among T-profiler alternatives according to [GGSAASeqSP paper](http://www.nature.com/articles/srep06347), has functioning conversion ability built in for yeast gene lists.  
Even given the conversion function of [g:Profiler](http://biit.cs.ut.ee/gprofiler/) you may wish to run this script first to clean up the list to make less work for yourself in the long run, especially if the data set is larger. [g:Profiler](http://biit.cs.ut.ee/gprofiler/) that is listed among T-profiler alternatives in [the GGSAASeqSP paper](http://www.nature.com/articles/srep06347), reported a few ambiguities came up from the data converted using this script. [g:Profiler](http://biit.cs.ut.ee/gprofiler/) gives you the option to resolve them manually and all such ambiguities are easily resolved. You just need to pick best match; match is obvious in all cases. For example from one list of 80 genes converted, only the genes `YLR154C-H` and `YNR073C` still elicted `Warning: Some gene identifiers are ambiguous. Resolve these manually?`, but these seem to be due to the fact these genes have paralogs and come up in the description of two genes. However, if one uses an unconverted version of the data from DESeq2, you'll have double the amoung of ambiguities to resolve.  
To get only a list of gene IDs, like g:Profiler uses, you can easily discard the second column, i.e. log2 ratio, from the results of the script. One way to do that is with the `cut` command on the command line (Bash) like so, `cut -f1 INPUT_FILE > OUTPUT_FILE`.   Alternatively, you can use Excel to delete the column and then save the data elsewhere.

---

- protein_sizes_sorted.py

> Uses YeastMine to sort yeast proteins based on size. This script doesn't produce a named file. It is suggested on the command line you redirect the output to a file yourself. (There was an issue with this ---> see last comment in script.) Or adapt it to meet your needs.

Related scripts
---------------

Several other of my code repositories hold code related to the use of YeastMine. Here are some:

- [My text-mining/text manipulation code repository](https://github.com/fomightez/text_mining) has several useful scripts.  
In particular the `find_overlap_in_lists.py` script and related `find_overlap_in_lists_with_Venn.py` are particularly useful with gene lists that YeastMine can produce.


Additional Info
----------------

Find out more about YeastMine and InterMine [here](http://yeastmine.yeastgenome.org/yeastmine/begin.do) and [here](http://intermine.github.io/intermine.org/), respectively.

You can also make your own custom [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) queries at the [site](http://yeastmine.yeastgenome.org/yeastmine/begin.do) by starting with the numerous provided `Templates`. You can even run them right there. Start with the templates by accesing `Templates` from the navigation bar torwards the top of InterMine's portal and then you can edit the templates them by choosing `Edit Query` button to access the Query builder interface. Now you have an option to run the query right there at the YeastMine site by pressing `Show results`.  
Or if you want the Python code to run that query integrated into your workflow or to further adapt, you then access the code by clicking on the `Python` link down at the bottom middle once you have your built Query. You can edit them further after using Python coding as well.

If you just want a `.gff` file for the whole Saccharomyces cerevisiae genome, as of March 2016, go the [yeast genome site](http://www.yeastgenome.org/) and toggle the menu under `Sequence` on the purple navigation bar and choose `Download` at the top of menu and it will bring you to [the page](http://www.yeastgenome.org/download-data/sequence). `saccharomyces_cerevisiae.gff` will be listed in the top section. Alternatively, on the the [yeast genome site](http://www.yeastgenome.org/) look for bold `Download` in upper right corner above the `Search` field and click on it. Use the left panel that comes up on the page to select `Sequence` from below the red `Download` text.
