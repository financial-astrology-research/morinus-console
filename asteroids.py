import astrology


class Asteroid:
	"""Data of an Asteroid"""

	def __init__(self, tjd_ut, aId, flag):
		self.aId = aId

		rflag, dat, serr = astrology.swe_calc_ut(tjd_ut, aId, flag)
		rflag, datEqu, serr = astrology.swe_calc_ut(tjd_ut, aId, flag+astrology.SEFLG_EQUATORIAL)
		self.data = (dat[0], dat[1], datEqu[0], datEqu[1])

		self.name = astrology.swe_get_planet_name(aId)


class Asteroids:
	"""Calculates the positions of the asteroids"""

	ids = [astrology.SE_CERES, astrology.SE_CHIRON, astrology.SE_JUNO, astrology.SE_PALLAS, astrology.SE_PHOLUS, astrology.SE_VESTA]

	def __init__(self, tjd_ut, flag):
		self.asteroids = []
		
		for i in Asteroids.ids:
			self.asteroids.append(Asteroid(tjd_ut, i, flag))

	
	

