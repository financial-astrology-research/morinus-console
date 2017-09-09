import planets
import math
import util


class Mid:
	def __init__(self, p1, p2, m, lat):
		self.p1 = p1
		self.p2 = p2
		self.m = m
		self.lat = lat


class MidPoints:
	"""Computes Midpoints"""

	def __init__(self, pls):
		self.pls = pls
		self.mids = []
		self.midslat = []

		self.countMidPoints()
		self.countMidPointsWithLatitude()
	
#		self.printMidPoints(self.midslat)


	def countMidPoints(self):	
		for i in range(planets.Planets.PLANETS_NUM-2):#Nodes are excluded
			for j in range(i+1, planets.Planets.PLANETS_NUM):
				p1 = self.pls.planets[i].data[planets.Planet.LONG]
				p2 = self.pls.planets[j].data[planets.Planet.LONG]
				d = math.fabs(p1-p2)
				m = 0.0
				if d <= 180.0:
					if p1 < p2:
						m = p1+d/2.0
					else:
						m = p2+d/2.0
				else:
					d = 360.0-d
					if p1 < p2:
						m = p2+d/2.0
					else:
						m = p1+d/2.0
					if m >= 360.0:
						m -= 360.0

				m = util.normalize(m)

				self.mids.append(Mid(i, j, m, 0.0))


	def countMidPointsWithLatitude(self):
		'''According to Ruediger Plantiko'''

		for i in range(planets.Planets.PLANETS_NUM-2):#Nodes are excluded
			for j in range(i+1, planets.Planets.PLANETS_NUM):
				p1 = self.pls.planets[i].data[planets.Planet.LONG]
				l1 = self.pls.planets[i].data[planets.Planet.LAT]
				p2 = self.pls.planets[j].data[planets.Planet.LONG]
				l2 = self.pls.planets[j].data[planets.Planet.LAT]
				dist = math.fabs(p2-p1)
				if dist >= 180.0:
					dist = 360.0-dist

				rl1 = math.radians(l1)
				rl2 = math.radians(l2)
				rdist = math.radians(dist)

				val = math.sin(rl1)*math.sin(rl2)+math.cos(rl1)*math.cos(rl2)*math.cos(rdist)
				if math.fabs(val) <= 1.0:
					d = math.acos(val)
					res = ((math.tan(rl2)*math.cos(rl1))/math.sin(rdist))-math.sin(rl1)/math.tan(rdist)
					A = 1.0
					if res != 0.0:
						A = math.atan(1.0/res)#1.0 is ok!?
						if A < 0.0:
							A += math.pi

					#latitude of the midpoint
					lat = math.degrees(math.asin(math.cos(d/2.0)*math.sin(rl1)+math.sin(d/2.0)*math.cos(rl1)*math.cos(A)))
					#long
					res = math.cos(rl1)*(1.0/math.tan(d/2.0))/math.sin(A)-math.sin(rl1)/math.tan(A)
					dd = 0.0
					if res != 0.0:
						dd = math.fabs(math.degrees(math.atan(1.0/res)))#

					lon = 0.0
					d = math.fabs(p1-p2)
					if d <= 180.0:
						if p1 < p2:
							lon = p1+dd
						else:
							lon = p2+dd
					else:
						if p1 < p2:
							lon = p2+dd
						else:
							lon = p1+dd
						if lon >= 360.0:
							lon -= 360.0

					self.midslat.append(Mid(i, j, lon, lat))
				else:
					self.midslat.append(Mid(i, j, 0.0, 0.0))


	def printMidPoints(self, mids):
		pls = ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'AscNode', 'DescNode')

		for x in mids:
			d,m,s = util.decToDeg(x.m)
			dl,ml,sl = util.decToDeg(x.lat)
			print "%s-%s: %d %d'%d\"  %d %d'%d\"" % (pls[x.p1], pls[x.p2], d,m,s, dl, ml, sl)



