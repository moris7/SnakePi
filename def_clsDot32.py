import time

class def_clsDot32(object):
	def __init__(self, X, Y, r, g, b, EstFatal, Points, type, Sens, Show):
		self.X = X
		self.Y = Y
		self.r = r
		self.g = g
		self.b = b
		self.EstFatal = EstFatal
		self.Points = Points
		self.type = type
		self.Sens = Sens
		self.Show = Show
		
	def NewXY(self, randomX, randomY):
		self.X += randomX
		self.Y += randomY
		#print str(self.X) + "-" + str(self.Y)
		
	def PrintCoord(self):
		print str(self.X) + "," + str(self.Y)