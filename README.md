# CompMethodsCode
Code for comparative methods stuff


### PhypartsPy.py
Named because I was originally writing a python version of phyparts but then deviated a little and didn't feel like changing the name. The program inputs are two trees you'd like to compare. Tree 1 is probably the species tree and tree two is the gene tree. The output is a "gene name".log file which contains all bipartition comparisons and how they relate to eachother, and a "gene name".txt file which contains a given bipartition from Tree1 and how it relates to a bipartition in Tree2. A single biparitition can have multiple conflicting bipartitions from another tree which is why multiple conflicts are reported (deviance from phyparts original), however, it only passes all of Tree2's biparts against Tree1's so that's why Tree1 has multiple conflicts against it reported.

EX: ```python PhypartsPy.py Tree1 Tree2```

The output for the log file is mainly to verify things worked ok, the output from the text file is likely the more useful one for downstream analysis. The text file is in tab delimited format as follows.

EX: ```Relationship_# Relationship_Info  How_it_relates_between_trees bipartition_from_tree1  bipartition_from_tree2  SupportValue  length_of_edge``` 


### vcv_correction.py
This got its name because it also deviated from what I was going to do with it, but that's another story. In short this breaks trees into their corresponding vcv's to analyze the total amount of evolutionary history shared between individuals. The program works where a species tree (or whatever as long as it is a tree) is given, this tree is simply used to order everything, then a set of gene trees, then a species of interest. What it does is break everything gene tree into their vcv and then transform each one to match the species tree, then depending on what species of interest you chose it will print out the evolutionary distance between that species and all others. This info is printed to a file called "species name".log. It prints a lot of stuff to the screen, such as how it manipulates the matrix to match others, but you can probably ignore all that and only look at the log.

EX: ```python vcv_correction.py Tree1 FileOftree(s) Species_of_interest```

The output will be all species as a header, and then each line after that will be evolutionary history shared.
