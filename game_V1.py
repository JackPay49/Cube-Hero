import tkinter
from tkinter import *

import tkinter.font as font #This will import the font changing part of tkinter and will assgin it to just the attribute "font"
# Will import everything from the tkinter library

#Classes
# class snake:

class Scoreboard:

	scores = []
	maxNumberOfScores = 10
	numberOfScores = 0

	def SortScores(self,low,high):
		tempLow = low
		tempHigh = high
		pivot = self.scores[int((low + high)/2)].score#Must specify self so that it changes the attribute of the class
		while(tempLow <= tempHigh):
			while(self.scores[tempLow].score > pivot and tempLow < high):
				tempLow += 1
			while(self.scores[tempHigh].score < pivot and tempHigh > low):
				tempHigh -= 1
			if (tempLow <= tempHigh):
				tempPlayer = self.scores[tempLow]
				self.scores[tempLow] = self.scores[tempHigh]
				self.scores[tempHigh] = tempPlayer
				tempLow += 1
				tempHigh -= 1
		if (low < tempHigh):
			self.SortScores(low,tempHigh)
		if (tempLow < high):
			self.SortScores(tempLow,high)

	def SaveScoreboard(self):
		self.SortScores(0,(self.numberOfScores - 1))#Sort the scoreboard before saving it so that we know it's in order
		file = open("gameFiles/scoreboard.txt","w")#Opens the scorebaord file to write into. Will rewrite the full thing
		file.write(str(self.numberOfScores))
		for i in range(0,len(self.scores)):
			file.write("\n" + self.scores[i].name)
			file.write("\n" + str(self.scores[i].score))
			file.write("\n")#Leaves a line for readability
		file.close()

	def LoadInScoreboard(self):
		file = open("gameFiles/scoreboard.txt","rt")
		self.numberOfScores = int(file.readline())
		for i in range(0,self.numberOfScores):
			tempPlayer = player()#Will create a dumby player to store within the scores list
			tempPlayer.name = file.readline().strip()#Loads in their name and score, on two separate lines. Strip is used to get rid of any leading or trailing white space.
			tempPlayer.score = int(file.readline())
			file.readline()#Will then skip one line, each player record has a space in between for readability
			self.scores.append(tempPlayer)#Will add the player to the scoreboard
		file.close()#Must close file!

	def AddScoreToScoreboard(self,newPlayer):
		#2 cases. Either the scoreboard is full or not. if not then we can just add the new score to the end and sort it. If it is full then we must check the lowest score
		if (len(self.scores) >= self.maxNumberOfScores):#If there are 10 scores then it is full, check lowest score
			if (newPlayer.score > self.scores[maxNumberOfScores - 1].score):#If their score is higher than the lowest score saved then replace it. Must still reorder incase its still larger than another score
				self.scores[maxNumberOfScores - 1] = newPlayer
				self.numberOfScores += 1
				self.SortScores(0,(self.numberOfScores - 1))
				self.SaveScoreboard()#Save these changes
		else: #else then the new score can just be added onto the end of the scoreboard
			self.scores.append(newPlayer)#adds onto the end
			self.numberOfScores += 1
			self.SortScores(0,(self.numberOfScores - 1))#sorts it again
			self.SaveScoreboard()#Save these changes

class player:
	name = ""#All variables or attributes of players
	level = 0
	score = 0
	# playerSnake = snake()

	def LoadPlayer(self,nValue):
		self.name = nValue
		file = open("gameFiles/" + name + ".txt","rt")#This will open a file for reading in the text format based on the input name of the user
		
		file.readline()#Used to skip the name which is written into the file for readability
		self.level = int(file.readline())#Gets their level and score & converts them into integers
		self.score = int(file.readline())
		file.close()#Must close the file afterwards!

	# def SavePlayer():
		#Code to write a text file for the player

#Setting up Windows
def SetUpMenu(windowMenu):
	windowMenu.geometry("500x500")#Sets the size of the window
	windowMenu.title("Menu") #Sets the title of the window currently

	#fonts
	fontTitle = tkinter.font.Font(size = 30) #This creates a new font called fontTitle that has the font size of 30
	fontButtons = tkinter.font.Font(size = 12) #This creates a new font called fontTitle that has the font size of 30

	#Buttons
	btnLoadGame = Button(windowMenu,text = "Load Game")#Creates a basic button displaying text
	btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)#Will place the button relative to 0.1 of the width of the screen, 0,5 of the height of the screen and in the center
	btnLoadGame['font'] = fontButtons #Will set the font of the button to the standard button font

	btnCreateNewGame = Button(windowMenu,text = "Create new Game")
	btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
	btnCreateNewGame['font'] = fontButtons


	btnScoreboard = Button(windowMenu,text = "Scoreboard",command = OpenScoreboard)
	btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = CENTER)
	btnScoreboard['font'] = fontButtons


	btnClose = Button(windowMenu,text = "Close",command = windowMenu.destroy) #This binds the command to close the screen to this button. We can instead specify procedures here
	btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)
	btnClose['font'] = fontButtons

	#labels
	lbTitle = Label(windowMenu,text = "Game Name!")#Creates a label, just the same type of commands as making a button
	lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)
	lbTitle['font'] = fontTitle

#All scoreboard stuff
def SetUpScoreboard(windowScoreboard):
	windowScoreboard.geometry("1000x700")
	windowScoreboard.title("Scoreboard")

	fontTitle = tkinter.font.Font(size = 50) 

	lbTitle = Label(windowScoreboard,text = "Scoreboard")
	lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)
	lbTitle['font'] = fontTitle


	btnClose = Button(windowScoreboard,text = "Back",command = windowScoreboard.destroy)
	btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)

	scoreBox = Text(windowScoreboard,height = 30, width = 80)#This makes a simple textbox for the scoreboard with the attributes mentioned
	scoreBox.place(relx = 0.5,rely = 0.5,anchor = CENTER)

	scoreboard = Scoreboard()#Load in the scoreboard to use
	scoreboard.LoadInScoreboard()

	scoreText = ""
	for i in range(0 ,scoreboard.numberOfScores):#Loops through every single score in the scorebaord and displays them. This way incase the number of scores on the board changes
		scoreBox.insert(INSERT,str(i + 1) + ".")#Will add the scoreboard text to the text box. The INSERT is the location of where to insert the text. This means to just insert it to the end
		#The part above will add the 1. or 2. or n. to each score to signify where they are in the rank
		scoreBox.insert(INSERT,scoreboard.scores[i].name + " : " + str(scoreboard.scores[i].score))#Will print their name and then score
		for j in range(0,3):
			scoreBox.insert(INSERT, "\n")#Will insert 3 lines between text to ensure each player entry is really spaced out

def OpenScoreboard():
	windowScoreboard = Tk()#Creates the scoreboard window
	SetUpScoreboard(windowScoreboard)#Will run and set up all textboxes for the scoreboard, Will also load in all of the players on the scoreboard
	windowScoreboard.mainloop()




#Main sub that runs the program
def BeginGame():
	windowMenu = Tk() #Creates a window

	SetUpMenu(windowMenu) #Will run the procedure and set up the menu correctly

	#Below is a test for adding a new player to a scoreboard
	# newPlayer = player()
	# newPlayer.name = "Kal"
	# newPlayer.score = 200

	# scoreboard = Scoreboard()
	# scoreboard.LoadInScoreboard()

	# scoreboard.AddScoreToScoreboard(newPlayer)

	windowMenu.mainloop() #Will put the window into a listening mode so that it waits for an event to happen. Without it will instantly close, this ensures the program remains open



BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet





