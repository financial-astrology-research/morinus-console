import math
import wx
import os
import astrology
import planets
import houses
import chart
import common
import commonwnd
import Image, ImageDraw, ImageFont
import mtexts
import util


class AspectsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(2*18*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/4
		self.XOFFSET = self.SPACE
		self.YOFFSET = self.SPACE/2
		self.SQUARE_SIZE = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = 12

		self.HOUSESOFFS = 13
		self.COLUMN_NUM = 19 
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1
			if not self.options.houses:
				self.COLUMN_NUM -= 6 

		self.TABLE_HEIGHT = (self.LINE_NUM*(self.SQUARE_SIZE+self.SPACE))

		self.TABLE_WIDTH = (self.COLUMN_NUM*(self.SQUARE_SIZE+self.SPACE))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, 4*self.FONT_SIZE/5)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE/2)
		self.fntAspects = ImageFont.truetype(common.common.symbols, self.FONT_SIZE/2)
		self.fntText = ImageFont.truetype(common.common.abc, 2*self.FONT_SIZE/3)
		self.fntText2 = ImageFont.truetype(common.common.abc, self.FONT_SIZE/3)
		self.fntText3 = ImageFont.truetype(common.common.abc, self.FONT_SIZE/2)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
		self.arsigndiff = (0, -1, -1, 2, -1, 3, 4, -1, -1, -1, 6)
		self.hidx = (1, 2, 3, 10, 11, 12)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Asps']


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

		x = BOR
		j = 0
		num = len(common.common.Planets)-1
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue

			y = BOR+(j+1)*(self.SQUARE_SIZE+self.SPACE)
			self.drawSquare(draw, x, y, tableclr)
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			w,h = draw.textsize(common.common.Planets[i], self.fntMorinus)
			draw.text((x+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), common.common.Planets[i], fill=clr, font=self.fntMorinus)
			j += 1

		#AscMC
		txt = ('0', '1')
		y = BOR
		for i in range(len(txt)):		
			x = BOR+(self.SQUARE_SIZE+self.SPACE)*(i+1)
			self.drawSquare(draw, x, y, tableclr)
			w,h = draw.textsize(txt[i], self.fntSymbol)
			draw.text((x+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE-h)/2), txt[i], fill=txtclr, font=self.fntSymbol)

		arAscMC = (self.chart.houses.ascmc[houses.Houses.ASC], self.chart.houses.ascmc[houses.Houses.MC])
		for i in range(len(self.chart.aspmatrixAscMC)):
			k = 0
			for j in range(len(self.chart.aspmatrixAscMC[i])):
				if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
					continue
				x = BOR+(i+1)*(self.SPACE+self.SQUARE_SIZE)
				y = BOR+(k+1)*(self.SQUARE_SIZE+self.SPACE)
				self.drawSquare(draw, x, y, tableclr)
				lon1 = arAscMC[i]
				lon2 = self.chart.planets.planets[j].data[planets.Planet.LONG]
				showasp = self.isShowAsp(self.chart.aspmatrixAscMC[i][j].typ, lon1, lon2)
				if showasp:
					if self.isExact(self.chart.aspmatrixAscMC[i][j].exact, lon1, lon2):
						draw.rectangle(((x+self.XOFFSET/2, y+self.XOFFSET/2), (x+self.SQUARE_SIZE-self.XOFFSET/2, y+self.SQUARE_SIZE-self.XOFFSET/2-1)), fill=self.bkgclr, outline=tableclr)

					if self.chart.aspmatrixAscMC[i][j].appl:
						draw.polygon(((x, y), (x+self.SPACE, y), (x, y+self.SPACE)), fill=tableclr, outline=tableclr)

					txt = common.common.Aspects[self.chart.aspmatrixAscMC[i][j].typ]
					clr = self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ]
					if self.bw:
						clr = (0,0,0)
					draw.text((BOR+(i+1)*(self.SPACE+self.SQUARE_SIZE)+self.XOFFSET, BOR+(self.SQUARE_SIZE+self.SPACE)*(k+1)+self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=self.fntAspects)
				
				if self.chart.aspmatrixAscMC[i][j].parallel != chart.Chart.NONE:
					pclr = (0,0,0)
					if not self.bw:
						pclr = self.options.clrperegrin
					txt = 'X'
					if self.chart.aspmatrixAscMC[i][j].parallel == chart.Chart.CONTRAPARALLEL:
						txt = 'Y'
					w,h = draw.textsize(txt, self.fntAspects)
					draw.text((BOR+(i+1)*(self.SPACE+self.SQUARE_SIZE)+self.SQUARE_SIZE-w-self.SPACE, BOR+(self.SQUARE_SIZE+self.SPACE)*(k+1)+self.YOFFSET, self.SQUARE_SIZE), txt, fill=pclr, font=self.fntAspects)

				txt = str(self.chart.aspmatrixAscMC[i][j].dif)
				if showasp:
					txt = str(self.chart.aspmatrixAscMC[i][j].aspdif)
				t = txt.partition('.')
				txt = t[0]+t[1]+t[2][0]
				fnt = self.fntText2
				clr = (0,0,0)
				if showasp:
					fnt = self.fntText3 
					if not self.bw:
						clr = self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ]
				else:
					if not self.bw:
						clr = txtclr
				w,h = draw.textsize(txt, fnt)
				draw.text((BOR+(i+1)*(self.SPACE+self.SQUARE_SIZE)+(self.SQUARE_SIZE-w)/2, BOR+(self.SQUARE_SIZE+self.SPACE)*(k+1)+self.SQUARE_SIZE-h-self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=fnt)
				k += 1

		#Planets
		x = BOR+3*self.SQUARE_SIZE+3*self.SPACE
		k = 0
		num = len(common.common.Planets)-2
		for i in range(num):#Diagonal planets	
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			self.drawSquare(draw, x+(self.SQUARE_SIZE+self.SPACE)*k, BOR+(self.SQUARE_SIZE+self.SPACE)*(k+1), tableclr)
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			w,h = draw.textsize(common.common.Planets[i], self.fntMorinus)
			draw.text((x+(self.SQUARE_SIZE+self.SPACE)*k+(self.SQUARE_SIZE-w)/2, BOR+(self.SQUARE_SIZE+self.SPACE)*(k+1)+(self.SQUARE_SIZE-h)/2), common.common.Planets[i], fill=clr, font=self.fntMorinus)
			k += 1

		x = BOR+(self.SQUARE_SIZE+self.SPACE)*3
		y = BOR+(self.SQUARE_SIZE+self.SPACE)
		ii = 0
		for i in range(self.chart.planets.PLANETS_NUM-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			jj = 0
			for j in range(self.chart.planets.PLANETS_NUM-1):
				if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
					continue
				if jj > ii:
					k = x+(self.SQUARE_SIZE+self.SPACE)*ii
					l = y+(self.SQUARE_SIZE+self.SPACE)*jj
					self.drawSquare(draw, k, l, tableclr)
					lon1 = self.chart.planets.planets[i].data[planets.Planet.LONG]
					lon2 = self.chart.planets.planets[j].data[planets.Planet.LONG]
					showasp = self.isShowAsp(self.chart.aspmatrix[j][i].typ, lon1, lon2, j)
					if showasp:
						if self.isExact(self.chart.aspmatrix[j][i].exact, lon1, lon2):
							draw.rectangle(((k+self.XOFFSET/2, l+self.XOFFSET/2), (k+self.SQUARE_SIZE-self.XOFFSET/2, l+self.SQUARE_SIZE-self.XOFFSET/2-1)), fill=self.bkgclr, outline=tableclr)
						if self.chart.aspmatrix[j][i].appl:
							draw.polygon(((k, l), (k+self.SPACE, l), (k, l+self.SPACE)), fill=tableclr, outline=tableclr)

						txt = common.common.Aspects[self.chart.aspmatrix[j][i].typ]
						clr = self.options.clraspect[self.chart.aspmatrix[j][i].typ]
						if self.bw:
							clr = (0,0,0)
						draw.text((x+(self.SQUARE_SIZE+self.SPACE)*ii+self.XOFFSET, y+(self.SQUARE_SIZE+self.SPACE)*jj+self.YOFFSET), txt, fill=clr, font=self.fntAspects)

					if self.chart.aspmatrix[j][i].parallel != chart.Chart.NONE:
						pclr = (0,0,0)
						if not self.bw:
							pclr = self.options.clrperegrin
						txt = 'X'
						if self.chart.aspmatrix[j][i].parallel == chart.Chart.CONTRAPARALLEL:
							txt = 'Y'
						w,h = draw.textsize(txt, self.fntAspects)
						draw.text((x+(self.SQUARE_SIZE+self.SPACE)*ii+self.SQUARE_SIZE-w-self.SPACE, y+(self.SQUARE_SIZE+self.SPACE)*jj+self.YOFFSET), txt, fill=pclr, font=self.fntAspects)

					txt = str(self.chart.aspmatrix[j][i].dif)
					if showasp:
						txt = str(self.chart.aspmatrix[j][i].aspdif)
					t = txt.partition('.')
					txt = t[0]+t[1]+t[2][0]
					fnt = self.fntText2
					clr = (0,0,0)
					if showasp:
						fnt = self.fntText3 
						if not self.bw:
							clr = self.options.clraspect[self.chart.aspmatrix[j][i].typ]
					else:
						if not self.bw:
							clr = txtclr
					w,h = draw.textsize(txt, fnt)
					draw.text((x+(self.SQUARE_SIZE+self.SPACE)*ii+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE+self.SPACE)*jj+self.SQUARE_SIZE-h-self.YOFFSET), txt, fill=clr, font=fnt)
				jj += 1
			ii += 1

		#Houses
		if not self.options.intables or (self.options.intables and self.options.houses):
			hidx = (1, 2, 3, 10, 11, 12)
			x = BOR+self.HOUSESOFFS*self.SQUARE_SIZE+self.HOUSESOFFS*self.SPACE
			for i in range(len(hidx)):		
				self.drawSquare(draw, x+(self.SQUARE_SIZE+self.SPACE)*i, BOR, tableclr)
				w,h = draw.textsize(common.common.Housenames2[hidx[i]-1], self.fntText)
				draw.text((x+(self.SQUARE_SIZE+self.SPACE)*i+(self.SQUARE_SIZE-w)/2, BOR+(self.SQUARE_SIZE-h)/2), common.common.Housenames2[hidx[i]-1], fill=(0,0,0), font=self.fntText)

			x = BOR+self.HOUSESOFFS*(self.SQUARE_SIZE+self.SPACE)
			y = BOR+(self.SQUARE_SIZE+self.SPACE)
			for i in range(len(self.chart.aspmatrixH)):
				kk = 0
				for j in range(len(self.chart.aspmatrixH[i])):
					if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
						continue
					k = x+(self.SQUARE_SIZE+self.SPACE)*i
					l = y+(self.SQUARE_SIZE+self.SPACE)*kk
					self.drawSquare(draw, k, l, tableclr)
					lon1 = self.chart.houses.cusps[self.hidx[i]]
					lon2 = self.chart.planets.planets[j].data[planets.Planet.LONG]
					showasp = self.isShowAsp(self.chart.aspmatrixH[i][j].typ, lon1, lon2)
					if showasp:
						if self.isExact(self.chart.aspmatrixH[i][j].exact, lon1, lon2):
							draw.rectangle(((k+self.XOFFSET/2, l+self.XOFFSET/2), (k+self.SQUARE_SIZE-self.XOFFSET/2, l+self.SQUARE_SIZE-self.XOFFSET/2-1)), fill=self.bkgclr, outline=tableclr)
						if self.chart.aspmatrixH[i][j].appl:
							draw.polygon(((k, l), (k+self.SPACE, l), (k, l+self.SPACE)), fill=tableclr, outline=tableclr)
	
						txt = common.common.Aspects[self.chart.aspmatrixH[i][j].typ]
						clr = self.options.clraspect[self.chart.aspmatrixH[i][j].typ]
						if self.bw:
							clr = (0,0,0)
						draw.text((x+i*(self.SPACE+self.SQUARE_SIZE)+self.XOFFSET, BOR+(self.SQUARE_SIZE+self.SPACE)*(kk+1)+self.YOFFSET, self.SQUARE_SIZE), txt, fill=clr, font=self.fntAspects)
	
					if self.chart.aspmatrixH[i][j].parallel != chart.Chart.NONE:
						pclr = (0,0,0)
						if not self.bw:
							pclr = self.options.clrperegrin
						txt = 'X'
						if self.chart.aspmatrixH[i][j].parallel == chart.Chart.CONTRAPARALLEL:
							txt = 'Y'
						w,h = draw.textsize(txt, self.fntAspects)
						draw.text((x+(self.SQUARE_SIZE+self.SPACE)*i+self.SQUARE_SIZE-w-self.SPACE, y+(self.SQUARE_SIZE+self.SPACE)*kk+self.YOFFSET), txt, fill=pclr, font=self.fntAspects)

					txt = str(self.chart.aspmatrixH[i][j].dif)
					if showasp:
						txt = str(self.chart.aspmatrixH[i][j].aspdif)
					t = txt.partition('.')
					txt = t[0]+t[1]+t[2][0]
					fnt = self.fntText2
					clr = (0,0,0)
					if showasp:
						fnt = self.fntText3 
						if not self.bw:
							clr = self.options.clraspect[self.chart.aspmatrixH[i][j].typ]
					else:
						if not self.bw:
							clr = txtclr

					w,h = draw.textsize(txt, fnt)
					draw.text((x+(self.SQUARE_SIZE+self.SPACE)*i+(self.SQUARE_SIZE-w)/2, y+(self.SQUARE_SIZE+self.SPACE)*kk+self.SQUARE_SIZE-h-self.YOFFSET), txt, fill=clr, font=fnt)
					kk += 1

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawSquare(self, draw, x, y, tableclr):
		draw.line((x, y, x+self.SQUARE_SIZE, y), fill=tableclr)
		draw.line((x, y, x, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x+self.SQUARE_SIZE, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y), fill=tableclr)


	def isShowAsp(self, typ, lon1, lon2, p = -1):
		res = False

		if typ != chart.Chart.NONE and (not self.options.intables or self.options.aspect[typ]):
			val = True
			#check traditional aspects
			if self.options.intables:
				if self.options.traditionalaspects:
					if not(typ == chart.Chart.CONJUNCTIO or typ == chart.Chart.SEXTIL or typ == chart.Chart.QUADRAT or typ == chart.Chart.TRIGON or typ == chart.Chart.OPPOSITIO):
						val = False
					else:
						lona1 = lon1
						lona2 = lon2
						if self.options.ayanamsha != 0:
							lona1 -= self.chart.ayanamsha
							lona1 = util.normalize(lona1)
							lona2 -= self.chart.ayanamsha
							lona2 = util.normalize(lona2)
						sign1 = int(lona1/chart.Chart.SIGN_DEG)
						sign2 = int(lona2/chart.Chart.SIGN_DEG)
						signdiff = math.fabs(sign1-sign2)
						#check pisces-aries transition
						if signdiff > chart.Chart.SIGN_NUM/2:
							signdiff = chart.Chart.SIGN_NUM-signdiff#!?
						if self.arsigndiff[typ] != signdiff:
							val = False

				if not self.options.aspectstonodes and p == astrology.SE_MEAN_NODE:
					val = False

			res = val

		return res


	def isExact(self, exact, lon1, lon2):
		res = False

		if self.options.intables and self.options.traditionalaspects:
			lona1 = lon1
			lona2 = lon2
			if self.options.ayanamsha != 0:
				lona1 -= self.chart.ayanamsha
				lona1 = util.normalize(lona1)
				lona2 -= self.chart.ayanamsha
				lona2 = util.normalize(lona2)
			deg1 = int(lona1%chart.Chart.SIGN_DEG)
			deg2 = int(lona2%chart.Chart.SIGN_DEG)
			if deg1 == deg2:
				res = True
		else:
			if exact:
				res = True

		return res



