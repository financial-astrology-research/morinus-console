import wx
import os
import astrology
import planets
import houses
import chart
import fortune
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class ProfectionsMonWnd(commonwnd.CommonWnd):
	AGE, DATE, ASC, MC, SUN, MOON, FORTUNE, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO = range(0, 15)

	def __init__(self, parent, age, pchrts, dates, options, mainfr, mainsigs, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, pchrts[0][0], options, id, size)
		
		self.age = age
		self.pcharts = pchrts
		self.dates = dates
		self.mainfr = mainfr
		self.mainsigs = mainsigs

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = len(dates)

		if self.mainsigs:
			self.COLUMN_NUM = 7
		else:
			self.COLUMN_NUM = 15
			if self.options.intables:
				if not self.options.transcendental[chart.Chart.TRANSURANUS]:
					self.COLUMN_NUM -= 1
				if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
					self.COLUMN_NUM -= 1
				if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
					self.COLUMN_NUM -= 1

		self.CELL_WIDTH = 3*self.FONT_SIZE
		self.BIG_CELL_WIDTH = 7*self.FONT_SIZE #Date
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.CELL_WIDTH+(self.COLUMN_NUM-1)*self.BIG_CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = ((self.COLUMN_NUM-1)*(self.BIG_CELL_WIDTH)+self.CELL_WIDTH)
		val = 0
		if len(self.dates) == 12:
			val = self.LINE_HEIGHT
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM*(self.LINE_HEIGHT))+val)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Pro']


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

		#Title
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt = (mtexts.txts['Age'], mtexts.txts['Date'], mtexts.txts['Asc'], mtexts.txts['MC'], common.common.Planets[0], common.common.Planets[1], common.common.fortune, common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9])
		arclrs = (txtclr, txtclr, txtclr, txtclr, self.options.clrindividual[0], self.options.clrindividual[1], self.options.clrindividual[11], self.options.clrindividual[2], self.options.clrindividual[3], self.options.clrindividual[4], self.options.clrindividual[5], self.options.clrindividual[6], self.options.clrindividual[7], self.options.clrindividual[8], self.options.clrindividual[9])

		cols = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)

		offs = 0
		for i in range(self.COLUMN_NUM):
			fnt = self.fntText
			if i > 3:
				fnt = self.fntMorinus
			tclr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					tclr = arclrs[i]
				else:
					if i > 3:
						tclr = self.options.clrperegrin

			w,h = draw.textsize(txt[i], fnt)
			clr = txtclr
			if i > 3:
				clr = tclr
			draw.text((BOR+offs+(cols[i]-w)/2, BOR+(self.TITLE_HEIGHT-h)/2), txt[i], fill=clr, font=fnt)
			offs += cols[i]

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
#		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

#		draw age
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt = str(self.age)
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.CELL_WIDTH-w)/2, y+(self.TABLE_HEIGHT-h)/2-self.LINE_HEIGHT/2), txt, fill=txtclr, font=self.fntText)

		agestart = agecont = self.age%12
		for i in range(self.LINE_NUM):
			if i < len(self.pcharts):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, self.pcharts[agecont], self.dates, i)
			else:
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, self.pcharts[agestart], self.dates, i)
			agecont += 1
			if agecont > 11:
				agecont = 0

		#draw 13th line (empty) in case of 12steps
		y = BOR+self.TABLE_HEIGHT
		if len(self.dates) == 12:
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
			offs = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)
			draw.line((x, y-self.LINE_HEIGHT, x, y), fill=tableclr)
			summa = 0
			for i in range(self.COLUMN_NUM):
				draw.line((x+summa+offs[i], y-self.LINE_HEIGHT, x+summa+offs[i], y), fill=tableclr)
				summa += offs[i]
		else:
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, clr, pcharts, dates, idx):
		#bottom horizontal line
		val = self.CELL_WIDTH
#		if idx == self.LINE_NUM-1:
#			val = 0
		draw.line((x+val, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		draw.line((x, y, x, y+self.LINE_HEIGHT), fill=clr)
		summa = 0
		for i in range(self.COLUMN_NUM):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			tclr = (0, 0, 0)
			if not self.bw:
				txtclr = self.options.clrtexts

			if i == ProfectionsMonWnd.DATE:
				txt = str(dates[idx][0])+'.'+str(dates[idx][1]).zfill(2)+'.'+str(dates[idx][2]).zfill(2)+'.'
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=tclr, font=self.fntText)
			elif i != ProfectionsMonWnd.AGE:
				if i == ProfectionsMonWnd.ASC:
					lon = pcharts[0].houses.ascmc[houses.Houses.ASC]
				if i == ProfectionsMonWnd.MC:
					lon = pcharts[0].houses.ascmc[houses.Houses.MC]
				if i == ProfectionsMonWnd.SUN:
					lon = pcharts[0].planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
				if i == ProfectionsMonWnd.MOON:
					lon = pcharts[0].planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]
				if i == ProfectionsMonWnd.FORTUNE:
					lon = pcharts[0].fortune.fortune[fortune.Fortune.LON]
				if i >= ProfectionsMonWnd.MERCURY:
					lon = pcharts[0].planets.planets[i-5].data[planets.Planet.LONG]
				if self.options.ayanamsha != 0:
					lon -= self.chart.ayanamsha
					lon = util.normalize(lon)
				d,m,s = util.decToDeg(lon)
				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=tclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=tclr, font=self.fntMorinus)

			summa += offs[i]





