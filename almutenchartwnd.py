import wx
import os
import astrology
import planets
import chart
import houses
import fortune
import almutens
import common
import commonwnd
import Image, ImageDraw, ImageFont
import util
import mtexts


class AlmutenChartWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		#essentials
		self.ELINE_NUM = 5# +"Essential" +2(Shares and Scores)
		self.ELINE_HEIGHT = 2*self.LINE_HEIGHT
		self.ECOLUMN_NUM = 7# +leftmost +degreewins
		self.ESMALL_CELL_WIDTH = 5*self.FONT_SIZE
		self.ELONGITUDE_CELL_WIDTH = 7*self.FONT_SIZE
		self.DEGREEWINS_CELL_WIDTH = 7*self.FONT_SIZE
		self.ECELL_WIDTH = 7*self.FONT_SIZE
		self.ETITLE_HEIGHT = self.LINE_HEIGHT
		self.ETITLE_WIDTH = 10*self.FONT_SIZE
		self.ETABLE_WIDTH = (self.ESMALL_CELL_WIDTH+self.ELONGITUDE_CELL_WIDTH+(self.ECOLUMN_NUM)*(self.ECELL_WIDTH)+self.DEGREEWINS_CELL_WIDTH)
		self.ETABLE_HEIGHT = (2*self.ETITLE_HEIGHT+(self.ELINE_NUM*self.LINE_HEIGHT+2*self.ELINE_HEIGHT))

		if self.options.useaccidental:
			#accidentals
			self.ALINE_HEIGHT = 2*self.LINE_HEIGHT
			self.ATABLE_OFFSET = self.LINE_HEIGHT
			self.ACCIDENTAL_Y_OFFSET = self.LINE_HEIGHT/2
			self.ACCIDENTAL_X_OFFSET = self.FONT_SIZE
			self.ATITLE_HEIGHT = self.LINE_HEIGHT
			self.ATITLE_WIDTH = 10*self.FONT_SIZE
			self.ALINE_NUM = 1
			self.A1COLUMN_NUM = 7
			self.A2COLUMN_NUM = 3
			self.ASMALL_CELL_WIDTH = 6*self.FONT_SIZE
			self.ACELL_WIDTH = 3*self.FONT_SIZE
			self.ATABLE_WIDTH = (3*self.ACCIDENTAL_X_OFFSET+2*(self.ASMALL_CELL_WIDTH+(self.A1COLUMN_NUM)*(self.ACELL_WIDTH)))
			self.ATABLE_HEIGHT = (self.ATITLE_HEIGHT+3*self.ACCIDENTAL_Y_OFFSET+(2*(self.LINE_HEIGHT)+2*self.ALINE_HEIGHT))

			#Totals
			self.TLINE_NUM = 3
			self.TCOLUMN_NUM = 7
			self.TTABLE_HEIGHT = self.LINE_HEIGHT+3*self.ELINE_HEIGHT
			self.TTABLE_WIDTH = (self.ASMALL_CELL_WIDTH+(self.TCOLUMN_NUM)*(self.ACELL_WIDTH))
			self.TTABLE_OFFSET = self.LINE_HEIGHT

			self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.ETABLE_HEIGHT+self.ATABLE_OFFSET+self.ATABLE_HEIGHT+self.TTABLE_OFFSET+self.TTABLE_HEIGHT+commonwnd.CommonWnd.BORDER)
		else:
			self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.ETABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.ETABLE_WIDTH+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.fntLargeText = ImageFont.truetype(common.common.abc, 5*self.FONT_SIZE/4)
		self.fntBigText = ImageFont.truetype(common.common.abc, 3*self.FONT_SIZE/2)
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

		#Essentials
		x = BOR
		y = BOR
		draw.line((x, y, x+self.ETITLE_WIDTH, y), fill=tableclr)
		draw.line((x, y+self.ETITLE_HEIGHT, x, y), fill=tableclr)
		draw.line((x+self.ETITLE_WIDTH, y, x+self.ETITLE_WIDTH, y+self.ETITLE_HEIGHT), fill=tableclr)
		draw.rectangle(((x, y+self.ETITLE_HEIGHT), (x+self.ETABLE_WIDTH, y+self.ETABLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

		txt = mtexts.txts['Essential']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ETITLE_WIDTH-w)/2, y+(self.ETITLE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.ETITLE_HEIGHT+self.LINE_HEIGHT
		for i in range(self.ELINE_NUM+1):
			draw.line((x, y+i*self.LINE_HEIGHT, x+self.ETABLE_WIDTH, y+i*self.LINE_HEIGHT), fill=tableclr)
		draw.line((x, y+i*self.LINE_HEIGHT+self.ELINE_HEIGHT, x+self.ETABLE_WIDTH, y+i*self.LINE_HEIGHT+self.ELINE_HEIGHT), fill=tableclr)

		x = BOR+self.ESMALL_CELL_WIDTH
		y = BOR+self.ETITLE_HEIGHT
		draw.line((x, y, x, y+self.ETABLE_HEIGHT-self.ETITLE_HEIGHT), fill=tableclr)
		for i in range(self.ECOLUMN_NUM+1):
			draw.line((x+self.ELONGITUDE_CELL_WIDTH+i*self.ECELL_WIDTH, y, x+self.ELONGITUDE_CELL_WIDTH+i*self.ECELL_WIDTH, y+self.ETABLE_HEIGHT-self.ETITLE_HEIGHT), fill=tableclr)

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
			draw.text((x+self.ELONGITUDE_CELL_WIDTH+i*self.ECELL_WIDTH+(self.ECELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

		txt = mtexts.txts['DegreeWins']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+self.ELONGITUDE_CELL_WIDTH+7*self.ECELL_WIDTH+(self.DEGREEWINS_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+2*self.ETITLE_HEIGHT
		for i in range(astrology.SE_MOON+1):
			clr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			txt = common.common.Planets[i]
			w,h = draw.textsize(txt, self.fntMorinus)
			draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

			plon = self.chart.planets.planets[i].data[planets.Planet.LONG]
			self.drawLong(draw, x+self.ESMALL_CELL_WIDTH, y+i*self.LINE_HEIGHT, plon, clr)

		y += 2*self.LINE_HEIGHT
		txt = mtexts.txts['Asc']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		alon = self.chart.houses.ascmc[houses.Houses.ASC]
		self.drawLong(draw, x+self.ESMALL_CELL_WIDTH, y, alon, txtclr)

		clr = (0, 0, 0)
		if not self.bw:
			if self.options.useplanetcolors:
				clr = self.options.clrindividual[11]
			else:
				clr = self.options.clrperegrin
		y += self.LINE_HEIGHT
		txt = common.common.fortune
		w,h = draw.textsize(txt, self.fntMorinus)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

		flon = self.chart.fortune.fortune[fortune.Fortune.LON]
		self.drawLong(draw, x+self.ESMALL_CELL_WIDTH, y, flon, clr)

		y += self.LINE_HEIGHT
		txt = mtexts.txts['Syzygy']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		slon = self.chart.syzygy.lon
		self.drawLong(draw, x+self.ESMALL_CELL_WIDTH, y, slon, txtclr)

		y += self.LINE_HEIGHT
		txt = mtexts.txts['TotalShares1']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
		txt = mtexts.txts['TotalShares2']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		y += self.ELINE_HEIGHT
		txt = mtexts.txts['TotalScores1']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
		txt = mtexts.txts['TotalScores2']
		w,h = draw.textsize(txt, self.fntText)
		draw.text((x+(self.ESMALL_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		x = BOR+self.ESMALL_CELL_WIDTH+self.ELONGITUDE_CELL_WIDTH
		y = BOR+2*self.ETITLE_HEIGHT
		subnum = len(self.chart.almutens.essentials.essentials[0])
		for i in range(astrology.SE_SATURN+1):
			for j in range(subnum):
				txt = self.chart.almutens.essentials.essentials[i][j][0]
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+i*self.ECELL_WIDTH+(self.ECELL_WIDTH-w)/2, y+j*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		y = BOR+2*self.ETITLE_HEIGHT+5*self.LINE_HEIGHT
		for i in range(astrology.SE_SATURN+1):
			fnt = self.fntLargeText
			if self.chart.almutens.essentials.maxshare[0] != -1 and self.chart.almutens.essentials.maxshare[0] == i and (not self.chart.almutens.essentials.maxshare[2]):
				fnt = self.fntBigText
			txt = str(self.chart.almutens.essentials.shares[i])
			w,h = draw.textsize(txt, fnt)
			draw.text((x+i*self.ECELL_WIDTH+(self.ECELL_WIDTH-w)/2, y+(self.ELINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		y += self.ELINE_HEIGHT
		for i in range(astrology.SE_SATURN+1):
			fnt = self.fntLargeText
			if self.chart.almutens.essentials.maxscore[0] != -1 and self.chart.almutens.essentials.maxscore[0] == i and (not self.chart.almutens.essentials.maxscore[2]):
				fnt = self.fntBigText
			txt = str(self.chart.almutens.essentials.scores[i])
			w,h = draw.textsize(txt, fnt)
			draw.text((x+i*self.ECELL_WIDTH+(self.ECELL_WIDTH-w)/2, y+(self.ELINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		x = BOR+self.ESMALL_CELL_WIDTH+self.ELONGITUDE_CELL_WIDTH+7*self.ECELL_WIDTH
		y = BOR+2*self.ETITLE_HEIGHT
		num = len(self.chart.almutens.essentials.degwinner)
		for i in range(num):
			aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]#planetid, score, width
			subnum = len(self.chart.almutens.essentials.degwinner[0])
			mwidth = 0
			for j in range(subnum):
				pid = self.chart.almutens.essentials.degwinner[i][j][0]
				if pid != -1:
					ptxt = common.common.Planets[pid]
					wpl,hpl = draw.textsize(ptxt, self.fntMorinus)
					sco = self.chart.almutens.essentials.degwinner[i][0][1]
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

					draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), pltxt, fill=clr, font=self.fntMorinus)
					draw.text((x+(self.DEGREEWINS_CELL_WIDTH-(mwidth))/2+prev+wpl+wsp, y+i*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

		if self.options.useaccidental:
			#Accidentals
			x = BOR
			y = BOR+self.ETABLE_HEIGHT+self.LINE_HEIGHT
			draw.line((x, y, x+self.ATITLE_WIDTH, y), fill=tableclr)
			draw.line((x, y+self.ATITLE_HEIGHT, x, y), fill=tableclr)
			draw.line((x+self.ATITLE_WIDTH, y, x+self.ATITLE_WIDTH, y+self.ETITLE_HEIGHT), fill=tableclr)
			draw.rectangle(((x, y+self.ATITLE_HEIGHT), (x+self.ATABLE_WIDTH, y+self.ATABLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

			txt = mtexts.txts['Accidental']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ATITLE_WIDTH-w)/2, y+(self.ATITLE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			x += self.ACCIDENTAL_X_OFFSET
			y += self.ATITLE_HEIGHT+self.ACCIDENTAL_Y_OFFSET
			width = 7*self.ACELL_WIDTH
			draw.line((x+self.ASMALL_CELL_WIDTH, y, x+self.ASMALL_CELL_WIDTH+width, y), fill=tableclr)
			draw.line((x+self.ASMALL_CELL_WIDTH, y+self.LINE_HEIGHT, x+self.ASMALL_CELL_WIDTH, y), fill=tableclr)
			draw.line((x+self.ASMALL_CELL_WIDTH+width, y, x+self.ASMALL_CELL_WIDTH+width, y+self.LINE_HEIGHT), fill=tableclr)
			draw.rectangle(((x, y+self.LINE_HEIGHT), (x+self.ASMALL_CELL_WIDTH+width, y+3*self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

			for i in range(self.A1COLUMN_NUM+1):
				draw.line((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+self.LINE_HEIGHT, x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+3*self.LINE_HEIGHT), fill=tableclr)

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
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

				txt = str(self.chart.almutens.accidentals.inhouses[i])
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.ALINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			y += self.LINE_HEIGHT
			txt = mtexts.txts['HouseScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['HouseScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			yday = y-self.LINE_HEIGHT
			xday = x+self.ACCIDENTAL_X_OFFSET+self.ASMALL_CELL_WIDTH+(self.A1COLUMN_NUM)*(self.ACELL_WIDTH)

			y += self.ALINE_HEIGHT+self.ACCIDENTAL_Y_OFFSET
			width = 3*self.ACELL_WIDTH
			draw.line((x+self.ASMALL_CELL_WIDTH, y, x+self.ASMALL_CELL_WIDTH+width, y), fill=tableclr)
			draw.line((x+self.ASMALL_CELL_WIDTH, y+self.LINE_HEIGHT, x+self.ASMALL_CELL_WIDTH, y), fill=tableclr)
			draw.line((x+self.ASMALL_CELL_WIDTH+width, y, x+self.ASMALL_CELL_WIDTH+width, y+self.LINE_HEIGHT), fill=tableclr)
			draw.rectangle(((x, y+self.LINE_HEIGHT), (x+self.ASMALL_CELL_WIDTH+width, y+3*self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

			for i in range(self.A2COLUMN_NUM+1):
				draw.line((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+self.LINE_HEIGHT, x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+3*self.LINE_HEIGHT), fill=tableclr)

			for i in range(astrology.SE_MARS, astrology.SE_SATURN+1):
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[i]
					else:
						dign = self.chart.dignity(i)
						clr = self.clrs[dign]
				txt = common.common.Planets[i]
				w,h = draw.textsize(txt, self.fntMorinus)
				draw.text((x+self.ASMALL_CELL_WIDTH+(i-astrology.SE_MARS)*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

				txt = str(self.chart.almutens.accidentals.inphases[i-astrology.SE_MARS])
				w,h = draw.textsize(txt, self.fntText)
				draw.text((x+self.ASMALL_CELL_WIDTH+(i-astrology.SE_MARS)*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.ALINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			#day/hour
			width = 7*self.ACELL_WIDTH
			draw.line((xday+self.ASMALL_CELL_WIDTH, yday, xday+self.ASMALL_CELL_WIDTH+width, yday), fill=tableclr)
			draw.line((xday+self.ASMALL_CELL_WIDTH, yday+self.LINE_HEIGHT, xday+self.ASMALL_CELL_WIDTH, yday), fill=tableclr)
			draw.line((xday+self.ASMALL_CELL_WIDTH+width, yday, xday+self.ASMALL_CELL_WIDTH+width, yday+self.LINE_HEIGHT), fill=tableclr)
			draw.rectangle(((xday, yday+self.LINE_HEIGHT), (xday+self.ASMALL_CELL_WIDTH+width, yday+3*self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
			for i in range(self.A1COLUMN_NUM+1):
				draw.line((xday+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, yday+self.LINE_HEIGHT, xday+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, yday+3*self.LINE_HEIGHT), fill=tableclr)

			txt = mtexts.txts['DayRulerScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((xday+(self.ASMALL_CELL_WIDTH-w)/2, yday+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['DayRulerScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((xday+(self.ASMALL_CELL_WIDTH-w)/2, yday+2*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

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
				draw.text((xday+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, yday+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

				txt = str(self.chart.almutens.accidentals.dayruler[i])
				w,h = draw.textsize(txt, self.fntText)
				draw.text((xday+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, yday+self.LINE_HEIGHT+(self.ALINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			yhour = yday+3*self.LINE_HEIGHT+self.ACCIDENTAL_Y_OFFSET
			xhour = xday

			width = 7*self.ACELL_WIDTH
			draw.line((xhour+self.ASMALL_CELL_WIDTH, yhour, xhour+self.ASMALL_CELL_WIDTH+width, yhour), fill=tableclr)
			draw.line((xhour+self.ASMALL_CELL_WIDTH, yhour+self.LINE_HEIGHT, xhour+self.ASMALL_CELL_WIDTH, yhour), fill=tableclr)
			draw.line((xhour+self.ASMALL_CELL_WIDTH+width, yhour, xhour+self.ASMALL_CELL_WIDTH+width, yhour+self.LINE_HEIGHT), fill=tableclr)
			draw.rectangle(((xhour, yhour+self.LINE_HEIGHT), (xhour+self.ASMALL_CELL_WIDTH+width, yhour+3*self.LINE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
			for i in range(self.A1COLUMN_NUM+1):
				draw.line((xhour+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, yhour+self.LINE_HEIGHT, xhour+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, yhour+3*self.LINE_HEIGHT), fill=tableclr)

			txt = mtexts.txts['HourRulerScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((xhour+(self.ASMALL_CELL_WIDTH-w)/2, yhour+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['HourRulerScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((xhour+(self.ASMALL_CELL_WIDTH-w)/2, yhour+2*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

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
				draw.text((xhour+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, yhour+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

				txt = str(self.chart.almutens.accidentals.hourruler[i])
				w,h = draw.textsize(txt, self.fntText)
				draw.text((xhour+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, yhour+self.LINE_HEIGHT+(self.ALINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			y += self.LINE_HEIGHT

			txt = mtexts.txts['PhaseScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			txt = mtexts.txts['PhaseScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			#Totals
			x = BOR
			y = BOR+self.ETABLE_HEIGHT+self.ATABLE_OFFSET+self.ATABLE_HEIGHT+self.TTABLE_OFFSET
			width = 7*self.ACELL_WIDTH
			draw.rectangle(((x, y), (x+self.ASMALL_CELL_WIDTH+width, y+self.TTABLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
			for i in range(self.A1COLUMN_NUM+1):
				if i == 0:
					draw.line((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y, x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+self.LINE_HEIGHT+3*self.ELINE_HEIGHT), fill=tableclr)
				draw.line((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+self.LINE_HEIGHT, x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH, y+self.LINE_HEIGHT+3*self.ELINE_HEIGHT), fill=tableclr)
			for i in range(self.TLINE_NUM+1):
				draw.line((x, y-self.LINE_HEIGHT+i*self.ELINE_HEIGHT, x+self.TTABLE_WIDTH, y-self.LINE_HEIGHT+i*self.ELINE_HEIGHT), fill=tableclr)

			txt = mtexts.txts['Total']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['EssentialScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			txt = mtexts.txts['EssentialScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+2*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['AccidentalScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+3*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			txt = mtexts.txts['AccidentalScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+4*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

			txt = mtexts.txts['GrandScores1']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+5*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)
			txt = mtexts.txts['GrandScores2']
			w,h = draw.textsize(txt, self.fntText)
			draw.text((x+(self.ASMALL_CELL_WIDTH-w)/2, y+6*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=self.fntText)

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
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntMorinus)

				fnt = self.fntLargeText

				txt = str(self.chart.almutens.essentials.scores[i])
				w,h = draw.textsize(txt, fnt)
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+self.LINE_HEIGHT+(self.ELINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

				txt = str(self.chart.almutens.accidentals.scores[i])
				w,h = draw.textsize(txt, fnt)
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+3*self.LINE_HEIGHT+(self.ELINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

				if i == self.chart.almutens.maxscore[0] and (not self.chart.almutens.maxscore[2]):
					fnt = self.fntBigText

				txt = str(self.chart.almutens.scores[i])
				w,h = draw.textsize(txt, fnt)
				draw.text((x+self.ASMALL_CELL_WIDTH+i*self.ACELL_WIDTH+(self.ACELL_WIDTH-w)/2, y+5*self.LINE_HEIGHT+(self.ELINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		wxImg = wx.EmptyImage(img.size[0], img.size[1])
		wxImg.SetData(img.tostring())
		self.buffer = wx.BitmapFromImage(wxImg)


	def drawLong(self, draw, x, y, lon, clr):
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
		offset = (self.ELONGITUDE_CELL_WIDTH-(w+wsp+wsg))/2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=clr, font=self.fntText)
		draw.text((x+offset+w+wsp, y+(self.LINE_HEIGHT-hsg)/2), self.signs[sign], fill=clr, font=self.fntMorinus)



