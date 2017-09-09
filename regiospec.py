import math
import astrology
import houses
import util


class RegiomontanianSpeculum:
	'''Calculates Regiomontanian Speculum for an object'''

	LON, LAT, RA, DECL, RMD, RHD, ZD, POLE, Q, W, CMP, RMP, AZM, ELV = range(14)
# ########################################
# Roberto change - V 7.1.0
# ########################################

	def __init__(self, placelat, ascmc2, raequasc, lon, lat, ra, decl):
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

# ########################################
# Roberto change - V 7.1.0
		#AZM (Astrological Azimuth, 0 = East, Counterclockwise)
		#
		#HA=ra-ramc
		#if HA<0:
		        #HA=360+HA
		#
		#alt=arcsin[sin(lat)sin(decl)+cos(lat)cos(decl)cos(HA)]
		#
		#AZMn=arccos[[cos(lat)sin(decl)-sin(lat)cos(decl)cos(HA)]/[cos(alt)]]
		#if HA>180:
		        #AZMn=360-AZMn
		#AZM=450-AZMn
		#if AZM>360:
		        #AZM=AZM-360
		
		#ELV (Astrological = Astronomical Elevation)
		#ELV=alt
# ########################################
			
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

		#md
		med = math.fabs(ramc-ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(raic-ra)
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

		#adlat
		adlat = 0.0
		val = math.tan(math.radians(placelat))*math.tan(math.radians(decl))
		if math.fabs(val) <= 1.0:
			adlat = math.degrees(math.asin(val))

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

		#zd
		zd = self.getZD(md, placelat, decl, umd)
		if zd > 90.0:
			zd = 180.0-zd
		tmpzd = zd
# ###########################################
# Roberto REGIO SPEC fix - V 7.0.1
		if (self.abovehorizon and md < 0.0):
			zd *= -1				
		if (not self.abovehorizon and md > 0.0):
			zd *= -1
# ###########################################

		#pole
		pole = 0.0
		val = math.sin(math.radians(placelat))*math.sin(math.radians(tmpzd))
		if math.fabs(val) <= 1.0:
			pole = math.degrees(math.asin(val))

		#Q
		Q = 0.0
		val = math.tan(math.radians(decl))*math.tan(math.radians(pole))
		if math.fabs(val) <= 1.0:
			Q = math.degrees(math.asin(val))

		#W
		W = 0.0
		if self.eastern:
			W = ra-Q
		else:
			W = ra+Q

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
# ###########################################
# Roberto CMP fix - V 7.0.0
		if (self.abovehorizon and tablemd < 0.0) or (not self.abovehorizon and tablemd > 0.0):
				Cmp = 360.0-Cmp 
# ###########################################

		#RMP (Roberto)
		RMP = 0.0
		if raequasc != None:
			RMP = util.normalize(W-raequasc)

# ########################################
# Roberto change - V 7.1.0
		#AZM
		#ELV

		AZM = 0.0 #Astrological Azimuth
		ELV = 0.0 #Altitude
		
		HAn = 0.0 #Hourly angle
		Han = ra-ramc
		if Han < 0.0:
			Han = 360+Han

		val = math.sin(math.radians(placelat))*math.sin(math.radians(decl))+math.cos(math.radians(placelat))*math.cos(math.radians(decl))*math.cos(math.radians(Han))	
		if math.fabs(val) <= 1.0:
			ELV = math.degrees(math.asin(val))
				
		val = (math.cos(math.radians(placelat))*math.sin(math.radians(decl))-math.sin(math.radians(placelat))*math.cos(math.radians(decl))*math.cos(math.radians(Han)))/math.cos(math.radians(ELV))		

		if math.fabs(val) <= 1.0:
			val = math.degrees(math.acos(val))
		if Han > 180:
			val = 360-val
		val = 450-val
		if val > 360:
			val = val-360
		AZM = val
# ########################################

		#md, hd, zd, pole, q, w
		self.speculum = (lon, lat, ra, decl, tablemd, hd, zd, pole, Q, W, Cmp, RMP, AZM, ELV)
# ########################################
# Roberto change - V 7.1.0
# ########################################

	def getZD(self, md, placelat, decl, umd):
		'''Calculates Regiomontan zenith distance '''

		zd = 0.0
		if md == 90.0:
			zd = 90.0-math.degrees(math.atan(math.sin(math.fabs(math.radians(placelat))))*math.tan(math.radians(decl)))
		elif md < 90.0:
			A = math.degrees(math.atan(math.cos(math.radians(placelat))*math.tan(math.radians(md))))
			B = math.degrees(math.atan(math.tan(math.fabs(math.radians(placelat)))*math.cos(math.radians(md))))

			C = 0.0
			if (decl < 0 and placelat < 0) or (decl >= 0 and placelat >= 0):
				if umd:
					C = B-math.fabs(decl)
				else:
					C = B+math.fabs(decl)
			elif (decl < 0 and placelat > 0) or (decl > 0 and placelat < 0):
				if umd:
					C = B+math.fabs(decl)
				else:
					C = B-math.fabs(decl)

			F = math.degrees(math.atan(math.sin(math.fabs(math.radians(placelat)))*math.sin(math.radians(md))*math.tan(math.radians(C)))) #C and F can be negative
			zd = A+F

		return zd


