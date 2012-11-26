import os
import wx
import astrology
import planets
import chart
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class MunPosWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = planets.Planets.PLANETS_NUM-1 
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1
		self.COLUMN_NUM = 1

		self.SPACE_ARABIANY = self.LINE_HEIGHT
		self.LINE_NUM_ARABIAN = 1
		self.COLUMN_NUM_ARABIAN = 4

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.TITLE_WIDTH_ARABIAN = (self.COLUMN_NUM_ARABIAN+1)*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
		self.TABLE_WIDTH_ARABIAN = self.TABLE_WIDTH
		self.TABLE_HEIGHT_ARABIAN = 0
		if not self.options.intables or (self.options.intables and self.options.showlof):
			self.TABLE_WIDTH_ARABIAN = (self.CELL_WIDTH+self.COLUMN_NUM_ARABIAN*(self.CELL_WIDTH))
			self.TABLE_HEIGHT_ARABIAN = (self.SPACE_ARABIANY+self.LINE_NUM_ARABIAN*self.LINE_HEIGHT)
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT)+self.TABLE_HEIGHT_ARABIAN)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH_ARABIAN+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Mun']


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
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt = mtexts.txts['HousePercent']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((BOR+self.SMALL_CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+(self.TITLE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		ii = 0
		for i in range(len(common.common.Planets)-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			self.drawline(draw, x, y+ii*self.LINE_HEIGHT, tableclr, i)
			ii += 1

		#Arabian Parts
		if not self.options.intables or (self.options.intables and self.options.showlof):
			x = BOR
			y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT)+self.SPACE_ARABIANY
			draw.rectangle(((x,y),(x+self.TITLE_WIDTH_ARABIAN, y+self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			self.drawlinelof(draw, x, y, mtexts.txts['MLoF'], self.chart.munfortune.mfortune, tableclr, 0)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			tclr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					tclr = self.options.clrindividual[idx]
				else:
					dign = self.chart.dignity(idx)
					tclr = self.clrs[dign]

			if i == 1:
				txt = common.common.Planets[idx]
				w,h = draw.textsize(txt, self.fntMorinus)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=tclr, font=self.fntMorinus)
			elif i != 0:
				ret, serr = astrology.swe_house_pos(self.chart.houses.ascmc[1], self.chart.place.lat, self.chart.obl[0], ord(self.chart.houses.hsys), self.chart.planets.planets[idx].data[planets.Planet.LONG], self.chart.planets.planets[idx].data[planets.Planet.LAT])
#				ret = int(ret*100.0)/100.0
				txt = str(ret)
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=tclr, font=self.fntText)

			summa += offs[i]


	def drawlinelof(self, draw, x, y, name, data, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH_ARABIAN, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		for i in range(self.COLUMN_NUM_ARABIAN+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			d, m, s = 0, 0, 0
			if i > 1:
				d,m,s = util.decToDeg(data[i-2])

			if i == 1:
				w,h = draw.textsize(name, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), name, fill=txtclr, font=self.fntText)
			elif i == 2:
				if self.options.ayanamsha != 0:
					lona = data[i-2]-self.chart.ayanamsha
					lona = util.normalize(lona)
					d,m,s = util.decToDeg(lona)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				txtsign = self.signs[sign]
				wsg,hsg = draw.textsize(txtsign, self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)/2), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == 3 or i == 5:
				sign = ''
				if data[i-2] < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			elif i == 4:
				txt = str(d)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if self.options.intime:
					d,m,s = util.decToDeg(data[i-2]/15.0)
					txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			summa += offs[i]




