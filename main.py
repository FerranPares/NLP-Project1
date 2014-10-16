# -*- coding: utf-8 -*-
#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        main.py
#
#-----------------------------------------------------------------------------
from auxiliar import *

def computeModel(pathfile):
	Lwords = getWordsFromFile(pathfile)
	(U,B,T) = countNgrams(Lwords,0,0)
	#print B['last','spring.']
	Uentropy = 0.0
	Bentropy = 0.0
	Tentropy = 0.0
	length = float(len(Lwords))
	prob = {}
	Bprob = {}

	for key in U.keys():
		pX = U[key]/length
		prob[key] = [pX, 0.0, 0.0]
		Uentropy += pX*log(pX)

	for bkey in B.keys():
		pYIX = float(B[bkey])/float(U[bkey[0]])
		Bprob[bkey] = [pYIX, 0.0]
		prob[bkey[0]][1] += pYIX * log(pYIX)

	for tkey in T.keys():
		pZIXY = float(T[tkey])/float(B[tkey[0], tkey[1]])
		#if pZIXY != 1.0:
		#	print pZIXY
			#Fuck! this is not working, pZIXY always equals 1.0
		Bprob[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY)

	for bkey in Bprob.keys():
		prob[bkey[0]][2] += Bprob[bkey][0]*Bprob[bkey][1]

	for val in prob.values():
		Bentropy += val[0] * val[1]
		Tentropy += val[0] * val[2]

	return (-1*Uentropy, -1*Bentropy, -1*Tentropy)

'''def computeBigramModel(pathfile):
	Lwords = getWordsFromFile(pathfile)
	(U,B,T) = countNgrams(Lwords,0,0)
	entropy = 0.0
	length = float(len(Lwords))
	prob = {}	

	for key in U.keys():
		pX = U[key]/length
		prob[key] = [pX, 0.0]

	for bkey in B.keys():
		#pYX = B[bkey]/length
		#pYIX = pYX/prob[bkey[0]][0]
		pYIX = float(B[bkey])/float(U[bkey[0]])
		prob[bkey[0]][1] += pYIX * log(pYIX)

	for val in prob.values():
		entropy += val[0] * val[1]

	return -1*entropy'''

def computeTrigramModel(T):
	print "Function to compute the trigram model"

	return -1*entropy

      
##importing tagged brown corpus from NLTK
##importingBrownCorpusFromNLTK("../corpus/taggedBrown.txt")

#taggedWords = getTaggedWordsFromFile("corpus/taggedBrown.txt")
#enWords = getWordsFromFile("corpus/en.txt")
#esWords = getWordsFromFile("corpus/es.txt")

#(U,B,T) = countNgrams(enWords,0,0)

#unigramEntropy = computeUnigramModel("corpus/en.txt")
#print unigramEntropy

(UEntropy, BEntropy, TEntropy) = computeModel("corpus/en.txt")
print UEntropy, BEntropy, TEntropy







