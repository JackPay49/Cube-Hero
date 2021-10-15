import tkinter
from tkinter import *

import tkinter.font as font #This will import the font changing part of tkinter and will assgin it to just the attribute "font"
# Will import everything from the tkinter library


def DisplayMenu():
	windowMenu = Tk() #Creates a window
	windowMenu.geometry("500x500")#Sets the size of the window
	windowMenu.title("Menu") #Sets the title of the window currently

	#Buttons
	fontTitle = tkinter.font.Font(size = 30) #This creates a new font called fontTitle that has the font size of 30
	fontButtons = tkinter.font.Font(size = 12) #This creates a new font called fontTitle that has the font size of 30


	btnLoadGame = Button(windowMenu,text = "Load Game")#Creates a basic button displaying text
	btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)#Will place the button relative to 0.1 of the width of the screen, 0,5 of the height of the screen and in the center
	btnLoadGame['font'] = fontButtons #Will set the font of the button to the standard button font

	btnCreateNewGame = Button(windowMenu,text = "Create new Game")
	btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
	btnCreateNewGame['font'] = fontButtons


	btnScoreboard = Button(windowMenu,text = "Scoreboard")
	btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = CENTER)
	btnScoreboard['font'] = fontButtons


	btnClose = Button(windowMenu,text = "Close")
	btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)
	btnClose['font'] = fontButtons


	lbTitle = Label(windowMenu,text = "Game Name!")#Creates a label, just the same type of commands as making a button
	lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)
	lbTitle['font'] = fontTitle


	windowMenu.mainloop() #Will put the window into a listening mode so that it waits for an event to happen. Without it will instantly close, this ensures the program remains open

DisplayMenu()



