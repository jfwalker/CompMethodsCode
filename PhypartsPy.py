'''
Program to get tree length, concordance or whatever
'''
import sys, tree_utils
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

def postorder2(root):
	
	cutoff = 0
	total_array = []
	for i in root.children:
		#part has children so grab'em
		if i.children:
			#checks internal labels
			bipart = []
			bipart.append(str(i.length))
			bipart.append(str(i.label))
			postorder3(i,bipart)
			print "Clade: " + str(bipart)
			total_array.append(bipart)
			#if i.label:

		#else:
		#	print i.label
				
		postorder2(i)
	return total_array

'''
Compare the bipartitions
'''
def comp_biparts(tree1,tree2):
	print "HERE"

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python " + sys.argv[0] + " treefile1"+ " treefile2"
		sys.exit(0)
	
	'''
	Hardcoded 0 as a cutoff
	'''
	tree1_biparts = []
	tree2_biparts = []
	cutoff = 0
	t1 = open(sys.argv[1],"r")
	for i in t1:
		n1 = i
	tree1 = build(n1)
	postorder2(tree1)
	t2 = open(sys.argv[2],"r")
	for i in t2:
		n2 = i
	tree2 = build(n2)
	postorder2(tree2)
	
	comp_biparts(tree2,tree2)

