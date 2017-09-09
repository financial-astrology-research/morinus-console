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


class ZodParsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.pars = chrt.zodpars.pars
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

		self.LINE_NUM = len(self.pars)
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
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

		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Par']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		txtclr = self.options.clrtexts
		if self.bw:
			txtclr = (0,0,0)

		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		#Title
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))

		txt = mtexts.txts['ZodPars']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH/2+self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		txt = (mtexts.txts['Parallel'], mtexts.txts['ContraParallel'])
		for i in range(len(txt)):
			w,h = draw.textsize(txt[i], self.fntText)
			offs = self.CELL_WIDTH/2
			if i != 0:
				offs += self.CELL_WIDTH
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+offs+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt[i], fill=txtclr, font=self.fntText)


		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		txts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9])
		ii = 0
		for i in range(len(txts)):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO])):
				continue
			self.drawline(draw, x, y+ii*self.LINE_HEIGHT, i, txts, self.pars[i].pts, tableclr)
			ii += 1

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, idx, txt, data, clr):
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
			if self.options.useplanetcolors:
				clr = self.options.clrindividual[idx]
			else:
				dign = self.chart.dignity(idx)
				clr = self.clrs[dign]

		w,h = draw.textsize(txt[idx], self.fntMorinus)
		offset = (self.SMALL_CELL_WIDTH-w)/2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt[idx], fill=clr, font=self.fntMorinus)

		#arrange data in order(parallel, contraparallel)
		dataord = []
		for i in range(len(data)):
			if data[i][0] == -1.0:
				break
			if data[i][1] == chart.Chart.PARALLEL:
				dataord.append(data[i][0])

		if len(dataord) < 2:
			dataord.append(-1.0)
			if len(dataord) < 2:
				dataord.append(-1.0)

		for i in range(len(data)):
			if data[i][0] == -1.0:
				break
			if data[i][1] == chart.Chart.CONTRAPARALLEL:
				dataord.append(data[i][0])

		if len(dataord) < 4:
			dataord.append(-1.0)
			if len(dataord) < 4:
				dataord.append(-1.0)

		#data
		offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(len(dataord)):
			if dataord[i] == -1:
				summa += offs[i]
				continue

			d,m,s = util.decToDeg(dataord[i])
			if self.options.ayanamsha != 0:
				lona = dataord[i]-self.chart.ayanamsha
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

			summa += offs[i]




