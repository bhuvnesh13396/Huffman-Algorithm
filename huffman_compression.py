#!/usr/local/bin/python
#
# Huffman Compression Algorithm 
# For compression of text data

# Created by bhuvi-->

###############################
##                           ##
## HUFFMAN DATA COMPRESSION  ##                    
##                           ##
###############################

import sys , string

codes = {}


def frequency(text):
	# Extracts frequency of each character and 
	# stores in a dictionary.

	freqs = {}
	for ch in text:
		freqs[ch] = freqs.get(ch,0) + 1

	return freqs

def sortFreq(freqs):
	# Sorts the frequency array 
	# [ (0,'q') , (1,'a') , (5,'e') ]
	letters = freqs.keys()
	tuples = []
	for let in letters:
		tuples.append(( freqs[let] , let))

	tuples.sort()
	return tuples


def buildTree(tuples):

	while len(tuples)>1:
		leastTwo = tuple(tuples[0:2])
		theRest = tuples[2:]

		# Branch point frequency
		combFreq = leastTwo[0][0] + leastTwo[1][0]

		# Add branch point to the end
		tuples = theRest + [(combFreq,leastTwo)]
		
		tuples.sort()

	return tuples[0]


def trimTree(tree):
	# Trim freq counterss off and leave letters only.

	p = tree[1]

	# if just a  leaf, return it
	if type(p) == type("") : return p

	else:
		# Trim left then right and then recombine
		return ( trimTree(p[0]) , trimTree(p[1]) )


def assignCodes(node,pat=''):
	global codes

	# A leaf set its code
	if type(node) == type(""):
		codes[node] = pat

	# Branch point.Do left branch
	# and then do right branch.
	else:
		assignCodes(node[0] , pat+"0")
		assignCodes(node[1] , pat+"1")


def encode(str):
	# Encode text into strings of 0's and 1's

	global codes
	output = ""
	for ch in str:
		output+=codes[ch]

	return output


def decode(tree,str):

	output = ""
	p = tree
	for bit in str:

		# Choose left branch
		if bit == '0':
			p = p[0]

		else:
		# Choose right branch
			p = p[1]

		# Found character.And to output
		# and restart for next character
		if type(p) == type(""):
			output += p
			p = tree	

	return output


def main():
	debug = None
	str = sys.stdin.read()
	freqs = frequency(str)
	tuples = sortFreq(freqs)

	tree = buildTree(tuples)
	if debug : print "Build tree", tree

	tree = trimTree(tree)
	if debug : print "Trimmed tree", tree

	assignCodes(tree)
	if debug : showCodes()

	small = encode(str)
	original = decode(tree,small)
	print "Original text length", len(str)
	print "Requires %d bits. (%d bytes)" % (len(small), (len(small)+7)/8)
	print "Restored matches original", str == original
	print "Code for space is ", codes[' ']
	print "Code for letter e ", codes['e']
	print "Code for letter y ", codes['y']
	print "Code for letter z ", codes['z']

if __name__ == "__main__" : main()
	 