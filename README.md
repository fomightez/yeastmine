YeastMine
=========

* Scripts using [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) (populated by [SGD](www.yeastgenome.org/) and powered by [InterMine](http://intermine.github.io/intermine.org/)) to collect [Saccharomyces Genome Database](www.yeastgenome.org/) data.

* These scripts will work on free [PythonAnywhere](https://www.pythonanywhere.com/) accounts because InterMine and YeastMine were graciously added to the [Whitelisted sites for free users](https://www.pythonanywhere.com/whitelist/) when I requested. THANKS, PythonAnywhere!  
Of course, they will also work on your computer, server, or cloud instance or wherever you run Python programs that can access the internet.


* Running them does require Intermine module be installed on system.


Installation of Intermine
-------------------------


Running the scripts
------------------
Add the script to your current directory and issue a command to tell python to run it.
Typically,

    python scriptname.py
   
You'll probably want to direct the output to a file.

    python scriptname.py > output_filename.txt


Additional Info
----------------

Find out more about YeastMine and InterMine [here](http://yeastmine.yeastgenome.org/yeastmine/begin.do) and [here](http://intermine.github.io/intermine.org/), respectively.

You can also make your own custom [YeastMine](http://yeastmine.yeastgenome.org/yeastmine/begin.do) queries at the [site](http://yeastmine.yeastgenome.org/yeastmine/begin.do) by starting with the numerous provided `Templates`. You can even run them right there. Start with the templates by accesing `Templates` from the navigation bar torwards the top of InterMine's portal and then you can edit the templates them by choosing `Edit Query` button to access the Query builder interface. Now you have an option to run the query right there at the YeastMine site by pressing `Show results`. Or if you want the Python code to run that query to integrate into your workflow or further adapt, you then access the code by clicking on the `Python` link down at the bottom middle once you have your built Query. You can edit them further after using Python coding as well.
