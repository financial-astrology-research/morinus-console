import wx
import os
import astrology
import chart
import houses
import planets
import fortune
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class StripWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.chart = chrt
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		BOR = commonwnd.CommonWnd.BORDER
		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!

		self.BSPACE = self.FONT_SIZE/5
		self.YPLANETS_OFFS = self.FONT_SIZE/2-self.FONT_SIZE/10
		self.LINE_LENGTH = self.FONT_SIZE/2+self.FONT_SIZE/5
		self.LONGTIC = (2*self.FONT_SIZE)/3
		self.TIC5 = self.FONT_SIZE/2+self.FONT_SIZE/5
		self.TIC = self.FONT_SIZE/2-self.FONT_SIZE/10
		self.TICSTEP = (4*self.FONT_SIZE)/3
		self.DEG_OFFS = self.FONT_SIZE/5

		self.YOFFS = self.FONT_SIZE+self.YPLANETS_OFFS+self.LINE_LENGTH
		self.TABLE_HEIGHT = (self.LONGTIC+self.DEG_OFFS+self.FONT_SIZE+self.YOFFS)
		self.TABLE_WIDTH = chart.Chart.SIGN_DEG*self.TICSTEP
	
		self.WIDTH = (BOR+self.TABLE_WIDTH+BOR)
		self.HEIGHT = (BOR+self.TABLE_HEIGHT+BOR)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
#		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.deg_symbol = u'\u00b0'

		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Strip']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		#line and tics
		x = BOR
		y = BOR+self.YOFFS
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		draw.line((x, y-self.LONGTIC, x, y+self.LONGTIC), fill=tableclr)
		x = BOR+self.TABLE_WIDTH
		draw.line((x, y-self.LONGTIC, x, y+self.LONGTIC), fill=tableclr)

		x = BOR
		y = BOR+self.YOFFS
		for i in range(chart.Chart.SIGN_DEG):
			if i == 0:
				continue

			offs = self.TIC
			if i % 5 == 0:
				offs = self.TIC5
			draw.line((x+i*self.TICSTEP, y, x+i*self.TICSTEP, y+offs), fill=tableclr)

		x = BOR
		y = BOR+self.YOFFS+self.LONGTIC+self.DEG_OFFS
		offs = 0
		for i in range(chart.Chart.SIGN_DEG+1):
			if i == 0 or i % 5 == 0:
				txt = str(i)
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+offs-w/2, y), txt, fill=txtclr, font=self.fntText)

			offs += self.TICSTEP

		self.ascmctxt = (mtexts.txts['StripAsc'], mtexts.txts['StripMC'])
		bodies, bshift, ids = self.arrange()

		#bodies

		x = BOR
		y = BOR
		num = len(bodies)
		for i in range(num):
			lon, w, h, txt, fnt = 0.0, 0.0, 0.0, self.ascmctxt[0], self.fntMorinus
			clr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					if ids[i] <= astrology.SE_MEAN_NODE+1:
						clr = self.options.clrindividual[ids[i]]
				else:
					if ids[i] < astrology.SE_MEAN_NODE+1:
						dign = self.chart.dignity(ids[i])
						clr = self.clrs[dign]
					elif ids[i] == astrology.SE_MEAN_NODE+1:
						clr = self.options.clrperegrin
			tidx = planets.Planets.PLANETS_NUM-1
			if ids[i] < tidx:
				lon = self.chart.planets.planets[ids[i]].data[planets.Planet.LONG]
				txt = common.common.Planets[ids[i]]
				fnt = self.fntMorinus
			elif ids[i] == tidx:
				lon = self.chart.fortune.fortune[fortune.Fortune.LON]
				txt = common.common.fortune
				fnt = self.fntMorinus
			elif ids[i] == tidx+1:
				lon = self.chart.houses.ascmc[0]
				txt = self.ascmctxt[0]
				fnt = self.fntText
			elif ids[i] == tidx+2:
				lon = self.chart.houses.ascmc[1]
				txt = self.ascmctxt[1]
				fnt = self.fntText

			if self.options.ayanamsha != 0:
				lon -= self.chart.ayanamsha
				lon = util.normalize(lon)

			lon %= float(chart.Chart.SIGN_DEG)
			pos = lon*self.TICSTEP
			w, h = draw.textsize(txt, fnt)
			draw.text((x+pos-w/2+bshift[i], y), txt, fill=clr, font=fnt)
			draw.line((x+pos, y+self.YOFFS, x+pos+bshift[i], y+self.FONT_SIZE+self.YPLANETS_OFFS), fill=clr)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def arrange(self):
		'''Arranges bodies so they won't overlap each other'''

		bodies = []
		bshift = []
		order = []
		mixed = []

#		num = planets.Planets.PLANETS_NUM-1+1+2#Planets-DescNode+LoF+AscMC

		for i in range(planets.Planets.PLANETS_NUM-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			lona = self.chart.planets.planets[i].data[planets.Planet.LONG]
			if self.options.ayanamsha != 0:
				lona -= self.chart.ayanamsha
				lona = util.normalize(lona)

			bodies.append((lona%float(chart.Chart.SIGN_DEG))*self.TICSTEP)
			mixed.append(i)

		idx = planets.Planets.PLANETS_NUM-1
		if not self.options.intables or (self.options.intables and self.options.showlof):
			lona = self.chart.fortune.fortune[fortune.Fortune.LON]
			if self.options.ayanamsha != 0:
				lona -= self.chart.ayanamsha
				lona = util.normalize(lona)
			bodies.append((lona%float(chart.Chart.SIGN_DEG))*self.TICSTEP)
			mixed.append(idx)

		idx += 1
		for i in range(houses.Houses.MC+1):
			lona = self.chart.houses.ascmc[i]
			if self.options.ayanamsha != 0:
				lona -= self.chart.ayanamsha
				lona = util.normalize(lona)
			bodies.append((lona%float(chart.Chart.SIGN_DEG))*self.TICSTEP)
			mixed.append(idx)
			idx += 1

		length = len(bodies)
		#arrange in order, initialize
		for i in range(length):
			order.append(bodies[i])
			bshift.append(0.0)
			
		for j in range(length):
			for i in range(length-1):
				if (order[i] > order[i+1]):
					tmp = order[i]
					order[i] = order[i+1]
					order[i+1] = tmp
					tmp = mixed[i]
					mixed[i] = mixed[i+1]
					mixed[i+1] = tmp
		
		#doArrange arranges consecutive two planets only(0 and 1, 1 and 2, ...), this is why we need to do it length+1 times
		for i in range(length+1):
			self.doArrange(length, bshift, order, mixed)

		#Arrange borders
		BOR = commonwnd.CommonWnd.BORDER/2
		#Left
		if order[0]+bshift[0] < BOR:
			diff = BOR-(order[0]+bshift[0])
			bshift[0] += diff

			#check the other bodies
			for i in range(len(order)-1):
				w1, h1 = 0.0, 0.0
				tidx = planets.Planets.PLANETS_NUM-1
				if i < tidx:
					w1, h1 = self.fntMorinus.getsize(common.common.Planets[i])
				elif i == tidx:
					w1, h1 = self.fntMorinus.getsize(common.common.fortune)
				elif i == tidx+1:
					w1, h1 = self.fntText.getsize(self.ascmctxt[0])
				elif i == tidx+2:
					w1, h1 = self.fntText.getsize(self.ascmctxt[1])

				w2, h2 = 0.0, 0.0
				if i < tidx:
					w2, h2 = self.fntMorinus.getsize(common.common.Planets[i])
				elif i == tidx:
					w2, h2 = self.fntMorinus.getsize(common.common.fortune)
				elif i == tidx+1:
					w2, h2 = self.fntText.getsize(self.ascmctxt[0])
				elif i == tidx+2:
					w2, h2 = self.fntText.getsize(self.ascmctxt[1])

				x1 = order[i]+bshift[i]
				x2 = order[i+1]+bshift[i+1]

				if order[i]+bshift[i] > order[i+1]+bshift[i+1] or self.overlap(x1, w1, x2, w2):
					bshift[i+1] += diff
				else:
					break

		#Right
		lenord = len(order)-1
		LIM = self.TABLE_WIDTH#+BOR!?

		val = order[lenord]+bshift[lenord]
		if order[lenord]+bshift[lenord] > LIM:
			diff = (order[lenord]+bshift[lenord])-LIM
			bshift[lenord] -= diff

			#check the other bodies
			for i in range(lenord, 0, -1):
				w1, h1 = 0.0, 0.0
				tidx = planets.Planets.PLANETS_NUM-1
				if i < tidx:
					w1, h1 = self.fntMorinus.getsize(common.common.Planets[i])
				elif i == tidx:
					w1, h1 = self.fntMorinus.getsize(common.common.fortune)
				elif i == tidx+1:
					w1, h1 = self.fntText.getsize(self.ascmctxt[0])
				elif i == tidx+2:
					w1, h1 = self.fntText.getsize(self.ascmctxt[1])

				w2, h2 = 0.0, 0.0
				if i < tidx:
					w2, h2 = self.fntMorinus.getsize(common.common.Planets[i])
				elif i == tidx:
					w2, h2 = self.fntMorinus.getsize(common.common.fortune)
				elif i == tidx+1:
					w2, h2 = self.fntText.getsize(self.ascmctxt[0])
				elif i == tidx+2:
					w2, h2 = self.fntText.getsize(self.ascmctxt[1])

				x1 = order[i-1]+bshift[i-1]
				x2 = order[i]+bshift[i]

				if order[i-1]+bshift[i-1] > order[i]+bshift[i] or self.overlap(x1, w1, x2, w2):
					bshift[i-1] -= diff
				else:
					break

		return bodies[:], bshift[:], mixed[:]


	def doArrange(self, num, bshift, order, mixed, forward = False):
		shifted = False

		for i in range(num-1):
			shifted = self.doShift(i, i+1, bshift, order, mixed, forward)

		if shifted:
			self.doArrange(num, bshift, order, mixed, forward)


	def doShift(self, b1, b2, bshift, order, mixed, forward = False):
		shifted = False

		x1 = order[b1]+bshift[b1]
		x2 = order[b2]+bshift[b2]

		w1, h1 = 0.0, 0.0
		tidx = planets.Planets.PLANETS_NUM-1
		mb1 = mixed[b1]
		if mb1 < tidx:
			w1, h1 = self.fntMorinus.getsize(common.common.Planets[mb1])
		elif mb1 == tidx:
			w1, h1 = self.fntMorinus.getsize(common.common.fortune)
		elif mb1 == tidx+1:
			w1, h1 = self.fntText.getsize(self.ascmctxt[0])
		elif mb1 == tidx+2:
			w1, h1 = self.fntText.getsize(self.ascmctxt[1])

		w2, h2 = 0.0, 0.0
		mb2 = mixed[b2]
		if mb2 < tidx:
			w2, h2 = self.fntMorinus.getsize(common.common.Planets[mb2])
		elif mb2 == tidx:
			w2, h2 = self.fntMorinus.getsize(common.common.fortune)
		elif mb2 == tidx+1:
			w2, h2 = self.fntText.getsize(self.ascmctxt[0])
		elif mb2 == tidx+2:
			w2, h2 = self.fntText.getsize(self.ascmctxt[1])

		while (self.overlap(x1, w1, x2, w2)):
			if not forward:
				bshift[b1] -= 1.0
			bshift[b2] += 1.0

			x1 = order[b1]+bshift[b1]
			x2 = order[b2]+bshift[b2]

			if not shifted:
				shifted = True

		return shifted


	def overlap(self, x1, w1, x2, w2):
		return (x1 <= x2 and x2 <= x1+w1+self.BSPACE) or (x2 <= x1 and x1 <= x2+w2+self.BSPACE)


