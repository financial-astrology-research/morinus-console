import wx
import os
import houses
import chart
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class MiscWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = 5
		self.COLUMN_NUM = 1
		self.CELL_WIDTH = 10*self.FONT_SIZE
		self.TABLE_HEIGHT = (self.LINE_NUM)*(self.LINE_HEIGHT)
		self.TABLE_WIDTH = (self.CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)

		self.TABLE2_OFFS = self.LINE_HEIGHT
		self.LINE_NUM2 = 1
		self.COLUMN_NUM2 = 2
		self.CELL_WIDTH2 = 10*self.FONT_SIZE
		self.TABLE_HEIGHT2 = (self.LINE_NUM2+1)*(self.LINE_HEIGHT)
		self.TABLE_WIDTH2 = (self.CELL_WIDTH+self.COLUMN_NUM2*self.CELL_WIDTH)

		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH2+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+self.TABLE2_OFFS+self.TABLE_HEIGHT2+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Misc']


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

		#Grid
		x = BOR
		y = BOR
		for i in range(self.LINE_NUM+1):
			draw.line((x, y+self.LINE_HEIGHT*i, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT*i), fill=tableclr)

		for i in range(self.COLUMN_NUM+1+1):
			draw.line((x+self.CELL_WIDTH*i, y, x+self.CELL_WIDTH*i, y+self.TABLE_HEIGHT), fill=tableclr)

		#Data
		SIDTIME = 0
		OBL = 1
		JD = 2
		VERTEX = 3
		EQUATASC = 4

		txts = (mtexts.txts['SidTime'], mtexts.txts['OblEcl'], mtexts.txts['JulianDay'], mtexts.txts['Vertex'], mtexts.txts['EquAsc'])
		data = (self.chart.houses.ascmc[houses.Houses.ARMC]/15.0, self.chart.obl[0], self.chart.time.jd, self.chart.houses.ascmc[houses.Houses.VERTEX], self.chart.houses.ascmc[houses.Houses.EQUASC])
		for i in range(self.LINE_NUM):
			w,h = draw.textsize(txts[i], self.fntText)
			draw.text((BOR+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txts[i], fill=txtclr, font=self.fntText)

			d, m, s = util.decToDeg(data[i])

			if i == SIDTIME:
				txt = str(d)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)
				w,h = draw.textsize(txt, self.fntText)
				draw.text((BOR+self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			elif i == OBL:
				txt = (str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				draw.text((BOR+self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			elif i == JD:
				txt = str(data[i])
				w,h = draw.textsize(txt, self.fntText)
				draw.text((BOR+self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			else:
				if self.options.ayanamsha != 0:
					ayanlon = data[i]-self.chart.ayanamsha
					ayanlon = util.normalize(ayanlon)
					d, m, s = util.decToDeg(ayanlon)
				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				wsp,hsp = draw.textsize(' ', self.fntText)
				txtsign = self.signs[sign]
				wsg,hsg = draw.textsize(txtsign, self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offset = (self.CELL_WIDTH-(w+wsp+wsg))/2
				draw.text((BOR+self.CELL_WIDTH+offset, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
				draw.text((BOR+self.CELL_WIDTH+offset+w+wsp, BOR+self.LINE_HEIGHT*i+(self.LINE_HEIGHT-h)/2), txtsign, fill=txtclr, font=self.fntMorinus)

		#Table 2
		txts = (mtexts.txts['Syzygy'], mtexts.txts['Date2'], mtexts.txts['Longitude'])
		x = BOR
		y = BOR+self.LINE_NUM*self.LINE_HEIGHT+self.TABLE2_OFFS

		draw.line((x, y, x+self.TABLE_WIDTH2, y), fill=tableclr)
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH2, y+self.LINE_HEIGHT), fill=tableclr)
		draw.line((x, y+2*self.LINE_HEIGHT, x+self.TABLE_WIDTH2, y+2*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x, y, x, y+2*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x+self.CELL_WIDTH, y+self.LINE_HEIGHT, x+self.CELL_WIDTH, y+2*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x+2*self.CELL_WIDTH, y+self.LINE_HEIGHT, x+2*self.CELL_WIDTH, y+2*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x+3*self.CELL_WIDTH, y+self.LINE_HEIGHT, x+3*self.CELL_WIDTH, y+2*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x+self.TABLE_WIDTH2, y, x+self.TABLE_WIDTH2, y+2*self.LINE_HEIGHT), fill=tableclr)

		num = len(txts)
		for i in range(num):
			w,h = draw.textsize(txts[i], self.fntText)
			draw.text((BOR+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txts[i], fill=txtclr, font=self.fntText)

		if not self.chart.time.bc:
			txt = mtexts.txts['NewMoon']
			if not self.chart.syzygy.newmoon:
				txt = mtexts.txts['FullMoon']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			h, m, s = util.decToDeg(self.chart.syzygy.time.time)
			txt = str(self.chart.syzygy.time.year)+'.'+str(self.chart.syzygy.time.month).zfill(2)+'.'+str(self.chart.syzygy.time.day).zfill(2)+'.'+' '+str(h).rjust(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			lon = self.chart.syzygy.lon
			if self.options.ayanamsha != 0:
				lon = lon-self.chart.ayanamsha
				lon = util.normalize(lon)

			d, m, s = util.decToDeg(lon)
			sign = d/chart.Chart.SIGN_DEG
			pos = d%chart.Chart.SIGN_DEG
			wsp,hsp = draw.textsize(' ', self.fntText)
			wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
			txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
			w,h = draw.textsize(txt, self.fntText)
			offset = (self.CELL_WIDTH-(w+wsp+wsg))/2
			draw.text((x+2*self.CELL_WIDTH+offset, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			draw.text((x+2*self.CELL_WIDTH+offset+w+wsp, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=txtclr, font=self.fntMorinus)


		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)







