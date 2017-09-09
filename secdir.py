import astrology
import chart
import mtexts
import util


class SecDir:
	def __init__(self, chrt, age, direct, soltime):
		self.chart = chrt
		self.age = age
		self.direct = direct
		self.soltime = soltime

	
	def compute(self):
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		hour = self.chart.time.hour
		minute = self.chart.time.minute
		second = self.chart.time.second

		hr = 0.0

		#GMT to LocalMean
		t = (self.chart.place.deglon+self.chart.place.minlon/60.0)*4 #long * 4min
		meantime = 0.0
		if self.chart.place.east:
			meantime = self.chart.time.time+t/60.0
		else:
			meantime = self.chart.time.time-t/60.0

		#check over/underflow
		HOURSPERDAY = 24.0
		if meantime >= HOURSPERDAY:
			meantime -= HOURSPERDAY
			y, m, d = util.incrDay(y, m, d)
		elif meantime < 0.0:
			meantime += HOURSPERDAY
			y, m, d = util.decrDay(y, m, d)

		if self.soltime:
			calflag = astrology.SE_GREG_CAL
			if self.chart.time.cal == chart.Time.JULIAN:
				calflag = astrology.SE_JUL_CAL
			yt = y
			if self.chart.time.bc:
				yt = -y
			jdmean = astrology.swe_julday(yt, m, d, meantime, calflag)

			#Get jdapp
			ret, te, serr = astrology.swe_time_equ(jdmean)
			jdapp = jdmean-te
			y, m, d, hr = astrology.swe_revjul(jdapp, calflag)
			hour,minute,second = util.decToDeg(hr)
#			print '%d:%02d:%02d' % (hour,minute,second)
		else:
			hour,minute,second = util.decToDeg(meantime)

		for i in range(self.age):
			if self.direct:
				y, m, d = util.incrDay(y, m, d)
			else:	
				y, m, d = util.decrDay(y, m, d)

		if self.soltime:
			#Back to meantime on the last day
			yt = y
			if self.chart.time.bc:
				yt = -y
			calflag = astrology.SE_GREG_CAL
			if self.chart.time.cal == chart.Time.JULIAN:
				calflag = astrology.SE_JUL_CAL
			jdapp = astrology.swe_julday(yt, m, d, hr, calflag)

			ret, te, serr = astrology.swe_time_equ(jdapp)
			jdmean = jdapp+te
			y, m, d, hr = astrology.swe_revjul(jdmean, calflag)
			hour,minute,second = util.decToDeg(hr)
#			print '%d:%02d:%02d' % (hour,minute,second)

		return y, m, d, hour, minute, second






