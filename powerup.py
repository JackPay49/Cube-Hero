import random
from block import Block as blk
class PowerUp:
	position = None
	powerUpType = "Grow"#Later in game dev there will be many different types of powerup like speedup, grow, shrink, slowdown,etc
	color = 'blue'


	def __init__(self,gameScreen):
		self.RandomlyPlace(gameScreen)
		self.RandomyType()

	def MakePowerUp(self,xPosition,yPosition,type):
		self.position = blk(xPosition,yPosition,"Null")
		self.powerUpType = type

	def RandomyType(self):
		#This will randomly pick which type of powerup it is and will then set the color based
		#on the color
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
	def RandomlyPlace(self,gameScreen):
		#This procedure is easy. It randomly finds a position on the board and will validate it. It will only place the powerup in that position if it is valid
		valid = False
		while (valid == False):
			x = random.randint(0,gameScreen.numberOfHorizontalLines)
			y = random.randint(0,gameScreen.numberOfVerticalLines)
			valid = self.CheckPosition(gameScreen,x,y)
		self.position = blk(x,y,"Null")

	def PowerUpConsumed(self,gameScreen,snake):
		#This procedure is simple currently but should become far more complex. It will carry out the actual function of the powerup. So it will increase size of the player if it is type grow, etc, etc.
		#The Shrink powerup gives no points as it makes the game easier to play
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