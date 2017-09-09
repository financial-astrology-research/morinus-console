from datetime import datetime, timedelta
import mtexts

# ##################################
# Roberto V 7.3.0
# *** SOME *** texts txtsxxx -> txts
# ##################################

#Csaba's code ("Object orientalized" by me)
class Firdaria:
	'''Firdaria (3 types): 1.Diurnal chart, 2.Nocturnal(Al Biruni) 3.Nocturnal(Bonatti)'''

	TIME_FORMAT="%Y.%m.%d"

	#birthyear, birthmonth, birthday
	def __init__(self, by, bm, bd, opts, isdaily):
		self.by = by
		self.bm = bm
		self.bd = bd

		self.startdate = datetime(self.by, self.bm, self.bd)
		self.isdaily = isdaily
		self.options = opts

		self.dailyplanetaryyears = [(3, 10), (4, 8), (5, 13), (6, 9), (0, 11), (1, 12), (2, 7), (7, 3), (8, 2)]
		self.nightlyplanetaryyearsalbiruni = [(6, 9), (0, 11), (1, 12), (2, 7), (3, 10), (4, 8), (5, 13), (7, 3), (8, 2)]
		self.nightlyplanetaryyearsbonatti = [(6, 9), (0, 11), (1, 12), (2, 7), (7, 3), (8, 2), (3, 10), (4, 8), (5, 13)]

#		self.printFirdaria()


	def isNode(self, index):
		if self.isdaily:
			return index == 7 or index == 8
		else:
			if self.options.isfirbonatti:
				return index == 4 or index == 5
			else:
				return index == 7 or index == 8


	def nextIndex(self, index):
		index = index + 1
		if self.isdaily:
			if self.isNode(index) or index > 8:
				return 0
		else:
			if self.options.isfirbonatti:
				if self.isNode(index):
					return 6
				elif index > 8:
					return 0
			else:
				if self.isNode(index) or index > 8:
					return 0
		return index
			

	#For printFirdaria()
	def displaySubPeriods(self, planetaryyears, index, starting, ending, pltxts):
		if self.isNode(index):
			return
		subperiodstart = starting
		secs = (ending - starting).total_seconds()
		for i in range(7): #planets.Planets.PLANETS_NUM?
			planet, years = planetaryyears[index]
			subperiodends = subperiodstart + timedelta(seconds = secs / 7)#planets.Planets.PLANETS_NUM?
			print("       {0:7}: {1}".format(pltxts[planet], subperiodstart.strftime(Firdaria.TIME_FORMAT)))
			subperiodstart = subperiodends
			index = self.nextIndex(index)


	def printFirdaria(self):
		pltxts = (mtexts.txts["Saturn"], mtexts.txts["Jupiter"], mtexts.txts["Mars"], mtexts.txts["Sun"], mtexts.txts["Venus"], mtexts.txts["Mercury"], mtexts.txts["Moon"], mtexts.txts["ANode"], mtexts.txts["DNode"])

		if self.isdaily:
			planetaryyears = self.dailyplanetaryyears
		else:
			if self.options.isfirbonatti:
				planetaryyears = self.nightlyplanetaryyearsbonatti
			else:
				planetaryyears = self.nightlyplanetaryyearsalbiruni

		starting = self.startdate
		for index in range(len(planetaryyears) + 3):
			aindex = index % len(planetaryyears)
			planet, years = planetaryyears[aindex]
			ending = datetime(starting.year + years, starting.month, starting.day)
			print("{0}: {1} - {2} ({3} years)".format(pltxts[planet], starting.strftime(Firdaria.TIME_FORMAT), (ending + timedelta(days=-1)).strftime(Firdaria.TIME_FORMAT), years))
			self.displaySubPeriods(planetaryyears, aindex, starting, ending, pltxts)
			print("")
			starting = ending



