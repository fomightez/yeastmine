YeastMine
=========

* Scripts using [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) (populated by [SGD](www.yeastgenome.org/) and powered by [InterMine](http://intermine.github.io/intermine.org/)) to collect [Saccharomyces Genome Database](www.yeastgenome.org/) data.

* Running these scripts does require InterMine Python Web Service Client module be installed on the system. See notes on installing the InterMine Python Web Service Client Module.

* **THERE IS AN ISSUE RIGHT NOW (EARLY 2018) PREVENTING THESE FROM WORKING ON FREE ACCOUNTS, see below.**  These scripts will work on free [PythonAnywhere](https://www.pythonanywhere.com/) accounts because InterMine and YeastMine were graciously added to the [Whitelisted sites for free users](https://www.pythonanywhere.com/whitelist/) when I requested. ***Thanks, PythonAnywhere!*** See [notes on installing](#installation-of-intermine-python-web-service-client-module) the InterMine Python Web Service Client Module on PythonAnywhere below.

* Of course, they will also work on your computer, server, or cloud instance or wherever you run Python programs that can access the internet. (On [SourceLair](https://www.sourcelair.com) `easy_install intermine  ` didn't work for adding the InterMine module, `pip install intermine` did work to install the InterMine module though; however, the company has now switched their business model to not include free accounts.)





Installation of InterMine Python Web Service Client Module
----------------------------------------------------------

As described at [here](http://yeastmine.yeastgenome.org/yeastmine/api.do?subtab=python) you intstall the module on your system by

    $ easy_install intermine

(Dollar sign is used to indicate prompt. Don’t include that in your command.)  
You may need to do that as a superuser, i.e. include `sudo` at the start of that command, depending on how your system is set up.


If you are choosing to use a [PythonAnywhere](https://www.pythonanywhere.com/) account, you still need to install the InterMine Python Web Service Client Module to your individual account. It is done very similarly. You just need to additionally pass the user flag `--user `, as shown below and described [here](https://www.pythonanywhere.com/wiki/InstallingNewModules).
 
    $ easy_install --user intermine

**PRESENTLY ON PYTHON ANYWHERE IN EARLY 2018 I AM UNABLE TO USE YeastMine.**
Present details:

* I looked at YeastMine presently and saw the current link to the site uses https and so I tried changing the address in my script to what is shown in samples, i.e., script obtained from going to https://yeastmine.yeastgenome.org/yeastmine/template.do?name=Gene_Transcript&scope=all and clicking link down below for `python` to open https://yeastmine.yeastgenome.org/yeastmine/templateAction.do .
	
* Ran updgrade of intermine with `python genes_ieasy_install --user --upgrade intermine`
	
* Still get Squid error running the sample script fro PythonAnywhere. Think it is related to fact for free PythonAnywhere accounts that things run through a proxy and the current `requests` package is broken for that, see https://www.pythonanywhere.com/forums/topic/761/ . That package is probably used in the intermine access or somethhing broken is. Since it is an overarching thing at the level of the popular requests package/https switch everyone is doing, maybe best to not try and make work from PythonAnywhere until the dust settles, since I think YeastMine may be working on my local Mac desktop for now. I'll just use that in the interim.

**ANOTHER FREE OPTION WHILE FREE ACCOUNTS ON PYTHONANYWHERE AND YEASTMINE SEEM TO NOT BE PLAYING NICE**  
I found I could launch versions of Jupyter notebooks served via the FREE Binder service, for example by pressing `launch binder` at https://github.com/fomightez/qgrid-notebooks, and start a Python 3 notebook that I could then install intermine into by pasting `!pip install intermine` into a cell and running and then yeastmine works. I could see it worked by pasting in and running the script obtained from going to https://yeastmine.yeastgenome.org/yeastmine/template.do?name=Gene_Transcript&scope=all and clicking link down below for `python` to open https://yeastmine.yeastgenome.org/yeastmine/templateAction.do . (I probably should put examples of that script and some of mine in a repo where I pre-install `intermine` and link to it from here.)

While they are no longer opening a free account, on [SourceLair](https://www.sourcelair.com), while `easy_install intermine  ` didn't work, `pip install intermine` did work to install the InterMine module.


Running the scripts
------------------
Add the script to your current directory and issue a command to tell python to run it.
Typically,

    python scriptname.py


For example,

    python protein_sizes_sorted.py

For the few scripts that don't make an output file automatically, you'll probably want to direct the output to a file.

    python scriptname.py > output_filename.txt


Find more information on general installing and running InterMine [here](http://yeastmine.yeastgenome.org/yeastmine/api.do?subtab=python). 

Descriptions of the Scripts
---------------------------

- get_protein_seq_as_FASTA.py

> gene --> corresponding protein sequence in FASTA format  
The script taakes a gene's systematic name, standard name, or alias as defined at gene page at yeastgenome.org, retrieves the associated information from YeastMine, and saves or returns the protein sequence in FASTA format. It depends on biopython installed as well; it will run in Jupyter sessions launched from [here](https://github.com/fomightez/cl_demo-binder).

---

- counting_amino_acid_residues_in_all_yeast_proteins.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces a file containing a sorted table of the counts and percent of occurences of amino acid residues in all the yeast proteins. The table is sorted in decreasing order with the most abundant amino acids at the top. The table can easily be pasted into or opened in Excel or Google Spreadsheets as it is tab-separated values (`tsv`) document. The way the code is arranged you can easily substitute the part that accesses YeastMine to specify your own subset list of proteins to analyze for amino acid content.

---

- residue_clustering_determinator_ALL_proteins.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces a file containing a sorted table of the density and clustering of certain amino acids.  The tables are sorted in decreasing order with the best scores for density/clustering at the top. The tables produced can easily be pasted into or opened in Excel or Google Spreadsheets as it is tab-separated values (`tsv`) document.  
The way the code is arranged you can easily substitute the part that accesses YeastMine to specify your own subset list of proteins to analyze for amino acid clustering.

---

- residue_density_plotting_to_gbrowse_custom_track.py

> Uses YeastMine to fetch information on all verfied proteins (currently 5917 mid-2015) and produces two files that can be uploaded to SGD's Gbrowse to produces tracks with residue density plotted. Combining all into one seems to be too many points along the chromosomes for the format being used to handle, and so there are two file made and both need to be uploaded. If you alter code to handle your own subset and have less than 4000 genes/loci, you will only get one file to upload.

---

- make_simulated_yeast_gene_set.py

> number --> random list with that number of yeast genes  
The script makes a simulated yeast gene set of user-determined size and saves a file of the generated gene list. The gene identifiers in the produced list are the SGD systematic names. The gene list file has each systematic ID on an individual line.
	
**Usage**

	usage: make_simulated_yeast_gene_set.py  [-h] Number  
	
	make_simulated_yeast_gene_set.py Makes a simulated yeast gene set of user-
	determined size and saves a file of the gene list using the SGD's systematic
	IDs, each on individual lines. **** Script by Wayne Decatur (fomightez @
	github) ***  
	
	positional arguments:
	  Number      Number of genes to have in the produced gene set.  
	  
	optional arguments:
	  -h, --help  show this help message and exit
---

- genes_in_list_with_SGD_Systematic_Name_to_standard_name.py

>  Systematic Name --> Standard ("common") Name  
Takes a list of genes provided in the SGD systematic name form and collects and produces as output the Standard Name at SGD (a.k.a. common name).  
Importantly, the information in the output file is in the same order as the input list, unlike `finding_genes_in_list_with_SGD_Systematic_Name.py`.  
The list has to have to have the gene identifiers at the start of each line. There can be other text on the line as long as the additional text is separated by space or tabs from the other identifier data at the start of the line. (It would be a simple edit from `line_list = line.split()` to `line_list = line.split(',')` in order to convert this script to work for comma-separated values on each line.)  
The produced output will place the additional content on any line after the identifier.    
While the default is to only send the standard (common) gene name to the output, the addition of the optional flag `--both_orf_std`  to the command call will make the information sent the output list be the systematic name followed by a tab and then the standard name. This will be convenient for use in text editors or Excel.  
While the default is to only send the standard (common) gene name to the output, the addition of the optional flag `--details` to the command call will expand the information sent to the output list beyond the standard name to a full list of details about the yeast gene. This will quickly allow one an overview of the gene information for many genes without use of SGD in a browser. The details printed on each line follow this order: primaryIdentifier, secondaryIdentifier, symbol, name, sgdAlias, featureType, and description.  

> A related script that employs a gtf file, which is common for many Cufflinks-related pipelines, in order to convert systematic names to yeast standard (common) gene names is available, see `systematic_names_to_standard_names_using_cufflinks_gtf.py` in the [Adjust_lists repository](https://github.com/fomightez/sequencework/tree/master/Adjust_lists). A script to aid in comparing results between the two, called `compare_results_systematic_to_std.py`, is found in the `Evaluation` subdirectory in this repository.

**Usage**

```
usage: genes_in_list_with_SGD_Systematic_Name_to_standard_name [-h] [-d] FILE

genes_in_list_with_SGD_Systematic_Name_to_standard_name.py uses data from
YeastMine to convert a list of systematic gene ids in a file to standard
(common) gene names, where they exist. The list should be gene ids each on a
separate line of the file. **** Script by Wayne Decatur (fomightez @ github)
***

positional arguments:
  FILE           Name of file containing `systematic ids` list to convert.
                 REQUIRED.

optional arguments:
  -h, --help     show this help message and exit  
  -b, --both_orf_std  add this flag to have produce an output file with both
                      the systematic name and the standard name. The output
                      file produced have the systematic name followed by the
                      the standard name with a tab in between for conveinence
                      in using in your favorite text editor or Microsfot
                      Excel.  
  -d, --details       add this flag to have the output file have an expanded
                      set of information about the gene in place of the
                      systematic id. The information will include a
                      description in addition to the standard name.

```



#### example of input and default output for `genes_in_list_with_SGD_Systematic_Name_to_standard_name.py`:

sample of original input `gene_list.txt`:
```
YJL074C
YNL088W
YPR168W	1.03
Q0250   ipsum_lorem_de_facotoris_du_mondi ahdjs ahsjshs s sjjsjsjs
```

**command:**

    python genes_in_list_with_SGD_Systematic_Name_to_standard_name.py gene_list.txt

**output after run:**
(text in a file, called `gene_list_converted_to_std_id.txt`, with the contents below)
```
SMC3
TOP2
NUT2 1.03
COX2 ipsum_lorem_de_facotoris_du_mondi ahdjs ahsjshs s sjjsjsjs
```

#### example of input and output for `genes_in_list_with_SGD_Systematic_Name_to_standard_name.py` with `--both_orf_std` flag:


sample of original input `gene_list.txt`:
```
YJL074C
YNL088W
YPR168W
Q0250
```


**command:**

    python genes_in_list_with_SGD_Systematic_Name_to_standard_name.py gene_list.txt --both_orf_std

**output after run:**
(text in a file, called `gene_list_converted_to_std_id.txt`, with the contents below)
```
YJL074C	SMC3
YNL088W TOP2
YPR168W	NUT2
Q0250	COX2
```

#### example of input and output for `genes_in_list_with_SGD_Systematic_Name_to_standard_name.py` with `--details` flag:


sample of original input `gene_list.txt`:
```
YJL074C
YNL088W
YPR168W
Q0250
```


**command:**

    python genes_in_list_with_SGD_Systematic_Name_to_standard_name.py gene_list.txt --details

**output after run:**
(text in a file, called `gene_list_converted_to_std_id.txt`, with the contents below)
```
S000003610 YJL074C SMC3 Stability of MiniChromosomes cohesin subunit SMC3 ORF Subunit of the multiprotein cohesin complex; required for sister chromatid cohesion in mitotic cells; also required, with Rec8p, for cohesion and recombination during meiosis; phylogenetically conserved SMC chromosomal ATPase family member
S000005032 YNL088W TOP2 TOPoisomerase TOR3 TRF3 DNA topoisomerase 2 ORF Topoisomerase II; relieves torsional strain in DNA by cleaving and re-sealing phosphodiester backbone of both positively and negatively supercoiled DNA; cleaves complementary strands; localizes to axial cores in meiosis; required for replication slow zone (RSZ) breakage following Mec1p inactivation; human homolog TOP2A implicated in cancers, and can complement yeast null mutant
S000006372 YPR168W NUT2 Negative regulation of URS Two MED10 mediator complex subunit NUT2 ORF Subunit of the RNA polymerase II mediator complex; associates with core polymerase subunits to form the RNA polymerase II holoenzyme; required for transcriptional activation and has a role in basal transcription; protein abundance increases in response to DNA replication stress
S000007281 Q0250 COX2 Cytochrome c OXidase OXI1 OXII cytochrome c oxidase subunit 2 ORF Subunit II of cytochrome c oxidase (Complex IV); Complex IV is the terminal member of the mitochondrial inner membrane electron transport chain; one of three mitochondrially-encoded subunits

```



---

- geneID_list_to_systematic_names.py

> Standard Name --> Systematic Name  
The script takes a list of yeast gene identifiers and changes them to be systematic names if it recognizes the standard name. It just adds the name to the new list if it doesn't match a systematic name. A file of the new information is produced.  
The list has to have to have the gene identifiers at the start of each line. There can be other text on the line as long as the additional text is separated by space or tabs from the identifier data at the start of the line. (It would be a simple edit from `line_list = line.split()` to `line_list = line.split(',')` in order to convert this script to work for comma-separated values on each line.) 
The produced output will place the additional content on any line after the identifier after a tab. (Change the `"\t"` on line 255 to read `", "` to change the output to also be csv.)  
Originally designed to adjust a gene list generated as output by Tophat to be useful for [T-profiler](http://www.t-profiler.org/index.html). As described [here](http://www.t-profiler.org/Saccharomyces/add_info/howtoupload.html), [T-profiler](http://www.t-profiler.org/index.html) wants the systematic ORF names at T-profiler. And it wants it with the fold change so there was the identifier and log2 ratio on each line of the list.  
Note that T-profiler seemed to not accept data uploads May 2016, and [g:Profiler](http://biit.cs.ut.ee/gprofiler/), that is listed among T-profiler alternatives according to [GGSAASeqSP paper](http://www.nature.com/articles/srep06347), has functioning conversion ability built in for yeast gene lists.  
Even given the conversion function of [g:Profiler](http://biit.cs.ut.ee/gprofiler/) you may wish to run this script first to clean up the list to make less work for yourself in the long run, especially if the data set is larger. [g:Profiler](http://biit.cs.ut.ee/gprofiler/) that is listed among T-profiler alternatives in [the GGSAASeqSP paper](http://www.nature.com/articles/srep06347), reported a few ambiguities came up from the data converted using this script. [g:Profiler](http://biit.cs.ut.ee/gprofiler/) gives you the option to resolve them manually and all such ambiguities are easily resolved. You just need to pick best match; match is obvious in all cases. For example from one list of 80 genes converted, only the genes `YLR154C-H` and `YNR073C` still elicted `Warning: Some gene identifiers are ambiguous. Resolve these manually?`, but these seem to be due to the fact these genes have paralogs and come up in the description of two genes. However, if one uses an unconverted version of the data from DESeq2, you'll have double the amoung of ambiguities to resolve.  
Assuming your original input had a second column, to get only a list of gene IDs, for use in g:Profiler uses, you can easily discard the second column, i.e. log2 ratio, from the results of the script. One way to do that is with the `cut` command on the command line (Bash) like so, `cut -f1 INPUT_FILE > OUTPUT_FILE`.   Alternatively, you can use Excel to delete the column and then save the data elsewhere.

#### example of input and output for `geneID_list_to_systematic_names.py`:

sample of original input in `culled_extracted_geneIDs_and_log2change.txt`:
```
SMC3
TOP2 
NUT2	1.03
COX2	ipsum_lorem_de_facotoris_du_mondi ahdjs ahsjshs s sjjsjsjs 
```
**command:**

    python geneID_list_to_systematic_names.py culled_extracted_geneIDs_and_log2change.txt

**output after run:**
(text in a file, called `culled_extracted_geneIDs_and_log2change_with_sys_id.txt`, with the contents below)
```
YJL074C	
YNL088W	
YPR168W	1.03
Q0250   ipsum_lorem_de_facotoris_du_mondi ahdjs ahsjshs s sjjsjsjs


```

---

- finding_genes_in_list_with_SGD_Systematic_Name.py

> Takes a list of genes provided in the SGD systematic name form and collects and produced as output information for each gene from YeastMine, that includes a more user friendly version of name, called the `Standard Name` at SGD (a.k.a. common name). It is suggested you redirect the output to a file yourself on the command line. Or adapt it to meet your needs.  
This script can be particulary useful after getting a lits of genes in the SGD systematic name form so that you can see if any are of interest because most people are more familiar with the Standard Names.  
THIS SCRIPT DOES NOT RETAIN ORDER OF THE INPUT LIST. Your are better off using the script `genes_in_list_with_SGD_Systematic_Name_to_standard_name.py` because that script will retain and match the input order. Additionally, that script has better abilities and is  more user-friendly as well. This script is only kept here as it allows one to designate a set of genes of interest so that the members of that list can be determined to be members of a provided gene list. This ability has not yet been built into the newer, better script `genes_in_list_with_SGD_Systematic_Name_to_standard_name.py`.

---

- all_genes_and_flanking_sequences.py

> Uses YeastMine to fetch genomic regions (gene + 1kb upstream and downstream) for all yeast genes. This script doesn't produce a named file. It is suggested you direct the output to a file yourself on the command line. For example when running, `python all_genes_and_flanking_sequences.py > all_genomic_regions.txt'. Or adapt it to meet your needs.

---

- gene_with_flanking_sequences.py

> Uses YeastMine to fetch genomic region (gene + 1kb upstream and downstream) for a yeast gene. This script doesn't produce a named file. It is suggested you direct the output to a file yourself on the command line. For example when running, `python gene_with_flanking_sequences.py > POP1_genomic_region.txt'. Or adapt it to meet your needs.  
The example is written to use POP1, but you can edit it to specify your gene.

---

- protein_sizes_sorted.py

> Uses YeastMine to sort yeast proteins based on size. This script doesn't produce a named file. It is suggested on the command line you redirect the output to a file yourself. (There was an issue with this ---> see last comment in script.) Or adapt it to meet your needs.

Related scripts
---------------

Several other of my code repositories hold code related to the use of YeastMine. Here are some:

- [My text-mining/text manipulation code repository](https://github.com/fomightez/text_mining) has several useful scripts.  
In particular the `find_overlap_in_lists.py` script and related `find_overlap_in_lists_with_Venn.py` are particularly useful with gene lists that YeastMine can produce.

- [My sequence work repository](https://github.com/fomightez/sequencework) has several useful scripts. Especially check the `Adjust_Annotation`, `ConvertSeq`, and `RetrieveSeq` sub-directories for scripts dealing with operations in line with the folder names.

- [My yeast snoRNAs repoitory](https://github.com/fomightez/yeast_snornas) has a script useful for examining lists of upregulated or downregulated genes and classifying snoRNA genes present and assessing enrichment.

Evaluation
----------

There is a sub-folder, called `Evaluation` in this one for comparing the results of output from certain scripts in order to evaluate the script realtive to another. As of now, this contains a script that goes beyond the `diff` built in to unix, and highlights only the differences that meet certain conditions.


Additional Info
----------------

Find out more about YeastMine and InterMine [here](http://yeastmine.yeastgenome.org/yeastmine/begin.do) and [here](http://intermine.github.io/intermine.org/), respectively.

You can also make your own custom [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) queries at the [site](http://yeastmine.yeastgenome.org/yeastmine/begin.do) by starting with the numerous provided `Templates`. You can even run them right there. Start with the templates by accesing `Templates` from the navigation bar torwards the top of InterMine's portal and then you can edit the templates them by choosing `Edit Query` button to access the Query builder interface. Now you have an option to run the query right there at the YeastMine site by pressing `Show results`.  
Or if you want the Python code to run that query integrated into your workflow or to further adapt, you then access the code by clicking on the `Python` link down at the bottom middle once you have your built Query. You can edit them further after using Python coding as well.

If you just want a `.gff` file for the whole Saccharomyces cerevisiae genome, as of March 2016, go the [yeast genome site](http://www.yeastgenome.org/) and toggle the menu under `Sequence` on the purple navigation bar and choose `Download` at the top of menu and it will bring you to [the page](http://www.yeastgenome.org/download-data/sequence). `saccharomyces_cerevisiae.gff` will be listed in the top section. Alternatively, on the the [yeast genome site](http://www.yeastgenome.org/) look for bold `Download` in upper right corner above the `Search` field and click on it. Use the left panel that comes up on the page to select `Sequence` from below the red `Download` text.

Related
------

- [2018 Newsletter (with 25th anniversay of SGD)](https://wiki.yeastgenome.org/index.php/SGD_Newsletter,_Fall_2018) pointed out,"SGD has a collection of python scripts which demonstrate how to access data from the SGD API".

	Looks like a few put up in August 2018 [here](https://github.com/yeastgenome/sgd_api_examples)

	Looking around also lead me to [SGD (yeastgenome) organization](https://github.com/yeastgenome).
