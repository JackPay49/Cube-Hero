# Jack Pay h61781jp
# 16/11/21
# Please note that to run this game correctly the gameRes and gameFiles must be present in the same directory as the .py file. These are needed for the saving functionality, scoreboard, cheat codes, all the game graphics and the help feature.
# My game: Cube Hero, is a snake like game. The objective is to earn points and not die. In cube hero you are a snake moving round the baord. You must be atelast of a length of 3 otherwise you will die. In cube hero you will earn points every game cycle. You will earn more points the longer you are. You can also earn points by eating powerups. There are 7 powerups that will each do something different whetehr that's instantly killing you, making you grow or speeding you up. In cube hero there are also enemy snakes. These will try to eat you but you can also eat them by running into their side. You will grow for half of the length you cut off of an enemy snake. You will also die if the player snake runs off of the board.
# In cube hero there are cheat codes, control customisation, a scoreboard,
# help documenation and saving and loading features.

import time
import random
from tkinter import Tk, Button as btn, Label as lb, Canvas as cv, Text as txt, Entry as ent, PhotoImage as img, messagebox as msgb, CENTER as algncenter, ALL, INSERT, Spinbox as numericUpDown, StringVar
# All images are original and made by myself
# Screen Resolution is 1920x1080. All screens are smaller than or equal to
# this resolution.
screenWidth = 1920
screenHeight = 1080
screenResolution = (str(screenWidth) + "x" + str(screenHeight))
# Game classes
numberOfPowerUpTypes = 7


class Block:
    # Below class is used to store a position on the baord and a direction.
    # This is to store a single section of a snake. This is used when the
    # snake is turninng and moving and just within a snake class
    x = 0
    y = 0
    facing = "Up"

    def __init__(self, xValue, yValue, fValue):
        self.x = xValue
        self.y = yValue
        self.facing = fValue


class Snake:
    color = '#0FFF50'
    length = 0
    moving = True

    snakeType = "Player"

    # The below list stores the actual body of the snake. It stores the
    # position on the board of each section and the direction that block is
    # moving in as the different parts can be moving in different ways
    body = []

    # Below stores positions on the board. When part of the snake reaches them
    # they should turn in a different direction
    turningPoints = []

    def __init__(self, stValue):
        body = []
        turningPoints = []
        length = 0
        self.snakeType = stValue
        if (self.snakeType == "Player"):
            self.color = '#0FFF50'
        else:
            self.color = '#FF5F1F'

    def Move(self, gameScreen):
        # This sub moves the snake. For each section of the snake's body it
        # will first check if the body has reached a turning point on the
        # baord. If the body section has then it will turn it's direction to
        # the one stored in the turning point. If the final section of the
        # snake passes a turning point then that turning point is no longer
        # needed and therefore it is remvoed from the turning point list. This
        # sub will then move the body of snake by just adding or subtracting
        # from the position of the body. This procedure is used every single
        # game cycle
        """test"""
        if (self.moving):
            indexToRemove = -1  # Below is used to validate whether the body has reached a turning point and then chagning the direction of movement
            i = 0
            while(i < self.length):  # This is used rather than a For loop as the length may change throughout this (like if the player find a shrink or grow powerup)
                for j in range(0, len(self.turningPoints)):
                    if ((self.body[i].x == self.turningPoints[j].x) and (
                            self.body[i].y == self.turningPoints[j].y)):
                        self.body[i].facing = self.turningPoints[j].facing
                        if (i == (self.length - 1)):
                            indexToRemove = j
                    # Below is used to remove the turning point once the final
                    # body section has passed through
                if (indexToRemove != -1):
                    self.turningPoints.remove(
                        self.turningPoints[indexToRemove])
                    # Below does the actual movement
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

                    # This will check for any game ending collisions such as
                    # colliding with the walls or colliding with the snakes own
                    # body. If either of these happen it will cause the game
                    # over sequence. If the move doesn't cause a collision then
                    # we can carry on moving and so set the new position of the
                    # snake. It only validating colliding with something on
                    # i==0 as this is the head. Only this can collide with
                    # something.
                if ((not self.CheckPosition(gameScreen, xPosition,
                                            yPosition, "Moving")) and (i == 0)):
                    self.KillSnake(gameScreen)

                else:
                    if (i < self.length):
                        self.body[i].x = xPosition
                        self.body[i].y = yPosition
                i += 1
            # This will check for collisions such as if the player intercepts a
            # powerup
            self.CheckCollisions(gameScreen)

    def KillSnake(self, gameScreen):
        self.moving = False
        self.color = "white"
        self.turningPoints = []
        # This will only cause a game over if the snake is the player. It will
        # make the snake flash white and stop moving
        if (self.snakeType == "Player"):
            gameScreen.GameOver()

    # The below procedures all do the same function for the different
    # directions. They will check to ensure that the movement is valid. So for
    # example the snake can only turn right if it is moving up or down.
    # Otherwise it is already going right or it cannot do a full 180 degree
    # turn The procedures will then change which direction the head of the
    # snake, the first block, is moving and will add the turning point to the
    # list. It adds the turning point after changing the direction the head is
    # moving as otherwise the rest of the body would keep on moving

    def UpAction(self, event):
        self.Turn("Up")

    def LeftAction(self, event):
        self.Turn("Left")

    def DownAction(self, event):
        self.Turn("Down")

    def RightAction(self, event):
        self.Turn("Right")

    def Turn(self, direction):
        valid = False
        if (direction == "Right"):
            if ((self.body[0].facing == "Up") or (
                    self.body[0].facing == "Down")):
                self.body[0].facing = "Right"
                valid = True
        elif (direction == "Left"):
            if ((self.body[0].facing == "Up") or (
                    self.body[0].facing == "Down")):
                self.body[0].facing = "Left"
                valid = True
        elif (direction == "Up"):
            if ((self.body[0].facing == "Right")
                    or (self.body[0].facing == "Left")):
                self.body[0].facing = "Up"
                valid = True
        elif (direction == "Down"):
            if ((self.body[0].facing == "Right")
                    or (self.body[0].facing == "Left")):
                self.body[0].facing = "Down"
                valid = True
        if (valid):
            self.turningPoints.append(
                Block(
                    self.body[0].x,
                    self.body[0].y,
                    self.body[0].facing))

    def CheckPosition(self, gameScreen, x, y, checkType):
        # This will ensure that the position input in is legal. It checks that
        # the position isn't outside of the grid and then checks to see whether
        # the position is already part of the current snakes body. This second
        # part is to check whether the player has run into themself
        if ((x < 0) or (x >= gameScreen.numberOfHorizontalLines)
                or (y < 0) or (y >= gameScreen.numberOfVerticalLines)):
            return False
        else:
            for i in range(0, len(self.body)):
                if ((x == self.body[i].x) and (y == self.body[i].y)):
                    return False
        if (self.snakeType == "Enemy"):
            for i in range(len(gameScreen.enemySnakes)):
                if (gameScreen.enemySnakes[i] != self):
                    for j in range(gameScreen.enemySnakes[i].length):
                        if ((gameScreen.enemySnakes[i].body[j].x == x) and (
                                gameScreen.enemySnakes[i].body[j].y == y)):
                            return False
        if ((checkType == "Spawning") and (self.snakeType == "Enemy")):
            for i in range(gameScreen.myPlayer.snake.length):
                if ((gameScreen.myPlayer.snake.body[i].x == x) and (
                        gameScreen.myPlayer.snake.body[i].y == y)):
                    return False

        return True

    def RandomlyGenerate(self, gameScreen):
        # Minimum size a snake can be is 3 long, as it reaches 2 it will die
        self.length = random.randint(3, 20)
        self.RandomlyPlace(gameScreen)

    def RandomlyPlace(self, gameScreen):
        # This procedure will repeat until the snake is palced into a valid
        # position
        valid = False
        x = 0
        y = 0
        while (not valid):
            x = random.randint(1, gameScreen.numberOfHorizontalLines - 1)
            y = random.randint(1, gameScreen.numberOfVerticalLines - 1)
            valid = self.GenerateSnakeBody(gameScreen, x, y, self.length)

    def GenerateSnakeBody(self, gameScreen, x, y, lValue):
        # This procedure will generate all the positions of the body of a snake
        # based on the position of its head and its length. It first checks
        # what direction to generate in and won't generate running straight
        # into the side of the screen. It then will then place the head of the
        # snake and just increase in length, using this pther procedure to grow
        # in a legal way. It will return true or false based on whether it
        # could be palced on the board or not successfully
        xPosition = x
        yPosition = y
        directions = ["Up", "Left", "Down", "Right"]
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
        self.body.append(Block(x, y, directionOfMovement))
        self.length = 1
        return self.IncreaseLength(gameScreen, (lValue - 1))

    def IncreaseLength(self, gameScreen, amount):
        # This procedure will increase the length of the snake and will chekc
        # to make sure it doesn't run off of the edge of the screen or collide
        # with any powerups. The snake must already have atleast a length of 1
        # and have the head placed already. It generates the new position of
        # the next body section and the direction it is generating in based off
        # of that head piece. It will check if the position is legal and place
        # the new body part at this position if so. If it is not legal then it
        # will remove this direction from the list of all possible directions,
        # will randomly pick a new one and attempt to generate this way. When
        # the snake begins generating in a new direction it will create a
        # turning point at the last body part This has a return. It will return
        # false if the snake could not be possibly placed or its length
        # couldn't be increased into any area
        if ((gameScreen.checkIfPlayerTooSmall) or (self.snakeType == "Enemy")):
            xPosition = self.body[len(self.body) - 1].x
            yPosition = self.body[len(self.body) - 1].y
            # direction of movement
            facing = self.body[len(self.body) - 1].facing
            for i in range(1, amount + 1):
                self.length += 1
                allDirections = ["Up", "Left", "Down", "Right"]
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
                    if (self.CheckPosition(gameScreen,
                                           newXPosition, newYPosition, "Spawning")):
                        valid = True
                        xPosition = newXPosition
                        yPosition = newYPosition
                        self.body.append(Block(xPosition, yPosition, facing))
                        if (changedDirections):
                            # We save the previous block as this is the one
                            # that is actually on the bend of the snake. It
                            # must be made in a new instance of Block() to
                            # ensure that it isn't updated like the body part
                            # is, when the snake moves next
                            turningPoint = Block(self.body[len(
                                self.body) - 2].x, self.body[len(self.body) - 2].y, self.body[len(self.body) - 2].facing)
                            self.turningPoints.append(turningPoint)
                    else:
                        valid = False
                        if (facing in allDirections):
                            allDirections.remove(facing)

                        if (len(allDirections) == 0):
                            return False
                        else:
                            facing = random.choice(allDirections)
                            if (i != 1):  # This is used as an error will be caused if we make a turning point of the previous body part, as obviously it doesn't exist. Also there's no need to have a turning point ahead of the head as at this point it is just changing the direction it will move off in
                                changedDirections = True
        return True

    def CheckCollisions(self, gameScreen):
        # This procedure checks through the list of powerups to see if the head
        # of the snake has intercepted any pwoerups. If it has then the powerup
        # will be activated on this snake
        count = 0
        while (count < len(gameScreen.powerUps)):
            if ((self.body[0].x == gameScreen.powerUps[count].position.x) and (
                    self.body[0].y == gameScreen.powerUps[count].position.y)):
                gameScreen.powerUps[count].PowerUpConsumed(gameScreen, self)
            else:
                count += 1
        self.CheckCollisionsWithOtherSnakes(gameScreen)

    def CheckCollisionsWithOtherSnakes(self, gameScreen):
        # This procedure will check whether snakes collide with each other. If
        # the snake is an enemy snake it will check to see if the enemy head
        # intercepts any part of the player's body. It will kill the player
        # instantly if it hits their head or a bit less than that (whilst
        # snakes must be atleast 3 long). If it will hit them then it saves the
        # place and will subtract the length past that point from the total
        # player snake's length. It will add half of this length to its own
        # length.  The same happens for the player except it will check for
        # each enemy snake too and will add score
        count = -1
        length = 0
        if (self.snakeType == "Enemy"):
            length = gameScreen.myPlayer.snake.length
            for i in range(length):
                if ((self.body[0].x == gameScreen.myPlayer.snake.body[i].x) and (
                        self.body[0].y == gameScreen.myPlayer.snake.body[i].y)):
                    count = i
            if (count != -1):
                if (count <= 1):
                    gameScreen.myPlayer.snake.KillSnake(gameScreen)
                else:
                    diff = length - count
                    length -= count
                    gameScreen.myPlayer.snake.DecreaseLength(gameScreen, diff)
                    self.IncreaseLength(gameScreen, int(diff / 2))

        elif(self.snakeType == "Player"):
            count = -1
            bodyCount = -1
            for i in range(len(gameScreen.enemySnakes)):
                for j in range(gameScreen.enemySnakes[i].length):
                    if ((gameScreen.enemySnakes[i].body[j].x == gameScreen.myPlayer.snake.body[0].x) and (
                            gameScreen.enemySnakes[i].body[j].y == gameScreen.myPlayer.snake.body[0].y)):
                        count = i
                        bodyCount = j
            if ((count != -1) and (bodyCount != -1)):
                if (bodyCount == 0):
                    self.KillSnake(gameScreen)
                else:
                    length = gameScreen.enemySnakes[count].length
                    diff = length - bodyCount
                    length -= bodyCount
                    gameScreen.enemySnakes[count].DecreaseLength(
                        gameScreen, diff)
                    self.IncreaseLength(gameScreen, int(diff / 2))
                    gameScreen.myPlayer.IncreaseScore(diff * 100)

    def DecreaseLength(self, gameScreen, amount):
        for i in range(amount):
            count = 0
            while (count < len(self.turningPoints)):
                if ((self.body[self.length - 1].x == self.turningPoints[count].x)
                        and (self.body[self.length - 1].y == self.turningPoints[count].y)):
                    self.turningPoints.remove(self.turningPoints[count])
                else:
                    count += 1
            self.body.remove(self.body[self.length - 1])
            self.length -= 1

    def SaveSnake(self, myPlayer):
        # This procedure writes up all of the details about the snake, which come down to each
        # of the body sections and all of the turning points
        file = open("gameFiles/" + myPlayer.name + "Snake.txt", "w")
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

    def LoadSnake(self, gameScreen, myPlayer):
        file = open("gameFiles/" + myPlayer.name + "Snake.txt", "r")
        self.length = int(file.readline().strip())
        self.body = []
        self.turningPoints = []
        for i in range(self.length):
            xPosition = int(file.readline().strip())
            yPosition = int(file.readline().strip())
            facing = file.readline().strip()
            self.body.append(Block(xPosition, yPosition, facing))

        file.readline()

        number = int(file.readline().strip())
        for i in range(number):
            xPosition = int(file.readline().strip())
            yPosition = int(file.readline().strip())
            facing = file.readline().strip()
            self.turningPoints.append(Block(xPosition, yPosition, facing))

        if (self.length == 1):
            gameScreen.checkIfPlayerTooSmall = False

    def DoEnemySnakeMove(self, gameScreen):
        # This procedure will make a random choice every single game cycle of
        # whether to turn the snake or not. There's a higher chance that the
        # snake will keep moving in the direction it is moving in. If the snake
        # is made to turn then it will randomly pick which direction to turn
        # into. It isn't possible to turn into directions that the snake is
        # already moving in or backwards so these directions are automatically
        # removed from the pool of possible directions It will then check if
        # the new position is a valid one. This is the case of whether the
        # snake is moving forwards or turning. If it is valid then it will do
        # the move. If it is not then , if the snake is moving straight it will
        # attempt to turn. If a turn is unsuccessful then that direction is
        # removed from the pool of possible directions to turn into. If the
        # snake runs out of directions to turn into then it will be killed
        choice = random.randint(0, 20)
        facing = self.body[0].facing
        xPosition = self.body[0].x
        yPosition = self.body[0].y

        allDirections = ["Up", "Down", "Left", "Right"]
        if ((self.body[0].facing == "Up") or (self.body[0].facing == "Down")):
            allDirections.remove("Up")
            allDirections.remove("Down")
        if ((self.body[0].facing == "Left") or (
                self.body[0].facing == "Right")):
            allDirections.remove("Right")
            allDirections.remove("Left")

        repeat = True
        while(repeat):
            repeat = False
            xPosition = self.body[0].x
            yPosition = self.body[0].y
            if (choice == 0):  # then turn in a random direction

                randomNumber = random.randint(0, len(allDirections) - 1)
                facing = allDirections[randomNumber]

            if (facing == "Right"):
                xPosition += 1
            elif (facing == "Left"):
                xPosition -= 1
            elif (facing == "Down"):
                yPosition += 1
            elif (facing == "Up"):
                yPosition -= 1

            if (self.CheckPosition(gameScreen, xPosition, yPosition, "Moving")):
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
    # This stores the player controls for up, left, down, right, pause and
    # boss screen respectively. These will be used when actraully assigning
    # controls in the game screen
    controls = ['w', 'a', 's', 'd', 'e', 'b']
    midLevel = False  # Midlevel is used to tell the program whether the player is mid way through a level already. If they are then it will actually load the level details in, but if they're not then it won't.

    snake = Snake("Player")

    difficultyLevel = 1  # Maybe 4 levels of difficulty

    def LoadPlayer(self, nValue):
        # This jsut loads in the details of the player. Important thing to note here is the loading of the controls. They are read in as a string and then a separate procedure will find the control values and
        # insert them into the array
        self.name = nValue
        file = open("gameFiles/" + self.name + ".txt", "rt")
        file.readline()
        self.password = (file.readline()).strip()
        self.highestScore = int(file.readline())
        self.score = int(file.readline())
        midLevelState = file.readline().strip()
        self.difficultyLevel = int(file.readline().strip())
        self.controls = ConvertToList(file.readline())
        file.close()
        if (midLevelState == "1"):
            self.midLevel = True
        else:
            self.score = 0

    def SavePlayer(self):
        file = open("gameFiles/" + self.name + ".txt", "wt")
        file.write(self.name + "\n")
        file.write(str(self.password) + "\n")
        file.write(str(self.highestScore) + "\n")
        if (self.midLevel):  # In the player file the midlevel boolean is stored as either a 0 or 1
            file.write(str(self.score) + "\n")  # The player score
            file.write("1\n")  # whether they're in a game
        else:
            file.write("0\n")  # score of 0
            file.write("0\n")
        file.write(str(self.difficultyLevel) + "\n")
        file.write(str(self.controls) + "\n")
        file.close()

        scoreboard = Scoreboard()
        scoreboard.LoadInScoreboard()
        scoreboard.AddScoreToScoreboard(self)
        scoreboard = None

    def CreatePlayer(self, nValue, pValue):
        self.name = nValue
        self.password = pValue
        self.SavePlayer()

    def ResetControls(self):
        self.controls = ['w', 'a', 's', 'd', 'e', 'b']
        self.SavePlayer()

    def CreateSnake(self, gameScreen, x, y, lValue):
        self.snake.GenerateSnakeBody(gameScreen, x, y, lValue)

    def IncreaseScore(self, amount):
        self.score += amount
        if (self.score > self.highestScore):
            self.highestScore = self.score


class PowerUp:
    position = None
    # Later in game dev there will be many different types of powerup like
    # speedup, grow, shrink, slowdown,etc
    powerUpType = "Grow"
    color = 'blue'
    img = None  # Powerups store their own images so that they only have to load in their image once. It can then be added to the screen as much as we need

    def __init__(self, gameScreen):
        self.RandomlyPlace(gameScreen)
        self.RandomyType()

    def MakePowerUp(self, xPosition, yPosition, type):
        self.position = Block(xPosition, yPosition, "Null")
        self.powerUpType = type
        self.img = img(file="gameRes/" + self.powerUpType + ".gif")

    def RandomyType(self):
        # This will randomly pick which type of powerup it is and will then set
        # the color based on the color
        randomNumber = random.randint(0, 11)
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
        self.img = img(file="gameRes/" + self.powerUpType + ".gif")

    def RandomlyPlace(self, gameScreen):
        # This procedure is easy. It randomly finds a position on the board and
        # will validate it. It will only place the powerup in that position if
        # it is valid
        valid = False
        while (valid == False):
            x = random.randint(0, gameScreen.numberOfHorizontalLines)
            y = random.randint(0, gameScreen.numberOfVerticalLines)
            valid = self.CheckPosition(gameScreen, x, y)
        self.position = Block(x, y, "Null")

    def PowerUpConsumed(self, gameScreen, snake):
        # This procedure is simple currently but should become far more
        # complex. It will carry out the actual function of the powerup. So it
        # will increase size of the player if it is type grow, etc, etc. The
        # Shrink powerup gives no points as it makes the game easier to play
        global numberOfPowerUpTypes
        if (self.powerUpType == "Grow"):
            # This is so that the length isn't increased if the player has
            # entered the cheat code to keep them at a length of 1
            if (gameScreen.checkIfPlayerTooSmall):
                snake.IncreaseLength(gameScreen, 1)
            if (snake.snakeType != "Enemy"):
                gameScreen.myPlayer.IncreaseScore(100)
        elif (self.powerUpType == "SpeedUp"):
            if (snake.snakeType != "Enemy"):
                gameScreen.IncreaseSpeed(1)
                gameScreen.myPlayer.IncreaseScore(50)
        elif (self.powerUpType == "SlowDown"):
            gameScreen.DecreaseSpeed(1)
            if (snake.snakeType != "Enemy"):
                gameScreen.myPlayer.IncreaseScore(50)
        elif (self.powerUpType == "Shrink"):
            # This is to ensure the player isn't made into a size of 0, if they
            # entered the cheat code to make them a size of 1 then keep them at
            # that size
            if (gameScreen.checkIfPlayerTooSmall):
                snake.DecreaseLength(gameScreen, 1)
        # This powerup gives more points as it will randomly assign pick a
        # powerup from the lsit of powerups
        elif (self.powerUpType == "Random"):
            randomPowerNumber = random.randint(1, (numberOfPowerUpTypes - 1))
            if (randomPowerNumber == 1):
                snake.IncreaseLength(gameScreen, 1)
            elif (randomPowerNumber == 2):
                gameScreen.IncreaseSpeed(1)
            elif (randomPowerNumber == 3):
                gameScreen.DecreaseSpeed(1)
            elif (randomPowerNumber == 4):
                snake.DecreaseLength(gameScreen, 1)

            if (snake.snakeType != "Enemy"):
                gameScreen.myPlayer.IncreaseScore(150)
        elif (self.powerUpType == "Kill"):
            snake.KillSnake(gameScreen)
        elif (self.powerUpType == "BoostScore"):
            if (snake.snakeType == "Player"):
                gameScreen.myPlayer.IncreaseScore(1000)
        gameScreen.powerUps.remove(self)

    def CheckPosition(self, gameScreen, x, y):
        # This just checks if the powerup if ontop of the player snake or is
        # ontop of another powerup
        for i in range(gameScreen.myPlayer.snake.length):
            if ((x == gameScreen.myPlayer.snake.body[i].x) and (
                    y == gameScreen.myPlayer.snake.body[i].y)):
                return False
        for i in range(len(gameScreen.powerUps)):
            if ((x == gameScreen.powerUps[i].position.x) and (
                    y == gameScreen.powerUps[i].position.y)):
                return False
        for i in range(len(gameScreen.enemySnakes)):
            for j in range(gameScreen.enemySnakes[i].length):
                if ((x == gameScreen.enemySnakes[i].body[j].x) and (
                        y == gameScreen.enemySnakes[i].body[j].y)):
                    return False
        return True


class Scoreboard:

    scores = []
    maxNumberOfScores = 10
    numberOfScores = 0

    # This is a basic quicksort that sorts the algorithm from greatest score
    # to smallest, 0 to 9. Based on the scores of each player
    def SortScores(self, low, high):
        tempLow = low
        tempHigh = high
        pivot = self.scores[int((low + high) / 2)].highestScore
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
            self.SortScores(low, tempHigh)
        if (tempLow < high):
            self.SortScores(tempLow, high)

    def SaveScoreboard(self):
        # This writes all scorebaorrd details into a text file. it will format them in the form of a name, then a score on a different line and then it will leave a blank line between different player scores.
        # At the top of the file there will also be the number of scores stored
        # which is used to change how long the loop will search for scores in
        # the file
        self.SortScores(0, (self.numberOfScores - 1))
        file = open("gameFiles/scoreboard.txt", "w")
        file.write(str(self.numberOfScores))
        for i in range(0, len(self.scores)):
            file.write("\n" + self.scores[i].name)
            file.write("\n" + str(self.scores[i].highestScore))
            file.write("\n")
        file.close()

    def LoadInScoreboard(self):
        # This will load in details from the scoreboard. It reads the values
        # for each player and puts them into a temporary player strcuture which
        # is then added to the scoreabord list.
        self.scores = []
        file = open("gameFiles/scoreboard.txt", "rt")
        self.numberOfScores = int(file.readline())
        for i in range(0, self.numberOfScores):
            tempPlayer = Player()
            tempPlayer.name = file.readline().strip()
            tempScore = int(file.readline())
            tempPlayer.score = tempScore
            tempPlayer.highestScore = tempScore
            file.readline()
            self.scores.append(tempPlayer)
        file.close()

    def AddScoreToScoreboard(self, newPlayer):
        # There are two possible cases to adding a score to the scorebaord. 1: the scoreboard is full already. If it is already full then it will compare to the last score in the scorebaord, the lowest. If the new
        # score is higher than that, it should be added and so replaces this last score. We then resort and save the scorebaord if it was added.
        # 2: in this case the scorebaord isn't full. In this case the new score
        # can just be added to the end of the scorebaord and it can be sorted
        # and saved.
        # This will first check to see if the player has already featured on
        # the scorebaord. It will remove them if they have, to reposition them
        self.RemoveScoreFromScoreboard(newPlayer)
        if (len(self.scores) >= self.maxNumberOfScores):
            if (newPlayer.highestScore >
                    self.scores[self.maxNumberOfScores - 1].highestScore):
                self.scores[self.maxNumberOfScores - 1] = newPlayer
                self.SortScores(0, (self.numberOfScores - 1))
                self.SaveScoreboard()
        else:
            self.scores.append(newPlayer)
            self.numberOfScores += 1
            self.SortScores(0, (self.numberOfScores - 1))
            self.SaveScoreboard()

    def RemoveScoreFromScoreboard(self, myPlayer):
        i = 0
        while i < len(self.scores):
            if (self.scores[i].name == myPlayer.name):
                self.scores.remove(self.scores[i])
                self.numberOfScores -= 1
            else:
                i += 1

# Main game


class GameScreen(Tk):
    background = cv

    lbScore = lb
    txtScore = ent

    backgroundWidth = 800
    backgroundHeight = 800
    numberOfVerticalLines = 40
    numberOfHorizontalLines = 40

    gameCycleLength = 300  # In milliseconds
    allSpeeds = [[300, 275, 250, 225], [250, 225, 200, 175], [200, 175, 150, 125], [
        150, 125, 100, 75]]  # This stores all 4 levels of speed for each of the difficulty levels
    gameSpeedLevel = 1
    gameCycleCount = 0

    myPlayer = Player()

    gameOver = False
    paused = False

    checkIfPlayerTooSmall = True

    powerUps = []
    powerUpImages = []

    pointModifier = 1
    difficultyLevel = 1

    enemySnakes = []
    # This is the number of snakes in the game based on difficulty level
    numberOfSnakes = [2, 3, 5, 6]

    def __init__(self, myPlayer):
        super().__init__()
        self.enemySnakes = []
        self.powerUps = []
        self.powerUpImages = []
        self.title("Game screen")
        self.geometry(screenResolution)

        self.background = cv(
            self,
            width=self.backgroundWidth,
            height=self.backgroundHeight)
        self.background.place(relx=0.5, rely=0.5, anchor=algncenter)
        self.background.configure(bg='black')
        self.background.pack()

        self.lbScore = lb(self, text="Score: ", font=("Default", 20, "bold"))
        self.lbScore.place(relx=0.4, rely=0.95, anchor=algncenter)
        self.txtScore = ent(self, font=("Default", 20, "bold"))
        self.txtScore.place(relx=0.6, rely=0.95, anchor=algncenter)

        self.myPlayer = myPlayer
        # We save the difficulty level lcoally to make it easier to retrieve.
        self.difficultyLevel = myPlayer.difficultyLevel

        if (self.myPlayer.midLevel == False):  # Here if the player is mid way through the level, only then will their game be loaded in and displayed. If they're not midlevel then they will always be randomly placed and be given a length of 3
            self.myPlayer.snake = Snake("Player")
            self.myPlayer.snake.length = 3
            self.myPlayer.snake.turningPoints = []
            self.myPlayer.snake.body = []
            self.myPlayer.snake.RandomlyPlace(self)
        else:
            self.LoadGame()
        self.SetSpeed()  # Sets the game cycle length based on the loaded in difficulty level and the speed saved within the game that may have just been loaded in
        self.DisplaySnake(self.myPlayer.snake)

        self.SetUpControls()
        self.StartGameCycle()

    def StartGameCycle(self):
        # This procedure does the game loop. On every iteration it clears the
        # entire board, moves each of the snakes and will then redraw all of
        # the snakes in their new positions. The final instruction is used to
        # make the delay between moves and to carry on the iterative procedure.
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

                self.gameCycleCount += 1
                self.AddPowerUps()
                self.after(self.gameCycleLength, self.StartGameCycle)

    def GameOver(self):
        # This procedure is used to end the game, like if the player collides
        # witht their own body or a wall. It will delete everything on the
        # canvas and will close the window. It then also reopens the menu
        # window.
        self.background.delete(ALL)
        self.DisplayAllElements()

        self.myPlayer.midLevel = False
        self.myPlayer.SavePlayer()
        msgb.showinfo("Game Over", "GAME OVER!!!!")
        self.gameOver = True
        self.CloseWindow(False)

    # Displaying game elements
    def DisplayAllElements(self):
        self.background.delete(ALL)
        self.DisplaySnake(self.myPlayer.snake)
        for i in range(len(self.enemySnakes)):
            self.DisplaySnake(self.enemySnakes[i])
        self.DisplayPowerUps()

    def DisplayPowerUps(self):
        # This will redisplay all of the powerup images onto the game board.
        # Don't need to load the image files in each time as they're stored
        # within the powerup objects
        gridBoxWidth = self.backgroundWidth / self.numberOfHorizontalLines
        for i in range(0, len(self.powerUps)):
            leftCornerX = (self.powerUps[i].position.x + 0.5) * gridBoxWidth
            leftCornerY = (self.powerUps[i].position.y + 0.5) * gridBoxWidth
            self.background.create_image(
                leftCornerX, leftCornerY, image=self.powerUps[i].img)

    def DisplaySnake(self, snake):
        # This will display a specific snake onto the screen. It calculates the
        # position on the baord of each section of the snake based on the
        # canvas width and the number of grid lines and will draw each body
        # section onto the canvas. This is used every single game cycle
        gridBoxWidth = self.backgroundWidth / self.numberOfHorizontalLines
        for i in range(0, snake.length):
            leftCornerX = snake.body[i].x * gridBoxWidth
            leftCornerY = snake.body[i].y * gridBoxWidth
            rightCornerX = (snake.body[i].x + 1) * gridBoxWidth
            rightCornerY = (snake.body[i].y + 1) * gridBoxWidth

            self.background.create_rectangle(
                leftCornerX,
                leftCornerY,
                rightCornerX,
                rightCornerY,
                outline="black",
                fill=snake.color)

    def CloseWindow(self, askToSave):
        # This will check if the player wants to save on certain occasions.
        # This is because we don't need to save if they lose a round of the
        # game
        saveGame = ""
        if (askToSave):
            saveGame = msgb.askquestion(
                "Quit", "Would you like to save your progress?")
            if (saveGame == 'yes'):
                self.SaveGame()
        self.background.delete(ALL)
        self.destroy()
        BeginGame()

    def AddPowerUps(self):
        # Every 10 game cycles a new powerup will be added to the screen
        if ((self.gameCycleCount % 20) == 0):
            self.gameCycleCount == 0
            self.powerUps.append(PowerUp(self))

    def CheckIfSnakesTooSmall(self):
        if (self.checkIfPlayerTooSmall):
            if (self.myPlayer.snake.length <= 2):
                self.GameOver()
        for i in range(len(self.enemySnakes)):
            if (self.enemySnakes[i].length <= 2):
                self.enemySnakes[i].KillSnake(self)

    def LoadGame(self):
        # This procedure will load in the player, their snake and the full
        # gameboard. The only detail from the game bpard to really load in is
        # all of the powerups on the screen
        self.myPlayer.LoadPlayer(self.myPlayer.name)
        self.myPlayer.snake.LoadSnake(self, self.myPlayer)
        file = open("gameFiles/" + self.myPlayer.name + "Level.txt", "r")

        self.powerUps = []
        self.gameCycleLength = int(file.readline().strip())
        number = int(file.readline().strip())
        for i in range(number):
            xPosition = int(file.readline().strip())
            yPosition = int(file.readline().strip())
            tempType = file.readline().strip()
            newPowerup = PowerUp(self)
            newPowerup.MakePowerUp(xPosition, yPosition, tempType)
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

                tempSnake.body.append(Block(xPosition, yPosition, facing))

            file.readline()

            numberOfTurningPoints = int(file.readline().strip())
            for j in range(numberOfTurningPoints):
                xPosition = int(file.readline().strip())
                yPosition = int(file.readline().strip())
                facing = file.readline().strip()

                tempSnake.turningPoints.append(
                    Block(xPosition, yPosition, facing))

            self.enemySnakes.append(tempSnake)
        file.close()

    def SaveGame(self):
        self.myPlayer.midLevel = True
        self.myPlayer.SavePlayer()
        self.myPlayer.snake.SaveSnake(self.myPlayer)
        file = open("gameFiles/" + self.myPlayer.name + "Level.txt", "w")

        file.write(str(self.gameCycleLength) + "\n")
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

        file.close()
        msgb.showinfo("Saved", "Game has been saved!")

    def DisplayScore(self):
        self.txtScore.delete(0, "end")
        self.txtScore.insert(0, self.myPlayer.score)

    def IncreasePlayerScore(self):
        # This will increase the players score by 1 times by each extra body
        # length they are on top of the base 3
        if (self.gameOver != True):
            if (self.pointModifier != 2500):
                self.pointModifier = self.myPlayer.snake.length - 2
            self.myPlayer.IncreaseScore(self.pointModifier)
            self.DisplayScore()

    def AddEnemySnake(self):
        if (len(self.enemySnakes) <
                self.numberOfSnakes[self.difficultyLevel - 1]):
            chance = random.randint(0, 10)
            if (chance == 0):
                tempSnake = Snake("Enemy")
                tempSnake.body = []
                tempSnake.turningPoints = []
                tempSnake.RandomlyGenerate(self)
                self.enemySnakes.append(tempSnake)

    def CheckForDeadEnemySnakes(self):
        i = 0
        while (i < len(self.enemySnakes)):
            # Enemy snake will be still if they are dead. Only then remove them
            if (self.enemySnakes[i].moving == False):
                self.enemySnakes.remove(self.enemySnakes[i])
            else:
                i += 1

    # Controls
    def SetUpControls(self):
        # This procedure makes all of the keybinds to be used in game. It makes
        # them using what the player input for their controls
        self.bind(
            ("<" + self.myPlayer.controls[0] + ">"),
            self.myPlayer.snake.UpAction)
        self.bind(
            ("<" + self.myPlayer.controls[1] + ">"),
            self.myPlayer.snake.LeftAction)
        self.bind(
            ("<" + self.myPlayer.controls[2] + ">"),
            self.myPlayer.snake.DownAction)
        self.bind(
            ("<" + self.myPlayer.controls[3] + ">"),
            self.myPlayer.snake.RightAction)
        self.bind(("<" + self.myPlayer.controls[4] + ">"), self.Pause)
        self.bind(("<" + self.myPlayer.controls[5] + ">"), self.BossScreen)

    def RemoveControls(self):
        self.unbind(("<" + self.myPlayer.controls[0] + ">"))
        self.unbind(("<" + self.myPlayer.controls[1] + ">"))
        self.unbind(("<" + self.myPlayer.controls[2] + ">"))
        self.unbind(("<" + self.myPlayer.controls[3] + ">"))
        self.unbind(("<" + self.myPlayer.controls[4] + ">"))
        self.unbind(("<" + self.myPlayer.controls[5] + ">"))

    # Pause functions
    def Pause(self, event):
        # This procedure pauses the game, opens the pause screen but also gets
        # rid of all keybinds. This is incase they are changed within the the
        # pause menu. This is so that the controls can be reassgined again
        self.paused = True
        self.RemoveControls()
        pauseMenu = PauseSceen(self)

    def Unpause(self):
        # We set up the controls each time after unpausing incase the player
        # decided to change them over the pause. We do the same for difficulty
        # level for the same reason
        self.paused = False
        self.SetUpControls()
        self.ResetDifficultyLevel()
        self.SetSpeed()
        self.StartGameCycle()

    def BossScreen(self, event):
        # This procedure is used whenever the player uses the boss screen
        # control. It will make the screen the boss screen or undo the boss
        # screen based on the current state. It works the same as pausing the
        # game except it also will paste an image of a word document to  make
        # it look like work is being done.
        if (self.paused):
            self.background.configure(
                width=self.backgroundWidth,
                height=self.backgroundHeight)
            self.lbScore.place(relx=0.4, rely=0.95, anchor=algncenter)
            self.txtScore.place(relx=0.6, rely=0.95, anchor=algncenter)
            self.DisplayAllElements()
            self.Unpause()
        else:
            self.paused = True
            self.background.delete(ALL)
            self.background.configure(width=screenWidth, height=screenHeight)
            self.image = img(file="gameRes/bossScreen.png")
            self.background.create_image(
                (screenWidth / 2),
                (screenHeight / 2),
                image=self.image)
            self.txtScore.place_forget()  # These two commands are used to hide the score parts
            self.lbScore.place_forget()

    def ResetDifficultyLevel(self):
        # This procedure will set the difficulty level lcoally and will remove
        # any enemy snakes until there are the correct amount of the level for
        # the difficulty level. It kills the snakes and removes them from the
        # game
        self.difficultyLevel = self.myPlayer.difficultyLevel
        if (len(self.enemySnakes) >
                self.numberOfSnakes[self.difficultyLevel - 1]):
            number = (len(self.enemySnakes) -
                      self.numberOfSnakes[self.difficultyLevel - 1])
            for i in range(number):
                self.enemySnakes[len(self.enemySnakes) - 1].KillSnake(self)
                self.enemySnakes.remove(
                    self.enemySnakes[len(self.enemySnakes) - 1])

    # The below procedures just increase or decrease the game cylce length
    # based on the difficulty level and the speed currently. The speed cannot
    # exceed a level of 4 and cannot go below 1.
    def SetSpeed(self):
        self.gameCycleLength = self.allSpeeds[self.difficultyLevel -
                                              1][self.gameSpeedLevel - 1]

    def IncreaseSpeed(self, amount):
        if ((amount + self.gameSpeedLevel) > 4):
            self.gameSpeedLevel = 4
        else:
            self.gameSpeedLevel += amount
        self.SetSpeed()

    def DecreaseSpeed(self, amount):
        if ((self.gameSpeedLevel - amount) < 1):
            self.gameSpeedLevel = 1
        else:
            self.gameSpeedLevel -= amount
        self.SetSpeed()

# Medium sized & importance screens


class Menu(Tk):
    lbTitle = lb

    btnLoadGame = btn
    btnCreateNewGame = btn
    btnScoreboard = btn
    btnClose = btn

    backgroundImage = lb

    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Menu")

        image = img(file="gameRes/background.png")
        self.backgroundImage = lb(self, image=image)
        self.backgroundImage.place(x=0, y=0, relwidth=1, relheight=1)

        self.lbTitle = TitleLabel(self, "Cube Hero!")

        # Buttons
        self.btnLoadGame = CustomButton(
            self, 0.5, 0.3, "Load Game", lambda: (
                self.destroy(), LoadGame()))

        self.btnCreateNewGame = CustomButton(
            self, 0.5, 0.5, "Create new Game", lambda: (
                self.destroy(), NewGame()))

        self.btnScoreboard = CustomButton(
            self, 0.5, 0.7, "Scoreboard", OpenScoreboard)

        self.btnClose = BackButton(self, "Close", False)

        self.mainloop()


class ScoreboardScreen(Tk):
    lbTitle = lb
    btnClose = btn
    scorebox = txt

    scoreboard = Scoreboard()

    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("Scoreboard")
        self.configure(background="black")

        self.lbTitle = TitleLabel(self, "Scoreboard")

        self.btnClose = BackButton(self, "Back", False)

        self.scoreBox = txt(self, font=("Default", 12))
        self.scoreBox.place(relx=0.5, rely=0.5, anchor=algncenter)

        self.DisplayScoreboard()
        self.mainloop()

    def DisplayScoreboard(self):
        # This procedure will load the scorebaord in. It will then format them
        # into the text box on the screen in the fornat of 'placeOnScorebaord.
        # Name: Score'. It will also make it so the scoreboard is read only
        # afterwards to prevent the player from altering scores
        self.scoreboard.LoadInScoreboard()
        scoreText = ""
        for i in range(0, self.scoreboard.numberOfScores):
            self.scoreBox.insert(INSERT, str(i + 1) + ".")
            self.scoreBox.insert(
                INSERT, self.scoreboard.scores[i].name + " : " + str(self.scoreboard.scores[i].score))
            self.scoreBox.insert(INSERT, "\n")
            self.scoreBox.insert(INSERT, "\n")
        self.scoreBox.configure(state='disabled')


class LoginScreen(Tk):
    lbTitle = lb
    lbName = lb
    lbPassword = lb

    txtName = ent
    txtPassword = ent

    btnBeginGame = btn
    btnSettings = btn
    btnClose = btn
    btnLogin = btn
    btnRules = btn

    backgroundImage = lb

    def __init__(self, newGame):
        # Important to note here. The newGame parameter is a boolean used to
        # tell us whether the login screen should be to login or to create a
        # new game. Based on this the title of the screen and the function of
        # the login button will be changed
        super().__init__()
        myPlayer = Player()
        self.geometry("600x600")
        if (newGame):
            titleText = "Create a new Game"
        else:
            titleText = "Login"
        self.title(titleText)

        image = img(file="gameRes/background.png")
        self.backgroundImage = lb(self, image=image)
        self.backgroundImage.place(x=0, y=0, relwidth=1, relheight=1)

        self.lbTitle = TitleLabel(self, titleText)

        self.lbName = CustomLabel(self, 0.2, 0.2, "Name:", False)
        self.txtName = ent(
            self,
            font=(
                "Default",
                12,
                "bold"),
            bg="black",
            fg="white")
        self.txtName.place(relx=0.5, rely=0.2, anchor=algncenter)

        self.lbPassword = CustomLabel(self, 0.2, 0.3, "Password:", False)
        self.txtPassword = ent(
            self,
            show="*",
            font=(
                "Default",
                12,
                "bold"),
            bg="black",
            fg="white")
        self.txtPassword.place(relx=0.5, rely=0.3, anchor=algncenter)

        if (newGame):
            self.btnLogin = CustomButton(
                self, 0.5, 0.4, "Create new game", lambda: self.CreateNewPlayer(
                    myPlayer, self.txtName.get(), self.txtPassword.get()))
        else:
            self.btnLogin = CustomButton(
                self, 0.5, 0.4, "Login", lambda: self.Login(
                    myPlayer, self.txtName.get(), self.txtPassword.get()))

        self.btnBeginGame = CustomButton(
            self, 0.5, 0.6, "Begin Game", lambda: (
                self.destroy(), OpenGameScreen(myPlayer)))

        self.btnSettings = CustomButton(
            self, 0.7, 0.8, "Settings", lambda: (
                OpenSettingsScreen(myPlayer)))

        self.btnRules = CustomButton(self, 0.3, 0.8, "Rules", OpenRulesScreen)

        self.btnClose = BackButton(self, "Back", True)
        self.mainloop()

    def Login(self, myPlayer, name, password):
        # This is a basic login function. It loads the player in and checks if
        # their entered password matches the saved one
        myPlayer.LoadPlayer(name)
        if (myPlayer.password == password):
            msgb.showinfo("Login", "Logged in!")
        else:
            msgb.showinfo("Login", "Password incorrect, try again!")

    def CreateNewPlayer(self, myPlayer, name, password):
        # This sub will create a player file for the new player. Doing this
        # will create an eror if the player exists already. Therefore this will
        # be caught and an error message displayed. If it is a new player Then
        # the player will be made with the input name and password, and will be
        # saved to the new file
        try:
            file = open("gameFiles/" + name + ".txt", "xt")
            file.close()
            myPlayer.CreatePlayer(name, password)
            msgb.showinfo("Login", "Account has been made!")

        except FileExistsError:
            msgb.showinfo(
                "Login",
                "User already exists! Please use a different name")
# Small screens


class PauseSceen(Tk):
    btnResumeGame = btn
    btnSaveGame = btn
    btnSettings = btn
    btnRules = btn
    btnScoreboard = btn
    btnBack = btn
    btnCheatCode = btn

    txtCheatCode = ent
    cheatCodes = []

    def __init__(self, parentWindow):
        super().__init__()
        self.geometry("300x700")
        self.title("Pause")
        self.configure(background="black")

        fontButton = ("Default", 12, "bold")
        fontNormal = ("Default", 12)

        self.lbTitle = TitleLabel(self, "Game Pause")

        self.btnResumeGame = CustomButton(
            self, 0.5, 0.2, "Resume Game", lambda: (
                parentWindow.Unpause(), self.destroy()))

        self.btnSaveGame = CustomButton(
            self, 0.5, 0.3, "Save Game", parentWindow.SaveGame)

        self.btnSettings = CustomButton(
            self, 0.5, 0.4, "Settings", lambda: (
                OpenSettingsScreen(
                    parentWindow.myPlayer)))

        self.btnRules = CustomButton(self, 0.5, 0.5, "Rules", OpenRulesScreen)

        self.btnScoreboard = CustomButton(
            self, 0.5, 0.6, "Scoreboard", OpenScoreboard)

        self.btnCheatCode = CustomButton(
            self, 0.5, 0.7, "Enter Cheat Code", lambda: (
                self.EnterCheatCode(parentWindow)))
        self.txtCheatCode = ent(self, font=fontNormal)
        self.txtCheatCode.place(relx=0.5, rely=0.8, anchor=algncenter)

        self.btnBack = CustomButton(
            self, 0.5, 0.9, "Quit Game", lambda: (
                self.destroy(), parentWindow.CloseWindow(True)))

        self.mainloop()

    def LoadInCheatCodes(self):
        file = open("gameFiles/cheatCodes.txt", "r")
        numberOfCheatCodes = int(file.readline().strip())
        self.cheatCodes = []
        for i in range(numberOfCheatCodes):
            tempString = file.readline().strip()
            self.cheatCodes.append(tempString)

    def EnterCheatCode(self, gameScreen):
        takenCheatCode = False
        self.LoadInCheatCodes()
        userInput = self.txtCheatCode.get().strip()
        if (self.cheatCodes[0] in userInput):
            gameScreen.myPlayer.snake.IncreaseLength(gameScreen, 10)
            takenCheatCode = True
        if (self.cheatCodes[1] in userInput):
            gameScreen.myPlayer.snake.DecreaseLength(
                gameScreen, int(gameScreen.myPlayer.snake.length / 2))
            takenCheatCode = True
        if (self.cheatCodes[2] in userInput):
            gameScreen.IncreaseSpeed(3)
            takenCheatCode = True
        if (self.cheatCodes[3] in userInput):
            gameScreen.DecreaseSpeed(3)
            takenCheatCode = True
        if (self.cheatCodes[4] in userInput):
            takenCheatCode = True
            gameScreen.checkIfPlayerTooSmall = False
            gameScreen.myPlayer.snake.DecreaseLength(
                gameScreen, gameScreen.myPlayer.snake.length - 1)
            while (len(gameScreen.myPlayer.snake.turningPoints) > 0):
                gameScreen.myPlayer.snake.turningPoints.remove(
                    gameScreen.myPlayer.snake.turningPoints[0])
        if (self.cheatCodes[5] in userInput):
            gameScreen.pointModifier = 2500
            takenCheatCode = True
        if (takenCheatCode):
            msgb.showinfo("Accepted!", "Cheat code has been accepted!")


class RulesScreen(Tk):
    btnBack = btn

    lbTitle = lb

    txtRules = txt

    def __init__(self):
        super().__init__()
        self.geometry(screenResolution)
        self.title("Rules")
        self.configure(background="black")

        lbTitle = TitleLabel(self, "Welcome to Cube Hero!")
        btnBack = BackButton(self, "Back", False)

        file = open("gameFiles/rules.txt", "r")
        rules = file.read()
        file.close()

        self.txtRules = txt(self, font=("Default", 12))
        self.txtRules.place(relx=0.5, rely=0.5, anchor=algncenter)
        self.txtRules.insert(INSERT, rules)

        self.mainloop()


class SettingsScreen(Tk):
    lbUpControl = lb
    lbRightControl = lb
    lbLeftControl = lb
    lbDownControl = lb
    lbPauseControl = lb
    lbBossControl = lb
    lbTitle = lb
    lbDifficultyLevel = lb

    nudDifficultyLevel = numericUpDown

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

    def __init__(self, myPlayer):
        super().__init__()
        self.geometry("600x800")
        self.title("Settings")
        self.configure(background="black")

        fontNormal = ("Default", 12)

        self.lbTitle = TitleLabel(self, "Settings")

        self.lbUpControl = CustomLabel(self, 0.2, 0.2, "Up Control:", False)
        self.txtUpControl = ent(self, font=fontNormal)
        self.txtUpControl.place(relx=0.5, rely=0.2, anchor=algncenter)

        self.lbLeftControl = CustomLabel(
            self, 0.2, 0.25, "Left Control:", False)
        self.txtLeftControl = ent(self, font=fontNormal)
        self.txtLeftControl.place(relx=0.5, rely=0.25, anchor=algncenter)

        self.lbDownControl = CustomLabel(
            self, 0.2, 0.3, "Down Control:", False)
        self.txtDownControl = ent(self, font=fontNormal)
        self.txtDownControl.place(relx=0.5, rely=0.3, anchor=algncenter)

        self.lbRightControl = CustomLabel(
            self, 0.2, 0.35, "Right Control:", False)
        self.txtRightControl = ent(self, font=fontNormal)
        self.txtRightControl.place(relx=0.5, rely=0.35, anchor=algncenter)

        self.lbPauseControl = CustomLabel(
            self, 0.2, 0.4, "Pause Control:", False)
        self.txtPauseControl = ent(self, font=fontNormal)
        self.txtPauseControl.place(relx=0.5, rely=0.4, anchor=algncenter)

        self.lbBossControl = CustomLabel(
            self, 0.2, 0.45, "Boss Control:", False)
        self.txtBossControl = ent(self, font=fontNormal)
        self.txtBossControl.place(relx=0.5, rely=0.45, anchor=algncenter)

        # StringVar is needed here to be able to set the default value of the
        # difficutly level
        difficultyLevel = StringVar(self)
        difficultyLevel.set(str(myPlayer.difficultyLevel))
        self.lbDifficultyLevel = CustomLabel(
            self, 0.2, 0.5, "Difficulty Level:", False)
        self.nudDifficultyLevel = numericUpDown(
            self, from_=1, to=4, textvariable=difficultyLevel)
        self.nudDifficultyLevel.place(relx=0.5, rely=0.5, anchor=algncenter)

        # This fills in all of the text boxes with the values of the controls
        self.DisplaySettings(myPlayer)

        self.btnResetControls = CustomButton(
            self, 0.5, 0.6, "Reset Controls", lambda: (
                self.ResetControls(myPlayer)))

        self.btnSaveChanges = CustomButton(
            self, 0.5, 0.7, "Save Changes", lambda: (
                self.SaveChanges(myPlayer)))

        self.btnInfo = CustomButton(self, 0.5, 0.8, "Info", self.DisplayInfo)

        self.btnClose = BackButton(self, "Back", False)
        self.mainloop()

    def DisplayInfo(self):
        msgb.showinfo("Info", "You can enter any characters here to set them as your controls for the game. Please note that the case of characters is taken into account. If you wish to use the Arrow keys you must enter 'Up', 'Left', 'Down' or 'Right depending on the key.")

    def ResetControls(self, myPlayer):
        # This procedure will set and save the player controls to the default.
        # It then redisplays them on screen
        myPlayer.ResetControls()
        self.DisplaySettings(myPlayer)

    def DisplaySettings(self, myPlayer):
        # This procedure will delete all of the text within the entry controls
        # and will then re-insert all of the player controls. Must do this due
        # to the entry control
        self.txtUpControl.delete(0, "end")
        self.txtLeftControl.delete(0, "end")
        self.txtDownControl.delete(0, "end")
        self.txtRightControl.delete(0, "end")
        self.txtPauseControl.delete(0, "end")
        self.txtBossControl.delete(0, "end")

        self.txtUpControl.insert(0, myPlayer.controls[0])
        self.txtLeftControl.insert(0, myPlayer.controls[1])
        self.txtDownControl.insert(0, myPlayer.controls[2])
        self.txtRightControl.insert(0, myPlayer.controls[3])
        self.txtPauseControl.insert(0, myPlayer.controls[4])
        self.txtBossControl.insert(0, myPlayer.controls[5])

    def SaveChanges(self, myPlayer):
        # This procedure gets the text fromm all of the entries, strips away
        # any white space connected to the controls and will then fill in the
        # player controls list.
        myPlayer.controls[0] = self.txtUpControl.get().strip()
        myPlayer.controls[1] = self.txtLeftControl.get().strip()
        myPlayer.controls[2] = self.txtDownControl.get().strip()
        myPlayer.controls[3] = self.txtRightControl.get().strip()
        myPlayer.controls[4] = self.txtPauseControl.get().strip()
        myPlayer.controls[5] = self.txtBossControl.get().strip()
        myPlayer.difficultyLevel = int(self.nudDifficultyLevel.get())
        myPlayer.SavePlayer()
        msgb.showinfo("Saved!", "Changes to controls have been saved!")

# Classees for general controls


class BackButton(btn):
    # This is a reusable back button. It will position itself in the same and
    # correct place on screen each time. It's text will change based on the
    # input parameter as some back buttons must say back Whilst others need to
    # say quit. It also takes the boolean value of openMenu which is used to
    # tell whether we should reopen the menu after closing the parentwindow
    # (the window it is put into) So if that value is true then it will reopen
    # the menu like for the login screen
    def __init__(self, parentWindow, textValue, openMenu):
        super().__init__()
        self = btn(
            parentWindow,
            text=textValue,
            font=(
                "Default",
                12,
                "bold"),
            bg="black",
            fg="white")
        self.place(relx=0.5, rely=0.9, anchor=algncenter)
        if (openMenu):
            self.configure(
                command=lambda: (
                    parentWindow.destroy(),
                    BeginGame()))
        else:
            self.configure(command=lambda: (parentWindow.destroy()))


class TitleLabel(lb):
    # This is a reusable title label. It will fomrat and position the label
    # correctly on the screen and will fill in the text based on the input
    # parameter
    def __init__(self, parentWindow, textValue):
        super().__init__()
        self = lb(parentWindow, text=textValue)
        self.place(relx=0.5, rely=0.1, anchor=algncenter)
        StyleControl(self, "Title")


class CustomButton(btn):
    # This class is a general button class. It will automatically place, set
    # the font, set the background and font color of a new button. It will
    # also assign it the given command. This saves having to do this for every
    # single button, changing from two or three lines to 1
    def __init__(self, parentWindow, x, y, textValue, command):
        super().__init__()
        self = btn(
            parentWindow,
            text=textValue,
            font=(
                "Default",
                12,
                "bold"),
            bg="black",
            fg="white",
            command=command)
        self.place(relx=x, rely=y, anchor=algncenter)


class CustomLabel(lb):
    # General label function that sets the color and font of the label. There
    # are two diffeent types: one for titles, with an underline, and one
    # without.
    def __init__(self, parentWindow, x, y, textValue, title):
        super().__init__()
        if (title):
            self = lb(
                parentWindow,
                text=textValue,
                font=(
                    "Default",
                    25,
                    "bold",
                    "underline"),
                bg="black",
                fg="white")
        else:
            self = lb(
                parentWindow,
                text=textValue,
                font=(
                    "Default",
                    12,
                    "bold"),
                bg="black",
                fg="white")
        self.place(relx=x, rely=y, anchor=algncenter)

# General functions


def ConvertToList(string):
    """This is used to convert a string to a list. It will move through each item skipping them if they are any of the list parts like [], etc. If they are not those characters it will add them to a temp string value. This is to allow longer strings for the controls. When the end of these strings have been reached, so when they're not blank and there's the second ' from ['a'] only then will it add the string to the list aas the current control. Must also reset the value of the temp item here"""
    Mylist = []
    currentItem = ""
    for i in range(0, len(string)):
        if ((string[i] != "[") and (string[i] != ",") and (string[i] != "]") and (
                string[i] != "'") and (string[i] != " ")):
            currentItem += string[i]
        elif ((string[i] == "'") and (currentItem != "")):
            Mylist.append(currentItem)
            currentItem = ""
    return Mylist


def StyleControl(control, type):
    if (type in ["Button", "button", "btn", "Entry", "ent", "entry"]):
        control.configure(font=("Default", 12, "bold"), bg="black", fg="white")
    elif (type in ["Label", "label", "lb"]):
        control.configure(
            font=(
                "Default",
                12,
                "bold",
                "underline"),
            bg="black",
            fg="white")
    elif (type in ["Title", "Title Label", "titleLabel"]):
        control.configure(
            font=(
                "Default",
                25,
                "bold",
                "underline"),
            bg="black",
            fg="white")


# Opening screens
def OpenScoreboard():
    windowScoreboard = ScoreboardScreen()


def OpenRulesScreen():
    rulesScreen = RulesScreen()


def OpenSettingsScreen(myPlayer):
    if (myPlayer.name == ""):
        msgb.showinfo("Error", "Please Login first!")
    else:
        windowSettingsScreen = SettingsScreen(myPlayer)


def OpenGameScreen(myPlayer):
    gameScreen = GameScreen(myPlayer)


def LoadGame():
    # Opens the login screen. NewGame variable is set to false as we are
    # loading a game
    windowLogin = LoginScreen(False)


def NewGame():
    # Opens the login screen. NewGame variable is set to true as we are making
    # a new game
    windowLogin = LoginScreen(True)


def BeginGame():
    # Main sub that runs the program
    global screenResolution, screenWidth, screenHeight
    windowMenu = Menu()


BeginGame()  # Needed here at the end for the full program to be run. Must be specified last otherwise the other things won't have been declared yet
