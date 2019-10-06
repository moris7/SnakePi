import time
from rgbmatrix import Adafruit_RGBmatrix
from def_clsDot32 import def_clsDot32 as def_clsDot
from def_Scores import def_Scores



class def_clsLightMatrix32:

	def __init__(self, device):
		self.device = device

	def lightUpDots(self, XYdots, delai):

		self.device.Clear()

		for dot in reversed(XYdots):
			#print str(dot.X-1) + "-" + str(dot.Y-1)
			if dot.Show == True:
				self.device.SetPixel(dot.X-1, dot.Y-1, dot.r, dot.g, dot.b)

		time.sleep(delai)
		
	def Explosion(self, centerX, centerY, MatrixMaxX, MatrixMaxY, Score):

		#print "BOOOOOOOOOM"

		#print "Explosition a : " + str(centerX) + "-" + str(centerY)

		for j in range(0,2): # le fait 2 fois
			self.device.Clear()

			for i in range(0,MatrixMaxX): #grandit a partir du centre

				BOOM = []

				for x in range(-i,i+1):
					for y in range(-i,i+1):
						if (centerX+x >= 1 and centerY+y>=1 and centerX+x <= MatrixMaxX and centerY+y<=MatrixMaxY):
							BOOM.append(def_clsDot(centerX+x, centerY+y, 255, 0, 0, True, 0, "boom", "", True))	

				self.lightUpDots(BOOM, 0.05)

		#print "cleanup explosion"
		self.device.Clear()
		
		NewScore = def_Scores(Score)

		print "Vous etes le top " + str(NewScore.FinalCount) + " avec " + str(NewScore.newScore) + " points !"
		
		return True