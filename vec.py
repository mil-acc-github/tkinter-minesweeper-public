from turtle import Vec2D


class Vec2(Vec2D):

	@property
	def x(self):
		return self[0]
	
	@property
	def y(self):
		return self[1]

	def __repr__(self):
		return f"Vec(x={self.x}, y={self.y})"

	def distance(self, o):
		return ( (self.x - o.x) ** 2 + (self.y - o.y) ** 2 ) ** 0.5
