import wx
import os
import astrology
import chart
import houses
import planets
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class AntisciaWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.ants = chrt.antiscia
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 4
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE

		self.TITLE_HEIGHT = 2*self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0

		self.LINE_NUM = 15
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.showlof:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 2

		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+self.LINE_NUM*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Ant']


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

		#Title
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt = (mtexts.txts['Antiscion'], mtexts.txts['Contraantiscion'])
		for i in range(len(txt)):
			w,h = draw.textsize(txt[i], self.fntText)
			offs = 0
			if i == 1:
				offs = self.CELL_WIDTH
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH/2+offs+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt[i], fill=txtclr, font=self.fntText)

		txt = (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Longitude'], mtexts.txts['Latitude'])
		for i in range(len(txt)):
			w,h = draw.textsize(txt[i], self.fntText)
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		txts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9], common.common.Planets[10], common.common.Planets[11], common.common.fortune, '0', '1')
		data = ((self.ants.plantiscia[0].lon, 0.0, self.ants.plcontraant[0].lon, 0.0), (self.ants.plantiscia[1].lon, self.ants.plantiscia[1].lat, self.ants.plcontraant[1].lon, self.ants.plcontraant[1].lat), (self.ants.plantiscia[2].lon, self.ants.plantiscia[2].lat, self.ants.plcontraant[2].lon, self.ants.plcontraant[2].lat), (self.ants.plantiscia[3].lon, self.ants.plantiscia[3].lat, self.ants.plcontraant[3].lon, self.ants.plcontraant[3].lat), (self.ants.plantiscia[4].lon, self.ants.plantiscia[4].lat, self.ants.plcontraant[4].lon, self.ants.plcontraant[4].lat), (self.ants.plantiscia[5].lon, self.ants.plantiscia[5].lat, self.ants.plcontraant[5].lon, self.ants.plcontraant[5].lat), (self.ants.plantiscia[6].lon, self.ants.plantiscia[6].lat, self.ants.plcontraant[6].lon, self.ants.plcontraant[6].lat), (self.ants.plantiscia[7].lon, self.ants.plantiscia[7].lat, self.ants.plcontraant[7].lon, self.ants.plcontraant[7].lat), (self.ants.plantiscia[8].lon, self.ants.plantiscia[8].lat, self.ants.plcontraant[8].lon, self.ants.plcontraant[8].lat), (self.ants.plantiscia[9].lon, self.ants.plantiscia[9].lat, self.ants.plcontraant[9].lon, self.ants.plcontraant[9].lat), (self.ants.plantiscia[10].lon, self.ants.plantiscia[10].lat, self.ants.plcontraant[10].lon, self.ants.plcontraant[10].lat), (self.ants.plantiscia[11].lon, self.ants.plantiscia[11].lat, self.ants.plcontraant[11].lon, self.ants.plcontraant[11].lat), (self.ants.lofant.lon, self.ants.lofant.lat, self.ants.lofcontraant.lon, self.ants.lofcontraant.lat), (self.ants.ascmcant[0].lon, self.ants.ascmcant[0].lat, self.ants.ascmccontraant[0].lon, self.ants.ascmccontraant[0].lat), (self.ants.ascmcant[1].lon, self.ants.ascmcant[1].lat, self.ants.ascmccontraant[1].lon, self.ants.ascmccontraant[1].lat))
		i = 0
		for j in range(len(txts)):
			ascmc = False
			if j > 12:
				ascmc = True

			if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes) or (j == astrology.SE_TRUE_NODE and not self.options.shownodes) or (j== astrology.SE_TRUE_NODE+1 and not self.options.showlof)):
				continue
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, txts[j], tableclr, data[j], j, ascmc)
			i += 1

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, txt, clr, data, idx, AscMC):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		summa = 0
		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)
			summa += offs[i]

		#draw symbols
		clr = (0,0,0)
		if not self.bw:
			if not AscMC:
				if self.options.useplanetcolors:
					objidx = idx
					if idx > astrology.SE_MEAN_NODE:
						objidx -= 1
					clr = self.options.clrindividual[objidx]
				else:
					clr = self.options.clrperegrin
			else:
				clr = self.options.clrtexts
		fnt = self.fntMorinus
		if AscMC:
			fnt = self.fntSymbol
		w,h = draw.textsize(txt, fnt)
		offset = (self.SMALL_CELL_WIDTH-w)/2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=fnt)

		#data
		offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(len(data)):
			d,m,s = util.decToDeg(data[i])

			if i == 0 or i == 2:
				if self.options.ayanamsha != 0:
					lona = data[i]+self.chart.ayanamsha
					lona = util.normalize(lona)
					d,m,s = util.decToDeg(lona)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset+w+wsp, y+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clr, font=self.fntMorinus)
			else:
				sign = ''
				if data[i] < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)				
				offset = (offs[i]-w)/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)

			summa += offs[i]




