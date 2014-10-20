#-----------------------------------------------------------------------------
# Name:        	main.py
# Authors:		Armand Vilalta, Ruben Garzon & Feran Pares
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

def getDicsfromPairs(LPairs, B, T):
	Btw = {}
	Btt = {}
	Ttww = {}
	Tttw = {}
	wordTagDIC = {}
	for i in range(len(LPairs)):
		if LPairs[i][0] not in wordTagDIC:
			wordTagDIC[LPairs[i][0]] = LPairs[i][1]

	for bkey in B.keys():
		if (wordTagDIC[bkey[0]],bkey[1]) not in Btw:
			Btw[wordTagDIC[bkey[0]],bkey[1]] = B[bkey]
		else:
			Btw[wordTagDIC[bkey[0]],bkey[1]] += B[bkey]
			
		if (wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]) not in Btt:
			Btt[wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]] = B[bkey]
		else:
			Btt[wordTagDIC[bkey[0]],wordTagDIC[bkey[1]]] += B[bkey]

	for tkey in T.keys():
		if (wordTagDIC[tkey[0]],tkey[1],tkey[2]) not in Ttww:
			Ttww[wordTagDIC[tkey[0]],tkey[1],tkey[2]] = T[tkey]
		else:
			Ttww[wordTagDIC[tkey[0]],tkey[1],tkey[2]] += T[tkey]
			
		if (wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]) not in Tttw:
			Tttw[wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]] = T[tkey]
		else:
			Tttw[wordTagDIC[tkey[0]],wordTagDIC[tkey[1]],tkey[2]] += T[tkey]

	return (wordTagDIC,Btw,Btt,Ttww,Tttw)
'''
def computeTaggedModel (pathfile):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Nwords = len(Lwords)
	Tperplexity = {}
	Tperplexity[1] = 0.0
	Tperplexity[2] = 0.0
	Tperplexity[4] = 0.0

	for part in [1,2,4]:
		for i in range(part):
			Tentropy = 0.0
			(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
			length = float(Nwords/part)
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
			
			Tperplexity[part] += pow(2,Tentropy)

		Tperplexity[part] *= 1/float(part)

	return (Tperplexity[1], Tperplexity[2], Tperplexity[4])

def computeTaggedModelTWW (pathfile):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	#wordTagDIC = getTagfromWord(LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	Tperplexity = {}
	Tperplexity[1] = 0.0
	Tperplexity[2] = 0.0
	Tperplexity[4] = 0.0

	for part in [1,2,4]:
		for i in range(part):
			Tentropy = 0.0
			(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
			(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
			length = float(Nwords/part) #equal length of tags
			prob = {}
			Bprob = {}
			wordTagDIC = {}
			Btw = {}
			Btt = {}
			Ttww = {}
			Tttw = {}
			
			(wordTagDIC, Btw, Btt, Ttww, Tttw) = getDicsfromPairs(LPairs, B, T)

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
			
			Tperplexity[part] += pow(2,Tentropy)

		Tperplexity[part] *= 1/float(part)

	return (Tperplexity[1], Tperplexity[2], Tperplexity[4])

def computeTaggedModelTTW (pathfile):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	#wordTagDIC = getTagfromWord(LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	Tperplexity = {}
	Tperplexity[1] = 0.0
	Tperplexity[2] = 0.0
	Tperplexity[4] = 0.0

	for part in [1,2,4]:
		for i in range(part):
			Tentropy = 0.0
			(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
			(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
			length = float(Nwords/part) #equal length of tags
			#lengthtags = float(Ntags/part)
			prob = {}
			Bprob = {}
			wordTagDIC = {}
			Btw = {}
			Btt = {}
			Ttww = {}
			Tttw = {}
			
			(wordTagDIC, Btw, Btt, Ttww, Tttw) = getDicsfromPairs(LPairs, B, T)
			
			

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
			
			Tperplexity[part] += pow(2,Tentropy)

		Tperplexity[part] *= 1/float(part)

	return (Tperplexity[1], Tperplexity[2], Tperplexity[4])
'''
	
def computeAllTaggedModels (pathfile):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	
	TperplexityWWW = {}
	TperplexityWWW[1] = 0.0 #[0.0,0.0,0.0]
	TperplexityWWW[2] = 0.0
	TperplexityWWW[4] = 0.0
	TperplexityTWW = {}
	TperplexityTWW[1] = 0.0
	TperplexityTWW[2] = 0.0
	TperplexityTWW[4] = 0.0
	TperplexityTTW = {}
	TperplexityTTW[1] = 0.0
	TperplexityTTW[2] = 0.0
	TperplexityTTW[4] = 0.0

	for part in [1,2,4]:
		for i in range(part):
			TentropyWWW = 0.0
			TentropyTWW = 0.0
			TentropyTTW = 0.0
			(U,B,T) = countNgrams(Lwords,i*Nwords/part,(i+1)*Nwords/part)
			(Ut, Bt, Tt) = countNgrams(Ltags,i*Ntags/part,(i+1)*Ntags/part)
			length = float(Nwords/part) #equal length of tags
			pWWW = {}
			BpWWW = {}
			pTWW = {}
			BpTWW = {}
			pTTW = {}
			BpTTW = {}
			wordTagDIC = {}
			Btw = {}
			Btt = {}
			Ttww = {}
			Tttw = {}
			
			(wordTagDIC, Btw, Btt, Ttww, Tttw) = getDicsfromPairs(LPairs, B, T)

			for key in U.keys():
				pX = U[key]/length
				pWWW[key] = [pX, 0.0]

			for key in Ut.keys():
				pX = Ut[key]/length
				pTWW[key] = [pX, 0.0]
				pTTW[key] = [pX, 0.0]

			for bkey in B.keys():
				pYIX = float(B[bkey])/float(U[bkey[0]])
				BpWWW[bkey] = [pYIX, 0.0]

			for bkey in Btw.keys():
				pYIX = float(Btw[bkey])/float(Ut[bkey[0]])
				BpTWW[bkey] = [pYIX, 0.0]

			for bkey in Btt.keys():
				pYIX = float(Btt[bkey])/float(Ut[bkey[0]])
				BpTTW[bkey] = [pYIX, 0.0]

			for tkey in T.keys():
				pZIXY = float(T[tkey])/float(B[tkey[0], tkey[1]])
				BpWWW[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

			for tkey in Ttww.keys():
				pZIXY = float(Ttww[tkey])/float(Btw[tkey[0], tkey[1]])
				BpTWW[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

			for tkey in Tttw.keys():
				pZIXY = float(Tttw[tkey])/float(Btt[tkey[0],tkey[1]])
				BpTTW[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

			for Bpkey in BpWWW.keys():
				pWWW[Bpkey[0]][1] += BpWWW[Bpkey][0]*BpWWW[Bpkey][1]

			for Bpkey in BpTWW.keys():
				pTWW[Bpkey[0]][1] += BpTWW[Bpkey][0]*BpTWW[Bpkey][1]

			for Bpkey in BpTTW.keys():
				pTTW[Bpkey[0]][1] += BpTTW[Bpkey][0]*BpTTW[Bpkey][1]

			for val in pWWW.values():
				TentropyWWW -= val[0] * val[1]

			for val in pTWW.values():
				TentropyTWW -= val[0] * val[1]

			for val in pTTW.values():
				TentropyTTW -= val[0] * val[1]

			TperplexityWWW[part] += pow(2,TentropyWWW)
			TperplexityTWW[part] += pow(2,TentropyTWW)
			TperplexityTTW[part] += pow(2,TentropyTTW)

		TperplexityWWW[part] *= 1/float(part)
		TperplexityTWW[part] *= 1/float(part)
		TperplexityTTW[part] *= 1/float(part)

	return (TperplexityWWW[1], TperplexityWWW[2], TperplexityWWW[4], TperplexityTWW[1], TperplexityTWW[2], TperplexityTWW[4], TperplexityTTW[1], TperplexityTTW[2], TperplexityTTW[4])




#(FPerplexityWWW, HPerplexityWWW, QPerplexityWWW) = computeTaggedModel ("corpus/taggedBrown.txt")
#(FPerplexityTWW, HPerplexityTWW, QPerplexityTWW) = computeTaggedModelTWW ("corpus/taggedBrown.txt")
#(FPerplexityTTW, HPerplexityTTW, QPerplexityTTW) = computeTaggedModelTTW ("corpus/taggedBrown.txt")

print ''
print 'Computing entropies with english corpus...'
t0 = time()
(UEntropyEN, BEntropyEN, TEntropyEN) = computeModel("corpus/en.txt")
t00 = time()

print ''
print 'Computing entropies with spanish corpus...'
t1 = time()
(UEntropyES, BEntropyES, TEntropyES) = computeModel("corpus/es.txt")
t11 = time()

print ''
print '----------------------------------ENTROPIES-----------------------------------'
print '------------------------------------------------------------------------------'
print '|| Corpus language ||     Unigram     ||     Bigram      ||     Trigram     ||'
print '||     English     || ',UEntropyEN,'   || ', BEntropyEN,'  || ', TEntropyEN,' ||'
print '||     Spanish     || ',UEntropyES,' || ', BEntropyES,' || ', TEntropyES,'   ||'
print '------------------------------------------------------------------------------'
print ''
print 'Time to run english entropies: ', (t00-t0)
print 'Time to run spanish entropies: ', (t11-t1)
print ''
print ''

#print 'Relation between entropies in english and spanish', UEntropy/UEntropyes, BEntropy/BEntropyes, TEntropy/TEntropyes

print 'Computing perplexities with Browncorpus...'
t2 = time()
(FPerplexityWWW, HPerplexityWWW, QPerplexityWWW, FPerplexityTWW, HPerplexityTWW, QPerplexityTWW, FPerplexityTTW, HPerplexityTTW, QPerplexityTTW) = computeAllTaggedModels("corpus/taggedBrown.txt")
t22 = time()

print ''
print '------------------------------PERPLEXITIES------------------------------'
print '------------------------------------------------------------------------'
print '||  Model    ||      Full       ||      Half       ||     Quarter     ||'
print '|| <x,y,z>   || ',FPerplexityWWW,'  || ',HPerplexityWWW,' || ',QPerplexityWWW,' ||'
print '|| <x`,y,z>  || ',FPerplexityTWW,' || ',HPerplexityTWW,'  || ',QPerplexityTWW,' ||'
print '|| <x`,y`,z> || ',FPerplexityTTW,' || ',HPerplexityTTW,' || ',QPerplexityTTW,' ||'
print '------------------------------------------------------------------------'
print ''
print 'Time to run perplexities: ', (t22-t2)