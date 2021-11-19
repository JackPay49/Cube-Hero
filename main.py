import time,random
from tkinter import Tk, Button as btn, Label as lb, Canvas as cv, Text as txt, Entry as ent, PhotoImage, messagebox as msgb, CENTER as algncenter, ALL, INSERT
from game_classes import Snake, Block as blk, Player, PowerUp, Scoreboard as scrb
#All images are original and made by myself
#Screen Resolution is 1920x1080. All screens are smaller than or equal to this resolution.
screenWidth = 1920
screenHeight = 1080
screenResolution = (str(screenWidth) + "x" + str(screenHeight))

#Main game
class GameScreen(Tk):
	background = cv

	lbScore = lb
	txtScore = ent

	backgroundWidth = 800
	backgroundHeight = 800
	numberOfVerticalLines = 50
	numberOfHorizontalLines = 50
	gridBoxWidth = backgroundWidth / numberOfVerticalLines


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

	entitiesToRemove = []

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
		if (self.myPlayer.midLevel == False): #Here if the player is mid way through the level, only then will their game be loaded in and displayed. If they're not midlevel then they will always be randomly placed and be given a length of 3
			self.myPlayer.snake = Snake("Player")
			self.myPlayer.snake.length = 3
			self.myPlayer.snake.turningPoints = []
			self.myPlayer.snake.body = []
			self.myPlayer.snake.RandomlyPlace(self)
		else:
			self.LoadGame()
		# self.DisplaySnake(self.myPlayer.snake)

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
		#This procedure pauses the game, opens the pause screen but also gets rid of all keybinds. This is incase they are changed within the the pause menu. This is so that the controls can be reassgined again
		self.paused = True
		self.RemoveControls()
		pauseMenu = PauseSceen(self)

	def Unpause(self):
		self.paused = False
		self.SetUpControls()
		self.StartGameCycle()

	def BossScreen(self,event):
		#This procedure is used whenever the player uses the boss screen control. It will make the screen the boss screen or undo the boss  screen based on the current state. It works the same as pausing the game except it also will paste an image of a word document to  make it look like work is being done.
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

	def StartGameCycle(self):
		#This procedure does the game loop. On every iteration it clears the entire board, moves each of the snakes and will then redraw all of the snakes in their new positions. The final instruction is used to make the delay between moves and to carry on the iterative procedure.
		if ((not self.paused) and (not self.gameOver)):
			self.CheckForDeadEnemySnakes()
			self.RemoveDeadEntities()
			self.myPlayer.snake.Move(self)

			for i in range(len(self.enemySnakes)):
				if (not self.gameOver):
					self.enemySnakes[i].DoEnemySnakeMove(self)

			self.CheckIfSnakesTooSmall()
			
			if (not self.gameOver):

				self.IncreasePlayerScore()

				self.AddEnemySnake()

				self.gameCycleCount +=1
				self.AddPowerUps()
				self.after(self.gameCycleLength,self.StartGameCycle)

	def GameOver(self):
		#This procedure is used to end the game, like if the player collides witht their own body or a wall. It will delete everything on the canvas and will close the window. It then also reopens the menu window.
		self.background.delete(ALL)
		# self.DisplayAllElements()

		self.myPlayer.midLevel = False
		self.myPlayer.SavePlayer()
		msgb.showinfo("Game Over","GAME OVER!!!!")
		self.gameOver = True
		self.CloseWindow(False)

	def RemoveDeadEntities(self):
		i = 0
		while (i < len(self.entitiesToRemove)):
			self.background.delete(self.entitiesToRemove[i])
			self.entitiesToRemove.remove(self.entitiesToRemove[i])



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
	def CheckIfSnakesTooSmall(self):
		if (self.checkIfPlayerTooSmall):
			if (self.myPlayer.snake.length <= 2):
				self.GameOver()
		for i in range(len(self.enemySnakes)):
			if (self.enemySnakes[i].length <=2):
				self.enemySnakes[i].KillSnake(self)

	def LoadGame(self):
		#This procedure will load in the player, their snake and the full gameboard. The only detail from the game bpard to really load in is all of the powerups on the screen
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
			newPowerup.MakePowerUp(self,xPosition,yPosition,tempType)
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

				tempSnake.body.append(blk(self,xPosition,yPosition,facing,tempSnake.color))
			file.readline()

			numberOfTurningPoints = int(file.readline().strip())
			for j in range(numberOfTurningPoints):
				xPosition = int(file.readline().strip())
				yPosition = int(file.readline().strip())
				facing = file.readline().strip()

				tempSnake.turningPoints.append(blk(self,xPosition,yPosition,facing,tempSnake.color))

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

	def CreateImage(self,x,y,fill):
		img = None
		width = self.gridBoxWidth
		if ("#" in fill):
			img = self.background.create_rectangle(0,0,width,width,fill = fill)
			self.background.move(img, (x * width),(y * width))
		else:
			self.powerUpImages.append(PhotoImage(file = ("gameRes/" + fill + ".gif")))
			img = self.background.create_image(0,0,image = self.powerUpImages[len(self.powerUpImages) - 1])
			self.background.move(img,((x + 0.5) * width),((y + 0.5) * width))
		return img


#Medium sized & importance screens
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

class ScoreboardScreen(Tk):
	lbTitle = lb
	btnClose = btn
	scorebox = txt

	scoreboard = scrb()
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
		#This procedure will load the scorebaord in. It will then format them into the text box on the screen in the fornat of 'placeOnScorebaord. Name: Score'. It will also make it so the scoreboard is read only afterwards to prevent the player from altering scores
		self.scoreboard.LoadInScoreboard()
		scoreText = ""
		for i in range(0 ,self.scoreboard.numberOfScores):
			self.scoreBox.insert(INSERT,str(i + 1) + ".")
			self.scoreBox.insert(INSERT,self.scoreboard.scores[i].name + " : " + str(self.scoreboard.scores[i].score))
			self.scoreBox.insert(INSERT, "\n")
			self.scoreBox.insert(INSERT, "\n")
		self.scoreBox.configure(state = 'disabled')
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
		#Important to note here. The newGame parameter is a boolean used to tell us whether the login screen should be to login or to create a new game. Based on this the title of the screen and the function of the login button will be changed
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
		#This sub will create a player file for the new player. Doing this will create an eror if the player exists already. Therefore this will be caught and an error message displayed. If it is a new player Then the player will be made with the input name and password, and will be saved to the new file
		try:
			file = open("gameFiles/" + name + ".txt","xt")
			file.close()
			myPlayer.CreatePlayer(name,password)
			msgb.showinfo("Login","Account has been made!")

		except FileExistsError:
			msgb.showinfo("Login","User already exists! Please use a different name")


#Small screens
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
		self.txtRules.insert(INSERT,rules)
		self.txtRules.pack(pady = 100)

		self.mainloop()
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

#Classees for general controls
class BackButton(btn):
	#This is a reusable back button. It will position itself in the same and correct place on screen each time. It's text will change based on the input parameter as some back buttons must say back Whilst others need to say quit. It also takes the boolean value of openMenu which is used to tell whether we should reopen the menu after closing the parentwindow (the window it is put into) So if that value is true then it will reopen the menu like for the login screen
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

def OpenScoreboard():
	windowScoreboard = ScoreboardScreen()
def OpenRulesScreen():
	rulesScreen = RulesScreen()
def OpenControlsScreen(myPlayer):
	if (myPlayer.name == ""):
		msgb.showinfo("Error","Please Login first!")
	else:
		windowControlsScreen = ControlsScreen(myPlayer)
def OpenGameScreen(myPlayer):
	gameScreen = GameScreen(myPlayer)
def LoadGame():
	windowLogin = LoginScreen(False)#Opens the login screen. NewGame variable is set to false as we are loading a game
def NewGame():
	windowLogin = LoginScreen(True)#Opens the login screen. NewGame variable is set to true as we are making a new game
def BeginGame():
	#Main sub that runs the program
	global screenResolution,screenWidth,screenHeight
	windowMenu = Menu()

BeginGame()#Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet
