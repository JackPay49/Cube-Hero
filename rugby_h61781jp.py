import sys

file = open(sys.argv[1],"r")
fullString = file.readline()
file.close()
team1Score = 0
team2Score = 0
teamOfWinner = 0
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

if (team1Score > team2Score):
	teamOfWinner = 1
elif (team2Score > team1Score):
	teamOfWinner = 2

if (teamOfWinner != 0):
	print("Team",str(teamOfWinner),"won!")
else:
	print("Draw!")

file = open(sys.argv[2],"w")
file.write((str(team1Score) + ":" + str(team2Score)))
file.close()

