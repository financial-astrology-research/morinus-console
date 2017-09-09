import wx
import os
import astrology
import chart
import planets
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class MidPointsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.YOFFSET = self.LINE_HEIGHT
		self.TABLE_HEIGHT = (30*(self.LINE_HEIGHT)+4*self.YOFFSET)

		self.SMALL_CELL_WIDTH = 5*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.XOFFSET = self.SMALL_CELL_WIDTH
		self.TABLE_WIDTH = (3*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH)+3*self.XOFFSET)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = [self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil]
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2

		self.deg_symbol = u'\u00b0'

		#X,Y
		LN = 12
		BOR = commonwnd.CommonWnd.BORDER
		self.ar = [[BOR, BOR], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR], [BOR, BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR, BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR, BOR+(LN+15)*self.LINE_HEIGHT+3*self.YOFFSET]]

		if self.options.intables:
			leng = len(self.ar)
			for i in range(3, leng):
				if not self.options.transcendental[chart.Chart.TRANSURANUS]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.shownodes:
					self.ar[i][1] -= 2*self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= 2*self.LINE_HEIGHT

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Mid']


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

		txt = mtexts.txts['Longitude']
		w,h = draw.textsize(txt, self.fntText)
		num = len(self.ar)
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				num -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				num -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				num -= 1
			if not self.options.shownodes:
				num -= 1
		for i in range(num):
			x = self.ar[i][0]+self.SMALL_CELL_WIDTH
			y = self.ar[i][1]
			draw.line((x, y, x+self.CELL_WIDTH, y), fill=tableclr)
			draw.line((x, y, x, y+self.LINE_HEIGHT), fill=tableclr)
			draw.line((x+self.CELL_WIDTH, y, x+self.CELL_WIDTH, y+self.LINE_HEIGHT), fill=tableclr)
			draw.line((x-self.SMALL_CELL_WIDTH, y+self.LINE_HEIGHT, x+self.CELL_WIDTH, y+self.LINE_HEIGHT), fill=tableclr)
			draw.text((x+(self.CELL_WIDTH-w)/2, self.ar[i][1]+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		artmp = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
		length = len(artmp)

#		arln = [0, 11, 21, 30, 38, 45, 51, 56, 60, 63, 65]  #11 is linenum of 1st table 21 is 1st and 2nd ...
		arln = [0]
		for i in range(length):
			arln.append(arln[i]+artmp[i])

		for i in range(num):
			ln = 1
			for j in range(arln[i], arln[i+1]):		
				if self.options.intables and ((self.chart.midpoints.mids[j].p2 == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_MEAN_NODE and not self.options.shownodes) or (self.chart.midpoints.mids[j].p2 == astrology.SE_TRUE_NODE and not self.options.shownodes)):
					continue
				wsp,hsp = draw.textsize(' - ', self.fntText)
				p1 = common.common.Planets[self.chart.midpoints.mids[j].p1]
				p2 = common.common.Planets[self.chart.midpoints.mids[j].p2]
				wpl1,hpl1 = draw.textsize(p1, self.fntMorinus)
				wpl2,hpl2 = draw.textsize(p2, self.fntMorinus)
				clr1 = (0,0,0)
				clr2 = (0,0,0)
				if not self.bw:
					if self.options.useplanetcolors:
						objidx1 = self.chart.midpoints.mids[j].p1
						objidx2 = self.chart.midpoints.mids[j].p2
						if objidx1 >= planets.Planets.PLANETS_NUM-1:
							objidx1 -= 1
						if objidx2 >= planets.Planets.PLANETS_NUM-1:
							objidx2 -= 1
						clr1 = self.options.clrindividual[objidx1]
						clr2 = self.options.clrindividual[objidx2]
					else:
						dign1 = self.chart.dignity(self.chart.midpoints.mids[j].p1)
						dign2 = self.chart.dignity(self.chart.midpoints.mids[j].p2)
						clr1 = self.clrs[dign1]
						clr2 = self.clrs[dign2]
				draw.text((self.ar[i][0]+(self.SMALL_CELL_WIDTH-(wpl1+wsp+wpl2))/2, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), p1, fill=clr1, font=self.fntMorinus)
				draw.text((self.ar[i][0]+(self.SMALL_CELL_WIDTH-(wpl1+wsp+wpl2))/2+wpl1, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), ' - ', fill=txtclr, font=self.fntText)
				draw.text((self.ar[i][0]+(self.SMALL_CELL_WIDTH-(wpl1+wsp+wpl2))/2+wpl1+wsp, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), p2, fill=clr2, font=self.fntMorinus)

				lona = self.chart.midpoints.mids[j].m
				if self.options.ayanamsha != 0:
					lona -= self.chart.ayanamsha
					lona = util.normalize(lona)
				lon = lona
				d,m,s = util.decToDeg(lon)
				sign = int(lon/chart.Chart.SIGN_DEG)
				pos = int(lon%chart.Chart.SIGN_DEG)
				wsp,hsp = draw.textsize(' ', self.fntText)
				wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				w,h = draw.textsize(txt, self.fntText)
				offs = (self.CELL_WIDTH-(w+wsp+wsg))/2
				draw.text((self.ar[i][0]+self.SMALL_CELL_WIDTH+offs, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), txt, fill=txtclr, font=self.fntText)
				draw.text((self.ar[i][0]+self.SMALL_CELL_WIDTH+offs+w, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), ' ', fill=txtclr, font=self.fntText)
				draw.text((self.ar[i][0]+self.SMALL_CELL_WIDTH+offs+w+wsp, self.ar[i][1]+self.LINE_HEIGHT*ln+(self.LINE_HEIGHT-hsp)/2), self.signs[sign], fill=txtclr, font=self.fntMorinus)

				x = self.ar[i][0]
				y = self.ar[i][1]+self.LINE_HEIGHT*ln
				draw.line((x, y+self.LINE_HEIGHT, x+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y+self.LINE_HEIGHT), fill=tableclr)
				draw.line((x, y+self.LINE_HEIGHT, x, y), fill=tableclr)
				draw.line((x+self.SMALL_CELL_WIDTH, y+self.LINE_HEIGHT, x+self.SMALL_CELL_WIDTH, y), fill=tableclr)
				draw.line((x+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y+self.LINE_HEIGHT, x+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y), fill=tableclr)

				ln += 1

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)





