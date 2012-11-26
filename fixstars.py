import astrology

class FixStars:
	"""Calculates the positions of the fixstars"""

	NAME = 0
	NOMNAME = 1
	LON = 2
	LAT = 3
	RA = 4
	DECL = 5

	def __init__(self, tjd_ut, flag, names, obl):
		
		self.data = []

		i = 0
		for k in names.iterkeys():
			self.data.append(['', '', 0.0, 0.0, 0.0, 0.0])
			ret, name, dat, serr = astrology.swe_fixstar_ut(','+k, tjd_ut, flag)

			nam = name[0].strip()
			nomnam = ''
			DELIMITER = ','
			if nam.find(DELIMITER) != -1:
				snam = nam.split(DELIMITER)
				nam = snam[0].strip()
				nomnam = snam[1].strip()

			self.data[i][FixStars.NAME] = nam
			self.data[i][FixStars.NOMNAME] = nomnam
			self.data[i][FixStars.LON] = dat[0]
			self.data[i][FixStars.LAT] = dat[1]
			ra, decl, dist = astrology.swe_cotrans(dat[0], dat[1], 1.0, -obl)
			self.data[i][FixStars.RA] = ra
			self.data[i][FixStars.DECL] = decl

			i += 1

		self.sort()


	def sort(self):
		num = len(self.data)
		self.mixed = []
			
		for i in range(num):
			self.mixed.append(i)

		for i in range(num):
			for j in range(num-1):
				if (self.data[j][FixStars.LON] > self.data[j+1][FixStars.LON]):
					tmp = self.data[j][:]
					self.data[j] = self.data[j+1][:]
					self.data[j+1] = tmp[:]
					tmp = self.mixed[j]
					self.mixed[j] = self.mixed[j+1]
					self.mixed[j+1] = tmp





