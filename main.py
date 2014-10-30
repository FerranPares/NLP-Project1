#-----------------------------------------------------------------------------
# Name:        	main.py
# Authors:		Armand Vilalta, Ruben Garzon & Feran Pares
#-----------------------------------------------------------------------------

from auxiliar import *
from time import time

def computeModel(pathfile, lencorpus=0):
	Lwords = getWordsFromFile(pathfile)
	(U,B,T) = countNgrams(Lwords,0,lencorpus)
	Uentropy = 0.0
	Bentropy = 0.0
	Tentropy = 0.0
	if lencorpus==0:
		length = float(len(Lwords))
	else:
		length = float(lencorpus)
	
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

def getDicsfromPairs(LPairs, inic, end):
	Btw = {}
	Ttww = {}
	Tttw = {}
	
	Btw[(LPairs[inic][1],LPairs[inic+1][0])]=1
	for i in range(inic+2,end):
		if (LPairs[i-1][1],LPairs[i][0]) not in Btw:
			Btw[(LPairs[i-1][1],LPairs[i][0])] = 1
		else:
			Btw[(LPairs[i-1][1],LPairs[i][0])] +=1
		
		if (LPairs[i-2][1],LPairs[i-1][0],LPairs[i][0]) not in Ttww:
			Ttww[(LPairs[i-2][1],LPairs[i-1][0],LPairs[i][0])] = 1
		else:
			Ttww[(LPairs[i-2][1],LPairs[i-1][0],LPairs[i][0])] +=1
		
		if (LPairs[i-2][1],LPairs[i-1][1],LPairs[i][0]) not in Tttw:
			Tttw[(LPairs[i-2][1],LPairs[i-1][1],LPairs[i][0])] = 1
		else:
			Tttw[(LPairs[i-2][1],LPairs[i-1][1],LPairs[i][0])] +=1
	
	return (Btw,Ttww,Tttw)

def computeAllTaggedModels (pathfile):
	LPairs = getTaggedWordsFromFile(pathfile)
	Lwords = map(lambda x:x[0],LPairs)
	Ltags = map(lambda x:x[1],LPairs)
	Nwords = len(Lwords)
	Ntags = len(Ltags)
	
	TperplexityWWW = {}
	TperplexityWWW[1] = 0.0 
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
			Btw = {}
			Ttww = {}
			Tttw = {}
			
			(Btw, Ttww, Tttw) = getDicsfromPairs(LPairs, i*Nwords/part, (i+1)*Nwords/part)

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

			for bkey in Bt.keys():
				pYIX = float(Bt[bkey])/float(Ut[bkey[0]])
				BpTTW[bkey] = [pYIX, 0.0]

			for tkey in T.keys():
				pZIXY = float(T[tkey])/float(B[tkey[0], tkey[1]])
				BpWWW[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

			for tkey in Ttww.keys():
				pZIXY = float(Ttww[tkey])/float(Btw[tkey[0], tkey[1]])
				BpTWW[tkey[0],tkey[1]][1] += pZIXY * log(pZIXY,2)

			for tkey in Tttw.keys():
				pZIXY = float(Tttw[tkey])/float(Bt[tkey[0],tkey[1]])
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


print ''
print 'Computing entropies with english corpus...'
t0 = time()
(UEntropyEN, BEntropyEN, TEntropyEN) = computeModel("corpus/en.txt")
t00 = time()

print ''
print 'Computing entropies with small english corpus...'
t1 = time()
(UEntropyENS, BEntropyENS, TEntropyENS) = computeModel("corpus/en.txt", 482373)
t11 = time()

print ''
print 'Computing entropies with spanish corpus...'
t2 = time()
(UEntropyES, BEntropyES, TEntropyES) = computeModel("corpus/es.txt")
t22 = time()

print ''
print '----------------------------------ENTROPIES-----------------------------------'
print '------------------------------------------------------------------------------'
print '|| Corpus language ||     Unigram     ||     Bigram      ||     Trigram     ||'
print '||     English     || ',UEntropyEN,'   || ', BEntropyEN,'  || ', TEntropyEN,' ||'
print '||  Small English  || ',UEntropyENS,' || ', BEntropyENS,' || ', TEntropyENS,' ||'
print '||     Spanish     || ',UEntropyES,' || ', BEntropyES,' || ', TEntropyES,'   ||'
print '------------------------------------------------------------------------------'
print ''
print 'Time to run english entropies: ', (t00-t0),' s'
print 'Time to run small english entropies: ', (t11-t1),' s'
print 'Time to run spanish entropies: ', (t22-t2),' s'
print ''
print ''

print 'Computing perplexities with Browncorpus...'
t2 = time()
(FPerplexityWWW, HPerplexityWWW, QPerplexityWWW, FPerplexityTWW, HPerplexityTWW, QPerplexityTWW, FPerplexityTTW, HPerplexityTTW, QPerplexityTTW) = computeAllTaggedModels("corpus/taggedBrown.txt")
t22 = time()

print ''
print '------------------------------PERPLEXITIES------------------------------'
print '------------------------------------------------------------------------'
print '||  Model    ||      Full       ||      Half       ||     Quarter     ||'
print '|| <x,y,z>   || ',FPerplexityWWW,'  || ',HPerplexityWWW,' || ',QPerplexityWWW,' ||'
print '|| <x`,y,z>  || ',FPerplexityTWW,' || ',HPerplexityTWW,' || ',QPerplexityTWW,' ||'
print '|| <x`,y`,z> || ',FPerplexityTTW,' || ',HPerplexityTTW,' || ',QPerplexityTTW,' ||'
print '------------------------------------------------------------------------'
print ''
print 'Time to run perplexities: ', (t22-t2),' s'
