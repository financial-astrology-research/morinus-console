import astrology
import swisseph


class Asteroid:
	"""Data of an Asteroid"""

	def __init__(self, tjd_ut, aId, flag):
		self.aId = aId

		self.data = swisseph.calc_ut(tjd_ut, aId, flag)[0]
		self.dataEqu = swisseph.calc_ut(tjd_ut, aId, flag+astrology.SEFLG_EQUATORIAL)[0]
		self.name = swisseph.get_planet_name(aId)

class Asteroids:
	"""Calculates the positions of the asteroids"""

	ids = [astrology.SE_CERES, astrology.SE_CHIRON, astrology.SE_JUNO, astrology.SE_PALLAS, astrology.SE_PHOLUS, astrology.SE_VESTA]

	def __init__(self, tjd_ut, flag):
		self.asteroids = []

		for i in Asteroids.ids:
			self.asteroids.append(Asteroid(tjd_ut, i, flag))
