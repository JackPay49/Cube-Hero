import tkinter
from tkinter import * 
# Will import everything from the tkinter library

windowMenu = Tk() #Creates a window
windowMenu.geometry("500x500")#Sets the size of the window
windowMenu.title("Menu") #Sets the title of the window currently

#Buttons
btnLoadGame = Button(windowMenu,text = "Load Game")#Creates a basic button displaying text
btnLoadGame.place(relx = 0.5, rely = 0.2, anchor = CENTER)#Will place the button relative to 0.1 of the width of the screen, 0,5 of the height of the screen and in the center

windowMenu.mainloop() #Will put the window into a listening mode so that it waits for an event to happen. Without it will instantly close, this ensures the program remains open



