import astrology
import chart
import util


class Profections:
	K = 12.17473968 # 365.2421904/30 days/degree

	def __init__(self, radix, y, m, d, t, cnt=0): #t is in GMT
		jdbirth = astrology.swe_julday(y, m, d, t, astrology.SE_GREG_CAL)
		jd = jdbirth+cnt*365.2421904

		#Find the difference in Julian days between today and the birth day. Say it Djd
		diffjd = jd-radix.time.jd

		#Find how many  degrees you must rotate the whole natal chart.
		rotdeg = diffjd/12.17474

		#Find the Profection cycle.
		profcyc = rotdeg/360.0

		#Determine the number of integer cycles.
		intcyc = int(profcyc)

		#Compute the number of degrees included in the integer cycles.
		degintcyc = intcyc*360.0

		#Compute the number of degrees (< 360), the true profectional movement
		self.offs = util.normalize(rotdeg-degintcyc)



