import random
from block import Block as blk
class Snake:
	color = '#0FFF50'
	length = 0
	moving = True

	speed = 1

	snakeType = "Player"

	#The below list stores the actual body of the snake. It stores the position on the board of each section and
	#the direction that block is moving in as the different parts can be moving in different ways
	body = []

	#Below stores positions on the board. When part of the snake reaches them they should turn in a different
	#direction
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
		

	#The below procedures all do the same function for the different directions. They will check to ensure that the movement is valid. So for example
	#the snake can only turn right if it is moving up or down. Otherwise it is already going right or it cannot do a full 180 degree turn
	#The procedures will then change which direction the head of the snake, the first block, is moving and will add the turning point to the list. It
	#adds the turning point after changing the direction the head is moving as otherwise the rest of the body would keep on moving
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
			self.turningPoints.append(blk(self.body[0].x,self.body[0].y,self.body[0].facing))


	def CheckPosition(self,gameScreen,x,y,checkType):
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
		#This procedure will generate all the positions of the body of a snake based on the position of its head and its length. It first checks what direction to generate in
		# and won't generate running straight into the side of the screen. It then will then place the head of the snake and just increase in length, using this pther procedure
		#to grow in a legal way. It will return true or false based on whether it could be palced on the board or not successfully						 
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
		self.body.append(blk(x,y,directionOfMovement))
		self.length = 1
		return self.IncreaseLength(gameScreen,(lValue - 1))



	def IncreaseLength(self,gameScreen,amount):
		#This procedure will increase the length of the snake and will chekc to make sure it doesn't run off of the edge of the screen or collide with any powerups. The snake must already have atleast a length of 1 and have the head placed already
		#It generates the new position of the next body section and the direction it is generating in based off of that head piece. It will check if the position is legal and place the new body part at this position if so. If it is not legal then
		#it will remove this direction from the list of all possible directions, will randomly pick a new one and attempt to generate this way. When the snake begins generating in a new direction it will create a turning point at the last body part
		#This has a return. It will return false if the snake could not be possibly placed or its length couldn't be increased into any area
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
					self.body.append(blk(xPosition,yPosition,facing))
					if (changedDirections):
						turningPoint = blk(self.body[len(self.body) - 2].x,self.body[len(self.body) - 2].y,self.body[len(self.body) - 2].facing)#We save the previous block as this is the one that is actually on the bend of the snake. It must
						#be made in a new instance of blk() to ensure that it isn't updated like the body part is, when the snake moves next
						self.turningPoints.append(turningPoint)
				else:
					valid = False
					if (facing in allDirections):
						allDirections.remove(facing)

					if (len(allDirections) == 0):
						return False
					else:
						facing = random.choice(allDirections)
						if (i != 1):#This is used as an error will be caused if we make a turning point of the previous body part, as obviously it doesn't exist. Also there's no need to have a turning point
						#ahead of the head as at this point it is just changing the direction it will move off in
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
		#This procedure will check whether snakes collide with each other. If the snake is an enemy snake it will check to
		#see if the enemy head intercepts any part of the player's body. It will kill the player instantly if it hits
		# their head or a bit less than that (whilst snakes must be atleast 3 long). If it will hit them then it saves the
		# place and will subtract the length past that point from the total player snake's length. It will add half of
		#this length to its own length. 
		#The same happens for the player except it will check for each enemy snake too and will add score
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
			self.body.append(blk(xPosition,yPosition,facing))

		file.readline()

		number = int(file.readline().strip())
		for i in range(number):
			xPosition = int(file.readline().strip())
			yPosition = int(file.readline().strip())
			facing = file.readline().strip()
			self.turningPoints.append(blk(xPosition,yPosition,facing))

		self.speed = int(file.readline().strip())

		if (self.length == 1):
			gameScreen.checkIfPlayerTooSmall = False

	def DoEnemySnakeMove(self,gameScreen):
		#This procedure will make a random choice every single game cycle of whether to turn the snake or not. There's a
		#higher chance that the snake will keep moving in the direction it is moving in. If the snake is made to turn then
		#it will randomly pick which direction to turn into. It isn't possible to turn into directions that the snake is
		#already moving in or backwards so these directions are automatically removed from the pool of possible directions
		#It will then check if the new position is a valid one. This is the case of whether the snake is moving forwards
		#or turning. If it is valid then it will do the move. If it is not then , if the snake is moving straight it will
		#attempt to turn. If a turn is unsuccessful then that direction is removed from the pool of possible directions to
		#turn into. If the snake runs out of directions to turn into then it will be killed
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
