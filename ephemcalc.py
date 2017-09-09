import astrology
import chart
import planets
import util


class EphemCalc:

	PLANET = 0
	DAY = 1
#	HOUR = 2

	def __init__(self, year, opts):
		self.year = year
		self.flags = astrology.SEFLG_SPEED+astrology.SEFLG_SWIEPH
		self.posArr = []

		self.calc(opts)


	def calc(self, opts):
		ayanamsha = 0.0
		if opts.ayanamsha != 0:
			astrology.swe_set_sid_mode(opts.ayanamsha-1, 0, 0)
			tim = chart.Time(self.year, 1, 1, 0, 0, 0, False, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
			ayanamsha = astrology.swe_get_ayanamsa_ut(tim.jd)

		plsnum = 7
		if opts.transcendental[chart.Chart.TRANSURANUS]:
			plsnum += 1
		if opts.transcendental[chart.Chart.TRANSNEPTUNE]:
			plsnum += 1
		if opts.transcendental[chart.Chart.TRANSPLUTO]:
			plsnum += 1

		#calculating one per day (per hour would be too slow)
		for i in range(plsnum):
			if i != 1:#moon excepted
				y = self.year; m = 1; d = 1
				ar = []
				for num in range(365):
					time = chart.Time(y, m, d, 0, 0, 0, False, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, None, False)
					pl = planets.Planet(time.jd, i, self.flags)
					pos = pl.data[planets.Planet.LONG]
					if opts.ayanamsha != 0:
						pos = util.normalize(pos-ayanamsha)

					ar.append(pos)

					y, m, d = util.incrDay(y, m, d)

				self.posArr.append(ar)



