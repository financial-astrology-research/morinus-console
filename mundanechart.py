import wx
import Image, ImageDraw, ImageFont
import math
import astrology
import chart, houses, planets, fortune
import placspec
import regiospec
import primdirs
import options
import common
import util
import mtexts


class MundaneChart:

	DEG1 = math.pi/180
	DEG5 = math.pi/36
	DEG10 = math.pi/18
	DEG30 = math.pi/6

	SMALL_SIZE = 400
	MEDIUM_SIZE = 600

	def __init__(self, chrt, size, opts, bw, planetaryday=True, chrt2 = None):
		self.chart = chrt
		self.chart2 = chrt2
		self.w, self.h = size
		self.options = opts
		self.bw = bw
		self.planetaryday = planetaryday #i.e. radix
		self.buffer = wx.EmptyBitmap(self.w, self.h)
		self.bdc = wx.BufferedDC(None, self.buffer)
		self.chartsize = min(self.w, self.h)
		self.maxradius = self.chartsize/2
		self.center = wx.Point(self.w/2, self.h/2)

		self.arrowlen = 0.04
		self.deg01510len = 0.01
		self.retrdiff = 0.01
		if self.chart2 == None:
			self.symbolSize = self.maxradius/12
			self.houseSize = self.maxradius/12
			self.planetsectorlen = 0.18
			self.housesectorlen = self.planetsectorlen
			self.planetoffs = (self.planetsectorlen/2.0)*self.maxradius
			self.planetlinelen = 0.03
			self.r30 = self.maxradius*0.96
			self.houseoffs = (self.housesectorlen/2.0-0.01)*self.maxradius
			self.rHouse = self.r30-self.houseoffs
			self.rASCMC = self.maxradius*0.88
			self.rArrow = self.rASCMC+self.arrowlen*self.maxradius
			self.r0 = self.r30-self.housesectorlen*self.maxradius
			self.r1 = self.r0+self.deg01510len*self.maxradius
			self.r5 = self.r1+self.deg01510len*self.maxradius
			self.r10 = self.r5+self.deg01510len*self.maxradius

			self.rInner = self.r0

			self.rLLine = self.rInner-self.planetlinelen*self.maxradius #line between zodiacpos & planet
			self.rPlanet = self.rInner-self.planetoffs
			self.rAsp = self.rInner-self.planetsectorlen*self.maxradius
			self.rLLine2 = self.rAsp+self.planetlinelen*self.maxradius
			self.rRetr = self.rLLine2+self.maxradius*self.retrdiff

			pos = 0.55
			aspascmc = 0.50
			posascmc = 0.50
			poshouses = 0.40				

			self.rPos = self.maxradius*pos
			self.rAspAscMC = self.maxradius*aspascmc
			self.rPosAscMC = self.maxradius*posascmc
			self.rPosHouses = self.maxradius*poshouses
			self.rBase = self.maxradius*0.2
		else:
			self.symbolSize = self.maxradius/16
			self.houseSize = self.maxradius/20
			self.outerplanetsectorlen = 0.12
			self.planetsectorlen = 0.15
			self.housesectorlen = self.planetsectorlen
			self.houseoffs = (self.housesectorlen/2.0)*self.maxradius
			self.planetoffs = (self.planetsectorlen/2.0)*self.maxradius
			self.planetlinelen = 0.03
			self.rHousesectorlen = 0.06
			self.rOuterMax = self.maxradius*0.97
			if self.options.houses:
				self.rOuterHouseName = self.rOuterMax-(self.rHousesectorlen*self.maxradius)/2.0
				self.rOuterHouse = self.rOuterMax-self.rHousesectorlen*self.maxradius
				self.r30 = self.rOuterHouse-self.outerplanetsectorlen*self.maxradius
			else:
				self.r30 = self.rOuterMax-self.outerplanetsectorlen*self.maxradius
				self.rOuterASCMC = self.maxradius*0.92

			self.rOuterPlanet = self.r30+self.planetoffs
			self.rOuterASCMC = self.maxradius*0.92
			self.rOuterArrow = self.rOuterASCMC+self.arrowlen*self.maxradius
			self.rOuterLine = self.r30+self.planetlinelen*self.maxradius
			self.rOuterRetr = self.rOuterLine+self.maxradius*self.retrdiff
			self.rOuter0 = self.r30
			self.rOuter1 = self.rOuter0-self.deg01510len*self.maxradius
			self.rOuter5 = self.rOuter1-self.deg01510len*self.maxradius
			self.rOuter10 = self.rOuter5-self.deg01510len*self.maxradius
			self.rOuterMin = self.maxradius*0.78
			self.rHouse = self.r30-self.houseoffs
			self.r0 = self.r30-self.housesectorlen*self.maxradius
			self.r1 = self.r0+self.deg01510len*self.maxradius
			self.r5 = self.r1+self.deg01510len*self.maxradius
			self.r10 = self.r5+self.deg01510len*self.maxradius
			self.rASCMC = self.maxradius*0.88
			self.rArrow = self.rASCMC+self.arrowlen*self.maxradius

			self.rInner = self.r0

			self.rLLine = self.rInner-self.planetlinelen*self.maxradius #line between zodiacpos & planet
			self.rPlanet = self.rInner-self.planetoffs
			self.rAsp = self.rInner-self.planetsectorlen*self.maxradius
			self.rLLine2 = self.rAsp+self.planetlinelen*self.maxradius
			self.rRetr = self.rLLine2+self.maxradius*self.retrdiff

			pos = 0.45
			aspascmc = 0.41
			posascmc = 0.41
			poshouses = 0.32				

			self.rPos = self.maxradius*pos
			self.rAspAscMC = self.maxradius*aspascmc
			self.rPosAscMC = self.maxradius*posascmc
			self.rPosHouses = self.maxradius*poshouses
			self.rBase = self.maxradius*0.11

		self.smallsymbolSize = 2*self.symbolSize/3

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.symbolSize)
		self.fntSmallMorinus = ImageFont.truetype(common.common.symbols, self.smallsymbolSize)
		self.fntAspects = ImageFont.truetype(common.common.symbols, self.symbolSize/2)
		self.fntText = ImageFont.truetype(common.common.abc, self.symbolSize/2)
		self.fntSmallText = ImageFont.truetype(common.common.abc, self.symbolSize/4)
		self.fntBigText = ImageFont.truetype(common.common.abc, self.symbolSize)
		self.fntMorinus2 = ImageFont.truetype(common.common.symbols, self.symbolSize/4*3)
		self.deg_symbol = u'\u00b0'


	def drawChart(self):
		# PIL can draw only 1-width ellipse (or is there a width=...?)
		self.drawCircles()

#		if self.options.houses:
		self.drawHouses(self.chart.houses, self.rBase, self.rInner)

		#Convert to PIL (truetype-font is not supported in wxPython)
		wxImag = self.buffer.ConvertToImage()
		self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
		self.img.fromstring(wxImag.GetData())
		self.draw = ImageDraw.Draw(self.img)

		self.drawHouseNames(self.rHouse)

		#Convert back from PIL
		wxImg = wx.EmptyImage(self.img.size[0], self.img.size[1])
		wxImg.SetData(self.img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)
		self.bdc = wx.BufferedDC(None, self.buffer)

		self.drawAscMC(self.rBase, self.rASCMC, self.rArrow)

		#calc shift of planets (in order to avoid overlapping)
		self.pshift = self.arrange(self.chart.planets.planets, self.chart.fortune, self.rPlanet)
		#PIL doesn't want to show short lines
		self.drawPlanetLines(self.pshift, self.chart.planets.planets, self.chart.fortune, self.rInner, self.rLLine, self.rAsp, self.rLLine2)
		if self.chart2 != None:
			self.pshift2 = self.arrange(self.chart2.planets.planets, self.chart2.fortune, self.rOuterPlanet)
			self.drawPlanetLines(self.pshift2, self.chart2.planets.planets, self.chart2.fortune, self.r30, self.rOuterLine)

		#Convert to PIL (truetype-font is not supported in wxPython)
		wxImag = self.buffer.ConvertToImage()
		self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
		self.img.fromstring(wxImag.GetData())
		self.draw = ImageDraw.Draw(self.img)

		self.drawPlanets(self.chart, self.pshift, self.rPlanet, self.rRetr)
		if self.chart2 != None:
			self.drawPlanets(self.chart2, self.pshift2, self.rOuterPlanet, self.rOuterRetr, True)

#		if self.options.positions:
#			self.drawAscMCPos()

		wxImg = wx.EmptyImage(self.img.size[0], self.img.size[1])
		wxImg.SetData(self.img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)

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

		#r30 circle
		if self.chart2 != None:
			clr = self.options.clrframe
			if self.bw:
				clr = (0,0,0)

			w = 3
			if self.chartsize <= MundaneChart.SMALL_SIZE:
				w = 1
			elif self.chartsize <= MundaneChart.MEDIUM_SIZE:
				w = 2

			pen = wx.Pen(clr, w)
			self.bdc.SetPen(pen)
			self.bdc.DrawCircle(cx, cy, self.r30)

			#Outer 10, 5, 1-circle
			pen = wx.Pen(clr, 1)
			self.bdc.SetPen(pen)
			self.bdc.DrawCircle(cx, cy, self.rOuter10)

		#r10 Circle
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.r10)

		#r0 Circle
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)

		w = 3
		if self.chartsize <= MundaneChart.SMALL_SIZE:
			w = 1
		elif self.chartsize <= MundaneChart.MEDIUM_SIZE:
			w = 2

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rInner)

		#rAsp Circle
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rAsp)

		#rHouse Circle
#		if self.options.houses:
#			clr = self.options.clrhouses
#			if self.bw:
#				clr = (0,0,0)
#			pen = wx.Pen(clr, 1)
#			self.bdc.SetPen(pen)
#			self.bdc.DrawCircle(cx, cy, self.rHouse)

		#Base Circle
		clr = self.options.clrAscMC
		if self.bw:
			clr = (0,0,0)

		w = self.options.ascmcsize
		if self.chartsize <= MundaneChart.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
			w = 2
		elif self.chartsize <= MundaneChart.MEDIUM_SIZE and (w == 5 or w == 4):
			w = 3

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.bdc.DrawCircle(cx, cy, self.rBase)

		asclon = self.chart.houses.ascmc[houses.Houses.ASC]

#		#30-degs
#		clr = self.options.clrframe
#		if self.bw:
#			clr = (0,0,0)
#		w = 3
#		if self.chartsize <= MundaneChart.SMALL_SIZE:
#			w = 1
#		elif self.chartsize <= MundaneChart.MEDIUM_SIZE:
#			w = 2

#		pen = wx.Pen(clr, w)
#		self.bdc.SetPen(pen)
#		self.drawLines(MundaneChart.DEG30, 0.0, self.rInner, self.r30)

		#10-degs
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		w = 2
		if self.chartsize <= MundaneChart.MEDIUM_SIZE:
			w = 1

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.drawLines(MundaneChart.DEG10, 0.0, self.r0, self.r10)

		#5-degs
		self.drawLines(MundaneChart.DEG5, 0.0, self.r0, self.r5)
		#1-degs
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)
		self.drawLines(MundaneChart.DEG1, 0.0, self.r0, self.r1)

		#Outer 10, 5, 1 -degs
		if self.chart2 != None:
			#10-degs
			clr = self.options.clrframe
			if self.bw:
				clr = (0,0,0)
			w = 2
			if self.chartsize <= MundaneChart.MEDIUM_SIZE:
				w = 1

			pen = wx.Pen(clr, w)
			self.bdc.SetPen(pen)
			self.drawLines(MundaneChart.DEG10, 0.0, self.rOuter0, self.rOuter10)

			#5-degs
			self.drawLines(MundaneChart.DEG5, 0.0, self.rOuter0, self.rOuter5)
			#1-degs
			clr = self.options.clrframe
			if self.bw:
				clr = (0,0,0)
			pen = wx.Pen(clr, 1)
			self.bdc.SetPen(pen)
			self.drawLines(MundaneChart.DEG1, 0.0, self.rOuter0, self.rOuter1)

		self.bdc.EndDrawing()


	def drawHouseNames(self, rHousenames):
		(cx, cy) = self.center.Get()
		clr = self.options.clrhousenumbers
		if self.bw:
			clr = (0,0,0)
#		asclon = self.chart.houses.ascmc[houses.Houses.ASC]

		offs = math.pi-MundaneChart.DEG30/2
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			x = cx+math.cos(offs)*rHousenames
			y = cy+math.sin(offs)*rHousenames
			self.draw.text((x-self.houseSize/2, y-self.houseSize/2), common.common.Housenames[i-1], font=self.fntBigText, fill=clr)
			offs -= MundaneChart.DEG30


	def drawHouses(self, chouses, r1, r2):
		(cx, cy) = self.center.Get()
		clr = self.options.clrhouses
		if self.bw:
			clr = (0,0,0)
		pen = wx.Pen(clr, 1)
		self.bdc.SetPen(pen)

		offs = math.pi
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			x1 = cx+math.cos(offs)*r1
			y1 = cy+math.sin(offs)*r1
			x2 = cx+math.cos(offs)*r2
			y2 = cy+math.sin(offs)*r2
			self.bdc.DrawLine(x1, y1, x2, y2)
			offs -= MundaneChart.DEG30

		#30-degs
		clr = self.options.clrframe
		if self.bw:
			clr = (0,0,0)
		w = 3
		if self.chartsize <= MundaneChart.SMALL_SIZE:
			w = 1
		elif self.chartsize <= MundaneChart.MEDIUM_SIZE:
			w = 2

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		self.drawLines(MundaneChart.DEG30, 0.0, self.rInner, self.r30)


	def drawAscMC(self, r1, r2, rArrow):
		(cx, cy) = self.center.Get()
		clr = self.options.clrAscMC
		if self.bw:
			clr = (0,0,0)
		w = self.options.ascmcsize
		if self.chartsize <= MundaneChart.SMALL_SIZE and (w == 5 or w == 4 or w == 3):
			w = 2
		elif self.chartsize <= MundaneChart.MEDIUM_SIZE and (w == 5 or w == 4):
			w = 3

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)

		offs = math.pi
		for i in range(4):
			x1 = cx+math.cos(offs)*r1
			y1 = cy+math.sin(offs)*r1
			x2 = cx+math.cos(offs)*r2
			y2 = cy+math.sin(offs)*r2
			self.bdc.DrawLine(x1, y1, x2, y2)
			offs -= 3*MundaneChart.DEG30

			if i == 2 or i == 3:
				self.drawArrow(offs, r2, clr, rArrow)


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


#	def drawAscMCPos(self):
#		(cx, cy) = self.center.Get()
#		clrpos = self.options.clrpositions
#		if self.bw:
#			clrpos = (0,0,0)

#		xmps = (0.0, 90.0, 180.0, 270.0)
#		offs = math.pi
#		for i in range(4):
#			x = cx+math.cos(offs)*self.rPosAscMC
#			y = cy+math.sin(offs)*self.rPosAscMC

#			d, m, s = util.decToDeg(lon)
#			wdeg, hdeg = self.draw.textsize(str(d), self.fntText)
#			wmin, hmin = self.draw.textsize((str(m).zfill(2)), self.fntSmallText)

#			xdeg = x-wdeg/2
#			ydeg = y-hdeg/2
#			self.draw.text((xdeg, ydeg), str(d), fill=clrpos, font=self.fntText)
#			self.draw.text((xdeg+wdeg, ydeg), (str(m)).zfill(2), fill=clrpos, font=self.fntSmallText)

#			offs -= 3*MundaneChart.DEG30


	def drawPlanets(self, chrt, pshift, rPlanet, rRetr, outer=False):
		(cx, cy) = self.center.Get()
		clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
		clrpos = self.options.clrpositions
		if self.bw:
			clrpos = (0,0,0)
		for i in range(planets.Planets.PLANETS_NUM+1):
			if (i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or ((i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not self.options.shownodes) or (i == planets.Planets.PLANETS_NUM and not self.options.showlof):
				continue

			xmp = 0.0
			if i < planets.Planets.PLANETS_NUM:
				if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
					xmp = chrt.planets.planets[i].speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
					xmp = chrt.planets.planets[i].speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
					xmp = chrt.planets.planets[i].speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP]
			else:
				if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
					xmp = chrt.fortune.speculum.speculum[placspec.PlacidianSpeculum.PMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
					xmp = chrt.fortune.speculum2.speculum[regiospec.RegiomontanianSpeculum.RMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
					xmp = chrt.fortune.speculum2.speculum[regiospec.RegiomontanianSpeculum.CMP]

			x = cx+math.cos(math.pi+math.radians(-xmp-pshift[i]))*rPlanet
			y = cy+math.sin(math.pi+math.radians(-xmp-pshift[i]))*rPlanet
			
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

			#Retrograde
			if i < planets.Planets.PLANETS_NUM:
				if chrt.planets.planets[i].data[planets.Planet.SPLON] <= 0.0:
					t = 'S'
					if chrt.planets.planets[i].data[planets.Planet.SPLON] < 0.0:
						t = 'R'

					x = cx+math.cos(math.pi+math.radians(-xmp-pshift[i]))*rRetr	
					y = cy+math.sin(math.pi+math.radians(-xmp-pshift[i]))*rRetr

					self.draw.text((x-self.symbolSize/8, y-self.symbolSize/8), t, fill=clr, font=self.fntSmallText)

			if not outer:
				#Position
				if self.options.positions:
					(d, m, s) = util.decToDeg(xmp)
#					d = d%chart.Chart.SIGN_DEG
#					d, m = util.roundDeg(d%chart.Chart.SIGN_DEG, m, s)
				
					wdeg, hdeg = self.draw.textsize(str(d), self.fntText)
					wmin, hmin = self.draw.textsize((str(m).zfill(2)), self.fntSmallText)
					x = cx+math.cos(math.pi+math.radians(-xmp-pshift[i]))*self.rPos
					y = cy+math.sin(math.pi+math.radians(-xmp-pshift[i]))*self.rPos	
					xdeg = x-wdeg/2
					ydeg = y-hdeg/2
					self.draw.text((xdeg, ydeg), str(d), fill=clrpos, font=self.fntText)
					self.draw.text((xdeg+wdeg, ydeg), (str(m)).zfill(2), fill=clrpos, font=self.fntSmallText)


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


	def drawPlanetLines(self, pshift, pls, frtn, r0, rl1, r02=None, rl2=None):
		clr = (0,0,0)
		if not self.bw:
			clr = self.options.clrframe
		w = 2
		if self.chartsize <= MundaneChart.MEDIUM_SIZE:
			w = 1

		pen = wx.Pen(clr, w)
		self.bdc.SetPen(pen)
		for i in range (planets.Planets.PLANETS_NUM+1):
			if (i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or ((i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not self.options.shownodes) or (i == planets.Planets.PLANETS_NUM and not self.options.showlof):
				continue
			self.drawPlanetLine(i, r0, rl1, pls, frtn, pshift)
			if r02 != None:
				self.drawPlanetLine(i, r02, rl2, pls, frtn, pshift)


	def drawPlanetLine(self, planet, r1, r2, pls, frtn, pshift):
		(cx, cy) = self.center.Get()

		xmp = 0.0
		if planet < planets.Planets.PLANETS_NUM:
			if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
				xmp = pls[planet].speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP]
			elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
				xmp = pls[planet].speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP]
			elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
				xmp = pls[planet].speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP]
		else:
			if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
				xmp = frtn.speculum.speculum[placspec.PlacidianSpeculum.PMP]
			elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
				xmp = frtn.speculum2.speculum[regiospec.RegiomontanianSpeculum.RMP]
			elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
				xmp = frtn.speculum2.speculum[regiospec.RegiomontanianSpeculum.CMP]

		x1 = cx+math.cos(math.pi+math.radians(-xmp))*r1
		y1 = cy+math.sin(math.pi+math.radians(-xmp))*r1
		x2 = cx+math.cos(math.pi+math.radians(-xmp-pshift[planet]))*r2
		y2 = cy+math.sin(math.pi+math.radians(-xmp-pshift[planet]))*r2
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
				if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
					pls[pnum] = plnts[i].speculums[chart.Chart.PLACIDIAN][planets.Planet.PMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
					pls[pnum] = plnts[i].speculums[chart.Chart.REGIOMONTAN][planets.Planet.RMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
					pls[pnum] = plnts[i].speculums[chart.Chart.REGIOMONTAN][planets.Planet.CMP]
			else:
				if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
					pls[pnum] = frtn.speculum.speculum[placspec.PlacidianSpeculum.PMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
					pls[pnum] = frtn.speculum2.speculum[regiospec.RegiomontanianSpeculum.RMP]
				elif self.chart.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
					pls[pnum] = frtn.speculum2.speculum[regiospec.RegiomontanianSpeculum.CMP]

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

		x1 = cx+math.cos(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
		y1 = cy+math.sin(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
		x2 = cx+math.cos(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet
		y2 = cy+math.sin(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet

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

			x1 = cx+math.cos(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
			y1 = cy+math.sin(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p1]-pshift[mixed[p1]]))*rPlanet
			x2 = cx+math.cos(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet
			y2 = cy+math.sin(math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC]-order[p2]-pshift[mixed[p2]]))*rPlanet

			if not shifted:
				shifted = True

		return shifted


	def overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
		xoverlap = (x1 <= x2 and x2 <= x1+w1) or (x2 <= x1 and x1 <= x2+w2)
		yoverlap = (y1 <= y2 and y2 <= y1+h1) or (y2 <= y1 and y1 <= y2+h2)

		if (xoverlap and yoverlap):
			return True

		return False


