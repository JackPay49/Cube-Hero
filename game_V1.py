import tkinter,time,random
from tkinter import *
from tkinter import messagebox

screenWidth = 1600
screenHeight = 900
screenResolution = (str(screenWidth) + "x" + str(screenHeight))

numberOfPowerUpTypes = 5
#Classes


class Block:
	#Below class is used to store a position on the baord and a direction. This is to store a single section
	#of a snake. This is used when the snake is turninng and moving and just within a snake class
	x = 0
	y = 0
	facing = "Up"
	def __init__(self,xValue,yValue,fValue):
		self.x = xValue
		self.y = yValue
		self.facing = fValue

class PowerUp:
	position = None
	powerUpType = "Grow"#Later in game dev there will be many different types of powerup like speedup, grow, shrink, slowdown,etc
	color = 'blue'

	def __init__(self,gameScreen):
		self.RandomlyPlace(gameScreen)
		self.RandomyType()

	def MakePowerUp(self,xPosition,yPosition,type):
		self.position = Block(xPosition,yPosition,"Null")
		self.powerUpType = type
		self.SetColor()

	def RandomyType(self):
		#This will randomly pick which type of powerup it is and will then set the color based
		#on the color
		typeNumber = random.randint(1,numberOfPowerUpTypes)
		if (typeNumber == 1):
			self.powerUpType = "Grow"
		elif (typeNumber == 2):
			self.powerUpType = "SpeedUp"
		elif (typeNumber == 3):
			self.powerUpType = "SlowDown"
		elif (typeNumber == 4):
			self.powerUpType = "Shrink"
		elif (typeNumber == 5):
			self.powerUpType = "Random"
		self.SetColor()

	def SetColor(self):
		#Changes the color based on the type of powerup
		if (self.powerUpType == "Grow"):
			self.color = 'blue'
		elif (self.powerUpType == "SpeedUp"):
			self.color = 'green'
		elif (self.powerUpType == "SlowDown"):
			self.color = 'red'
		elif (self.powerUpType == "Shrink"):
			self.color = 'yellow'
		elif (self.powerUpType == "Random"):
			self.color = 'purple'

	def RandomlyPlace(self,gameScreen):
		#This procedure is easy. It randomly finds a position on the board and will validate it. It will only place the powerup in that position if it is valid
		valid = False
		while (valid == False):
			x = random.randint(0,gameScreen.numberOfHorizontalLines)
			y = random.randint(0,gameScreen.numberOfVerticalLines)
			valid = self.CheckPosition(gameScreen,x,y)
		self.position = Block(x,y,"Null")

	def PowerUpConsumed(self,gameScreen,snake):
		#This procedure is simple currently but should become far more complex. It will carry out the actual function of the powerup. So it will increase size of the player if it is type grow, etc, etc.
		#The Shrink powerup gives no points as it makes the game easier to play
		if (self.powerUpType == "Grow"):
			snake.IncreaseLength(1)
			gameScreen.myPlayer.IncreaseScore(100)
		elif (self.powerUpType == "SpeedUp"):
			snake.IncreaseSpeed(1)
			gameScreen.myPlayer.IncreaseScore(50)
		elif (self.powerUpType == "SlowDown"):
			snake.DecreaseSpeed(1)
			gameScreen.myPlayer.IncreaseScore(50)
		elif (self.powerUpType == "Shrink"):
			snake.DecreaseLength(gameScreen,1)
		elif (self.powerUpType == "Random"):#This powerup gives more points as it will randomly assign pick a powerup from the lsit of powerups
			randomPowerNumber = random.randint(1,(numberOfPowerUpTypes - 1))
			if (randomPowerNumber == 1):
				snake.IncreaseLength(1)
			elif (randomPowerNumber == 2):
				snake.IncreaseSpeed(1)
			elif (randomPowerNumber == 3):
				snake.DecreaseSpeed(1)
			elif (randomPowerNumber == 4):
				snake.DecreaseLength(gameScreen,1)
			gameScreen.myPlayer.IncreaseScore(150)
		gameScreen.powerUps.remove(self)

	def CheckPosition(self,gameScreen,x,y):
		#This just checks if the powerup if ontop of the player snake or is ontop of another powerup
		for i in range(gameScreen.myPlayer.snake.length):
			if ((x == gameScreen.myPlayer.snake.body[i].x) and (y == gameScreen.myPlayer.snake.body[i].y)):
				return False
		for i in range(len(gameScreen.powerUps)):
			if ((x == gameScreen.powerUps[i].position.x) and (y == gameScreen.powerUps[i].position.y)):
				return False
		return True		


class Snake:
	color = 'black'
	length = 0
	moving = True

	speed = 1

	#The below list stores the actual body of the snake. It stores the position on the board of each section and
	#the direction that block is moving in as the different parts can be moving in different ways
	body = []

	#Below stores positions on the board. When part of the snake reaches them they should turn in a different
	#direction
	turningPoints = []

	def Move(self,gameScreen):
		#This sub moves the snake. For each section of the snake's body it will first check if the body has reached a turning point on the baord. If the
		# body section has then it will turn it's direction to the one stored in the turning point. If the final section of the snake passes a turning
		#point then that turning point is no longer needed and therefore it is remvoed from the turning point list. This sub will then move the body of 
		#snake by just adding or subtracting from the position of the body.
		#This procedure is used every single game cycle
		for k in range(self.speed):#It will move multiple times in one turn depending on the speed
			if (self.moving):
				indexToRemove = -1 #Below is used to validate whether the body has reached a turning point and then chagning the direction of movement
				i = 0
				while(i < self.length):#This is used rather than a For loop as the length may change throughout this (like if the player find a shrink or grow powerup)
					for j in range(0,len(self.turningPoints)):
						if ((self.body[i].x == self.turningPoints[j].x) and (self.body[i].y == self.turningPoints[j].y)):
							self.body[i].facing = self.turningPoints[j].facing
							if (i == (self.length - 1)):
								indexToRemove = j
					#Below is used to remove the turning point once the final body section has passed through
					if (indexToRemove != -1):
						self.turningPoints.remove(self.turningPoints[indexToRemove])
					#Below does the actual movement
					xPosition = self.body[i].x
					yPosition = self.body[i].y
					if (self.body[i].facing == "Up"):
						yPosition -= 1
					elif (self.body[i].facing == "Down"):
						yPosition += 1
					elif (self.body[i].facing == "Right"):
						xPosition += 1
					elif (self.body[i].facing == "Left"):
						xPosition -= 1

					#This will check for any game ending collisions such as colliding with the walls or colliding with the snakes own body. If either of
					#these happen it will cause the game over sequence. If the move doesn't cause a collision then we can carry on moving and so set
					#the new position of the snake. It only validating colliding with something on i==0 as this is the head. Only this can collide with
					#something.
					if ((not self.CheckPosition(gameScreen,xPosition,yPosition)) and (i == 0)):
						gameScreen.GameOver()
						self.moving = False
					else:
						self.CheckCollisions(gameScreen)#This will check for collisions such as if the player intercepts a powerup
						if (i < self.length):
							self.body[i].x = xPosition
							self.body[i].y = yPosition
					i +=1



	#The below procedures all do the same function for the different directions. They will check to ensure that the movement is valid. So for example
	#the snake can only turn right if it is moving up or down. Otherwise it is already going right or it cannot do a full 180 degree turn
	#The procedures will then change which direction the head of the snake, the first block, is moving and will add the turning point to the list. It
	#adds the turning point after changing the direction the head is moving as otherwise the rest of the body would keep on moving
	def UpAction(self,event):
		if ((self.body[0].facing == "Right") or (self.body[0].facing == "Left")):
			self.body[0].facing = "Up"
			self.turningPoints.append(Block(self.body[0].x,self.body[0].y,self.body[0].facing))

	def LeftAction(self,event):
		if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
			self.body[0].facing = "Left"
			self.turningPoints.append(Block(self.body[0].x,self.body[0].y,self.body[0].facing))

	def DownAction(self,event):
		if ((self.body[0].facing == "Right") or (self.body[0].facing == "Left")):
			self.body[0].facing = "Down"
			self.turningPoints.append(Block(self.body[0].x,self.body[0].y,self.body[0].facing))
	def RightAction(self,event):
		if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
			self.body[0].facing = "Right"
			self.turningPoints.append(Block(self.body[0].x,self.body[0].y,self.body[0].facing))

	def CheckPosition(self,gameScreen,x,y):
		#This will ensure that the position input in is legal. It checks that the position isn't
		#outside of the grid and then checks to see whether the position is already part of the
		#current snakes body. This second part is to check whether the player has run into
		#themself
		if ((x < 0) or (x >= gameScreen.numberOfHorizontalLines) or (y < 0) or (y >= gameScreen.numberOfVerticalLines)):
			return False
		else:
			for i in range(0,len(self.body)):
				if ((x == self.body[i].x) and (y == self.body[i].y)):	
					return False			
		return True

	def RandomlyGenerate(self,gameScreen):
		self.length = random.randint(3,20)#Minimum size a snake can be is 3 long, as it reaches 2 it will die
		self.RandomlyPlace(gameScreen)

	def RandomlyPlace(self,gameScreen):
		x = random.randint(1,gameScreen.numberOfHorizontalLines)
		y = random.randint(1,gameScreen.numberOfVerticalLines)
		self.GenerateSnakeBody(gameScreen,x,y,self.length)


	def GenerateSnakeBody(self,gameScreen,x,y,lValue):
		#The point of this procedure is to place the snake on the screen and to generate the position of all its body sections. The length can or cannot be specified beforehand. 
		#The way this works is that it will first pick a random direction to generate in from the start position. It will move one section at a time in this direction and check if this new position is valid 
		#for the snake to exist in. It checks using the CheckPosition procedure. If it is a valid position it will add the snake to the body, otherwise it will remove this direction from those that are valid
		#to generate in, for this body section. It will then randomly pick another direction and loop again trying to place the same body section. It's important to note here too that changedDirections
		#boolean is used to remember if we have suddenly begun generating in a different direction. This is then used to create a turning point, when the next body section is generated in this new direction.
		#This turning point is very important as it ensures that then when the snake begins to move away, each of the body sections will also turn with the head. 
		#This sub is crucial incase further snakes are added in the future, if the player is generated near to the edge of the board, if other snakes are randomly placed in the future or if the game ends up
		# having walls through the middle of the grid
		directionOfMovement = ""
		xPosition = x
		yPosition = y
		allDirections = ["Up","Left","Down","Right"]
		self.body = []
		if (x <= 5):
			allDirections.remove("Right")
		elif (y <= 5):
			allDirections.remove("Down")
		elif (x >= (gameScreen.numberOfHorizontalLines - 5)):
			allDirections.remove("Left")
		elif (y <= (gameScreen.numberOfVerticalLines - 5)):
			allDirections.remove("Up")

		directionOfGeneration = random.choice(allDirections)
		self.length = lValue
		for i in range(0,self.length):
			allDirections = ["Up","Left","Down","Right"]
			valid = False
			changedDirections = False
			while(not valid):
				newYPosition = yPosition
				newXPosition = xPosition		
				if (directionOfGeneration == "Up"):
					directionOfMovement = "Down"
					newYPosition -= 1
				elif(directionOfGeneration == "Down"):
					directionOfMovement = "Up"
					newYPosition += 1
				elif(directionOfGeneration == "Right"):
					directionOfMovement = "Left"
					newXPosition += 1
				elif(directionOfGeneration == "Left"):
					directionOfMovement = "Right"
					newXPosition -= 1
				if (self.CheckPosition(gameScreen,newXPosition,newYPosition)):
					valid = True
					xPosition = newXPosition
					yPosition = newYPosition
					self.body.append(Block(xPosition,yPosition,directionOfMovement))
					if (changedDirections):
						turningPoint = Block(self.body[i - 1].x,self.body[i - 1].y,self.body[i - 1].facing)#We save the previous block as this is the one that is actually on the bend of the snake. It must
						#be made in a new instance of Block() to ensure that it isn't updated like the body part is, when the snake moves next
						self.turningPoints.append(turningPoint)
				else:
					valid = False
					allDirections.remove(directionOfGeneration)
					if (len(allDirections) == 0):
						print("Error!")
					else:		
						directionOfGeneration = random.choice(allDirections)
						if (i != 1):#This is used as an error will be caused if we make a turning point of the previous body part, as obviously it doesn't exist. Also there's no need to have a turning point 
						#ahead of the head as at this point it is just changing the direction it will move off in
							changedDirections = True

	def IncreaseLength(self,amount):
		#This procedure will increase the size of the snake by a certain amount. It does this by mimicking the tail of the snake and adding it to the list of the snake's body.
		for i in range(amount):
			xPosition = self.body[self.length - 1].x
			yPosition = self.body[self.length - 1].y
			facing = self.body[self.length - 1].facing
			self.length +=1
			if (facing == "Right"):
				xPosition -=1
			elif (facing == "Left"):
				xPosition +=1			
			elif (facing == "Up"):
				yPosition +=1			
			elif (facing == "Down"):
				yPosition -=1
			self.body.append(Block(xPosition,yPosition,facing))

	def CheckCollisions(self,gameScreen):
		#This procedure checks through the list of powerups to see if the head of the snake has intercepted any pwoerups. If it has then the powerup will be activated on this snake
		count = 0
		while (count < len(gameScreen.powerUps)):
			if ((self.body[0].x == gameScreen.powerUps[count].position.x) and (self.body[0].y == gameScreen.powerUps[count].position.y)):
				gameScreen.powerUps[count].PowerUpConsumed(gameScreen,self)
			else:
				count +=1

	def IncreaseSpeed(self,amount):
		for i in range(amount):
			if (self.speed < 3):
				self.speed +=1

	def DecreaseSpeed(self,amount):
		for i in range(amount):
			if (self.speed > 1):
				self.speed -=1

	def DecreaseLength(self,gameScreen,amount):
		for i in range(amount):
			self.body.remove(self.body[self.length - 1])
			self.length -=1


	def SaveSnake(self,myPlayer):
		#This procedure writes up all of the details about the snake, which come down to each
		#of the body sections and all of the turning points
		file = open("gameFiles/" + myPlayer.name + "Snake.txt","w")
		file.write(str(self.length) + "\n")
		for i in range(self.length):
			file.write(str(self.body[i].x) + "\n")
			file.write(str(self.body[i].y) + "\n")
			file.write(self.body[i].facing + "\n")	

		file.write("\n")

		file.write(str(len(self.turningPoints)) + "\n")
		for i in range(len(self.turningPoints)):
			file.write(str(self.turningPoints[i].x) + "\n")
			file.write(str(self.turningPoints[i].y) + "\n")
			file.write(self.turningPoints[i].facing + "\n")

	def LoadSnake(self,myPlayer):
		file = open("gameFiles/" + myPlayer.name + "Snake.txt","r")
		self.length = int(file.readline().strip())
		self.body = []
		self.turningPoints = []
		for i in range(self.length):
			xPosition = int(file.readline().strip())
			yPosition = int(file.readline().strip())
			facing = file.readline().strip()
			self.body.append(Block(xPosition,yPosition,facing))

		file.readline()

		number = int(file.readline().strip())
		for i in range(number):
			xPosition = int(file.readline().strip())
			yPosition = int(file.readline().strip())
			facing = file.readline().strip()
			self.turningPoints.append(Block(xPosition,yPosition,facing))


class Scoreboard:

	scores = []
	maxNumberOfScores = 10
	numberOfScores = 0

	def SortScores(self,low,high):#This is a basic quicksort that sorts the algorithm from greatest score to smallest, 0 to 9. Based on the scores of each player
		tempLow = low
		tempHigh = high
		pivot = self.scores[int((low + high)/2)].score
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
		#This writes all scorebaorrd details into a text file. it will format them in the form of a name, then a score on a different line and then it will leave a blank line between different player scores.
		#At the top of the file there will also be the number of scores stored which is used to change how long the loop will search for scores in the file
		self.SortScores(0,(self.numberOfScores - 1))
		file = open("gameFiles/scoreboard.txt","w")
		file.write(str(self.numberOfScores))
		for i in range(0,len(self.scores)):
			file.write("\n" + self.scores[i].name)
			file.write("\n" + str(self.scores[i].score))
			file.write("\n")
		file.close()

	def LoadInScoreboard(self):
		#This will load in details from the scoreboard. It reads the values for each player and puts them into a temporary player strcuture which is then added to the scoreabord list.
		file = open("gameFiles/scoreboard.txt","rt")
		self.numberOfScores = int(file.readline())
		for i in range(0,self.numberOfScores):
			tempPlayer = Player()
			tempPlayer.name = file.readline().strip()
			tempPlayer.score = int(file.readline())
			file.readline()
			self.scores.append(tempPlayer)
		file.close()

	def AddScoreToScoreboard(self,newPlayer):
		#There are two possible cases to adding a score to the scorebaord. 1: the scoreboard is full already. If it is already full then it will compare to the last score in the scorebaord, the lowest. If the new
		#score is higher than that, it should be added and so replaces this last score. We then resort and save the scorebaord if it was added.
		#2: in this case the scorebaord isn't full. In this case the new score can just be added to the end of the scorebaord and it can be sorted and saved.
		if (len(self.scores) >= self.maxNumberOfScores):
			if (newPlayer.score > self.scores[maxNumberOfScores - 1].score):
				self.scores[maxNumberOfScores - 1] = newPlayer
				self.numberOfScores += 1
				self.SortScores(0,(self.numberOfScores - 1))
				self.SaveScoreboard()
		else: 
			self.scores.append(newPlayer)
			self.numberOfScores += 1
			self.SortScores(0,(self.numberOfScores - 1))
			self.SaveScoreboard()

class Player:
	name = ""
	score = 0
	password = ""
	controls = ['w','a','s','d','e','b']#This stores the player controls for up, left, down, right, pause and boss screen respectively. These will be used when actraully assigning controls in the game screen
	midLevel = False#Midlevel is used to tell the program whether the player is mid way through a level already. If they are then it will actually load the level details in, but if they're not then it won't.

	snake = Snake()

	def LoadPlayer(self,nValue):
		#This jsut loads in the details of the player. Important thing to note here is the loading of the controls. They are read in as a string and then a separate procedure will find the control values and
		#insert them into the array
		self.name = nValue
		file = open("gameFiles/" + self.name + ".txt","rt")
		file.readline()
		self.password = (file.readline()).strip()
		self.score = int(file.readline())
		self.controls = ConvertToList(file.readline())
		midLevelState = file.readline().strip()
		file.close()
		if (midLevelState == "1"):
			self.midLevel = True

	def SavePlayer(self):
		file = open("gameFiles/" + self.name + ".txt","wt")
		file.write(self.name + "\n")
		file.write(str(self.password) + "\n")
		file.write(str(self.score) + "\n")
		file.write(str(self.controls) + "\n")
		if (self.midLevel == True):#In the player file the midlevel boolean is stored as either a 0 or 1
			file.write("1\n")
		else:
			file.write("0\n")
		file.close()

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

#Screen Classes:
class Menu(Tk):
	lbTitle = Label

	btnLoadGame = Button
	btnCreateNewGame = Button
	btnScoreboard = Button
	btnClose = Button

	def __init__(self):
		super().__init__()
		self.geometry("500x500")
		self.title("Menu")

		#fonts
		fontNormal = ("Default",12,"bold")

		self.lbTitle = TitleLabel(self,"Cube Hero!")

		#Buttons
		self.btnLoadGame = Button(self,text = "Load Game", command = lambda: (self.destroy(),LoadGame()),font = fontNormal)
		self.btnLoadGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)

		self.btnCreateNewGame = Button(self,text = "Create new Game",command = lambda: (self.destroy(),NewGame()),font = fontNormal)
		self.btnCreateNewGame.place(relx = 0.5, rely = 0.5, anchor = CENTER)


		self.btnScoreboard = Button(self,text = "Scoreboard",command = OpenScoreboard,font = fontNormal)
		self.btnScoreboard.place(relx = 0.5, rely = 0.7, anchor = CENTER)

		self.btnClose = BackButton(self,"Close",False)

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
	btnRules = Button

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

		self.lbName = Label(self,text = "Name:",font = fontBold)
		self.lbName.place(relx = 0.2,rely = 0.2, anchor = CENTER)
		self.txtName = Entry(self,font = fontNormal)
		self.txtName.place(relx = 0.5,rely = 0.2, anchor = CENTER)

		self.lbPassword = Label(self,text = "Password:",font = fontBold)
		self.lbPassword.place(relx = 0.2,rely = 0.3, anchor = CENTER)
		self.txtPassword = Entry(self,show = "*",font = fontNormal)
		self.txtPassword.place(relx = 0.5,rely = 0.3, anchor = CENTER)

		if (newGame):
			self.btnLogin = Button(self,text = "Create new game",font = fontBold, command = lambda: self.CreateNewPlayer(myPlayer,self.txtName.get(),self.txtPassword.get()))
		else:
			self.btnLogin = Button(self,text = "Login",font = fontBold, command = lambda: self.Login(myPlayer,self.txtName.get(),self.txtPassword.get()) )
		self.btnLogin.place(relx = 0.5,rely = 0.4, anchor = CENTER)

		self.btnBeginGame = Button(self,text = "Begin Game",command = lambda:(self.destroy(),OpenGameScreen(myPlayer)), font = fontBold)
		self.btnBeginGame.place(relx = 0.7,rely = 0.6,anchor = CENTER)

		self.btnControls = Button(self,text = "Controls",command = lambda:(OpenControlsScreen(myPlayer)), font = fontBold)
		self.btnControls.place(relx = 0.3,rely = 0.6, anchor = CENTER)

		self.btnRules = Button(self,text = "Rules",command = OpenRulesScreen, font = fontBold)
		self.btnRules.place(relx = 0.3,rely = 0.8, anchor = CENTER)

		self.btnClose = BackButton(self,"Back",True)
		self.mainloop()

	def Login(self,myPlayer,name,password):
		#This is a basic login function. It loads the player in and checks if their entered password matches the saved one
		myPlayer.LoadPlayer(name)
		if (myPlayer.password == password):
			messagebox.showinfo("Login","Logged in!")
		else:
			messagebox.showinfo("Login","Password incorrect, try again!")

	def CreateNewPlayer(self,myPlayer,name,password):
		#This sub will create a player file for the new player. Doing this will create an eror if the player exists already. Therefore this will be caught and an error message displayed. If it is a new player
		#Then the player will be made with the input name and password, and will be saved to the new file
		try:
			file = open("gameFiles/" + name + ".txt","xt")
			file.close()
			myPlayer.CreatePlayer(name,password)
			messagebox.showinfo("Login","Account has been made!")

		except FileExistsError:
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

		self.lbTitle = TitleLabel(self,"Scoreboard")


		self.btnClose = BackButton(self,"Back",False)

		self.scoreBox = Text(self, font = ("Default",12))
		self.scoreBox.place(relx = 0.5,rely = 0.5,anchor = CENTER)

		self.DisplayScoreboard()
		self.mainloop()

	def DisplayScoreboard(self):
		#This procedure will load the scorebaord in. It will then format them into the text box on the screen in the fornat of 'placeOnScorebaord. Name: Score'. It will also make it so the scoreboard is read
		#only afterwards to prevent the player from altering scores
		self.scoreboard.LoadInScoreboard()
		scoreText = ""
		for i in range(0 ,self.scoreboard.numberOfScores):
			self.scoreBox.insert(INSERT,str(i + 1) + ".")
			self.scoreBox.insert(INSERT,self.scoreboard.scores[i].name + " : " + str(self.scoreboard.scores[i].score))
			for j in range(0,3):
				self.scoreBox.insert(INSERT, "\n")
		self.scoreBox.configure(state = 'disabled')

def OpenScoreboard():
	windowScoreboard = ScoreboardScreen()

class PauseSceen(Tk):
	btnResumeGame =  Button
	btnSaveGame = Button
	btnControls = Button
	btnRules = Button
	btnScoreboard = Button
	btnBack = Button
	btnCheatCode = Button

	txtCheatCode = Entry

	def __init__(self,parentWindow):
		super().__init__()
		self.geometry("300x700")
		self.title("Pause")

		fontButton = ("Default",12,"bold")
		fontNormal = ("Default",12)


		self.lbTitle = TitleLabel(self,"Game Pause")

		self.btnResumeGame = Button(self,text = "Resume Game",font = fontButton)
		self.btnResumeGame.place(relx = 0.5, rely = 0.2, anchor = CENTER)
		self.btnResumeGame.configure(command = lambda:(parentWindow.Unpause(),self.destroy()))

		self.btnSaveGame = Button(self,text = "Save Game",font = fontButton)
		self.btnSaveGame.place(relx = 0.5, rely = 0.3, anchor = CENTER)
		self.btnSaveGame.configure(command = parentWindow.SaveGame)

		self.btnControls = Button(self,text = "Controls",font = fontButton)
		self.btnControls.place(relx = 0.5, rely = 0.4, anchor = CENTER)
		self.btnControls.configure(command = lambda:(OpenControlsScreen(parentWindow.myPlayer)))

		self.btnRules = Button(self,text = "Rules",font = fontButton)
		self.btnRules.place(relx = 0.5, rely = 0.5, anchor = CENTER)
		self.btnRules.configure(command = OpenRulesScreen)

		self.btnScoreboard = Button(self,text = "Scoreboard",font = fontButton)
		self.btnScoreboard.place(relx = 0.5, rely = 0.6, anchor = CENTER)
		self.btnScoreboard.configure(command = OpenScoreboard)

		self.btnCheatCode = Button(self,text = "Enter Cheat Code",font = fontButton)
		self.btnCheatCode.place(relx = 0.5, rely = 0.7, anchor = CENTER)
		self.txtCheatCode = Entry(self,font = fontNormal)
		self.txtCheatCode.place(relx = 0.5,rely = 0.8, anchor = CENTER)

		self.btnBack = Button(self,text = "Quit Game",font = fontButton)
		self.btnBack.place(relx = 0.5, rely = 0.9, anchor = CENTER)
		self.btnBack.configure(command = lambda:(self.destroy(),parentWindow.CloseWindow(True)))

		self.mainloop()

class RulesScreen(Tk):
	btnBack = Button

	lbTitle = Label

	txtRules = Text

	def __init__(self):
		super().__init__()
		self.geometry("700x700")
		self.title("Rules")

		lbTitle = TitleLabel(self,"Welcome to Cube Hero!")
		btnBack = BackButton(self,"Back",False)

		file = open("gameFiles/rules.txt","r")
		rules = file.read()
		file.close()

		self.txtRules = Text(self, font = ("Default",12))
		self.txtRules.place(relx = 0.5,rely = 0.5,anchor = CENTER)
		self.txtRules.insert(INSERT,rules)
		self.txtRules.pack(pady = 100)

		self.mainloop()

def OpenRulesScreen():
	rulesScreen = RulesScreen()


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

		self.DisplayControls(myPlayer) #This fills in all of the text boxes with the values of the controls

		self.btnResetControls = Button(self,text = "Reset Controls" ,command = lambda:(self.ResetControls(myPlayer)),font = fontBold)
		self.btnResetControls.place(relx = 0.3,rely = 0.8,anchor = CENTER)

		self.btnSaveChanges = Button(self,text = "Save Changes" ,command = lambda:(self.SaveChanges(myPlayer)),font = fontBold)
		self.btnSaveChanges.place(relx = 0.7,rely = 0.8,anchor = CENTER)

		self.btnClose = BackButton(self,"Back",False)
		self.mainloop()

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
		messagebox.showinfo("Saved!","Changes to controls have been saved!")
def OpenControlsScreen(myPlayer):
	#This procedure only displays if the player is logged in as we need their controls, without that this screen is useless
	if (myPlayer.name == ""):
		messagebox.showinfo("Error","Please Login first!")
	else:
		windowControlsScreen = ControlsScreen(myPlayer)

#Classees for general controls
class BackButton(Button):
	#This is a reusable back button. It will position itself in the same and correct place on screen each time. It's text will change based on the input parameter as some back buttons must say back
	#Whilst others need to say quit. It also takes the boolean value of openMenu which is used to tell whether we should reopen the menu after closing the parentwindow (the window it is put into)
	# So if that value is true then it will reopen the menu like for the login screen
	def __init__(self,parentWindow,textValue,openMenu):
		super().__init__()
		self = Button(parentWindow,text = textValue,font = ("Default",12,"bold"))
		self.place(relx = 0.5, rely = 0.9, anchor = CENTER)
		if (openMenu):
			self.configure(command = lambda:(parentWindow.destroy(),BeginGame()))
		else:
			self.configure(command = lambda:(parentWindow.destroy()))
class TitleLabel(Label):
	#This is a reusable title label. It will fomrat and position the label correctly on the screen and will fill in the text based on the input parameter
	def __init__(self,parentWindow,textValue):
		super().__init__()
		self = Label(parentWindow,text = textValue,font = ("Default",30,"bold","underline")) 
		self.place(relx = 0.5, rely = 0.1, anchor = CENTER)

#Main game
class GameScreen(Tk):
	background = Canvas

	backgroundWidth = 800
	backgroundHeight = 800
	numberOfVerticalLines = 50
	numberOfHorizontalLines = 50

	gameCycleLength = 200 #In milliseconds
	gameCycleCount = 0;

	myPlayer = Player()

	gameOver = False

	paused = False

	powerUps = []
	def __init__(self,myPlayer):
		super().__init__()
		self.title("Game screen")
		self.geometry(screenResolution)

		self.background = Canvas(self,width = self.backgroundWidth,height = self.backgroundHeight)
		self.background.place(relx = 0.5,rely = 0.5, anchor = CENTER)
		self.background.configure(bg = 'white')
		self.background.pack()
		self.DisplayGrid()

		self.myPlayer = myPlayer
		if (self.myPlayer.midLevel == False): #Here if the player is mid way through the level, only then will their game be loaded in and 
		#displayed. If they're not midlevel then they will always be randomly placed and be given a length of 3
			self.myPlayer.snake.length = 3
			self.myPlayer.snake.RandomlyPlace(self)
		else:
			self.LoadGame()
		self.DisplaySnake(self.myPlayer.snake)

		self.SetUpControls()
		self.StartGameCycle()


	def DisplayGrid(self):
		#This procedure will set up the grid for the game. It creates a canvas on the screen and draws a grid on 
		#that. The loop draws this grid, firstly it draws two lines as the top and left borders. It then draws 21 
		#horizontal and 21 vertical lines to create the grid with borders. This is so that snakes can be painted in
		self.background.create_line(1,0,1,self.backgroundHeight)#Must draw these lines separate otherwise they would appear outside of the canvas
		self.background.create_line(0,1,self.backgroundWidth,1)

		for i in range(1,(self.numberOfVerticalLines + 1) ):
			xposition = (i * (self.backgroundWidth/self.numberOfVerticalLines))
			self.background.create_line(xposition,0,xposition,self.backgroundHeight)

		for i in range(1,(self.numberOfHorizontalLines + 1)):
			yPosition = (i * (self.backgroundHeight/self.numberOfHorizontalLines))
			self.background.create_line(0,yPosition,self.backgroundWidth,yPosition)
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
		if (self.paused == True):
			self.Unpause()
		else:
			self.paused = True


	def DisplaySnake(self,snake):
		#This will display a specific snake onto the screen. It calculates the position on the baord of each section of the snake based on the 
		#canvas width and the number of grid lines and will draw each body section onto the canvas. This is used every single game cycle
		gridBoxWidth = self.backgroundWidth/self.numberOfHorizontalLines
		for i in range(0,snake.length):
			leftCornerX = snake.body[i].x * gridBoxWidth
			leftCornerY = snake.body[i].y * gridBoxWidth
			rightCornerX = (snake.body[i].x + 1) * gridBoxWidth
			rightCornerY = (snake.body[i].y + 1) * gridBoxWidth

			self.background.create_rectangle(leftCornerX,leftCornerY,rightCornerX,rightCornerY,outline = snake.color,fill = snake.color)

	def StartGameCycle(self):
		#This procedure does the game loop. On every iteration it clears the entire board, moves each of the snakes and will then redraw all of the
		#snakes in their new positions. The final instruction is used to make the delay between moves and to carry on the iterative procedure.
		if ((not self.paused) and (not self.gameOver)):
			self.background.delete(ALL)
			self.DisplayGrid()

			self.myPlayer.snake.Move(self)
			self.CheckIfPlayerTooSmall()
			if (not self.gameOver):

				self.DisplaySnake(self.myPlayer.snake)
				self.DisplayPowerUps()

				self.gameCycleCount +=1
				self.AddPowerUps()
				self.after(self.gameCycleLength,self.StartGameCycle)

	def GameOver(self):
		#This procedure is used to end the game, like if the player collides witht their own body or a wall. It will delete everything on the 
		#canvas and will close the window. It then also reopens the menu window.
		self.myPlayer.midLevel = False
		self.myPlayer.SavePlayer()
		messagebox.showinfo("Game Over","GAME OVER!!!!")
		self.gameOver = True	
		self.CloseWindow(False)

	def CloseWindow(self,askToSave):
		#This will check if the player wants to save on certain occasions. This is because we don't need to save if they lose a round of the game
		saveGame = ""
		if (askToSave):
			saveGame = messagebox.askquestion("Quit","Would you like to save your progress?")
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
			leftCornerX = self.powerUps[i].position.x * gridBoxWidth
			leftCornerY = self.powerUps[i].position.y * gridBoxWidth
			rightCornerX = (self.powerUps[i].position.x + 1) * gridBoxWidth
			rightCornerY = (self.powerUps[i].position.y + 1) * gridBoxWidth

			self.background.create_rectangle(leftCornerX,leftCornerY,rightCornerX,rightCornerY,outline = self.powerUps[i].color,fill = self.powerUps[i].color)

	def CheckIfPlayerTooSmall(self):
		if (self.myPlayer.snake.length <= 2):
			self.GameOver()

	def LoadGame(self):
		#This procedure will load in the player, their snake and the full gameboard. The only detail from the game bpard to really load in is all of the powerups on the
		#screen
		self.myPlayer.LoadPlayer(self.myPlayer.name)
		self.myPlayer.snake.LoadSnake(self.myPlayer)
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

		messagebox.showinfo("Saved","Game has been saved!")

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





