import sys
from node import Node

'''
Random code to make a vcv and multiply that times the alignment
Most code is modified from code by Stephen Smith
'''


def read_tree_string(instr):
	root = None
	names = []
	index = 0
	nextchar = instr[index]
	start = True
	keepgoing = True
	curnode = None
	while keepgoing == True:
		if nextchar == "(":
			if start == True:
				root = Node()
				curnode = root
				start = False
			else:
				newnode = Node()
				curnode.add_child(newnode)
				curnode = newnode
		elif nextchar == "[":
			note = ""
			index += 1
			nextchar = instr[index]
			while True:
				if nextchar == "]":
					break
				index += 1
				note += nextchar
				nextchar = instr[index]
			curnode.note = note
		elif nextchar == ',':
			curnode = curnode.parent
		elif nextchar == ")":
			curnode = curnode.parent
			index += 1
			nextchar = instr[index]
			name = ""
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				if index < len(instr)-1:
					index += 1
					nextchar = instr[index]
				else:
					keepgoing = False
					break
			curnode.label = name
			index -= 1
		elif nextchar == ';':
			keepgoing = False
			break
		elif nextchar == ":":
			index += 1
			nextchar = instr[index]
			brlen = ""
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				brlen += nextchar
				index += 1
				nextchar = instr[index]
			curnode.length = float(brlen)
			index -= 1
		elif nextchar == ' ':
			index += 1
			nextchar = instr[index]
		else: # this is an external named node
			newnode = Node()
			curnode.add_child(newnode)
			curnode = newnode
			curnode.istip = True
			name = ""
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			curnode.label = name
			names.append(name)
			index -= 1
		if index < len(instr) - 1:
			index += 1
		nextchar = instr[index]
	return root,names

def read_tree_file_iter(inf):
	array = []
	info = open(inf,"r")
	for i in info:
		yield read_tree_string(i.strip())
	info.close()

def mrca_recurs(node1,path1,node2):
    path = path1[path1.index(node1):]
    parent = node2
    mrca = None
    while parent != None:
        if parent in path:
            mrca = parent
            break
        parent = parent.parent
    return mrca

def get_mrca(nodes,tree):
    traceback = []
    first = nodes[0]
    while first != tree:
        first = first.parent
        traceback.append(first)
        if first.parent == None:
            break
    curmrca = nodes[0].parent
    for i in nodes:
        if i == nodes[0]:
            continue
        curmrca = mrca_recurs(curmrca,traceback,i)
    return curmrca


"""
this will calculate a variance covariance matrix 
for the species and output in an order that is 
the order for tree.leaves()
"""
def var_cov_matrix(tree):
	lvs = tree.leaves()
	ll = len(lvs)
	#zm = zeros((ll,ll))
	zm = [[0.0 for col in range(ll)] for row in range(ll)]
	for i in range(ll):
		for j in range(ll):
			curnode = None
			if i == j:
				curnode = lvs[i]
			elif j > i:
				curnode = get_mrca([lvs[i],lvs[j]],tree)
			else:
				continue
			count = 0
			while curnode != tree:
				count += curnode.length
				curnode = curnode.parent
			zm[i][j] = count
			zm[j][i] = count
	return zm

'''
Takes in tree file and length as integer
'''
def do_correction(info, l):
	
	names = []
	matrix = []
	matrix2 = []
	for i in info:
		t,names = read_tree_string(i)
	matrix = var_cov_matrix(t)
	for i in range(len(matrix)):
		matrix2 = []
		for j in matrix[i]:
			j *= l
			matrix2.append(j)
		print names[i].strip() + " " + str(matrix2)
	

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python " + sys.argv[0] + " treefile"+ " AlignmentLength"
		sys.exit(0)

	length = 0
	info = open(sys.argv[1],"r")
	length = sys.argv[2]
	l = int(length)
	do_correction(info, l)

