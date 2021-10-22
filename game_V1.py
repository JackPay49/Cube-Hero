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
		file.write(str(self.controls) + "\n")
		file.close()
	def CreatePlayer(self,nValue,pValue):#Will create an object for the player with the values and will create their file & save it
		self.name = nValue
		self.password = pValue
		self.SavePlayer()

	def ResetControls(self):
		self.controls = ['w','a','s','d','e','b']
		self.SavePlayer()

class Menu(Tk):
	lbTitle = Label

	btnLoadGame = Button
	btnCreateNewGame = Button
	btnScoreboard = Button
	btnClose = Button
	
	def __init__(self):
		super().__init__()
		self.geometry("500x500")#Sets the size of the window
		self.title("Menu") #Sets the title of the window currently

		#fonts
		fontNormal = ("Default",12,"bold")

		self.lbTitle = TitleLabel(self,"Game Name!")

		#Buttons
		self.btnLoadGame = Button(self,text = "Load Game", command = lambda: (self.destroy(),LoadGame()),font = fontNormal)#Creates a basic button displaying text
		self.btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)#Will place the button relative to 0.1 of the width of the screen, 0,5 of the height of the screen and in the center

		self.btnCreateNewGame = Button(self,text = "Create new Game",command = lambda: (self.destroy(),NewGame()),font = fontNormal)
		self.btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = CENTER)


		self.btnScoreboard = Button(self,text = "Scoreboard",command = lambda: (self.destroy(),OpenScoreboard()),font = fontNormal)
		self.btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = CENTER)

		self.btnClose = BackButton(self,"Close",False)

		#
		self.mainloop()
def LoadGame():
	windowLogin = LoginScreen(False)#Opens the login screen. NewGame variable is set to false as we are loading a game
def NewGame():
	windowLogin = LoginScreen(True)#Opens the login screen. NewGame variable is set to true as we are making a new game
class LoginScreen(Tk):
	lbTitle = Label
	lbName = Label
	lbPassword = Label

	txtName = Entry
	txtPassword = Entry

	btnBeginGame = Button
	btnControls = Button
	btnClose = Button
	btnLogin = Button


	def __init__(self,newGame):
		super().__init__()
		myPlayer = player()
		self.geometry("600x600")
		if (newGame):#If its a new game then say instead to create a new account
			titleText = "Create a new Game"
		else:
			titleText = "Login"#Otherwise it should just say to load a game
		self.title(titleText)


		fontNormal = ("Default",12)
		fontBold = ("Default",12,"bold")


		self.lbTitle = TitleLabel(self,titleText)

		self.lbName = Label(self,text = "Name:",font = fontBold)
		self.lbName.place(relx = 0.2,rely = 0.2, anchor = CENTER)
		self.txtName = Entry(self,font = fontNormal)
		self.txtName.place(relx = 0.5,rely = 0.2, anchor = CENTER)

		self.lbPassword = Label(self,text = "Password:",font = fontBold)
		self.lbPassword.place(relx = 0.2,rely = 0.3, anchor = CENTER)
		self.txtPassword = Entry(self,show = "*",font = fontNormal)#show will changed this entry so that instead of actual text just * will be displayed for each character on screen for privacy
		self.txtPassword.place(relx = 0.5,rely = 0.3, anchor = CENTER)

		if (newGame):#If its a new game then make it a create account button
			self.btnLogin = Button(self,text = "Create new game",font = fontBold, command = lambda: self.CreateNewPlayer(myPlayer,self.txtName.get(),self.txtPassword.get()))#lambda used here otherwise the command will be initiated as soon as the button is made
		else:#Else if it is just loading a game then make a login button
			self.btnLogin = Button(self,text = "Login",font = fontBold, command = lambda: self.Login(myPlayer,self.txtName.get(),self.txtPassword.get()) )
		self.btnLogin.place(relx = 0.5,rely = 0.4, anchor = CENTER)

		self.btnBeginGame = Button(self,text = "Begin Game",command = lambda:(self.destroy(),OpenGameScreen(myPlayer)), font = fontBold)
		self.btnBeginGame.place(relx = 0.7,rely = 0.6,anchor = CENTER)

		self.btnControls = Button(self,text = "Controls",command = lambda:(OpenControlsScreen(myPlayer)), font = fontBold)
		self.btnControls.place(relx = 0.3,rely = 0.6, anchor = CENTER)

		self.btnClose = BackButton(self,"Back",True)
		self.mainloop()

	def Login(self,myPlayer,name,password):
		myPlayer.LoadPlayer(name)
		if (myPlayer.password == password):#If there password is correct
			messagebox.showinfo("Login","Logged in!")#Log them in, don't start game yet as they may want to do something else
		else:#Do nothing if it is wrong, let them enter it again
			messagebox.showinfo("Login","Password incorrect, try again!")
	def CreateNewPlayer(self,myPlayer,name,password):
		try:
			file = open("gameFiles/" + name + ".txt","xt")#Creates the file for the user. If it exists then this will cause and erorr thus triggering the Except statement
			file.close()
			myPlayer.CreatePlayer(name,password)
			messagebox.showinfo("Login","Account has been made!")

		except FileExistsError:#do nothing other than tell them that the name exists, let them reenter details
			messagebox.showinfo("Login","User already exists! Please use a different name")

class ScoreboardScreen(Tk):
	lbTitle = Label
	btnClose = Button
	scorebox = Text

	scoreboard = Scoreboard()
	def __init__(self):
		super().__init__()
		self.geometry("1000x700")
		self.title("Scoreboard")

		fontNormal = ("Default",12)

		self.lbTitle = TitleLabel(self,"Scoreboard")


		self.btnClose = BackButton(self,"Back",True)

		self.scoreBox = Text(self, font = fontNormal)#This makes a simple textbox for the scoreboard with the attributes mentioned
		self.scoreBox.place(relx = 0.5,rely = 0.5,anchor = CENTER)

		self.scoreboard.LoadInScoreboard()

		scoreText = ""
		for i in range(0 ,self.scoreboard.numberOfScores):#Loops through every single score in the scorebaord and displays them. This way incase the number of scores on the board changes
			self.scoreBox.insert(INSERT,str(i + 1) + ".")#Will add the scoreboard text to the text box. The INSERT is the location of where to insert the text. This means to just insert it to the end
			#The part above will add the 1. or 2. or n. to each score to signify where they are in the rank
			self.scoreBox.insert(INSERT,self.scoreboard.scores[i].name + " : " + str(self.scoreboard.scores[i].score))#Will print their name and then score
			for j in range(0,3):
				self.scoreBox.insert(INSERT, "\n")#Will insert 3 lines between text to ensure each player entry is really spaced out
		self.scoreBox.configure(state = 'disabled')#Makes the textbox read-only so that the user cannot edit it. Does this now as the text has been set
		self.mainloop()
def OpenScoreboard():
	windowScoreboard = ScoreboardScreen()

class GameScreen(Tk):
	def __init__(self):
		super().__init__()
		self.title("Game screen")
		self.geometry("1000x1000")
def OpenGameScreen(myPlayer):
	gameScreen = GameScreen()

class ControlsScreen(Tk):
	lbUpControl = Label
	lbRightControl = Label
	lbLeftControl = Label
	lbDownControl = Label
	lbPauseControl = Label
	lbBossControl = Label
	lbTitle = Label

	txtUpControl = Entry
	txtRightControl = Entry
	txtLeftControl = Entry
	txtDownControl = Entry
	txtPauseControl = Entry
	txtBossControl = Entry

	btnClose = Button
	btnResetControls = Button
	btnSaveChanges = Button

	def __init__(self,myPlayer):
		super().__init__()
		self.geometry("600x500")
		self.title("Controls")

		fontBold = ("Default",12,"bold")
		fontNormal = ("Default",12)


		self.lbTitle = TitleLabel(self,"Controls")

		self.lbUpControl = Label(self,text = "Up Control:",font = fontBold)
		self.lbUpControl.place(relx = 0.2,rely = 0.2, anchor = CENTER)
		self.txtUpControl = Entry(self,font = fontNormal)
		self.txtUpControl.place(relx = 0.5,rely = 0.2, anchor = CENTER)

		self.lbLeftControl = Label(self,text = "Left Control:",font = fontBold)
		self.lbLeftControl.place(relx = 0.2,rely = 0.3, anchor = CENTER)
		self.txtLeftControl = Entry(self,font = fontNormal)
		self.txtLeftControl.place(relx = 0.5,rely = 0.3, anchor = CENTER)


		self.lbDownControl = Label(self,text = "Down Control:",font = fontBold)
		self.lbDownControl.place(relx = 0.2,rely = 0.4, anchor = CENTER)
		self.txtDownControl = Entry(self,font = fontNormal)
		self.txtDownControl.place(relx = 0.5,rely = 0.4, anchor = CENTER)

		self.lbRightControl = Label(self,text = "Right Control:",font = fontBold)
		self.lbRightControl.place(relx = 0.2,rely = 0.5, anchor = CENTER)
		self.txtRightControl = Entry(self,font = fontNormal)
		self.txtRightControl.place(relx = 0.5,rely = 0.5, anchor = CENTER)

		self.lbPauseControl = Label(self,text = "Pause Control:",font = fontBold)
		self.lbPauseControl.place(relx = 0.2,rely = 0.6, anchor = CENTER)
		self.txtPauseControl = Entry(self,font = fontNormal)
		self.txtPauseControl.place(relx = 0.5,rely = 0.6, anchor = CENTER)

		self.lbBossControl = Label(self,text = "Boss Control:",font = fontBold)
		self.lbBossControl.place(relx = 0.2,rely = 0.7, anchor = CENTER)
		self.txtBossControl = Entry(self,font = fontNormal)
		self.txtBossControl.place(relx = 0.5,rely = 0.7, anchor = CENTER)

		self.DisplayControls(myPlayer)

		self.btnResetControls = Button(self,text = "Reset Controls" ,command = lambda:(self.ResetControls(myPlayer)),font = fontBold)
		self.btnResetControls.place(relx = 0.3,rely = 0.8,anchor = CENTER)

		self.btnSaveChanges = Button(self,text = "Save Changes" ,command = lambda:(self.SaveChanges(myPlayer)),font = fontBold)
		self.btnSaveChanges.place(relx = 0.7,rely = 0.8,anchor = CENTER)

		self.btnClose = BackButton(self,"Back",False)
		self.mainloop()

	def ResetControls(self,myPlayer):
		myPlayer.ResetControls()
		self.DisplayControls(myPlayer)

	def DisplayControls(self,myPlayer):
		self.txtUpControl.delete(0,"end")
		self.txtLeftControl.delete(0,"end")
		self.txtDownControl.delete(0,"end")
		self.txtRightControl.delete(0,"end")
		self.txtPauseControl.delete(0,"end")
		self.txtBossControl.delete(0,"end")

		self.txtUpControl.insert(0,myPlayer.controls[0])
		self.txtLeftControl.insert(0,myPlayer.controls[1])
		self.txtDownControl.insert(0,myPlayer.controls[2])
		self.txtRightControl.insert(0,myPlayer.controls[3])
		self.txtPauseControl.insert(0,myPlayer.controls[4])
		self.txtBossControl.insert(0,myPlayer.controls[5])


	def SaveChanges(self,myPlayer):
		myPlayer.controls[0] = self.txtUpControl.get().strip()
		myPlayer.controls[1] = self.txtLeftControl.get().strip()
		myPlayer.controls[2] = self.txtDownControl.get().strip()
		myPlayer.controls[3] = self.txtRightControl.get().strip()
		myPlayer.controls[4] = self.txtPauseControl.get().strip()
		myPlayer.controls[5] = self.txtBossControl.get().strip()
		myPlayer.SavePlayer()
		messagebox.showinfo("Saved!","Changes to controls have been saved!")


def OpenControlsScreen(myPlayer):
	if (myPlayer.name == ""):
		messagebox.showinfo("Error","Please Login first!")
	else:
		windowControlsScreen = ControlsScreen(myPlayer)

#Classees for general controls
class BackButton(Button):	
	def __init__(self,parentWindow,textValue,openMenu):
		super().__init__()
		self = Button(parentWindow,text = textValue,font = ("Default",12,"bold"))
		self.place(relx = 0.5, rely = 0.9, anchor = CENTER)
		#Below Will reopn the menu if the value of openMenu is true. This is so that screens like the controls screen don't open the menu but the login does
		if (openMenu):
			self.configure(command = lambda:(parentWindow.destroy(),BeginGame()))
		else:
			self.configure(command = lambda:(parentWindow.destroy()))
class TitleLabel(Label):
	def __init__(self,parentWindow,textValue):
		super().__init__()
		self = Label(parentWindow,text = textValue,font = ("Default",30,"bold","underline")) 
		self.place(relx = 0.5, rely = 0.1, anchor = CENTER)





#General Procedures
def ConvertToList(string):#This is used to convert a string containing a list to an actual list variable
	Mylist = []
	for i in range(0,len(string)):
		if ((string[i] != "[") and (string[i] != ",") and (string[i] != "]") and (string[i] != "'") and (string[i] != " ")):
			Mylist.append(string[i])
	return Mylist

#Main sub that runs the program
def BeginGame():
	windowMenu = Menu() 



BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet





