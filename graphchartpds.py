import wx
import Image, ImageDraw, ImageFont
import math
import astrology
import chart, houses, planets, fortune
import fixstars
import options
import common
import util
import mtexts


class GraphChartPDs:

	DEG1 = math.pi/180
	DEG5 = math.pi/36
	DEG10 = math.pi/18
	DEG30 = math.pi/6

	SMALL_SIZE = 400
	MEDIUM_SIZE = 600

	def __init__(self, chartRadix, chartPDs, chartIngress, size, opts, bw):
		self.chartRadix = chartRadix
		self.chartPDs = chartPDs
		self.chartIngress = chartIngress
		self.w, self.h = size
		self.options = opts
		self.bw = bw
		self.buffer = wx.EmptyBitmap(self.w, self.h)
		self.bdc = wx.BufferedDC(None, self.buffer)
		self.chartsize = min(self.w, self.h)
		self.maxradius = self.chartsize/2
		self.center = wx.Point(self.w/2, self.h/2)

		self.arrowlen = 0.04
		self.symbolSize = self.maxradius/16

		#Radix (innermost)
		self.signSize = self.maxradius/20
		self.rEarth = 0.10*self.maxradius #'r' means radius
		self.rHouses = 0.16*self.maxradius
		self.rHouseName = self.rEarth+(self.rHouses-self.rEarth)/2.0
		self.rPlanets = 0.34*self.maxradius
		self.rSigns = 0.45*self.maxradius
		self.r30 = 0.50*self.maxradius
		self.signsectorlen = 0.1
		self.deg01510len = 0.01
		self.r10 = self.r30-self.deg01510len*self.maxradius
		self.r0 = self.r30-self.signsectorlen*self.maxradius
		self.r10Inner = self.r0+self.deg01510len*self.maxradius
		self.planetsectorlen = self.r0-self.rHouses

		self.rASCMC = self.rSigns-0.03*self.maxradius
		self.rArrow = self.rASCMC+self.arrowlen*self.maxradius
		self.rLine = self.r0-0.02*self.maxradius

		self.rPosDeg = self.rPlanets-0.07*self.maxradius
		self.rPosMin = self.rPosDeg-0.04*self.maxradius
		self.rRetr = self.rPosMin-0.05*self.maxradius

		#PDs
		self.rPDsline0 = self.r30+self.planetsectorlen
		self.rPlanetsPDs = self.r30+(self.r0-self.rPlanets)
		self.rAscMCPDsBeg = self.r30+(self.r0-0.8*self.rPlanets)
		self.rASCMCPDs = self.rPDsline0-0.05*self.maxradius
		self.rArrowPDs = self.rASCMCPDs+self.arrowlen*self.maxradius
		self.rRetrPDs = self.rPlanetsPDs+0.06*self.maxradius
		self.rPosMinPDs = self.rRetrPDs+0.04*self.maxradius
		self.rPosDegPDs = self.rPosMinPDs+0.04*self.maxradius
		self.rLinePDs = self.r30+0.02*self.maxradius


		#Ingress (outermost)
		self.rIngressline0 = self.rPDsline0+self.planetsectorlen
		self.rPlanetsIng = self.rPDsline0+(self.r0-self.rPlanets)
		self.rRetrIng = self.rPlanetsIng+0.06*self.maxradius
		self.rPosMinIng = self.rRetrIng+0.04*self.maxradius
		self.rPosDegIng = self.rPosMinIng+0.04*self.maxradius
		self.rLineIng = self.rPDsline0+0.02*self.maxradius

		#Fonts
		self.smallsymbolSize = 2*self.symbolSize/3

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.symbolSize)
		self.fntSmallMorinus = ImageFont.truetype(common.common.symbols, self.smallsymbolSize)
		self.fntMorinusSigns = ImageFont.truetype(common.common.symbols, self.signSize)
		self.fntText = ImageFont.truetype(common.common.abc, self.symbolSize/2)
		self.fntSmallText = ImageFont.truetype(common.common.abc, self.symbolSize/4)
		self.fntSmallText2 = ImageFont.truetype(common.common.abc, self.symbolSize/3)
		self.fntBigText = ImageFont.truetype(common.common.abc, self.symbolSize/4*3)
		self.fntMorinus2 = ImageFont.truetype(common.common.symbols, self.symbolSize/4*3)
		self.fntRetr = ImageFont.truetype(common.common.symbols, self.symbolSize/2)
		self.deg_symbol = u'\u00b0'

#		self.hsystem = {'P':mtexts.txts['HSPlacidus'], 'K':mtexts.txts['HSKoch'], 'R':mtexts.txts['HSRegiomontanus'], 'C':mtexts.txts['HSCampanus'], 'E':mtexts.txts['HSEqual'], 'W':mtexts.txts['HSWholeSign'], 'X':mtexts.txts['HSAxial'], 'M':mtexts.txts['HSMorinus'], 'H':mtexts.txts['HSHorizontal'], 'T':mtexts.txts['HSPagePolich'], 'B':mtexts.txts['HSAlcabitus'], 'O':mtexts.txts['HSPorphyrius']}

#		self.ayans = {0:mtexts.txts['None'], 1:mtexts.txts['FaganBradley'], 2:mtexts.txts['Lahiri'], 3:mtexts.txts['Deluce'], 4:mtexts.txts['Raman'], 5:mtexts.txts['Ushashashi'], 6:mtexts.txts['Krishnamurti'], 7:mtexts.txts['DjwhalKhul'], 8:mtexts.txts['Yukteshwar'], 9:mtexts.txts['JNBhasin'], 10:mtexts.txts['BabylonianKuglerI2'], 11:mtexts.txts['BabylonianKuglerII2'], 12:mtexts.txts['BabylonianKuglerIII2'], 13:mtexts.txts['BabylonianHuber2'], 14:mtexts.txts['BabylonianMercier2'], 15:mtexts.txts['Aldebaran15Tau2'], 16:mtexts.txts['Hipparchos'], 17:mtexts.txts['Sassanian'], 18:mtexts.txts['GalacticCenter0Sag2'], 19:mtexts.txts['J2000'], 20:mtexts.txts['J1900'], 21:mtexts.txts['B1950']}


	def drawChart(self):
		self.drawCircles()

		if self.options.houses:
			self.drawHouses(self.chartRadix.houses, self.rEarth, self.r0)

		self.drawAscMC(self.chartRadix.houses.ascmc, self.rEarth, self.rASCMC, self.rArrow)
		self.drawAscMC(self.chartPDs.houses.ascmc, self.rAscMCPDsBeg, self.rASCMCPDs, self.rArrowPDs, True)

		#Convert to PIL (truetype-font is not supported in wxPython)
		wxImag = self.buffer.ConvertToImage()
		self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
		self.img.fromstring(wxImag.GetData())
		self.draw = ImageDraw.Draw(self.img)

		if self.options.houses:
			self.drawHouseNames(self.chartRadix, self.rHouseName)

		self.drawSigns()

		self.pshift = self.arrange(self.chartRadix.planets.planets, self.chartRadix.fortune.fortune, self.rPlanets)
		self.drawPlanets(self.chartRadix, self.pshift, self.rPlanets, self.rPosDeg, self.rPosMin, self.rRetr)
		self.pshiftPDs = self.arrange(self.chartPDs.planets.planets, self.chartPDs.fortune.fortune, self.rPlanetsPDs)
		self.drawPlanets(self.chartPDs, self.pshiftPDs, self.rPlanetsPDs, self.rPosDegPDs, self.rPosMinPDs, self.rRetrPDs)
		self.pshiftIng = self.arrange(self.chartIngress.planets.planets, self.chartIngress.fortune.fortune, self.rPlanetsIng)
		self.drawPlanets(self.chartIngress, self.pshiftIng, self.rPlanetsIng, self.rPosDegIng, self.rPosMinIng, self.rRetrIng)

		#Convert back from PIL
		wxImg = wx.EmptyImage(self.img.size[0], self.img.size[1])
		wxImg.SetData(self.img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)
		self.bdc = wx.BufferedDC(None, self.buffer)

		self.drawPlanetLines(self.pshift, self.chartRadix.planets.planets, self.chartRadix.fortune.fortune, self.r0, self.rLine)
		self.drawPlanetLines(self.pshiftPDs, self.chartPDs.planets.planets, self.chartPDs.fortune.fortune, self.r30, self.rLinePDs)
		self.drawPlanetLines(self.pshiftIng, self.chartIngress.planets.planets, self.chartIngress.fortune.fortune, self.rPDsline0, self.rLineIng)

		return self.buffer


	def drawCircles(self):
		bkgclr = self.options.clrbackground
		if self.bw:
			bkgclr = (255,255,255)
		self.bdc.SetBackground(wx.Brush(bkgclr))
		self.bdc.Clear()
		self.bdc.BeginDrawing()

		self.bdc.SetBrush(wx.Brush(bkgclr))	

		(cx, cy) = self.center.Get()

		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)

		w = 3
		if self.chartsize <= GraphChartPDs.SMALL_SIZE:
			w = 1
		elif self.chartsize <= GraphChartPDs.MEDIUM_SIZE:
			w = 2

		#Ingress
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rIngressline0)

		#PDs
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rPDsline0)

		#Radix (innermost)
		#r30 circle
		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.r30)

		#r10 Circle
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.r10)

		#r10Inner Circle
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.r10Inner)

		#r0 Circle
		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.r0)

		#rHouse Circle
		if self.options.houses:
			clr = self.options.clrhouses
			if self.bw:
				clr = (0,0,0)
			pen = wx.Pen(clr, 1)
			self.bdc.SetPen(pen)
			self.bdc.DrawCircle(cx, cy, self.rHouses)

		#Earth Circle
		clr = self.options.clrAscMC
		if self.bw:
			clr = (0,0,0)

		w = self.options.ascmcsize
		if self.chartsize <= GraphChartPDs.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
			w = 2
		elif self.chartsize <= GraphChartPDs.MEDIUM_SIZE and (w == 5 or w == 4):
			w = 3

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rEarth)

		asclon = self.chartRadix.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)

		#30-degs
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		w = 3
		if self.chartsize <= GraphChartPDs.SMALL_SIZE:
			w = 1
		elif self.chartsize <= GraphChartPDs.MEDIUM_SIZE:
			w = 2

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.drawLines(GraphChartPDs.DEG30, asclon, self.r0, self.r30)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.drawLines(GraphChartPDs.DEG30, asclon, self.r30, self.rIngressline0)

		#10-degs
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		w = 2
		if self.chartsize <= GraphChartPDs.MEDIUM_SIZE:
			w = 1

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.drawLines(GraphChartPDs.DEG10, asclon, self.r30, self.r10)
		self.drawLines(GraphChartPDs.DEG10, asclon, self.r0, self.r10Inner)

		self.bdc.EndDrawing()


	def drawSigns(self):
		(cx, cy) = self.center.Get()
		clr = self.options.clrsigns
		if self.bw:
			clr = (0,0,0)
		j = 0
		asclon = self.chartRadix.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)
		i = math.pi+math.radians(asclon)-GraphChartPDs.DEG30/2

		signs = common.common.Signs1
		if not self.options.signs:
			signs = common.common.Signs2

		while j < chart.Chart.SIGN_NUM:
			x = cx+math.cos(i)*self.rSigns
			y = cy+math.sin(i)*self.rSigns
			self.draw.text((x-self.signSize/2, y-self.signSize/2), signs[j], font=self.fntMorinusSigns, fill=clr)
			i -= GraphChartPDs.DEG30
			j += 1


	def drawHouses(self, chouses, r1, r2):
		(cx, cy) = self.center.Get()
		clr = self.options.clrhouses
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		asc = self.chartRadix.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0 and self.options.hsys == 'W':
			asc = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC]-self.chartRadix.ayanamsha)
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			dif = math.radians(util.normalize(asc-chouses.cusps[i]))
			x1 = cx+math.cos(math.pi+dif)*r1
			y1 = cy+math.sin(math.pi+dif)*r1
			x2 = cx+math.cos(math.pi+dif)*r2
			y2 = cy+math.sin(math.pi+dif)*r2
			self.bdc.DrawLine(x1, y1, x2, y2)
	

	def drawAscMC(self, ascmc, r1, r2, rArrow, AscMConly=False):
		(cx, cy) = self.center.Get()
		#AscMC
		clr = self.options.clrAscMC
		if self.bw:
			clr = (0,0,0)
		w = self.options.ascmcsize
		if self.chartsize <= GraphChartPDs.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
			w = 2
		elif self.chartsize <= GraphChartPDs.MEDIUM_SIZE and (w == 5 or w == 4):
			w = 3

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)

		for i in range(4):
			if AscMConly and (i == 1 or i == 3):
				continue
			ang = math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC])
			if i == 0:
				ang -= math.radians(ascmc[houses.Houses.ASC])
			if i == 1:
				ang -= math.radians(ascmc[houses.Houses.ASC])+math.pi
			if i == 2:
				ang -= math.radians(ascmc[houses.Houses.MC])
			if i == 3:
				ang -= math.radians(ascmc[houses.Houses.MC])+math.pi

			x1 = cx+math.cos(ang)*r1
			y1 = cy+math.sin(ang)*r1
			x2 = cx+math.cos(ang)*r2
			y2 = cy+math.sin(ang)*r2
			self.bdc.DrawLine(x1, y1, x2, y2)

			if i == 0 or i == 2:
				self.drawArrow(ang, r2, clr, rArrow)


	def drawArrow(self, ang, r2, clr, rArrow):
		(cx, cy) = self.center.Get()
		offs = math.pi/360.0 

		xl = cx+math.cos(ang+offs)*r2
		yl = cy+math.sin(ang+offs)*r2
		xr = cx+math.cos(ang-offs)*r2
		yr = cy+math.sin(ang-offs)*r2
		xm = cx+math.cos(ang)*rArrow
		ym = cy+math.sin(ang)*rArrow

		li = ((xl, yl, xr, yr), (xr, yr, xm, ym), (xm, ym, xl, yl))
		self.bdc.DrawLineList(li)

#		self.bdc.SetBrush(wx.Brush(clr))	

#		x = (xl+xr)/2
#		x = (x+xm)/2
#		y = (yl+yr)/2
#		y = (y+ym)/2	

#		self.bdc.FloodFill(x, y, clr, wx.FLOOD_BORDER)


	def drawAscMCPos(self): #Not used
		(cx, cy) = self.center.Get()
		clrpos = self.options.clrpositions
		if self.bw:
			clrpos = (0,0,0)
		for i in range(2):
			lon = self.chart.houses.ascmc[i]
			if self.options.ayanamsha != 0:
				lon -= self.chartRadix.ayanamsha
				lon = util.normalize(lon)

			(d, m, s) = util.decToDeg(lon)
			d = d%chart.Chart.SIGN_DEG
#			d, m = util.roundDeg(d%chart.Chart.SIGN_DEG, m, s)
				
			wdeg, hdeg = self.draw.textsize(str(d), self.fntText)
			wmin, hmin = self.draw.textsize((str(m).zfill(2)), self.fntSmallText)
			x = cx+math.cos(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-self.chart.houses.ascmc[i]))*self.rPosAscMC
			y = cy+math.sin(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-self.chart.houses.ascmc[i]))*self.rPosAscMC
			xdeg = x-wdeg/2
			ydeg = y-hdeg/2
			self.draw.text((xdeg, ydeg), str(d), fill=clrpos, font=self.fntText)
			self.draw.text((xdeg+wdeg, ydeg), (str(m)).zfill(2), fill=clrpos, font=self.fntSmallText)


	def drawHousePos(self): #Not used
		(cx, cy) = self.center.Get()
		clrpos = self.options.clrpositions
		if self.bw:
			clrpos = (0,0,0)
		skipasc = False
		skipmc = False
		if self.chart.houses.cusps[1] == self.chart.houses.ascmc[houses.Houses.ASC]:
			skipasc = True
		if self.chart.houses.cusps[10] == self.chart.houses.ascmc[houses.Houses.MC]:
			skipmc = True

		asc = self.chart.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0 and self.options.hsys == 'W':
			asc = util.normalize(self.chart.houses.ascmc[houses.Houses.ASC]-self.chartRadix.ayanamsha)
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			if i >= 4 and i < 10:
				continue
			if (skipasc and i == 1) or (skipmc and i == 10):
				continue

			lon = self.chart.houses.cusps[i]
			if self.options.ayanamsha != 0 and self.options.hsys != 'W':
				lon -= self.chartRadix.ayanamsha
				lon = util.normalize(lon)
			(d, m, s) = util.decToDeg(lon)
			d = d%chart.Chart.SIGN_DEG
#			d, m = util.roundDeg(d%chart.Chart.SIGN_DEG, m, s)
				
			wdeg, hdeg = self.draw.textsize(str(d), self.fntText)
			wmin, hmin = self.draw.textsize((str(m).zfill(2)), self.fntSmallText)
			x = cx+math.cos(math.pi+math.radians(asc-self.chart.houses.cusps[i]))*self.rPosHouses
			y = cy+math.sin(math.pi+math.radians(asc-self.chart.houses.cusps[i]))*self.rPosHouses
			xdeg = x-wdeg/2
			ydeg = y-hdeg/2
			self.draw.text((xdeg, ydeg), str(d), fill=clrpos, font=self.fntText)
			self.draw.text((xdeg+wdeg, ydeg), (str(m)).zfill(2), fill=clrpos, font=self.fntSmallText)


	def drawHouseNames(self, chrt, rHouseNames):
		(cx, cy) = self.center.Get()
		clr = self.options.clrhousenumbers
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		asc = self.chartRadix.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0 and self.options.hsys == 'W':
			asc = util.normalize(self.chartRadix.houses.ascmc[houses.Houses.ASC]-self.chartRadix.ayanamsha)
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			width = 0.0
			if i != houses.Houses.HOUSE_NUM:
				width = chrt.houses.cusps[i+1]-chrt.houses.cusps[i]
			else:
				width = chrt.houses.cusps[1]-chrt.houses.cusps[houses.Houses.HOUSE_NUM]

			width = util.normalize(width)
			halfwidth = math.radians(width/2.0)
			dif = math.radians(util.normalize(asc-chrt.houses.cusps[i]))
			
			x = cx+math.cos(math.pi+dif-halfwidth)*rHouseNames
			y = cy+math.sin(math.pi+dif-halfwidth)*rHouseNames
			if i == 1 or i == 2:
				xoffs = 0
				yoffs = self.symbolSize/4
				if i == 2:
					xoffs = self.symbolSize/8
			else:
				xoffs = self.symbolSize/4
				yoffs = self.symbolSize/4

			self.draw.text((x-xoffs,y-yoffs), common.common.Housenames[i-1], fill=clr, font=self.fntText)
	

	def drawPlanets(self, chrt, pshift, rPlanet, rPosDeg, rPosMin, rRetr, reverse=True):
		(cx, cy) = self.center.Get()
		clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
		clrpos = self.options.clrpositions
		if self.bw:
			clrpos = (0,0,0)
		for i in range(planets.Planets.PLANETS_NUM+1):
			if (i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or ((i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not self.options.shownodes) or (i == planets.Planets.PLANETS_NUM and not self.options.showlof):
				continue
			lon = 0.0
			if i < planets.Planets.PLANETS_NUM:
				lon = chrt.planets.planets[i].data[planets.Planet.LONG]
			else:
				lon = chrt.fortune.fortune[fortune.Fortune.LON]

			x = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPlanet	
			y = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPlanet	
			
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					objidx = i
					if i >= planets.Planets.PLANETS_NUM-1:
						objidx -= 1
					clr = self.options.clrindividual[objidx]
				else:
					if i < planets.Planets.PLANETS_NUM:
						dign = chrt.dignity(i)
						clr = clrs[dign]
					else:
						clr = self.options.clrperegrin

			txtpl = ''
			if i < planets.Planets.PLANETS_NUM:
				txtpl = common.common.Planets[i]
			else:
				txtpl = common.common.fortune

			self.draw.text((x-self.symbolSize/2, y-self.symbolSize/2), txtpl, fill=clr, font=self.fntMorinus)

			#Position
			alon = lon
			if self.options.ayanamsha != 0:
				alon -= chrt.ayanamsha
				alon = util.normalize(alon)
			(d, m, s) = util.decToDeg(alon)
			d = d%chart.Chart.SIGN_DEG
#			d, m = util.roundDeg(d%chart.Chart.SIGN_DEG, m, s)
				
			degtxt = str(d).zfill(2)+self.deg_symbol
			wdeg, hdeg = self.draw.textsize(degtxt, self.fntText)
			x = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPosDeg
			y = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPosDeg
			xdeg = x-wdeg/2
			ydeg = y-hdeg/2
			self.draw.text((xdeg, ydeg), degtxt, fill=clr, font=self.fntText)

			mintxt = str(m).zfill(2)+"'"
			wdeg, hdeg = self.draw.textsize(mintxt, self.fntSmallText2)
			x = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPosMin
			y = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[i]))*rPosMin
			xdeg = x-wdeg/2
			ydeg = y-hdeg/2
			self.draw.text((xdeg, ydeg), (mintxt).zfill(2), fill=clr, font=self.fntSmallText2)

			#Retrograde
			if i < planets.Planets.PLANETS_NUM and chrt.planets.planets[i].data[planets.Planet.SPLON] <= 0.0:
				if chrt.planets.planets[i].data[planets.Planet.SPLON] == 0.0:
					t = 'S'
					rfnt = self.fntSmallText
				elif chrt.planets.planets[i].data[planets.Planet.SPLON] < 0.0:
					t = common.common.retr
					rfnt = self.fntRetr

				wdeg, hdeg = self.draw.textsize(t, rfnt)
				x = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-chrt.planets.planets[i].data[planets.Planet.LONG]-pshift[i]))*rRetr	
				y = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-chrt.planets.planets[i].data[planets.Planet.LONG]-pshift[i]))*rRetr
				xdeg = x-wdeg/2
				ydeg = y-hdeg/2

				self.draw.text((xdeg, ydeg), t, fill=clr, font=rfnt)


	def drawLines(self, deg, shift, r1, r2):
		(cx, cy) = self.center.Get()
		i = math.pi+math.radians(shift)
		while i>-math.pi+math.radians(shift):
			x1 = cx+math.cos(i)*r1
			y1 = cy+math.sin(i)*r1
			x2 = cx+math.cos(i)*r2
			y2 = cy+math.sin(i)*r2

			self.bdc.DrawLine(x1, y1, x2, y2)
			i -= deg


	def drawTermsLines(self): #Not used
		(cx, cy) = self.center.Get()
		asclon = self.chart.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)

		shift = math.radians(asclon)
		signdeg = float(chart.Chart.SIGN_DEG)
		num = len(self.options.terms[self.options.selterm])
		subnum = len(self.options.terms[self.options.selterm][0])
		sign = 0.0
		for i in range(num):
			deg = sign
			for j in range(subnum):
				deg += float(self.options.terms[self.options.selterm][i][j][1])

				x1 = cx+math.cos(math.pi+shift-math.radians(deg))*self.rTerms
				y1 = cy+math.sin(math.pi+shift-math.radians(deg))*self.rTerms
				x2 = cx+math.cos(math.pi+shift-math.radians(deg))*self.rDecans
				y2 = cy+math.sin(math.pi+shift-math.radians(deg))*self.rDecans

				self.bdc.DrawLine(x1, y1, x2, y2)

			sign += signdeg


	def drawTerms(self): #Not used
		(cx, cy) = self.center.Get()
		clr = (0,0,0)
		if not self.bw:
			clr = self.options.clrsigns

		asclon = self.chart.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)
		shift = math.radians(asclon)
		signdeg = float(chart.Chart.SIGN_DEG)
		num = len(self.options.terms[self.options.selterm])
		subnum = len(self.options.terms[self.options.selterm][0])
		sign = 0.0
		for i in range(num):
			deg = sign
			for j in range(subnum):
				pldeg = deg+float(self.options.terms[self.options.selterm][i][j][1])/2.0
				deg += float(self.options.terms[self.options.selterm][i][j][1])

				x = cx+math.cos(math.pi+shift-math.radians(pldeg))*self.rTermsPlanet
				y = cy+math.sin(math.pi+shift-math.radians(pldeg))*self.rTermsPlanet

				self.draw.text((x-self.smallsymbolSize/2, y-self.smallsymbolSize/2), common.common.Planets[self.options.terms[self.options.selterm][i][j][0]], fill=clr, font=self.fntSmallMorinus)

			sign += signdeg


	def drawDecansLines(self): #Not used
		(cx, cy) = self.center.Get()

		asclon = self.chart.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)

		shift = asclon
		deg = GraphChartPDs.DEG10
		i = math.pi+math.radians(shift)
		while i>-math.pi+math.radians(shift):
			x1 = cx+math.cos(i)*self.rInner
			y1 = cy+math.sin(i)*self.rInner
			x2 = cx+math.cos(i)*self.rDecans
			y2 = cy+math.sin(i)*self.rDecans

			self.bdc.DrawLine(x1, y1, x2, y2)
			i -= deg


	def drawDecans(self): #Not used
		(cx, cy) = self.center.Get()
		clr = (0,0,0)
		if not self.bw:
			clr = self.options.clrsigns

		asclon = self.chart.houses.ascmc[houses.Houses.ASC]
		if self.options.ayanamsha != 0:
			asclon -= self.chartRadix.ayanamsha
			asclon = util.normalize(asclon)

		shift = math.radians(asclon)
		num = len(self.options.decans[self.options.seldecan])
		subnum = len(self.options.decans[self.options.seldecan][0])
		deg = 5.0
		for i in range(num):
			for j in range(subnum):
				x = cx+math.cos(math.pi+shift-math.radians(deg))*self.rDecansPlanet
				y = cy+math.sin(math.pi+shift-math.radians(deg))*self.rDecansPlanet

				self.draw.text((x-self.smallsymbolSize/2, y-self.smallsymbolSize/2), common.common.Planets[self.options.decans[self.options.seldecan][i][j]], fill=clr, font=self.fntSmallMorinus)

				deg += 10.0


	def drawPlanetLines(self, pshift, pls, frtn, r0, rl1):
		clr = (0,0,0)
		if not self.bw:
			clr = self.options.clrframe
		w = 2
		if self.chartsize <= GraphChartPDs.MEDIUM_SIZE:
			w = 1

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		for i in range (planets.Planets.PLANETS_NUM+1):
			if (i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or ((i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not self.options.shownodes) or (i == planets.Planets.PLANETS_NUM and not self.options.showlof):
				continue
			self.drawPlanetLine(i, r0, rl1, pls, frtn, pshift)


	def drawPlanetLine(self, planet, r1, r2, pls, frtn, pshift):
		(cx, cy) = self.center.Get()

		lon = 0.0
		if planet < planets.Planets.PLANETS_NUM:
			lon = pls[planet].data[planets.Planet.LONG]
		else:
			lon = frtn[fortune.Fortune.LON]

		x1 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon))*r1
		y1 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon))*r1
		x2 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[planet]))*r2
		y2 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-lon-pshift[planet]))*r2
		self.bdc.DrawLine(x1, y1, x2, y2)


	def arrange(self, plnts, frtn, rPlanet):
		'''Arranges planets so they won't overlap each other'''

		pls = []
		pshift = []
		order = []
		mixed = []

		for i in range (planets.Planets.PLANETS_NUM+1):
			pls.append(0.0)
			pshift.append(0.0)
			order.append(0)
			mixed.append(0)

		pnum = 0
		for i in range (planets.Planets.PLANETS_NUM+1):
			if i < planets.Planets.PLANETS_NUM:
				pls[pnum] = plnts[i].data[planets.Planet.LONG]
			else:
				pls[pnum] = frtn[fortune.Fortune.LON]

			if (i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or ((i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not self.options.shownodes) or (i == planets.Planets.PLANETS_NUM and not self.options.showlof):
				continue
			mixed[pnum] = i
			pnum += 1

		#arrange in order, initialize
		for i in range(pnum):
			order[i] = pls[i]
			
		for j in range(pnum):
			for i in range(pnum-1):
				if (order[i] > order[i+1]):
					tmp = order[i]
					order[i] = order[i+1]
					order[i+1] = tmp
					tmp = mixed[i]
					mixed[i] = mixed[i+1]
					mixed[i+1] = tmp
		
		#doArrange arranges consecutive two planets only(0 and 1, 1 and 2, ...), this is why we need to do it pnum+1 times
		for i in range(pnum+1):
			self.doArrange(pnum, pshift, order, mixed, rPlanet)

		#Arrange 360-0 transition also
		#We only shift forward at 360-0
		shifted = self.doShift(pnum-1, 0, pshift, order, mixed, rPlanet, True)

 		if shifted:
			for i in range(pnum):
				self.doArrange(pnum, pshift, order, mixed, rPlanet, True)

		#check if beyond (not overlapping but beyond)
		else:
			if order[pnum-1] > 300.0 and order[0] < 60.0:
				lon1 = order[pnum-1]+pshift[mixed[pnum-1]]
				lon2 = order[0]+360.0+pshift[mixed[0]]

				if lon1 > lon2:
					dist = lon1-lon2
					pshift[mixed[0]] += dist
					self.doShift(pnum-1, 0, pshift, order, mixed, rPlanet, True)

					for i in range(pnum-1):
						lon1 = order[i]+pshift[mixed[i]]
						lon2 = order[i+1]+pshift[mixed[i+1]]	
						if lon1 < 180.0 and lon2 < 180.0:
							if lon1 > lon2:
								dist = lon1-lon2
								pshift[mixed[i+1]] += dist
								self.doShift(i, i+1, pshift, order, mixed, rPlanet, True)
							else:
								break
						else:
							break

					for i in range(pnum):
						self.doArrange(pnum, pshift, order, mixed, rPlanet, True)

		return pshift[:]


	def doArrange(self, pnum, pshift, order, mixed, rPlanet, forward = False):
		shifted = False

		for i in range(pnum-1):
			shifted = self.doShift(i, i+1, pshift, order, mixed, rPlanet, forward)

		if shifted:
			self.doArrange(pnum, pshift, order, mixed, rPlanet, forward)


	def doShift(self, p1, p2, pshift, order, mixed, rPlanet, forward = False):
		(cx, cy) = self.center.Get()
		shifted = False

		x1 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
		y1 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
		x2 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet
		y2 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet

		w1, h1 = 0.0, 0.0
		if mixed[p1] < planets.Planets.PLANETS_NUM:
			w1, h1 = self.fntMorinus.getsize(common.common.Planets[mixed[p1]])
		else:
			w1, h1 = self.fntMorinus.getsize(common.common.fortune)
		w2, h2 = 0.0, 0.0
		if mixed[p2] < planets.Planets.PLANETS_NUM:
			w2, h2 = self.fntMorinus.getsize(common.common.Planets[mixed[p2]])
		else:
			w2, h2 = self.fntMorinus.getsize(common.common.fortune)

		while (self.overlap(x1, y1, w1, h1, x2, y2, w2, h2)):
			if not forward:
				pshift[mixed[p1]] -= 0.1
			pshift[mixed[p2]] += 0.1

			x1 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
			y1 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
			x2 = cx+math.cos(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet
			y2 = cy+math.sin(math.pi+math.radians(self.chartRadix.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet

			if not shifted:
				shifted = True

		return shifted


	def overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
		xoverlap = (x1 <= x2 and x2 <= x1+w1) or (x2 <= x1 and x1 <= x2+w2)
		yoverlap = (y1 <= y2 and y2 <= y1+h1) or (y2 <= y1 and y1 <= y2+h2)

		if (xoverlap and yoverlap):
			return True

		return False


