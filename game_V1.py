import tkinter
from tkinter import *
from tkinter import messagebox#imports the messagebox library specifically so that it can be used to output messages
# Will import everything from the tkinter library

#Classes
# class snake:

class Scoreboard:

	scores = []
	maxNumberOfScores = 10
	numberOfScores = 0

	def SortScores(self,low,high):#This is a basic quicksort that sorts the algorithm from greatest score to smallest, 0 to 9. Based on the scores of each player
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
	password = ""#Stores their password to be used to login and out
	controls = ['w','a','s','d','e','b']#This stores the player controls for up, left, down, right, pause and boss screen respectively
	# playerSnake = snake()

	def LoadPlayer(self,nValue):
		self.name = nValue
		file = open("gameFiles/" + self.name + ".txt","rt")#This will open a file for reading in the text format based on the input name of the user
		
		file.readline()#Used to skip the name which is written into the file for readability
		self.password = (file.readline()).strip()#Gets rid of white space too
		self.level = int(file.readline())#Gets their level and score & converts them into integers
		self.score = int(file.readline())
		self.controls = ConvertToList(file.readline())
		file.close()#Must close the file afterwards!

	def SavePlayer(self):
		file = open("gameFiles/" + self.name + ".txt","wt")#Remakes the file
		file.write(self.name + "\n")
		file.write(str(self.password) + "\n")
		file.write(str(self.level) + "\n")
		file.write(str(self.score) + "\n")
		file.write(self.controls + "\n")
		file.close()
	def CreatePlayer(self,nValue,pValue):#Will create an object for the player with the values and will create their file & save it
		self.name = nValue
		self.password = pValue
		self.SavePlayer()

#Setting up Windows
class Menu(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("500x500")#Sets the size of the window
		self.title("Menu") #Sets the title of the window currently

		#fonts
		fontTitle = ("Default",30,"bold")
		fontNormal = ("Default",12)

		#Buttons
		btnLoadGame = Button(self,text = "Load Game", command = lambda: (self.destroy(),LoadGame()),font = fontNormal)#Creates a basic button displaying text
		btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)#Will place the button relative to 0.1 of the width of the screen, 0,5 of the height of the screen and in the center

		btnCreateNewGame = Button(self,text = "Create new Game",command = lambda: (self.destroy(),NewGame()),font = fontNormal)
		btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = CENTER)


		btnScoreboard = Button(self,text = "Scoreboard",command = lambda: (self.destroy(),OpenScoreboard()),font = fontNormal)
		btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = CENTER)


		btnClose = Button(self,text = "Close",command = self.destroy,font = fontNormal) #This binds the command to close the screen to this button. We can instead specify procedures here
		btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)

		#labels
		lbTitle = Label(self,text = "Game Name!",font = fontTitle)#Creates a label, just the same type of commands as making a button
		lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)
		self.mainloop()
def LoadGame():
	windowLogin = LoginScreen(False)#Opens the login screen. NewGame variable is set to false as we are loading a game
def NewGame():
	windowLogin = LoginScreen(True)#Opens the login screen. NewGame variable is set to true as we are making a new game
class LoginScreen(Tk):
	def __init__(self,newGame):
		super().__init__()
		myPlayer = player()
		self.geometry("600x600")
		if (newGame):#If its a new game then say instead to create a new account
			titleText = "Create a new Game"
		else:
			titleText = "Login"#Otherwise it should just say to load a game
		self.title(titleText)


		fontTitle = ("Default",30,"bold","underline")
		fontNormal = ("Default",12)
		fontBold = ("Default",12,"bold")


		lbTitle = Label(self, text = titleText, font = fontTitle)
		lbTitle.place(relx = 0.5,rely = 0.05,anchor = CENTER)

		lbName = Label(self,text = "Name:",font = fontBold)
		lbName.place(relx = 0.2,rely = 0.2, anchor = CENTER)
		txtName = Entry(self,font = fontNormal)
		txtName.place(relx = 0.5,rely = 0.2, anchor = CENTER)

		lbPassword = Label(self,text = "Password:",font = fontBold)
		lbPassword.place(relx = 0.2,rely = 0.3, anchor = CENTER)
		txtPassword = Entry(self,show = "*",font = fontNormal)#show will changed this entry so that instead of actual text just * will be displayed for each character on screen for privacy
		txtPassword.place(relx = 0.5,rely = 0.3, anchor = CENTER)

		if (newGame):#If its a new game then make it a create account button
			btnLogin = Button(self,text = "Create new game",font = fontBold, command = lambda: CreateNewPlayer(myPlayer,txtName.get(),txtPassword.get()))#lambda used here otherwise the command will be initiated as soon as the button is made
		else:#Else if it is just loading a game then make a login button
			btnLogin = Button(self,text = "Login",font = fontBold, command = lambda: Login(myPlayer,txtName.get(),txtPassword.get()) )
		btnLogin.place(relx = 0.5,rely = 0.4, anchor = CENTER)

		btnBeginGame = Button(self,text = "Begin Game",command = lambda:(self.destroy(),OpenGameScreen(myPlayer)), font = fontBold)
		btnBeginGame.place(relx = 0.5,rely = 0.6,anchor = CENTER)

		btnControls = Button(self,text = "Controls",command = lambda:(OpenControlsScreen(myPlayer)), font = fontBold)
		btnControls.place(relx = 0.3,rely = 0.8, anchor = CENTER)

		btnClose = Button(self,text = "Back",command = lambda: (self.destroy(), BeginGame()), font = fontBold)
		btnClose.place(relx = 0.7, rely = 0.8, anchor = CENTER)
		self.mainloop()

#All scoreboard stuff
class ScoreboardScreen(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("1000x700")
		self.title("Scoreboard")

		fontTitle = ("Default",30,"bold")
		fontNormal = ("Default",12)

		lbTitle = Label(self,text = "Scoreboard", font = fontTitle)
		lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)


		btnClose = Button(self,text = "Back",command = lambda: (self.destroy(),BeginGame()), font = fontNormal)
		btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)

		scoreBox = Text(self, font = fontNormal)#This makes a simple textbox for the scoreboard with the attributes mentioned
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
		scoreBox.configure(state = 'disabled')#Makes the textbox read-only so that the user cannot edit it. Does this now as the text has been set
		self.mainloop()
def OpenScoreboard():
	windowScoreboard = ScoreboardScreen()

	

def Login(myPlayer,name,password):
	myPlayer.LoadPlayer(name)
	if (myPlayer.password == password):#If there password is correct
		messagebox.showinfo("Login","Logged in!")#Log them in, don't start game yet as they may want to do something else
	else:#Do nothing if it is wrong, let them enter it again
		messagebox.showinfo("Login","Password incorrect, try again!")
def CreateNewPlayer(myPlayer,name,password):
	try:
		file = open("gameFiles/" + name + ".txt","xt")#Creates the file for the user. If it exists then this will cause and erorr thus triggering the Except statement
		file.close()
		myPlayer.CreatePlayer(name,password)
		messagebox.showinfo("Login","Account has been made!")

	except FileExistsError:#do nothing other than tell them that the name exists, let them reenter details
		messagebox.showinfo("Login","User already exists! Please use a different name")

def OpenGameScreen(myPlayer):
	print("Open Game screen")

#All control screen stuff below
class ControlsScreen(Tk):
	def __init__(self,myPlayer):
		super().__init__()
		self.geometry("600x500")
		self.title("Controls")

		fontTitle = ("Default",30,"bold","underline")
		fontNormal = ("Default",12)
		fontBold = ("Default",12,"bold")

		lbTitle = Label(self,text = "Controls", font = fontTitle)
		lbTitle.place(relx = 0.5, rely = 0.1, anchor = CENTER)

		lbUpControl = Label(self,text = "Up Control:",font = fontBold)
		lbUpControl.place(relx = 0.2,rely = 0.2, anchor = CENTER)
		txtUpControl = Entry(self,font = fontNormal)
		txtUpControl.place(relx = 0.5,rely = 0.2, anchor = CENTER)
		txtUpControl.insert(0,myPlayer.controls[0])

		lbLeftControl = Label(self,text = "Left Control:",font = fontBold)
		lbLeftControl.place(relx = 0.2,rely = 0.3, anchor = CENTER)
		txtLeftControl = Entry(self,font = fontNormal)
		txtLeftControl.place(relx = 0.5,rely = 0.3, anchor = CENTER)
		txtLeftControl.insert(0,myPlayer.controls[1])


		lbDownControl = Label(self,text = "Down Control:",font = fontBold)
		lbDownControl.place(relx = 0.2,rely = 0.4, anchor = CENTER)
		txtDownControl = Entry(self,font = fontNormal)
		txtDownControl.place(relx = 0.5,rely = 0.4, anchor = CENTER)
		txtDownControl.insert(0,myPlayer.controls[2])

		lbRightControl = Label(self,text = "Right Control:",font = fontBold)
		lbRightControl.place(relx = 0.2,rely = 0.5, anchor = CENTER)
		txtRightControl = Entry(self,font = fontNormal)
		txtRightControl.place(relx = 0.5,rely = 0.5, anchor = CENTER)
		txtRightControl.insert(0,myPlayer.controls[2])

		lbPauseControl = Label(self,text = "Pause Control:",font = fontBold)
		lbPauseControl.place(relx = 0.2,rely = 0.6, anchor = CENTER)
		txtPauseControl = Entry(self,font = fontNormal)
		txtPauseControl.place(relx = 0.5,rely = 0.6, anchor = CENTER)
		txtPauseControl.insert(0,myPlayer.controls[3])

		lbBossControl = Label(self,text = "Boss Control:",font = fontBold)
		lbBossControl.place(relx = 0.2,rely = 0.7, anchor = CENTER)
		txtBossControl = Entry(self,font = fontNormal)
		txtBossControl.place(relx = 0.5,rely = 0.7, anchor = CENTER)
		txtBossControl.insert(0,myPlayer.controls[4])

		btnResetControls = Button(self,text = "Reset Controls" ,font = fontBold)
		btnResetControls.place(relx = 0.3,rely = 0.8,anchor = CENTER)

		btnClose = Button(self,text = "Back",command = lambda: (self.destroy()), font = fontBold)
		btnClose.place(relx = 0.5, rely = 0.9, anchor = CENTER)
		self.mainloop()
def OpenControlsScreen(myPlayer):
	if (myPlayer.name == ""):
		messagebox.showinfo("Error","Please Login first!")
	else:
		windowControlsScreen = ControlsScreen(myPlayer)

#General Procedures
def ConvertToList(string):#This is used to convert a string containing a list to an actual list variable
	Mylist = []
	for i in range(0,len(string)):
		if ((string[i] != "[") and (string[i] != ",") and (string[i] != "]") and (string[i] != "'")):
			Mylist.append(string[i])
	return Mylist

#Main sub that runs the program
def BeginGame():
	windowMenu = Menu() 



BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet





