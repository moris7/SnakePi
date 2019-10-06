import random

class def_clsRandom:
	
	def __init__(self):
		self = self

	def SensRandom(self, Sens):
	
		found = 0
	
		while found == 0:
	
			alea = random.randint(1,4)

			if alea == 1:
				NewSens = "bas"
				Opposite = "haut"
			elif alea == 2:
				NewSens = "haut"
				Opposite = "bas"
			elif alea == 3:
				NewSens = "gauche"
				Opposite = "droite"
			elif alea == 4:
				NewSens = "droite"
				Opposite = "gauche"
			
			if Sens != Opposite:
				found=1
	
		return NewSens
		
	def GetRandom(self, value, MaxValue):
		if value == 1:
			return random.randint(0,1)
		elif value == MaxValue:
			return random.randint(-1,0)
		else:
			return random.randint(-1,1)

	def GetRandomForce(self, value, MaxValue):
		resultat=0

		while resultat==0:
			resultat = self.GetRandom(value, MaxValue)

		return resultat