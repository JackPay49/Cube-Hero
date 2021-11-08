import sys

dictionary = []
file = open(sys.argv[1],"r")
for line in file:
	line = line.rstrip()
	dictionary.append(line)
file.close()

file = open(sys.argv[2],"r")#1 is english words, 2 is input, 3 is output
fullString = file.read()
file.close()

nPunctuation = 0
nUpperCase = 0
nNumbers = 0
nWords = 0
nCorrectWords = 0
allwords = []

uppcaseLetters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

currentWord = ""
for i in range(len(fullString)):
	addWord = False
	if (fullString[i] in ("!","?",",",".","(",")",":",";","[","]",'"',"'","-","/","@","{","}","*","|","£","$","%","^","=","+","_","~","#","<",">",)):
		nPunctuation +=1
		if (fullString[i] not in ("'","-")):
			addWord = True
	elif (fullString[i] in ("1","2","3","4","5","6","7","8","9","0")):
		nNumbers +=1
		addWord = True
	elif (fullString[i] in uppcaseLetters):
		nUpperCase += 1
		currentWord += fullString[i].lower()
	elif (fullString[i] == " "):
		addWord = True
	else:
		currentWord += fullString[i]

	if (currentWord == ""):
		addWord = False
	elif(i == len(fullString) - 1):
		addWord = True

	if (addWord):
		nWords +=1
		allwords.append(currentWord.strip())
		currentWord = ""

for i in range(nWords):
	if (allwords[i] in dictionary):
		nCorrectWords +=1

file = open(sys.argv[3],"w")
file.write("h61781jp\n")
file.write("Formatting ###################\n")
file.write("Number of upper case words changed: " + str(nUpperCase) + "\n")
file.write("Number of punctuations removed: " + str(nPunctuation)+ "\n")
file.write("Number of numbers removed: " + str(nNumbers)+ "\n")
file.write("Spellchecking ###################\n")
file.write("Number of words: " + str(nWords) + "\n")
file.write("Number of correct words: " + str(nCorrectWords) + "\n")
file.write("Number of incorrect words: " + str(nWords - nCorrectWords) + "\n")
file.close()