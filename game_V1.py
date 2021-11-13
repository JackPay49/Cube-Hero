import time,random
from tkinter import Tk, Button as btn, Label as lb, Canvas as cv, Text as txt, Entry as ent, PhotoImage as img, messagebox as msgb, CENTER as algncenter, ALL 
from snake import Snake
from powerup import PowerUp
#Screen Resolution is 1920x1080. All screens are smaller than or equal to this resolution.
screenWidth = 1920
screenHeight = 1080
screenResolution = (str(screenWidth) + "x" + str(screenHeight))

numberOfPowerUpTypes = 5

#Classes


class Scoreboard:

	scores = []
	maxNumberOfScores = 10
	numberOfScores = 0

	def SortScores(self,low,high):#This is a basic quicksort that sorts the algorithm from greatest score to smallest, 0 to 9. Based on the scores of each player
		tempLow = low
		tempHigh = high
		pivot = self.scores[int((low + high)/2)].highestScore
		while(tempLow <= tempHigh):
			while(self.scores[tempLow].highestScore > pivot and tempLow < high):
				tempLow += 1
			while(self.scores[tempHigh].highestScore < pivot and tempHigh > low):
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
		#This writes all scorebaorrd details into a text file. it will format them in the form of a name, then a score on a different line and then it will leave a blank line between different player scores.
		#At the top of the file there will also be the number of scores stored which is used to change how long the loop will search for scores in the file
		self.SortScores(0,(self.numberOfScores - 1))
		file = open("gameFiles/scoreboard.txt","w")
		file.write(str(self.numberOfScores))
		for i in range(0,len(self.scores)):
			file.write("\n" + self.scores[i].name)
			file.write("\n" + str(self.scores[i].highestScore))
			file.write("\n")
		file.close()

	def LoadInScoreboard(self):
		#This will load in details from the scoreboard. It reads the values for each player and puts them into a temporary player strcuture which is then added to the scoreabord list.
		self.scores = []
		file = open("gameFiles/scoreboard.txt","rt")
		self.numberOfScores = int(file.readline())
		for i in range(0,self.numberOfScores):
			tempPlayer = Player()
			tempPlayer.name = file.readline().strip()
			tempScore = int(file.readline())
			tempPlayer.score = tempScore
			tempPlayer.highestScore = tempScore
			file.readline()
			self.scores.append(tempPlayer)
		file.close()

	def AddScoreToScoreboard(self,newPlayer):
		#There are two possible cases to adding a score to the scorebaord. 1: the scoreboard is full already. If it is already full then it will compare to the last score in the scorebaord, the lowest. If the new
		#score is higher than that, it should be added and so replaces this last score. We then resort and save the scorebaord if it was added.
		#2: in this case the scorebaord isn't full. In this case the new score can just be added to the end of the scorebaord and it can be sorted and saved.
		self.RemoveScoreFromScoreboard(newPlayer)#This will first check to see if the player has already featured on the scorebaord. It will remove them if they have, to reposition them
		if (len(self.scores) >= self.maxNumberOfScores):
			if (newPlayer.highestScore > self.scores[self.maxNumberOfScores - 1].highestScore):
				self.scores[self.maxNumberOfScores - 1] = newPlayer
				self.SortScores(0,(self.numberOfScores - 1))
				self.SaveScoreboard()
		else:
			self.scores.append(newPlayer)
			self.numberOfScores += 1
			self.SortScores(0,(self.numberOfScores - 1))
			self.SaveScoreboard()

	def RemoveScoreFromScoreboard(self,myPlayer):
		i = 0
		while i < len(self.scores):
			if (self.scores[i].name == myPlayer.name):
					self.scores.remove(self.scores[i])
					self.numberOfScores -=1
			else:
				i+=1

class Player:
	name = ""
	score = 0
	highestScore = 0
	password = ""
	controls = ['w','a','s','d','e','b']#This stores the player controls for up, left, down, right, pause and boss screen respectively. These will be used when actraully assigning controls in the game screen
	midLevel = False#Midlevel is used to tell the program whether the player is mid way through a level already. If they are then it will actually load the level details in, but if they're not then it won't.

	snake = Snake("Player")

	def LoadPlayer(self,nValue):
		#This jsut loads in the details of the player. Important thing to note here is the loading of the controls. They are read in as a string and then a separate procedure will find the control values and
		#insert them into the array
		self.name = nValue
		file = open("gameFiles/" + self.name + ".txt","rt")
		file.readline()
		self.password = (file.readline()).strip()
		self.highestScore = int(file.readline())
		self.score = int(file.readline())
		midLevelState = file.readline().strip()
		self.controls = ConvertToList(file.readline())
		file.close()
		if (midLevelState == "1"):
			self.midLevel = True

	def SavePlayer(self):
		file = open("gameFiles/" + self.name + ".txt","wt")
		file.write(self.name + "\n")
		file.write(str(self.password) + "\n")
		file.write(str(self.highestScore) + "\n")
		if (self.midLevel == True):#In the player file the midlevel boolean is stored as either a 0 or 1
			file.write(str(self.score) + "\n")#The player score
			file.write("1\n")#whether they're in a game
		else:
			file.write("0\n")#score of 0
			file.write("0\n")
		file.write(str(self.controls) + "\n")
		file.close()

		scoreboard = Scoreboard()
		scoreboard.LoadInScoreboard()
		scoreboard.AddScoreToScoreboard(self)
		scoreboard = None

	def CreatePlayer(self,nValue,pValue):
		self.name = nValue
		self.password = pValue
		self.SavePlayer()

	def ResetControls(self):
		self.controls = ['w','a','s','d','e','b']
		self.SavePlayer()

	def CreateSnake(self,gameScreen,x,y,lValue):
		self.snake.GenerateSnakeBody(gameScreen,x,y,lValue)

	def IncreaseScore(self,amount):
		self.score += amount
		if (self.score > self.highestScore):
			self.highestScore = self.score

#Screen Classes:
class Menu(Tk):
	lbTitle = lb

	btnLoadGame = btn
	btnCreateNewGame = btn
	btnScoreboard = btn
	btnClose = btn

	def __init__(self):
		super().__init__()
		self.geometry("500x500")
		self.title("Menu")

		#fonts
		fontNormal = ("Default",12,"bold")

		self.lbTitle = TitleLabel(self,"Cube Hero!")

		#Buttons
		self.btnLoadGame = btn(self,text = "Load Game", command = lambda: (self.destroy(),LoadGame()),font = fontNormal)
		self.btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = algncenter)

		self.btnCreateNewGame = btn(self,text = "Create new Game",command = lambda: (self.destroy(),NewGame()),font = fontNormal)
		self.btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = algncenter)


		self.btnScoreboard = btn(self,text = "Scoreboard",command = OpenScoreboard,font = fontNormal)
		self.btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = algncenter)

		self.btnClose = BackButton(self,"Close",False)

		self.mainloop()
def LoadGame():
	windowLogin = LoginScreen(False)#Opens the login screen. NewGame variable is set to false as we are loading a game
def NewGame():
	windowLogin = LoginScreen(True)#Opens the login screen. NewGame variable is set to true as we are making a new game
class LoginScreen(Tk):
	lbTitle = lb
	lbName = lb
	lbPassword = lb

	txtName = ent
	txtPassword = ent

	btnBeginGame = btn
	btnControls = btn
	btnClose = btn
	btnLogin = btn
	btnRules = btn

	def __init__(self,newGame):
		#Important to note here. The newGame parameter is a boolean used to tell us whether the login screen should be to login or to create a new game. Based on this the title of the screen and the
		#function of the login button will be changed
		super().__init__()
		myPlayer = Player()
		self.geometry("600x600")
		if (newGame):
			titleText = "Create a new Game"
		else:
			titleText = "Login"
		self.title(titleText)


		fontNormal = ("Default",12)
		fontBold = ("Default",12,"bold")


		self.lbTitle = TitleLabel(self,titleText)

		self.lbName = lb(self,text = "Name:",font = fontBold)
		self.lbName.place(relx = 0.2,rely = 0.2, anchor = algncenter)
		self.txtName = ent(self,font = fontNormal)
		self.txtName.place(relx = 0.5,rely = 0.2, anchor = algncenter)

		self.lbPassword = lb(self,text = "Password:",font = fontBold)
		self.lbPassword.place(relx = 0.2,rely = 0.3, anchor = algncenter)
		self.txtPassword = ent(self,show = "*",font = fontNormal)
		self.txtPassword.place(relx = 0.5,rely = 0.3, anchor = algncenter)

		if (newGame):
			self.btnLogin = btn(self,text = "Create new game",font = fontBold, command = lambda: self.CreateNewPlayer(myPlayer,self.txtName.get(),self.txtPassword.get()))
		else:
			self.btnLogin = btn(self,text = "Login",font = fontBold, command = lambda: self.Login(myPlayer,self.txtName.get(),self.txtPassword.get()) )
		self.btnLogin.place(relx = 0.5,rely = 0.4, anchor = algncenter)

		self.btnBeginGame = btn(self,text = "Begin Game",command = lambda:(self.destroy(),OpenGameScreen(myPlayer)), font = fontBold)
		self.btnBeginGame.place(relx = 0.7,rely = 0.6,anchor = algncenter)

		self.btnControls = btn(self,text = "Controls",command = lambda:(OpenControlsScreen(myPlayer)), font = fontBold)
		self.btnControls.place(relx = 0.3,rely = 0.6, anchor = algncenter)

		self.btnRules = btn(self,text = "Rules",command = OpenRulesScreen, font = fontBold)
		self.btnRules.place(relx = 0.3,rely = 0.8, anchor = algncenter)

		self.btnClose = BackButton(self,"Back",True)
		self.mainloop()

	def Login(self,myPlayer,name,password):
		#This is a basic login function. It loads the player in and checks if their entered password matches the saved one
		myPlayer.LoadPlayer(name)
		if (myPlayer.password == password):
			msgb.showinfo("Login","Logged in!")
		else:
			msgb.showinfo("Login","Password incorrect, try again!")

	def CreateNewPlayer(self,myPlayer,name,password):
		#This sub will create a player file for the new player. Doing this will create an eror if the player exists already. Therefore this will be caught and an error message displayed. If it is a new player
		#Then the player will be made with the input name and password, and will be saved to the new file
		try:
			file = open("gameFiles/" + name + ".txt","xt")
			file.close()
			myPlayer.CreatePlayer(name,password)
			msgb.showinfo("Login","Account has been made!")

		except FileExistsError:
			msgb.showinfo("Login","User already exists! Please use a different name")

class ScoreboardScreen(Tk):
	lbTitle = lb
	btnClose = btn
	scorebox = txt

	scoreboard = Scoreboard()
	def __init__(self):
		super().__init__()
		self.geometry("1000x700")
		self.title("Scoreboard")

		self.lbTitle = TitleLabel(self,"Scoreboard")


		self.btnClose = BackButton(self,"Back",False)

		self.scoreBox = txt(self, font = ("Default",12))
		self.scoreBox.place(relx = 0.5,rely = 0.5,anchor = algncenter)

		self.DisplayScoreboard()
		self.mainloop()

	def DisplayScoreboard(self):
		#This procedure will load the scorebaord in. It will then format them into the text box on the screen in the fornat of 'placeOnScorebaord. Name: Score'. It will also make it so the scoreboard is read
		#only afterwards to prevent the player from altering scores
		self.scoreboard.LoadInScoreboard()
		scoreText = ""
		for i in range(0 ,self.scoreboard.numberOfScores):
			self.scoreBox.insert(tkinter.INSERT,str(i + 1) + ".")
			self.scoreBox.insert(tkinter.INSERT,self.scoreboard.scores[i].name + " : " + str(self.scoreboard.scores[i].score))
			self.scoreBox.insert(tkinter.INSERT, "\n")
			self.scoreBox.insert(tkinter.INSERT, "\n")
		self.scoreBox.configure(state = 'disabled')

def OpenScoreboard():
	windowScoreboard = ScoreboardScreen()

class PauseSceen(Tk):
	btnResumeGame =  btn
	btnSaveGame = btn
	btnControls = btn
	btnRules = btn
	btnScoreboard = btn
	btnBack = btn
	btnCheatCode = btn

	txtCheatCode = ent
	cheatCodes = []

	def __init__(self,parentWindow):
		super().__init__()
		self.geometry("300x700")
		self.title("Pause")

		fontButton = ("Default",12,"bold")
		fontNormal = ("Default",12)


		self.lbTitle = TitleLabel(self,"Game Pause")

		self.btnResumeGame = btn(self,text = "Resume Game",font = fontButton)
		self.btnResumeGame.place(relx = 0.5, rely = 0.2, anchor = algncenter)
		self.btnResumeGame.configure(command = lambda:(parentWindow.Unpause(),self.destroy()))

		self.btnSaveGame = btn(self,text = "Save Game",font = fontButton)
		self.btnSaveGame.place(relx = 0.5, rely = 0.3, anchor = algncenter)
		self.btnSaveGame.configure(command = parentWindow.SaveGame)

		self.btnControls = btn(self,text = "Controls",font = fontButton)
		self.btnControls.place(relx = 0.5, rely = 0.4, anchor = algncenter)
		self.btnControls.configure(command = lambda:(OpenControlsScreen(parentWindow.myPlayer)))

		self.btnRules = btn(self,text = "Rules",font = fontButton)
		self.btnRules.place(relx = 0.5, rely = 0.5, anchor = algncenter)
		self.btnRules.configure(command = OpenRulesScreen)

		self.btnScoreboard = btn(self,text = "Scoreboard",font = fontButton)
		self.btnScoreboard.place(relx = 0.5, rely = 0.6, anchor = algncenter)
		self.btnScoreboard.configure(command = OpenScoreboard)

		self.btnCheatCode = btn(self,text = "Enter Cheat Code",font = fontButton)
		self.btnCheatCode.place(relx = 0.5, rely = 0.7, anchor = algncenter)
		self.btnCheatCode.configure(command = lambda:(self.EnterCheatCode(parentWindow)))
		self.txtCheatCode = ent(self,font = fontNormal)
		self.txtCheatCode.place(relx = 0.5,rely = 0.8, anchor = algncenter)

		self.btnBack = btn(self,text = "Quit Game",font = fontButton)
		self.btnBack.place(relx = 0.5, rely = 0.9, anchor = algncenter)
		self.btnBack.configure(command = lambda:(self.destroy(),parentWindow.CloseWindow(True)))

		self.mainloop()

	def LoadInCheatCodes(self):
		file = open("gameFiles/cheatCodes.txt","r")
		numberOfCheatCodes = int(file.readline().strip())
		self.cheatCodes = []
		for i in range(numberOfCheatCodes):
			tempString = file.readline().strip()
			self.cheatCodes.append(tempString)

	def EnterCheatCode(self,gameScreen):
		self.LoadInCheatCodes()
		userInput = self.txtCheatCode.get().strip()
		if (self.cheatCodes[0] in userInput):
			gameScreen.myPlayer.snake.IncreaseLength(gameScreen,10)
		if (self.cheatCodes[1] in userInput):
			gameScreen.myPlayer.snake.DecreaseLength(gameScreen,10)		
		if (self.cheatCodes[2] in userInput):
			gameScreen.myPlayer.snake.IncreaseSpeed(3)		
		if (self.cheatCodes[3] in userInput):
			gameScreen.myPlayer.snake.DecreaseSpeed(3)		
		if (self.cheatCodes[4] in userInput):
			gameScreen.checkIfPlayerTooSmall = False
			gameScreen.myPlayer.snake.DecreaseLength(gameScreen,gameScreen.myPlayer.snake.length - 1)
			while (len(gameScreen.myPlayer.snake.turningPoints) > 0):
				gameScreen.myPlayer.snake.turningPoints.remove(gameScreen.myPlayer.snake.turningPoints[0])		
		if (self.cheatCodes[5] in userInput):
			gameScreen.pointModifier = 2500	
class RulesScreen(Tk):
	btnBack = btn

	lbTitle = lb

	txtRules = txt

	def __init__(self):
		super().__init__()
		self.geometry("700x700")
		self.title("Rules")

		lbTitle = TitleLabel(self,"Welcome to Cube Hero!")
		btnBack = BackButton(self,"Back",False)

		file = open("gameFiles/rules.txt","r")
		rules = file.read()
		file.close()

		self.txtRules = txt(self, font = ("Default",12))
		self.txtRules.place(relx = 0.5,rely = 0.5,anchor = algncenter)
		self.txtRules.insert(tkinter.INSERT,rules)
		self.txtRules.pack(pady = 100)

		self.mainloop()

def OpenRulesScreen():
	rulesScreen = RulesScreen()


class ControlsScreen(Tk):
	lbUpControl = lb
	lbRightControl = lb
	lbLeftControl = lb
	lbDownControl = lb
	lbPauseControl = lb
	lbBossControl = lb
	lbTitle = lb

	txtUpControl = ent
	txtRightControl = ent
	txtLeftControl = ent
	txtDownControl = ent
	txtPauseControl = ent
	txtBossControl = ent

	btnClose = btn
	btnResetControls = btn
	btnSaveChanges = btn
	btnInfo = btn

	def __init__(self,myPlayer):
		super().__init__()
		self.geometry("600x500")
		self.title("Controls")

		fontBold = ("Default",12,"bold")
		fontNormal = ("Default",12)


		self.lbTitle = TitleLabel(self,"Controls")

		self.lbUpControl = lb(self,text = "Up Control:",font = fontBold)
		self.lbUpControl.place(relx = 0.2,rely = 0.2, anchor = algncenter)
		self.txtUpControl = ent(self,font = fontNormal)
		self.txtUpControl.place(relx = 0.5,rely = 0.2, anchor = algncenter)

		self.lbLeftControl = lb(self,text = "Left Control:",font = fontBold)
		self.lbLeftControl.place(relx = 0.2,rely = 0.3, anchor = algncenter)
		self.txtLeftControl = ent(self,font = fontNormal)
		self.txtLeftControl.place(relx = 0.5,rely = 0.3, anchor = algncenter)


		self.lbDownControl = lb(self,text = "Down Control:",font = fontBold)
		self.lbDownControl.place(relx = 0.2,rely = 0.4, anchor = algncenter)
		self.txtDownControl = ent(self,font = fontNormal)
		self.txtDownControl.place(relx = 0.5,rely = 0.4, anchor = algncenter)

		self.lbRightControl = lb(self,text = "Right Control:",font = fontBold)
		self.lbRightControl.place(relx = 0.2,rely = 0.5, anchor = algncenter)
		self.txtRightControl = ent(self,font = fontNormal)
		self.txtRightControl.place(relx = 0.5,rely = 0.5, anchor = algncenter)

		self.lbPauseControl = lb(self,text = "Pause Control:",font = fontBold)
		self.lbPauseControl.place(relx = 0.2,rely = 0.6, anchor = algncenter)
		self.txtPauseControl = ent(self,font = fontNormal)
		self.txtPauseControl.place(relx = 0.5,rely = 0.6, anchor = algncenter)

		self.lbBossControl = lb(self,text = "Boss Control:",font = fontBold)
		self.lbBossControl.place(relx = 0.2,rely = 0.7, anchor = algncenter)
		self.txtBossControl = ent(self,font = fontNormal)
		self.txtBossControl.place(relx = 0.5,rely = 0.7, anchor = algncenter)

		self.DisplayControls(myPlayer) #This fills in all of the text boxes with the values of the controls

		self.btnResetControls = btn(self,text = "Reset Controls" ,command = lambda:(self.ResetControls(myPlayer)),font = fontBold)
		self.btnResetControls.place(relx = 0.2,rely = 0.8,anchor = algncenter)

		self.btnSaveChanges = btn(self,text = "Save Changes" ,command = lambda:(self.SaveChanges(myPlayer)),font = fontBold)
		self.btnSaveChanges.place(relx = 0.8,rely = 0.8,anchor = algncenter)

		self.btnInfo = btn(self,text = "Info" ,command = self.DisplayInfo,font = fontBold)
		self.btnInfo.place(relx = 0.5,rely = 0.8,anchor = algncenter)

		self.btnClose = BackButton(self,"Back",False)
		self.mainloop()

	def DisplayInfo(self):
		msgb.showinfo("Info","You can enter any characters here to set them as your controls for the game. Please note that the case of characters is taken into account. If you wish to use the Arrow keys you must enter 'Up', 'Left', 'Down' or 'Right depending on the key.")

	def ResetControls(self,myPlayer):
		#This procedure will set and save the player controls to the default. It then redisplays them on screen
		myPlayer.ResetControls()
		self.DisplayControls(myPlayer)

	def DisplayControls(self,myPlayer):
		# This procedure will delete all of the text within the entry controls and will then re-insert all of the player controls. Must do this due to the entry control
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
		#This procedure gets the text fromm all of the entries, strips away any white space connected to the controls and will then fill in the player controls list.
		myPlayer.controls[0] = self.txtUpControl.get().strip()
		myPlayer.controls[1] = self.txtLeftControl.get().strip()
		myPlayer.controls[2] = self.txtDownControl.get().strip()
		myPlayer.controls[3] = self.txtRightControl.get().strip()
		myPlayer.controls[4] = self.txtPauseControl.get().strip()
		myPlayer.controls[5] = self.txtBossControl.get().strip()
		myPlayer.SavePlayer()
		msgb.showinfo("Saved!","Changes to controls have been saved!")
def OpenControlsScreen(myPlayer):
	#This procedure only displays if the player is logged in as we need their controls, without that this screen is useless
	if (myPlayer.name == ""):
		msgb.showinfo("Error","Please Login first!")
	else:
		windowControlsScreen = ControlsScreen(myPlayer)

#Classees for general controls
class BackButton(btn):
	#This is a reusable back button. It will position itself in the same and correct place on screen each time. It's text will change based on the input parameter as some back buttons must say back
	#Whilst others need to say quit. It also takes the boolean value of openMenu which is used to tell whether we should reopen the menu after closing the parentwindow (the window it is put into)
	# So if that value is true then it will reopen the menu like for the login screen
	def __init__(self,parentWindow,textValue,openMenu):
		super().__init__()
		self = btn(parentWindow,text = textValue,font = ("Default",12,"bold"))
		self.place(relx = 0.5, rely = 0.9, anchor = algncenter)
		if (openMenu):
			self.configure(command = lambda:(parentWindow.destroy(),BeginGame()))
		else:
			self.configure(command = lambda:(parentWindow.destroy()))
class TitleLabel(lb):
	#This is a reusable title label. It will fomrat and position the label correctly on the screen and will fill in the text based on the input parameter
	def __init__(self,parentWindow,textValue):
		super().__init__()
		self = lb(parentWindow,text = textValue,font = ("Default",30,"bold","underline"))
		self.place(relx = 0.5, rely = 0.1, anchor = algncenter)

#Main game
class GameScreen(Tk):
	background = cv

	lbScore = lb
	txtScore = ent

	backgroundWidth = 800
	backgroundHeight = 800
	numberOfVerticalLines = 50
	numberOfHorizontalLines = 50

	gameCycleLength = 200 #In milliseconds
	gameCycleCount = 0;

	myPlayer = Player()

	gameOver = False
	paused = False

	checkIfPlayerTooSmall = True

	powerUps = []
	powerUpImages = []

	pointModifier = 1

	enemySnakes = []

	def __init__(self,myPlayer):
		super().__init__()
		self.enemySnakes = []
		self.powerUps = []
		self.powerUpImages = []
		self.title("Game screen")
		self.geometry(screenResolution)

		self.background = cv(self,width = self.backgroundWidth,height = self.backgroundHeight)
		self.background.place(relx = 0.5,rely = 0.5, anchor = algncenter)
		self.background.configure(bg = 'black')
		self.background.pack()

		self.lbScore = lb(self,text = "Score: ",font = ("Default",20,"bold"))
		self.lbScore.place(relx = 0.4,rely = 0.95,anchor = algncenter)
		self.txtScore = ent(self,font = ("Default",20,"bold"))
		self.txtScore.place(relx = 0.6,rely = 0.95,anchor = algncenter)

		self.myPlayer = myPlayer
		if (self.myPlayer.midLevel == False): #Here if the player is mid way through the level, only then will their game be loaded in and
		#displayed. If they're not midlevel then they will always be randomly placed and be given a length of 3
			self.myPlayer.snake = Snake("Player")
			self.myPlayer.snake.length = 3
			self.myPlayer.snake.turningPoints = []
			self.myPlayer.snake.body = []
			self.myPlayer.snake.RandomlyPlace(self)
		else:
			self.LoadGame()
		self.DisplaySnake(self.myPlayer.snake)

		self.SetUpControls()
		self.StartGameCycle()

	def SetUpControls(self):
		#This procedure makes all of the keybinds to be used in game. It makes them using what the player input for their controls
		self.bind(("<" + self.myPlayer.controls[0] + ">"),self.myPlayer.snake.UpAction)
		self.bind(("<" + self.myPlayer.controls[1] + ">"),self.myPlayer.snake.LeftAction)
		self.bind(("<" + self.myPlayer.controls[2] + ">"),self.myPlayer.snake.DownAction)
		self.bind(("<" + self.myPlayer.controls[3] + ">"),self.myPlayer.snake.RightAction)
		self.bind(("<" + self.myPlayer.controls[4] + ">"),self.Pause)
		self.bind(("<" + self.myPlayer.controls[5] + ">"),self.BossScreen)

	def RemoveControls(self):
		self.unbind(("<" + self.myPlayer.controls[0] + ">"))
		self.unbind(("<" + self.myPlayer.controls[1] + ">"))
		self.unbind(("<" + self.myPlayer.controls[2] + ">"))
		self.unbind(("<" + self.myPlayer.controls[3] + ">"))
		self.unbind(("<" + self.myPlayer.controls[4] + ">"))
		self.unbind(("<" + self.myPlayer.controls[5] + ">"))

	def Pause(self,event):
		#This procedure pauses the game, opens the pause screen but also gets rid of all keybinds. This is incase they are changed within the
		#the pause menu. This is so that the controls can be reassgined again
		self.paused = True
		self.RemoveControls()
		pauseMenu = PauseSceen(self)

	def Unpause(self):
		self.paused = False
		self.SetUpControls()
		self.StartGameCycle()

	def BossScreen(self,event):
		#This procedure is used whenever the player uses the boss screen control. It will make the screen the boss screen or undo the boss 
		#screen based on the current state. It works the same as pausing the game except it also will paste an image of a word document to 
		#make it look like work is being done.
		if (self.paused == True):
			self.background.configure(width = self.backgroundWidth,height = self.backgroundHeight)
			self.lbScore.place(relx = 0.4,rely = 0.95,anchor = algncenter)
			self.txtScore.place(relx = 0.6,rely = 0.95,anchor = algncenter)			
			self.Unpause()
		else:
			self.paused = True
			self.background.configure(width = screenWidth,height = screenHeight)
			self.image = img(file = "gameRes/bossScreen.png")
			self.background.create_image((screenWidth/2),(screenHeight/2),image = self.image)
			self.txtScore.place_forget()#These two commands are used to hide the score parts
			self.lbScore.place_forget()



	def DisplaySnake(self,snake):
		#This will display a specific snake onto the screen. It calculates the position on the baord of each section of the snake based on the
		#canvas width and the number of grid lines and will draw each body section onto the canvas. This is used every single game cycle
		gridBoxWidth = self.backgroundWidth/self.numberOfHorizontalLines
		for i in range(0,snake.length):
			leftCornerX = snake.body[i].x * gridBoxWidth
			leftCornerY = snake.body[i].y * gridBoxWidth
			rightCornerX = (snake.body[i].x + 1) * gridBoxWidth
			rightCornerY = (snake.body[i].y + 1) * gridBoxWidth

			self.background.create_rectangle(leftCornerX,leftCornerY,rightCornerX,rightCornerY,outline = "black",fill = snake.color)

	def StartGameCycle(self):
		#This procedure does the game loop. On every iteration it clears the entire board, moves each of the snakes and will then redraw all of the
		#snakes in their new positions. The final instruction is used to make the delay between moves and to carry on the iterative procedure.
		if ((not self.paused) and (not self.gameOver)):
			self.CheckForDeadEnemySnakes()

			self.myPlayer.snake.Move(self)

			for i in range(len(self.enemySnakes)):
				if (not self.gameOver):
					self.enemySnakes[i].DoEnemySnakeMove(self)

			self.CheckIfSnakesTooSmall()
			
			if (not self.gameOver):

				self.DisplayAllElements()

				self.IncreasePlayerScore()

				self.AddEnemySnake()

				self.gameCycleCount +=1
				self.AddPowerUps()
				self.after(self.gameCycleLength,self.StartGameCycle)

	def GameOver(self):
		#This procedure is used to end the game, like if the player collides witht their own body or a wall. It will delete everything on the
		#canvas and will close the window. It then also reopens the menu window.
		self.background.delete(ALL)
		self.DisplayAllElements()

		self.myPlayer.midLevel = False
		self.myPlayer.SavePlayer()
		msgb.showinfo("Game Over","GAME OVER!!!!")
		self.gameOver = True
		self.CloseWindow(False)

	def DisplayAllElements(self):
		self.background.delete(ALL)
		self.DisplaySnake(self.myPlayer.snake)
		for i in range(len(self.enemySnakes)):
			self.DisplaySnake(self.enemySnakes[i])
		self.DisplayPowerUps()


	def CloseWindow(self,askToSave):
		#This will check if the player wants to save on certain occasions. This is because we don't need to save if they lose a round of the game
		saveGame = ""
		if (askToSave):
			saveGame = msgb.askquestion("Quit","Would you like to save your progress?")
			if (saveGame == 'yes'):
				self.SaveGame()
		self.background.delete(ALL)
		self.destroy()
		BeginGame()

	def AddPowerUps(self):
		#Every 10 game cycles a new powerup will be added to the screen
		if ((self.gameCycleCount % 20)== 0):
			self.gameCycleCount == 0
			self.powerUps.append(PowerUp(self))

	def DisplayPowerUps(self):
		#This just displays and paints each of the powerups on the screen in the same way that snakes are
		gridBoxWidth = self.backgroundWidth/self.numberOfHorizontalLines
		for i in range(0,len(self.powerUps)):
			leftCornerX = (self.powerUps[i].position.x + 0.5) * gridBoxWidth
			leftCornerY = (self.powerUps[i].position.y + 0.5) * gridBoxWidth

			self.powerUpImages.append(img(file = "gameRes/" + self.powerUps[i].powerUpType +".gif"))
			self.background.create_image(leftCornerX,leftCornerY,image = self.powerUpImages[len(self.powerUpImages) - 1])
	def CheckIfSnakesTooSmall(self):
		if (self.checkIfPlayerTooSmall):
			if (self.myPlayer.snake.length <= 2):
				self.GameOver()
		for i in range(len(self.enemySnakes)):
			if (self.enemySnakes[i].length <=2):
				self.enemySnakes[i].KillSnake(self)

	def LoadGame(self):
		#This procedure will load in the player, their snake and the full gameboard. The only detail from the game bpard to really load in is all of the powerups on the
		#screen
		self.myPlayer.LoadPlayer(self.myPlayer.name)
		self.myPlayer.snake.LoadSnake(self,self.myPlayer)
		file = open("gameFiles/" + self.myPlayer.name + "Level.txt","r")

		self.powerUps = []
		number = int(file.readline().strip())
		for i in range(number):
			xPosition =  int(file.readline().strip())
			yPosition =  int(file.readline().strip())
			tempType =  file.readline().strip()
			newPowerup = PowerUp(self)
			newPowerup.MakePowerUp(xPosition,yPosition,tempType)
			self.powerUps.append(newPowerup)

		file.readline()

		number = int(file.readline().strip())
		self.enemySnakes = []
		for i in range(number):
			tempSnake = Snake("Enemy")
			tempSnake.length = int(file.readline().strip())
			tempSnake.body = []
			tempSnake.turningPoints = []
			for j in range(tempSnake.length):
				xPosition = int(file.readline().strip())
				yPosition = int(file.readline().strip())
				facing = file.readline().strip()

				tempSnake.body.append(Block(xPosition,yPosition,facing))

			file.readline()

			numberOfTurningPoints = int(file.readline().strip())
			for j in range(numberOfTurningPoints):
				xPosition = int(file.readline().strip())
				yPosition = int(file.readline().strip())
				facing = file.readline().strip()

				tempSnake.turningPoints.append(Block(xPosition,yPosition,facing))

			tempSnake.speed = int(file.readline().strip())

			self.enemySnakes.append(tempSnake)
		file.close()

	def SaveGame(self):
		self.myPlayer.midLevel = True
		self.myPlayer.SavePlayer()
		self.myPlayer.snake.SaveSnake(self.myPlayer)
		file = open("gameFiles/" + self.myPlayer.name + "Level.txt","w")

		file.write(str(len(self.powerUps)) + "\n")
		for i in range(len(self.powerUps)):
			file.write(str(self.powerUps[i].position.x) + "\n")
			file.write(str(self.powerUps[i].position.y) + "\n")
			file.write(self.powerUps[i].powerUpType + "\n")

		file.write("\n")

		file.write(str(len(self.enemySnakes)) + "\n")
		for i in range(len(self.enemySnakes)):
			file.write(str(self.enemySnakes[i].length) + "\n")
			for j in range(self.enemySnakes[i].length):
				file.write(str(self.enemySnakes[i].body[j].x) + "\n")
				file.write(str(self.enemySnakes[i].body[j].y) + "\n")
				file.write(self.enemySnakes[i].body[j].facing + "\n")

			file.write("\n")

			file.write(str(len(self.enemySnakes[i].turningPoints)) + "\n")
			for j in range(len(self.enemySnakes[i].turningPoints)):
				file.write(str(self.enemySnakes[i].turningPoints[j].x) + "\n")
				file.write(str(self.enemySnakes[i].turningPoints[j].y) + "\n")
				file.write(self.enemySnakes[i].turningPoints[j].facing + "\n")

			file.write(str(self.enemySnakes[i].speed) + "\n")

		file.close()
		msgb.showinfo("Saved","Game has been saved!")

	def DisplayScore(self):
		self.txtScore.delete(0,"end")
		self.txtScore.insert(0,self.myPlayer.score)

	def IncreasePlayerScore(self):
		#This will increase the players score by 1 times by each extra body length they are on top of the base 3
		if (self.gameOver != True):
			if (self.pointModifier != 2500):
				self.pointModifier = self.myPlayer.snake.length - 2
			self.myPlayer.IncreaseScore(self.pointModifier)
			self.DisplayScore()

	def AddEnemySnake(self):
		if (len(self.enemySnakes) < 2):
			chance = random.randint(0,10)
			if (chance == 0):
				tempSnake = Snake("Enemy")
				tempSnake.body = []
				tempSnake.turningPoints = []
				tempSnake.RandomlyGenerate(self)
				self.enemySnakes.append(tempSnake)

	def CheckForDeadEnemySnakes(self):
		i = 0
		while (i < len(self.enemySnakes)):
			if (self.enemySnakes[i].moving == False):#Enemy snake will be still if they are dead. Only then remove them
				self.enemySnakes.remove(self.enemySnakes[i])
			else:
				i += 1



def OpenGameScreen(myPlayer):
	gameScreen = GameScreen(myPlayer)

#General Procedures
def ConvertToList(string):#This is used to convert a string containing a list to an actual list variable
	#This is used to convert a string to a list. It will move through each item skipping them if they are any of the list
	#parts like [], etc. If they are not those characters it will add them to a temp string value. This is to allow longer
	# strings for the controls. When the end of these strings have been reached, so when they're not blank and there's
	# the second ' from ['a'] only then will it add the string to the list aas the current control. Must also reset the
	# value of the temp item here
	Mylist = []
	currentItem = ""
	for i in range(0,len(string)):
		if ((string[i] != "[") and (string[i] != ",") and (string[i] != "]") and (string[i] != "'") and (string[i] != " ")):
			currentItem += string[i]
		elif ((string[i] == "'") and (currentItem != "")):
			Mylist.append(currentItem)
			currentItem = ""
	return Mylist

#Main sub that runs the program
def BeginGame():
	global screenResolution,screenWidth,screenHeight, numberOfPowerUpTypes
	windowMenu = Menu()



BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet
