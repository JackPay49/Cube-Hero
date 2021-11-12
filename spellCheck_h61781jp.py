import sys,os

dictionary = []
file = open(sys.argv[1],"r")
for line in file:
	line = line.rstrip()
	dictionary.append(line)
file.close()


for filename in os.listdir(sys.argv[2]):
	file = open((sys.argv[2] + filename),"r")
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
	i = 0
	while (i <len(fullString)):
		amountToIncrement = 1
		addWord = False

		if (fullString[i] in (".","?","!",",",":",";","-","—","(",")","{","}","[","]","'",'"')):
			if (fullString[i] == "."):
				if ((i + 2) < (len(fullString) - 1)):
					if (fullString[i] == fullString[i + 1] == fullString[i + 2] == "."):#if its an elipisis then skip the next two characters as they are part of it
						amountToIncrement = 3
			nPunctuation +=1
			if (fullString[i] not in ("'","-")):
				addWord = True
		elif (fullString[i] in ("1","2","3","4","5","6","7","8","9","0")):
			nNumbers +=1
		elif (fullString[i] in uppcaseLetters):
			nUpperCase += 1
			currentWord += fullString[i].lower()
		elif (fullString[i] == " "):
			addWord = True
		else:
			currentWord += fullString[i]

		currentWord = currentWord.strip()
		if ((currentWord == "")):
			addWord = False
		elif(i == len(fullString) - 1):
			addWord = True

		if (addWord):
			nWords +=1
			allwords.append(currentWord)
			currentWord = ""
		i += amountToIncrement

	for i in range(nWords):
		if (allwords[i] in dictionary):
			nCorrectWords +=1

	newFileName = filename[0:(len(filename) - 4):1]
	file = open((sys.argv[3] + newFileName + "_h61781jp.txt"),"w")

	file.write("h61781jp\n")
	file.write("Formatting ###################\n")
	file.write("Number of upper case letters changed: " + str(nUpperCase) + "\n")
	file.write("Number of punctuations removed: " + str(nPunctuation)+ "\n")
	file.write("Number of numbers removed: " + str(nNumbers)+ "\n")
	file.write("Spellchecking ###################\n")
	file.write("Number of words: " + str(nWords) + "\n")
	file.write("Number of correct words: " + str(nCorrectWords) + "\n")
	file.write("Number of incorrect words: " + str(nWords - nCorrectWords) + "\n")
	file.close()