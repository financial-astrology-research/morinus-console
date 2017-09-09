import wx
import os
import astrology
import planets
import houses
import chart
import fortune
import almutens
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class AlmutenZodsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		#essentials
		self.LINE_NUM = 23
		self.COLUMN_NUM = 7# +leftmost +degreewins
		self.SMALL_CELL_WIDTH = 5*self.FONT_SIZE
		self.LONGITUDE_CELL_WIDTH = 7*self.FONT_SIZE
		self.CELL_WIDTH = 7*self.FONT_SIZE
		self.DEGREEWINS_CELL_WIDTH = 7*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = 10*self.FONT_SIZE
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.LONGITUDE_CELL_WIDTH+(self.COLUMN_NUM)*(self.CELL_WIDTH)+self.DEGREEWINS_CELL_WIDTH)
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.LINE_NUM*self.LINE_HEIGHT)

		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)

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
		return mtexts.txts['Alm']


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
		y = BOR
		draw.line((x+self.SMALL_CELL_WIDTH, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		y += self.LINE_HEIGHT
		for i in range(self.LINE_NUM+1):
			draw.line((x, y+i*self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+i*self.LINE_HEIGHT), fill=tableclr)

		draw.line((x, y, x, y+self.TABLE_HEIGHT-self.LINE_HEIGHT), fill=tableclr)
		x += self.SMALL_CELL_WIDTH
		y -= self.LINE_HEIGHT
		draw.line((x, y, x, y+self.TABLE_HEIGHT), fill=tableclr)
		for i in range(self.COLUMN_NUM+2):
			draw.line((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH, y, x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH, y+self.TABLE_HEIGHT), fill=tableclr)

		for i in range(astrology.SE_SATURN+1):
			clr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			txt = common.common.Planets[i]
			w,h = draw.textsize(txt, self.fntMorinus)
			draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)
			draw.text((x-self.SMALL_CELL_WIDTH+(self.SMALL_CELL_WIDTH-w)/2, y+(i+1)*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

			plon = self.chart.planets.planets[i].data[planets.Planet.LONG]
			self.drawLong(draw, x, y+self.TITLE_HEIGHT+i*self.LINE_HEIGHT, plon, clr)

			for j in range(astrology.SE_SATURN+1):
				if j == astrology.SE_SUN or j == astrology.SE_MOON:
					txt = self.chart.almutens.essentials.essentials[i][j][0]
					w,h = draw.textsize(txt, self.fntText)
					draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(j+1)*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
				else:
					txt = self.chart.almutens.essentials.essentials2[i][j-2][0]
					w,h = draw.textsize(txt, self.fntText)
					draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+(j+1)*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = self.chart.almutens.essentials.essentials[i][3][0]
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+8*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = self.chart.almutens.essentials.essentials[i][4][0]
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+9*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = self.chart.almutens.essentials.essentials[i][2][0]
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+10*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = self.chart.almutens.essentials.essentialsmc[i][0]
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+11*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		#Degree Wins
		txt = mtexts.txts['Almuten']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+self.LONGITUDE_CELL_WIDTH+7*self.CELL_WIDTH+(self.DEGREEWINS_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT
#		num = len(self.chart.almutens.essentials.degwinner)
		for i in range(2):
			self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, i, False, self.chart.almutens.essentials.degwinner, txtclr)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+2*self.LINE_HEIGHT
		num = len(self.chart.almutens.essentials.degwinner2)
		for i in range(num):
			self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, i, False, self.chart.almutens.essentials.degwinner2, txtclr)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+7*self.LINE_HEIGHT
		self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, 3, True, self.chart.almutens.essentials.degwinner, txtclr)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+8*self.LINE_HEIGHT
		self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, 4, True, self.chart.almutens.essentials.degwinner, txtclr)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+9*self.LINE_HEIGHT
		self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, 2, True, self.chart.almutens.essentials.degwinner, txtclr)

		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+10*self.LINE_HEIGHT
		self.drawDegWinner2(draw, x+self.LONGITUDE_CELL_WIDTH, y, self.chart.almutens.essentials.degwinnermc, txtclr)

		x = BOR
		y = BOR+self.LINE_HEIGHT
		#LoF
		clr = (0, 0, 0)
		if not self.bw:
			if self.options.useplanetcolors:
				clr = self.options.clrindividual[11]
			else:
				clr = self.options.clrperegrin
		txt = common.common.fortune
		w,h = draw.textsize(txt, self.fntMorinus)
		draw.text((x+(self.SMALL_CELL_WIDTH-w)/2, y+7*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

		flon = self.chart.fortune.fortune[fortune.Fortune.LON]
		self.drawLong(draw, x+self.SMALL_CELL_WIDTH, y+7*self.LINE_HEIGHT, flon, clr)

		#Syzygy
		txt = mtexts.txts['Syzygy']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.SMALL_CELL_WIDTH-w)/2, y+8*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		slon = self.chart.syzygy.lon
		self.drawLong(draw, x+self.SMALL_CELL_WIDTH, y+8*self.LINE_HEIGHT, slon, txtclr)

		#Asc
		txt = mtexts.txts['Asc']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.SMALL_CELL_WIDTH-w)/2, y+9*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		alon = self.chart.houses.ascmc[houses.Houses.ASC]
		self.drawLong(draw, x+self.SMALL_CELL_WIDTH, y+9*self.LINE_HEIGHT, alon, txtclr)

		#MC
		txt = mtexts.txts['MC']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.SMALL_CELL_WIDTH-w)/2, y+10*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		mlon = self.chart.houses.ascmc[houses.Houses.MC]
		self.drawLong(draw, x+self.SMALL_CELL_WIDTH, y+10*self.LINE_HEIGHT, mlon, txtclr)

		y = BOR+self.LINE_HEIGHT
		#Housecusps
		hcstxt = [mtexts.txts['HC1'], mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC4'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC7'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC10'], mtexts.txts['HC11'], mtexts.txts['HC12']]
		for i in range(astrology.SE_SATURN+1):
			for j in range(houses.Houses.HOUSE_NUM):
				if i == 0:
					txt = hcstxt[j]
					w,h = draw.textsize(txt, self.fntText)
					draw.text((x+(self.SMALL_CELL_WIDTH-w)/2, y+11*self.LINE_HEIGHT+j*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

				txt = self.chart.almutens.essentials.essentialshcs[i][j][0]
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+self.LONGITUDE_CELL_WIDTH+i*self.CELL_WIDTH+(self.CELL_WIDTH-w)/2, y+11*self.LINE_HEIGHT+j*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

				if i == 0:
					hlon = self.chart.houses.cusps[j+1]
					if self.options.ayanamsha != 0 and self.options.hsys != 'W':
						hlon -= self.chart.ayanamsha
						hlon = util.normalize(hlon)
					self.drawLong(draw, x+self.SMALL_CELL_WIDTH, y+11*self.LINE_HEIGHT+j*self.LINE_HEIGHT, hlon, txtclr, False)

		#Housecusps degwinner
		x = BOR+self.SMALL_CELL_WIDTH+7*self.CELL_WIDTH
		y = BOR+self.TITLE_HEIGHT+11*self.LINE_HEIGHT
		num = len(self.chart.almutens.essentials.degwinnerhcs)
		for i in range(num):
			self.drawDegWinner(draw, x+self.LONGITUDE_CELL_WIDTH, y, i, False, self.chart.almutens.essentials.degwinnerhcs, txtclr)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawDegWinner(self, draw, x, y, i, onlyone, degwinner, txtclr):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
		subnum = len(degwinner[0])
		mwidth = 0
		for j in range(subnum):
			pid = degwinner[i][j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
				sco = degwinner[i][0][1]
				txt = '('+str(sco)+')'
				w,h = draw.textsize(txt, self.fntText)
				wsp,hsp = draw.textsize(' ', self.fntText)
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				pltxt = common.common.Planets[aux[j][0]]
				wpl,hpl = draw.textsize(pltxt, self.fntMorinus)
				txt = '('+str(aux[j][1])+')'
				wsp,hsp = draw.textsize(' ', self.fntText)
				w,h = draw.textsize(txt, self.fntText)
				prev = 0
				for p in range(j):
					prev += aux[j][2]+wsp

				offs = i
				if onlyone:
					offs = 0
				draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)


	def drawDegWinner2(self, draw, x, y, degwinner, txtclr):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
		subnum = len(degwinner)
		mwidth = 0
		for j in range(subnum):
			pid = degwinner[j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
				sco = degwinner[0][1]
				txt = '('+str(sco)+')'
				w,h = draw.textsize(txt, self.fntText)
				wsp,hsp = draw.textsize(' ', self.fntText)
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				pltxt = common.common.Planets[aux[j][0]]
				wpl,hpl = draw.textsize(pltxt, self.fntMorinus)
				txt = '('+str(aux[j][1])+')'
				wsp,hsp = draw.textsize(' ', self.fntText)
				w,h = draw.textsize(txt, self.fntText)
				prev = 0
				for p in range(j):
					prev += aux[j][2]+wsp

				draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev, y+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)


	def drawLong(self, draw, x, y, lon, clr, nonHCs = True):
		if nonHCs and self.options.ayanamsha != 0:
			lon -= self.chart.ayanamsha
			lon = util.normalize(lon)

		d,m,s = util.decToDeg(lon)

		sign = d/chart.Chart.SIGN_DEG
		pos = d%chart.Chart.SIGN_DEG
		wsp,hsp = draw.textsize(' ', self.fntText)
		wsg,hsg = draw.textsize(self.signs[sign], self.fntMorinus)
		txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
		w,h = draw.textsize(txt, self.fntText)
		offset = (self.LONGITUDE_CELL_WIDTH-(w+wsp+wsg))/2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)
		draw.text((x+offset+w+wsp, y+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clr, font=self.fntMorinus)





