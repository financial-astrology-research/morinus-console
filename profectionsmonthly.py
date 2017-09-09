import astrology
import chart
import util
import mtexts


class ProfectionsMonthly:
	def __init__(self, pchrts, step12, rownum):
		self.dates = []

		y = pchrts[0][1]+rownum
		m = pchrts[0][2]
		d = pchrts[0][3]
		if (not util.checkDate(y, m, d)):
			y, m, d = util.incrDay(y, m, d)

		#calc
		dat = (y, m, d)
		self.dates.append(dat)

		idx = 12
		mon = 30.4368492
		if not step12:
			idx = 13
			mon = 28.0955531

		calflag = astrology.SE_GREG_CAL
		if pchrts[0][0].time.cal == chart.Time.JULIAN:
			calflag = astrology.SE_JUL_CAL
		jdval = astrology.swe_julday(y, m, d, pchrts[0][0].time.time, calflag)
		for i in range(idx-1):
			jdval += mon
			jy, jm, jd, jh = astrology.swe_revjul(jdval, calflag)
#			d, m, s = util.decToDeg(jh)
			dat = (jy, jm, jd)
			self.dates.append(dat)



