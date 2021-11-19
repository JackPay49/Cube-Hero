import random
from tkinter import PhotoImage as img
numberOfPowerUpTypes = 7
class Block:
	#Below class is used to store a position on the baord and a direction. This is to store a single section of a snake. This is used when the snake is turninng and moving and just within a snake class
	x = 0
	y = 0
	facing = "Up"
	def __init__(self,xValue,yValue,fValue):
		self.x = xValue
		self.y = yValue
		self.facing = fValue
class Snake:
	color = '#0FFF50'
	length = 0
	moving = True

	speed = 1

	snakeType = "Player"

	#The below list stores the actual body of the snake. It stores the position on the board of each section and the direction that block is moving in as the different parts can be moving in different ways
	body = []
	

	#Below stores positions on the board. When part of the snake reaches them they should turn in a different direction
	turningPoints = []

	def __init__(self,stValue):
		body = []
		turningPoints = []
		length = 0
		speed = 1
		self.snakeType = stValue
		if (self.snakeType == "Player"):
			self.color = '#0FFF50'
		else:
			self.color = '#FF5F1F'


	def Move(self,gameScreen):
		#This sub moves the snake. For each section of the snake's body it will first check if the body has reached a turning point on the baord. If the body section has then it will turn it's direction to the one stored in the turning point. If the final section of the snake passes a turning point then that turning point is no longer needed and therefore it is remvoed from the turning point list. This sub will then move the body of snake by just adding or subtracting from the position of the body. This procedure is used every single game cycle
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

					#This will check for any game ending collisions such as colliding with the walls or colliding with the snakes own body. If either of these happen it will cause the game over sequence. If the move doesn't cause a collision then we can carry on moving and so set the new position of the snake. It only validating colliding with something on i==0 as this is the head. Only this can collide with something.
					if ((not self.CheckPosition(gameScreen,xPosition,yPosition,"Moving")) and (i == 0)):
						self.KillSnake(gameScreen)

					else:
						if (i < self.length):
							self.body[i].x = xPosition
							self.body[i].y = yPosition
					i +=1
				self.CheckCollisions(gameScreen)#This will check for collisions such as if the player intercepts a powerup

	def KillSnake(self,gameScreen):
		self.moving = False
		self.color = "white"
		self.turningPoints = []
		if (self.snakeType == "Player"):#This will only cause a game over if the snake is the player. It will make the snake flash white and stop moving
			gameScreen.GameOver()
		

	#The below procedures all do the same function for the different directions. They will check to ensure that the movement is valid. So for example the snake can only turn right if it is moving up or down. Otherwise it is already going right or it cannot do a full 180 degree turn The procedures will then change which direction the head of the snake, the first block, is moving and will add the turning point to the list. It adds the turning point after changing the direction the head is moving as otherwise the rest of the body would keep on moving
	def UpAction(self,event):
		self.Turn("Up")		
	def LeftAction(self,event):
		self.Turn("Left")
	def DownAction(self,event):
		self.Turn("Down")
	def RightAction(self,event):
		self.Turn("Right")

	def Turn(self,direction):
		valid = False
		if (direction == "Right"):
			if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
				self.body[0].facing = "Right"
				valid = True
		elif (direction == "Left"):
			if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
				self.body[0].facing = "Left"
				valid = True
		elif (direction == "Up"):
			if ((self.body[0].facing == "Right") or (self.body[0].facing == "Left")):
				self.body[0].facing = "Up"
				valid = True
		elif (direction == "Down"):
			if ((self.body[0].facing == "Right") or (self.body[0].facing == "Left")):
				self.body[0].facing = "Down"
				valid = True
		if (valid):
			self.turningPoints.append(Block(self.body[0].x,self.body[0].y,self.body[0].facing))


	def CheckPosition(self,gameScreen,x,y,checkType):
		#This will ensure that the position input in is legal. It checks that the position isn't outside of the grid and then checks to see whether the position is already part of the current snakes body. This second part is to check whether the player has run into themself
		if ((x < 0) or (x >= gameScreen.numberOfHorizontalLines) or (y < 0) or (y >= gameScreen.numberOfVerticalLines)):
			return False
		else:
			for i in range(0,len(self.body)):
				if ((x == self.body[i].x) and (y == self.body[i].y)):
					return False
		if (self.snakeType == "Enemy"):
			for i in range(len(gameScreen.enemySnakes)):
				if (gameScreen.enemySnakes[i] != self):
					for j in range(gameScreen.enemySnakes[i].length):
						if ((gameScreen.enemySnakes[i].body[j].x == x) and (gameScreen.enemySnakes[i].body[j].y == y)):
							return False
		if ((checkType == "Spawning") and (self.snakeType == "Enemy")):
			for i in range(gameScreen.myPlayer.snake.length):
				if ((gameScreen.myPlayer.snake.body[i].x == x) and (gameScreen.myPlayer.snake.body[i].y == y)):
					return False

		return True

	def RandomlyGenerate(self,gameScreen):
		self.length = random.randint(3,20)#Minimum size a snake can be is 3 long, as it reaches 2 it will die
		self.RandomlyPlace(gameScreen)
	def RandomlyPlace(self,gameScreen):
		#This procedure will repeat until the snake is palced into a valid position
		valid = False
		x = 0
		y = 0
		while (not valid):
			x = random.randint(1,gameScreen.numberOfHorizontalLines - 1)
			y = random.randint(1,gameScreen.numberOfVerticalLines - 1)
			valid = self.GenerateSnakeBody(gameScreen,x,y,self.length)

	def GenerateSnakeBody(self,gameScreen,x,y,lValue):
		#This procedure will generate all the positions of the body of a snake based on the position of its head and its length. It first checks what direction to generate in and won't generate running straight into the side of the screen. It then will then place the head of the snake and just increase in length, using this pther procedure to grow in a legal way. It will return true or false based on whether it could be palced on the board or not successfully						 
		xPosition = x
		yPosition = y
		directions = ["Up","Left","Down","Right"]
		self.body = []
		if (x <= 10):
			directions.remove("Left")
		elif (y <= 10):
			directions.remove("Up")
		elif (x >= (gameScreen.numberOfHorizontalLines - 10)):
			directions.remove("Right")
		elif (y <= (gameScreen.numberOfVerticalLines - 10)):
			directions.remove("Down")
		directionOfMovement = random.choice(directions)
		self.body.append(Block(x,y,directionOfMovement))
		self.length = 1
		return self.IncreaseLength(gameScreen,(lValue - 1))



	def IncreaseLength(self,gameScreen,amount):
		#This procedure will increase the length of the snake and will chekc to make sure it doesn't run off of the edge of the screen or collide with any powerups. The snake must already have atleast a length of 1 and have the head placed already. It generates the new position of the next body section and the direction it is generating in based off of that head piece. It will check if the position is legal and place the new body part at this position if so. If it is not legal then it will remove this direction from the list of all possible directions, will randomly pick a new one and attempt to generate this way. When the snake begins generating in a new direction it will create a turning point at the last body part This has a return. It will return false if the snake could not be possibly placed or its length couldn't be increased into any area
		xPosition = self.body[len(self.body) - 1].x		
		yPosition = self.body[len(self.body) - 1].y		
		facing = self.body[len(self.body) - 1].facing #direction of movement		
		for i in range(1,amount + 1):
			self.length += 1
			allDirections = ["Up","Left","Down","Right"]
			valid = False
			changedDirections = False
			while(not valid):
				newYPosition = yPosition
				newXPosition = xPosition
				if (facing == "Down"):
					newYPosition -= 1
				elif(facing == "Up"):
					newYPosition += 1
				elif(facing == "Left"):
					newXPosition += 1
				elif(facing == "Right"):
					newXPosition -= 1
				if (self.CheckPosition(gameScreen,newXPosition,newYPosition,"Spawning")):
					valid = True
					xPosition = newXPosition
					yPosition = newYPosition
					self.body.append(Block(xPosition,yPosition,facing))
					if (changedDirections):
						turningPoint = Block(self.body[len(self.body) - 2].x,self.body[len(self.body) - 2].y,self.body[len(self.body) - 2].facing)#We save the previous block as this is the one that is actually on the bend of the snake. It must be made in a new instance of Block() to ensure that it isn't updated like the body part is, when the snake moves next
						self.turningPoints.append(turningPoint)
				else:
					valid = False
					if (facing in allDirections):
						allDirections.remove(facing)

					if (len(allDirections) == 0):
						return False
					else:
						facing = random.choice(allDirections)
						if (i != 1):#This is used as an error will be caused if we make a turning point of the previous body part, as obviously it doesn't exist. Also there's no need to have a turning point ahead of the head as at this point it is just changing the direction it will move off in
		 					changedDirections = True
		return True 



	def CheckCollisions(self,gameScreen):
		#This procedure checks through the list of powerups to see if the head of the snake has intercepted any pwoerups. If it has then the powerup will be activated on this snake
		count = 0
		while (count < len(gameScreen.powerUps)):
			if ((self.body[0].x == gameScreen.powerUps[count].position.x) and (self.body[0].y == gameScreen.powerUps[count].position.y)):
				gameScreen.powerUps[count].PowerUpConsumed(gameScreen,self)
			else:
				count +=1
		self.CheckCollisionsWithOtherSnakes(gameScreen)

	def CheckCollisionsWithOtherSnakes(self,gameScreen):
		#This procedure will check whether snakes collide with each other. If the snake is an enemy snake it will check to see if the enemy head intercepts any part of the player's body. It will kill the player instantly if it hits their head or a bit less than that (whilst snakes must be atleast 3 long). If it will hit them then it saves the place and will subtract the length past that point from the total player snake's length. It will add half of this length to its own length.  The same happens for the player except it will check for each enemy snake too and will add score
		count = -1
		length = 0
		if (self.snakeType == "Enemy"):
			length = gameScreen.myPlayer.snake.length
			for i in range(length):
				if ((self.body[0].x == gameScreen.myPlayer.snake.body[i].x) and (self.body[0].y == gameScreen.myPlayer.snake.body[i].y)):
					count = i
			if (count != -1):
				if (count <= 1):
					gameScreen.myPlayer.snake.KillSnake(gameScreen)
				else:
					diff = length - count
					length -= count
					gameScreen.myPlayer.snake.DecreaseLength(gameScreen,diff)
					self.IncreaseLength(gameScreen, int(diff / 2))

		elif(self.snakeType == "Player"):
			count = -1
			bodyCount = -1
			for i in range(len(gameScreen.enemySnakes)):
				for j in range(gameScreen.enemySnakes[i].length):
					if ((gameScreen.enemySnakes[i].body[j].x == gameScreen.myPlayer.snake.body[0].x) and (gameScreen.enemySnakes[i].body[j].y == gameScreen.myPlayer.snake.body[0].y)):
						count = i
						bodyCount = j
			if ((count != -1) and (bodyCount != -1)):
				if (bodyCount == 0):
					self.KillSnake(gameScreen)
				else:
					length = gameScreen.enemySnakes[count].length
					diff = length - bodyCount
					length -= bodyCount
					gameScreen.enemySnakes[count].DecreaseLength(gameScreen,diff)
					self.IncreaseLength(gameScreen, int(diff / 2))
					gameScreen.myPlayer.IncreaseScore(diff * 100)


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
			count = 0
			while (count < len(self.turningPoints)):
				if ((self.body[self.length - 1].x == self.turningPoints[count].x) and (self.body[self.length - 1].y == self.turningPoints[count].y)):
					self.turningPoints.remove(self.turningPoints[count])
				else:
					count +=1
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

		file.write(str(self.speed) + "\n")



	def LoadSnake(self,gameScreen,myPlayer):
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

		self.speed = int(file.readline().strip())

		if (self.length == 1):
			gameScreen.checkIfPlayerTooSmall = False

	def DoEnemySnakeMove(self,gameScreen):
		#This procedure will make a random choice every single game cycle of whether to turn the snake or not. There's a higher chance that the snake will keep moving in the direction it is moving in. If the snake is made to turn then it will randomly pick which direction to turn into. It isn't possible to turn into directions that the snake is already moving in or backwards so these directions are automatically removed from the pool of possible directions It will then check if the new position is a valid one. This is the case of whether the snake is moving forwards or turning. If it is valid then it will do the move. If it is not then , if the snake is moving straight it will attempt to turn. If a turn is unsuccessful then that direction is removed from the pool of possible directions to turn into. If the snake runs out of directions to turn into then it will be killed
		choice = random.randint(0,20)
		facing = self.body[0].facing
		xPosition = self.body[0].x
		yPosition = self.body[0].y


		allDirections = ["Up","Down","Left","Right"]
		if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
			allDirections.remove("Up")
			allDirections.remove("Down")
		if ((self.body[0].facing == "Left") or (self.body[0].facing == "Right")):
			allDirections.remove("Right")
			allDirections.remove("Left")

		repeat = True
		while(repeat):
			repeat = False
			xPosition = self.body[0].x
			yPosition = self.body[0].y
			if (choice == 0):#then turn in a random direction

				randomNumber = random.randint(0,len(allDirections) - 1)
				facing = allDirections[randomNumber]

			if (facing == "Right"):
				xPosition +=1
			elif (facing == "Left"):
				xPosition -=1
			elif (facing == "Down"):
				yPosition +=1
			elif (facing == "Up"):
				yPosition -=1

			if (self.CheckPosition(gameScreen,xPosition,yPosition,"Moving")):
				if (choice == 0):
					self.Turn(facing)
				self.Move(gameScreen)
			else:
				if (choice == 0):
					allDirections.remove(facing)
				else:
					choice = 0
				if (len(allDirections) <= 0):
					self.KillSnake(gameScreen)
					repeat = False
				else:
					repeat = True

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

class PowerUp:
	position = None
	powerUpType = "Grow"#Later in game dev there will be many different types of powerup like speedup, grow, shrink, slowdown,etc
	color = 'blue'
	img = None

	def __init__(self,gameScreen):
		self.RandomlyPlace(gameScreen)
		self.RandomyType()

	def MakePowerUp(self,xPosition,yPosition,type):
		self.position = Block(xPosition,yPosition,"Null")
		self.powerUpType = type
		self.img = img(file = "gameRes/" + self.powerUpType +".gif")

	def RandomyType(self):
		#This will randomly pick which type of powerup it is and will then set the color based on the color
		randomNumber = random.randint(0,11)
		if (randomNumber < 5):
			self.powerUpType = "Grow"
		elif (randomNumber == 6):
			self.powerUpType = "SpeedUp"
		elif (randomNumber == 7):
			self.powerUpType = "SlowDown"
		elif (randomNumber == 8):
			self.powerUpType = "Shrink"
		elif (randomNumber == 9):
			self.powerUpType = "Random"
		elif (randomNumber == 10):
			self.powerUpType = "Kill"
		elif (randomNumber == 11):
			self.powerUpType = "BoostScore"
		self.img = img(file = "gameRes/" + self.powerUpType +".gif")

	def RandomlyPlace(self,gameScreen):
		#This procedure is easy. It randomly finds a position on the board and will validate it. It will only place the powerup in that position if it is valid
		valid = False
		while (valid == False):
			x = random.randint(0,gameScreen.numberOfHorizontalLines)
			y = random.randint(0,gameScreen.numberOfVerticalLines)
			valid = self.CheckPosition(gameScreen,x,y)
		self.position = Block(x,y,"Null")

	def PowerUpConsumed(self,gameScreen,snake):
		#This procedure is simple currently but should become far more complex. It will carry out the actual function of the powerup. So it will increase size of the player if it is type grow, etc, etc. The Shrink powerup gives no points as it makes the game easier to play
		global numberOfPowerUpTypes
		if (self.powerUpType == "Grow"):
			if (gameScreen.checkIfPlayerTooSmall == True):#This is so that the length isn't increased if the player has entered the cheat code to keep them at a length of 1
				snake.IncreaseLength(gameScreen,1)
			if (snake.snakeType != "Enemy"):
				gameScreen.myPlayer.IncreaseScore(100)
		elif (self.powerUpType == "SpeedUp"):
			if (snake.snakeType != "Enemy"):
				snake.IncreaseSpeed(1)
				gameScreen.myPlayer.IncreaseScore(50)
		elif (self.powerUpType == "SlowDown"):
			snake.DecreaseSpeed(1)	
			if (snake.snakeType != "Enemy"):
				gameScreen.myPlayer.IncreaseScore(50)
		elif (self.powerUpType == "Shrink"):
			if (gameScreen.checkIfPlayerTooSmall == True):#This is to ensure the player isn't made into a size of 0, if they entered the cheat code to make them a size of 1 then keep them at that size
				snake.DecreaseLength(gameScreen,1)
		elif (self.powerUpType == "Random"):#This powerup gives more points as it will randomly assign pick a powerup from the lsit of powerups
			randomPowerNumber = random.randint(1,(numberOfPowerUpTypes - 1))
			if (randomPowerNumber == 1):
				snake.IncreaseLength(gameScreen,1)
			elif (randomPowerNumber == 2):
				snake.IncreaseSpeed(1)
			elif (randomPowerNumber == 3):
				snake.DecreaseSpeed(1)
			elif (randomPowerNumber == 4):
				snake.DecreaseLength(gameScreen,1)

			if (snake.snakeType != "Enemy"):
				gameScreen.myPlayer.IncreaseScore(150)
		elif (self.powerUpType == "Kill"):
			snake.KillSnake(gameScreen)
		elif (self.powerUpType == "BoostScore"):
			if (snake.snakeType == "Player"):
				gameScreen.myPlayer.IncreaseScore(1000)
		gameScreen.powerUps.remove(self)

	def CheckPosition(self,gameScreen,x,y):
		#This just checks if the powerup if ontop of the player snake or is ontop of another powerup
		for i in range(gameScreen.myPlayer.snake.length):
			if ((x == gameScreen.myPlayer.snake.body[i].x) and (y == gameScreen.myPlayer.snake.body[i].y)):
				return False
		for i in range(len(gameScreen.powerUps)):
			if ((x == gameScreen.powerUps[i].position.x) and (y == gameScreen.powerUps[i].position.y)):
				return False
		for i in range(len(gameScreen.enemySnakes)):
			for j in range(gameScreen.enemySnakes[i].length):
				if ((x == gameScreen.enemySnakes[i].body[j].x) and (y == gameScreen.enemySnakes[i].body[j].y)):
					return False
		return True

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

def ConvertToList(string):
	"""This is used to convert a string to a list. It will move through each item skipping them if they are any of the list parts like [], etc. If they are not those characters it will add them to a temp string value. This is to allow longer strings for the controls. When the end of these strings have been reached, so when they're not blank and there's the second ' from ['a'] only then will it add the string to the list aas the current control. Must also reset the value of the temp item here"""
	Mylist = []
	currentItem = ""
	for i in range(0,len(string)):
		if ((string[i] != "[") and (string[i] != ",") and (string[i] != "]") and (string[i] != "'") and (string[i] != " ")):
			currentItem += string[i]
		elif ((string[i] == "'") and (currentItem != "")):
			Mylist.append(currentItem)
			currentItem = ""
	return Mylist
