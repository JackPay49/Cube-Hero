import tkinter
from tkinter import *

import tkinter.font as font #This will import the font changing part of tkinter and will assgin it to just the attribute "font"
# Will import everything from the tkinter library

#Classes
# class snake:

# class player:

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
	# scoreBox.config(state = "disabled")#Will disable the text box so that the user cannot change what's in it

	player1 = {"name":"Jack","score":1000}#Test data below
	player2 = {"name":"Mark","score":100}
	player3 = {"name":"Phil","score":10}
	scores = [player1,player3,player2]
	SortScores(scores)#Ensures to order the data incase it isn't currently in order

	numberOfScores = 3
	scoreText = ""
	for i in range(0 ,numberOfScores):
		scoreBox.insert(INSERT,str(i + 1) + ".")#Will add the scoreboard text to the text box. The INSERT is the location of where to insert the text. This means to just insert it to the end
		#The part above will add the 1. or 2. or n. to each score to signify where they are in the rank
		scoreBox.insert(INSERT,scores[i].get("name") + " : " + str(scores[i].get("score")))#Will print their name and then score
		for j in range(0,3):
			scoreBox.insert(INSERT, "\n")#Will insert 3 lines between text to ensure each player entry is really spaced out


def SortScores(scores):
	for i in range(0,len(scores)):
		print("Sort Scores!") #Placeholder for now



def OpenScoreboard():
	windowScoreboard = Tk()#Creates the scoreboard window
	SetUpScoreboard(windowScoreboard)#Will run and set up all textboxes for the scoreboard, Will also load in all of the players on the scoreboard
	windowScoreboard.mainloop()

def BeginGame():
	windowMenu = Tk() #Creates a window
	SetUpMenu(windowMenu) #Will run the procedure and set up the menu correctly
	windowMenu.mainloop() #Will put the window into a listening mode so that it waits for an event to happen. Without it will instantly close, this ensures the program remains open



BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet





