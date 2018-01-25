Evaluation
==========

The scripts in this folder are for comparing the results of output from certain scripts in order to evaluate the script realtive to another.

Sometines you'll produce related information by different means and you may find that you want to compare the results produced in a manner that is more advanced than using the built-in Unix `diff`command. These scripts address that. They are here because the use of YeastMine is commonly a route to producing output that is easier to compare with computer-assistance.



Descriptions of the Scripts
---------------------------

- compare_results_systematic_to_std.py

> Takes two output files where a gene list was converted to standard (common) gene names, each by a different method and details the differences. It is being written with the idea it would compare results of using YeastMine as the source of gene data to results of using a gtf file as the source.  
As written, by default the comparison is case-insensitive.

> This script goes beyond the `diff` built in to unix, and highlights only the differences that meet certain conditions.


---


