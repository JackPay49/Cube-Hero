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