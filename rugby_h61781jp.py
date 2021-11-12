import sys, os

for filename in os.listdir(sys.argv[1]):
	file = open((sys.argv[1] + filename),"r")
	fullString = file.readline()
	file.close()
	team1Score = 0
	team2Score = 0
	i = 0
	while i < len(fullString):
		teamNumber = 0
		scoreType = ""
		if (fullString[i] == "T"):
			teamNumber = int(fullString[i + 1])
			scoreType = fullString[i + 2]

			if (scoreType == 't'):
				scoreQuantity = 5
			elif (scoreType == 'c'):
				scoreQuantity = 2
			elif (scoreType == 'p'):
				scoreQuantity = 3
			elif (scoreType == 'd'):
				scoreQuantity = 3
			else:
				scoreQuantity = 0

			if (teamNumber == 1):
				team1Score += scoreQuantity
			elif(teamNumber == 2):
				team2Score += scoreQuantity
		i += 3

	newFileName = filename[0:(len(filename) - 4):1]
	file = open((sys.argv[2] + newFileName + "_h61781jp.txt"),"w")
	file.write((str(team1Score) + ":" + str(team2Score)))
	file.close()

