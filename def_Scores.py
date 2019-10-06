import numpy as np

class def_Scores(object):
	def __init__(self, newScore):
		
		count = 1
		self.newScore = newScore
		self.FinalCount=1
		data = np.genfromtxt("highscore",delimiter="\n")
		
		f2 = open('highscore', 'w')

		newScoreAdded=False

		for score in data:
			#print str(score)

			if newScoreAdded==True or newScore < int(score):
				f2.write(str(int(score)) + '\n')
				count+=1
			else:
				f2.write(str(newScore) + '\n')
				self.FinalCount = count
				f2.write(str(int(score)) + '\n')
				count+=1
				newScoreAdded=True
				
		if newScoreAdded==False:
			f2.write(str(newScore) + '\n')
			self.FinalCount = count
		
		