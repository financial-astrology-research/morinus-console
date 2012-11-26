import astrology
import mtexts
import transits
import util


class SunTransits:
	def __init__(self):
		self.t = [0, 0, 0, 0, 0, 0]


	def compute(self, by, bm, bd, chrt, trlon):
		for i in range(13):
			trans = transits.Transits()
			trans.month(by, bm, chrt, astrology.SE_SUN, trlon)

			if len(trans.transits) > 0:
				if not (i == 0 and bd > trans.transits[0].day):
					self.createTransit(by, bm, trans)
					return True

			by, bm = self.incrMonth(by, bm)

		return False


	def decrMonth(self, year, month):
		if month != 1:
			month -= 1
		else:
			month = 12
			year -= 1
		
		return year, month


	def incrMonth(self, year, month):
		if month != 12:
			month += 1
		else:
			month = 1
			year += 1
		
		return year, month


	def createTransit(self, year, month, trans):
		self.t[0] = year
		self.t[1] = month
		self.t[2] = trans.transits[0].day
		h, m, s = util.decToDeg(trans.transits[0].time)
		self.t[3] = h
		self.t[4] = m
		self.t[5] = s



