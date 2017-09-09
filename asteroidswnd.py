import wx
import os
import chart
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class AsteroidsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = len(self.chart.asteroids.asteroids)
		self.COLUMN_NUM = 4
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Ast']


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
		draw.rectangle(((BOR+self.CELL_WIDTH, BOR),(BOR+self.CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt = (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'])

		for i in range(len(txt)):
			w,h = draw.textsize(txt[i], self.fntText)
			draw.text((BOR+self.CELL_WIDTH*(i+1)+(self.CELL_WIDTH-w)/2, BOR+(self.TITLE_HEIGHT-h)/2), txt[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		for i in range(len(self.chart.asteroids.asteroids)):
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, self.chart.asteroids.asteroids[i].name, self.chart.asteroids.asteroids[i].data, tableclr, i)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawline(self, draw, x, y, name, data, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
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






