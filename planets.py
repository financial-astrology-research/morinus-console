import math
import astrology
import houses
import util


class Planet:
	"""Data of a Planet"""

	#Speculum
	#Common
	LONG = 0
	LAT = 1
	RA = 2
	DECL = 3

	#Placidus
	ADLAT = 4
	SA = 5
	MD = 6
	HD = 7
	TH = 8
	HOD = 9
	PMP = 10
	ADPH = 11
	POH = 12 
	AODO = 13

	#Regiomontanian/Campanian
	RMD = 4
	RHD = 5
	ZD = 6
	POLE = 7
	Q = 8
	W = 9
	CMP = 10
	RMP = 11

	#data[x]
	DIST = 2
	SPLON = 3
	SPLAT = 4
	SPDIST = 5

	#dataEqu
	RAEQU = 0
	DECLEQU = 1
	DISTEQU = 2
	SPRAEQU = 3
	SPDECLEQU = 4
	SPDISTEQU = 5

	def __init__(self, tjd_ut, pId, flag, lat = None, ascmc2 = None, raequasc = None, ecl = None, equ = None, nolat = False, obl = 0.0):
		self.pId = pId

		self.speculums = None

		if (ecl == None):
			rflag, self.data, serr = astrology.swe_calc_ut(tjd_ut, pId, flag)
			rflag, self.dataEqu, serr = astrology.swe_calc_ut(tjd_ut, pId, flag+astrology.SEFLG_EQUATORIAL)

			# data[0] : longitude
			# data[1] : latitude
			# data[2] : distance
			# data[3] : speed in long
			# data[4] : speed in lat
			# data[5] : speed in dist

			# if rflag < 0:
			#	print 'Error: %s' % serr

			self.name = astrology.swe_get_planet_name(pId)
		else:
			self.data = tuple(ecl)
			self.dataEqu = tuple(equ)
			self.name = 'DescNode'

		if nolat:
			self.data = (self.data[Planet.LONG], 0.0, self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
			ra, decl, dist = astrology.swe_cotrans(self.data[Planet.LONG], 0.0, 1.0, -obl)
			self.dataEqu = (ra, decl, self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])

		if lat != None:
			#placspec.py and regiospec should be used instead, remove these!
			self.speculums = []
			self.computePlacidianSpeculum(lat, ascmc2)
			self.computeRegiomontanSpeculum(lat, ascmc2, raequasc)


	def computePlacidianSpeculum(self, lat, ascmc2):
		#transform
		#0-90: x = x
		#90-180: 180-x = 180-x	(before the trigon. calc. subtract x from 180.0 and at the end of the calc the result should be subtr. from 180.0)
		#180-270: x-180 = x+180	(before the trigon. calc. subtract 180.0 from x and at the end of the calc the result should be added to 180.0)
		#270-360: 360-x = 360-x

		#sin(delta) = sin(long)*sin(obl)
		#sin(ar) = ctg(obl)*tg(delta)   or tg(ar) = cos(obl)*/ctg(long)
		#cos(war) = cos(long)*cos(beta)/cos(delta)

		#sin(A.D.)(FI or lat)[ascensio-differentia] = tg(FI)*tg(delta)
		#SemiArcus
			#dsa = 90.0+A.D.
			#nsa = 90.0-A.D.
		#MeridianDistance:
			#Diurnal planet: |wRA-ARMC|   (wahre = real)
			#Nocturnal planet : |wRA-ARIC|

		#HD(HorizonDistance)

		#TH(TemporalHour) = SA/6   semiarcus is either diurnal or nocturnal dependig on the planet

		#HOD(HourlyDistance)=MD/TH

		#PMP (Placidus Mundane Position)
			#if QuadrantI:		pmp = 90.0-90.0*MD/SA
			#if QuadrantII:		pmp = 90.0+90.0*MD/SA
			#if QuadrantIII:	pmp = 270.0-90.0*MD/SA
			#if QuadrantIV:		pmp = 270.0+90.0*MD/SA
		
		#A.D.(fi or poleheight) = MD*AD(FI)/SA
		#Poleheight(fi): tg(fi) = sin(AD(fi))/tg(delta)
		#A.O. D.O.:
			#AO: Eastern planet:  AO = AR-AD
			#DO: western planet:  DO = AR+AD

		#sa, adlat, md, hd, adph, ph, ao/do

		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		self.eastern = True
		if ramc > raic:
			if self.dataEqu[Planet.RAEQU] > raic and self.dataEqu[Planet.RAEQU] < ramc:
				self.eastern = False
		else:
			if (self.dataEqu[Planet.RAEQU] > raic and self.dataEqu[Planet.RAEQU] < 360.0) or (self.dataEqu[Planet.RAEQU] < ramc and self.dataEqu[Planet.RAEQU] > 0.0):
				self.eastern = False

		#adlat
		adlat = 0.0
		val = math.tan(math.radians(lat))*math.tan(math.radians(self.dataEqu[Planet.DECLEQU]))
		if math.fabs(val) <= 1.0:
			adlat = math.degrees(math.asin(val))

		#md
		med = math.fabs(ramc-self.dataEqu[Planet.RAEQU])

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(raic-self.dataEqu[Planet.RAEQU])
		if icd > 180.0:
			icd = 360.0-icd

		md = med

		#hd
		aoasc = ramc+90.0
		if aoasc >= 360.0:
			aoasc -= 360.0

		dodesc = raic+90.0
		if dodesc >= 360.0:
			dodesc -= 360.0

		aohd = self.dataEqu[Planet.RAEQU]-adlat
		hdasc = aohd-aoasc
		if hdasc < 0.0:
			hdasc *= -1
		if hdasc > 180.0:
			hdasc = 360.0-hdasc 

		dohd = self.dataEqu[Planet.RAEQU]+adlat
		hddesc = dohd-dodesc
		if hddesc < 0.0:
			hddesc *= -1
		if hddesc > 180.0:
			hddesc = 360.0-hddesc 

		self.hd = hdasc
		if hddesc < hdasc:
			self.hd = hddesc
			self.hd *= -1

		#sa (southern hemisphere!?)
		dsa = 90.0+adlat
		nsa = 90.0-adlat

		self.abovehorizon = True
		if med > dsa:
			self.abovehorizon = False

		sa = dsa
		if not self.abovehorizon:
			sa = -nsa #nocturnal if negative
			md = icd
			md *= -1

		#TH(TemporalHour)
		th = sa/6.0

		#HOD(HourlyDistance)
		hod = 0.0
		if th != 0.0:
			hod = md/math.fabs(th)

		#pmp
		pmp = 0.0
		tmd = md
		if tmd < 0.0:
			tmd *= -1

		pmpsa = sa
		if pmpsa < 0.0:
			pmpsa *= -1

		if not self.abovehorizon and self.eastern:
			pmp = 90.0-90.0*(tmd/pmpsa)
		elif not self.abovehorizon and not self.eastern:
			pmp = 90.0+90.0*(tmd/pmpsa)
		elif self.abovehorizon and not self.eastern:
			pmp = 270.0-90.0*(tmd/pmpsa)
		elif self.abovehorizon and self.eastern:
			pmp = 270.0+90.0*(tmd/pmpsa)

		#adphi
		tval = math.fabs(sa)
		adphi = 0.0
		if tval != 0.0:
			adphi = math.fabs(tmd)*adlat/tval

		#phi
		tval = math.tan(math.radians(self.dataEqu[Planet.DECLEQU]))
		phi = 0.0
		if tval != 0.0:
			phi = math.degrees(math.atan(math.sin(math.radians(adphi))/tval))

		#ao/do (southern hemisphere!?)
		if self.eastern:
			ao = self.dataEqu[Planet.RAEQU]-adphi
		else:
			ao = self.dataEqu[Planet.RAEQU]+adphi
			ao *= -1 #do if negative

		self.speculums.append((self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], adlat, sa, md, self.hd, th, hod, pmp, adphi, phi, ao))


	def computeRegiomontanSpeculum(self, lat, ascmc2, raequasc):
		#transform
		#0-90: x = x
		#90-180: 180-x = 180-x	(before the trigon. calc. subtract x from 180.0 and at the end of the calc the result should be subtr. from 180.0)
		#180-270: x-180 = x+180	(before the trigon. calc. subtract 180.0 from x and at the end of the calc the result should be added to 180.0)
		#270-360: 360-x = 360-x

		#sin(delta) = sin(long)*sin(obl)
		#sin(ar) = ctg(obl)*tg(delta)   or tg(ar) = cos(obl)*/ctg(long)
		#cos(war) = cos(long)*cos(beta)/cos(delta)

		#zd
			#if md==90:
				#zd=90-arctan(sin(abs(FI))*tan(delta))
				#if planet is in quad I or II => zd from nadir
				#else from zenith
			#elif md<90:
				#A=arctan(cos(FI)*tan(MD))
				#B=arctan(tan(abs(FI))*cos(MD))

				#if (delta < 0 and FI < 0) or (delta >= 0 and FI >= 0):
					#if md is umd:
						#C=B-abs(delta)
					#else:
						#C=B+abs(delta)
				#elif (delta < 0 and FI > 0) or (delta > 0 and FI < 0):
					#if md is umd:
						#C=B+abs(delta)
					#else:
						#C=B-abs(delta)

				#F=arctan(sin(abs(FI))*sin(MD)*tan(C)) #C and F can be negative
				#zd=A+F

				#if md is umd => zd from zenith
				#else from nadir
		#pole
			#pole=arcsin(sin(FI)*sin(zd))
		#Q
			#Q=arcsin(tan(delta)*tan(pole))
		#W
			#if planet is in quad I or IV => W = RA-Q
			#else W = RA+Q

		#CMP
		#if eastern:
			#if zd measured from the zenith:
				#CMP=270+zd
			#else:
				#CMP=90-zd
		#else:
			#if zd measured from the zenith:
				#CMP=270-zd
			#else:
				#CMP=90+zd
		#RMP
		#W-RA(EquatorialAsc) [normalize]
			
		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		#md
		med = math.fabs(ramc-self.dataEqu[Planet.RAEQU])

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(raic-self.dataEqu[Planet.RAEQU])
		if icd > 180.0:
			icd = 360.0-icd

		md = med
		tablemd = med
		umd = True
		if icd < med:
			md = icd
			tablemd = icd
			tablemd *= -1
			umd = False

		#zd
		zd = self.getZD(md, lat, self.dataEqu[Planet.DECLEQU], umd)
		if zd > 90.0:
			zd = 180.0-zd
		tmpzd = zd

#		if not abovehorizon:
		if not umd: #!? or with abovehorizon!?
			zd *= -1

		#pole
		pole = 0.0
		val = math.sin(math.radians(lat))*math.sin(math.radians(tmpzd))
		if math.fabs(val) <= 1.0:
			pole = math.degrees(math.asin(val))

		#Q
		Q = 0.0
		val = math.tan(math.radians(self.dataEqu[Planet.DECLEQU]))*math.tan(math.radians(pole))
		if math.fabs(val) <= 1.0:
			Q = math.degrees(math.asin(val))

		#W
		W = 0.0
		if self.eastern:
			W = self.dataEqu[Planet.RAEQU]-Q
		else:
			W = self.dataEqu[Planet.RAEQU]+Q

		W = util.normalize(W)

		#CMP
		Cmp = 0.0
		if self.eastern:
			if umd:
				Cmp = 270.0+tmpzd
			else:
				Cmp = 90.0-tmpzd
		else:
			if umd:
				Cmp = 270.0-tmpzd
			else:
				Cmp = 90.0+tmpzd

		#Roberto's bugreport(Giacomo's chart)
#		if (self.abovehorizon and tablemd < 0.0) or (not self.abovehorizon and tablemd >= 0.0):
#			if Cmp < 0.0:
#				Cmp = 360.0+Cmp
#			else:
#				Cmp = 360.0-Cmp

		#RMP (Roberto)
		RMP = 0.0
		if raequasc != None:
			RMP = util.normalize(W-raequasc)

		#md, hd, zd, pole, q, w
		self.speculums.append((self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], tablemd, self.hd, zd, pole, Q, W, Cmp, RMP))


	def getZD(self, md, lat, decl, umd):
		'''Calculates Regiomontan zenith distance '''

		zd = 0.0
		if md == 90.0:
			zd = 90.0-math.degrees(math.atan(math.sin(math.fabs(math.radians(lat))))*math.tan(math.radians(decl)))
		elif md < 90.0:
			A = math.degrees(math.atan(math.cos(math.radians(lat))*math.tan(math.radians(md))))
			B = math.degrees(math.atan(math.tan(math.fabs(math.radians(lat)))*math.cos(math.radians(md))))

			C = 0.0
			if (decl < 0 and lat < 0) or (decl >= 0 and lat >= 0):
				if umd:
					C = B-math.fabs(decl)
				else:
					C = B+math.fabs(decl)
			elif (decl < 0 and lat > 0) or (decl > 0 and lat < 0):
				if umd:
					C = B+math.fabs(decl)
				else:
					C = B-math.fabs(decl)

			F = math.degrees(math.atan(math.sin(math.fabs(math.radians(lat)))*math.sin(math.radians(md))*math.tan(math.radians(C)))) #C and F can be negative
			zd = A+F

		return zd


	def calcProfPos(self, prof):
		self.data = (util.normalize(self.data[Planet.LONG]+prof.offs), self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])

		#Placidus
		self.speculums[0] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], self.speculums[0][Planet.ADLAT], self.speculums[0][Planet.SA], self.speculums[0][Planet.MD], self.speculums[0][Planet.HD], self.speculums[0][Planet.TH], self.speculums[0][Planet.HOD], self.speculums[0][Planet.PMP], self.speculums[0][Planet.ADPH], self.speculums[0][Planet.POH], self.speculums[0][Planet.AODO])

		#Regiomontanus
		self.speculums[1] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], self.speculums[1][Planet.RMD], self.speculums[1][Planet.RHD], self.speculums[1][Planet.ZD], self.speculums[1][Planet.POLE], self.speculums[1][Planet.Q], self.speculums[1][Planet.W], self.speculums[1][Planet.CMP], self.speculums[1][Planet.RMP])


	def calcMundaneProfPos(self, ascmc2, pl, placelat, obl):
#		print '****** %s ******' % pl.name

		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		md = pl.speculums[0][Planet.MD]
		if md < 0.0:
			md *= -1
#		print 'MD=%f' % md
		ra = pl.speculums[0][Planet.RA]

		if pl.speculums[0][Planet.PMP] < 90.0:
			ra = raic-md
#			print 'Q1'
		elif pl.speculums[0][Planet.PMP] >= 90.0 and pl.speculums[0][Planet.PMP] < 180.0:
			ra = raic+md
#			print 'Q2'
		elif pl.speculums[0][Planet.PMP] >= 180.0 and pl.speculums[0][Planet.PMP] < 270.0:
			ra = ramc-md
#			print 'Q3'
		elif pl.speculums[0][Planet.PMP] >= 270.0 and pl.speculums[0][Planet.PMP] < 360.0:
			ra = ramc+md
#			print 'Q4'

		ra = util.normalize(ra)
#		print 'ra=%f' % ra

		ao = do = 0.0
		adph = math.fabs(pl.speculums[0][Planet.ADPH])#####
		if placelat == 0.0 or pl.speculums[0][Planet.DECL] == 0.0:
			ao = do = ra
#			print 'First'
		if (placelat > 0.0 and pl.speculums[0][Planet.DECL] > 0.0) or (placelat < 0.0 and pl.speculums[0][Planet.DECL] < 0.0):
			ao = ra-adph
			do = ra+adph
#			print 'Second'
		if (placelat > 0.0 and pl.speculums[0][Planet.DECL] < 0.0) or (placelat < 0.0 and pl.speculums[0][Planet.DECL] > 0.0):
			ao = ra+adph
			do = ra-adph
#			print 'Third'

		ao = util.normalize(ao)
		do = util.normalize(do)

		poh = pl.speculums[0][Planet.POH]
		rao = math.radians(ao)
		rdo = math.radians(do)
		robl = math.radians(obl)
		rpoh = math.radians(poh)
		lon = pl.speculums[0][Planet.LONG]
		okGa, okGd, lon = self.iterate(pl, rao, rdo, robl, rpoh, lon)
		if not okGa:
			rao1 = rao+math.radians(0.5)
			lon1 = self.iterate(pl, rao1, rdo, robl, rpoh, lon)
			rao2 = rao-math.radians(0.5)
			lon2 = self.iterate(pl, rao2, rdo, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)
		elif not okGd:
			rdo1 = rdo+math.radians(0.5)
			lon1 = self.iterate(pl, rao, rdo1, robl, rpoh, lon)
			rdo2 = rdo-math.radians(0.5)
			lon2 = self.iterate(pl, rao, rdo2, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)

#		print 'lon=%f' % lon

		self.data = (lon, self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
		self.dataEqu = (ra, self.dataEqu[Planet.DECLEQU], self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])

		#Placidus
		self.speculums[0] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], pl.speculums[0][Planet.ADLAT], pl.speculums[0][Planet.SA], pl.speculums[0][Planet.MD], pl.speculums[0][Planet.HD], pl.speculums[0][Planet.TH], pl.speculums[0][Planet.HOD], pl.speculums[0][Planet.PMP], pl.speculums[0][Planet.ADPH], pl.speculums[0][Planet.POH], pl.speculums[0][Planet.AODO])

		#Regiomontanus
		self.speculums[1] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], pl.speculums[1][Planet.RMD], pl.speculums[1][Planet.RHD], pl.speculums[1][Planet.ZD], pl.speculums[1][Planet.POLE], pl.speculums[1][Planet.Q], pl.speculums[1][Planet.W], pl.speculums[1][Planet.CMP], pl.speculums[1][Planet.RMP])


	def iterate(self, pl, rao, rdo, robl, rpoh, lon):
		
		okGa = okGd = True

		if pl.speculums[0][Planet.PMP] < 90.0 or (pl.speculums[0][Planet.PMP] >= 270.0 and pl.speculums[0][Planet.PMP] < 360.0):
			Ga = math.degrees(math.cos(rao)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))
			if Ga != 0.0:
				Fa = math.degrees(math.atan(math.sin(rao)/(math.cos(rao)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))))

				if Fa >= 0.0 and Ga > 0.0:
					lon = Fa
				elif Fa < 0.0 and Ga > 0.0:
					lon = Fa+360.0
				elif Ga < 0.0:
					lon = Fa+180.0
			else:
				okGa = False
		else:
			Gd = math.degrees(math.cos(rdo)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))
			if Gd != 0.0:
				Fd = math.degrees(math.atan(math.sin(rdo)/(math.cos(rdo)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))))

				if Fd >= 0.0 and Gd > 0.0:
					lon = Fd
				elif Fd < 0.0 and Gd > 0.0:
					lon = Fd+360.0
				elif Gd < 0.0:
					lon = Fd+180.0
			else:
				okGd = False

		return okGa, okGd, lon


	def calcFullAstronomicalProc(self, da, oblN, raN, declN, placelat, ascmc2, raequasc):
#		print '**** %s ****' % pl.name
		ksi = raN+da
		ksi = util.normalize(ksi)

#		print 'ksi=%f' % ksi
#		print 'declN=%f' % declN

		roblN = math.radians(oblN)
		rksi = math.radians(ksi)
		rdeclN = math.radians(declN)
		longSZ = 0.0
		if ksi == 90.0:
			longSZ = 90.0
		elif ksi == 270.0:
			longSZ = 270.0
		else:
#			print 'obl=%f' % oblN
			Fd = 0.0
			if math.cos(rksi) != 0.0:
				Fd = math.degrees(math.atan((math.cos(roblN)*math.sin(rksi)+math.sin(roblN)*math.tan(rdeclN))/math.cos(rksi)))
#				print 'rFd=%f' % math.radians(Fd)

			if ksi >= 0.0 and ksi < 90.0:
				longSZ = Fd
#				print 'First ksi'
			elif ksi > 90.0 and ksi < 270.0:
				longSZ = Fd+180.0
#				print 'Second ksi'
			elif ksi > 270.0 and ksi < 360.0:
				longSZ = Fd+360.0
#				print 'Third ksi'

			if longSZ <= 0.0:
#				print 'longSz<=0'
				longSZ = Fd+360.0
				
		longSZ = util.normalize(longSZ)##
#		print 'longSz=%f' % longSZ

		roblN = math.radians(oblN)
		rksi = math.radians(ksi)
		rdeclN = math.radians(declN)

		latSZ = math.degrees(math.asin(math.sin(rdeclN)*math.cos(roblN)-math.cos(rdeclN)*math.sin(rksi)*math.sin(roblN)))
		raSZ, declSZ, distSZ = astrology.swe_cotrans(longSZ, latSZ, 1.0, -oblN)

		self.data = (longSZ, latSZ, self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
		self.dataEqu = (raSZ, declSZ, self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])

		self.speculums = []
		self.computePlacidianSpeculum(placelat, ascmc2)
		self.computeRegiomontanSpeculum(placelat, ascmc2, raequasc)


	def calcRegioPDsInChartsPos(self, ascmc2, pl, placelat, obl):
#		print '****** %s ******' % pl.name

		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		md = pl.speculums[0][Planet.MD]
		if md < 0.0:
			md *= -1
#		print 'MD=%f' % md
		ra = pl.speculums[0][Planet.RA]

		if pl.speculums[0][Planet.PMP] < 90.0:
			ra = raic-md
#			print 'Q1'
		elif pl.speculums[0][Planet.PMP] >= 90.0 and pl.speculums[0][Planet.PMP] < 180.0:
			ra = raic+md
#			print 'Q2'
		elif pl.speculums[0][Planet.PMP] >= 180.0 and pl.speculums[0][Planet.PMP] < 270.0:
			ra = ramc-md
#			print 'Q3'
		elif pl.speculums[0][Planet.PMP] >= 270.0 and pl.speculums[0][Planet.PMP] < 360.0:
			ra = ramc+md
#			print 'Q4'

		ra = util.normalize(ra)
#		print 'ra=%f' % ra

		qreg = math.fabs(pl.speculums[1][Planet.Q])
		wa = wd = 0.0
		if placelat == 0.0 or pl.speculums[1][Planet.DECL] == 0.0:
			wa = ra
			wd = ra
#			print 'First'
		if (placelat > 0.0 and pl.speculums[1][Planet.DECL] > 0.0) or (placelat < 0.0 and pl.speculums[1][Planet.DECL] < 0.0):
			wa = ra-qreg
			wd = ra+qreg
#			print 'Second'
		if (placelat > 0.0 and pl.speculums[1][Planet.DECL] < 0.0) or (placelat < 0.0 and pl.speculums[1][Planet.DECL] > 0.0):
			wa = ra+qreg
			wd = ra-qreg
#			print 'Third'

		wa = util.normalize(wa)
		wd = util.normalize(wd)

		poh = pl.speculums[1][Planet.POLE]
		rwa = math.radians(wa)
		rwd = math.radians(wd)
		robl = math.radians(obl)
		rpoh = math.radians(poh)
		lon = pl.speculums[1][Planet.LONG]
		okGa, okGd, lon = self.iterateRegio(pl, rwa, rwd, robl, rpoh, lon)
		if not okGa:
			rwa1 = rwa+math.radians(0.5)
			lon1 = self.iterateRegio(pl, rwa1, rwd, robl, rpoh, lon)
			rwa2 = rwa-math.radians(0.5)
			lon2 = self.iterateiRegio(pl, rwa2, rwd, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)
		elif not okGd:
			rwd1 = rwd+math.radians(0.5)
			lon1 = self.iterateiRegio(pl, rwa, rwd1, robl, rpoh, lon)
			rwd2 = rwd-math.radians(0.5)
			lon2 = self.iterateRegio(pl, rwa, rwd2, robl, rpoh, lon)
			lon = (lon1+lon2)/2
			lon = util.normalize(lon)

#		print 'lon=%f' % lon

		self.data = (lon, self.data[Planet.LAT], self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
		self.dataEqu = (ra, self.dataEqu[Planet.DECLEQU], self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])

		#Placidus
		self.speculums[0] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], pl.speculums[0][Planet.ADLAT], pl.speculums[0][Planet.SA], pl.speculums[0][Planet.MD], pl.speculums[0][Planet.HD], pl.speculums[0][Planet.TH], pl.speculums[0][Planet.HOD], pl.speculums[0][Planet.PMP], pl.speculums[0][Planet.ADPH], pl.speculums[0][Planet.POH], pl.speculums[0][Planet.AODO])

		#Regiomontanus
		self.speculums[1] = (self.data[Planet.LONG], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU], pl.speculums[1][Planet.RMD], pl.speculums[1][Planet.RHD], pl.speculums[1][Planet.ZD], pl.speculums[1][Planet.POLE], pl.speculums[1][Planet.Q], pl.speculums[1][Planet.W], pl.speculums[1][Planet.CMP], pl.speculums[1][Planet.RMP])


	def iterateRegio(self, pl, rwa, rwd, robl, rpoh, lon):
		
		okGa = okGd = True

		if pl.speculums[0][Planet.PMP] < 90.0 or (pl.speculums[0][Planet.PMP] >= 270.0 and pl.speculums[0][Planet.PMP] < 360.0):
			Ga = math.degrees(math.cos(rwa)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))
			if Ga != 0.0:
				Fa = math.degrees(math.atan(math.sin(rwa)/(math.cos(rwa)*math.cos(robl)-math.sin(robl)*math.tan(rpoh))))

				if Fa >= 0.0 and Ga > 0.0:
					lon = Fa
				elif Fa < 0.0 and Ga > 0.0:
					lon = Fa+360.0
				elif Ga < 0.0:
					lon = Fa+180.0
			else:
				okGa = False
		else:
			Gd = math.degrees(math.cos(rwd)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))
			if Gd != 0.0:
				Fd = math.degrees(math.atan(math.sin(rwd)/(math.cos(rwd)*math.cos(robl)+math.sin(robl)*math.tan(rpoh))))

				if Fd >= 0.0 and Gd > 0.0:
					lon = Fd
				elif Fd < 0.0 and Gd > 0.0:
					lon = Fd+360.0
				elif Gd < 0.0:
					lon = Fd+180.0
			else:
				okGd = False

		return okGa, okGd, lon


	def calcMundaneWithoutSM(self, da, obl, placelat, ascmc2, raequasc):
		ra = self.dataEqu[Planet.RAEQU]
		decl = self.dataEqu[Planet.DECLEQU]

		da *= -1
		ra += da

		ra = util.normalize(ra)

		lon, lat, dist = astrology.swe_cotrans(ra, decl, 1.0, obl)

		self.data = (lon, lat, self.data[Planet.DIST], self.data[Planet.SPLON], self.data[Planet.SPLAT], self.data[Planet.SPDIST])
		self.dataEqu = (ra, decl, self.dataEqu[Planet.DISTEQU], self.dataEqu[Planet.SPRAEQU], self.dataEqu[Planet.SPDECLEQU], self.dataEqu[Planet.SPDISTEQU])

		self.speculums = []
		self.computePlacidianSpeculum(placelat, ascmc2)
		self.computeRegiomontanSpeculum(placelat, ascmc2, raequasc)




class Planets:
	"""Calculates the positions of the planets"""

#	HELIOCENTRIC = 
#	ECLIPTIC = 
#	EQUATORIAL =
#	XYZ = 
#	TOPOCENTRIC = 
#	SIDEREAL = 
	
	PLANETS_NUM = 12

	def __init__(self, tjd_ut, meannode, flag, lat, ascmc2, raequasc, nolat = False, obl = 0.0):

		self.planets = []

		self.create(self.planets, tjd_ut, meannode, flag, lat, ascmc2, raequasc, nolat, obl)
		

	def create(self, pls, tjd_ut, meannode, flag, lat, ascmc2, raequasc, nolat, obl):
		for i in range(astrology.SE_SUN, astrology.SE_PLUTO+1):
			pls.append(Planet(tjd_ut, i, flag, lat, ascmc2, raequasc, None, None, nolat, obl))

		node = astrology.SE_TRUE_NODE
		if meannode:
			node = astrology.SE_MEAN_NODE

		pls.append(Planet(tjd_ut, node, flag, lat, ascmc2, raequasc, None, None, nolat, obl))

		data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		#Node+180.0 in planets
		data[Planet.LONG] = pls[astrology.SE_PLUTO+1].data[Planet.LONG]+180.0
		if data[Planet.LONG] > 360.0:
			data[Planet.LONG] -= 360.0
		data[Planet.LAT] = pls[astrology.SE_PLUTO+1].data[Planet.LAT]
		data[Planet.DIST] = pls[astrology.SE_PLUTO+1].data[Planet.DIST]
		data[Planet.SPLON] = pls[astrology.SE_PLUTO+1].data[Planet.SPLON]
		data[Planet.SPLAT] = pls[astrology.SE_PLUTO+1].data[Planet.SPLAT]
		data[Planet.SPDIST] = pls[astrology.SE_PLUTO+1].data[Planet.SPDIST]

		dataEqu = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		#Equatorial: Node+180.0 in planets
		dataEqu[Planet.RAEQU] = pls[astrology.SE_PLUTO+1].dataEqu[Planet.RAEQU]+180.0
		if dataEqu[Planet.RAEQU] > 360.0:
			dataEqu[Planet.RAEQU] -= 360.0
		dataEqu[Planet.DECLEQU] = -1*(pls[astrology.SE_PLUTO+1].dataEqu[Planet.DECLEQU])
		dataEqu[Planet.DISTEQU] = pls[astrology.SE_PLUTO+1].dataEqu[Planet.DISTEQU]
		dataEqu[Planet.SPRAEQU] = pls[astrology.SE_PLUTO+1].dataEqu[Planet.SPRAEQU]
		dataEqu[Planet.SPDECLEQU] = pls[astrology.SE_PLUTO+1].dataEqu[Planet.SPDECLEQU]
		dataEqu[Planet.SPDISTEQU] = pls[astrology.SE_PLUTO+1].dataEqu[Planet.SPDISTEQU]

		pls.append(Planet(tjd_ut, node, flag, lat, ascmc2, raequasc, data, dataEqu, nolat, obl))


	def calcProfPos(self, prof):
		for pl in range(Planets.PLANETS_NUM):
			self.planets[pl].calcProfPos(prof)


	def calcMundaneProfPos(self, ascmc2, pls, placelat, obl):
		for pl in range(Planets.PLANETS_NUM):
			self.planets[pl].calcMundaneProfPos(ascmc2, pls[pl], placelat, obl)


	def calcFullAstronomicalProc(self, da, oblN, pls, placelat, ascmc2, raequasc):
		for pl in range(Planets.PLANETS_NUM):
			self.planets[pl].calcFullAstronomicalProc(da, oblN, pls[pl].dataEqu[Planet.RAEQU], pls[pl].dataEqu[Planet.DECLEQU], placelat, ascmc2, raequasc)


	def calcRegioPDsInChartsPos(self, ascmc2, pls, placelat, obl):
		for pl in range(Planets.PLANETS_NUM):
			self.planets[pl].calcRegioPDsInChartsPos(ascmc2, pls[pl], placelat, obl)


	def calcMundaneWithoutSM(self, da, obl, placelat, ascmc2, raequasc):
		for pl in range(Planets.PLANETS_NUM):
			self.planets[pl].calcMundaneWithoutSM(da, obl, placelat, ascmc2, raequasc)




