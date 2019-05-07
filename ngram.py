#Ricardo Saucedo, submission for Kaggle competition with a BIGRAM Implementation
#

import re
import csv


diacritics = ['a','á','ais','áis','aisti','aistí','ait','áit','ar','ár','arsa','ársa',
			'ban','bán','cead','céad','chas','chás','chuig','chúig','dar','dár','do',
			'dó','gaire','gáire','i','í','inar','inár','leacht','léacht','leas','léas',
			'mo','mó','na','ná','os','ós','re','ré','scor','scór','te','té','teann',
			'téann','thoir','thóir']

num = 1
row = ["Id","Expected"]
with open('mySubmission.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(row)
       
	tempLib = {}
	unigramLib = {}
	beforeLib = {}
	afterLib = {}         
	'''
	READ IN TRAINING TEXT & FORM DIACRITICS
	'''

	fileReader = open('train.txt','r', errors = "replace")
	lines = fileReader.read()
	            
	words = re.split("[, \@\"\'\-!?:.+/\[\])(><\n_]+", lines)
	words = [w.strip() for w in words]

	'''
	set up dictionaries for unigram/bigram
	'''

	for i in diacritics:
		tempLib = {i:{}}
		beforeLib.update(tempLib)
		afterLib.update(tempLib)	
	tempLib.clear()

	'''
	UNIGRAM IMPLEMENTATION
	'''

	for t in diacritics:
		count = 0
		for word in words:
			if (t == word):
				count += 1
		unigramLib[t] = count
		
	##################### BIGRAM IMPLEMENTATION #####################


	for t in diacritics:		
		for i in range(len(words)):	
			
			if (t == words[i]) and (words[i-1] not in beforeLib[t]):		
				beforeLib[t][words[i-1]] = 1
			
			elif (t == words[i]) and (words[i-1] in beforeLib):
				beforeLib[t][words[i-1]] += 1
			
			elif (t == words[i]) and (words[i+1] not in afterLib[t]):
				afterLib[t][words[i+1]] = 1
			
			elif (t == words[i]) and (words[i+1] in afterLib):
				afterLib[t][words[i+1]] += 1
				
			

	######### TEST DATA PROCESSING ############# 
	testFileReader = open('test.txt','r', errors="replace")
	testLines = testFileReader.read()
	testWords = re.split("[, \@\"\'\-!?:.+/\[\])_(><\n]+", testLines)
	testWords = [w.strip() for w in testWords]
	testWords.remove("")

	row = ["Id","Expected"]
	with open('KaggleSubmission.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(row)
		for i in range(len(testWords)):
			if ((len(testWords[i]) >= 1) and testWords[i] != "\n"):
				if (testWords[i][0] == '{'):
					checkWord = testWords[i-1]
					checkWord2 = testWords[i+1]
					splitBrace = testWords[i].strip('{}')
					splitBrace = re.split("\|",splitBrace)
					choice1 = splitBrace[0]
					choice2 = splitBrace[1]
					
					###Computation###
					for j in beforeLib[choice1]:
						if (j == checkWord):
							numValueBefore = beforeLib[choice1][j]
						else:
							numValueBefore = 0
							
					for k in afterLib[choice1]:
						if (k == checkWord2):
							numValueAfter = afterLib[choice1][k]
						else:
							numValueAfter = 0	

					for l in beforeLib[choice2]:
						if (l == checkWord):
							numValue2Before = beforeLib[choice2][l]
						else:
							numValue2Before = 0
					#numValue2Before = 0

					for m in afterLib[choice2]:
						if (m == checkWord2):
							numValue2After = afterLib[choice2][m]
						else:
							numValue2After = 0
					
					#or (numValue2Before == 0) or (numValue2After == 0)
					
					if (numValueBefore == 0) or (numValueAfter == 0) or (numValue2Before ==0) or (numValue2After == 0):
						count1 = 0
						count2 = 0
						total = 0
						prob = 0
						for key, value in unigramLib.items():
							if key == choice1:
								count1 = value
							if key == choice2:
								count2 = value
								
						if count1 is not 0 and count2 is not 0:
							total = count1 + count2
							probchoice1 = count1/total
							newRows = [num,probchoice1]
							#writeOutput('mySubmission.csv',num,probchoice1)
							writer.writerow(newRows)
							num += 1
						
					## BIGRAM ##		 
					else:
						probBefore = numValueBefore/(numValueBefore + numValue2Before)
						probAfter = numValueAfter/(numValueAfter + numValue2After)
						
						#probBeforeOther = numValue2Before/(numValue2Before + numValueBefore)
						#probAfterOther = numValue2After/(numValue2After + numValueAfter)
						
						alpha = probAfter * probBefore
						#beta = probBeforeOther * probAfterOther  
						totalProb = alpha/(alpha + 1)
					
						newRows = [num,totalProb]
						#writeOutput('mySubmission.csv',num,totalProb)
						writer.writerow(newRows)
						num += 1
	fileReader.close()
csvfile.close()


