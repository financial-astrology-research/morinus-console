import math
import astrology
import chart#Time
import planets
import util


class SecMotion:
	"""Calculates the secondary motions of a planet for PDs(arc)"""

	ST2UTCONV = 0.997269566

	def __init__(self, rtime, rplace, pId, arc, lat, ascmc2, topo):
		direct = True
		if arc < 0.0:
			arc *= -1
			direct = False
		if arc > 180.0:
			arc = 360.0-arc 
			direct = not direct

		if not direct and arc > 0.0:
			arc *= -1

 		flag = astrology.SEFLG_SWIEPH+astrology.SEFLG_SPEED
		if topo:
			flag += astrology.SEFLG_TOPOCTR

		#calc new time
		rate = arc/15.0
		ut = rate*SecMotion.ST2UTCONV
		newtime = rtime.time+ut
		year, month, day = rtime.year, rtime.month, rtime.day

		#check overflow
		if newtime >= chart.Time.HOURSPERDAY:
			newtime -= chart.Time.HOURSPERDAY
			year, month, day = util.incrDay(year, month, day)
		elif newtime < 0.0:
			newtime += chart.Time.HOURSPERDAY
			year, month, day = util.decrDay(year, month, day)

		calflag = astrology.SE_GREG_CAL
		if rtime.cal == chart.Time.JULIAN:
			calflag = astrology.SE_JUL_CAL
		tjd_ut = astrology.swe_julday(year, month, day, newtime, calflag)

		#self.planet contains the new position of the planet(it proceeded on its way during the PD(arc))
		self.planet = planets.Planet(tjd_ut, pId, flag, lat, ascmc2)

		




