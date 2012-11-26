import math
import astrology
import houses
import planets
import placspec
import util


class MundaneFortune:
	'''Computes mundane Lot-of-Fortune (acc. to Placidus)'''
	LON = 0
	LAT = 1
	RA = 2
	DECL = 3

	def __init__(self, ascmc2, pls, obl, placelat):
		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		aoasc = ramc+90.0
		if aoasc >= 360.0:
			aoasc -= 360.0
		ramoon = pls.planets[astrology.SE_MOON].dataEqu[planets.Planet.RAEQU]
		rasun = pls.planets[astrology.SE_SUN].dataEqu[planets.Planet.RAEQU]
		adsun = 0.0
		self.mLoFvalid = False
		val = math.tan(math.radians(placelat))*math.tan(math.radians(pls.planets[astrology.SE_SUN].dataEqu[planets.Planet.DECLEQU]))
		if math.fabs(val) <= 1.0:
			adsun = math.degrees(math.asin(val))
			self.mLoFvalid = True
		aosun = rasun-adsun
		if aosun < 0.0:
			aosun += 360.0
		raMLoF = aoasc+ramoon-aosun
		raMLoF = util.normalize(raMLoF)
		declMLoF = pls.planets[astrology.SE_MOON].dataEqu[planets.Planet.DECLEQU]
		lonMLoF, latMLoF, dist = astrology.swe_cotrans(raMLoF, declMLoF, 1.0, obl)

		self.mfortune = (lonMLoF, latMLoF, raMLoF, declMLoF)

		self.speculum = placspec.PlacidianSpeculum(placelat, ascmc2, lonMLoF, latMLoF, raMLoF, declMLoF)

		self.valid = self.mLoFvalid and self.speculum.valid





