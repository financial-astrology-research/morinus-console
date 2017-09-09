import math
import houses


class PlacidianSpeculum:
	'''Calculates Placidian Speculum for an object'''

	LON, LAT, RA, DECL, ADLAT, SA, MD, HD, TH, HOD, PMP, ADPH, POH, AODO = range(0, 14)


	def __init__(self, placelat, ascmc2, lon, lat, ra, decl):
		#transform
		#0-90: x = x
		#90-180: 180-x = 180-x	(before the trigon. calc. subtract x from 180.0 and at the end of the calc the result should be subtr. from 180.0)
		#180-270: x-180 = x+180	(before the trigon. calc. subtract 180.0 from x and at the end of the calc the result should be added to 180.0)
		#270-360: 360-x = 360-x

		#sin(delta) = sin(long)*sin(obl)
		#sin(ar) = ctg(obl)*tg(delta)   or tg(ar) = cos(obl)*/ctg(long)
		#cos(war) = cos(long)*cos(beta)/cos(delta)

		#sin(A.D.)(FI or placelat)[ascensio-differentia] = tg(FI)*tg(delta)
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

		#the sign (positive or negative) is used in the Positions-table (e.g. if SA is positive then a 'D' will indicate that it is diurnal)

		ramc = ascmc2[houses.Houses.MC][houses.Houses.RA]
		raic = ramc+180.0
		if raic > 360.0:
			raic -= 360.0

		self.eastern = True
		if ramc > raic:
			if ra > raic and ra < ramc:
				self.eastern = False
		else:
			if (ra > raic and ra < 360.0) or (ra < ramc and ra > 0.0):
				self.eastern = False

		#adlat
		adlat = 0.0
		self.valid = True
		val = math.tan(math.radians(placelat))*math.tan(math.radians(decl))
		if math.fabs(val) <= 1.0:
			adlat = math.degrees(math.asin(val))
			self.valid = False

		#md
		med = math.fabs(ramc-ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(raic-ra)
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

		aohd = ra-adlat
		hdasc = aohd-aoasc
		if hdasc < 0.0:
			hdasc *= -1
		if hdasc > 180.0:
			hdasc = 360.0-hdasc 

		dohd = ra+adlat
		hddesc = dohd-dodesc
		if hddesc < 0.0:
			hddesc *= -1
		if hddesc > 180.0:
			hddesc = 360.0-hddesc 

		hd = hdasc
		if hddesc < hdasc:
			hd = hddesc
			hd *= -1

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
		tval = math.tan(math.radians(decl))
		phi = 0.0
		if tval != 0.0:
			phi = math.degrees(math.atan(math.sin(math.radians(adphi))/tval))

		#ao/do (southern hemisphere!?)
		if self.eastern:
			ao = ra-adphi
		else:
			ao = ra+adphi
			ao *= -1 #do if negative

		self.speculum = (lon, lat, ra, decl, adlat, sa, md, hd, th, hod, pmp, adphi, phi, ao)


