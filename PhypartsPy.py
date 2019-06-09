'''
Program to get tree length, concordance or whatever
'''
import sys
from node import Node
 
#This takes in the newick and the
#seq data then puts them in a data
#structure that can be preorder or
#postorder traversed pretty easily
def build(instr):
	#print "Entered build"
	root = None
	index = 0
	nextchar = instr[index]
	begining = "Yep"
	keepgoing = True
	current_node = None
	#keeps going until the value becomes false
	while keepgoing == True:
		#This situation will only happen at the very beginning but
		#when it hits this it will create a root and change begining
		#to no
		if nextchar == "(" and begining == "Yep":
				
			root = Node()
			current_node = root
			begining = "No"
		#This happens anytime their is an open bracket thats not the
		#beginning
		elif nextchar == "(" and begining == "No":
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
		#This indicates that you are in a clade and tells the 
		#program to move back one to grab the sister to the clade
		elif nextchar == ',':
		
			current_node = current_node.parent
		#This says you are closing a clade and therefore it moves
		#back to where the parent node is which allows the name
		#to be added to the parent node
		elif nextchar == ")":
			#print "Closing Clade"
			current_node = current_node.parent
			index += 1
			nextchar = instr[index]
			while True:
			
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			index -= 1
		#This indicates everything is done so keepgoing becomes false
		elif nextchar == ';':
		
			keepgoing = False
			break
		#This indicates you have branch lengths so it grabs the branch
		#lengths turns them into floats and puts them in the current node
		elif nextchar == ":":
			index += 1
			nextchar = instr[index]
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				branch += nextchar
				index += 1
				nextchar = instr[index]
			current_node.length = float(branch)
			index -= 1
		#This is for if anywhitespace exists
		elif nextchar == ' ':
		
			index += 1
			nextchar = instr[index]
		#This is for when any taxa name is hit, it will concatenate
		#the taxa names together and add the name
		else: # this is an external named node
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
			current_node.istip = True
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			index -= 1
		if index < len(instr) - 1:
			index += 1
		nextchar = instr[index]
		name = ""
		branch = ""
	return root


def postorder3(root,bipart):
	for i in root.children:
		if i.istip:
			bipart.append(i.label)
	
		postorder3(i,bipart)

def postorder2(root,total_array):
	
	cutoff = 0
	for i in root.children:
		#part has children so grab'em
		if i.children:
			#checks internal labels
			#if i.label
			bipart = []
			bipart.append(str(i.length))
			bipart.append(str(i.label))
			postorder3(i,bipart)
			#print "Clade: " + str(bipart)
			total_array.append(bipart)
			#if i.label:

		#else:
		#	print i.label
			
		postorder2(i,total_array)
	return total_array

def unique_array(array,tree1,tree2):
	all_species = set()
	for x in array:
		all_species.add(x)
	mis1 = list(set(all_species) - set(tree1))
	mis2 = list(set(all_species) - set(tree2))
	return mis1,mis2

'''
How do the biparts relate
'''
def bipart_properties(bp1,bp2):
	
	keepgoing = "false"
	#difference in the biparts
	diff1 = list(set(bp1) - set(bp2))
	diff2 = list(set(bp2) - set(bp1))

	print "bipart 1: " + str(bp1)
	print "bipart 2: " + str(bp2)
	print diff1
	print diff2
	#check for no overlp
	if len(bp1) == 1 or len(bp2) == 1:
		print "uninformative"
	elif len(diff1) == len(bp1):
		print "no comp"
	#check if nested
	elif len(bp1) == len(bp2) and len(diff1) == 0:
		print "identical"
	elif len(diff1) == 0:
		print "nested in 2"
	elif len(diff2) == 0:
		print "nested in 1"
	else:
		print "conflict"

	
		


'''
Compare the bipartitions
'''
def comp_biparts(tree1,tree2):
	
	all_names = []
	test_bp1 = []
	test_bp2 = []
	rel = 0
	all_species = set()
	'''
	first two columns of the tree should be names
	'''
	all_names = tree1[0][2:] + tree2[0][2:]
	# get the names, for missing taxa check etc.
	mis1,mis2 = unique_array(all_names,tree1[0][2:],tree2[0][2:])
	for i in tree1:
		for j in tree2:
			#i is bipart from tree1 (species tree), check for concordance
			#unable to speak to, and conflict for everything in tree2
			#remove stuff that's not going to be found first
			
			test_bp1 = list(set(i[2:]) - set(mis2))
			test_bp2 = list(set(j[2:]) - set(mis1))
			
			rel = bipart_properties(test_bp1,test_bp2)
	
	
	

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python " + sys.argv[0] + " treefile1"+ " treefile2"
		sys.exit(0)
	
	'''
	Hardcoded 0 as a cutoff
	'''
	tree1_biparts = []
	tree2_biparts = []
	total_array = []
	cutoff = 0
	t1 = open(sys.argv[1],"r")
	for i in t1:
		n1 = i
	tree1 = build(n1)
	tree1_biparts = postorder2(tree1, total_array)
	t2 = open(sys.argv[2],"r")
	for i in t2:
		n2 = i
	tree2 = build(n2)
	total_array = []
	tree2_biparts = postorder2(tree2, total_array)
	
	comp_biparts(tree1_biparts,tree2_biparts)

