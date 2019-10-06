import os
import time, datetime
from rgbmatrix import Adafruit_RGBmatrix
import sys
import copy
import curses
import random
from def_clsDot32 import def_clsDot32 as def_clsDot
from def_clsLightMatrix32 import def_clsLightMatrix32 as def_clsLightMatrix
from def_clsRandom import def_clsRandom
import Tkinter as tk
			
def MoveSnake():
	
	global Snake
	global Sens
	global MatrixMaxX
	global MatrixMaxY
	global Mur
	global FrappeSnake
	global gaterie
	global GameOver
	global Score
	global ModeInvincible
	global DebutInvincible
	global Tirs
	global Shoot
	
	if len(Snake)==0:
		return
	
	tete = copy.copy(Snake[0])
	teteOld = copy.copy(Snake[0])
	
	#Bouge la tete
	if Sens == "droite":
		tete.X += 1
	elif Sens == "gauche":
		tete.X -= 1
	elif Sens == "bas":
		tete.Y += 1
	elif Sens == "haut":
		tete.Y -= 1
	else:
		print "COMMANDE INCONNUE"	
	
	#Ajoute un tir si voulu
	if Shoot == 1:
		Shoot = 0
		Tirs.append(def_clsDot(teteOld.X, teteOld.Y, 255, 255, 255, True, 0, "tir", Sens, False))
		Tirs.append(def_clsDot(tete.X, tete.Y, 255, 255, 255, True, 0, "tir", Sens, True))
		
	#On fait avancer les tirs
	for tir in Tirs:
		if tir.Sens == "droite":
			tir.X += 2
		elif tir.Sens == "gauche":
			tir.X -= 2
		elif tir.Sens == "bas":
			tir.Y += 2
		elif tir.Sens == "haut":
			tir.Y -= 2
		else:
			print "COMMANDE INCONNUE"
			
	#Enleve les tirs sorti de l'ecran
	for i in range(len(Tirs)-1, -1, -1):
		if Tirs[i].X>MatrixMaxX or Tirs[i].X<1 or Tirs[i].Y > MatrixMaxY or Tirs[i].Y < 1:
			Tirs.remove(Tirs[i])

	bFound=False
	
	#Check si trouve une des gateries...si oui...alors devient plus grand sans deplacer le corps
	for i in range(len(gaterie)-1, -1, -1):
		
		#gaterie[i].PrintCoord()
	
		if (tete.X == gaterie[i].X and tete.Y == gaterie[i].Y):
			#Ajoute un nouveau dot dans le snake et repige une gaterie
			Score += gaterie[i].Points * ScoreMult
			print "Points : " + str(Score)
			Snake.insert(0, tete)
			gaterie.remove(gaterie[i])
			bFound=True
			continue
			
		for j in range(len(Tirs)-1, -1, -1):
			if Tirs[j].X == gaterie[i].X and Tirs[j].Y == gaterie[i].Y:
				#Le tir a frappe une gaterie
				
				Score += gaterie[i].Points * ScoreMult
				print "Points : " + str(Score)
				
				gaterie.remove(gaterie[i])
				Tirs.remove(Tirs[j])
				break
				
		if len(gaterie)==0:
			for dot in CreationSpecial("gaterie"):
				gaterie.append(dot)
				
	#Check si pogne un obstacle	
	for j in range(len(obstacles)-1, -1, -1):
		
		ForceBreak = False
	
		for i in range(len(obstacles[j])-1, -1, -1):

			if (tete.X == obstacles[j][i].X and tete.Y == obstacles[j][i].Y):
				if ModeInvincible==True:
					print "Casse un obstacle"
					Score += obstacles[j][i].Points * ScoreMult
					print "Points : " + str(Score)
					obstacles.remove(obstacles[j])
					break
				else:
					print "Frappe un obstacle"
					gLightMatrix.Explosion(tete.X, tete.Y, MatrixMaxX, MatrixMaxY, Score)  #Position 1 etait la derniere position viable de la tete
					GameOver=True
					return []
					
			for k in range(len(Tirs)-1, -1, -1):
				if Tirs[k].X == obstacles[j][i].X and Tirs[k].Y == obstacles[j][i].Y:
					#Le tir a frappe un obstacle
					
					Score += obstacles[j][i].Points * ScoreMult
					print "Points : " + str(Score)
					
					obstacles.remove(obstacles[j])
					Tirs.remove(Tirs[k])
					ForceBreak=True
					break
					
			if ForceBreak==True:
				break
					
	#Check si pogne un mur
	if Mur == 1:
		for i in range(len(Murs)-1, -1, -1):

			if (tete.X == Murs[i].X and tete.Y == Murs[i].Y and Murs[i].EstFatal==True):
				if ModeInvincible==True:
					print "Casse un mur"
					Score += Murs[i].Points * ScoreMult
					print "Points : " + str(Score)
					Murs.remove(Murs[i])
					break
				else:
					print "Frappe un mur"
					gLightMatrix.Explosion(tete.X, tete.Y, MatrixMaxX, MatrixMaxY, Score)  #Position 1 etait la derniere position viable de la tete
					GameOver=True
					return []
					
			for k in range(len(Tirs)-1, -1, -1):
				if Tirs[k].X == Murs[i].X and Tirs[k].Y == Murs[i].Y:
					#Le tir a frappe un mur
					
					Score += Murs[i].Points * ScoreMult
					print "Points : " + str(Score)
					
					Murs.remove(Murs[i])
					Tirs.remove(Tirs[k])
					break
			
	#Check si pogne une etoile	
	for j in range(len(etoiles)-1, -1, -1):
		for i in range(len(etoiles[j])-1, -1, -1):

			if (tete.X == etoiles[j][i].X and tete.Y == etoiles[j][i].Y):
				print "Frappe une etoile"
				ModeInvincible = True
				DebutInvincible = time.time()
			
				#Remove l'etoile
				etoiles.remove(etoiles[j])
				break
	
	if bFound == False:

		#Bouge la queue
		for i in range(len(Snake)-1, 0, -1):
			Snake[i].X = Snake[i-1].X
			Snake[i].Y = Snake[i-1].Y
	
		#replace la tete
		Snake[0] = tete	
		
	#VERIFICATION si on passe par le mur ou non
	if Snake[0].X < 1 or Snake[0].X > MatrixMaxX or Snake[0].Y < 1 or Snake[0].Y > MatrixMaxY:
		if Snake[0].X < 1:
			Snake[0].X = MatrixMaxX
		elif Snake[0].X > MatrixMaxX:
			Snake[0].X = 1
		elif Snake[0].Y < 1:
			Snake[0].Y = MatrixMaxY
		elif Snake[0].Y > MatrixMaxY:
			Snake[0].Y = 1
	
	if FrappeSnake == 1:   #Si peut se frapper....
		ForceBreak=False
		for i in range(len(Snake)-2, 0, -1):
			if Snake[0].X == Snake[i].X and Snake[0].Y == Snake[i].Y:	
				print "frappe un Snake"
			
				gLightMatrix.Explosion(Snake[0].X, Snake[0].Y, MatrixMaxX, MatrixMaxY, Score)  #Position 1 etait la derniere position viable de la tete
				GameOver=True
				return []
				
			#Check si les tirs frappe le Snake...si oui perd la queue
			for k in range(len(Tirs)-1, -1, -1):
				if Tirs[k].X == Snake[i].X and Tirs[k].Y == Snake[i].Y:
					#Le tir a frappe un Snake
					Tirs.remove(Tirs[k])
					
					#Coupe la queue
					for i in range(len(Snake)-1, i, -1):
						Score -= Snake[i].Points * ScoreMult
						Snake.remove(Snake[i])
						
					ForceBreak=True
					break
					
			if ForceBreak == True:
				break
				
	return Snake
	

	
def CreationSpecial(type):
	
	global MatrixMaxX
	global MatrixMaxY
	global Snake
	global gaterie
	global obstacles
	global Tirs
	
	found = 0
	
	AllDots = copy.copy(Snake)
	
	for i in range(0, len(gaterie)):
		AllDots.append(copy.copy(gaterie[i]))
		
	for j in range(0, len(obstacles)):
		for i in range(0, len(obstacles[j])):
			AllDots.append(copy.copy(obstacles[j][i]))
	
	for j in range(0, len(etoiles)):
		for i in range(0, len(etoiles[j])):
			AllDots.append(copy.copy(etoiles[j][i]))
			
	for i in range(0, len(Tirs)):
		AllDots.append(copy.copy(Tirs[i]))
	
	while found == 0:
		
		#print type

		BreakForce=False
		newSpecial=[]
		if type == "gaterie":
			newSpecial.append(def_clsDot(random.randint(1,MatrixMaxX),random.randint(1,MatrixMaxY), 0, 255, 0, False, 50, type, "", True))
		
		if type == "obstacle":
			newSpecial.append(def_clsDot(random.randint(1,MatrixMaxX),random.randint(1,MatrixMaxY), 255, 0, 0, True, 100, type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X-1, newSpecial[0].Y, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X-1, newSpecial[0].Y-1, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X, newSpecial[0].Y-1, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))

		if type == "etoile":
			newSpecial.append(def_clsDot(random.randint(1,MatrixMaxX),random.randint(1,MatrixMaxY), 255, 255, 0, False, 200, type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X-1, newSpecial[0].Y-1, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X, newSpecial[0].Y-1, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X+1, newSpecial[0].Y-1, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))
			newSpecial.append(def_clsDot(newSpecial[0].X, newSpecial[0].Y-2, newSpecial[0].r, newSpecial[0].g, newSpecial[0].b, newSpecial[0].EstFatal, newSpecial[0].Points, newSpecial[0].type, "", True))

		if type == "mur":
			#Mur gauche/droit
			random1 = random.randint(3,MatrixMaxY-1)
			random2 = random.randint(3,MatrixMaxY-1)
			
			for epaisseur in range(1,3):
				for i in range(1, MatrixMaxY+1):
					if (i>= random1-1 and i<= random1+1) or (i>= random2-1 and i<= random2+1):
						i=i #skipit
					else:	
						newSpecial.append(def_clsDot(epaisseur, i, 128, 0, 0, False, 5, type, "", True))
						newSpecial.append(def_clsDot(MatrixMaxX+1-epaisseur, i, 128, 0, 0, False, 5, type, "", True))
						
			#Mur top/down
			
			random1 = random.randint(3,MatrixMaxX-1)
			random2 = random.randint(3,MatrixMaxX-1)
			
			for epaisseur in range(1,3):
				for i in range(1, MatrixMaxX+1):
					if (i>= random1-1 and i<= random1+1) or (i>= random2-1 and i<= random2+1):
						i=i #skipit
					else:	
						newSpecial.append(def_clsDot(i, epaisseur, 128, 0, 0, False, 5, type, "", True))
						newSpecial.append(def_clsDot(i, MatrixMaxY+1-epaisseur, 128, 0, 0, False, 5, type, "", True))
					
			found = 1
			print "mur done"

		if type != "mur":
			for dotSpecial in newSpecial:
				for dot in AllDots:
					#Ne peux pas se mettre a la meme place que quelque chose d'autre
					if dot.X == dotSpecial.X and dot.Y == dotSpecial.Y:
						found=0
						BreakForce=True
						break
					#ne peux pas etre dans le pourtour pour les murs
					if dotSpecial.X<=2 or dotSpecial.X >= MatrixMaxX-1 or dotSpecial.Y<=2 or dotSpecial.Y>=MatrixMaxY-1:
						found=0
						BreakForce=True
						break
					else: 
						found = 1
				if BreakForce==True:
					break
				
			#if found==0:
				#print "repige"
			
	return newSpecial
	
def MoveOnce():

	global Snake
	global gaterie
	global Vitesse
	global GameOver
	
	if GameOver == False:	
		Snake = MoveSnake()
	
	if GameOver == False:
		SnakeGaterie = copy.copy(Snake)
		
		for i in range(0, len(gaterie)):
			SnakeGaterie.append(gaterie[i])
			
		for j in range(0, len(obstacles)):
			for i in range(0, len(obstacles[j])):
				SnakeGaterie.append(obstacles[j][i])
			
		for j in range(0, len(etoiles)):
			for i in range(0, len(etoiles[j])):
				SnakeGaterie.append(etoiles[j][i])
				
		for i in range(0, len(Murs)):
			SnakeGaterie.append(Murs[i])
			
		for i in range(0, len(Tirs)):
			SnakeGaterie.append(Tirs[i])
	
		gLightMatrix.lightUpDots(SnakeGaterie, Vitesse)
	
def key(event):
	
	global Sens
	global Snake
	global Shoot
	NewSens = ""
	bFound = True
	
	#print str(event.keysym)
	#print "pressed", repr(event.char)
	
	if event.keysym=="Left":
		NewSens = "gauche"
	elif event.keysym=="Up":
		NewSens = "haut"
	elif event.keysym=="Right":
		NewSens = "droite"
	elif event.keysym=="Down":
		NewSens = "bas"
	elif event.char == " ":
		Shoot=1
		NewSens = Sens
		#print "bang bang"
	else:
		bFound = False
		#Nothing
		
		
	#Verification que le nouveau sens ne rentre pas dans le 2eme point...donc sur lui-meme
	if Snake != []:
		tete = copy.copy(Snake[0])
	
		#Bouge la tete
		if NewSens == "droite":
			tete.X += 1
		elif NewSens == "gauche":
			tete.X -= 1
		elif NewSens == "bas":
			tete.Y += 1
		elif NewSens == "haut":
			tete.Y -= 1
	
		#Check si trouve la gaterie...si oui...alors devient plus grand sans deplacer le corps
		if (tete.X == Snake[1].X and tete.Y == Snake[1].Y):
			#On recule...pas suppose
			Sens = Sens
		else:
			if bFound:	
				#print "nouveau sens : " + Sens
				Sens = NewSens

def callback(event):
	root.focus_set()
	#print "clicked at", event.x, event.y

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.AvecMurValue = tk.IntVar()
		#self.frame = self.Frame(self, width=100, height=100)
		self.bind_all("<Key>", key)
		self.bind_all("<Button-1>", callback)
		
		self.pack()
		self.createWidgets()

	def createWidgets(self):

		self.buttonEasy = tk.Button(self, text = 'Easy', command = self.EasyGame)
		self.buttonEasy.pack(pady=20, padx = 20)
		
		self.buttonMedium = tk.Button(self, text = 'Medium', command = self.MediumGame)
		self.buttonMedium.pack(pady=10, padx = 20)
		
		self.buttonMedium = tk.Button(self, text = 'Hard', command = self.HardGame)
		self.buttonMedium.pack(pady=10, padx = 20)
		
		self.buttonMedium = tk.Button(self, text = 'Insane', command = self.InsaneGame)
		self.buttonMedium.pack(pady=10, padx = 20)
		
		self.AvecMur = tk.Checkbutton(self, text = "Avec mur ?", variable = self.AvecMurValue, command = self.GetAvecMurValue)
		self.AvecMur.pack(pady=10, padx = 20)

		self.QUIT = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
		self.QUIT.pack(pady=10, padx = 20)
		
	def GetAvecMurValue(self):
		global Mur
		
		Mur = self.AvecMurValue.get()
		
	def SetupSnake(self):
		global Snake
		global GameOver 
		global Sens
		global gaterie
		global obstacles
		global Score
		global ModeInvincible
		global Mur
		global Murs
		global Tirs
		
		Mur = 0
		Murs = []
		Tirs = []
		Score = 0
		GameOver = False
		ModeInvincible = False

		Snake = []
		
		for i in range(25,0, -1):
			Snake.append(def_clsDot(i,4, 0, 0, 255, True, 200, "snake", "", True))

		Sens = "droite"
		
		gaterie = []
		for dot in CreationSpecial("gaterie"):
			#dot.PrintCoord()
			gaterie.append(dot)
			
		#print len(gaterie)
		
		obstacles = []
		
	def EasyGame(self):
		global Vitesse 
		global ScoreMult
		
		self.SetupSnake()
		Vitesse = 0.25
		ScoreMult = 1
		self.onUpdate()
	
	def MediumGame(self):
		global Vitesse 
		global ScoreMult
		self.SetupSnake()
		Vitesse = 0.1
		ScoreMult = 2
		self.onUpdate()
		
	def HardGame(self):
		global Vitesse 
		global ScoreMult
		self.SetupSnake()
		Vitesse = 0.05
		ScoreMult = 4
		self.onUpdate()
		
	def InsaneGame(self):
		global Vitesse 
		global ScoreMult
		self.SetupSnake()
		Vitesse = 0.02
		ScoreMult = 10
		self.onUpdate()

	def onUpdate(self):
		
		global Vitesse
		global gaterie
		global obstacles
		global Snake
		global ModeInvincible
		global DebutInvincible
		global Mur
		global DebutMur
		global Murs
		#print "onUpdate"
		
		# schedule timer to call myself after 1 second
		if GameOver == False:
			MoveOnce()
		if GameOver == False:
			#time.sleep(int(Vitesse*1000))
			#self.onUpdate()
			self.after(int(Vitesse*1000), self.onUpdate)
			
		#Cree une gaterie supplementaire de temps en temps
		if len(gaterie)<=10:
			tirage = random.randint(0,1000)
			if tirage<10:
				for dot in CreationSpecial("gaterie"):
					gaterie.append(dot)
				
		#Cree un obstacle supplementaire de temps en temps
		if len(obstacles)<=8:
			tirage = random.randint(0,1000)
			if tirage<4:
				obstacles.append(CreationSpecial("obstacle"))
					
		#Cree une etoile supplementaire de temps en temps
		if len(etoiles)<=2:
			tirage = random.randint(0,1000)
			if tirage<4:
				etoiles.append(CreationSpecial("etoile"))
				
				#for j in range(0, len(etoiles)):
				#	for i in range(0, len(etoiles[j])):
				#		etoiles[j][i].PrintCoord()
						
		if Mur == 0:
			tirage = random.randint(0,1000)
			if tirage<5:
				Mur = 1
				DebutMur = time.time()
				Murs = CreationSpecial("mur")
				
		if Mur == 1:
			TempsActuel = time.time()
			
			if (TempsActuel - DebutMur >= 0) and (TempsActuel - DebutMur < 3): #Warning
				if Murs[0].g == 128:
					for dot in Murs:
						dot.r = 128
						dot.g = 0
						dot.b = 0
				else:
					for dot in Murs:
						dot.r = 128
						dot.g = 128
						dot.b = 128
			elif TempsActuel - DebutMur >= 3 and TempsActuel - DebutMur < 20: #arme les murs
				for dot in Murs:
					dot.r = 128
					dot.g = 0
					dot.b = 0
				
				if Murs[0].EstFatal==False:
					for dot in Murs:
						dot.EstFatal=True
			elif TempsActuel - DebutMur >= 20: #Revert
				print "mur is over"
				Mur=0
				Murs=[]
						
		#Met le serpent multicolor pendant qu'il est invincible
		if ModeInvincible == True:
			TempsActuel = time.time()
			
			#print str(TempsActuel - DebutInvincible)
			if (TempsActuel - DebutInvincible >= 7) and (TempsActuel - DebutInvincible < 11): #Warning
				if Snake[0].r == 255:
					for dot in Snake:
						dot.r = 0
						dot.g = 0
						dot.b = 255
				else:
					for dot in Snake:
						dot.r = 255
						dot.g = 255
						dot.b = 255
			elif TempsActuel - DebutInvincible >= 11: #Revert
				ModeInvincible=False
				for dot in Snake:
					dot.r = 0
					dot.g = 0
					dot.b = 255
			else:	
				for dot in Snake:
					dot.r = random.randint(0,255)
					dot.g = random.randint(0,255)
					dot.b = random.randint(0,255)

# Rows and chain length are both required parameters:
device = Adafruit_RGBmatrix(32, 1)

gLightMatrix = def_clsLightMatrix(device)
gRand = def_clsRandom()
Score = 0
ScoreMult = 1
ModeInvincible = False
DebutInvincible = time.time()
DebutMur = time.time()

gaterie=[]
Snake=[]
obstacles=[]
etoiles=[]
Murs=[]
Tirs = []

Shoot = 0
Mur = 0 # 0 = Mur est absent, 1 = Mur est present
FrappeSnake = 1 # 0 = On se frappe pas dessus, 1 = On explose si le serpent tourne sur lui-meme
Vitesse = 0.2 #Temps entre chaque move
Sens = "droite" #bas, haut, gauche, droite
MatrixMaxX = 32
MatrixMaxY = 32
GameOver = True

root = tk.Tk()
app = Application(master=root)
root.mainloop()
