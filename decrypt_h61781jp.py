import sys,os

morseCodeAlphabet =[".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..",".----","..---","...--","....-",".....","-....","--...","---..","----.","-----"]
morseEquivalentAlphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0"]


for filename in os.listdir(sys.argv[1]):

	file = open((sys.argv[1] + filename),"r")
	fullString = file.readline()
	file.close()

	tempString = ""

	for i in range(len(fullString)):
		if (fullString[i] != ":"):
			tempString += fullString[i]
		else:
			algorithm = tempString
			tempString = ""
	ciphertext = tempString.lower()
	plaintext = ""

	if (algorithm == "Morse Code"):
		morseChar = ""
		plaintext = ""
		for i in range(len(ciphertext)):
			atEndOfLetter = False

			if (i == (len(ciphertext) -1)):
				atEndOfLetter = True

			if (ciphertext[i] != "/"):
				if (ciphertext[i] != " "):
					morseChar += ciphertext[i]
				else:
					atEndOfLetter = True

				if (atEndOfLetter):
					for j in range(len(morseCodeAlphabet)):
						if (morseChar == morseCodeAlphabet[j]):
							plaintext += morseEquivalentAlphabet[j]
					morseChar = ""
			else:
				plaintext += " "
				morseChar = ""

	elif (algorithm == "Caesar Cipher(+3)"):
		for i in range(len(ciphertext)):
			if (ciphertext[i] != " "):
				currentASCII = ord(ciphertext[i])
				newASCII = currentASCII - 3
				if (newASCII == 96):
					newASCII = 122
				elif (newASCII == 95):
					newASCII = 121
				elif (newASCII == 94):
					newASCII = 120
				plaintext += chr(newASCII)
			else:
				plaintext += " "
	elif (algorithm == "Hex"):
		currentChar = ""
		for i in range(len(ciphertext)):
			atEndOfLetter = False
			if (i == (len(ciphertext) -1)):
				atEndOfLetter = True

			if (ciphertext[i] != " "):
				currentChar += ciphertext[i]
			else:
				atEndOfLetter = True

			if (atEndOfLetter):
				plaintext += chr(int(currentChar,16))
				currentChar = ""

		plaintext = plaintext.lower()

	newFileName = filename[0:(len(filename) - 4):1]
	file = open((sys.argv[2] + newFileName + "_h61781jp.txt"),"w")
	file.write(plaintext)
	file.close()
