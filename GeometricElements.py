class Size:
	def __init__(self, width, height):
		self.widthValue = float(width)
		self.heightValue = float(height)

	@property
	def width(self):
		return self.widthValue

	@property
	def height(self):
		return self.heightValue

	def getTuple(self):
		return (self.widthValue, self.heightValue)

class Rectangle:
	def __init__(self, x, y, width, height):
		self.xValue = float(x)
		self.yValue = float(y)
		self.widthValue = float(width)
		self.heightValue = float(height)
	
	@property
	def x(self):
		return self.xValue

	@property
	def y(self):
		return self.yValue

	@property
	def width(self):
		return self.widthValue

	@property
	def height(self):
		return self.heightValue

	def getTuple(self):
		return ((int(self.xValue), int(self.yValue)), 
			(int(self.xValue + self.widthValue), int(self.yValue + self.heightValue)))

	@classmethod
	def FromTuple(cls, tuple):
		return cls(tuple[0], tuple[1], tuple[2], tuple[3])

class Point:
	def __init__(self, x, y):
		self.xValue = float(x)
		self.yValue = float(y)

	@property
	def x(self):
		return self.xValue

	@property
	def y(self):
		return self.yValue

	def getTuple(self):
		return (self.xValue, self.yValue)



#Testing
if __name__ == '__main__':

	print 'Testing Size class...'
	size = Size(10.7, 21.8)
	print size.width
	print size.height
	print size.getTuple()
	print ''

	print 'Testing Rectangle class...'
	rectangle = Rectangle(0.3, 0.1, 10.2, 5.4)
	print rectangle.width
	print rectangle.height
	print rectangle.x
	print rectangle.y
	print rectangle.getTuple()
	rectangle = Rectangle.FromTuple(((0.3, 0.1), (10.5, 5.5)))
	print rectangle.width
	print rectangle.height
	print rectangle.x
	print rectangle.y
	print rectangle.getTuple()
	print ''

	print 'Testing Point class...'
	point = Point(2.3, 6.8)
	print point.x
	print point.y
	print point.getTuple()