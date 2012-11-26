import math
import astrology
import houses
import util


class CustomerPD:
	"""Data of CPD"""

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

	def __init__(self, londeg, lonmin, lonsec, latdeg, latmin, latsec, southern, placelat, ascmc2, obl, raequasc):
		self.londeg = londeg
		self.lonmin = lonmin
		self.lonsec = lonsec
		self.latdeg = latdeg
		self.latmin = latmin
		self.latsec = latsec
		self.southern = southern

		self.lon = londeg+lonmin/60.0+lonsec/3600.0
		self.lat = latdeg+latmin/60.0+latsec/3600.0

		if self.southern:
			self.lat *= -1

		self.ra, self.decl, dist = astrology.swe_cotrans(self.lon, self.lat, 1.0, -obl)

		self.speculums = []
		self.computePlacidianSpeculum(placelat, ascmc2)
		self.computeRegiomontanSpeculum(placelat, ascmc2, raequasc)


	def computePlacidianSpeculum(self, placelat, ascmc2):
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

		#sa, adlat, md, adph, ph, ao/do

		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		self.eastern = True
		if ramc > raic:
			if self.ra > raic and self.ra < ramc:
				self.eastern = False
		else:
			if (self.ra > raic and self.ra < 360.0) or (self.ra < ramc and self.ra > 0.0):
				self.eastern = False

		#adlat
		adlat = 0.0
		val = math.tan(math.radians(placelat))*math.tan(math.radians(self.decl))
		if math.fabs(val) <= 1.0:
			adlat = math.degrees(math.asin(val))

		#md
		med = math.fabs(ramc-self.ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(raic-self.ra)
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

		aohd = self.ra-adlat
		hdasc = aohd-aoasc
		if hdasc < 0.0:
			hdasc *= -1
		if hdasc > 180.0:
			hdasc = 360.0-hdasc 

		dohd = self.ra+adlat
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
			adphi = math.fabs(md)*adlat/tval

		#phi
		tval = math.tan(math.radians(self.decl))
		phi = 0.0
		if tval != 0.0:
			phi = math.degrees(math.atan(math.sin(math.radians(adphi))/tval))

		#ao/do (southern hemisphere!?)
		if self.eastern:
			ao = self.ra-adphi
		else:
			ao = self.ra+adphi
			ao *= -1 #do if negative

		self.speculums.append((self.lon, self.lat, self.ra, self.decl, adlat, sa, md, self.hd, th, hod, pmp, adphi, phi, ao))


	def computeRegiomontanSpeculum(self, placelat, ascmc2, raequasc):
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
			

		md = self.speculums[0][CustomerPD.MD]

		umd = True
		if md < 0.0:
			md *= -1
			umd = False

		#zd
		zd = self.getZD(md, placelat, self.decl, umd)
		tmpzd = zd
#		if not abovehorizon:
		if not umd: #!? or with abovehorizon!?
			zd *= -1

		#pole
		pole = 0.0
		val = math.sin(math.radians(placelat))*math.sin(math.radians(tmpzd))
		if math.fabs(val) <= 1.0:
			pole = math.degrees(math.asin(val))

		#Q
		Q = 0.0
		val = math.tan(math.radians(self.decl))*math.tan(math.radians(pole))
		if math.fabs(val) <= 1.0:
			Q = math.degrees(math.asin(val))

		#W
		W = 0.0
		if self.eastern:
			W = self.ra-Q
		else:
			W = self.ra+Q

		W = util.normalize(W)

		#CMP
		Cmp = 0.0
		if self.eastern:
			if umd:
				Cmp = 270+tmpzd
			else:
				Cmp = 90-tmpzd
		else:
			if umd:
				Cmp = 270-tmpzd
			else:
				Cmp = 90+tmpzd

		#RMP (Roberto)
		RMP = 0.0
		if raequasc != None:
			RMP = util.normalize(W-raequasc)

		#md, zd, pole, q, w
		md = self.speculums[0][CustomerPD.MD]
		self.speculums.append((self.lon, self.lat, self.ra, self.decl, md, self.hd, zd, pole, Q, W, Cmp, RMP))


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


