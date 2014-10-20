# -*- coding: utf-8 -*-
#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        main.py
#
#-----------------------------------------------------------------------------
from auxiliar import *
from time import time

def computeModel(pathfile):
	Lwords = getWordsFromFile(pathfile)
	(U,B,T) = countNgrams(Lwords,0,0)
	Uentropy = 0.0
	Bentropy = 0.0
	Tentropy = 0.0
	length = float(len(Lwords))
	#length = float(100554)
	prob = {}
	Bprob = {}

	for key in U.keys():
		pX = U[key]/length
		prob[key] = [pX, 0.0, 0.0]
		Uentropy -= pX*log(pX,2)

	for bkey in B.keys():
		pYIX = float(B[bkey])/float(U[bkey[0]])
		Bprob[bkey] = [pYIX, 0.0]
		prob[bkey[0]][1] += pYIX * log(pYIX,2)

	for tkey in T.keys():
		pZIXY = float(T[tkey])/float(B[tkey[0], tkey[1]])
		Bprob[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

	for bkey in Bprob.keys():
		prob[bkey[0]][2] += Bprob[bkey][0]*Bprob[bkey][1]

	for val in prob.values():
		Bentropy -= val[0] * val[1]
		Tentropy -= val[0] * val[2]

	return (Uentropy, Bentropy, Tentropy)

def computeTaggedModel (pathfile, part):
	LofPwords = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LofPwords)
	#Ltags = map(lambda x:x[1],LofPwords)
	Nwords = len(Lwords)
	#Ntags = len(Ltags)
	Tentropy = 0.0

	for i in range(part):
		(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
		#(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
		length = float(Nwords/part)
		#lengthtags = float(Ntags/part)
		prob = {}
		Bprob = {}

		for key in U.keys():
			pX = U[key]/length
			prob[key] = [pX, 0.0]

		for bkey in B.keys():
			pYIX = float(B[bkey])/float(U[bkey[0]])
			Bprob[bkey] = [pYIX, 0.0]

		for tkey in T.keys():
			pZIXY = float(T[tkey])/float(B[tkey[0], tkey[1]])
			Bprob[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

		for Bprobkey in Bprob.keys():
			prob[Bprobkey[0]][1] += Bprob[Bprobkey][0]*Bprob[Bprobkey][1]

		for val in prob.values():
			Tentropy -= val[0] * val[1]

	Tentropy *= 1/float(part)

	return (Tentropy)

def getTagfromWord(LPairs):
	wordtagDIC = {}
	for i in range(len(LPairs)):
		if LPairs[i][0] not in wordtagDIC:
			wordtagDIC[LPairs[i][0]] = LPairs[i][1]

	return wordtagDIC


def computeTaggedModelTWW (pathfile, part):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	wordTagDIC = getTagfromWord(LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	Tentropy = 0.0

	for i in range(part):
		(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
		(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
		length = float(Nwords/part) #equal length of tags
		#lengthtags = float(Ntags/part)
		prob = {}
		Bprob = {}
		Btw = {}
		Ttww = {}
		
		for bkey in B.keys():
			if (wordTagDIC[bkey[0]],bkey[1]) not in Btw:
				Btw[wordTagDIC[bkey[0]],bkey[1]] = B[bkey]
			else:
				Btw[wordTagDIC[bkey[0]],bkey[1]] += B[bkey]

		for tkey in T.keys():
			if (wordTagDIC[tkey[0]],tkey[1],tkey[2]) not in Ttww:
				Ttww[wordTagDIC[tkey[0]],tkey[1],tkey[2]] = T[tkey]
			else:
				Ttww[wordTagDIC[tkey[0]],tkey[1],tkey[2]] += T[tkey]

		for key in Ut.keys():
			pX = Ut[key]/length
			prob[key] = [pX, 0.0]

		for bkey in Btw.keys():
			pYIX = float(Btw[bkey])/float(Ut[bkey[0]])
			Bprob[bkey] = [pYIX, 0.0]

		for tkey in Ttww.keys():
			pZIXY = float(Ttww[tkey])/float(Btw[tkey[0], tkey[1]])
			Bprob[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

		for Bprobkey in Bprob.keys():
			prob[Bprobkey[0]][1] += Bprob[Bprobkey][0]*Bprob[Bprobkey][1]

		for val in prob.values():
			Tentropy -= val[0] * val[1]

	Tentropy *= 1/float(part)

	return (Tentropy)
	
def computeTaggedModelTTW (pathfile, part):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	wordTagDIC = getTagfromWord(LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	Tentropy = 0.0

	for i in range(part):
		(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
		(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
		length = float(Nwords/part) #equal length of tags
		#lengthtags = float(Ntags/part)
		prob = {}
		Bprob = {}
		Btt = {}
		Tttw = {}
		
		for bkey in B.keys():
			if (wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]) not in Btt:
				Btt[wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]] = B[bkey]
			else:
				Btt[wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]] += B[bkey]

		for tkey in T.keys():
			if (wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]) not in Tttw:
				Tttw[wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]] = T[tkey]
			else:
				Tttw[wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]] += T[tkey]

		for key in Ut.keys():
			pX = Ut[key]/length
			prob[key] = [pX, 0.0]

		for bkey in Btt.keys():
			pYIX = float(Btt[bkey])/float(Ut[bkey[0]])
			Bprob[bkey] = [pYIX, 0.0]

		for tkey in Tttw.keys():
			pZIXY = float(Tttw[tkey])/float(Btt[tkey[0],tkey[1]])
			Bprob[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

		for Bprobkey in Bprob.keys():
			prob[Bprobkey[0]][1] += Bprob[Bprobkey][0]*Bprob[Bprobkey][1]

		for val in prob.values():
			Tentropy -= val[0] * val[1]

	Tentropy *= 1/float(part)

	return (Tentropy)
	
	


'''
t0 = time()
(UEntropy, BEntropy, TEntropy) = computeModel("corpus/en.txt")
t01 = time()
print (t01-t0),'s -- Entropies of english corpus: ',UEntropy, BEntropy, TEntropy

t1 = time()
(UEntropyes, BEntropyes, TEntropyes) = computeModel("corpus/es.txt")
t11 = time()
print (t11-t1),'s -- Entropies of spanish corpus: ',UEntropyes, BEntropyes, TEntropyes

print 'Relation between entropies in english and spanish', UEntropy/UEntropyes, BEntropy/BEntropyes, TEntropy/TEntropyes


FEntropy = computeTaggedModel ("corpus/taggedBrown.txt", 1)
print 'Entropy of full Browncorpus: ' , FEntropy

HEntropy = computeTaggedModel ("corpus/taggedBrown.txt", 2)
print 'Entropy of half Browncorpus: ' , HEntropy

QEntropy = computeTaggedModel ("corpus/taggedBrown.txt", 4)
print 'Entropy of quarter Browncorpus: ' , QEntropy
'''

FEntropyTWW = computeTaggedModelTWW ("corpus/taggedBrown.txt", 1)
print 'Entropy of full Browncorpus TWW: ' , FEntropyTWW

FEntropyTTW = computeTaggedModelTTW ("corpus/taggedBrown.txt", 1)
print 'Entropy of full Browncorpus TTW: ' , FEntropyTTW

