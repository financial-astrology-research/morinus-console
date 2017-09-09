import math
import datetime
import calendar


def decToDeg(num):
	"""Converts a float number to deg min sec"""
	num = math.fabs(num)
	d = int(num)
	part = (num-d)*60
	m = int(part)
	s = int((part-m)*60)
	return (d, m, s)


def normalize(deg):
	"""Adjusts deg between 0-360"""
	while deg < 0.0:
		deg += 360.0
	while deg >= 360.0:
		deg -= 360.0
	return deg
	   

def normalizeTime(t):
	"""Adjusts time between 0-24"""
	while t < 0.0:
		t += 24.0
	while t > 24.0:
		t -= 24.0
	return t


def roundDeg(d, m, s):
	if s > 30:
		m += 1
		if m == 60:
			m = 0
			d += 1
			if d == 30:
				d = 0

	return (d, m)


# Given an x and y coordinate, return the angle formed by a line from the 
# origin to this coordinate. This is just converting from rectangular to  
# polar coordinates; however, we don't determine the radius here.         
def angle(x, y):
	if (x != 0.0): 
		if (y != 0.0):
			a = math.atan(y/x)
		else:
			if x < 0.0:
				a = math.pi
			else:
				a = 0.0
	else:
		if y < 0.0:
			a = -math.pi/2
		else:
			a = math.pi/2
	if (a < 0.0):
		a += math.pi
	if (y < 0.0):
		a += math.pi

	return a


def transform(lon, lat, tilt):
	"""(lon,lat,obl) is ecl2equ, (ra,decl,-obl) is equ2ecl, (ra,decl,pi-lat) is EquToLocal"""
	lon = math.radians(lon)
	lat = math.radians(lat)
	tilt = math.radians(tilt)

	sinalt = math.sin(lat)
	cosalt = math.cos(lat)
	sinazi = math.sin(lon)
	sintilt = math.sin(tilt)
	costilt = math.cos(tilt)

	x = cosalt * sinazi * costilt
	y = sinalt * sintilt
	x -= y
	a1 = cosalt
	y = cosalt * math.cos(lon)
	l1 = angle(y, x)
	a1 = a1 * sinazi * sintilt + sinalt * costilt
	a1 = math.asin(a1)

	return (math.degrees(l1), math.degrees(a1))


def ra2ecl(ra, obl):
	lon = 0.0

	if ra == 0.0 or ra == 90.0 or ra == 180.0 or ra == 270.0:
		lon = ra
	elif ra < 90.0:
		lon = math.degrees(math.atan(math.tan(math.radians(ra))/math.cos(math.radians(obl))))
	elif ra > 90.0 and ra < 180.0:
		ra = 180.0-ra
		lon = math.degrees(math.atan(math.tan(math.radians(ra))/math.cos(math.radians(obl))))
		lon = 180.0-lon
	elif ra > 180.0 and ra < 270.0:
		ra -= 180.0
		lon = math.degrees(math.atan(math.tan(math.radians(ra))/math.cos(math.radians(obl))))
		lon += 180.0
	elif ra > 270.0 and ra < 360.0:
		ra = 360.0-ra
		lon = math.degrees(math.atan(math.tan(math.radians(ra))/math.cos(math.radians(obl))))
		lon = 360.0-lon

	return lon
		

def decrMonth(year, month):
	y = year
	m = month
	if m != 1:
		m -= 1
	else:
		m = 12
		y -= 1
	
	return y, m


def incrMonth(year, month):
	y = year
	m = month
	if m != 12:
		m += 1
	else:
		m = 1
		y += 1
	
	return y, m


def incrDay(year, month, day):
	y = year
	m = month
	d = day

	d += 1

	if y > 0:
		try:	
			datetime.datetime(y, m, d, 0, 0, 0)
		except ValueError:
			d = 1
			if m < 12:
				m += 1
			else:
				m = 1
				y += 1
	else:
		days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
		dd = days[m-1]
		if d > dd:
			d = 1
			if m < 12:
				m += 1
			else:
				m = 1
				y += 1

	return y, m, d


def decrDay(year, month, day):
	y = year
	m = month
	d = day

	if d > 1:
		d -= 1
	else:
		if m > 1:
			m -= 1
		else:
			m = 12
			y -= 1

		if y > 0:
			d = 31
			found = False
			for j in range(4):	
				try:	
					datetime.datetime(y, m, d, 0, 0, 0)
					found = True
					break
				except ValueError:
					d -= 1
			if not found:
				d = 28
		else:
			days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
			d = days[m-1]

	return y, m, d


def addSecs(y, m, d, h, mi, s, sadd):
	s += sadd

	if s >= 60:
		if s > 60:
			s -= 60
		else:
			s = 0
		y, m, d, h, mi = addMins(y, m, d, h, mi, 1)

	return y, m, d, h, mi, s


def subtractSecs(y, m, d, h, mi, s, ssub):
	s -= ssub

	if s < 0:
		s += 60
		y, m, d, h, mi = subtractMins(y, m, d, h, mi, 1)

	return y, m, d, h, mi, s


def addMins(y, m, d, h, mi, madd):
	mi += madd

	if mi >= 60:
		if mi > 60:
			mi -= 60
		else:
			mi = 0

		h += 1
		if h == 24:
			h = 0
			y, m, d = incrDay(y, m, d)

	return y, m, d, h, mi


def subtractMins(y, m, d, h, mi, msub):
	mi -= msub

	if mi < 0:
		mi += 60

		h -= 1
		if h < 0:
			h = 23
			y, m, d = decrDay(y, m, d)

	return y, m, d, h, mi


def addHour(y, m, d, h):
	h += 1
	if h == 24:
		h = 0
		y, m, d = incrDay(y, m, d)

	return y, m, d, h


def subtractHour(y, m, d, h):
	h -= 1
	if h < 0:
		h = 23
		y, m, d = decrDay(y, m, d)

	return y, m, d, h


def checkDate(year, month, day):
	try:	
		datetime.datetime(year, month, day, 0, 0, 0)

	except ValueError:
		return False

	return True


def convDate(year, month, day):
	days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

	ds = 0
	for i in range(0, month-1):
		ds += days[i]

	extra = 0
	if calendar.isleap(year):
		ds += 1
		extra = 1

	return year+(ds+day)/(365.0+extra)


def revConvDate(dat):
	days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
	MONTHSPERYEAR = 12

	year = int(dat)
	frac = dat-year

	extra = 0
	if calendar.isleap(year):
		extra = 1

	ds = int((365.0+extra)*frac)

	month = 1
	for i in range(0, MONTHSPERYEAR-1):
		numdays = days[i]
		if i == 1 and extra != 0:
			numdays += 1

		if ds > numdays:
			ds -= numdays
			month += 1
		else:
			break

	#just for safety
#	if ds < 1:
#		ds = 1
#	elif ds > 31:
#		ds = 31

	return year, month, ds, extra


def getPrevDay(day):
	day -= 1
	if day < 0:
		day = 6

	return day


def getNextDay(day):
	day += 1
	if day > 6:
		day = 0

	return day


def getRaDecl(lon, lat, obl):
	rlon = math.radians(lon)
	rlat = math.radians(lat)
	robl = math.radians(obl)
	decl = math.degrees(math.asin(math.cos(robl)*math.sin(rlat)+math.sin(robl)*math.cos(rlat)*math.sin(rlon)))
	rdecl = math.radians(decl)

	ra = 0.0
	if lon == 90.0 or lon == 270.0:
		ra = lon
	else:
		X = math.degrees(math.atan(math.tan(rlon)/math.cos(robl))-sgn(math.cos(rlon))*math.asin(math.tan(rdecl)*math.sin(robl)/math.sqrt(math.pow(math.tan(rlon),2)+math.pow(math.cos(robl),2))))
		if lon >= 0.0 and lon < 90.0:
			ra = X
		elif lon > 90.0 and lon < 270.0:
			ra = X+180.0
		elif lon > 270.0 and lon < 360.0:
			ra = X+360.0

		ra = normalize(ra)

	return ra, decl
			

def sgn(x):
	ret = 0

	if x < 0.0:
		ret = -1
	elif x > 0.0:
		ret = 1
	else:
		ret = 0

	return ret



